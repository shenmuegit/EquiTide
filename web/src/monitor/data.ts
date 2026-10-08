export type Cost = '1' | '2' | '3';
export type Weight = { asset: string; weight: number; indicator?: string };
export type PaperScene = {
  nav: string; pnl: string; return_pct: number; drawdown_pct: number; cost: string;
  cost_parts: Record<string, string>; executions: number; round_trips: number;
  positions: Record<string, { units: string; cash_usdt: string; desired_long: boolean; last_signal_open_ms: number | null }>;
};
export type PaperAccount = {
  id: string; label: string; capital_usdt: string; weights: Weight[]; scenes: Record<Cost, PaperScene>;
  coverage_fraction: number; source_spec: string; source_fingerprint: string; criteria: Record<string, boolean>;
};
export type Totals = { nav: string; pnl: string; return_pct: number; cost: string; fee: string; executions: number; round_trips: number };
export type Operation = { id: string; at: string | null; mode: string; error?: string; virtual_orders: number; report: string };
export type Trade = {
  trade_id: string; portfolio: string; asset: string; side: string; cost_multiplier: number; status: string;
  quantity?: string; execution?: string; cost_usdt?: string; cost_parts?: Record<string, string>;
  simulated_at_utc?: string; quote_observed_at_utc?: string; signal_available_at_utc?: string;
};
export type Paper = {
  status: 'ready' | 'degraded' | 'unavailable'; errors: string[]; observation_id: string;
  observed_at_utc: string; start_utc: string; end_utc: string; elapsed_seconds: number;
  duration_days: number; fold_days: number; observation_count: number; maximum_gap_seconds: number;
  coverage_gaps: unknown[]; plan_sha256: string; state_sha256: string; report_sha256: string;
  accounts: PaperAccount[]; totals: Record<Cost, Totals>;
  history: { at: string; totals: Record<Cost, Totals>; returns: Record<string, Record<Cost, number>> }[];
  trades: Trade[]; operations: Operation[]; report: string; trade_count: number;
  decisions: { portfolio: string; asset: string; execution_delay_seconds: number; signal_available_at_utc: string;
    context: Record<string, string | number | boolean> }[];
};
export type ResearchScene = {
  return_pct: number; drawdown_pct: number; sharpe: number | null; cost: number | null;
  executions: number | null; round_trips: number | null; nav_hash: string | null;
  fold_returns_pct: number[]; fold_drawdowns_pct: (number | null)[]; first_five_return_pct: number | null;
};
export type ResearchConfig = {
  fingerprint: string; name: string; family: string; kind: 'strategy' | 'combination'; indicator: string;
  weights: Weight[]; capital_usdt: number | null; start_utc: string; end_utc: string; status: string;
  cross_period_passed: boolean; scenes: Partial<Record<Cost, ResearchScene>>; criteria: Record<string, boolean>;
  failed_criteria: string[]; positive_folds_1x: number | null; report: string; spec_path: string | null;
  validation: { walk_forward_folds: number; cost_scenarios: string[]; sensitivity_recorded: boolean };
  spec: { name: string; kind: string; family: string; parameters: Record<string, string | number | boolean> };
};
export type ResearchRound = { id: string; at: string | null; new_configs: number; passed: number; rejected: number;
  new_cross_period_pairs: number; report: string; result: string };
export type Snapshot = {
  schema_version: number; generated_at_utc: string; source_commit: string; source_repository: string;
  refresh: { paper_seconds: number; feed_seconds: number; quote_seconds: number };
  paper: Paper; research: {
    last_run: ResearchRound | null; registry_sha256: string; counts: Record<string, number>;
    configs_path: string; configs_sha256: string; periods: { start_utc: string; end_utc: string }[];
    rounds: ResearchRound[]; unranked: { fingerprint: string; family: string; status: string; result_available: boolean; report: string | null }[];
  };
};
export type Quote = { symbol: string; bid: number; ask: number; mid: number; observedAt: string; latency: number };

const REPOSITORY = 'https://github.com/shenmuegit/EquiTide/blob/codex/strategy-research/';
export const FEED_URL = import.meta.env.VITE_MONITOR_FEED_URL || 'https://raw.githubusercontent.com/shenmuegit/EquiTide/codex/strategy-research/research/monitor/latest.json';
export const evidenceUrl = (path: string) => REPOSITORY + path.split('/').map(encodeURIComponent).join('/');

export async function fetchSnapshot(signal: AbortSignal): Promise<Snapshot> {
  const response = await fetch(FEED_URL, { signal: AbortSignal.any([signal, AbortSignal.timeout(20_000)]), cache: 'no-cache' });
  if (!response.ok) throw new Error(`研究账本暂不可用（${response.status}）`);
  const data = await response.json();
  if (data.schema_version !== 1 || !data.paper || !data.research?.configs_sha256) throw new Error('研究数据格式异常，保留上次有效记录');
  return data;
}

export async function fetchResearch(snapshot: Snapshot, signal: AbortSignal): Promise<ResearchConfig[]> {
  const response = await fetch(new URL(snapshot.research.configs_path, new URL(FEED_URL, location.href)), { signal: AbortSignal.any([signal, AbortSignal.timeout(20_000)]), cache: 'no-cache' });
  if (!response.ok) throw new Error('研究排名暂不可用，请稍后刷新');
  const stream = response.body?.pipeThrough(new DecompressionStream('gzip'));
  if (!stream) throw new Error('研究排名未返回完整数据');
  const raw = await new Response(stream).arrayBuffer();
  const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', raw)), b => b.toString(16).padStart(2, '0')).join('');
  if (hash !== snapshot.research.configs_sha256) throw new Error('研究排名正在同步，保留上次有效排名');
  const rows = JSON.parse(new TextDecoder().decode(raw));
  if (!Array.isArray(rows) || rows.length !== snapshot.research.counts.ranked) throw new Error('研究排名完整性检查未通过');
  return rows;
}

export async function fetchQuote(symbol: 'BTCUSDT' | 'ETHUSDT', signal: AbortSignal): Promise<Quote> {
  const started = performance.now();
  const response = await fetch(`https://data-api.binance.vision/api/v3/ticker/bookTicker?symbol=${symbol}`, { signal: AbortSignal.any([signal, AbortSignal.timeout(8_000)]), cache: 'no-store' });
  if (!response.ok) throw new Error(`${symbol} 行情请求失败（${response.status}）`);
  const data = await response.json();
  const bid = Number(data.bidPrice), ask = Number(data.askPrice);
  if (data.symbol !== symbol || !Number.isFinite(bid) || !Number.isFinite(ask) || bid <= 0 || ask < bid)
    throw new Error(`${symbol} 报价校验失败`);
  return { symbol, bid, ask, mid: (bid + ask) / 2, observedAt: new Date().toISOString(), latency: performance.now() - started };
}

export function comparableRows(rows: ResearchConfig[], start: string, end: string, kind: string, cost: Cost) {
  return rows.filter(r => r.start_utc === start && r.end_utc === end && r.kind === kind && r.scenes[cost]
    && (kind !== 'combination' || r.capital_usdt === 2000));
}

// Shared display formatting; chart code is loaded only after ledger content.
export const COSTS: Cost[] = ['1', '2', '3'];
export const COLORS = ['var(--chart-main)', 'var(--chart-secondary)', 'var(--chart-stress)'];
export const number = (value: string | number | null | undefined, digits = 2) => value == null ? '暂无' :
  Number(value).toLocaleString('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits });
export const signed = (value: string | number, digits = 2) => `${Number(value) > 0 ? '+' : Number(value) < 0 ? '−' : ''}${number(Math.abs(Number(value)), digits)}`;
export const tone = (value: string | number) => Number(value) > 0 ? 'positive' : Number(value) < 0 ? 'negative' : 'neutral';
export const date = (value: string | null | undefined, short = false) => value ? new Intl.DateTimeFormat('zh-CN', {
  timeZone: 'Asia/Shanghai', month: '2-digit', day: '2-digit', ...(short ? {} : { year: 'numeric' }),
  hour: '2-digit', minute: '2-digit', hour12: false,
}).format(new Date(value)) : '暂无';
export const clock = (value: number | string) => new Intl.DateTimeFormat('zh-CN', {
  timeZone: 'Asia/Shanghai', hour: '2-digit', minute: '2-digit', hour12: false,
}).format(new Date(value));
