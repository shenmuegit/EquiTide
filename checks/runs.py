"""Real HTTP + PostgreSQL + child-process check for task 4."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import shutil
from tempfile import TemporaryDirectory
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import polars as pl
import psycopg

from usdt_quant.records import Records
from usdt_quant.runs import _process_alive, _watch_worker, reconcile_active


ROOT = Path(__file__).resolve().parents[1]
SECOND = 1_000_000_000
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
START = 1_704_067_200 * SECOND


def _write_dataset(root: Path, version: str, *, broken: bool = False) -> Path:
    directory = root / "normalized" / "binance" / "BTC" / version
    directory.mkdir(parents=True)
    times = [START + index * MINUTE for index in range(481)]
    for name, offset in (("spot_bars", 0), ("perp_bars", 1), ("mark_bars", 1)):
        close_times = [value + (SECOND if broken and name == "mark_bars" else 0) for value in times]
        pl.DataFrame({
            "close_ts": close_times,
            "available_ts": close_times,
            "close": [str(100 + offset + index / 100) for index in range(len(times))],
            "is_closed": [True] * len(times),
        }).write_parquet(directory / f"{name}.parquet")
    settlements = [START - (21 - index) * 4 * HOUR for index in range(21)]
    settlements.append(START + 4 * HOUR)
    pl.DataFrame({
        "settlement_ts": settlements,
        "available_ts": [value + SECOND for value in settlements],
        "realized_rate": ["0.002"] * 21 + ["-0.001"],
        "mark_price_at_settlement": ["100"] * 21 + ["103"],
        "actual_interval_hours": ["4"] * 22,
    }).write_parquet(directory / "funding_settlement.parquet")
    for name in ("spot_instrument_meta", "perp_instrument_meta"):
        pl.DataFrame({
            "contract_multiplier": ["1"],
            "lot_size": ["0.001"],
            "tick_size": ["0.01"],
            "effective_from": [0],
        }).write_parquet(directory / f"{name}.parquet")

    datasets = []
    for path in sorted(directory.glob("*.parquet")):
        rows = pl.read_parquet(path).height
        datasets.append({
            "dataset": path.stem,
            "status": "ok",
            "rows": rows,
            "actual_start_ts": times[0],
            "actual_end_ts": times[-1],
            "raw_path": str(root / "raw" / path.with_suffix(".jsonl").name),
            "parquet_path": str(path),
            "source_time_unit": "ms",
            "normalized_time_unit": "ns",
            "quality": {"ok": rows},
            "error": None,
        })
    coverage = {
        "data_version": version,
        "exchange": "binance",
        "base": "BTC",
        "requested_start": datetime.fromtimestamp(START / SECOND, timezone.utc).isoformat(),
        "requested_end_exclusive": datetime.fromtimestamp((START + 8 * HOUR) / SECOND, timezone.utc).isoformat(),
        "generated_ts": time.time_ns(),
        "raw_time_unit": "milliseconds",
        "normalized_time_unit": "nanoseconds",
        "historical_receive_ts": None,
        "rule_effective_time": "check fixture",
        "datasets": datasets,
        "known_unavailable": {},
    }
    coverage_dir = root / "coverage"
    coverage_dir.mkdir(parents=True, exist_ok=True)
    (coverage_dir / f"binance_BTC_{version}.json").write_text(
        json.dumps(coverage), encoding="utf-8",
    )
    return directory


def _port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


def _request(base: str, path: str, body: dict | None = None):
    data = json.dumps(body).encode() if body is not None else None
    request = Request(
        base + path,
        data=data,
        method="POST" if body is not None else "GET",
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=5) as response:
        return response.status, json.loads(response.read())


def _request_error(base: str, path: str, body: dict | None = None) -> tuple[int, dict]:
    try:
        _request(base, path, body)
    except HTTPError as error:
        return error.code, json.loads(error.read())
    raise AssertionError("request unexpectedly succeeded")


def _wait_api(base: str) -> None:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        try:
            _request(base, "/api/coverage")
            return
        except (URLError, ConnectionError):
            time.sleep(0.1)
    raise AssertionError("API did not start")


def _wait_task(base: str, task_id: str) -> dict:
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        _, task = _request(base, f"/api/tasks/{task_id}")
        if task["status"] in {"succeeded", "failed"}:
            return task
        time.sleep(0.2)
    raise AssertionError(f"task remained active: {task_id}")


def _config() -> dict:
    return {
        "baseline": "B0",
        "start_ns": START,
        "end_ns": START + 8 * HOUR,
        "decision_interval_ns": HOUR,
        "holding_period_ns": 8 * HOUR,
        "funding_window": 21,
        "initial_spot_usdt": "10000",
        "initial_perp_usdt": "10000",
        "target_spot_base": "12",
        "spot_taker_fee": "0.001",
        "perp_taker_fee": "0.0002",
        "execution_bps_per_leg": "5",
        "buffer_usdt": "1",
    }


def _cleanup(database_url: str) -> None:
    with psycopg.connect(database_url) as connection:
        config_ids = connection.execute(
            """DELETE FROM tasks
               WHERE data_version IN ('check-success', 'check-failure', 'check-monitor', 'check-restart', 'check-restart-live', 'check-no-run')
               RETURNING strategy_config_id""",
        ).fetchall()
        if config_ids:
            connection.execute(
                "DELETE FROM strategy_configs WHERE id = ANY(%s)",
                ([row[0] for row in config_ids],),
            )


def _cleanup_research(database_url: str, task_id: str) -> None:
    with psycopg.connect(database_url) as connection:
        row = connection.execute(
            """
            SELECT strategy_config_id FROM tasks
            WHERE id=%s AND kind='research'
            """,
            (task_id,),
        ).fetchone()
        if row is None:
            return
        connection.execute("DELETE FROM experiments WHERE id=%s", (task_id,))
        connection.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        connection.execute(
            "DELETE FROM strategy_configs WHERE id=%s",
            (row[0],),
        )
    research_root = (ROOT / "data" / "research").resolve()
    output_dir = (research_root / task_id).resolve()
    if output_dir.is_relative_to(research_root):
        shutil.rmtree(output_dir, ignore_errors=True)


def _automatic_request_check() -> None:
    from unittest.mock import patch

    from usdt_quant.api import _automatic_research_request

    def coverage(version: str, generated_ts: int, *, start_ns: int = START,
                 missing_minutes: int = 0, funding_quality: dict | None = None) -> dict:
        datasets = [
            {"dataset": name, "missing_closed_minutes": missing_minutes if name == "mark_bars" else 0}
            for name in ("spot_bars", "perp_bars", "mark_bars")
        ]
        datasets.extend([
            {"dataset": "funding_settlement", "quality": funding_quality or {}},
            {"dataset": "spot_instrument_meta"},
            {"dataset": "perp_instrument_meta"},
        ])
        return {
            "data_version": version,
            "requested_start": datetime.fromtimestamp(start_ns / SECOND, timezone.utc).isoformat(),
            "requested_end_exclusive": datetime.fromtimestamp((start_ns + 60 * 24 * HOUR) / SECOND, timezone.utc).isoformat(),
            "generated_ts": generated_ts,
            "datasets": datasets,
        }

    entry_ns = START + 43 * 24 * HOUR + 6 * HOUR
    reports = [
        coverage("missing-rate", 5, funding_quality={"missing_realized_rate": 1}),
        coverage("off-grid", 4, start_ns=START + 30 * MINUTE),
        coverage("missing-minute", 3, missing_minutes=1),
        coverage("missing-mark", 2, funding_quality={"missing_mark_price_at_settlement": 1}),
        coverage("valid", 1),
    ]
    with patch("usdt_quant.api._coverage", return_value=reports), \
         patch("usdt_quant.api._dataset", return_value=Path(".")):
        request = _automatic_research_request(entry_ns, Path("."))
    assert request.data_version == "valid"


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is required")
    _automatic_request_check()
    _cleanup(database_url)
    records = Records(database_url)
    records.initialize()
    exited = subprocess.Popen([sys.executable, "-c", "import os, time; time.sleep(0.05); os._exit(9)"])
    time.sleep(0.15)
    assert not _process_alive(exited.pid)
    exited.wait()
    dead = records.create_backtest(
        config=_config(), dependency_versions={}, data_version="check-monitor",
        dataset_dir=ROOT / "data",
    )
    dead_run = records.create_run(dead["id"])
    process = subprocess.Popen([sys.executable, "-c", "import os; os._exit(7)"])
    records.mark_spawned(dead["id"], dead_run, process.pid)
    _watch_worker(records, dead["id"], dead_run, process)
    assert records.task(dead["id"])["status"] == "failed"
    assert "worker exited with code 7" in records.task(dead["id"])["error"]

    orphan = records.create_backtest(
        config=_config(), dependency_versions={}, data_version="check-no-run",
        dataset_dir=ROOT / "data",
    )
    assert reconcile_active(records) == 1
    assert records.task(orphan["id"])["status"] == "failed"

    stale = records.create_backtest(
        config=_config(), dependency_versions={}, data_version="check-restart",
        dataset_dir=ROOT / "data",
    )
    stale_run = records.create_run(stale["id"])
    records.mark_spawned(stale["id"], stale_run, 2_147_483_647)
    assert reconcile_active(records) == 1
    assert records.task(stale["id"])["status"] == "failed"

    late = records.create_backtest(
        config=_config(), dependency_versions={}, data_version="check-restart-live",
        dataset_dir=ROOT / "data",
    )
    late_run = records.create_run(late["id"])
    late_process = subprocess.Popen([sys.executable, "-c", "import time, os; time.sleep(0.4); os._exit(9)"])
    records.mark_spawned(late["id"], late_run, late_process.pid)
    assert reconcile_active(records) == 0
    deadline = time.monotonic() + 3
    while records.task(late["id"])["status"] != "failed" and time.monotonic() < deadline:
        time.sleep(0.1)
    assert records.task(late["id"])["status"] == "failed"
    with TemporaryDirectory(prefix="usdt-quant-runs-") as temp:
        data_root = Path(temp)
        _write_dataset(data_root, "check-success")
        _write_dataset(data_root, "check-failure", broken=True)
        with psycopg.connect(database_url) as connection:
            connection.execute((ROOT / "sql" / "001_initial.sql").read_text(encoding="utf-8"))

        port = _port()
        base = f"http://127.0.0.1:{port}"
        environment = {
            **os.environ,
            "DATABASE_URL": database_url,
            "USDT_QUANT_DATA_ROOT": str(data_root),
        }
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "usdt_quant.api:app", "--host", "127.0.0.1", "--port", str(port), "--log-level", "error"],
            cwd=ROOT,
            env=environment,
            shell=False,
            creationflags=creationflags,
        )
        try:
            _wait_api(base)
            _, reports = _request(base, "/api/coverage")
            assert {item["data_version"] for item in reports} >= {"check-success", "check-failure"}

            invalid_decimal = _config()
            invalid_decimal["initial_spot_usdt"] = "NaN"
            assert _request_error(base, "/api/backtests", {
                "data_version": "check-success", "config": invalid_decimal,
            })[0] == 422
            invalid_decimal["initial_spot_usdt"] = "Infinity"
            assert _request_error(base, "/api/backtests", {
                "data_version": "check-success", "config": invalid_decimal,
            })[0] == 422
            invalid_integer = _config()
            invalid_integer["start_ns"] = 1.5
            assert _request_error(base, "/api/backtests", {
                "data_version": "check-success", "config": invalid_integer,
            })[0] == 422

            started = time.monotonic()
            status, success = _request(base, "/api/backtests", {
                "data_version": "check-success", "config": _config(),
            })
            submit_seconds = time.monotonic() - started
            assert status == 202
            assert submit_seconds < 3, f"POST waited for computation: {submit_seconds:.2f}s"
            ping_started = time.monotonic()
            _request(base, "/api/coverage")
            assert time.monotonic() - ping_started < 1, "API blocked while worker was active"

            _, failure = _request(base, "/api/backtests", {
                "data_version": "check-failure", "config": _config(),
            })
            success = _wait_task(base, success["id"])
            failure = _wait_task(base, failure["id"])
            assert success["status"] == "succeeded", success
            assert failure["status"] == "failed", failure
            assert "no shared closed spot/perp/mark bars" in failure["error"]

            _, report = _request(base, f"/api/tasks/{success['id']}/report")
            assert report["config"]["data_version"] == "check-success"
            assert report["summary"]["fill_count"] == 4
            _, fills = _request(base, f"/api/tasks/{success['id']}/artifacts/fills")
            assert len(fills) == 4
            _, equity = _request(base, f"/api/tasks/{success['id']}/artifacts/equity")
            assert equity == [json.loads(line) for line in
                              (Path(success["result_path"]).parent / "equity.jsonl").read_text(encoding="utf-8").splitlines() if line]
            assert _request_error(base, f"/api/tasks/{success['id']}/artifacts/equity?baseline=B0")[0] == 422

            _, reread = _request(base, "/api/tasks")
            assert {success["id"], failure["id"]} <= {item["id"] for item in reread}
            with psycopg.connect(database_url) as connection:
                stored = connection.execute(
                    "SELECT status, data_version FROM tasks WHERE id=%s",
                    (success["id"],),
                ).fetchone()
            assert stored == ("succeeded", "check-success")
        finally:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)

    _cleanup(database_url)

    expected_research_config = json.loads(
        (ROOT / "data" / "research" / "binance_btc_60d" / "config.json").read_text(encoding="utf-8")
    )
    research_version = expected_research_config["data_version"]
    research_config = {
        key: value for key, value in expected_research_config.items() if key != "data_version"
    }
    with TemporaryDirectory(prefix="usdt-quant-research-", dir=ROOT) as research_directory:
        research_root = Path(research_directory)
        coverage = json.loads(
            (ROOT / "data" / "coverage" / f"{research_version}.json").read_text(encoding="utf-8")
        )
        source_dataset = (ROOT / next(
            Path(item["parquet_path"])
            for item in coverage["datasets"]
            if item.get("parquet_path")
        )).resolve().parent
        isolated_dataset = research_root / "normalized" / coverage["exchange"] / coverage["base"] / research_version
        shutil.copytree(source_dataset, isolated_dataset)
        for item in coverage["datasets"]:
            if item.get("parquet_path"):
                item["parquet_path"] = str(isolated_dataset / Path(item["parquet_path"]).name)
        (research_root / "coverage").mkdir()
        (research_root / "coverage" / f"{research_version}.json").write_text(
            json.dumps(coverage), encoding="utf-8",
        )
        port = _port()
        base = f"http://127.0.0.1:{port}"
        environment = {
            **os.environ,
            "DATABASE_URL": database_url,
            "USDT_QUANT_DATA_ROOT": str(research_root),
        }
        server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "usdt_quant.api:app", "--host", "127.0.0.1", "--port", str(port), "--log-level", "error"],
            cwd=ROOT,
            env=environment,
            shell=False,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        research_id: str | None = None
        try:
            _wait_api(base)
            invalid_research = {**research_config, "seed": -1}
            assert _request_error(base, "/api/research", {
                "data_version": research_version,
                "config": invalid_research,
            })[0] == 422
            entry_ns = expected_research_config["validation_end_ns"] + 6 * HOUR
            assert _request_error(base, "/api/entry-analyses", {"entry_ns": -1})[0] == 422
            assert _request_error(base, "/api/entry-analyses", {"entry_ns": 1.5})[0] == 422
            assert _request_error(base, "/api/entry-analyses", {"entry_ns": entry_ns + 1})[0] == 422
            assert _request_error(base, "/api/entry-analyses", {
                "entry_ns": expected_research_config["validation_end_ns"] - HOUR,
            })[0] == 422
            assert _request_error(base, "/api/entry-analyses", {
                "entry_ns": entry_ns,
                "data_version": research_version,
            })[0] == 422
            started = time.monotonic()
            status, research = _request(base, "/api/entry-analyses", {"entry_ns": entry_ns})
            research_id = research["id"]
            assert status == 202
            assert time.monotonic() - started < 3
            assert research["data_version"] == research_version
            assert research["config"]["start_ns"] == expected_research_config["start_ns"]
            assert research["config"]["train_end_ns"] == expected_research_config["train_end_ns"]
            assert research["config"]["validation_end_ns"] == expected_research_config["validation_end_ns"]
            assert research["config"]["entry_analysis_ns"] == entry_ns
            assert research["config"]["seed"] == 20260916
            assert research["config"]["bootstrap_samples"] == 200
            _request(base, "/api/coverage")
            research = _wait_task(base, research["id"])
            assert research["status"] == "succeeded", research
            _, report = _request(base, f"/api/tasks/{research['id']}/report")
            assert report["config"]["data_version"] == research_version
            assert report["split"] == {
                "train": 600,
                "validation": 216,
                "test": 384,
                "purged_or_unmatured": 49,
                "test_status": "registered evaluation split; not claimed untouched by prior research",
                "refit_on_validation": False,
            }
            assert report["models"]["ridge"]["status"] == "evaluated"
            assert report["models"]["logistic"]["status"] == "training_has_one_class"
            _, equity = _request(base, f"/api/tasks/{research['id']}/artifacts/equity?baseline=B0")
            assert equity == [json.loads(line) for line in
                              (Path(research["result_path"]).parent / "B0" / "equity.jsonl").read_text(encoding="utf-8").splitlines() if line]
            assert equity
            assert _request_error(base, f"/api/tasks/{research['id']}/artifacts/equity?baseline=invalid")[0] == 422
            _, experiments = _request(base, "/api/experiments")
            assert research["id"] in {item["id"] for item in experiments}
            with psycopg.connect(database_url) as connection:
                stored = connection.execute(
                    "SELECT status, result_path FROM tasks WHERE id=%s",
                    (research["id"],),
                ).fetchone()
            assert stored[0] == "succeeded"
            assert Path(stored[1]).name == "report.json"
        finally:
            try:
                server.terminate()
                try:
                    server.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait(timeout=5)
            finally:
                if research_id:
                    task = records.task(research_id)
                    pid = task["pid"] if task and task["status"] in {"queued", "running"} else None
                    if _process_alive(pid):
                        if os.name == "nt":
                            subprocess.run(
                                ["taskkill", "/PID", str(pid), "/T", "/F"],
                                capture_output=True,
                                creationflags=subprocess.CREATE_NO_WINDOW,
                            )
                        else:
                            try:
                                os.kill(pid, signal.SIGTERM)
                            except ProcessLookupError:
                                pass
                        deadline = time.monotonic() + 5
                        while _process_alive(pid) and time.monotonic() < deadline:
                            time.sleep(0.05)
                        if _process_alive(pid) and os.name != "nt":
                            try:
                                os.kill(pid, signal.SIGKILL)
                            except ProcessLookupError:
                                pass
                            deadline = time.monotonic() + 5
                            while _process_alive(pid) and time.monotonic() < deadline:
                                time.sleep(0.05)
                        assert not _process_alive(pid), f"research worker did not stop: {pid}"
                    _cleanup_research(database_url, research_id)

    print("run checks passed")


if __name__ == "__main__":
    main()
