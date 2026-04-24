/**
 * Application Routes
 * Centralized route definitions for the application
 */

export const ROUTES = {
  // Auth
  LOGIN: '/login',
  SIGNUP: '/signup',
  FORGOT_PASSWORD: '/forgot-password',
  
  // Main Dashboard
  DASHBOARD: '/',
  
  // Core Sections
  FINANCIAL_HEALTH: '/financial-health',
  EXPENSE_ANALYSIS: '/expense-analysis',
  FORECASTING: '/forecasting',
  GOALS: '/goals',
  RISK_ANALYSIS: '/risk-analysis',
  SCENARIO_SIMULATION: '/scenario-simulation',
  INVESTMENTS: '/investments',
  
  // Intelligence
  AI_INSIGHTS: '/ai-insights',
  RECOMMENDATIONS: '/recommendations',
  ALERTS: '/alerts',
  CHAT: '/chat',
  
  // Reports
  REPORTS: '/reports',
  HISTORY: '/history',
  
  // User
  PROFILE: '/profile',
  SETTINGS: '/settings',
  SECURITY: '/security',
  
  // Advanced (Optional)
  TAX_PLANNER: '/tax-planner',
  CREDIT_SCORE: '/credit-score',
  BILLS: '/bills',
  CALENDAR: '/calendar',
  FAMILY: '/family',
} as const;

export type RouteKey = keyof typeof ROUTES;
export type RoutePath = typeof ROUTES[RouteKey];
