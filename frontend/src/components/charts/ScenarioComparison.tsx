/**
 * ScenarioComparison Component
 * Side-by-side bar chart for before/after scenario comparison
 */

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { COLORS } from '@/constants/colors';

interface ScenarioData {
  category: string;
  current: number;
  projected: number;
}

interface ScenarioComparisonProps {
  data: ScenarioData[];
  height?: number;
  currentLabel?: string;
  projectedLabel?: string;
}

export const ScenarioComparison = ({ 
  data, 
  height = 300,
  currentLabel = 'Current',
  projectedLabel = 'Projected'
}: ScenarioComparisonProps) => {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
        <XAxis 
          dataKey="category" 
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
        <Bar 
          dataKey="current" 
          fill={COLORS.info}
          radius={[8, 8, 0, 0]}
          name={currentLabel}
        />
        <Bar 
          dataKey="projected" 
          fill={COLORS.success}
          radius={[8, 8, 0, 0]}
          name={projectedLabel}
        />
      </BarChart>
    </ResponsiveContainer>
  );
};
