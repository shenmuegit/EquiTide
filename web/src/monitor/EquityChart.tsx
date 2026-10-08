import { useMemo } from 'react';
import { CartesianGrid, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { COSTS, COLORS, clock, date, number, signed } from './data';
import type { Paper } from './data';

export default function EquityChart({ paper, account }: { paper: Paper; account?: string }) {
  const points = useMemo(() => paper.history.map(row => ({ time: Date.parse(row.at),
    '1': account ? row.returns[account]?.['1'] : row.totals['1'].return_pct,
    '2': account ? row.returns[account]?.['2'] : row.totals['2'].return_pct,
    '3': account ? row.returns[account]?.['3'] : row.totals['3'].return_pct })), [paper.history, account]);
  return <div className="equity-chart" role="img" aria-label={`${account || '十组账户合计'}在${paper.observation_count}次真实观察中的成本后累计收益率曲线；回撤限于采样点`}>
    <ResponsiveContainer width="100%" height="100%"><LineChart data={points} margin={{ top: 8, right: 12, bottom: 0, left: 0 }} accessibilityLayer>
      <CartesianGrid stroke="var(--grid)" vertical={false} strokeDasharray="3 5" />
      <XAxis dataKey="time" type="number" domain={['dataMin', 'dataMax']} tickFormatter={clock} minTickGap={45} tick={{ fill: 'var(--muted)', fontSize: 11 }} axisLine={false} tickLine={false} />
      <YAxis tickFormatter={v => `${number(v, 2)}%`} tick={{ fill: 'var(--muted)', fontSize: 12 }} axisLine={false} tickLine={false} domain={['auto', 'auto']} />
      <ReferenceLine y={0} stroke="var(--border)" />
      <Tooltip labelFormatter={v => date(new Date(Number(v)).toISOString())} formatter={(v, name) => [`${signed(Number(v), 4)}%`, `${name}×成本`]} contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12, color: 'var(--text)' }} />
      {COSTS.map((cost, i) => <Line key={cost} type="linear" dataKey={cost} stroke={COLORS[i]} strokeWidth={cost === '1' ? 2.5 : 1.75} strokeDasharray={cost === '2' ? '6 4' : cost === '3' ? '2 4' : undefined} dot={{ r: 3, strokeWidth: 0 }} activeDot={{ r: 5 }} isAnimationActive={false} />)}
    </LineChart></ResponsiveContainer>
  </div>;
}
