/**
 * SpendingHeatmap Component
 * Calendar heatmap for daily spending patterns
 */

import { COLORS } from '@/constants/colors';

interface DayData {
  date: string;
  amount: number;
}

interface SpendingHeatmapProps {
  data: DayData[];
  height?: number;
}

export const SpendingHeatmap = ({ data, height = 200 }: SpendingHeatmapProps) => {
  const maxAmount = Math.max(...data.map(d => d.amount));
  
  const getColor = (amount: number): string => {
    const intensity = amount / maxAmount;
    if (intensity === 0) return '#F3F4F6';
    if (intensity < 0.25) return '#DBEAFE';
    if (intensity < 0.5) return '#93C5FD';
    if (intensity < 0.75) return '#3B82F6';
    return '#1E40AF';
  };

  const weeks = 12;
  const days = 7;

  return (
    <div className="space-y-4">
      <div className="flex gap-1" style={{ height }}>
        {Array.from({ length: weeks }).map((_, weekIndex) => (
          <div key={weekIndex} className="flex flex-col gap-1 flex-1">
            {Array.from({ length: days }).map((_, dayIndex) => {
              const dataIndex = weekIndex * days + dayIndex;
              const dayData = data[dataIndex];
              const amount = dayData?.amount || 0;
              
              return (
                <div
                  key={dayIndex}
                  className="flex-1 rounded-sm cursor-pointer hover:ring-2 hover:ring-blue-500 transition-all"
                  style={{ backgroundColor: getColor(amount) }}
                  title={dayData ? `${dayData.date}: ₹${amount.toLocaleString()}` : 'No data'}
                />
              );
            })}
          </div>
        ))}
      </div>
      
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>Less</span>
        <div className="flex gap-1">
          {[0, 0.25, 0.5, 0.75, 1].map((intensity, i) => (
            <div
              key={i}
              className="w-4 h-4 rounded-sm"
              style={{ backgroundColor: getColor(maxAmount * intensity) }}
            />
          ))}
        </div>
        <span>More</span>
      </div>
    </div>
  );
};
