/**
 * GoalProgressBars Component
 * Horizontal progress bars for multiple goals
 */

import { COLORS } from '@/constants/colors';

interface Goal {
  id: string;
  name: string;
  current: number;
  target: number;
  color?: string;
}

interface GoalProgressBarsProps {
  goals: Goal[];
  showValues?: boolean;
}

export const GoalProgressBars = ({ goals, showValues = true }: GoalProgressBarsProps) => {
  const getProgressColor = (percentage: number): string => {
    if (percentage >= 75) return COLORS.success;
    if (percentage >= 50) return COLORS.info;
    if (percentage >= 25) return COLORS.warning;
    return COLORS.danger;
  };

  return (
    <div className="space-y-4">
      {goals.map((goal) => {
        const percentage = Math.min((goal.current / goal.target) * 100, 100);
        const color = goal.color || getProgressColor(percentage);

        return (
          <div key={goal.id} className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-gray-700">{goal.name}</span>
              {showValues && (
                <span className="text-sm text-gray-500">
                  ₹{goal.current.toLocaleString()} / ₹{goal.target.toLocaleString()}
                </span>
              )}
            </div>
            <div className="relative w-full h-3 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="absolute top-0 left-0 h-full rounded-full transition-all duration-500 ease-out"
                style={{
                  width: `${percentage}%`,
                  backgroundColor: color,
                }}
              />
            </div>
            <div className="flex justify-between items-center">
              <span className="text-xs text-gray-500">{percentage.toFixed(1)}% complete</span>
              {percentage < 100 && (
                <span className="text-xs text-gray-500">
                  ₹{(goal.target - goal.current).toLocaleString()} remaining
                </span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
