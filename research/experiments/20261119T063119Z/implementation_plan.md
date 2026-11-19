# BTC actual entry budget with matched holds Implementation Plan

> For agentic workers: execute inline in this chat; the user's automation explicitly forbids subagents and other branches. The standing authorization covers choosing and executing this preregistered research batch.

**Goal:** Evaluate BTC entry budgets 1250/1500 USDT against the readonly 1000 control, crossed with readonly ETH caps .0525/.05625, with actual execution costs and exposure-matched holding references.

**Architecture:** Reuse the unchanged native engine and Decimal accounting. Recompute the two changed BTC strategy banks and two BTC constant-long references; reuse exact ETH net NAVs and sum complete independent banks with raw weights [1,1]. Add four strategy parents and two matching hold parents. Ten concrete new definitions are reserved before any market calculation.

**Tech Stack:** Existing Python research venv, NumPy, pandas, real saved Binance inputs and registry.

**Spec:** This round's plan.json/spec.json, frozen by freeze_confirmation.py before reserve.

## Global Constraints

Use only /home/desktop/Documents/Codex/EquiTide and main, with the acquired branch.lock. Preserve every old result and account; no real orders, new paper10 observations, normalization, NAV scaling, collateral transfers or parent rebalancing. Total initial capital stays 18750 (BTC3750/ETH15000); ETH entry budget4000, BTC nominal entry budget is the varied parameter, not capital share. Representative BTC1250/ETHcap.05625 is fixed before results. All391days are reused development history.

## Approaches

Moving collateral while keeping actual positions fixed can leave parent NAV unchanged. Linear resizing misses LOT rounding and nonlinear impact. The selected approach recomputes changed actual order sizes and their matched holds while reusing unchanged components; this is the assistant's choice within the user's explicit authorization.

## Review Focus

- LOT rounding and actual order notional must follow the prior completed close and next executable OPEN.
- Fees, spread, slippage, square-root ADV impact and funding outflow stress must use each actual new quantity.
- Each new sizing scenario must use its own BTC holding reference with the same capital and entry budget.
- Both sensitivity axes and every new benchmark must have independent reserve/finish records; completed controls remain readonly.
- Original accounts must retain first16 source bytes/UTC even when this round's fresh query excludes16; no duplicate settlement or cash reset.

## Tasks

- [ ] Freeze ten exact definitions, two axes, representative, failure gates, input/source hashes and matching-reference map; run synthetic LOT/impact/funding/calendar checks with zero market backtests.
- [ ] Bind creators, reserve both batches successfully, evaluate once, audit actual decisions/cash/quantities/funding/costs/full NAV, export all folds/costs/heatmap, and finish all ten IDs including negative holds.
- [ ] Continue each original account from its own saved state; audit complete prefixes and once-only settlements, run registry and readonly monitor checks, review scope, seal, commit/push main, verify the remote tree, unlock natively and check again.

Self-review: exact reuse sources are in sizing_reference_availability.json; new order budgets and derived notional fractions change together. Current originals are mark-only windows, not fresh strategy trials. No implementation or verification will be delegated.
