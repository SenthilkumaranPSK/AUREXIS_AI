/**
 * TopExpensesBar Component
 * Horizontal bar chart for top expenses
 */

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { CATEGORY_COLORS } from '@/constants/colors';

interface ExpenseItem {
  name: string;
  amount: number;
  category?: string;
}

interface TopExpensesBarProps {
  data: ExpenseItem[];
  height?: number;
  maxItems?: number;
}

export const TopExpensesBar = ({ data, height = 300, maxItems = 10 }: TopExpensesBarProps) => {
  const sortedData = [...data]
    .sort((a, b) => b.amount - a.amount)
    .slice(0, maxItems);

  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart 
        data={sortedData} 
        layout="vertical"
        margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
        <XAxis 
          type="number"
          stroke="#6B7280"
          style={{ fontSize: '12px' }}
          tickFormatter={(value) => `₹${(value / 1000).toFixed(0)}k`}
        />
        <YAxis 
          type="category"
          dataKey="name" 
          stroke="#6B7280"
          style={{ fontSize: '12px' }}
          width={90}
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
        <Bar dataKey="amount" radius={[0, 4, 4, 0]}>
          {sortedData.map((entry, index) => (
            <Cell 
              key={`cell-${index}`} 
              fill={entry.category ? CATEGORY_COLORS[entry.category.toLowerCase()] : '#3B82F6'} 
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};
