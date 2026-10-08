import { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowClockwise, ArrowUpRight, CaretDown, ChartLine, ClockCounterClockwise, Flask,
  MagnifyingGlass, Moon, Pause, Play, Sun, WarningCircle, X, CheckCircle, GithubLogo } from '@phosphor-icons/react';
import { CartesianGrid, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { comparableRows, evidenceUrl, fetchQuote, fetchResearch, fetchSnapshot } from './data';
import type { Cost, Paper, PaperAccount, Quote, ResearchConfig, Snapshot, Weight } from './data';

const COSTS: Cost[] = ['1', '2', '3'];
const COLORS = ['#a3dfb2', '#d3ba89', '#91b6d0'];
const number = (value: string | number | null | undefined, digits = 2) => value == null ? '—' :
  Number(value).toLocaleString('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits });
const signed = (value: string | number, digits = 2) => `${Number(value) > 0 ? '+' : Number(value) < 0 ? '−' : ''}${number(Math.abs(Number(value)), digits)}`;
const tone = (value: string | number) => Number(value) > 0 ? 'positive' : Number(value) < 0 ? 'negative' : 'neutral';
const date = (value: string | null | undefined, short = false) => value ? new Intl.DateTimeFormat('zh-CN', {
  timeZone: 'Asia/Shanghai', month: '2-digit', day: '2-digit', ...(short ? {} : { year: 'numeric' }),
  hour: '2-digit', minute: '2-digit', hour12: false,
}).format(new Date(value)) : '—';
const clock = (value: number | string) => new Intl.DateTimeFormat('zh-CN', {
  timeZone: 'Asia/Shanghai', hour: '2-digit', minute: '2-digit', hour12: false,
}).format(new Date(value));
const elapsed = (seconds: number) => seconds >= 86400 ? `${number(seconds / 86400, 1)} 天` : `${number(seconds / 3600, 1)} 小时`;
const weights = (items: Weight[]) => items.length ? items.map(w => `${w.asset} ${number(w.weight * 100, w.weight * 100 % 1 ? 1 : 0)}%`).join(' / ') : '独立单币配置';

function failureLabel(key: string) {
  if (/four_positive|positive_folds/.test(key)) return '至少4折盈利';
  if (/drawdown|max_dd/.test(key)) return '整体回撤不超过25%';
  if (/positive_all|positive_.*cost/.test(key)) return '各成本档位净收益为正';
  if (/gross|cost.*ratio|cost_margin/.test(key)) return '毛收益覆盖成本门槛';
  if (/round_trip|two_round/.test(key)) return '至少2次完整往返';
  if (/six.*fold|fold_count/.test(key)) return '6个连续验证窗口';
  if (/minimum180/.test(key)) return '至少180天观察';
  if (/terminal/.test(key)) return '期末持仓条件';
  if (/cash|balance/.test(key)) return '账户余额守恒';
  if (/coverage/.test(key)) return '有效观察覆盖率';
  return key.replaceAll('_', ' ');
}

function useEvidence(enabled: boolean, refreshKey: number) {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [configs, setConfigs] = useState<ResearchConfig[]>([]);
  const [error, setError] = useState('');
  const [researchError, setResearchError] = useState('');
  const [reading, setReading] = useState(false);
  const [receivedAt, setReceivedAt] = useState('');
  const loadedResearch = useRef('');
  const lastRefresh = useRef(0);
  useEffect(() => {
    const manual = refreshKey !== lastRefresh.current;
    lastRefresh.current = refreshKey;
    if (!enabled && !manual) { setReading(false); return; }
    let active = true, busy = false;
    const controller = new AbortController();
    const run = async () => {
      if (document.hidden || busy) return;
      busy = true; setReading(true);
      try {
        const next = await fetchSnapshot(controller.signal);
        if (!active) return;
        setSnapshot(next); setError(''); setReceivedAt(new Date().toISOString());
        if (loadedResearch.current !== next.research.configs_sha256) {
          try {
            const rows = await fetchResearch(next, controller.signal);
            if (!active) return;
            loadedResearch.current = next.research.configs_sha256;
            setConfigs(rows); setResearchError('');
          } catch (err) {
            if (active) setResearchError(err instanceof Error ? err.message : '研究排名暂不可用');
          }
        }
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : '读取账本失败');
      } finally { busy = false; if (active) setReading(false); }
    };
    void run();
    const timer = enabled ? window.setInterval(() => void run(), 30_000) : undefined;
    const visible = () => { if (enabled && !document.hidden) void run(); };
    document.addEventListener('visibilitychange', visible);
    return () => { active = false; controller.abort(); window.clearInterval(timer); document.removeEventListener('visibilitychange', visible); };
  }, [enabled, refreshKey]);
  return { snapshot, configs, error, researchError, reading, receivedAt };
}

function useQuotes(enabled: boolean, refreshKey: number) {
  const [quotes, setQuotes] = useState<Record<string, Quote>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const lastRefresh = useRef(0);
  useEffect(() => {
    const manual = refreshKey !== lastRefresh.current;
    lastRefresh.current = refreshKey;
    if (!enabled && !manual) return;
    let active = true, busy = false;
    const controller = new AbortController();
    const run = async () => {
      if (document.hidden || busy) return;
      busy = true;
      await Promise.allSettled((['BTCUSDT', 'ETHUSDT'] as const).map(async symbol => {
        try {
          const quote = await fetchQuote(symbol, controller.signal);
          if (active) { setQuotes(prior => ({ ...prior, [symbol]: quote })); setErrors(prior => ({ ...prior, [symbol]: '' })); }
        } catch (err) { if (active) setErrors(prior => ({ ...prior, [symbol]: err instanceof Error ? err.message : '行情暂不可用' })); }
      }));
      busy = false;
    };
    void run();
    const timer = enabled ? window.setInterval(() => void run(), 10_000) : undefined;
    const visible = () => { if (enabled && !document.hidden) void run(); };
    document.addEventListener('visibilitychange', visible);
    return () => { active = false; controller.abort(); window.clearInterval(timer); document.removeEventListener('visibilitychange', visible); };
  }, [enabled, refreshKey]);
  return { quotes, errors };
}

function Brand() {
  return <span className="brand"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M3 18c5-14 8 14 13 0s8 14 13-5" /></svg><span>EquiTide<small>RESEARCH MONITOR</small></span></span>;
}

function QuoteTile({ symbol, quote, error, now, paused }: { symbol: string; quote?: Quote; error?: string; now: number; paused: boolean }) {
  const stale = !quote || now - Date.parse(quote.observedAt) > 45_000 || !!error;
  return <div className="quote-tile">
    <div className={`coin ${symbol === 'BTC' ? 'btc' : 'eth'}`} aria-hidden="true">{symbol === 'BTC' ? '₿' : 'Ξ'}</div>
    <div className="quote-content"><div className="quote-label"><b>{symbol}<span>/ USDT</span></b>
      <span className={`market-state ${stale ? 'warning' : ''}`}>{stale ? '待更新' : paused ? '已暂停' : '实时中间价'}</span></div>
      <div className="quote-value mono">{quote ? number(quote.mid) : '—'}<small>USDT</small></div>
      <div className="quote-bottom">买一 <span className="mono">{quote ? number(quote.bid) : '—'}</span><i />卖一 <span className="mono">{quote ? number(quote.ask) : '—'}</span></div>
      <div className="quote-time" title={error || '接收时间；bookTicker接口不提供成交事件时间'}>
        {error ? '请求失败 · 保留上次报价' : quote ? `接收于 ${clock(quote.observedAt)} · ${number(quote.latency, 0)} ms` : '正在连接 Binance 公开行情…'}
      </div>
    </div>
  </div>;
}

function Metric({ label, value, sub, valueTone = '', unit }: { label: string; value: string; sub: string; valueTone?: string; unit?: string }) {
  return <div className="metric"><span className="metric-label">{label}</span><div className={`metric-value mono ${valueTone}`}>{value}<small>{unit}</small></div><span className="metric-sub">{sub}</span></div>;
}

function CostSelector({ value, onChange, label = '成本情景' }: { value: Cost; onChange: (v: Cost) => void; label?: string }) {
  return <div className="segmented" role="group" aria-label={label}>{COSTS.map(cost => <button type="button" key={cost}
    aria-pressed={value === cost} className={value === cost ? 'selected' : ''} onClick={() => onChange(cost)}>{cost}×{cost === '1' ? ' 主账户' : ' 成本'}</button>)}</div>;
}

function PanelHeading({ title, sub, children }: { title: string; sub?: string; children?: React.ReactNode }) {
  return <div className="panel-heading"><div><h2>{title}</h2>{sub && <p>{sub}</p>}</div>{children}</div>;
}

function EvidenceLink({ path, children = '查看证据' }: { path: string; children?: React.ReactNode }) {
  return <a className="text-link" href={evidenceUrl(path)} target="_blank" rel="noreferrer">{children}<ArrowUpRight size={14} /></a>;
}

function EquityChart({ paper, account }: { paper: Paper; account?: string }) {
  const points = useMemo(() => paper.history.map(row => ({ time: Date.parse(row.at),
    '1': account ? row.returns[account]?.['1'] : row.totals['1'].return_pct,
    '2': account ? row.returns[account]?.['2'] : row.totals['2'].return_pct,
    '3': account ? row.returns[account]?.['3'] : row.totals['3'].return_pct })), [paper.history, account]);
  return <div className="equity-chart" role="img" aria-label={`${account || '十组账户合计'}在${paper.observation_count}次真实观察中的成本后累计收益率曲线；回撤限于采样点`}>
    <ResponsiveContainer width="100%" height="100%"><LineChart data={points} margin={{ top: 8, right: 12, bottom: 0, left: -18 }} accessibilityLayer>
      <CartesianGrid stroke="var(--grid)" vertical={false} strokeDasharray="3 5" />
      <XAxis dataKey="time" type="number" domain={['dataMin', 'dataMax']} tickFormatter={clock} minTickGap={45} tick={{ fill: 'var(--muted)', fontSize: 11 }} axisLine={false} tickLine={false} />
      <YAxis tickFormatter={v => `${number(v, 2)}%`} tick={{ fill: 'var(--muted)', fontSize: 11 }} axisLine={false} tickLine={false} domain={['auto', 'auto']} />
      <ReferenceLine y={0} stroke="var(--border)" />
      <Tooltip labelFormatter={v => date(new Date(Number(v)).toISOString())} formatter={(v, name) => [`${signed(Number(v), 4)}%`, `${name}×成本`]} contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12, color: 'var(--text)' }} />
      {COSTS.map((cost, i) => <Line key={cost} type="linear" dataKey={cost} stroke={COLORS[i]} strokeWidth={cost === '1' ? 2 : 1.5} dot={{ r: 3, strokeWidth: 0 }} activeDot={{ r: 5 }} isAnimationActive={false} />)}
    </LineChart></ResponsiveContainer>
  </div>;
}

function Position({ scene }: { scene: PaperAccount['scenes']['1'] }) {
  const held = Object.entries(scene.positions).filter(([, p]) => Number(p.units) > 0);
  return held.length ? <span className="positions">{held.map(([asset, p]) => <span key={asset}><b>{asset}</b> <span className="mono">{number(p.units, asset === 'BTC' ? 5 : 4)}</span></span>)}</span> : <span className="cash-label">USDT 空仓</span>;
}

function PaperView({ paper, now, onSelect }: { paper: Paper; now: number; onSelect: (a: PaperAccount) => void }) {
  const [cost, setCost] = useState<Cost>('1');
  const [chartAccount, setChartAccount] = useState('');
  if (paper.status === 'unavailable') return <div className="empty-state"><WarningCircle size={32} /><h2>尚无完整模拟盘观察</h2><p>{paper.errors.join('；')}</p></div>;
  const total = paper.totals[cost];
  const days = paper.elapsed_seconds / 86400;
  const stale = now - Date.parse(paper.observed_at_utc) > paper.maximum_gap_seconds * 1000;
  const accounts = [...paper.accounts].sort((a, b) => b.scenes[cost].return_pct - a.scenes[cost].return_pct || a.id.localeCompare(b.id));
  const winners = paper.accounts.filter(a => a.scenes[cost].return_pct > 0).length;
  return <>
    {(stale || paper.status === 'degraded') && <div className="alert" role="status"><WarningCircle size={19} /><span>{paper.errors.length ? paper.errors.join('；') : '模拟盘采样已超过3小时，请检查执行任务；以下保留最后有效账本。'}</span></div>}
    <div className="page-title"><div><div className="eyebrow">真实行情 · 虚拟资金</div><h1>模拟盘<span className="badge">{days >= 180 ? '等待完整评审' : '持续观察中'}</span></h1></div>
      <div className="updated-note">账本采样时间<strong>{date(paper.observed_at_utc)} 北京时间</strong></div></div>
    <div className="metrics-strip">
      <Metric label={cost === '1' ? '主账户总资产' : `${cost}×成本情景总资产`} value={number(total.nav)} unit="USDT" sub="10组独立账户 · 初始资金 20,000 USDT" />
      <Metric label="成本后累计盈亏" value={signed(total.pnl)} unit="USDT" valueTone={tone(total.pnl)} sub={`${signed(total.return_pct, 4)}% 累计收益 · ${winners}/10组正收益`} />
      <Metric label="虚拟成交" value={number(total.executions, 0)} unit="笔" sub={`${total.round_trips}次完整往返 · 累计手续费 ${number(total.fee, 4)} USDT`} />
      <Metric label="实际观察" value={elapsed(paper.elapsed_seconds)} sub={`${paper.observation_count}次有效采样 · ${paper.coverage_gaps.length}段记录缺口`} />
    </div>
    <div className="overview-grid">
      <section className="panel chart-panel"><PanelHeading title="累计净收益" sub="只连接已保存的真实观察点，市场报价不改写账户净值。">
        <label className="select-wrap"><span className="sr-only">选择收益曲线账户</span><select value={chartAccount} onChange={e => setChartAccount(e.target.value)}><option value="">10组账户合计</option>{paper.accounts.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}</select><CaretDown size={13} /></label>
      </PanelHeading><EquityChart paper={paper} account={chartAccount || undefined} /><div className="chart-legend">{COSTS.map((c, i) => <span key={c}><i style={{ background: COLORS[i] }} />{c}×{c === '1' ? ' 主账户' : ' 成本'}</span>)}<span className="legend-note">采样口径回撤</span></div></section>
      <section className="panel progress-panel"><PanelHeading title="前向验证进度" /><div className="progress-number mono">{number(days, 2)}<span>/ 180 天</span></div>
        <progress value={Math.min(days, 180)} max={180} aria-label="180天前向测试进度" />
        <div className="window-track">{Array.from({ length: 6 }, (_, i) => <div key={i} className={days >= (i + 1) * 30 ? 'done' : days >= i * 30 ? 'current' : ''}><span>W{i + 1}</span><small>{(i + 1) * 30}天</small></div>)}</div>
        <p className="progress-copy">6个连续30天窗口。样本仍在积累，<strong>尚未通过完整验证</strong>。</p>
        <dl className="mini-facts"><div><dt>启动时间</dt><dd>{date(paper.start_utc, true)}</dd></div><div><dt>完整评审日期</dt><dd>{date(paper.end_utc)}</dd></div><div><dt>交易规则</dt><dd>UTC闭合日线 · 现货只做多</dd></div></dl>
      </section>
    </div>
    <section className="panel account-panel"><PanelHeading title="10组固定策略" sub="按所选成本情景的累计收益倒序；权重为初始分仓，不自动再平衡。"><CostSelector value={cost} onChange={setCost} /></PanelHeading>
      <div className="table-scroll" tabIndex={0} aria-label="模拟账户表，可横向滚动"><table className="account-table"><thead><tr><th>策略 / 技术指标</th><th>BTC / ETH 初始权重</th><th className="right">净收益率 ↓</th><th className="right">盈亏 USDT</th><th className="right">采样回撤</th><th>当前持仓</th><th className="right">成交</th><th><span className="sr-only">账户详情</span></th></tr></thead>
        <tbody>{accounts.map(a => { const s = a.scenes[cost]; return <tr key={a.id}><td><div className="strategy-cell"><span className="strategy-id mono">{a.id}</span><span><b>{a.label}</b><small>{a.weights.map(w => w.indicator).join(' · ')}</small></span></div></td><td className="mono muted">{a.weights.map(w => number(w.weight * 100, 1).replace('.0', '')).join(' / ')}<small className="percent-unit">%</small></td><td className={`right mono ${tone(s.return_pct)}`}>{signed(s.return_pct, 4)}%</td><td className={`right mono ${tone(s.pnl)}`}>{signed(s.pnl, 4)}</td><td className="right mono">{number(s.drawdown_pct, 4)}%</td><td><Position scene={s} /></td><td className="right mono">{s.executions}</td><td><button className="icon-button row-detail" onClick={() => onSelect(a)} aria-label={`查看 ${a.id} 详情`}><ArrowUpRight size={18} /></button></td></tr>; })}</tbody>
      </table></div>
      <div className="panel-foot"><span>手续费、观察点差、滑点及成交量冲击已计入；回撤限于实际净值采样。</span><EvidenceLink path={paper.report}>本轮账本</EvidenceLink></div>
    </section>
  </>;
}

function ResearchView({ snapshot, configs, error, onSelect }: { snapshot: Snapshot; configs: ResearchConfig[]; error: string; onSelect: (r: ResearchConfig) => void }) {
  const research = snapshot.research;
  const [cost, setCost] = useState<Cost>('3');
  const [kind, setKind] = useState('combination');
  const [period, setPeriod] = useState('2026-03-18T00:01:00Z|2026-09-14T00:01:00Z');
  const [status, setStatus] = useState('all');
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState('return');
  const [page, setPage] = useState(1);
  const [start, end] = period.split('|');
  const comparable = useMemo(() => comparableRows(configs, start, end, kind, cost), [configs, start, end, kind, cost]);
  const filtered = useMemo(() => comparable.filter(r => (status === 'all' || (status === 'cross' ? r.cross_period_passed : r.status === status))
    && `${r.name} ${r.indicator} ${r.family} ${weights(r.weights)}`.toLowerCase().includes(query.toLowerCase())).sort((a, b) =>
    sort === 'drawdown' ? a.scenes[cost]!.drawdown_pct - b.scenes[cost]!.drawdown_pct : b.scenes[cost]!.return_pct - a.scenes[cost]!.return_pct),
  [comparable, status, query, sort, cost]);
  const pages = Math.max(1, Math.ceil(filtered.length / 25));
  const safePage = Math.min(page, pages);
  const rows = filtered.slice((safePage - 1) * 25, safePage * 25);
  const passed = comparable.filter(r => r.status === 'passed').length;
  const positive = comparable.filter(r => r.scenes[cost]!.return_pct > 0).length;
  const cross = comparable.filter(r => r.cross_period_passed).length;
  const latest = research.last_run;
  return <>
    <div className="page-title"><div><div className="eyebrow">历史回测 · 持续挖掘</div><h1>策略研究<span className="badge">{research.counts.registered.toLocaleString()}个独立配置</span></h1></div><div className="updated-note">最新研究轮次<strong>{latest ? date(latest.at) : '—'}</strong></div></div>
    {error && <div className="alert" role="status"><WarningCircle size={18} />{error}</div>}
    <div className="metrics-strip research-metrics">
      <Metric label="已有实际回测" value={number(research.counts.results, 0)} unit="配置" sub={`${research.counts.observation_records_excluded}条持续观察记录已单独统计`} />
      <Metric label="当前区间正收益" value={number(positive, 0)} unit={`/ ${comparable.length}`} sub={`${cost}×成本 · 相同时间区间、配置类型`} valueTone="positive" />
      <Metric label="当前区间通过门槛" value={number(passed, 0)} unit="配置" sub="结合逐折盈利、整体回撤、交易及成本条件" />
      <Metric label="跨2025/2026通过" value={number(cross, 0)} unit="配置" sub="两个时期均通过历史门槛 · 非独立最终测试集" />
    </div>
    <div className="research-context"><div><Flask size={20} /><span>这些历史区间已反复用于研究。参数敏感性以原批次报告为准；历史通过不代表稳定实盘盈利。</span></div>{latest && <EvidenceLink path={latest.result}>最新中文结论</EvidenceLink>}</div>
    <section className="panel research-panel"><PanelHeading title="收益排名" sub={kind === 'combination' ? '同区间、初始本金2,000 USDT的组合比较；配置不按指标族合并。' : '同区间的单币组件比较；各组件原始本金见详情。'}><CostSelector value={cost} onChange={v => { setCost(v); setPage(1); }} label="研究成本档位" /></PanelHeading>
      <div className="research-filters">
        <label className="search-box"><MagnifyingGlass size={17} /><span className="sr-only">搜索技术指标、参数或权重</span><input placeholder="搜索指标、参数或权重…" value={query} onChange={e => { setQuery(e.target.value); setPage(1); }} /></label>
        <label className="select-wrap"><span className="sr-only">回测区间</span><select value={period} onChange={e => { setPeriod(e.target.value); setPage(1); }}>{research.periods.map(p => <option key={p.start_utc + p.end_utc} value={`${p.start_utc}|${p.end_utc}`}>{p.start_utc.slice(0, 10)} — {p.end_utc.slice(0, 10)} UTC</option>)}</select><CaretDown size={13} /></label>
        <label className="select-wrap"><span className="sr-only">配置类型</span><select value={kind} onChange={e => { setKind(e.target.value); setPage(1); }}><option value="combination">BTC / ETH 组合</option><option value="strategy">单币策略组件</option></select><CaretDown size={13} /></label>
        <label className="select-wrap"><span className="sr-only">验证筛选</span><select value={status} onChange={e => { setStatus(e.target.value); setPage(1); }}><option value="all">全部验证状态</option><option value="passed">通过历史门槛</option><option value="rejected">未通过历史门槛</option><option value="cross">跨两个时期通过</option></select><CaretDown size={13} /></label>
        <label className="select-wrap"><span className="sr-only">排名排序</span><select value={sort} onChange={e => { setSort(e.target.value); setPage(1); }}><option value="return">收益率倒序</option><option value="drawdown">回撤从低到高</option></select><CaretDown size={13} /></label>
      </div>
      <div className="research-summary"><span>当前筛选 <b>{filtered.length}</b> 个配置</span><span>正收益 {positive} · 通过 {passed} · 未通过 {comparable.length - passed}</span></div>
      <div className="table-scroll" tabIndex={0} aria-label="研究收益榜，可横向滚动"><table className="research-table"><thead><tr><th className="rank-col">#</th><th>技术指标 / 参数</th><th>原始权重</th><th className="right">{cost}×净收益 {sort === 'return' ? '↓' : ''}</th><th className="right">整体回撤</th><th className="right">1×盈利折</th><th>验证状态</th><th><span className="sr-only">配置详情</span></th></tr></thead><tbody>{rows.map((r, i) => { const s = r.scenes[cost]!; return <tr key={r.fingerprint}><td className="mono muted">{(safePage - 1) * 25 + i + 1}</td><td><button className="strategy-link" onClick={() => onSelect(r)}>{r.indicator}</button><small className="config-name mono">{r.name}</small></td><td className="weight-text">{weights(r.weights)}</td><td className={`right mono ${tone(s.return_pct)}`}>{signed(s.return_pct)}%</td><td className="right mono">{number(s.drawdown_pct)}%</td><td className="right mono">{r.positive_folds_1x ?? r.scenes['1']?.fold_returns_pct.filter(x => x > 0).length ?? '—'}<span className="muted"> / {r.validation.walk_forward_folds || '—'}</span></td><td><span className={`status-label ${r.status === 'passed' ? 'positive' : 'muted'}`}>{r.status === 'passed' ? <CheckCircle size={14} /> : <X size={14} />}{r.status === 'passed' ? '历史通过' : '未通过'}</span>{r.cross_period_passed && <small className="cross-period">跨两期通过</small>}</td><td><button className="icon-button row-detail" onClick={() => onSelect(r)} aria-label={`查看研究配置 ${r.name}`}><ArrowUpRight size={18} /></button></td></tr>; })}</tbody></table></div>
      {!configs.length && <div className="table-empty">{error || '正在读取并核验研究结果…'}</div>}
      {!!configs.length && !rows.length && <div className="table-empty">没有符合当前条件的配置。可调整区间或筛选条件。</div>}
      <div className="pagination"><span>第 {safePage} / {pages} 页 · 每页25条</span><div><button disabled={safePage <= 1} onClick={() => setPage(safePage - 1)}>上一页</button><button disabled={safePage >= pages} onClick={() => setPage(safePage + 1)}>下一页</button></div></div>
      <div className="panel-foot"><span>另有 {research.counts.unranked} 个历史配置无同格式可比指标，保留原始结果并排除出此收益榜。等效净值不代表独立验证。</span><EvidenceLink path="research/automation/registry.jsonl">完整登记</EvidenceLink></div>
    </section>
  </>;
}

function ActivityView({ snapshot }: { snapshot: Snapshot }) {
  const paper = snapshot.paper;
  const [cost, setCost] = useState<Cost>('1');
  const trades = (paper.trades || []).filter(t => String(t.cost_multiplier) === cost).slice().reverse();
  return <>
    <div className="page-title"><div><div className="eyebrow">执行证据 · 更新记录</div><h1>运行记录</h1></div><span className="readonly-label">只读 · 无交易入口</span></div>
    <section className="panel"><PanelHeading title="虚拟成交账本" sub="成交使用当时观察到的公开买卖报价；无历史订单倒填。"><CostSelector value={cost} onChange={setCost} /></PanelHeading>
      <div className="table-scroll" tabIndex={0} aria-label="虚拟成交表"><table><thead><tr><th>模拟成交时间 · 北京</th><th>账户</th><th>方向</th><th>资产</th><th className="right">数量</th><th className="right">执行价格 USDT</th><th className="right">总成本 USDT</th><th>信号到执行</th></tr></thead><tbody>{trades.map(t => <tr key={t.trade_id}><td className="mono">{date(t.simulated_at_utc)}</td><td className="mono">{t.portfolio}</td><td className={t.side === 'buy' ? 'positive' : 'negative'}>{t.side === 'buy' ? '买入' : '卖出'}</td><td>{t.asset}</td><td className="right mono">{number(t.quantity, 8)}</td><td className="right mono">{number(t.execution)}</td><td className="right mono">{number(t.cost_usdt, 6)}</td><td>{t.simulated_at_utc && t.signal_available_at_utc ? elapsed((Date.parse(t.simulated_at_utc) - Date.parse(t.signal_available_at_utc)) / 1000) : '—'}</td></tr>)}</tbody></table></div>{!trades.length && <div className="table-empty">当前情景尚无虚拟成交，账户继续观察。</div>}
    </section>
    <div className="activity-grid">
      <section className="panel"><PanelHeading title="行情观察任务" sub="每两小时采样；离线和失败不补造交易。" /><div className="activity-list">{(paper.operations || []).slice().reverse().map(op => <div className="activity-item" key={op.id}><span className={`event-icon ${op.mode === 'success' ? 'positive' : 'warning'}`}>{op.mode === 'success' ? <CheckCircle size={17} /> : <WarningCircle size={17} />}</span><div><b>{op.mode === 'success' ? `观察已保存 · ${op.virtual_orders}笔新增虚拟成交` : '观察未完成'}</b><small>{op.at ? date(op.at) : op.id}</small>{op.error && <p>{op.error}</p>}</div><EvidenceLink path={op.report}>记录</EvidenceLink></div>)}</div></section>
      <section className="panel"><PanelHeading title="最近研究轮次" sub="显示新评估配置数量，复用组件不重复计数。" /><div className="activity-list">{snapshot.research.rounds.slice(-12).reverse().map(round => <div className="activity-item" key={round.id}><span className="event-icon"><Flask size={18} /></span><div><b>{round.new_configs}个新配置 · {round.passed}通过 / {round.rejected}未通过</b><small>{date(round.at) || round.id}</small><p>{round.new_cross_period_pairs}组新增跨期通过组合</p></div><EvidenceLink path={round.result}>结论</EvidenceLink></div>)}</div></section>
    </div>
    <section className="panel provenance"><PanelHeading title="数据来源与口径" /><dl><div><dt>实时市场报价</dt><dd>Binance现货公开买一/卖一，约10秒刷新；时间为浏览器实际接收时间。</dd></div><div><dt>模拟盘净值</dt><dd>独立虚拟账户的已保存账本，任务约每两小时采样。行情显示不触发虚拟交易或重估净值。</dd></div><div><dt>研究结果</dt><dd>完整登记的真实历史回测；这些历史区间已反复使用，未作为未触碰最终测试集。</dd></div><div><dt>冻结计划</dt><dd className="mono hash">{paper.plan_sha256 || '—'}</dd></div><div><dt>账户状态哈希</dt><dd className="mono hash">{paper.state_sha256 || '—'}</dd></div><div><dt>研究登记哈希</dt><dd className="mono hash">{snapshot.research.registry_sha256}</dd></div><div><dt>证据基准提交</dt><dd><a href={`https://github.com/shenmuegit/EquiTide/commit/${snapshot.source_commit}`} target="_blank" rel="noreferrer" className="text-link mono">{snapshot.source_commit.slice(0, 12)}<ArrowUpRight size={14} /></a></dd></div></dl></section>
  </>;
}

function DetailDialog({ account, research, paper, onClose }: { account: PaperAccount | null; research: ResearchConfig | null; paper: Paper | undefined; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [cost, setCost] = useState<Cost>('1');
  useEffect(() => { if ((account || research) && dialog.current && !dialog.current.open) dialog.current.showModal(); }, [account, research]);
  if (!account && !research) return null;
  const title = account ? `${account.id} · ${account.label}` : research!.indicator;
  const rs = research?.scenes[cost];
  return <dialog ref={dialog} onClose={onClose} className="detail-dialog" aria-labelledby="detail-title" onClick={e => { if (e.target === e.currentTarget) dialog.current?.close(); }}>
    <div className="dialog-head"><div><div className="eyebrow">{account ? '固定策略 · 实盘行情模拟资金' : '历史回测 · 配置证据'}</div><h2 id="detail-title">{title}</h2></div><button className="icon-button" onClick={() => dialog.current?.close()} aria-label="关闭详情"><X size={21} /></button></div>
    <div className="dialog-body">
      <p className="detail-weight">{weights(account?.weights || research?.weights || [])} · 初始本金 {number(account?.capital_usdt || research?.capital_usdt)} USDT</p>
      <div className="detail-scenes"><table><thead><tr><th>成本情景</th><th className="right">累计净收益</th><th className="right">{account ? '采样回撤' : '整体回撤'}</th><th className="right">成本 USDT</th><th className="right">成交</th></tr></thead><tbody>{COSTS.map(c => { const p = account?.scenes[c], r = research?.scenes[c]; return <tr key={c}><td>{c}×{c === '1' ? ' 主账户成本' : ' 成本压力'}</td><td className={`right mono ${tone(p?.return_pct ?? r?.return_pct ?? 0)}`}>{p || r ? `${signed(p?.return_pct ?? r!.return_pct, 4)}%` : '—'}</td><td className="right mono">{number(p?.drawdown_pct ?? r?.drawdown_pct, 4)}%</td><td className="right mono">{number(p?.cost ?? r?.cost, 6)}</td><td className="right mono">{p?.executions ?? r?.executions ?? '—'}</td></tr>; })}</tbody></table></div>
      {account && <><h3>持仓与资金</h3><dl className="detail-facts">{Object.entries(account.scenes['1'].positions).map(([asset, p]) => <div key={asset}><dt>{asset}</dt><dd><span className="mono">{number(p.units, 8)}</span> 币 · 现金 <span className="mono">{number(p.cash_usdt, 6)}</span> USDT · {p.desired_long ? '目标持有' : '目标空仓'}</dd></div>)}</dl>
        <h3>主账户成本拆分</h3><dl className="detail-facts">{Object.entries(account.scenes['1'].cost_parts).map(([key, value]) => <div key={key}><dt>{{ fee: '手续费', half_spread: '观察点差', impact: '成交量冲击', slippage: '估计滑点', tick_rounding: '价格舍入' }[key] || key}</dt><dd className="mono">{number(value, 8)} USDT</dd></div>)}</dl>
        {paper && <><h3>最近日线信号</h3><dl className="detail-facts">{paper.decisions.filter(d => d.portfolio === account.id).map(d => <div key={d.asset}><dt>{d.asset}</dt><dd>{d.context.long ? '继续持有' : '保持空仓'} · 信号可用 {date(d.signal_available_at_utc, true)} · 延迟 {elapsed(d.execution_delay_seconds)}</dd></div>)}</dl></>}
        <p className="detail-note">参数和初始分仓保持冻结，未满180天；短期收益不决定账户重启或淘汰。回撤只覆盖实际采样点。</p>
        <EvidenceLink path={account.source_spec}>完整源配置与规则</EvidenceLink>
      </>}
      {research && <><h3>三项验证记录</h3><div className="validation-grid"><div><span>按时间验证</span><b>{research.validation.walk_forward_folds}折已有结果</b></div><div><span>参数敏感性</span><b>{research.validation.sensitivity_recorded ? '原批次已留档' : '查看原始证据'}</b></div><div><span>成本压力</span><b>{research.validation.cost_scenarios.join(' / ')}× 已执行</b></div></div>
        <div className="detail-heading"><h3>逐折净收益</h3><CostSelector value={cost} onChange={setCost} /></div>
        <div className="fold-grid">{rs?.fold_returns_pct.map((v, i) => <div key={i}><span>第{i + 1}折</span><b className={`mono ${tone(v)}`}>{signed(v)}%</b><small>折内回撤 {number(rs.fold_drawdowns_pct[i])}%</small></div>)}</div>
        <h3>{research.status === 'passed' ? '历史门槛通过' : '未通过的预注册条件'}</h3>
        {research.failed_criteria.length ? <ul className="failed-list">{research.failed_criteria.map(k => <li key={k} title={k}>{failureLabel(k)}</li>)}</ul> : <p className="detail-note">本配置在该历史区间通过预注册门槛。{research.cross_period_passed ? '对应配置在2025和2026两个时期均有通过记录。' : '跨时期通过尚未确认。'}</p>}
        <p className="detail-note">收盘通道的参考窗口排除正在比较的收盘；均线计算、退出优先级和完整成本假设见源配置。相同净值的参数变体不构成独立验证。</p>
        <div className="detail-links"><EvidenceLink path={research.report}>逐变体原始报告</EvidenceLink>{research.spec_path && <EvidenceLink path={research.spec_path}>完整规则与参数</EvidenceLink>}</div>
      </>}
    </div>
  </dialog>;
}

export default function Monitor() {
  const [tab, setTab] = useState<'paper' | 'research' | 'activity'>('paper');
  const [enabled, setEnabled] = useState(true);
  const [refreshKey, setRefreshKey] = useState(0);
  const [now, setNow] = useState(Date.now());
  const [theme, setTheme] = useState(() => { try { return localStorage.getItem('equitide-monitor-theme') || 'dark'; } catch { return 'dark'; } });
  const [account, setAccount] = useState<PaperAccount | null>(null);
  const [research, setResearch] = useState<ResearchConfig | null>(null);
  const data = useEvidence(enabled, refreshKey);
  const market = useQuotes(enabled, refreshKey);
  useEffect(() => { const timer = setInterval(() => setNow(Date.now()), 10_000); return () => clearInterval(timer); }, []);
  useEffect(() => { document.documentElement.dataset.monitorTheme = theme; try { localStorage.setItem('equitide-monitor-theme', theme); } catch { /* optional preference */ } }, [theme]);
  const paper = data.snapshot?.paper;
  const healthy = paper?.status === 'ready' && now - Date.parse(paper.observed_at_utc) <= paper.maximum_gap_seconds * 1000;
  return <div className="monitor-app">
    <a href="#monitor-main" className="skip-link">跳到监控内容</a>
    <aside className="sidebar"><a className="brand-link" href="#paper" onClick={() => setTab('paper')} aria-label="EquiTide模拟盘首页"><Brand /></a><div className="nav-caption">工作台</div>
      <nav aria-label="监控导航">{([{ id: 'paper', label: '模拟盘', icon: ChartLine }, { id: 'research', label: '策略研究', icon: Flask }, { id: 'activity', label: '运行记录', icon: ClockCounterClockwise }] as const).map(item => <button key={item.id} aria-label={item.label} className={tab === item.id ? 'active' : ''} aria-current={tab === item.id ? 'page' : undefined} onClick={() => setTab(item.id)}><item.icon size={20} weight={tab === item.id ? 'fill' : 'regular'} /><span>{item.label}</span>{item.id === 'paper' && <small>10</small>}</button>)}</nav>
      <div className="sidebar-bottom"><span className={`system-status ${healthy ? '' : 'warning'}`}><i />{paper ? healthy ? '账户记录正常' : '等待有效观察' : '正在读取记录'}</span><p>BTC / ETH · 现货<br />真实行情 + 模拟资金</p><a href="https://github.com/shenmuegit/EquiTide/tree/codex/strategy-research" target="_blank" rel="noreferrer"><GithubLogo size={17} />研究证据<ArrowUpRight size={13} /></a></div>
    </aside>
    <div className="workspace"><header className="topbar"><div className="breadcrumb">EquiTide <span>/</span> {tab === 'paper' ? '模拟盘' : tab === 'research' ? '策略研究' : '运行记录'}<span className="readonly-label">公开只读</span></div><div className="toolbar"><span className="refresh-state">{enabled ? '自动刷新中' : '自动刷新已暂停'}</span><button className="icon-button" aria-label={enabled ? '暂停自动刷新' : '恢复自动刷新'} title={enabled ? '暂停自动刷新' : '恢复自动刷新'} onClick={() => setEnabled(!enabled)}>{enabled ? <Pause size={17} /> : <Play size={17} />}</button><button className={`icon-button ${data.reading ? 'is-reading' : ''}`} aria-label="立即刷新" title="立即刷新" onClick={() => setRefreshKey(k => k + 1)}><ArrowClockwise size={18} /></button><span className="toolbar-divider" /><button className="icon-button" aria-label={theme === 'dark' ? '切换浅色主题' : '切换深色主题'} onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>{theme === 'dark' ? <Sun size={19} /> : <Moon size={19} />}</button></div></header>
      <main id="monitor-main" className="main-content"><section className="market-strip" aria-label="BTC与ETH实时公开报价"><div className="market-heading"><span className="eyebrow">MARKET WATCH</span><b>实时市场</b><small>Binance 现货 · 10秒刷新</small></div><QuoteTile symbol="BTC" quote={market.quotes.BTCUSDT} error={market.errors.BTCUSDT} now={now} paused={!enabled} /><QuoteTile symbol="ETH" quote={market.quotes.ETHUSDT} error={market.errors.ETHUSDT} now={now} paused={!enabled} /><div className="market-footnote">报价独立展示<br />账户以保存采样为准</div></section>
        {data.error && <div className="alert" role="alert"><WarningCircle size={18} />{data.error}{data.snapshot && '；以下保留最后有效记录。'}</div>}
        {!data.snapshot ? <div className="loading-panel" aria-live="polite"><span className="loading-mark"><ChartLine size={30} /></span><h1>{data.error ? '暂时无法读取研究账本' : '正在读取研究账本'}</h1><p>{data.error ? '可使用右上角刷新按钮重试。实时市场报价仍单独运行。' : '核对10组账户状态与历史研究记录。'}</p></div> : <>
          {tab === 'paper' && <PaperView paper={data.snapshot.paper} now={now} onSelect={a => { setAccount(a); setResearch(null); }} />}
          {tab === 'research' && <ResearchView snapshot={data.snapshot} configs={data.configs} error={data.researchError} onSelect={r => { setResearch(r); setAccount(null); }} />}
          {tab === 'activity' && <ActivityView snapshot={data.snapshot} />}
        </>}
        <footer className="site-footer"><span>EquiTide · Research Monitor</span><span>账本约2小时更新 · 页面30秒检查 · 北京时间</span><span title={data.receivedAt ? `最近读取 ${date(data.receivedAt)}` : ''}>数据汇总 {data.snapshot ? date(data.snapshot.generated_at_utc, true) : '—'}</span></footer>
      </main>
    </div>
    <DetailDialog account={account ? paper?.accounts?.find(a => a.id === account.id) || account : null} research={research} paper={paper} onClose={() => { setAccount(null); setResearch(null); }} />
  </div>;
}
