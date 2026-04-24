/**
 * Navigation Configuration
 * Sidebar navigation structure with grouped sections
 */

import { 
  LayoutDashboard, 
  Heart, 
  TrendingDown, 
  TrendingUp, 
  Target, 
  AlertTriangle,
  GitCompare,
  PieChart,
  FileText,
  Bell,
  Sparkles,
  MessageSquare,
  User,
  Settings,
  Shield,
  Calculator,
  CreditCard,
  Receipt,
  Calendar,
  Users,
  type LucideIcon
} from 'lucide-react';
import { ROUTES } from './routes';

export interface NavigationItem {
  id: string;
  label: string;
  path: string;
  icon: LucideIcon;
  badge?: string | number;
  description?: string;
}

export interface NavigationSection {
  id: string;
  label: string;
  items: NavigationItem[];
}

export const NAVIGATION: NavigationSection[] = [
  {
    id: 'core',
    label: 'Core',
    items: [
      {
        id: 'dashboard',
        label: 'Overview',
        path: ROUTES.DASHBOARD,
        icon: LayoutDashboard,
        description: 'Financial snapshot',
      },
      {
        id: 'financial-health',
        label: 'Financial Health',
        path: ROUTES.FINANCIAL_HEALTH,
        icon: Heart,
        description: 'Health score & analysis',
      },
      {
        id: 'risk-analysis',
        label: 'Risk Analysis',
        path: ROUTES.RISK_ANALYSIS,
        icon: AlertTriangle,
        description: 'Risk assessment',
      },
    ],
  },
  {
    id: 'finance',
    label: 'Finance',
    items: [
      {
        id: 'expense-analysis',
        label: 'Expenses',
        path: ROUTES.EXPENSE_ANALYSIS,
        icon: TrendingDown,
        description: 'Spending analysis',
      },
      {
        id: 'investments',
        label: 'Investments',
        path: ROUTES.INVESTMENTS,
        icon: PieChart,
        description: 'Portfolio tracking',
      },
      {
        id: 'goals',
        label: 'Goals',
        path: ROUTES.GOALS,
        icon: Target,
        description: 'Financial goals',
      },
    ],
  },
  {
    id: 'intelligence',
    label: 'Intelligence',
    items: [
      {
        id: 'forecasting',
        label: 'Forecasting',
        path: ROUTES.FORECASTING,
        icon: TrendingUp,
        description: 'Future projections',
      },
      {
        id: 'scenario-simulation',
        label: 'Scenario Simulation',
        path: ROUTES.SCENARIO_SIMULATION,
        icon: GitCompare,
        description: 'What-if analysis',
      },
      {
        id: 'ai-insights',
        label: 'AI Insights',
        path: ROUTES.AI_INSIGHTS,
        icon: Sparkles,
        description: 'AI observations',
      },
      {
        id: 'alerts',
        label: 'Alerts',
        path: ROUTES.ALERTS,
        icon: Bell,
        description: 'Notifications',
      },
    ],
  },
  {
    id: 'reports',
    label: 'Reports',
    items: [
      {
        id: 'reports',
        label: 'Reports',
        path: ROUTES.REPORTS,
        icon: FileText,
        description: 'Generate reports',
      },
      {
        id: 'history',
        label: 'History',
        path: ROUTES.HISTORY,
        icon: Calendar,
        description: 'Past records',
      },
    ],
  },
  {
    id: 'user',
    label: 'User',
    items: [
      {
        id: 'profile',
        label: 'Profile',
        path: ROUTES.PROFILE,
        icon: User,
        description: 'User information',
      },
      {
        id: 'security',
        label: 'Security',
        path: ROUTES.SECURITY,
        icon: Shield,
        description: 'Security settings',
      },
      {
        id: 'settings',
        label: 'Settings',
        path: ROUTES.SETTINGS,
        icon: Settings,
        description: 'App preferences',
      },
    ],
  },
];

// Optional advanced features (can be enabled later)
export const ADVANCED_NAVIGATION: NavigationSection = {
  id: 'advanced',
  label: 'Advanced',
  items: [
    {
      id: 'tax-planner',
      label: 'Tax Planner',
      path: ROUTES.TAX_PLANNER,
      icon: Calculator,
      description: 'Tax optimization',
    },
    {
      id: 'credit-score',
      label: 'Credit Score',
      path: ROUTES.CREDIT_SCORE,
      icon: CreditCard,
      description: 'Credit tracking',
    },
    {
      id: 'bills',
      label: 'Bills & Subscriptions',
      path: ROUTES.BILLS,
      icon: Receipt,
      description: 'Recurring payments',
    },
    {
      id: 'family',
      label: 'Family Finance',
      path: ROUTES.FAMILY,
      icon: Users,
      description: 'Shared finances',
    },
  ],
};

// Chat is separate (floating or dedicated page)
export const CHAT_NAVIGATION: NavigationItem = {
  id: 'chat',
  label: 'Chat Assistant',
  path: ROUTES.CHAT,
  icon: MessageSquare,
  description: 'AI financial advisor',
};
