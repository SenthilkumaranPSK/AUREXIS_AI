/**
 * Financial Health Gauge Component
 * Radial progress chart showing health score
 */

import { RadialBarChart, RadialBar, Legend, ResponsiveContainer } from 'recharts';
import { getHealthColor } from '@/constants/colors';
import { cn } from '@/lib/utils';

interface FinancialHealthGaugeProps {
  score: number;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function FinancialHealthGauge({ score, className, size = 'md' }: FinancialHealthGaugeProps) {
  const data = [
    {
      name: 'Health Score',
      value: score,
      fill: getHealthColor(score),
    },
  ];

  const sizeConfig = {
    sm: { height: 150, fontSize: '24px', labelSize: '12px' },
    md: { height: 200, fontSize: '32px', labelSize: '14px' },
    lg: { height: 250, fontSize: '40px', labelSize: '16px' },
  };

  const config = sizeConfig[size];

  const getHealthLabel = (score: number): string => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  };

  return (
    <div className={cn('relative', className)}>
      <ResponsiveContainer width="100%" height={config.height}>
        <RadialBarChart
          cx="50%"
          cy="50%"
          innerRadius="70%"
          outerRadius="100%"
          barSize={20}
          data={data}
          startAngle={180}
          endAngle={0}
        >
          <RadialBar
            minAngle={15}
            background
            clockWise
            dataKey="value"
            cornerRadius={10}
          />
        </RadialBarChart>
      </ResponsiveContainer>

      {/* Center Text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <div className="text-center" style={{ marginTop: config.height * 0.15 }}>
          <div
            className="font-bold"
            style={{ fontSize: config.fontSize, color: getHealthColor(score) }}
          >
            {score}
          </div>
          <div
            className="text-muted-foreground font-medium"
            style={{ fontSize: config.labelSize }}
          >
            {getHealthLabel(score)}
          </div>
        </div>
      </div>
    </div>
  );
}
