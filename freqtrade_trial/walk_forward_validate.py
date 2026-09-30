"""Walk-forward test of the existing indicator strategies."""

import argparse
import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents/skills/walk-forward-validation/scripts"))
from walk_forward import WalkForwardConfig, WalkForwardValidator  # noqa: E402


CANDIDATES = ("EmaCross", "RsiOversold", "BollingerRevert")
BAR = pd.Timedelta(minutes=15)


def backtest(
    start: pd.Timestamp, end: pd.Timestamp, fold: int, segment: str,
    pair: str, data_dir: Path, run_dir: Path,
) -> dict:
    output = run_dir / f"{fold:02d}_{segment}"
    output.mkdir(parents=True, exist_ok=True)
    command = [
        str(ROOT / "Freqtrade/.venv/Scripts/freqtrade.exe"),
        "backtesting",
        "--userdir", str(ROOT / "freqtrade_trial"),
        "--config", str(ROOT / "freqtrade_trial/config.json"),
        "--datadir", str(data_dir),
        "--strategy-path", str(ROOT / "freqtrade_trial"),
        "--strategy-list", *CANDIDATES,
        "--pairs", pair,
        "--timeframe", "15m",
        "--data-format-ohlcv", "parquet",
        "--timerange", f"{start:%Y%m%dT%H%M}-{end:%Y%m%dT%H%M}",
        "--fee", "0.001",
        "--cache", "none",
        "--export", "trades",
        "--backtest-directory", str(output),
        "--no-color",
    ]
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, errors="replace")
    if run.returncode:
        raise RuntimeError(f"Fold {fold} {segment} failed:\n{run.stdout[-4000:]}\n{run.stderr[-4000:]}")

    archive = max(output.glob("*.zip"), key=lambda path: path.stat().st_mtime)
    with ZipFile(archive) as saved:
        strategies = json.loads(saved.read(f"{archive.stem}.json"))["strategy"]
    for name in CANDIDATES:
        result = strategies[name]
        assert pd.Timestamp(result["backtest_start"], tz="UTC") == start
        assert pd.Timestamp(result["backtest_end"], tz="UTC") == end
    return {
        name: {
            "return": strategies[name]["profit_total"],
            "trades": strategies[name]["total_trades"],
            "max_drawdown": strategies[name]["max_drawdown_account"],
        }
        for name in CANDIDATES
    }


def compounded(returns: list[float]) -> float:
    return math.prod(1 + value for value in returns) - 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", default="BTC/USDT")
    parser.add_argument("--data-dir", default="freqtrade_trial/data/binance")
    parser.add_argument("--start", default="2026-07-18")
    parser.add_argument("--end", default="2026-09-16")
    parser.add_argument("--train-days", type=int, default=14)
    parser.add_argument("--test-days", type=int, default=3)
    parser.add_argument("--report", default="freqtrade_trial/results/walk_forward_2026-09-29.json")
    args = parser.parse_args()
    data_dir = ROOT / args.data_dir
    report_path = ROOT / args.report
    run_dir = ROOT / "data/runs/walk_forward_extended/backtests" / f"{args.pair.replace('/', '_')}_{args.train_days}_{args.test_days}"
    start = pd.Timestamp(args.start, tz="UTC")
    end = pd.Timestamp(args.end, tz="UTC")
    pair_filename = args.pair.replace("/", "_") + "-15m.parquet"
    candles = pd.read_parquet(data_dir / pair_filename)
    candles = candles.loc[(candles["date"] >= start) & (candles["date"] < end)].reset_index(drop=True)
    assert candles["date"].iloc[0] == start and candles["date"].iloc[-1] + BAR == end
    assert (candles["date"].diff().dropna() == BAR).all()
    # The first 200 candles warm up Freqtrade indicators before the first train fold.
    dates = candles["date"].iloc[200:].reset_index(drop=True)
    config = WalkForwardConfig(
        train_size=args.train_days * 96,
        test_size=args.test_days * 96,
        step_size=args.test_days * 96,
        window_type="rolling",
        purge_size=0,  # These strategies have no forward-return labels.
        embargo_size=48,
    )
    rows = []
    for fold in WalkForwardValidator(config).split(len(dates), pd.DatetimeIndex(dates)):
        train_start = dates.iloc[fold.train_indices[0]]
        train_end = dates.iloc[fold.train_indices[-1]] + BAR
        test_start = dates.iloc[fold.test_indices[0]]
        test_end = dates.iloc[fold.test_indices[-1]] + BAR
        assert train_end + 48 * BAR == test_start
        if rows:
            assert pd.Timestamp(rows[-1]["test_end"]) == test_start

        print(f"Fold {fold.fold_idx + 1}: {train_start} -> {test_end}", flush=True)
        train = backtest(train_start, train_end, fold.fold_idx, "train", args.pair, data_dir, run_dir)
        selected = max(CANDIDATES, key=lambda name: train[name]["return"])
        test = backtest(test_start, test_end, fold.fold_idx, "test", args.pair, data_dir, run_dir)
        rows.append({
            "fold": fold.fold_idx + 1,
            "train_start": train_start.isoformat(),
            "train_end": train_end.isoformat(),
            "test_start": test_start.isoformat(),
            "test_end": test_end.isoformat(),
            "train": train,
            "selected": selected,
            "test": test,
        })
        print(f"  selected={selected} train={train[selected]['return']:.2%} test={test[selected]['return']:.2%}", flush=True)

    chosen = [row["test"][row["selected"]]["return"] for row in rows]
    ema = [row["test"]["EmaCross"]["return"] for row in rows]
    report = {
        "data": f"{args.pair} Binance spot, 15m, {start.date()} through {(end - BAR).date()} UTC",
        "method": f"{args.train_days}d rolling train, 12h embargo, {args.test_days}d test/step; select the highest train net return among three fixed indicator strategies",
        "fee_per_side": 0.001,
        "selection_test_compounded_return": compounded(chosen),
        "fixed_ema_test_compounded_return": compounded(ema),
        "selection_positive_folds": sum(value > 0 for value in chosen),
        "selection_total_trades": sum(row["test"][row["selected"]]["trades"] for row in rows),
        "selection_largest_fold_drawdown": max(row["test"][row["selected"]]["max_drawdown"] for row in rows),
        "selected_counts": dict(Counter(row["selected"] for row in rows)),
        "folds": rows,
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {report_path}")
    print(f"Selected OOS: {report['selection_test_compounded_return']:.2%}; fixed EMA OOS: {report['fixed_ema_test_compounded_return']:.2%}")


if __name__ == "__main__":
    main()
