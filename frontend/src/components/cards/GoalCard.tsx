/**
 * GoalCard Component
 * Card for displaying financial goals with progress
 */

import { Target, Calendar, TrendingUp, Edit, Trash2 } from 'lucide-react';
import { COLORS } from '@/constants/colors';
import { formatCurrency } from '@/lib/formatters';

interface GoalCardProps {
  id: string;
  name: string;
  targetAmount: number;
  currentAmount: number;
  deadline: string;
  category?: string;
  monthlyRequired?: number;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}

export const GoalCard = ({
  id,
  name,
  targetAmount,
  currentAmount,
  deadline,
  category = 'General',
  monthlyRequired,
  onEdit,
  onDelete,
}: GoalCardProps) => {
  const percentage = Math.min((currentAmount / targetAmount) * 100, 100);
  const remaining = targetAmount - currentAmount;
  
  const getProgressColor = (percentage: number): string => {
    if (percentage >= 75) return COLORS.success;
    if (percentage >= 50) return COLORS.info;
    if (percentage >= 25) return COLORS.warning;
    return COLORS.danger;
  };

  const color = getProgressColor(percentage);

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start gap-3">
          <div
            className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
            style={{ backgroundColor: `${color}20` }}
          >
            <Target className="w-5 h-5" style={{ color }} />
          </div>
          <div>
            <h4 className="text-base font-semibold text-gray-900">{name}</h4>
            <span className="text-xs text-gray-500">{category}</span>
          </div>
        </div>

        <div className="flex items-center gap-1">
          {onEdit && (
            <button
              onClick={() => onEdit(id)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="Edit goal"
            >
              <Edit className="w-4 h-4 text-gray-600" />
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(id)}
              className="p-2 hover:bg-red-50 rounded-lg transition-colors"
              title="Delete goal"
            >
              <Trash2 className="w-4 h-4 text-red-600" />
            </button>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">
            {formatCurrency(currentAmount)}
          </span>
          <span className="text-sm text-gray-500">
            {formatCurrency(targetAmount)}
          </span>
        </div>
        <div className="relative w-full h-3 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="absolute top-0 left-0 h-full rounded-full transition-all duration-500"
            style={{
              width: `${percentage}%`,
              backgroundColor: color,
            }}
          />
        </div>
        <div className="flex justify-between items-center mt-2">
          <span className="text-xs font-medium" style={{ color }}>
            {percentage.toFixed(1)}% complete
          </span>
          <span className="text-xs text-gray-500">
            {formatCurrency(remaining)} remaining
          </span>
        </div>
      </div>

      {/* Footer Info */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <Calendar className="w-4 h-4" />
          <span>{deadline}</span>
        </div>
        {monthlyRequired !== undefined && (
          <div className="flex items-center gap-2 text-sm font-medium" style={{ color }}>
            <TrendingUp className="w-4 h-4" />
            <span>{formatCurrency(monthlyRequired)}/mo</span>
          </div>
        )}
      </div>
    </div>
  );
};
