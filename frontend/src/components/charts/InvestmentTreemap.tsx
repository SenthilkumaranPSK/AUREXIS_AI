/**
 * InvestmentTreemap Component
 * Treemap for asset allocation visualization
 */

import { Treemap, ResponsiveContainer, Tooltip } from 'recharts';
import { COLORS } from '@/constants/colors';

interface AssetData {
  name: string;
  value: number;
  color?: string;
}

interface InvestmentTreemapProps {
  data: AssetData[];
  height?: number;
}

const ASSET_COLORS: Record<string, string> = {
  stocks: '#3B82F6',
  bonds: '#10B981',
  'mutual funds': '#F59E0B',
  gold: '#EAB308',
  'real estate': '#8B5CF6',
  crypto: '#EC4899',
  cash: '#6B7280',
};

export const InvestmentTreemap = ({ data, height = 400 }: InvestmentTreemapProps) => {
  const formattedData = data.map(item => ({
    ...item,
    color: item.color || ASSET_COLORS[item.name.toLowerCase()] || COLORS.info,
  }));

  const CustomContent = (props: any) => {
    const { x, y, width, height, name, value, color } = props;
    
    if (width < 50 || height < 50) return null;

    return (
      <g>
        <rect
          x={x}
          y={y}
          width={width}
          height={height}
          style={{
            fill: color,
            stroke: '#fff',
            strokeWidth: 2,
          }}
        />
        <text
          x={x + width / 2}
          y={y + height / 2 - 10}
          textAnchor="middle"
          fill="#fff"
          fontSize={14}
          fontWeight="bold"
        >
          {name}
        </text>
        <text
          x={x + width / 2}
          y={y + height / 2 + 10}
          textAnchor="middle"
          fill="#fff"
          fontSize={12}
        >
          ₹{value.toLocaleString()}
        </text>
        <text
          x={x + width / 2}
          y={y + height / 2 + 28}
          textAnchor="middle"
          fill="#fff"
          fontSize={11}
          opacity={0.9}
        >
          {((value / data.reduce((sum, item) => sum + item.value, 0)) * 100).toFixed(1)}%
        </text>
      </g>
    );
  };

  return (
    <ResponsiveContainer width="100%" height={height}>
      <Treemap
        data={formattedData}
        dataKey="value"
        aspectRatio={4 / 3}
        stroke="#fff"
        fill="#8884d8"
        content={<CustomContent />}
      >
        <Tooltip
          contentStyle={{
            backgroundColor: 'white',
            border: '1px solid #E5E7EB',
            borderRadius: '8px',
            padding: '12px',
          }}
          formatter={(value: number) => [`₹${value.toLocaleString()}`, 'Value']}
        />
      </Treemap>
    </ResponsiveContainer>
  );
};
