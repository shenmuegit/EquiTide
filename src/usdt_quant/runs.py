from __future__ import annotations

import argparse
from decimal import Decimal
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
from typing import Any

from usdt_quant.records import Records


DECIMAL_FIELDS = {
    "initial_spot_usdt",
    "initial_perp_usdt",
    "target_spot_base",
    "spot_taker_fee",
    "perp_taker_fee",
    "execution_bps_per_leg",
    "buffer_usdt",
    "future_basis_change_prediction",
}
RESEARCH_FIELDS = {
    "train_end_ns",
    "validation_end_ns",
    "ridge_alpha",
    "logistic_c",
    "seed",
    "bootstrap_samples",
}
OPTIONAL_RESEARCH_FIELDS = {"entry_analysis_ns"}


def _inside(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"path is outside data root: {path}")
    return resolved


def _watch_worker(records: Records, task_id: str, run_id: int, process: subprocess.Popen[Any]) -> None:
    exit_code = process.wait()
    records.finish(
        task_id,
        run_id,
        error=f"worker exited with code {exit_code} before recording completion",
        exit_code=exit_code,
    )


def launch_task(records: Records, task_id: str) -> None:
    run_id = records.create_run(task_id)
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    try:
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "usdt_quant.runs",
                "worker",
                "--task-id",
                task_id,
                "--run-id",
                str(run_id),
            ],
            env=os.environ.copy(),
            shell=False,
            creationflags=creationflags,
        )
        records.mark_spawned(task_id, run_id, process.pid)
        threading.Thread(
            target=_watch_worker,
            args=(records, task_id, run_id, process),
            daemon=True,
            name=f"task-{task_id[:8]}",
        ).start()
    except OSError as error:
        records.fail_launch(task_id, run_id, f"{type(error).__name__}: {error}")
        raise


def launch_backtest(records: Records, task_id: str) -> None:
    launch_task(records, task_id)


def _process_alive(pid: int | None) -> bool:
    if not pid or pid <= 0:
        return False
    if os.name == "nt":
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            shell=False,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return result.returncode == 0 and f'"{pid}"' in result.stdout
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    stat = Path(f"/proc/{pid}/stat")
    if stat.is_file():
        try:
            if stat.read_text(encoding="utf-8").split()[2] == "Z":
                return False
        except (OSError, IndexError):
            pass
    return True


def _watch_pid(records: Records, task_id: str, run_id: int, pid: int) -> None:
    while _process_alive(pid):
        time.sleep(0.25)
    records.finish(
        task_id,
        run_id,
        error=f"worker process {pid} exited before recording completion",
        exit_code=-1,
    )


def reconcile_active(records: Records) -> int:
    failed = records.fail_queued_without_run()
    for run in records.active_runs():
        if _process_alive(run["pid"]):
            threading.Thread(
                target=_watch_pid,
                args=(records, run["task_id"], run["run_id"], run["pid"]),
                daemon=True,
                name=f"recovered-task-{run['task_id'][:8]}",
            ).start()
            continue
        if records.finish(
            run["task_id"],
            run["run_id"],
            error="worker process was not running when the API started",
            exit_code=-1,
        ):
            failed += 1
    return failed


def _config(values: dict[str, Any]):
    from usdt_quant.strategy import BacktestConfig

    parsed = {
        key: Decimal(str(value)) if key in DECIMAL_FIELDS else value
        for key, value in values.items()
    }
    return BacktestConfig(**parsed)


def _research_config(values: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(RESEARCH_FIELDS - values.keys())
    if missing:
        raise ValueError(f"missing research config fields: {', '.join(missing)}")
    for key in ("train_end_ns", "validation_end_ns", "seed", "bootstrap_samples"):
        if type(values[key]) is not int:
            raise ValueError(f"{key} must be an integer")
    if "entry_analysis_ns" in values and type(values["entry_analysis_ns"]) is not int:
        raise ValueError("entry_analysis_ns must be an integer")
    for key in ("ridge_alpha", "logistic_c"):
        number = Decimal(str(values[key]))
        if not number.is_finite() or number <= 0:
            raise ValueError(f"{key} must be a finite positive number")
    if not 1 <= values["bootstrap_samples"] <= 10_000:
        raise ValueError("bootstrap_samples must be between 1 and 10000")
    if values["seed"] < 0:
        raise ValueError("seed must be non-negative")
    backtest = _config({
        key: value for key, value in values.items()
        if key not in RESEARCH_FIELDS | OPTIONAL_RESEARCH_FIELDS
    })
    if not backtest.start_ns < values["train_end_ns"] < values["validation_end_ns"] < backtest.end_ns:
        raise ValueError("split must satisfy start_ns < train_end_ns < validation_end_ns < end_ns")
    if backtest.holding_period_ns != 24 * 60 * 60 * 1_000_000_000:
        raise ValueError("research holding_period_ns must be 24 hours")
    entry = values.get("entry_analysis_ns")
    if entry is not None:
        if not values["validation_end_ns"] <= entry <= backtest.end_ns - backtest.holding_period_ns:
            raise ValueError("entry_analysis_ns must be inside the test range with a full holding period")
        if (entry - values["validation_end_ns"]) % backtest.decision_interval_ns:
            raise ValueError("entry_analysis_ns must match the registered decision grid")
    return {
        **backtest.as_json(),
        **{key: values[key] for key in RESEARCH_FIELDS},
        **({"entry_analysis_ns": entry} if entry is not None else {}),
    }


def work(task_id: str, run_id: int) -> int:
    database_url = os.environ["DATABASE_URL"]
    data_root = Path(os.environ.get("USDT_QUANT_DATA_ROOT", "data")).resolve()
    records = Records(database_url)
    records.mark_running(task_id, run_id, os.getpid())
    try:
        task = records.task(task_id)
        if task is None:
            raise ValueError(f"task not found: {task_id}")
        dataset_dir = _inside(Path(task["dataset_dir"]), data_root)
        if task["kind"] == "backtest":
            output_dir = _inside(data_root / "runs" / task_id, data_root)
            from usdt_quant.backtest import BacktestData, run_backtest

            report = run_backtest(
                _config(task["config"]),
                BacktestData.from_parquet(dataset_dir),
                output_dir,
            )
            report_path = output_dir / "summary.json"
        elif task["kind"] == "research":
            output_dir = _inside(data_root / "research" / task_id, data_root)
            from usdt_quant.research import run_research

            report = run_research(task["config"], dataset_dir, output_dir)
            report_path = output_dir / "report.json"
        else:
            raise ValueError(f"unsupported task kind: {task['kind']}")
        if not report_path.is_file():
            raise RuntimeError(f"task did not write {report_path.name}")
        if report.get("config", {}).get("data_version") != task["data_version"]:
            raise RuntimeError("report data_version does not match task")
        records.finish(task_id, run_id, result_path=report_path)
        return 0
    except Exception as error:
        message = f"{type(error).__name__}: {error}"
        records.finish(task_id, run_id, error=message, exit_code=1)
        print(message, file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="USDT research and backtest process runner")
    subparsers = parser.add_subparsers(dest="command", required=True)
    worker = subparsers.add_parser("worker")
    worker.add_argument("--task-id", required=True)
    worker.add_argument("--run-id", required=True, type=int)
    args = parser.parse_args(argv)
    raise SystemExit(work(args.task_id, args.run_id))


if __name__ == "__main__":
    main()
