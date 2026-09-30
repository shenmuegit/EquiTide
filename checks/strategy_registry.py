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
        variant = {**strategy, "parameters":{"entry_days":21,"exit_days":11}}
        changed_parameters = call("reserve", variant)
        assert changed_parameters != first
        call("reserve", {**strategy, "parameters":{"entry_days":20.0,"exit_days":10.0}}, 3)
        call("reserve", {**strategy, "family":"renamed-family"}, 3)
        report = root / "report.json"
        report.write_text('{"net_return":-0.1}')
        call("finish", strategy, 0, "rejected", str(report))
        call("reserve", strategy, 3)
        second = call("reserve", {**strategy, "family":"test-momentum", "logic":{"entry":"past return > 0","exit":"past return <= 0"}})
        combo = {"kind":"combination", "family":"test-combination", "logic":{"allocation":"fixed sleeve weights", "rebalance":"monthly"}, "components":[{"fingerprint":first,"weight":1},{"fingerprint":second,"weight":1}]}
        call("reserve", combo)
        call("reserve", {**combo, "components":list(reversed(combo["components"]))}, 3)
        call("reserve", {**combo, "components":[{"fingerprint":first,"weight":2},{"fingerprint":second,"weight":2}]})
        changed_weights = {**combo, "components":[{"fingerprint":first,"weight":3},{"fingerprint":second,"weight":1}]}
        call("reserve", changed_weights)
        call("reserve", {**changed_weights, "components":list(reversed(changed_weights["components"]))}, 3)
        call("reserve", {**combo, "parameters":{"rebalance_days":7}})
        call("reserve", {**combo, "components":[{"fingerprint":changed_parameters,"weight":1},{"fingerprint":second,"weight":1}]})
        call("reserve", {**combo, "components":[{"fingerprint":"0"*64,"weight":1},{"fingerprint":first,"weight":1}]}, 2)
        # Historical IDs stay valid, but entries without results can be tested again.
        legacy = {"fingerprint":"a"*64, "spec":{**combo,"parameters":{"rebalance_days":90}}, "status":"legacy-script", "result_available":False}
        with ledger.open("a") as output:
            output.write(json.dumps(legacy)+"\n")
        call("reserve", legacy["spec"])
        call("reserve", legacy["spec"], 3)
        call("finish", legacy["spec"], 0, "rejected", str(report))
        call("reserve", legacy["spec"], 3)
        tested_legacy = {"fingerprint":"b"*64,"spec":{**combo,"parameters":{"rebalance_days":120}},"status":"legacy-tested","result_available":True}
        with ledger.open("a") as output:
            output.write(json.dumps(tested_legacy)+"\n")
        call("reserve", tested_legacy["spec"], 3)
        records = [json.loads(line) for line in ledger.read_text().splitlines()]
        assert len(records) == 13 and records[2]["status"] == "rejected"
        assert records[-2]["result_available"] is True
    print("PASS: new parameters/weights and missing-result retries are allowed; exact/reordered completed trials stay blocked")


if __name__ == "__main__":
    main()
