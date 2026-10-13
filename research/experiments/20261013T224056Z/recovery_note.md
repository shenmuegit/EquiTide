# Recovery note: first un-audited run

The first evaluation completed for all 10 already-reserved definitions but had not been audited or finished. Review found that `skipped_below_lot` requests appeared in the decisions file but were omitted from the per-order ledger and therefore from skip counts. This did not change balances or computed NAV, but it invalidated the skip-order audit. The first report and outputs are preserved under `recovery/attempt1/`; the corrected execution script records these skips in the ledger and the full batch is rerun under the same reservations before any configuration is finished.


Second run completed but was superseded before final audit because the report omitted the terminal reference metadata needed for per-sleeve terminal equity verification and the terminal-flat gate was initially checked only at 1x. The entire run output is preserved under `recovery/attempt2/`; all configs remain reserved and not finished.


A third completed calculation was also superseded before audit/finish because the report omitted terminal sleeve cash needed to compare the final ledger. Its report/log hashes are preserved in `recovery/attempt3/manifest.json`; configuration fingerprints remain reserved.
