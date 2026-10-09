"""Publish a compact, read-only view of committed research and paper evidence.

No prices are downloaded, no strategies evaluated, and no account state is changed.
Run under research/automation/branch.lock before each research/paper evidence push.
"""
import argparse
import gzip
import hashlib
import importlib.util
import json
import os
import subprocess
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def is_observation(spec):
    return (spec.get("family") == "paper-live-portfolio-observation"
            or spec.get("name", "").startswith("forward_snapshot_")
            or "observation_terminal_action" in spec.get("parameters", {}))


def registry_module(root):
    spec = importlib.util.spec_from_file_location("monitor_registry", root / "research/automation/registry.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def indicator(spec, records, depth=0):
    """Labels are derived from exact registered parameters, never from rankings."""
    if depth > 3:
        return "组合"
    if spec.get("kind") == "combination":
        return " · ".join(indicator(records.get(c["fingerprint"], {}).get("spec", {}), records, depth + 1)
                          for c in spec.get("components", []))
    p, family = spec.get("parameters", {}), spec.get("family", "")
    asset = "/".join(s.split("/")[0] for s in spec.get("universe", []))
    percent = lambda value: f"{float(value) * 100:g}%"
    if "channel" in family or "close-range" in family:
        text = f"收盘通道 {p.get('entry_lookback_days', '?')}/{p.get('exit_lookback_days', '?')}"
        if "EMA_span_days" in p:
            text += f" + EMA{p['EMA_span_days']} ±{percent(p['EMA_symmetric_band'])}"
    elif "sma" in family or "ema" in family:
        kind = "OBV SMA" if "obv" in family else "EMA" if "ema" in family else "SMA"
        text = f"{kind}{p.get('lookback_days', p.get('span_days', p.get('lookback', '?')))}"
        if "entry_band_fraction" in p:
            text += f" +{percent(p['entry_band_fraction'])}/−{percent(p.get('exit_band_fraction', 0))}"
        elif "symmetric_band_fraction" in p:
            text += f" ±{percent(p['symmetric_band_fraction'])}"
        if "confirmation_days" in p:
            text += f" 连续{p['confirmation_days']}日"
        if "annual_volatility_ceiling" in p:
            text += f" 波动率≤{percent(p['annual_volatility_ceiling'])}"
    elif "hold" in family:
        text = "买入持有基准"
    else:
        text = family or "组件规则见源配置"
    return f"{asset} {text}".strip()


def read_journal(folder, plan_hash):
    report_raw, state_raw = (folder / "report.json").read_bytes(), (folder / "state_after.json").read_bytes()
    complete, report, state = load(folder / "complete.json"), json.loads(report_raw), json.loads(state_raw)
    if (complete.get("report_sha256") != sha(report_raw)
            or complete.get("state_after_sha256") != sha(state_raw)
            or report.get("state_after_sha256") != sha(state_raw)
            or report.get("plan_sha256") != plan_hash
            or state.get("plan_sha256") != plan_hash
            or report.get("mode") != "live_public_quotes"
            or report.get("real_orders") != 0
            or report.get("observation_id") != state.get("last_observation_id")):
        raise ValueError(f"Inconsistent paper journal: {folder.name}")
    return report, state, sha(state_raw)


def paper_scene(scene):
    return {"nav": scene["NAV_usdt"], "pnl": scene["net_PnL_usdt"],
            "return_pct": scene["net_return_pct"], "drawdown_pct": scene["observed_sample_max_drawdown_pct"],
            "cost": scene["cost_usdt"], "cost_parts": scene["cost_parts"],
            "executions": scene["executions"], "round_trips": scene["round_trips"],
            "positions": {asset: {k: sleeve[k] for k in ("units", "cash_usdt", "desired_long", "last_signal_open_ms")}
                          for asset, sleeve in scene["sleeves"].items()}}


def paper_totals(accounts):
    result = {}
    capital = sum(Decimal(a["capital_usdt"]) for a in accounts)
    for cost in ("1", "2", "3"):
        scenes = [a["scenes"][cost] for a in accounts]
        nav = sum(Decimal(s["nav"]) for s in scenes)
        result[cost] = {"nav": str(nav), "pnl": str(nav - capital),
                        "return_pct": float((nav / capital - 1) * 100),
                        "cost": str(sum(Decimal(s["cost"]) for s in scenes)),
                        "fee": str(sum(Decimal(s["cost_parts"]["fee"]) for s in scenes)),
                        "executions": sum(s["executions"] for s in scenes),
                        "round_trips": sum(s["round_trips"] for s in scenes)}
    return result


def build_paper(root):
    base = root / "research/paper10"
    plan_raw = (base / "plan.json").read_bytes()
    plan, plan_hash = json.loads(plan_raw), sha(plan_raw)
    journals, operations, errors = [], [], []
    for folder in sorted((base / "observations").iterdir()):
        if not folder.is_dir():
            continue
        report_path = folder / "report.json"
        if (folder / "complete.json").exists():
            try:
                report, state, state_hash = read_journal(folder, plan_hash)
                journals.append((folder, report, state, state_hash))
                operations.append({"id": folder.name, "at": report["observed_at_utc"], "mode": "success",
                                   "virtual_orders": report["new_filled_virtual_orders"],
                                   "report": report_path.relative_to(root).as_posix()})
            except (ValueError, OSError, KeyError) as error:
                errors.append(str(error))
        elif report_path.exists():
            report = load(report_path)
            operations.append({"id": folder.name, "at": report.get("observed_at_utc", report.get("created_at_utc")),
                               "mode": "failed", "error": str(report.get("error", report.get("reason", "观察未完成")))[:500],
                               "virtual_orders": 0, "report": report_path.relative_to(root).as_posix()})
    if not journals:
        return {"status": "unavailable", "errors": errors or ["尚无完整真实行情观察"], "operations": operations}
    folder, latest, state, state_hash = journals[-1]
    if any(op["mode"] == "failed" and op["id"] > folder.name for op in operations):
        errors.append("最新一轮观察失败；继续显示最后完整账户，等待执行器恢复")
    current_raw = (base / "state.json").read_bytes()
    if sha(current_raw) != state_hash:
        errors.append("当前账户与最后完整观察不一致；显示最后校验通过的观察，等待下一轮核对")
    configs = {p["id"]: p for p in plan["portfolios"]}
    components = {fp: {"spec": spec} for fp, spec in plan["components"].items()}
    accounts = []
    for account_id, cfg in sorted(latest["configs"].items()):
        source = configs[account_id]
        accounts.append({"id": account_id, "label": source["label"], "capital_usdt": str(source["capital_usdt"]),
                         "source_spec": source["source_path"], "source_fingerprint": source["source_fingerprint"],
                         "weights": [{"asset": c["asset"], "weight": c["weight"],
                                      "indicator": indicator(components[c["source_fingerprint"]]["spec"], components)}
                                     for c in source["components"]],
                         "coverage_fraction": cfg["observation_coverage_fraction"],
                         "scenes": {cost: paper_scene(scene) for cost, scene in cfg["scenes"].items()},
                         "criteria": cfg["criteria"]})
    history, trades = [], []
    for journal_folder, report, _, _ in journals:
        rows = [{"capital_usdt": str(configs[key]["capital_usdt"]),
                 "scenes": {cost: paper_scene(scene) for cost, scene in cfg["scenes"].items()}}
                for key, cfg in report["configs"].items()]
        history.append({"at": report["observed_at_utc"], "totals": paper_totals(rows),
                        "returns": {key: {cost: scene["net_return_pct"] for cost, scene in cfg["scenes"].items()}
                                    for key, cfg in report["configs"].items()}})
        for trade in load(journal_folder / "trade_ledger.json"):
            trades.append({k: trade[k] for k in ("trade_id", "portfolio", "asset", "side", "cost_multiplier", "status",
                                                "quantity", "execution", "cost_usdt", "cost_parts", "simulated_at_utc",
                                                "quote_observed_at_utc", "signal_available_at_utc") if k in trade})
    if len({t["trade_id"] for t in trades}) != len(trades):
        raise ValueError("Duplicate paper trade IDs")
    if len(history) != state["observations"]:
        errors.append("完整观察数量与账户记录不一致")
    market = load(folder / "market.json")
    return {"status": "degraded" if errors else "ready", "errors": errors,
            "observation_id": folder.name, "observed_at_utc": latest["observed_at_utc"],
            "start_utc": state["cohort_started_at_utc"], "end_utc": state["cohort_end_utc"],
            "elapsed_seconds": max(c["observed_elapsed_seconds"] for c in latest["configs"].values()),
            "duration_days": plan["duration_days"], "fold_days": plan["fold_days"],
            "observation_count": len(history), "maximum_gap_seconds": plan["maximum_observation_gap_seconds"],
            "coverage_gaps": state["coverage_gaps"], "plan_sha256": plan_hash, "state_sha256": state_hash,
            "report_sha256": sha((folder / "report.json").read_bytes()), "quotes_at_valuation": market["quotes"],
            "decisions": [d for d in latest["decisions"] if d["cost_multiplier"] == 1],
            "accounts": accounts, "totals": paper_totals(accounts), "history": history,
            "trades": trades[-500:], "trade_count": len(trades), "operations": operations[-100:],
            "report": (folder / "report.json").relative_to(root).as_posix()}


def metric_scene(scene):
    if not isinstance(scene, dict) or "net_return_pct" not in scene or "max_drawdown_pct" not in scene:
        return None
    display = lambda value: round(float(value), 6) if value is not None else None
    return {"return_pct": display(scene["net_return_pct"]), "drawdown_pct": display(scene["max_drawdown_pct"]),
            "sharpe": display(scene.get("sharpe_365")), "cost": display(scene.get("cost_usdt")),
            "executions": scene.get("executions"), "round_trips": scene.get("round_trips"),
            "nav_hash": scene.get("NAV_sha256_f64le"),
            "fold_returns_pct": [display(f["net_return_pct"]) for f in scene.get("folds", [])],
            "fold_drawdowns_pct": [display(f.get("max_drawdown_pct")) for f in scene.get("folds", [])],
            "first_five_return_pct": display(scene.get("first_five_fold_return_pct"))}


def build_research(root):
    registry = registry_module(root)
    ledger_path = root / "research/automation/registry.jsonl"
    records = registry.read_records(ledger_path)
    canonical, aliases, excluded = {}, {}, 0
    for old_fp, record in records.items():
        fp = registry.fingerprint(record["spec"])
        aliases[old_fp] = fp
        if is_observation(record["spec"]):
            excluded += 1
            continue
        prior = canonical.get(fp)
        if prior is None or (record.get("result_available") and not prior.get("result_available")):
            canonical[fp] = record
    reports, matches, cross = {}, {}, set()
    rounds = []
    experiments = root / "research/experiments"
    report_paths = set(experiments.glob("*/report.json"))
    for record in canonical.values():
        if record.get("result_available") and record.get("report"):
            path = (root / record["report"]).resolve()
            if path.is_relative_to(experiments.resolve()) and path.suffix == ".json" and path.is_file():
                report_paths.add(path)
    for path in sorted(report_paths):
        report, relative = load(path), path.relative_to(root).as_posix()
        digest = sha(path.read_bytes())
        reports[relative] = (report, digest)
        cfgs = report.get("configs", {})
        if not isinstance(cfgs, dict):
            continue
        for name, cfg in cfgs.items():
            if not isinstance(cfg, dict):
                continue
            fp = aliases.get(cfg.get("fingerprint"), cfg.get("fingerprint"))
            record = canonical.get(fp)
            if record and relative == record.get("report") and digest == record.get("report_sha256"):
                matches[fp] = (name, cfg, report, relative)
            other = cfgs.get(cfg.get("other_period_config"), {})
            if (cfg.get("both_periods_meet_full_gates") is True
                    and cfg.get("status") == "passed" and other.get("status") == "passed"
                    and len(cfg.get("scenes", {})) >= 3 and len(other.get("scenes", {})) >= 3):
                cross.add(fp)
        summary = report.get("summary", {})
        new_count = summary.get("new_configs", len([c for c in cfgs.values() if isinstance(c, dict) and c.get("is_new")]))
        if new_count and path.name == "report.json":
            passed, rejected = summary.get("passed", []), summary.get("rejected", [])
            rounds.append({"id": path.parent.name, "at": report.get("evaluation_started_utc", report.get("created_at_utc")),
                           "new_configs": new_count, "passed": len(passed) if isinstance(passed, list) else passed,
                           "rejected": len(rejected) if isinstance(rejected, list) else rejected,
                           "new_cross_period_pairs": len(summary.get("new_both_periods_passed_combination_pairs", [])),
                           "report": relative, "result": str(path.parent.relative_to(root) / "result.md")})
    rows, unranked = [], []
    for fp, record in canonical.items():
        if not record.get("result_available") or fp not in matches:
            unranked.append({"fingerprint": fp, "family": record["spec"]["family"], "status": record["status"],
                             "result_available": record.get("result_available", False), "report": record.get("report")})
            continue
        name, cfg, report, relative = matches[fp]
        scenes = {str(cost): metric_scene(scene) for cost, scene in cfg.get("scenes", cfg.get("cost_scenarios", {})).items()}
        scenes = {cost: scene for cost, scene in scenes.items() if scene is not None}
        spec, params = record["spec"], record["spec"].get("parameters", {})
        start = params.get("start_utc", report.get("oos_start_utc"))
        end = params.get("end_utc", report.get("terminal_exit_utc"))
        if not scenes or not start or not end:
            unranked.append({"fingerprint": fp, "family": spec["family"], "status": record["status"],
                             "result_available": True, "report": relative})
            continue
        weights = [{"asset": "/".join(a.split("/")[0] for a in records.get(c["fingerprint"], {}).get("spec", {}).get("universe", [])),
                    "weight": c["weight"]} for c in spec.get("components", [])]
        rows.append({"fingerprint": fp, "name": name, "family": spec["family"], "kind": spec["kind"],
                     "indicator": indicator(spec, records), "weights": weights, "capital_usdt": params.get("initial_capital_usdt"),
                     "start_utc": start, "end_utc": end, "status": record["status"], "cross_period_passed": fp in cross,
                     "scenes": scenes, "criteria": cfg.get("criteria", {}),
                     "failed_criteria": cfg.get("failed_criteria", [k for k, v in cfg.get("criteria", {}).items() if v is False]),
                     "positive_folds_1x": cfg.get("positive_folds_1x"), "report": relative,
                     "validation": {"walk_forward_folds": len(scenes.get("1", {}).get("fold_returns_pct", [])),
                                    "cost_scenarios": sorted(scenes), "sensitivity_recorded": bool(report.get("sensitivity"))},
                     "spec_path": cfg.get("spec", cfg.get("spec_path")),
                     "spec": {"name": spec.get("name", name), "kind": spec["kind"], "family": spec["family"],
                              "parameters": {k: v for k, v in params.items()
                                                                         if isinstance(v, (int, float, bool))
                                                                         or k in ("start_utc", "end_utc")}}})
    counts = Counter(record["status"] for record in canonical.values())
    period_pairs = sorted(set((r["start_utc"], r["end_utc"]) for r in rows), reverse=True)
    return {"last_run": rounds[-1] if rounds else None, "registry_sha256": sha(ledger_path.read_bytes()),
            "counts": {"registered": len(canonical), "results": sum(bool(r.get("result_available")) for r in canonical.values()),
                       "passed": counts["passed"], "rejected": counts["rejected"], "blocked": counts["blocked"],
                       "legacy_tested": counts["legacy-tested"], "ranked": len(rows), "unranked": len(unranked),
                       "observation_records_excluded": excluded, "canonical_aliases_merged": len(records) - excluded - len(canonical)},
            "configs": rows, "unranked": unranked, "rounds": rounds[-60:],
            "periods": [{"start_utc": start, "end_utc": end} for start, end in period_pairs]}


def build_snapshot(root):
    # Fail closed on malformed registry/JSON. Keep the previous atomic feed intact.
    return {"schema_version": 1, "generated_at_utc": utc_now(),
            "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
            "source_repository": "https://github.com/shenmuegit/EquiTide/tree/codex/strategy-research",
            "refresh": {"paper_seconds": 7200, "feed_seconds": 30, "quote_seconds": 10},
            "paper": build_paper(root), "research": build_research(root)}


def atomic_write(path, data):
    atomic_bytes(path, (json.dumps(data, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n").encode())


def atomic_bytes(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as output:
        output.write(raw)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, default=Path("research/monitor/latest.json"))
    args = parser.parse_args()
    root = args.root.resolve()
    data = build_snapshot(root)
    path = args.output if args.output.is_absolute() else root / args.output
    configs = data["research"].pop("configs")
    raw = json.dumps(configs, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode()
    compressed = gzip.compress(raw, mtime=0)
    config_path = path.with_name("configs.json.gz")
    atomic_bytes(config_path, compressed)
    data["research"].update({"configs_sha256": sha(raw), "configs_path": "configs.json.gz"})
    atomic_write(path, data)
    print(json.dumps({"output": str(path), "bytes": path.stat().st_size, "paper_status": data["paper"]["status"],
                      "research_configs": len(configs), "compressed_research_bytes": len(compressed)}))


if __name__ == "__main__":
    main()
