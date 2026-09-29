// Run with: node --experimental-transform-types checks/frontend_api.mjs
import assert from 'node:assert/strict';
import { ApiError, chinaInput, entryFromChina, getAnalysis, startAnalysis } from '../web/src/api.ts';

const entryNs = 1789430400000000000;
assert.equal(entryFromChina('2026-09-15', '08'), entryNs);
assert.deepEqual(chinaInput(entryNs), { date: '2026-09-15', hour: '08' });
assert.throws(() => entryFromChina('2026-02-31', '08'), ApiError);

const task = {
  id: 'entry-check', status: 'succeeded',
  config: { entry_analysis_ns: entryNs, holding_period_ns: 86400000000000, base_asset: 'BTC', exchange: 'binance' },
};
const summary = {
  status: 'completed', initial_nav_usdt: '20000', net_pnl_usdt: '-2.69014786',
  return_on_total_capital: '-0.000134507393', funding_usdt: '0.12262664',
  fees_usdt: '2.30727450', two_leg_price_pnl_usdt: '-0.5055', max_drawdown_usdt: '2.69014786',
  entry_fill_ts: entryNs + 60000000000, exit_fill_ts: entryNs + 86400000000000,
};
const report = { strategy_comparison: {
  B0: { status: 'evaluated', summary },
  B1: { status: 'evaluated', summary: { ...summary, status: 'no_trade', net_pnl_usdt: '0', no_trade_reason: 'expected_net_not_above_buffer' } },
  M1: { status: 'not_run', reason: 'no_fitted_ridge_forecasts' },
} };

let curveStatus = 200;
globalThis.fetch = async (path, options) => {
  if (path === '/api/entry-analyses') {
    assert.deepEqual(JSON.parse(options.body), { entry_ns: entryNs });
    return Response.json(task, { status: 202 });
  }
  if (path.endsWith('/report')) return Response.json(report);
  assert.ok(path.endsWith('/artifacts/equity?baseline=B0'));
  return curveStatus === 200
    ? Response.json([{ ts: entryNs, nav_usdt: '20000' }, { ts: entryNs + 86400000000000, nav_usdt: '19997.30985214' }])
    : Response.json({ detail: '明细文件不存在' }, { status: curveStatus });
};
await startAnalysis(entryFromChina('2026-09-15', '08'));
const analysis = await getAnalysis(task);
assert.equal(analysis.replay.netPnl, -2.69014786);
assert.equal(analysis.rule.status, 'no-trade');
assert.equal(analysis.model.status, 'unavailable');
assert.equal(analysis.equity[0].pnl, 0);
assert.ok(Math.abs(analysis.equity.at(-1).pnl - analysis.replay.netPnl) < 1e-8);
curveStatus = 404;
const missingCurve = await getAnalysis(task);
assert.deepEqual(missingCurve.equity, []);
assert.equal(missingCurve.curveError.kind, 'missing-data');
assert.equal(missingCurve.replay.netPnl, analysis.replay.netPnl);
await assert.rejects(getAnalysis({ ...task, status: 'failed', error: 'worker exited' }), { kind: 'task-failed' });
globalThis.fetch = async () => Response.json({ detail: '没有覆盖该建仓时间且满足研究窗口要求的数据版本' }, { status: 422 });
await assert.rejects(startAnalysis(entryNs), { kind: 'missing-data' });
globalThis.fetch = async () => { throw new TypeError('network unavailable'); };
await assert.rejects(startAnalysis(entryNs), { kind: 'network' });
console.log('Frontend semantics passed: UTC submission, separate no-trade result, real equity, explicit failures.');
