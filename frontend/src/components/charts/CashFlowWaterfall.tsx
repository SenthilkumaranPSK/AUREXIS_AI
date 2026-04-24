/**
 * CashFlowWaterfall Component
 * Waterfall chart for cash flow visualization
 */

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';
import { COLORS } from '@/constants/colors';

interface CashFlowItem {
  name: string;
  value: number;
  isTotal?: boolean;
}

interface CashFlowWaterfallProps {
  data: CashFlowItem[];
  height?: number;
}

export const CashFlowWaterfall = ({ data, height = 300 }: CashFlowWaterfallProps) => {
  // Calculate cumulative values for waterfall effect
  let cumulative = 0;
  const chartData = data.map((item) => {
    const start = cumulative;
    cumulative += item.value;
    return {
      ...item,
      start,
      end: cumulative,
      displayValue: item.isTotal ? cumulative : item.value,
    };
  });

  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
        <XAxis 
          dataKey="name" 
          stroke="#6B7280"
          style={{ fontSize: '12px' }}
          angle={-45}
          textAnchor="end"
          height={80}
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
          formatter={(value: number) => [`₹${value.toLocaleString()}`, 'Amount']}
        />
        <ReferenceLine y={0} stroke="#9CA3AF" />
        
        {/* Invisible bars for positioning */}
        <Bar dataKey="start" stackId="stack" fill="transparent" />
        
        {/* Visible bars */}
        <Bar dataKey="displayValue" stackId="stack" radius={[4, 4, 0, 0]}>
          {chartData.map((entry, index) => {
            let color = COLORS.info;
            if (entry.isTotal) {
              color = '#6B7280';
            } else if (entry.value > 0) {
              color = COLORS.success;
            } else if (entry.value < 0) {
              color = COLORS.danger;
            }
            return <Cell key={`cell-${index}`} fill={color} />;
          })}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};
