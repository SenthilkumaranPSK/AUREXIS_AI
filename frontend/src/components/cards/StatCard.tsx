/**
 * Stat Card Component
 * Display key metrics with trend indicators
 */

import { ReactNode, ComponentType } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { TrendingUp, TrendingDown, Minus, LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon?: ReactNode | LucideIcon;
  trend?: 'up' | 'down' | 'neutral';
  className?: string;
  valuePrefix?: string;
  valueSuffix?: string;
}

export function StatCard({
  title,
  value,
  change,
  changeLabel,
  icon,
  trend,
  className,
  valuePrefix = '',
  valueSuffix = '',
}: StatCardProps) {
  const getTrendIcon = () => {
    if (trend === 'up') return <TrendingUp className="h-4 w-4" />;
    if (trend === 'down') return <TrendingDown className="h-4 w-4" />;
    return <Minus className="h-4 w-4" />;
  };

  const getTrendColor = () => {
    if (trend === 'up') return 'text-green-600';
    if (trend === 'down') return 'text-red-600';
    return 'text-gray-600';
  };

  const renderIcon = () => {
    if (!icon) return null;
    
    // If it's a component (function or object with render/$$typeof like forwardRef)
    // but not a React element (already instantiated)
    if (typeof icon === 'function' || (typeof icon === 'object' && 'render' in (icon as any))) {
      const IconComponent = icon as any;
      return <IconComponent className="h-6 w-6" />;
    }
    
    // Otherwise assume it's a ReactNode/Element
    return icon as ReactNode;
  };

  return (
    <Card className={cn('hover:shadow-md transition-shadow', className)}>
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="space-y-2 flex-1">
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <div className="flex items-baseline gap-2">
              <h3 className="text-3xl font-bold tracking-tight">
                {valuePrefix}
                {value !== undefined && value !== null ? (typeof value === 'number' ? value.toLocaleString('en-IN') : value) : '0'}
                {valueSuffix}
              </h3>
            </div>
            {(change !== undefined || changeLabel) && (
              <div className={cn('flex items-center gap-1 text-sm', getTrendColor())}>
                {trend && getTrendIcon()}
                {change !== undefined && (
                  <span className="font-medium">
                    {change > 0 ? '+' : ''}
                    {change}%
                  </span>
                )}
                {changeLabel && (
                  <span className="text-muted-foreground">{changeLabel}</span>
                )}
              </div>
            )}
          </div>
          {icon && (
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
              {renderIcon()}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
