/**
 * TrendLineChart Component
 * Line chart for showing trends over time (Income vs Expense)
 */

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { COLORS } from '@/constants/colors';

interface DataPoint {
  month: string;
  income: number;
  expense: number;
  savings?: number;
}

interface TrendLineChartProps {
  data: DataPoint[];
  height?: number;
  showSavings?: boolean;
}

export const TrendLineChart = ({ data, height = 300, showSavings = false }: TrendLineChartProps) => {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
        <Legend 
          wrapperStyle={{ paddingTop: '20px' }}
          iconType="line"
        />
        <Line 
          type="monotone" 
          dataKey="income" 
          stroke={COLORS.success}
          strokeWidth={2}
          dot={{ fill: COLORS.success, r: 4 }}
          activeDot={{ r: 6 }}
          name="Income"
        />
        <Line 
          type="monotone" 
          dataKey="expense" 
          stroke={COLORS.danger}
          strokeWidth={2}
          dot={{ fill: COLORS.danger, r: 4 }}
          activeDot={{ r: 6 }}
          name="Expense"
        />
        {showSavings && (
          <Line 
            type="monotone" 
            dataKey="savings" 
            stroke={COLORS.info}
            strokeWidth={2}
            dot={{ fill: COLORS.info, r: 4 }}
            activeDot={{ r: 6 }}
            name="Savings"
          />
        )}
      </LineChart>
    </ResponsiveContainer>
  );
};
