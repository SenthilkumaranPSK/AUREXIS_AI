/**
 * AlertCard Component
 * Card for displaying alerts and notifications
 */

import { AlertTriangle, AlertCircle, Info, CheckCircle, X } from 'lucide-react';
import { COLORS } from '@/constants/colors';

type AlertSeverity = 'critical' | 'warning' | 'info' | 'success';

interface AlertCardProps {
  title: string;
  message: string;
  severity: AlertSeverity;
  timestamp?: string;
  onDismiss?: () => void;
  onAction?: () => void;
  actionLabel?: string;
}

const severityConfig = {
  critical: {
    icon: AlertTriangle,
    color: COLORS.danger,
    bgColor: '#FEE2E2',
    borderColor: '#FCA5A5',
  },
  warning: {
    icon: AlertCircle,
    color: COLORS.warning,
    bgColor: '#FEF3C7',
    borderColor: '#FCD34D',
  },
  info: {
    icon: Info,
    color: COLORS.info,
    bgColor: '#DBEAFE',
    borderColor: '#93C5FD',
  },
  success: {
    icon: CheckCircle,
    color: COLORS.success,
    bgColor: '#D1FAE5',
    borderColor: '#6EE7B7',
  },
};

export const AlertCard = ({
  title,
  message,
  severity,
  timestamp,
  onDismiss,
  onAction,
  actionLabel = 'View Details',
}: AlertCardProps) => {
  const config = severityConfig[severity];
  const Icon = config.icon;

  return (
    <div
      className="rounded-lg border-l-4 p-4 shadow-sm"
      style={{
        backgroundColor: config.bgColor,
        borderLeftColor: config.color,
      }}
    >
      <div className="flex items-start gap-3">
        <Icon className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: config.color }} />
        
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <h4 className="text-sm font-semibold text-gray-900">{title}</h4>
            {onDismiss && (
              <button
                onClick={onDismiss}
                className="flex-shrink-0 p-1 hover:bg-white/50 rounded transition-colors"
              >
                <X className="w-4 h-4 text-gray-600" />
              </button>
            )}
          </div>
          
          <p className="text-sm text-gray-700 mt-1">{message}</p>
          
          <div className="flex items-center justify-between mt-3">
            {timestamp && (
              <span className="text-xs text-gray-500">{timestamp}</span>
            )}
            {onAction && (
              <button
                onClick={onAction}
                className="text-xs font-medium hover:underline"
                style={{ color: config.color }}
              >
                {actionLabel} →
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
