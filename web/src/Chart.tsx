import { Area, AreaChart, CartesianGrid, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { useId } from 'react';
import type { EquityPoint } from './api';

const clock = new Intl.DateTimeFormat('zh-CN', { timeZone: 'Asia/Shanghai', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
const moment = new Intl.DateTimeFormat('zh-CN', { timeZone: 'Asia/Shanghai', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });

export default function ReplayChart({ points, entryNs, exitNs }: { points: EquityPoint[]; entryNs: number; exitNs: number }) {
  const fillId = useId();
  const ticks = Array.from({ length: 5 }, (_, i) => entryNs + (exitNs - entryNs) * i / 4);
  return <div className="replay-chart" role="img" aria-label="模拟买入后 24 小时的净收益曲线，单位 USDT；可用左右方向键查看时间点。">
    <ResponsiveContainer width="100%" height="100%" minWidth={0}>
      <AreaChart data={points} margin={{ top: 16, right: 8, left: 0, bottom: 0 }} accessibilityLayer>
        <defs><linearGradient id={fillId} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="var(--accent)" stopOpacity={0.13} /><stop offset="100%" stopColor="var(--accent)" stopOpacity={0.01} /></linearGradient></defs>
        <CartesianGrid vertical={false} stroke="var(--chart-grid)" strokeDasharray="3 5" />
        <XAxis type="number" dataKey="ts" domain={[entryNs, exitNs]} ticks={ticks} axisLine={false} tickLine={false} tickMargin={14} height={38} tick={{ fill: 'var(--muted)', fontSize: 11 }} tickFormatter={n => clock.format(new Date(n / 1e6))} minTickGap={22} />
        <YAxis width={43} axisLine={false} tickLine={false} tickMargin={12} tick={{ fill: 'var(--muted)', fontSize: 11 }} tickFormatter={n => Number(n).toFixed(1)} domain={['auto', 'auto']} />
        <ReferenceLine y={0} stroke="var(--muted)" strokeOpacity={0.6} strokeDasharray="4 4" />
        <Tooltip labelFormatter={n => moment.format(new Date(Number(n) / 1e6))} formatter={value => [`${Number(value).toFixed(4)} USDT`, '模拟净收益']} contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, color: 'var(--text)', fontSize: 12, boxShadow: 'var(--shadow)' }} labelStyle={{ color: 'var(--muted)', marginBottom: 6 }} itemStyle={{ color: 'var(--text)' }} cursor={{ stroke: 'var(--accent)', strokeDasharray: '3 4' }} />
        <Area type="linear" dataKey="pnl" stroke="var(--accent)" strokeWidth={1.8} fill={`url(#${fillId})`} baseValue="dataMin" dot={false} activeDot={{ r: 4, stroke: 'var(--surface)', strokeWidth: 2, fill: 'var(--accent)' }} isAnimationActive={false} />
      </AreaChart>
    </ResponsiveContainer>
  </div>;
}
