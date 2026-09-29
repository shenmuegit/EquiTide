from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone
import importlib.metadata
import json
import os
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from usdt_quant.records import Records
from usdt_quant.runs import launch_task, reconcile_active


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = {"fills", "funding", "equity"}
DAY_NS = 24 * 60 * 60 * 1_000_000_000
HOUR_NS = 60 * 60 * 1_000_000_000


class BacktestRequest(BaseModel):
    data_version: str = Field(min_length=1, max_length=200)
    config: dict[str, Any]


class ResearchRequest(BaseModel):
    data_version: str = Field(min_length=1, max_length=200)
    config: dict[str, Any]


class EntryAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entry_ns: int = Field(ge=0, strict=True)


def _data_root() -> Path:
    return Path(os.environ.get("USDT_QUANT_DATA_ROOT", PROJECT_ROOT / "data")).resolve()


def _inside(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise HTTPException(400, "数据路径超出数据目录")
    return resolved


def _disk_path(value: str, root: Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return _inside(path, root)


def _coverage(root: Path) -> list[dict[str, Any]]:
    coverage_dir = root / "coverage"
    reports: list[dict[str, Any]] = []
    if not coverage_dir.is_dir():
        return reports
    for path in sorted(coverage_dir.glob("*.json"), reverse=True):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if report.get("data_version") and isinstance(report.get("datasets"), list):
            reports.append(report)
    return reports


def _dataset(report: dict[str, Any], root: Path) -> Path:
    required = {
        "spot_bars",
        "perp_bars",
        "mark_bars",
        "funding_settlement",
        "spot_instrument_meta",
        "perp_instrument_meta",
    }
    by_name = {item.get("dataset"): item for item in report["datasets"]}
    missing = sorted(required - by_name.keys())
    if missing:
        raise HTTPException(400, f"数据集缺少：{', '.join(missing)}")
    paths = []
    for name in required:
        item = by_name[name]
        if item.get("status") != "ok" or not item.get("parquet_path"):
            raise HTTPException(400, f"数据集不可用于回测：{name}")
        path = _disk_path(item["parquet_path"], root)
        if not path.is_file():
            raise HTTPException(400, f"数据文件不存在：{name}")
        paths.append(path)
    parents = {path.parent for path in paths}
    if len(parents) != 1:
        raise HTTPException(400, "回测数据文件不在同一数据版本目录")
    return parents.pop()


def _dependencies() -> dict[str, str]:
    names = ("usdt-quant", "nautilus-trader", "polars", "numpy", "scikit-learn")
    return {name: importlib.metadata.version(name) for name in names}


def _coverage_match(data_version: str, root: Path) -> dict[str, Any]:
    matches = [item for item in _coverage(root) if item["data_version"] == data_version]
    if not matches:
        raise HTTPException(400, "数据版本不存在")
    if len(matches) > 1:
        raise HTTPException(400, "数据版本不唯一，请重新生成覆盖报告")
    return matches[0]


def _iso_ns(value: Any) -> int:
    if not isinstance(value, str):
        raise ValueError("coverage boundary must be an ISO timestamp")
    moment = datetime.fromisoformat(value)
    if moment.tzinfo is None:
        raise ValueError("coverage boundary must include a timezone")
    delta = moment.astimezone(timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)
    return (delta.days * 86_400 + delta.seconds) * 1_000_000_000 + delta.microseconds * 1_000


def _automatic_research_request(entry_ns: int, root: Path) -> ResearchRequest:
    if entry_ns % HOUR_NS:
        raise HTTPException(422, "建仓时间必须为 UTC 整点")
    candidates: list[tuple[int, str, int, int]] = []
    for report in _coverage(root):
        try:
            start_ns = _iso_ns(report.get("requested_start"))
            end_ns = _iso_ns(report.get("requested_end_exclusive"))
            generated_ns = int(report.get("generated_ts", 0))
            data_version = report["data_version"]
            by_name = {item["dataset"]: item for item in report["datasets"]}
            funding = by_name["funding_settlement"]
            funding_quality = funding.get("quality") or {}
            missing_marks = int(funding_quality.get("missing_mark_price_at_settlement", 0))
            missing_rates = int(funding_quality.get("missing_realized_rate", 0))
            missing_minutes = max(
                int(by_name[name].get("missing_closed_minutes", 0))
                for name in ("spot_bars", "perp_bars", "mark_bars")
            )
        except (AttributeError, KeyError, TypeError, ValueError):
            continue
        if missing_marks > 0 or missing_rates > 0 or missing_minutes > 0:
            continue
        sample_start_ns = start_ns + 7 * DAY_NS
        train_end_ns = sample_start_ns + 26 * DAY_NS
        validation_end_ns = train_end_ns + 10 * DAY_NS
        if (entry_ns - validation_end_ns) % HOUR_NS or not validation_end_ns <= entry_ns <= end_ns - DAY_NS:
            continue
        try:
            _dataset(report, root)
        except (AttributeError, HTTPException, TypeError):
            continue
        candidates.append((generated_ns, data_version, sample_start_ns, end_ns))
    if not candidates:
        raise HTTPException(422, "没有覆盖该建仓时间且满足研究窗口要求的数据版本")

    _, data_version, start_ns, end_ns = max(candidates, key=lambda item: (item[0], item[1]))
    return ResearchRequest(data_version=data_version, config={
        "baseline": "B0",
        "start_ns": start_ns,
        "end_ns": end_ns,
        "decision_interval_ns": HOUR_NS,
        "holding_period_ns": DAY_NS,
        "funding_window": 21,
        "initial_spot_usdt": "10000",
        "initial_perp_usdt": "10000",
        "target_spot_base": "0.01",
        "spot_taker_fee": "0.001",
        "perp_taker_fee": "0.0005",
        "execution_bps_per_leg": "2",
        "buffer_usdt": "0",
        "train_end_ns": start_ns + 26 * DAY_NS,
        "validation_end_ns": start_ns + 36 * DAY_NS,
        "entry_analysis_ns": entry_ns,
        "ridge_alpha": 1,
        "logistic_c": 1,
        "seed": 20260916,
        "bootstrap_samples": 200,
    })


def _json_file(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise HTTPException(404, "结果文件不存在") from error
    except json.JSONDecodeError as error:
        raise HTTPException(500, "结果文件格式无效") from error


def create_app() -> FastAPI:
    database_url = os.environ.get("DATABASE_URL")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not database_url:
            raise RuntimeError("DATABASE_URL is required")
        app.state.records = Records(database_url)
        app.state.records.initialize()
        reconcile_active(app.state.records)
        yield

    app = FastAPI(title="USDT 量化控制台", lifespan=lifespan)

    @app.get("/api/coverage")
    def coverage() -> list[dict[str, Any]]:
        return _coverage(_data_root())

    @app.get("/api/tasks")
    def tasks(
        limit: int = Query(50, ge=1, le=100),
        kind: str | None = Query(None, pattern="^(backtest|research)$"),
    ) -> list[dict[str, Any]]:
        return app.state.records.tasks(limit, kind)

    @app.get("/api/experiments")
    def experiments(limit: int = Query(50, ge=1, le=100)) -> list[dict[str, Any]]:
        return app.state.records.experiments(limit)

    @app.get("/api/tasks/{task_id}")
    def task(task_id: str) -> dict[str, Any]:
        result = app.state.records.task(task_id)
        if result is None:
            raise HTTPException(404, "任务不存在")
        return result

    @app.post("/api/backtests", status_code=202)
    def submit(request: BacktestRequest) -> dict[str, Any]:
        root = _data_root()
        report = _coverage_match(request.data_version, root)
        config = {
            **request.config,
            "data_version": request.data_version,
            "exchange": report["exchange"],
            "base_asset": report["base"],
        }
        try:
            from usdt_quant.runs import _config

            validated = _config(config)
            config = validated.as_json()
        except (TypeError, ValueError, ArithmeticError) as error:
            raise HTTPException(422, str(error)) from error
        dataset_dir = _dataset(report, root)
        result = app.state.records.create_backtest(
            config=config,
            dependency_versions=_dependencies(),
            data_version=request.data_version,
            dataset_dir=dataset_dir,
        )
        launch_task(app.state.records, result["id"])
        return app.state.records.task(result["id"])

    @app.post("/api/research", status_code=202)
    def submit_research(request: ResearchRequest) -> dict[str, Any]:
        root = _data_root()
        report = _coverage_match(request.data_version, root)
        config = {
            **request.config,
            "data_version": request.data_version,
            "exchange": report["exchange"],
            "base_asset": report["base"],
        }
        try:
            from usdt_quant.runs import _research_config

            config = _research_config(config)
        except (TypeError, ValueError, ArithmeticError) as error:
            raise HTTPException(422, str(error)) from error
        result = app.state.records.create_research(
            config=config,
            dependency_versions=_dependencies(),
            data_version=request.data_version,
            dataset_dir=_dataset(report, root),
        )
        launch_task(app.state.records, result["id"])
        return app.state.records.task(result["id"])

    @app.post("/api/entry-analyses", status_code=202)
    def submit_entry_analysis(request: EntryAnalysisRequest) -> dict[str, Any]:
        try:
            return submit_research(_automatic_research_request(request.entry_ns, _data_root()))
        except HTTPException as error:
            if error.status_code == 400:
                raise HTTPException(422, error.detail) from error
            raise

    @app.get("/api/tasks/{task_id}/report")
    def task_report(task_id: str) -> Any:
        result = app.state.records.task(task_id)
        if result is None:
            raise HTTPException(404, "任务不存在")
        if result["status"] != "succeeded" or not result["result_path"]:
            raise HTTPException(409, result["error"] or "任务尚未完成")
        path = _inside(Path(result["result_path"]), _data_root())
        return _json_file(path)

    @app.get("/api/tasks/{task_id}/artifacts/{name}")
    def artifact(task_id: str, name: str, baseline: Literal["B0", "B1", "M1"] | None = None) -> list[Any]:
        if name not in ARTIFACTS:
            raise HTTPException(404, "明细不存在")
        result = app.state.records.task(task_id)
        if result is None:
            raise HTTPException(404, "任务不存在")
        if result["status"] != "succeeded" or not result["result_path"]:
            raise HTTPException(409, result["error"] or "任务尚未完成")
        directory = Path(result["result_path"]).parent
        if baseline is not None:
            if result["kind"] != "research":
                raise HTTPException(422, "基准仅适用于研究任务")
            directory /= baseline
        path = _inside(directory / f"{name}.jsonl", _data_root())
        try:
            return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
        except FileNotFoundError as error:
            raise HTTPException(404, "明细文件不存在") from error
        except json.JSONDecodeError as error:
            raise HTTPException(500, "明细文件格式无效") from error

    return app


app = create_app()
