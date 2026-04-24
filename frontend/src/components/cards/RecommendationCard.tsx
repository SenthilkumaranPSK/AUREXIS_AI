/**
 * RecommendationCard Component
 * Card for displaying AI recommendations
 */

import { Lightbulb, TrendingUp, Shield, Target, ArrowRight } from 'lucide-react';
import { COLORS } from '@/constants/colors';

type RecommendationType = 'savings' | 'investment' | 'risk' | 'goal' | 'general';

interface RecommendationCardProps {
  title: string;
  description: string;
  type: RecommendationType;
  impact?: string;
  priority?: 'high' | 'medium' | 'low';
  onApply?: () => void;
  onDismiss?: () => void;
}

const typeConfig = {
  savings: {
    icon: TrendingUp,
    color: COLORS.success,
    label: 'Savings',
  },
  investment: {
    icon: Target,
    color: COLORS.info,
    label: 'Investment',
  },
  risk: {
    icon: Shield,
    color: COLORS.warning,
    label: 'Risk',
  },
  goal: {
    icon: Target,
    color: '#8B5CF6',
    label: 'Goal',
  },
  general: {
    icon: Lightbulb,
    color: '#F59E0B',
    label: 'Insight',
  },
};

const priorityColors = {
  high: COLORS.danger,
  medium: COLORS.warning,
  low: COLORS.info,
};

export const RecommendationCard = ({
  title,
  description,
  type,
  impact,
  priority = 'medium',
  onApply,
  onDismiss,
}: RecommendationCardProps) => {
  const config = typeConfig[type];
  const Icon = config.icon;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-4">
        <div
          className="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center"
          style={{ backgroundColor: `${config.color}20` }}
        >
          <Icon className="w-5 h-5" style={{ color: config.color }} />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 mb-2">
            <div>
              <span
                className="text-xs font-medium px-2 py-1 rounded"
                style={{
                  backgroundColor: `${config.color}20`,
                  color: config.color,
                }}
              >
                {config.label}
              </span>
              {priority && (
                <span
                  className="ml-2 text-xs font-medium px-2 py-1 rounded"
                  style={{
                    backgroundColor: `${priorityColors[priority]}20`,
                    color: priorityColors[priority],
                  }}
                >
                  {priority.toUpperCase()}
                </span>
              )}
            </div>
          </div>

          <h4 className="text-base font-semibold text-gray-900 mb-2">{title}</h4>
          <p className="text-sm text-gray-600 mb-3">{description}</p>

          {impact && (
            <div className="bg-gray-50 rounded-lg p-3 mb-3">
              <p className="text-xs font-medium text-gray-500 mb-1">Expected Impact</p>
              <p className="text-sm text-gray-900">{impact}</p>
            </div>
          )}

          <div className="flex items-center gap-2">
            {onApply && (
              <button
                onClick={onApply}
                className="flex items-center gap-1 px-4 py-2 rounded-lg text-sm font-medium text-white transition-colors"
                style={{ backgroundColor: config.color }}
              >
                Apply
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
            {onDismiss && (
              <button
                onClick={onDismiss}
                className="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors"
              >
                Dismiss
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
