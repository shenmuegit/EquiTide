import { lazy, Suspense, useEffect, useId, useMemo, useRef, useState } from 'react';
import { Button, Search, Select, SkeletonPlaceholder, Table, TableBody,
  TableCell, TableHead, TableHeader, TableRow, Tag, Theme } from '@carbon/react';
import { ArrowClockwise, ArrowUpRight, ChartLine, ClockCounterClockwise, Flask,
  Moon, Pause, Play, Sun, WarningCircle, X, CheckCircle, GithubLogo } from '@phosphor-icons/react';
import { COSTS, COLORS, clock, date, number, signed, tone, comparableRows, evidenceUrl, fetchQuote, fetchResearch, fetchSnapshot } from './data';
import type { Paper, PaperAccount, Quote, ResearchConfig, Snapshot, Weight } from './data';

const EquityChart = lazy(() => import('./EquityChart'));
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

function useEvidence(enabled: boolean, refreshKey: number, includeResearch: boolean) {
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
        if (includeResearch && loadedResearch.current !== next.research.configs_sha256) {
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
  }, [enabled, refreshKey, includeResearch]);
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
  return <span className="brand"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M3 18c5-14 8 14 13 0s8 14 13-5" /></svg><span>EquiTide{' '}<small>RESEARCH MONITOR</small></span></span>;
}

function QuoteTile({ symbol, quote, error, now, paused }: { symbol: string; quote?: Quote; error?: string; now: number; paused: boolean }) {
  const stale = !quote || now - Date.parse(quote.observedAt) > 45_000 || !!error;
  return <div className="quote-tile">
    <div className="coin" aria-hidden="true">{symbol === 'BTC' ? '₿' : 'Ξ'}</div>
    <div className="quote-content"><div className="quote-label"><b>{symbol}<span>/ USDT</span></b>
      <span className={`market-state ${stale ? 'warning' : ''}`}>{stale ? '待更新' : paused ? '已暂停' : '实时中间价'}</span></div>
      <div className="quote-value mono">{quote ? number(quote.mid) : '待连接'}<small>USDT</small></div>
      <div className="quote-bottom">买一 <span className="mono">{quote ? number(quote.bid) : '暂无'}</span><i />卖一 <span className="mono">{quote ? number(quote.ask) : '暂无'}</span></div>
      <div className="quote-time" title={error || '接收时间；bookTicker接口不提供成交事件时间'}>
        {error ? '请求失败，保留上次报价' : quote ? `接收于 ${clock(quote.observedAt)}` : '连接公开行情…'}
      </div>
    </div>
  </div>;
}

function Metric({ label, value, sub, valueTone = '', unit }: { label: string; value: string; sub: string; valueTone?: string; unit?: string }) {
  return <div className="metric"><span className="metric-label">{label}</span><div className={`metric-value mono ${valueTone}`}>{value}<small>{unit}</small></div><span className="metric-sub">{sub}</span></div>;
}

function FilterSelect({ label, value, onChange, children, compact = false }: {
  label: string; value: string; onChange: (value: string) => void; children: React.ReactNode; compact?: boolean;
}) {
  const id = useId();
  return <Select id={id} labelText={label} hideLabel={compact} size="md" value={value}
    onChange={e => onChange(e.target.value)} className="filter-select">{children}</Select>;
}

function PanelHeading({ title, sub, children }: { title: string; sub?: string; children?: React.ReactNode }) {
  return <div className="panel-heading"><div><h2>{title}</h2>{sub && <p>{sub}</p>}</div>{children}</div>;
}

function EvidenceLink({ path, children = '查看证据' }: { path: string; children?: React.ReactNode }) {
  return <a className="text-link" href={evidenceUrl(path)} target="_blank" rel="noreferrer">{children}<ArrowUpRight size={14} /></a>;
}

function WeightList({ items }: { items: Weight[] }) {
  return items.length ? <span className="weight-list">{items.map(w => <span className="weight-line" key={w.asset}>
    <span>{w.asset}</span><span className="mono">{number(w.weight * 100, w.weight * 100 % 1 ? 1 : 0)}%</span>
  </span>)}</span> : <span className="muted">独立单币配置</span>;
}

function Position({ scene }: { scene: PaperAccount['scenes']['1'] }) {
  const held = Object.entries(scene.positions).filter(([, p]) => Number(p.units) > 0);
  return held.length ? <span className="positions">{held.map(([asset, p]) => <span key={asset}><b>{asset}</b> <span className="mono">{number(p.units, asset === 'BTC' ? 5 : 4)}</span></span>)}</span> : <span className="cash-label">USDT 空仓</span>;
}

function PaperView({ paper, now, onSelect }: { paper: Paper; now: number; onSelect: (a: PaperAccount) => void }) {
  const [chartAccount, setChartAccount] = useState('');
  if (paper.status === 'unavailable') return <div className="empty-state"><WarningCircle size={32} /><h2>尚无完整模拟盘观察</h2><p>{paper.errors.join('；')}</p></div>;
  const total = paper.totals['1'];
  const days = paper.elapsed_seconds / 86400;
  const stale = now - Date.parse(paper.observed_at_utc) > paper.maximum_gap_seconds * 1000;
  const accounts = [...paper.accounts].sort((a, b) => b.scenes['1'].return_pct - a.scenes['1'].return_pct || a.id.localeCompare(b.id));
  const winners = paper.accounts.filter(a => a.scenes['1'].return_pct > 0).length;
  return <>
    {(stale || paper.status === 'degraded') && <div className="alert" role="status"><WarningCircle size={19} /><span>{paper.errors.length ? paper.errors.join('；') : '模拟盘采样已超过3小时，请检查执行任务；以下保留最后有效账本。'}</span></div>}
    <div className="page-title"><div><h1>模拟盘<Tag type="gray" size="sm" className="badge">{days >= 180 ? '等待完整评审' : '持续观察中'}</Tag></h1><p className="page-description">真实市场行情，10组独立虚拟资金账户。</p></div>
      <div className="updated-note">账本采样时间<strong>{date(paper.observed_at_utc)} 北京时间</strong></div></div>
    <div className="metrics-strip">
      <Metric label="主账户总资产" value={number(total.nav)} unit="USDT" sub="10组独立账户 · 初始资金 20,000 USDT" />
      <Metric label="成本后累计盈亏" value={signed(total.pnl)} unit="USDT" valueTone={tone(total.pnl)} sub={`${signed(total.return_pct, 4)}% 累计收益 · ${winners}/10组正收益`} />
      <Metric label="虚拟成交" value={number(total.executions, 0)} unit="笔" sub={`${total.round_trips}次完整往返 · 累计手续费 ${number(total.fee, 4)} USDT`} />
      <Metric label="实际观察" value={elapsed(paper.elapsed_seconds)} sub={`${paper.observation_count}次有效采样 · ${paper.coverage_gaps.length}段记录缺口`} />
    </div>
    <div className="overview-grid">
      <section className="panel chart-panel"><PanelHeading title="累计净收益" sub="只连接已保存的真实观察点，市场报价不改写账户净值。">
        <FilterSelect label="选择收益曲线账户" value={chartAccount} onChange={setChartAccount} compact><option value="">10组账户合计</option>{paper.accounts.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}</FilterSelect>
      </PanelHeading><Suspense fallback={<div className="equity-chart plot-skeleton" aria-label="正在加载收益图"><SkeletonPlaceholder /></div>}><EquityChart paper={paper} account={chartAccount || undefined} /></Suspense><div className="chart-legend">{COSTS.map((c, i) => <span key={c}><i style={{ background: COLORS[i] }} />{c}×{c === '1' ? ' 主账户' : ' 成本'}</span>)}<span className="legend-note">采样口径回撤</span></div></section>
      <section className="panel progress-panel"><PanelHeading title="前向验证进度" /><div className="progress-number mono">{elapsed(paper.elapsed_seconds)}<span>目标 180 天</span></div>
        <div className="window-track">{Array.from({ length: 6 }, (_, i) => <div key={i} className={days >= (i + 1) * 30 ? 'done' : days >= i * 30 ? 'current' : ''}><span>W{i + 1}</span><small>{(i + 1) * 30}天</small></div>)}</div>
        <p className="progress-copy">6个连续30天窗口。样本仍在积累，<strong>尚未通过完整验证</strong>。</p>
        <dl className="mini-facts"><div><dt>启动时间</dt><dd>{date(paper.start_utc, true)}</dd></div><div><dt>完整评审日期</dt><dd>{date(paper.end_utc)}</dd></div><div><dt>交易规则</dt><dd>UTC闭合日线 · 现货只做多</dd></div></dl>
      </section>
    </div>
    <section className="panel account-panel"><PanelHeading title="10组固定策略" sub="1×、2×、3×列依次展示收益、盈亏 USDT、采样回撤。按主账户排序，初始分仓不再平衡。" />
      <div className="table-scroll" aria-label="模拟账户表"><Table size="xl" className="account-table scenario-table">
        <colgroup><col className="identity-col" /><col className="weight-col" />{COSTS.map(c => <col className="scenario-col" key={c} />)}<col className="context-col" /><col className="context-col" /><col className="detail-col" /></colgroup>
        <TableHead><TableRow><TableHeader><span className="identity-header"><span>策略</span><span>技术指标 / 参数</span></span></TableHeader><TableHeader>初始权重</TableHeader>
          {COSTS.map(c => <TableHeader className="right scenario-header" key={c}>{c}×{c === '1' ? ' 主账户 ↓' : ' 成本'}<small>收益 / 盈亏 / 回撤</small></TableHeader>)}
          <TableHeader>主账户持仓</TableHeader><TableHeader className="right">主账户成交</TableHeader><TableHeader className="detail-header">详情</TableHeader>
        </TableRow></TableHead>
        <TableBody>{accounts.map(a => <TableRow key={a.id}>
          <TableCell className="identity-cell"><div className="strategy-cell"><span className="strategy-id mono">{a.id}</span><span><b>{a.label}</b></span></div></TableCell>
          <TableCell data-label="初始权重" className="weight-cell muted"><WeightList items={a.weights} /></TableCell>
          {COSTS.map(c => { const scene = a.scenes[c]; return <TableCell key={c} data-label={`${c}×${c === '1' ? ' 主账户' : ' 成本'}`} className={`right scenario-cell scenario-${c}`}>
            <span className={`scenario-return mono ${tone(scene.return_pct)}`}>{signed(scene.return_pct, 4)}%</span>
            <span className={`scenario-pnl mono ${tone(scene.pnl)}`} title="成本后累计盈亏，单位 USDT">{signed(scene.pnl, 4)}</span>
            <small className="scenario-note">回撤 <span className="mono">{number(scene.drawdown_pct, 4)}%</span></small>
          </TableCell>; })}
          <TableCell data-label="主账户持仓" className="context-one"><Position scene={a.scenes['1']} /></TableCell>
          <TableCell data-label="主账户成交" className="right mono context-two">{a.scenes['1'].executions}</TableCell>
          <TableCell className="detail-cell"><button className="icon-button row-detail" onClick={() => onSelect(a)} aria-label={`查看 ${a.id} 详情`}><ArrowUpRight size={18} /></button></TableCell>
        </TableRow>)}</TableBody>
      </Table></div>
      <div className="panel-foot"><span>手续费、观察点差、滑点及成交量冲击已计入；回撤限于实际净值采样。</span><EvidenceLink path={paper.report}>本轮账本</EvidenceLink></div>
    </section>
  </>;
}

function ResearchView({ snapshot, configs, error, onSelect }: { snapshot: Snapshot; configs: ResearchConfig[]; error: string; onSelect: (r: ResearchConfig) => void }) {
  const research = snapshot.research;
  const cost = '3';
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
    <div className="page-title"><div><h1>策略研究<Tag type="gray" size="sm" className="badge">{research.counts.registered.toLocaleString()}个独立配置</Tag></h1><p className="page-description">同区间比较收益、回撤与验证记录。</p></div><div className="updated-note">最新研究轮次<strong>{latest ? date(latest.at) : '暂无'}</strong></div></div>
    {error && <div className="alert" role="status"><WarningCircle size={18} />{error}</div>}
    <div className="metrics-strip research-metrics">
      <Metric label="已有实际回测" value={number(research.counts.results, 0)} unit="配置" sub={`${research.counts.observation_records_excluded}条持续观察记录已单独统计`} />
      <Metric label="当前区间正收益" value={configs.length ? number(positive, 0) : "读取中"} unit={configs.length ? `/ ${comparable.length}` : undefined} sub={`${cost}×成本 · 相同时间区间、配置类型`} valueTone="positive" />
      <Metric label="当前区间通过门槛" value={configs.length ? number(passed, 0) : "读取中"} unit="配置" sub="结合逐折盈利、整体回撤、交易及成本条件" />
      <Metric label="跨2025/2026通过" value={configs.length ? number(cross, 0) : "读取中"} unit="配置" sub="两个时期均通过历史门槛 · 非独立最终测试集" />
    </div>
    <div className="research-context"><div><Flask size={20} /><span>这些历史区间已反复用于研究。参数敏感性以原批次报告为准；历史通过不代表稳定实盘盈利。</span></div>{latest && <EvidenceLink path={latest.result}>最新中文结论</EvidenceLink>}</div>
    <section className="panel research-panel"><PanelHeading title="收益排名" sub={kind === 'combination' ? '同区间、初始本金2,000 USDT的组合比较；配置不按指标族合并。' : '同区间的单币组件比较；各组件原始本金见详情。'} />
      <div className="research-filters">
        <div className="search-box"><span className="field-label">指标、参数或权重</span><Search id="monitor-research-search" size="md" labelText="搜索技术指标、参数或权重" closeButtonLabelText="清除搜索" placeholder="例如 EMA29、0.75" value={query} onChange={e => { setQuery(e.target.value); setPage(1); }} /></div>
        <FilterSelect label="回测区间" value={period} onChange={v => { setPeriod(v); setPage(1); }}>{research.periods.map(p => <option key={p.start_utc + p.end_utc} value={`${p.start_utc}|${p.end_utc}`}>{p.start_utc.slice(0, 10)} 至 {p.end_utc.slice(0, 10)} UTC</option>)}</FilterSelect>
        <FilterSelect label="配置类型" value={kind} onChange={v => { setKind(v); setPage(1); }}><option value="combination">BTC / ETH 组合</option><option value="strategy">单币策略组件</option></FilterSelect>
        <FilterSelect label="验证筛选" value={status} onChange={v => { setStatus(v); setPage(1); }}><option value="all">全部验证状态</option><option value="passed">通过历史门槛</option><option value="rejected">未通过历史门槛</option><option value="cross">跨两个时期通过</option></FilterSelect>
        <FilterSelect label="排名排序" value={sort} onChange={v => { setSort(v); setPage(1); }}><option value="return">3×收益率倒序</option><option value="drawdown">3×回撤从低到高</option></FilterSelect>
      </div>
      <div className="research-summary"><span>当前筛选 <b>{filtered.length}</b> 个配置</span><span>正收益 {positive} · 通过 {passed} · 未通过 {comparable.length - passed}</span></div>
      <div className="table-scroll" aria-label="研究收益榜"><Table size="xl" className="research-table scenario-table">
        <colgroup><col className="identity-col" /><col className="weight-col" />{COSTS.map(c => <col className="scenario-col" key={c} />)}<col className="context-col" /><col className="context-col" /><col className="detail-col" /></colgroup>
        <TableHead><TableRow><TableHeader><span className="identity-header"><span>排名</span><span>技术指标 / 参数</span></span></TableHeader><TableHeader>原始权重</TableHeader>
          {COSTS.map(c => <TableHeader key={c} className="right scenario-header">{c}×{c === '1' ? ' 基准' : ' 成本'}{c === '3' ? sort === 'return' ? ' ↓' : ' ↑' : ''}<small>净收益 / 回撤</small></TableHeader>)}
          <TableHeader className="right">1×盈利折</TableHeader><TableHeader>验证状态</TableHeader><TableHeader className="detail-header">详情</TableHeader>
        </TableRow></TableHead>
        <TableBody>{rows.map((r, i) => <TableRow key={r.fingerprint}>
          <TableCell className="identity-cell"><div className="strategy-cell"><span className="strategy-id mono">{(safePage - 1) * 25 + i + 1}</span><span><button className="strategy-link" onClick={() => onSelect(r)}>{r.indicator}</button><small className="config-name mono">{r.name}</small></span></div></TableCell>
          <TableCell data-label="原始权重" className="weight-text weight-cell"><WeightList items={r.weights} /></TableCell>
          {COSTS.map(c => { const scene = r.scenes[c]; return <TableCell key={c} data-label={`${c}×${c === '1' ? ' 基准' : ' 成本'}`} className={`right scenario-cell scenario-${c}`}>
            {scene ? <><span className={`scenario-return mono ${tone(scene.return_pct)}`}>{signed(scene.return_pct)}%</span><small className="scenario-note">回撤 <span className="mono">{number(scene.drawdown_pct)}%</span></small></> : <span className="muted">暂无</span>}
          </TableCell>; })}
          <TableCell data-label="1×盈利折" className="right mono context-one">{r.positive_folds_1x ?? r.scenes['1']?.fold_returns_pct.filter(x => x > 0).length ?? '暂无'}<span className="muted"> / {r.validation.walk_forward_folds || '暂无'}</span></TableCell>
          <TableCell data-label="验证状态" className="context-two"><span className={`status-label ${r.status === 'passed' ? 'positive' : 'muted'}`}>{r.status === 'passed' ? <CheckCircle size={14} /> : <X size={14} />}{r.status === 'passed' ? '历史通过' : '未通过'}</span>{r.cross_period_passed && <small className="cross-period">跨两期通过</small>}</TableCell>
          <TableCell className="detail-cell"><button className="icon-button row-detail" onClick={() => onSelect(r)} aria-label={`查看研究配置 ${r.name}`}><ArrowUpRight size={18} /></button></TableCell>
        </TableRow>)}</TableBody>
      </Table></div>
      {!configs.length && <div className="table-empty">{error || '正在读取并核验研究结果…'}</div>}
      {!!configs.length && !rows.length && <div className="table-empty">没有符合当前条件的配置。可调整区间或筛选条件。</div>}
      <div className="pagination"><span>第 {safePage} / {pages} 页，每页25条</span><div><Button kind="ghost" size="md" disabled={safePage <= 1} onClick={() => setPage(safePage - 1)}>上一页</Button><Button kind="ghost" size="md" disabled={safePage >= pages} onClick={() => setPage(safePage + 1)}>下一页</Button></div></div>
      <div className="panel-foot"><span>另有 {research.counts.unranked} 个历史配置无同格式可比指标，保留原始结果并排除出此收益榜。等效净值不代表独立验证。</span><EvidenceLink path="research/automation/registry.jsonl">完整登记</EvidenceLink></div>
    </section>
  </>;
}

function ActivityView({ snapshot }: { snapshot: Snapshot }) {
  const paper = snapshot.paper;
  const trades = (paper.trades || []).slice().reverse();
  return <>
    <div className="page-title"><div><h1>运行记录</h1><p className="page-description">查看虚拟成交、行情观察与研究轮次。</p></div><Tag type="gray" size="sm">公开只读</Tag></div>
    <section className="panel"><PanelHeading title="虚拟成交账本" sub="三种成本情景逐笔并列记录，成交使用当时实际观察的公开报价。"></PanelHeading>
      <div className="table-scroll" tabIndex={0} aria-label="虚拟成交表"><Table size="xl" className="trade-table"><TableHead><TableRow><TableHeader>模拟成交时间 · 北京</TableHeader><TableHeader>账户</TableHeader><TableHeader>成本情景</TableHeader><TableHeader>方向</TableHeader><TableHeader>资产</TableHeader><TableHeader className="right">数量</TableHeader><TableHeader className="right">执行价格 USDT</TableHeader><TableHeader className="right">总成本 USDT</TableHeader><TableHeader>信号到执行</TableHeader></TableRow></TableHead><TableBody>{trades.map(t => <TableRow key={t.trade_id}><TableCell className="mono trade-time" data-label="模拟成交时间 · 北京">{date(t.simulated_at_utc)}</TableCell><TableCell className="mono" data-label="账户">{t.portfolio}</TableCell><TableCell data-label="成本情景">{t.cost_multiplier}×{t.cost_multiplier === 1 ? ' 主账户' : ' 成本'}</TableCell><TableCell data-label="方向" className={t.side === 'buy' ? 'positive' : 'negative'}>{t.side === 'buy' ? '买入' : '卖出'}</TableCell><TableCell data-label="资产">{t.asset}</TableCell><TableCell data-label="数量" className="right mono">{number(t.quantity, 8)}</TableCell><TableCell data-label="执行价格 USDT" className="right mono">{number(t.execution)}</TableCell><TableCell data-label="总成本 USDT" className="right mono">{number(t.cost_usdt, 6)}</TableCell><TableCell data-label="信号到执行">{t.simulated_at_utc && t.signal_available_at_utc ? elapsed((Date.parse(t.simulated_at_utc) - Date.parse(t.signal_available_at_utc)) / 1000) : '暂无'}</TableCell></TableRow>)}</TableBody></Table></div>{!trades.length && <div className="table-empty">尚无虚拟成交，账户继续观察。</div>}
    </section>
    <div className="activity-grid">
      <section className="panel"><PanelHeading title="行情观察任务" sub="每两小时采样；离线和失败不补造交易。" /><div className="activity-list">{(paper.operations || []).slice().reverse().map(op => <div className="activity-item" key={op.id}><span className={`event-icon ${op.mode === 'success' ? 'positive' : 'warning'}`}>{op.mode === 'success' ? <CheckCircle size={17} /> : <WarningCircle size={17} />}</span><div><b>{op.mode === 'success' ? `观察已保存 · ${op.virtual_orders}笔新增虚拟成交` : '观察未完成'}</b><small>{op.at ? date(op.at) : op.id}</small>{op.error && <p>{op.error}</p>}</div><EvidenceLink path={op.report}>记录</EvidenceLink></div>)}</div></section>
      <section className="panel"><PanelHeading title="最近研究轮次" sub="显示新评估配置数量，复用组件不重复计数。" /><div className="activity-list">{snapshot.research.rounds.slice(-12).reverse().map(round => <div className="activity-item" key={round.id}><span className="event-icon"><Flask size={18} /></span><div><b>{round.new_configs}个新配置 · {round.passed}通过 / {round.rejected}未通过</b><small>{date(round.at) || round.id}</small><p>{round.new_cross_period_pairs}组新增跨期通过组合</p></div><EvidenceLink path={round.result}>结论</EvidenceLink></div>)}</div></section>
    </div>
    <section className="panel provenance"><PanelHeading title="数据来源与口径" /><dl><div><dt>实时市场报价</dt><dd>Binance现货公开买一/卖一，约10秒刷新；时间为浏览器实际接收时间。</dd></div><div><dt>模拟盘净值</dt><dd>独立虚拟账户的已保存账本，任务约每两小时采样。行情显示不触发虚拟交易或重估净值。</dd></div><div><dt>研究结果</dt><dd>完整登记的真实历史回测；这些历史区间已反复使用，未作为未触碰最终测试集。</dd></div><div><dt>冻结计划</dt><dd className="mono hash">{paper.plan_sha256 || '暂无'}</dd></div><div><dt>账户状态哈希</dt><dd className="mono hash">{paper.state_sha256 || '暂无'}</dd></div><div><dt>研究登记哈希</dt><dd className="mono hash">{snapshot.research.registry_sha256}</dd></div><div><dt>证据基准提交</dt><dd><a href={`https://github.com/shenmuegit/EquiTide/commit/${snapshot.source_commit}`} target="_blank" rel="noreferrer" className="text-link mono">{snapshot.source_commit.slice(0, 12)}<ArrowUpRight size={14} /></a></dd></div></dl></section>
  </>;
}

function DetailDialog({ account, research, paper, onClose }: { account: PaperAccount | null; research: ResearchConfig | null; paper: Paper | undefined; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => { if ((account || research) && dialog.current && !dialog.current.open) dialog.current.showModal(); }, [account, research]);
  if (!account && !research) return null;
  const title = account ? `${account.id} · ${account.label}` : research!.indicator;
  return <dialog ref={dialog} onClose={onClose} className="detail-dialog" aria-labelledby="detail-title" onClick={e => { if (e.target === e.currentTarget) dialog.current?.close(); }}>
    <div className="dialog-head"><div><div className="eyebrow">{account ? '固定策略 · 实盘行情模拟资金' : '历史回测 · 配置证据'}</div><h2 id="detail-title">{title}</h2></div><button className="icon-button" onClick={() => dialog.current?.close()} aria-label="关闭详情"><X size={21} /></button></div>
    <div className="dialog-body">
      <p className="detail-weight">{weights(account?.weights || research?.weights || [])} · 初始本金 {number(account?.capital_usdt || research?.capital_usdt)} USDT</p>
      <div className="detail-scenes"><Table size="xl"><TableHead><TableRow><TableHeader>成本情景</TableHeader><TableHeader className="right">累计净收益</TableHeader><TableHeader className="right">{account ? '采样回撤' : '整体回撤'}</TableHeader><TableHeader className="right">成本 USDT</TableHeader><TableHeader className="right">成交</TableHeader></TableRow></TableHead><TableBody>{COSTS.map(c => { const p = account?.scenes[c], r = research?.scenes[c]; return <TableRow key={c}><TableCell className="detail-scenario-label">{c}×{c === '1' ? account ? ' 主账户成本' : ' 基准成本' : ' 成本压力'}</TableCell><TableCell data-label="累计净收益" className={`right mono ${tone(p?.return_pct ?? r?.return_pct ?? 0)}`}>{p || r ? `${signed(p?.return_pct ?? r!.return_pct, 4)}%` : '暂无'}</TableCell><TableCell data-label={account ? '采样回撤' : '整体回撤'} className="right mono">{number(p?.drawdown_pct ?? r?.drawdown_pct, 4)}%</TableCell><TableCell data-label="成本 USDT" className="right mono">{number(p?.cost ?? r?.cost, 6)}</TableCell><TableCell data-label="成交" className="right mono">{p?.executions ?? r?.executions ?? '暂无'}</TableCell></TableRow>; })}</TableBody></Table></div>
      {account && <><h3>持仓与资金</h3><dl className="detail-facts">{Object.entries(account.scenes['1'].positions).map(([asset, p]) => <div key={asset}><dt>{asset}</dt><dd><span className="mono">{number(p.units, 8)}</span> 币，现金 <span className="mono">{number(p.cash_usdt, 6)}</span> USDT，{p.desired_long ? '目标持有' : '目标空仓'}</dd></div>)}</dl>
        <h3>主账户成本拆分</h3><dl className="detail-facts">{Object.entries(account.scenes['1'].cost_parts).map(([key, value]) => <div key={key}><dt>{{ fee: '手续费', half_spread: '观察点差', impact: '成交量冲击', slippage: '估计滑点', tick_rounding: '价格舍入' }[key] || key}</dt><dd className="mono">{number(value, 8)} USDT</dd></div>)}</dl>
        {paper && <><h3>最近日线信号</h3><dl className="detail-facts">{paper.decisions.filter(d => d.portfolio === account.id).map(d => <div key={d.asset}><dt>{d.asset}</dt><dd>{d.context.long ? '继续持有' : '保持空仓'}，信号可用 {date(d.signal_available_at_utc, true)}，延迟 {elapsed(d.execution_delay_seconds)}</dd></div>)}</dl></>}
        <p className="detail-note">参数和初始分仓保持冻结，未满180天；短期收益不决定账户重启或淘汰。回撤只覆盖实际采样点。</p>
        <EvidenceLink path={account.source_spec}>完整源配置与规则</EvidenceLink>
      </>}
      {research && <><h3>三项验证记录</h3><div className="validation-grid"><div><span>按时间验证</span><b>{research.validation.walk_forward_folds}折已有结果</b></div><div><span>参数敏感性</span><b>{research.validation.sensitivity_recorded ? '原批次已留档' : '查看原始证据'}</b></div><div><span>成本压力</span><b>{research.validation.cost_scenarios.join(' / ')}× 已执行</b></div></div>
        <h3>逐折净收益 · 三种成本同时比较</h3>
        <div className="fold-grid">{Array.from({ length: Math.max(0, ...COSTS.map(c => research.scenes[c]?.fold_returns_pct.length || 0)) }, (_, i) => <div key={i}>
          <span className="fold-title">第{i + 1}折</span><div className="fold-costs">{COSTS.map(c => { const scene = research.scenes[c], value = scene?.fold_returns_pct[i], drawdown = scene?.fold_drawdowns_pct[i]; return <div key={c}>
            <span>{c}×</span><b className={`mono ${value == null ? 'muted' : tone(value)}`}>{value == null ? '暂无' : `${signed(value)}%`}</b><small>回撤 {drawdown == null ? '暂无' : `${number(drawdown)}%`}</small>
          </div>; })}</div>
        </div>)}</div>
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
  const [theme, setTheme] = useState(() => {
    try {
      const saved = localStorage.getItem('equitide-monitor-theme');
      if (saved === 'dark' || saved === 'light') return saved;
    } catch { /* optional preference */ }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  });
  const [account, setAccount] = useState<PaperAccount | null>(null);
  const [research, setResearch] = useState<ResearchConfig | null>(null);
  const data = useEvidence(enabled, refreshKey, tab === 'research');
  const market = useQuotes(enabled, refreshKey);
  useEffect(() => { const timer = setInterval(() => setNow(Date.now()), 10_000); return () => clearInterval(timer); }, []);
  useEffect(() => { document.documentElement.dataset.monitorTheme = theme; const meta = document.querySelector<HTMLMetaElement>('meta[name=theme-color]'); if (meta) meta.content = theme === 'dark' ? '#171b19' : '#f5f6f5'; try { localStorage.setItem('equitide-monitor-theme', theme); } catch { /* optional preference */ } }, [theme]);
  const paper = data.snapshot?.paper;
  const healthy = paper?.status === 'ready' && now - Date.parse(paper.observed_at_utc) <= paper.maximum_gap_seconds * 1000;
  return <Theme theme={theme === 'dark' ? 'g100' : 'g10'}><div className="monitor-app">
    <a href="#monitor-main" className="skip-link">跳到监控内容</a>
    <header className="app-header"><div className="header-inner">
      <a className="brand-link" href="#paper" onClick={() => setTab('paper')} title="模拟盘首页"><Brand /></a>
      <nav aria-label="监控导航">{([{ id: 'paper', label: '模拟盘', icon: ChartLine }, { id: 'research', label: '策略研究', icon: Flask }, { id: 'activity', label: '运行记录', icon: ClockCounterClockwise }] as const).map(item => <button key={item.id} aria-label={item.label} className={tab === item.id ? 'active' : ''} aria-current={tab === item.id ? 'page' : undefined} onClick={() => setTab(item.id)}><item.icon size={18} /><span>{item.label}</span></button>)}</nav>
      <div className="toolbar"><Tag type="gray" size="sm" className="header-readonly">公开只读</Tag><Button kind="ghost" size="md" hasIconOnly tooltipAlignment="end" tooltipPosition="bottom" iconDescription={enabled ? '暂停自动刷新' : '恢复自动刷新'} renderIcon={enabled ? Pause : Play} onClick={() => setEnabled(!enabled)} />
        <Button kind="ghost" size="md" className={data.reading ? 'is-reading' : ''} hasIconOnly tooltipAlignment="end" tooltipPosition="bottom" iconDescription="立即刷新" renderIcon={ArrowClockwise} onClick={() => setRefreshKey(k => k + 1)} />
        <Button kind="ghost" size="md" hasIconOnly tooltipAlignment="end" tooltipPosition="bottom" iconDescription={theme === 'dark' ? '切换浅色主题' : '切换深色主题'} renderIcon={theme === 'dark' ? Sun : Moon} onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} />
      </div>
    </div></header>
    <main id="monitor-main" className="main-content">
      <section className="market-strip" aria-label="BTC与ETH实时公开报价"><div className="market-heading"><b>实时行情</b><small>Binance 现货</small></div>
        <QuoteTile symbol="BTC" quote={market.quotes.BTCUSDT} error={market.errors.BTCUSDT} now={now} paused={!enabled} />
        <QuoteTile symbol="ETH" quote={market.quotes.ETHUSDT} error={market.errors.ETHUSDT} now={now} paused={!enabled} />
        <div className="market-footnote"><span className={`system-status ${healthy ? '' : 'warning'}`}><i />{paper ? healthy ? '账户记录正常' : '等待有效观察' : '正在读取记录'}</span><small>{enabled ? '行情每10秒刷新' : '自动刷新已暂停'}</small></div>
      </section>
      {data.error && <div className="alert" role="alert"><WarningCircle size={18} />{data.error}{data.snapshot && '；以下保留最后有效记录。'}</div>}
      {!data.snapshot ? <section className="loading-panel" aria-live="polite"><h1>{data.error ? '暂时无法读取研究账本' : '正在读取研究账本'}</h1>
        {data.error ? <p>使用顶部刷新按钮重试。实时市场报价仍单独运行。</p> : <><div className="loading-metrics">{[0, 1, 2, 3].map(i => <SkeletonPlaceholder key={i} />)}</div><SkeletonPlaceholder className="loading-chart" /><SkeletonPlaceholder className="loading-table" /></>}
      </section> : <>
        {tab === 'paper' && <PaperView paper={data.snapshot.paper} now={now} onSelect={a => { setAccount(a); setResearch(null); }} />}
        {tab === 'research' && <ResearchView snapshot={data.snapshot} configs={data.configs} error={data.researchError} onSelect={r => { setResearch(r); setAccount(null); }} />}
        {tab === 'activity' && <ActivityView snapshot={data.snapshot} />}
      </>}
      <footer className="site-footer"><a href="https://github.com/shenmuegit/EquiTide/tree/codex/strategy-research" target="_blank" rel="noreferrer"><GithubLogo size={16} />研究证据<ArrowUpRight size={13} /></a><span>账本约2小时更新 / 页面30秒检查 / 北京时间</span><span title={data.receivedAt ? `最近读取 ${date(data.receivedAt)}` : ''}>数据汇总 {data.snapshot ? date(data.snapshot.generated_at_utc, true) : '暂无'}</span></footer>
    </main>
    <DetailDialog account={account ? paper?.accounts?.find(a => a.id === account.id) || account : null} research={research} paper={paper} onClose={() => { setAccount(null); setResearch(null); }} />
  </div></Theme>;
}
