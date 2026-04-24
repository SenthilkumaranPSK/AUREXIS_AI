/**
 * ChartCard Component
 * Wrapper card for charts with title and actions
 */

import { ReactNode } from 'react';
import { MoreVertical, Download, Maximize2 } from 'lucide-react';

interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: ReactNode;
  actions?: ReactNode;
  onDownload?: () => void;
  onExpand?: () => void;
  className?: string;
}

export const ChartCard = ({
  title,
  subtitle,
  children,
  actions,
  onDownload,
  onExpand,
  className = '',
}: ChartCardProps) => {
  return (
    <div className={`bg-white rounded-lg shadow-sm border border-gray-200 p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
        </div>
        
        <div className="flex items-center gap-2">
          {actions}
          
          {(onDownload || onExpand) && (
            <div className="flex items-center gap-1">
              {onDownload && (
                <button
                  onClick={onDownload}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  title="Download"
                >
                  <Download className="w-4 h-4 text-gray-600" />
                </button>
              )}
              {onExpand && (
                <button
                  onClick={onExpand}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  title="Expand"
                >
                  <Maximize2 className="w-4 h-4 text-gray-600" />
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Chart Content */}
      <div>{children}</div>
    </div>
  );
};
