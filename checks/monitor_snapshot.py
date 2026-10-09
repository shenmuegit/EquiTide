"""Read-only dashboard evidence checks; run from the repository root."""
import importlib.util
import gzip
import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
module_spec = importlib.util.spec_from_file_location("monitor_snapshot", ROOT / "research/monitor/snapshot.py")
snapshot = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(snapshot)


def main():
    protected = [ROOT / p for p in (
        "research/paper10/plan.json", "research/paper10/state.json",
        "research/automation/registry.jsonl", "research/paper10/run.py",
    )]
    before = {p: snapshot.sha(p.read_bytes()) for p in protected}
    data = snapshot.build_snapshot(ROOT)
    assert before == {p: snapshot.sha(p.read_bytes()) for p in protected}, "monitor changed trading/research inputs"
    paper = data["paper"]
    assert paper["status"] == "ready", paper.get("errors")
    assert len(paper["accounts"]) == 10
    assert len({a["id"] for a in paper["accounts"]}) == 10
    assert paper["observation_count"] == len(paper["history"])
    assert sum(Decimal(a["capital_usdt"]) for a in paper["accounts"]) == Decimal("20000")
    for cost in ("1", "2", "3"):
        total = sum(Decimal(a["scenes"][cost]["nav"]) for a in paper["accounts"])
        assert total == Decimal(paper["totals"][cost]["nav"])
        assert total == Decimal(paper["history"][-1]["totals"][cost]["nav"])
    ids = [r["fingerprint"] for r in data["research"]["configs"]]
    assert len(ids) == len(set(ids)), "equivalent configurations counted twice"
    # Finished structured evidence may use a component-specific report filename.
    registry = snapshot.registry_module(ROOT)
    for record in registry.read_records(ROOT / "research/automation/registry.jsonl").values():
        report_path = ROOT / record.get("report", "")
        params = record["spec"].get("parameters", {})
        if (not record.get("result_available") or snapshot.is_observation(record["spec"])
                or report_path.name == "report.json" or report_path.suffix != ".json"
                or not report_path.is_file() or not params.get("start_utc") or not params.get("end_utc")):
            continue
        if snapshot.sha(report_path.read_bytes()) != record.get("report_sha256"):
            continue
        fp = registry.fingerprint(record["spec"])
        configs = snapshot.load(report_path).get("configs", {})
        if not isinstance(configs, dict):
            continue
        cfg = next((c for c in configs.values() if isinstance(c, dict) and c.get("fingerprint") == fp), {})
        if any(snapshot.metric_scene(s) for s in cfg.get("scenes", {}).values()):
            assert fp in ids, f"finished report absent from dashboard: {report_path.name} {fp}"
    assert len({r["id"] for r in data["research"]["rounds"]}) == len(data["research"]["rounds"])
    assert all(not snapshot.is_observation(r["spec"]) for r in data["research"]["configs"])
    assert any(r["status"] == "rejected" for r in data["research"]["configs"])
    assert any(s["return_pct"] < 0 for r in data["research"]["configs"] for s in r["scenes"].values()), "negative results disappeared"
    assert data["research"]["counts"]["observation_records_excluded"] > 0
    assert all(r["start_utc"] and r["end_utc"] for r in data["research"]["configs"])
    assert snapshot.is_observation({"name": "forward_snapshot_BTC", "parameters": {}})
    assert snapshot.is_observation({"family": "paper-live-portfolio-observation"})
    assert snapshot.is_observation({"parameters": {"observation_terminal_action": "mark only"}})
    # A torn journal must never become the latest valuation.
    original = ROOT / "research/paper10/observations" / paper["observation_id"]
    with TemporaryDirectory() as tmp:
        folder = Path(tmp)
        for name in ("report.json", "state_after.json", "complete.json"):
            (folder / name).write_bytes((original / name).read_bytes())
        snapshot.read_journal(folder, paper["plan_sha256"])
        (folder / "report.json").write_text('{"mode":"live_public_quotes"}\n')
        try:
            snapshot.read_journal(folder, paper["plan_sha256"])
        except ValueError:
            pass
        else:
            raise AssertionError("torn report accepted")
    with TemporaryDirectory() as tmp:
        target = Path(tmp) / "latest.json"
        snapshot.atomic_write(target, data)
        restored = json.loads(target.read_text())
        assert restored["paper"]["state_sha256"] == paper["state_sha256"]
        assert len(gzip.compress(target.read_bytes(), mtime=0)) < 1_000_000, "monitor feed contains bulky raw evidence"
    print(json.dumps({"ok": True, "paper_accounts": 10, "observations": len(paper["history"]),
                      "research_configs": len(ids), "protected_inputs_unchanged": True}))


if __name__ == "__main__":
    main()
