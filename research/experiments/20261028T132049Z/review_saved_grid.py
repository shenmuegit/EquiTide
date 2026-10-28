"""Describe the finished grid without evaluating models or changing old ratings."""
import hashlib
import json
from pathlib import Path

from run import axes, grid_configs

R = Path(__file__).resolve().parent
report_path = R / "report.json"
report = json.loads(report_path.read_text())
assert len(report["configs"]) == 24
assert all(c["status"] in ("passed", "rejected") for c in report["configs"].values())
grid = grid_configs(report["configs"])
rows = []
for scope in ("native", "parent"):
    for hurdle in (.02, .025, .03):
        for slow in (27, 28, 29):
            cells = []
            for c in grid.values():
                fields = list(axes(c))
                if c["scope"] == scope and c[fields[0]] == hurdle and c[fields[1]] == slow:
                    cells.append(c)
            cells.sort(key=lambda c: c[list(axes(c))[2]])
            assert len(cells) == 2
            rows.append({"scope": scope, "hurdle": hurdle, "slow_center_days": slow,
                         "fast_days": [c[list(axes(c))[2]] for c in cells],
                         "already_saved_statuses": [c["status"] for c in cells],
                         "positive_recent5d_folds_1x": [c["recent40_positive_5d_folds_1x"] for c in cells],
                         "positive_complete30d_folds_1x": [c["positive_complete_30d_folds_1x"] for c in cells],
                         "full_return_3x_pct": [c["scenes"]["3"]["net_return_pct"] for c in cells],
                         "old_readonly_H025": hurdle == .025})
out = {"financial_report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
       "new_financial_evaluations": 0, "saved_cells": len(grid), "old_statuses_unchanged": True,
       "no_reselection_or_threshold_changes": True, "rows": rows,
       "interpretation_zh": "通过项仍集中在父组合 S28，H2/H2.5 两个阈值相邻而 H3 近期正折不足；全期正收益平台不能替代近期折稳健性，也不构成独立未来验证。"}
(R / "recent_platform_diagnostics.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(out, ensure_ascii=False))
