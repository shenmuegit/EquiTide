# BTC/ETH rolling hourly relative-price strategy implementation plan

> **For agentic workers:** use inline execution. The user's unattended authorization fixes main only, this workspace and no subagents; no additional approval or worktree is needed.

**Goal:** Actually evaluate nine preregistered entry/exit configurations with native two-bank execution, costs and independent accounting evidence.

**Architecture:** Import the immutable previous accounting engine for data validation, Decimal fills, funding, native statistics and margin calculations. Add only a joint hourly clock, past-only OLS features and a coupled two-leg state machine. Save all completed scenes and audit recorded events independently without invoking the new trading model.

**Tech Stack:** Existing Python, NumPy, Polars and Matplotlib; no new dependency.

**Spec:** This round's plan.json and nine specs, frozen before reservations/calculation. Prior proposal is in ../20261030T173813Z/next_direction_proposal.json; full rules below are researcher choices under the existing authorization.

## Global constraints

- Fixed working directory /home/desktop/Documents/Codex/EquiTide; main only; common branch.lock held until actual publisher process exit0 and complete remote proof. No real orders or subagents.
- Read complete registry/fragments and243 conclusions; initial16actual evidence complete. Old nine OLS/ADF pairs have real results and remain immutable; reversed regression, new time/capital, embargo, holding and execution rules must be compared in full.
- 370day OOS 2025-10-19UTC00:01 to2026-10-24UTC00:01; original8Parquet, 33day context. Rolling720completedhours training excludes tested hour plus24 intervening bars; no supervised future labels, purge0.
- Fit logETH=intercept+beta*logBTC; sample residual std ddof1. Entry eligibility beta in[.5,2], finite positive residual std. Entry absZ2/2.5/3, exit crossing .5/1/1.5, center2.5/1, maximumhold48hours.
- Two separately funded10000USDT banks; ETH entry notional2000 and BTC beta_at_entry*2000, raw funded bank units[1,1], total20000. Quantities floor using tested completed-hour closes and native LOT; no NAV sizing or resizing while held, no collateral netting.
- Next signalhour+1minute actual OPEN, BTC first thenETH; failedBTC opening skipsETH. IfETH fails afterBTC fill, immediately attemptBTC unwind at same reference, paying both costs. Any residual position enters close-only recovery at subsequent hours. No invented atomic fill or free rollback.
- Existing pair: invalid fit or48h timeout closes without same-hour reentry; otherwise opposite fresh threshold closes then reverses; short spread exits whenZ<=X, long spread whenZ>=-X, handling overshoots. Same-direction fresh signals retain original quantity. Terminal closes all actual legs, rejected closes remain actual/recovery and fail qualification.
- Reuse old5bp fee/1bp halfspread/2bp slippage/.5lag20dailyvol*sqrt(q*OPEN/lag20quoteADV), actualLOT/tick/minnotional, participation<=.001, postfee1xcollateral, real funding ns/marks/rates with outflows stressed/inflows unchanged. Hourmark maintenance1% is a checked proxy, no new liquidation execution or true tick/capacity claim.
- Strict numerical gates unchanged: allcost annual/recent positive, >=9/12 positive fullmonthly folds, eachcost >=6/8 recent5d folds, local3xpositive andstrict fractions>=.6, DD3<=25%, >=4completedPAIRS, gross+fund/cost1>=2.5, no negativebankcash/rejects/marginviolations, terminalflat, >=180days.
- Whole570543point native/hourly-event clock expected, verified from actual union. Benchmark oldlong B1000/E2000 has same fundedcapital but different notional/risk and545013mark clock; preserve its original results, disclose comparison scope, no new benchmark rerun.

## Review focus

- Future or embargo-hour mutations must not change fit coefficients; tested close may change Z only.
- Same-ns funding/mark and submillisecond asynchronous events retain code order; no funding credited to new entries.
- BTC-only rejection and second-leg rejection/unwind retain actual cash/cost/quantity and recovery state.
- Count completed pairs independently of leg roundtrips; terminal and timeout exits are costed.
- Full event NAV and per-bank risk remain separate; recent40/fold boundaries inherit actual books, no reset.

## Tasks

- [x] Validate root, sync remote main under lock, read full history and old pairs; record true inaccessible literature pages.
- [x] Create features.py: fit_at(logBTC,logETH,hour,window=720,gap=24), with training/index/time metadata; check synthetic fit, embargo/test exclusion and future mutation.
- [x] Create market.py: load validated real markets and replace only decision clock with all8880hourly decisions, preserving minute/hour/funding/terminal events and structured common alignment.
- [x] Create pair_model.py: decide(side,entry_ns,recovery,feature,E,X,now_ns), open_pair/close_pair with native Decimal fill contexts and explicit rejection handling. Fixture first for threshold crossings,48h timeout, partial rejection, unwind cost, and actual recovery.
- [x] Freeze plan/specs/code bindings before PnL; reserve nine models in8+1 batches before any real feature/model evaluation.
- [x] Calculate features once, actual27scenes once, retain each scene immediately in archive and resume only missing scenes. Derive wholeNAV/folds/recent40/strict neighborhoods, finish every actual configuration.
- [x] Independently audit rollingOLS with math.fsum, all native fills/funding/segments/risk/NAV and joint decisions/pair counts; no model/trade call in audit. Export all variants/costs/folds, render and actually view six-panel sensitivity plot.
- [x] Continue originalSMA65/singleS28 from16:30to18:30 only, no rule/account reset; preserve actual16UTCfunding and same-ns pre/post state semantics. Six observation IDs, not new strategy candidates.
- [x] Run registry/snapshot/monitor checks in same lock, retain old feed rows and all protected files. Seal lightweight evidence, clean reconstructible setup/progress only, commit/push main, verify full remote tree/blobs and actual process exit0, then release own lock.

真实研究/必要核验完成，准备和审计依赖/数据抓取失败及修复保留；main发布与解锁见.git证明。
