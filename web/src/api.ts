export type TaskStatus = 'queued' | 'running' | 'succeeded' | 'failed';

export interface Task {
  id: string;
  kind: 'research' | 'backtest';
  status: TaskStatus;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
  error: string | null;
  config: {
    entry_analysis_ns?: number;
    holding_period_ns: number;
    base_asset: string;
    exchange: string;
    [key: string]: unknown;
  };
}

export type ErrorKind = 'network' | 'missing-data' | 'task-failed' | 'invalid-input' | 'not-ready' | 'server';

export class ApiError extends Error {
  constructor(
    public readonly kind: ErrorKind,
    message: string,
    public readonly detail = '',
    public readonly status?: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export interface StrategyResult {
  status: 'traded' | 'no-trade' | 'unavailable' | 'failed';
  reason: string | null;
  netPnl: number | null;
  returnRate: number | null;
  initialNav: number | null;
  funding: number | null;
  fees: number | null;
  pricePnl: number | null;
  maxDrawdown: number | null;
  entryFillNs: number | null;
  exitFillNs: number | null;
}

export interface EquityPoint {
  ts: number;
  pnl: number;
}

export interface Analysis {
  task: Task;
  entryNs: number;
  exitNs: number;
  asset: string;
  exchange: string;
  replay: StrategyResult;
  rule: StrategyResult;
  model: StrategyResult;
  equity: EquityPoint[];
  curveError: ApiError | null;
}

interface RawOutcome {
  status: 'evaluated' | 'not_run' | 'failed';
  reason?: string;
  summary?: {
    status: string;
    no_trade_reason: string | null;
    initial_nav_usdt: string;
    net_pnl_usdt: string;
    return_on_total_capital: string;
    funding_usdt: string;
    fees_usdt: string;
    two_leg_price_pnl_usdt: string;
    max_drawdown_usdt: string;
    entry_fill_ts: number | null;
    exit_fill_ts: number | null;
  };
}

interface ResearchReport {
  strategy_comparison: Partial<Record<'B0' | 'B1' | 'M1', RawOutcome>>;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(path, options);
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') throw error;
    throw new ApiError('network', '暂时连接不上分析服务，请稍后重试。', String(error));
  }

  let body: unknown;
  try {
    body = await response.json();
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') throw error;
    throw new ApiError('server', '分析服务返回了无法读取的结果。', String(error), response.status);
  }
  if (!response.ok) {
    const detailValue = (body as { detail?: unknown })?.detail;
    const detail = typeof detailValue === 'string' ? detailValue : JSON.stringify(detailValue ?? body);
    if (response.status === 422) {
      if (detail.includes('数据版本') || detail.includes('数据集') || detail.includes('数据文件')) {
        throw new ApiError('missing-data', '这个时间暂时没有足够的历史数据，请选择其他时间。', detail, 422);
      }
      throw new ApiError('invalid-input', '买入时间格式无效，请重新选择整点。', detail, 422);
    }
    if (response.status === 409) {
      throw new ApiError('not-ready', '分析仍在进行，请稍候。', detail, 409);
    }
    if (response.status === 404) {
      throw new ApiError('missing-data', '这次分析的结果暂不可用。', detail, 404);
    }
    throw new ApiError('server', '分析服务暂时不可用，请稍后重试。', detail, response.status);
  }
  return body as T;
}

export async function listAnalyses(signal?: AbortSignal): Promise<Task[]> {
  const tasks = await request<Task[]>('/api/tasks?kind=research&limit=100', { signal });
  return tasks.filter(task => typeof task.config.entry_analysis_ns === 'number');
}

export function getTask(id: string, signal?: AbortSignal): Promise<Task> {
  return request<Task>(`/api/tasks/${encodeURIComponent(id)}`, { signal });
}

export function startAnalysis(entryNs: number, signal?: AbortSignal): Promise<Task> {
  return request<Task>('/api/entry-analyses', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ entry_ns: entryNs }),
    signal,
  });
}

function numberValue(value: string | number | null | undefined): number | null {
  if (value === null || value === undefined || value === '') return null;
  const result = Number(value);
  if (!Number.isFinite(result)) {
    throw new ApiError('server', '分析结果中的数值无法读取。', String(value));
  }
  return result;
}

function strategy(outcome?: RawOutcome): StrategyResult {
  const summary = outcome?.status === 'evaluated' ? outcome.summary : undefined;
  return {
    status: !summary
      ? outcome?.status === 'failed' ? 'failed' : 'unavailable'
      : summary.status === 'no_trade' ? 'no-trade' : 'traded',
    reason: summary?.no_trade_reason ?? outcome?.reason ?? null,
    netPnl: numberValue(summary?.net_pnl_usdt),
    returnRate: numberValue(summary?.return_on_total_capital),
    initialNav: numberValue(summary?.initial_nav_usdt),
    funding: numberValue(summary?.funding_usdt),
    fees: numberValue(summary?.fees_usdt),
    pricePnl: numberValue(summary?.two_leg_price_pnl_usdt),
    maxDrawdown: numberValue(summary?.max_drawdown_usdt),
    entryFillNs: summary?.entry_fill_ts ?? null,
    exitFillNs: summary?.exit_fill_ts ?? null,
  };
}

export async function getAnalysis(task: Task, signal?: AbortSignal): Promise<Analysis> {
  if (task.status === 'failed') {
    throw new ApiError('task-failed', '这次分析未能完成，请重新分析。', task.error ?? '');
  }
  if (task.status !== 'succeeded') {
    throw new ApiError('not-ready', '分析仍在进行，请稍候。');
  }
  const entryNs = task.config.entry_analysis_ns;
  if (typeof entryNs !== 'number') {
    throw new ApiError('missing-data', '这条记录没有指定买入时间。');
  }
  const path = `/api/tasks/${encodeURIComponent(task.id)}`;
  const report = await request<ResearchReport>(`${path}/report`, { signal });
  if (!report.strategy_comparison) {
    throw new ApiError('server', '分析结果缺少回放记录。');
  }
  const replay = strategy(report.strategy_comparison.B0);
  let equity: EquityPoint[] = [];
  let curveError: ApiError | null = null;
  if (replay.initialNav !== null) {
    try {
      const rows = await request<Array<{ ts: number; nav_usdt: string }>>(
        `${path}/artifacts/equity?baseline=B0`, { signal },
      );
      equity = rows.map(row => {
        const nav = numberValue(row.nav_usdt);
        if (nav === null || !Number.isFinite(row.ts)) {
          throw new ApiError('server', '回放曲线中的数据无法读取。');
        }
        return { ts: row.ts, pnl: nav - replay.initialNav! };
      });
    } catch (error) {
      if (!(error instanceof ApiError)) throw error;
      curveError = error;
    }
  }
  return {
    task,
    entryNs,
    exitNs: entryNs + task.config.holding_period_ns,
    asset: task.config.base_asset,
    exchange: task.config.exchange,
    replay,
    rule: strategy(report.strategy_comparison.B1),
    model: strategy(report.strategy_comparison.M1),
    equity,
    curveError,
  };
}

export function chinaInput(ns: number): { date: string; hour: string } {
  const local = new Date(ns / 1_000_000 + 8 * 60 * 60 * 1000).toISOString();
  return { date: local.slice(0, 10), hour: local.slice(11, 13) };
}

export function entryFromChina(date: string, hour: string): number {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !/^(?:[01]\d|2[0-3])$/.test(hour)) {
    throw new ApiError('invalid-input', '请选择买入日期和整点时间。');
  }
  const ms = Date.parse(`${date}T${hour}:00:00+08:00`);
  if (!Number.isFinite(ms) || ms < 0) {
    throw new ApiError('invalid-input', '请选择有效的买入时间。');
  }
  const ns = ms * 1_000_000;
  const parsed = chinaInput(ns);
  if (parsed.date !== date || parsed.hour !== hour) {
    throw new ApiError('invalid-input', '请选择有效的买入时间。');
  }
  return ns;
}

export function formatChinaTime(ns: number, options: Intl.DateTimeFormatOptions = {}): string {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
    ...options,
    timeZone: 'Asia/Shanghai',
  }).format(new Date(ns / 1_000_000));
}
