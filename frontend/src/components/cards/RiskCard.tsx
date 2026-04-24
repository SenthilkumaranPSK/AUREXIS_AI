/**
 * RiskCard Component
 * Card for displaying risk factors and warnings
 */

import { AlertTriangle, Shield, TrendingDown, AlertCircle } from 'lucide-react';
import { COLORS } from '@/constants/colors';

type RiskLevel = 'critical' | 'high' | 'medium' | 'low';

interface RiskCardProps {
  title: string;
  description: string;
  level: RiskLevel;
  impact?: string;
  mitigation?: string;
  onViewDetails?: () => void;
}

const levelConfig = {
  critical: {
    icon: AlertTriangle,
    color: COLORS.danger,
    bgColor: '#FEE2E2',
    label: 'Critical Risk',
  },
  high: {
    icon: AlertCircle,
    color: '#F97316',
    bgColor: '#FFEDD5',
    label: 'High Risk',
  },
  medium: {
    icon: TrendingDown,
    color: COLORS.warning,
    bgColor: '#FEF3C7',
    label: 'Medium Risk',
  },
  low: {
    icon: Shield,
    color: COLORS.success,
    bgColor: '#D1FAE5',
    label: 'Low Risk',
  },
};

export const RiskCard = ({
  title,
  description,
  level,
  impact,
  mitigation,
  onViewDetails,
}: RiskCardProps) => {
  const config = levelConfig[level];
  const Icon = config.icon;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
      {/* Header with colored bar */}
      <div className="h-2" style={{ backgroundColor: config.color }} />

      <div className="p-5">
        {/* Title Section */}
        <div className="flex items-start gap-3 mb-3">
          <div
            className="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center"
            style={{ backgroundColor: config.bgColor }}
          >
            <Icon className="w-5 h-5" style={{ color: config.color }} />
          </div>

          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span
                className="text-xs font-semibold px-2 py-1 rounded"
                style={{
                  backgroundColor: config.bgColor,
                  color: config.color,
                }}
              >
                {config.label}
              </span>
            </div>
            <h4 className="text-base font-semibold text-gray-900">{title}</h4>
          </div>
        </div>

        {/* Description */}
        <p className="text-sm text-gray-600 mb-4">{description}</p>

        {/* Impact */}
        {impact && (
          <div className="bg-gray-50 rounded-lg p-3 mb-3">
            <p className="text-xs font-medium text-gray-500 mb-1">Potential Impact</p>
            <p className="text-sm text-gray-900">{impact}</p>
          </div>
        )}

        {/* Mitigation */}
        {mitigation && (
          <div className="bg-blue-50 rounded-lg p-3 mb-3">
            <p className="text-xs font-medium text-blue-700 mb-1">Recommended Action</p>
            <p className="text-sm text-gray-900">{mitigation}</p>
          </div>
        )}

        {/* Action Button */}
        {onViewDetails && (
          <button
            onClick={onViewDetails}
            className="w-full mt-2 px-4 py-2 rounded-lg text-sm font-medium text-white transition-colors"
            style={{ backgroundColor: config.color }}
          >
            View Details & Solutions
          </button>
        )}
      </div>
    </div>
  );
};
