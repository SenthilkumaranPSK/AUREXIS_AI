/**
 * RiskMeter Component
 * Segmented gauge for risk level visualization
 */

import { COLORS } from '@/constants/colors';

interface RiskMeterProps {
  score: number; // 0-100
  size?: number;
  showLabel?: boolean;
}

export const RiskMeter = ({ score, size = 200, showLabel = true }: RiskMeterProps) => {
  const getRiskLevel = (score: number): { label: string; color: string } => {
    if (score <= 20) return { label: 'Very Low', color: COLORS.success };
    if (score <= 40) return { label: 'Low', color: '#84CC16' };
    if (score <= 60) return { label: 'Moderate', color: COLORS.warning };
    if (score <= 80) return { label: 'High', color: '#F97316' };
    return { label: 'Very High', color: COLORS.danger };
  };

  const risk = getRiskLevel(score);
  const rotation = (score / 100) * 180 - 90; // -90 to 90 degrees

  return (
    <div className="flex flex-col items-center">
      <div className="relative" style={{ width: size, height: size / 2 }}>
        {/* Background segments */}
        <svg width={size} height={size / 2} viewBox={`0 0 ${size} ${size / 2}`}>
          <defs>
            <linearGradient id="riskGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor={COLORS.success} />
              <stop offset="25%" stopColor="#84CC16" />
              <stop offset="50%" stopColor={COLORS.warning} />
              <stop offset="75%" stopColor="#F97316" />
              <stop offset="100%" stopColor={COLORS.danger} />
            </linearGradient>
          </defs>
          
          {/* Gauge background */}
          <path
            d={`M ${size * 0.1} ${size / 2} A ${size * 0.4} ${size * 0.4} 0 0 1 ${size * 0.9} ${size / 2}`}
            fill="none"
            stroke="#E5E7EB"
            strokeWidth={size * 0.08}
            strokeLinecap="round"
          />
          
          {/* Colored gauge */}
          <path
            d={`M ${size * 0.1} ${size / 2} A ${size * 0.4} ${size * 0.4} 0 0 1 ${size * 0.9} ${size / 2}`}
            fill="none"
            stroke="url(#riskGradient)"
            strokeWidth={size * 0.08}
            strokeLinecap="round"
            strokeDasharray={`${(score / 100) * (size * 1.256)} ${size * 1.256}`}
          />
        </svg>

        {/* Needle */}
        <div
          className="absolute bottom-0 left-1/2 origin-bottom transition-transform duration-700 ease-out"
          style={{
            width: 3,
            height: size * 0.35,
            backgroundColor: '#374151',
            transform: `translateX(-50%) rotate(${rotation}deg)`,
          }}
        >
          <div
            className="absolute -top-2 left-1/2 -translate-x-1/2 w-4 h-4 rounded-full"
            style={{ backgroundColor: risk.color }}
          />
        </div>

        {/* Center circle */}
        <div
          className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2 bg-white border-4 border-gray-300 rounded-full flex items-center justify-center"
          style={{ width: size * 0.15, height: size * 0.15 }}
        >
          <span className="text-xs font-bold text-gray-700">{score}</span>
        </div>
      </div>

      {showLabel && (
        <div className="mt-4 text-center">
          <div className="text-2xl font-bold" style={{ color: risk.color }}>
            {risk.label}
          </div>
          <div className="text-sm text-gray-500 mt-1">Risk Level</div>
        </div>
      )}
    </div>
  );
};
