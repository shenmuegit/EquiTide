import { lazy, Suspense, useEffect, useRef, useState, type FormEvent } from 'react';
import { ArrowRight, ArrowUpRight, ArrowsClockwise, CalendarBlank, CaretDown, Check, Clock, CurrencyBtc, HourglassMedium, IconContext, Info, Moon, Pause, Sun, WarningCircle, Waveform } from '@phosphor-icons/react';
import { ApiError, chinaInput, entryFromChina, formatChinaTime, getAnalysis, getTask, listAnalyses, startAnalysis, type Analysis, type StrategyResult, type Task } from './api';

const ReplayChart = lazy(() => import('./Chart'));
const number = new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const signed = (n: number | null) => n === null ? '暂无结果' : `${n > 0 ? '+' : ''}${number.format(n)}`;
const isActive = (task: Task | null) => task?.status === 'queued' || task?.status === 'running';
const statusName = { queued: '等待分析', running: '分析中', succeeded: '已完成', failed: '未完成' };

function reason(result: StrategyResult): string {
  if (result.status === 'unavailable') return '这个时点暂时无法形成判断。';
  if (result.status === 'failed') return '判断计算未完成，请重新分析。';
  if (result.reason === 'expected_net_not_above_buffer') return '当时预期的收益不足以覆盖交易成本。';
  if (result.status === 'no-trade') return '这个时间没有满足买入条件。';
  return '根据当时已知的信息，这个时间满足买入条件。';
}

function Result({ analysis }: { analysis: Analysis }) {
  const { model, replay } = analysis;
  const wait = model.status === 'no-trade';
  const traded = model.status === 'traded';
  const decision = wait ? '暂不买入，继续等待' : traded ? '当时满足买入条件' : '暂时无法给出判断';
  const DecisionIcon = wait ? Pause : traded ? Check : Info;
  const complete = replay.status === 'traded' && replay.netPnl !== null;
  return <div className="result-content">
    <div className="result-topline">
      <div className="market"><span className="coin"><CurrencyBtc size={25} /></span><span><strong>{analysis.asset} <span className="subtle">/ USDT</span></strong><small>{analysis.exchange === 'binance' ? 'Binance' : analysis.exchange.toUpperCase()} 现货与永续对冲</small></span></div>
      <span className="result-date">{formatChinaTime(analysis.entryNs)}<small>北京时间</small></span>
    </div>
    <section className="decision" aria-labelledby="decision-heading">
      <span className="decision-symbol"><DecisionIcon size={27} weight="regular" /></span>
      <div><p className="decision-label">当时的判断</p><h2 id="decision-heading">{decision}</h2><p>{reason(model)}</p></div>
    </section>
    <section className="replay" aria-labelledby="replay-heading">
      <div className="replay-heading"><h3 id="replay-heading">如果当时买入</h3><span><Clock size={14} />随后 24 小时</span></div>
      <div className="pnl-summary"><div><p className="pnl-label">模拟净收益 <span>已计交易成本</span></p><div className={`pnl-value ${complete && replay.netPnl! < 0 ? 'negative' : ''}`}>{signed(replay.netPnl)}{replay.netPnl !== null && <span>USDT</span>}</div></div><div className="return-value"><p>总资金收益率</p><strong>{replay.returnRate === null ? '暂无结果' : `${replay.returnRate > 0 ? '+' : ''}${(replay.returnRate * 100).toFixed(4)}%`}</strong></div></div>
      {analysis.equity.length > 1 ? <Suspense fallback={<div className="chart-skeleton skeleton" />}><ReplayChart points={analysis.equity} entryNs={analysis.entryNs} exitNs={analysis.exitNs} /></Suspense> : <div className="chart-unavailable"><Waveform size={30} /><p>{analysis.curveError ? '收益汇总已就绪，回放曲线暂不可用。' : '这个时点没有可展示的成交曲线。'}</p></div>}
      <div className="chart-caption"><span className="chart-key" />模拟持有的净收益<span className="caption-end">{formatChinaTime(analysis.exitNs)} 结束</span></div>
    </section>
    <details className="explanation"><summary><Info size={16} /><span>怎么看这次结果</span><CaretDown size={14} /></summary><div className="explanation-body"><p>“当时的判断”只使用买入时间之前已知的信息。“如果当时买入”模拟现货买入并用永续合约对冲，展示之后 24 小时的收益，不代表实际成交。</p><p>收益按系统模拟仓位计算，并计入资金费、手续费及执行成本。历史回放不代表未来收益。</p><dl><div><dt>资金费收益</dt><dd>{signed(replay.funding)} USDT</dd></div><div><dt>价差损益</dt><dd>{signed(replay.pricePnl)} USDT</dd></div><div><dt>交易手续费</dt><dd>{replay.fees === null ? '暂无结果' : number.format(replay.fees)} USDT</dd></div></dl></div></details>
  </div>;
}

function Pending({ task, fetching }: { task: Task | null; fetching: boolean }) {
  return <div className="pending" role="status" aria-live="polite"><div className="pending-top"><HourglassMedium size={25} /><div><h2>{fetching ? '正在读取分析结果' : task?.status === 'queued' ? '等待开始分析' : '正在分析这个时间'}</h2><p>{fetching ? '正在加载历史判断和回放。' : '系统正在计算当时的判断与随后 24 小时的结果。'}</p></div></div><div className="skeleton decision-skeleton" /><div className="skeleton number-skeleton" /><div className="skeleton chart-skeleton" /><p className="pending-note">{task?.config.entry_analysis_ns ? formatChinaTime(task.config.entry_analysis_ns) : '只需选择买入时间，其余交给系统。'}</p></div>;
}

export default function App() {
  const [input, setInput] = useState({ date: '', hour: '08' });
  const [tasks, setTasks] = useState<Task[]>([]);
  const [task, setTask] = useState<Task | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [issue, setIssue] = useState<string | null>(null);
  const [formIssue, setFormIssue] = useState<string | null>(null);
  const [historyIssue, setHistoryIssue] = useState<string | null>(null);
  const [reload, setReload] = useState(0);
  const [visibleCount, setVisibleCount] = useState(4);
  const [theme, setTheme] = useState<'light' | 'dark'>(() => matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const submitLock = useRef(false);
  const touched = useRef(false);

  useEffect(() => { document.documentElement.dataset.theme = theme; }, [theme]);

  useEffect(() => {
    const controller = new AbortController();
    listAnalyses(controller.signal).then(items => {
      setTasks(items);
      if (items[0] && !touched.current) {
        setInput(chinaInput(items[0].config.entry_analysis_ns!));
        setTask(items[0]);
      } else setLoading(false);
    }).catch(error => { if (controller.signal.aborted) return; setHistoryIssue(error.message); setLoading(false); });
    return () => controller.abort();
  }, []);

  useEffect(() => {
    if (!task) return;
    const controller = new AbortController();
    let timer: ReturnType<typeof setTimeout>;
    let current = task;
    setLoading(true); setIssue(null); setAnalysis(null);
    async function read() {
      try {
        if (isActive(current)) current = await getTask(current.id, controller.signal);
        if (controller.signal.aborted) return;
        setTask(current);
        setTasks(items => items.map(item => item.id === current.id ? current : item));
        if (isActive(current)) { timer = setTimeout(read, 1600); return; }
        const result = await getAnalysis(current, controller.signal);
        if (!controller.signal.aborted) { setAnalysis(result); setLoading(false); }
      } catch (error) {
        if (controller.signal.aborted) return;
        setIssue(error instanceof Error ? error.message : '结果读取失败，请重试。');
        setLoading(false);
      }
    }
    void read();
    return () => { controller.abort(); clearTimeout(timer); };
  }, [task?.id, reload]);

  function openTask(item: Task) {
    touched.current = true;
    setInput(chinaInput(item.config.entry_analysis_ns!));
    setTask(item); setFormIssue(null);
    if (item.id === task?.id) setReload(n => n + 1);
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (submitLock.current) return;
    submitLock.current = true;
    touched.current = true;
    setFormIssue(null); setSending(true);
    try {
      const entryNs = entryFromChina(input.date, input.hour);
      const created = await startAnalysis(entryNs);
      setTasks(items => [created, ...items]);
      setTask(created); setHistoryIssue(null);
    } catch (error) {
      setFormIssue(error instanceof ApiError ? error.message : '提交失败，请稍后重试。');
    } finally { setSending(false); submitLock.current = false; }
  }

  const pending = !issue && (loading || isActive(task));
  const latestSuccess = tasks.find(item => item.status === 'succeeded');
  return <IconContext.Provider value={{ weight: 'regular', size: 20 }}><a className="skip-link" href="#main">跳到分析页面</a>
    <header className="site-header"><div className="header-inner"><a className="brand" href="#main"><span className="brand-mark"><Waveform size={23} weight="bold" /></span><span>USDT<span className="brand-name">量化</span></span></a><nav aria-label="主导航"><a href="#main" className="nav-active">买入分析</a><a href="#history">分析记录</a></nav><button className="icon-button theme-toggle" onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} aria-label={theme === 'light' ? '切换深色模式' : '切换浅色模式'}>{theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}</button></div></header>
    <main id="main" className="page"><div className="intro"><p className="eyebrow">历史买入分析</p><h1>这个时间，适合买入吗？</h1><p className="intro-copy">选择一个过去的时间，看看当时的判断与之后 24 小时的结果。</p></div>
      <div className="workspace"><aside className="entry-column"><form className="entry-form" onSubmit={submit}><div className="form-title"><CalendarBlank size={22} /><h2>选择买入时间</h2></div><p className="form-description">你决定时间，系统完成分析。</p><div className="field"><label htmlFor="entry-date">买入日期</label><input id="entry-date" name="entry-date" type="date" disabled={sending} required max={chinaInput(Date.now() * 1e6).date} value={input.date} onChange={e => { touched.current = true; setInput({ ...input, date: e.target.value }); setFormIssue(null); }} aria-describedby={formIssue ? 'form-error' : undefined} aria-invalid={!!formIssue} /></div><div className="field"><div className="label-row"><label htmlFor="entry-hour">买入时刻</label><span>北京时间 UTC+8</span></div><div className="select-wrap"><Clock size={18} /><select id="entry-hour" name="entry-hour" disabled={sending} value={input.hour} onChange={e => { touched.current = true; setInput({ ...input, hour: e.target.value }); setFormIssue(null); }}>{Array.from({ length: 24 }, (_, i) => <option key={i} value={String(i).padStart(2, '0')}>{String(i).padStart(2, '0')}:00</option>)}</select><CaretDown size={15} /></div></div><button className="primary-button" type="submit" disabled={!input.date || sending || isActive(task)}>{sending ? '正在提交' : isActive(task) ? '正在分析' : '分析这个时间'}{sending || isActive(task) ? <HourglassMedium size={18} /> : <ArrowRight size={18} />}</button>{formIssue && <div className="form-error" id="form-error" role="alert"><WarningCircle size={18} /><div><p>{formIssue}</p>{latestSuccess && <button type="button" className="text-button" onClick={() => openTask(latestSuccess)}>查看最近一次成功分析<ArrowUpRight size={14} /></button>}</div></div>}<p className="form-note"><Check size={14} />分析完成后，结果自动保存</p></form><div className="small-explainer"><div className="small-explainer-icon"><Clock size={19} /></div><h3>看判断，也看后来</h3><p>判断只依据当时已知的信息。回放告诉你，如果买入，接下来发生了什么。</p><span>历史回放，不会产生真实交易</span></div></aside>
        <section className="result-panel" aria-label="分析结果" aria-busy={pending}>{pending ? <Pending task={task} fetching={!isActive(task)} /> : issue ? <div className="empty-result" role="alert"><span className="empty-symbol"><WarningCircle size={34} /></span><h2>暂时无法显示结果</h2><p>{issue}</p><button className="secondary-button" onClick={() => setReload(n => n + 1)}><ArrowsClockwise size={16} />重新读取</button></div> : analysis ? <Result analysis={analysis} /> : <div className="empty-result"><span className="empty-symbol"><CalendarBlank size={34} /></span><h2>从一个买入时间开始</h2><p>选好时间后，这里会显示当时的判断、<br />模拟收益和 24 小时回放。</p><div className="empty-tags"><span>当时的判断</span><ArrowRight size={14} /><span>后来的结果</span></div></div>}</section>
      </div>
      <section id="history" className="history" aria-labelledby="history-title"><div className="history-heading"><h2 id="history-title">最近分析<span>{tasks.length > 0 ? String(tasks.length) : ''}</span></h2><p>回看你研究过的买入时刻</p></div>{historyIssue ? <p className="history-error" role="alert">{historyIssue}</p> : tasks.length ? <div className="history-list">{tasks.slice(0, visibleCount).map(item => { const time = chinaInput(item.config.entry_analysis_ns!); return <button key={item.id} className={`history-row ${item.id === task?.id ? 'selected' : ''}`} onClick={() => openTask(item)} disabled={sending} aria-pressed={item.id === task?.id}><span className="history-icon"><Clock size={18} /></span><span className="history-time"><strong>{time.date.replaceAll('-', '.')}<span>{time.hour}:00</span></strong><small>{item.config.base_asset} / USDT<span>{item.config.exchange === 'binance' ? 'Binance' : item.config.exchange.toUpperCase()}</span></small></span><span className="history-status">{item.id === task?.id && item.status === 'succeeded' ? '正在查看' : statusName[item.status]}</span><ArrowUpRight size={17} /></button>; })}</div> : <p className="no-history">完成第一次分析后，可以在这里回看结果。</p>}{tasks.length > visibleCount && <button className="text-button more-history" onClick={() => setVisibleCount(n => n + 6)}>查看更多记录<CaretDown size={14} /></button>}</section>
      <footer><span>USDT 量化</span><p>现货与永续对冲的历史分析</p><span className="footer-note">历史结果不代表未来收益</span></footer>
    </main>
  </IconContext.Provider>;
}
