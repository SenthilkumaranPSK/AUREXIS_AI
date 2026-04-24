/**
 * TransactionCard Component
 * Card for displaying transaction details
 */

import { ArrowUpRight, ArrowDownRight, Calendar, Tag } from 'lucide-react';
import { CATEGORY_COLORS, COLORS } from '@/constants/colors';

interface TransactionCardProps {
  id: string;
  description: string;
  amount: number;
  type: 'income' | 'expense';
  category: string;
  date: string;
  merchant?: string;
  onClick?: (id: string) => void;
}

export const TransactionCard = ({
  id,
  description,
  amount,
  type,
  category,
  date,
  merchant,
  onClick,
}: TransactionCardProps) => {
  const isIncome = type === 'income';
  const color = isIncome ? COLORS.success : COLORS.danger;
  const Icon = isIncome ? ArrowUpRight : ArrowDownRight;
  const categoryColor = CATEGORY_COLORS[category.toLowerCase()] || COLORS.info;

  return (
    <div
      className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-all cursor-pointer"
      onClick={() => onClick?.(id)}
    >
      <div className="flex items-start justify-between gap-3">
        {/* Icon */}
        <div
          className="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center"
          style={{ backgroundColor: `${color}20` }}
        >
          <Icon className="w-5 h-5" style={{ color }} />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 mb-1">
            <h4 className="text-sm font-semibold text-gray-900 truncate">
              {description}
            </h4>
            <span
              className="text-base font-bold flex-shrink-0"
              style={{ color }}
            >
              {isIncome ? '+' : '-'}₹{amount.toLocaleString()}
            </span>
          </div>

          {merchant && (
            <p className="text-xs text-gray-500 mb-2">{merchant}</p>
          )}

          <div className="flex items-center gap-3 text-xs text-gray-500">
            <div className="flex items-center gap-1">
              <Calendar className="w-3 h-3" />
              <span>{date}</span>
            </div>
            <div className="flex items-center gap-1">
              <Tag className="w-3 h-3" />
              <span
                className="px-2 py-0.5 rounded font-medium"
                style={{
                  backgroundColor: `${categoryColor}20`,
                  color: categoryColor,
                }}
              >
                {category}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
