/**
 * CategoryStackedBar Component
 * Stacked bar chart for category breakdown over time
 */

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { CATEGORY_COLORS } from '@/constants/colors';

interface CategoryStackedBarProps {
  data: any[];
  categories: string[];
  height?: number;
}

export const CategoryStackedBar = ({ data, categories, height = 300 }: CategoryStackedBarProps) => {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
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
        <Legend />
        {categories.map((category) => (
          <Bar 
            key={category}
            dataKey={category}
            stackId="a"
            fill={CATEGORY_COLORS[category.toLowerCase()] || '#6B7280'}
            name={category}
          />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
};
