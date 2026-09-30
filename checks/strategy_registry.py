"""One runnable check for cross-round novelty enforcement, using only stdlib."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "research/automation/registry.py"


def main():
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        ledger, spec = root / "ledger.jsonl", root / "spec.json"

        def call(command, value, expected=0, *extra):
            spec.write_text(json.dumps(value))
            result = subprocess.run([sys.executable, str(TOOL), "--ledger", str(ledger), command, str(spec), *extra], capture_output=True, text=True)
            assert result.returncode == expected, result.stdout + result.stderr
            return result.stdout.strip()

        strategy = {"kind":"strategy", "family":"test-breakout", "name":"First", "universe":["BTC/USDT","ETH/USDT"], "market":"spot", "timeframe":"1d", "logic":{"entry":"close > prior channel high", "exit":"close < prior channel low"}, "parameters":{"entry_days":20,"exit_days":10}}
        first = call("reserve", strategy)
        call("reserve", {**strategy, "name":"Renamed", "universe":list(reversed(strategy["universe"]))}, 3)
        call("reserve", {**strategy, "parameters":{"entry_days":21,"exit_days":11}}, 3)
        call("reserve", {**strategy, "family":"renamed-family"}, 3)
        report = root / "report.json"
        report.write_text('{"net_return":-0.1}')
        call("finish", strategy, 0, "rejected", str(report))
        call("reserve", strategy, 3)
        second = call("reserve", {**strategy, "family":"test-momentum", "logic":{"entry":"past return > 0","exit":"past return <= 0"}})
        combo = {"kind":"combination", "family":"test-combination", "logic":{"allocation":"fixed sleeve weights", "rebalance":"monthly"}, "components":[{"fingerprint":first,"weight":1},{"fingerprint":second,"weight":1}]}
        call("reserve", combo)
        call("reserve", {**combo, "components":list(reversed(combo["components"]))}, 3)
        call("reserve", {**combo, "components":[{"fingerprint":first,"weight":2},{"fingerprint":second,"weight":2}]}, 3)
        call("reserve", {**combo, "components":[{"fingerprint":first,"weight":3},{"fingerprint":second,"weight":1}]}, 3)
        call("reserve", {**combo, "components":[{"fingerprint":"0"*64,"weight":1},{"fingerprint":first,"weight":1}]}, 2)
        records = [json.loads(line) for line in ledger.read_text().splitlines()]
        assert len(records) == 4 and records[1]["status"] == "rejected"
    print("PASS: renamed strategies, parameter-only changes and reordered/reweighted combinations are blocked; rejected trials persist")


if __name__ == "__main__":
    main()
