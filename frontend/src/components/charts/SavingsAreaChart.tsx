/**
 * SavingsAreaChart Component
 * Area chart for visualizing savings growth over time
 */

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { COLORS } from '@/constants/colors';

interface DataPoint {
  month: string;
  savings: number;
  target?: number;
}

interface SavingsAreaChartProps {
  data: DataPoint[];
  height?: number;
  showTarget?: boolean;
}

export const SavingsAreaChart = ({ data, height = 300, showTarget = false }: SavingsAreaChartProps) => {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="colorSavings" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={COLORS.success} stopOpacity={0.8}/>
            <stop offset="95%" stopColor={COLORS.success} stopOpacity={0.1}/>
          </linearGradient>
          {showTarget && (
            <linearGradient id="colorTarget" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={COLORS.info} stopOpacity={0.3}/>
              <stop offset="95%" stopColor={COLORS.info} stopOpacity={0.05}/>
            </linearGradient>
          )}
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
        <XAxis 
          dataKey="month" 
          stroke="#6B7280"
          style={{ fontSize: '12px' }}
        />
        <YAxis 
          stroke="#6B7280"
          style={{ fontSize: '12px' }}
          tickFormatter={(value) => `₹${(value / 1000).toFixed(0)}k`}
        />
        <Tooltip 
          contentStyle={{
            backgroundColor: 'white',
            border: '1px solid #E5E7EB',
            borderRadius: '8px',
            padding: '12px',
          }}
          formatter={(value: number) => [`₹${value.toLocaleString()}`, '']}
        />
        {showTarget && (
          <Area 
            type="monotone" 
            dataKey="target" 
            stroke={COLORS.info}
            strokeWidth={2}
            strokeDasharray="5 5"
            fill="url(#colorTarget)"
            name="Target"
          />
        )}
        <Area 
          type="monotone" 
          dataKey="savings" 
          stroke={COLORS.success}
          strokeWidth={2}
          fillOpacity={1} 
          fill="url(#colorSavings)"
          name="Savings"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
};
