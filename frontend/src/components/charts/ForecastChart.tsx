/**
 * ForecastChart Component
 * Line chart with dotted projection for forecasting
 */

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { COLORS } from '@/constants/colors';

interface DataPoint {
  month: string;
  actual?: number;
  forecast?: number;
  upperBound?: number;
  lowerBound?: number;
}

interface ForecastChartProps {
  data: DataPoint[];
  height?: number;
  showConfidenceInterval?: boolean;
  currentMonth?: string;
}

export const ForecastChart = ({ 
  data, 
  height = 300, 
  showConfidenceInterval = true,
  currentMonth 
}: ForecastChartProps) => {
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
        <Legend />
        
        {currentMonth && (
          <ReferenceLine 
            x={currentMonth} 
            stroke="#9CA3AF" 
            strokeDasharray="3 3"
            label={{ value: 'Today', position: 'top', fill: '#6B7280' }}
          />
        )}

        {/* Confidence interval */}
        {showConfidenceInterval && (
          <>
            <Line 
              type="monotone" 
              dataKey="upperBound" 
              stroke={COLORS.info}
              strokeWidth={1}
              strokeDasharray="3 3"
              dot={false}
              name="Upper Bound"
              strokeOpacity={0.5}
            />
            <Line 
              type="monotone" 
              dataKey="lowerBound" 
              stroke={COLORS.info}
              strokeWidth={1}
              strokeDasharray="3 3"
              dot={false}
              name="Lower Bound"
              strokeOpacity={0.5}
            />
          </>
        )}

        {/* Actual data */}
        <Line 
          type="monotone" 
          dataKey="actual" 
          stroke={COLORS.info}
          strokeWidth={2}
          dot={{ fill: COLORS.info, r: 4 }}
          activeDot={{ r: 6 }}
          name="Actual"
        />

        {/* Forecast */}
        <Line 
          type="monotone" 
          dataKey="forecast" 
          stroke={COLORS.success}
          strokeWidth={2}
          strokeDasharray="5 5"
          dot={{ fill: COLORS.success, r: 4 }}
          activeDot={{ r: 6 }}
          name="Forecast"
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
