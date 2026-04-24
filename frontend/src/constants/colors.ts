/**
 * Color Palette
 * Consistent color scheme across the application
 */

export const COLORS = {
  // Status Colors
  success: '#10B981',
  warning: '#F59E0B',
  danger: '#EF4444',
  info: '#3B82F6',
  
  // Category Colors
  housing: '#3B82F6',
  food: '#F59E0B',
  transport: '#10B981',
  utilities: '#EC4899',
  entertainment: '#8B5CF6',
  healthcare: '#06B6D4',
  education: '#F97316',
  shopping: '#EF4444',
  other: '#6B7280',
  
  // Chart Colors
  chart: {
    primary: '#3B82F6',
    secondary: '#10B981',
    tertiary: '#F59E0B',
    quaternary: '#EC4899',
    quinary: '#8B5CF6',
  },
  
  // Gradient Colors
  gradient: {
    start: '#3B82F6',
    end: '#1D4ED8',
  },
  
  // Neutral Colors
  gray: {
    50: '#F9FAFB',
    100: '#F3F4F6',
    200: '#E5E7EB',
    300: '#D1D5DB',
    400: '#9CA3AF',
    500: '#6B7280',
    600: '#4B5563',
    700: '#374151',
    800: '#1F2937',
    900: '#111827',
  },
  
  // Risk Levels
  risk: {
    low: '#10B981',
    medium: '#F59E0B',
    high: '#EF4444',
  },
  
  // Health Score
  health: {
    excellent: '#10B981',
    good: '#3B82F6',
    fair: '#F59E0B',
    poor: '#EF4444',
  },
} as const;

export const CATEGORY_COLORS: Record<string, string> = {
  Housing: COLORS.housing,
  Food: COLORS.food,
  Transport: COLORS.transport,
  Utilities: COLORS.utilities,
  Entertainment: COLORS.entertainment,
  Healthcare: COLORS.healthcare,
  Education: COLORS.education,
  Shopping: COLORS.shopping,
  Other: COLORS.other,
};

export const getHealthColor = (score: number): string => {
  if (score >= 80) return COLORS.health.excellent;
  if (score >= 60) return COLORS.health.good;
  if (score >= 40) return COLORS.health.fair;
  return COLORS.health.poor;
};

export const getRiskColor = (level: 'low' | 'medium' | 'high'): string => {
  return COLORS.risk[level];
};

export const getCategoryColor = (category: string): string => {
  return CATEGORY_COLORS[category] || COLORS.other;
};
