# EquiTide scheduled automation working directory

- The `btc-eth` and `btc-eth-2` heartbeat threads must use `/home/desktop/Documents/Codex/EquiTide` as their working directory.
- Do not use `/root/Documents/Codex/EquiTide` for scheduled work. The Codex automation runtime runs as `desktop` and cannot traverse `/root`.
- Before a scheduled run, verify this directory is the EquiTide repository with `git rev-parse --show-toplevel` and confirm it is readable. If it is unavailable, record the access failure instead of switching to an unrelated checkout.
- Keep each task's required research branch, account state, and data-use constraints from its automation instructions.
