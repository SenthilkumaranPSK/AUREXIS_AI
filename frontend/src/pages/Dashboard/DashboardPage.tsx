/**
 * Dashboard Overview Page
 * Main dashboard with financial snapshot
 */

import { PageContainer } from '@/components/layout/PageContainer';
import { StatCard } from '@/components/cards/StatCard';
import { FinancialHealthGauge } from '@/components/charts/FinancialHealthGauge';
import { ExpenseDonut } from '@/components/charts/ExpenseDonut';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Wallet, 
  TrendingUp, 
  CreditCard, 
  PiggyBank,
  AlertCircle,
  CheckCircle,
  Info,
  ArrowRight
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';

export function DashboardPage() {
  const navigate = useNavigate();

  // TODO: Fetch from API
  const stats = {
    netWorth: 2500000,
    netWorthChange: 12,
    savingsRate: 25,
    savingsRateChange: 3,
    creditScore: 750,
    creditScoreChange: 10,
    dtiRatio: 35,
    dtiRatioChange: -2,
  };

  const healthScore = 85;

  const expenseData = [
    { category: 'Housing', amount: 40000, percentage: 40 },
    { category: 'Food', amount: 20000, percentage: 20 },
    { category: 'Transport', amount: 15000, percentage: 15 },
    { category: 'Utilities', amount: 10000, percentage: 10 },
    { category: 'Other', amount: 15000, percentage: 15 },
  ];

  const recentAlerts = [
    {
      id: 1,
      type: 'success',
      title: 'Savings Milestone',
      message: "You've saved 20% more than last month!",
      time: '2 hours ago',
    },
    {
      id: 2,
      type: 'warning',
      title: 'Large Expense',
      message: 'Unexpected transaction of ₹15,000 detected.',
      time: '5 hours ago',
    },
    {
      id: 3,
      type: 'info',
      title: 'Goal Progress',
      message: 'Emergency Fund is now 75% complete.',
      time: '1 day ago',
    },
  ];

  const recommendations = [
    {
      id: 1,
      title: 'Reduce Dining Expenses',
      description: 'Save ₹2,000/month by reducing dining out.',
      impact: 'High',
    },
    {
      id: 2,
      title: 'Increase Emergency Fund',
      description: 'Add ₹5,000/month to reach 6-month coverage.',
      impact: 'Medium',
    },
    {
      id: 3,
      title: 'Review Subscriptions',
      description: 'Cancel unused subscriptions to save ₹1,500/month.',
      impact: 'Low',
    },
  ];

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'warning':
        return <AlertCircle className="h-5 w-5 text-yellow-600" />;
      default:
        return <Info className="h-5 w-5 text-blue-600" />;
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'High':
        return 'bg-red-100 text-red-700';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-700';
      default:
        return 'bg-blue-100 text-blue-700';
    }
  };

  return (
    <PageContainer
      title="Dashboard Overview"
      description="Your financial snapshot at a glance"
    >
      <div className="space-y-6">
        {/* KPI Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <StatCard
            title="Net Worth"
            value={stats.netWorth}
            valuePrefix="₹"
            change={stats.netWorthChange}
            trend="up"
            icon={<Wallet className="h-6 w-6" />}
          />
          <StatCard
            title="Savings Rate"
            value={stats.savingsRate}
            valueSuffix="%"
            change={stats.savingsRateChange}
            trend="up"
            icon={<PiggyBank className="h-6 w-6" />}
          />
          <StatCard
            title="Credit Score"
            value={stats.creditScore}
            change={stats.creditScoreChange}
            trend="up"
            icon={<CreditCard className="h-6 w-6" />}
          />
          <StatCard
            title="DTI Ratio"
            value={stats.dtiRatio}
            valueSuffix="%"
            change={stats.dtiRatioChange}
            trend="down"
            icon={<TrendingUp className="h-6 w-6" />}
          />
        </div>

        {/* Financial Health & Expense Breakdown */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Financial Health */}
          <Card>
            <CardHeader>
              <CardTitle>Financial Health Score</CardTitle>
              <CardDescription>
                Your overall financial wellness indicator
              </CardDescription>
            </CardHeader>
            <CardContent>
              <FinancialHealthGauge score={healthScore} size="lg" />
              <div className="mt-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Savings</span>
                  <span className="font-medium">Excellent</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Debt Management</span>
                  <span className="font-medium">Good</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Emergency Fund</span>
                  <span className="font-medium">Fair</span>
                </div>
              </div>
              <Button
                variant="outline"
                className="w-full mt-4"
                onClick={() => navigate(ROUTES.FINANCIAL_HEALTH)}
              >
                View Detailed Analysis
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </CardContent>
          </Card>

          {/* Expense Breakdown */}
          <Card>
            <CardHeader>
              <CardTitle>Expense Breakdown</CardTitle>
              <CardDescription>
                Monthly spending by category
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ExpenseDonut data={expenseData} height={280} />
              <Button
                variant="outline"
                className="w-full mt-4"
                onClick={() => navigate(ROUTES.EXPENSE_ANALYSIS)}
              >
                View Detailed Expenses
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Alerts & Recommendations */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Recent Alerts */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Recent Alerts</CardTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => navigate(ROUTES.ALERTS)}
                >
                  View All
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentAlerts.map((alert) => (
                  <div
                    key={alert.id}
                    className="flex items-start gap-3 rounded-lg border p-3 hover:bg-accent cursor-pointer transition-colors"
                  >
                    {getAlertIcon(alert.type)}
                    <div className="flex-1 space-y-1">
                      <p className="text-sm font-medium">{alert.title}</p>
                      <p className="text-xs text-muted-foreground">
                        {alert.message}
                      </p>
                      <p className="text-xs text-muted-foreground">{alert.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Quick Recommendations */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Quick Recommendations</CardTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => navigate(ROUTES.AI_INSIGHTS)}
                >
                  View All
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recommendations.map((rec) => (
                  <div
                    key={rec.id}
                    className="flex items-start gap-3 rounded-lg border p-3 hover:bg-accent cursor-pointer transition-colors"
                  >
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium">{rec.title}</p>
                        <Badge
                          variant="secondary"
                          className={getImpactColor(rec.impact)}
                        >
                          {rec.impact}
                        </Badge>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {rec.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Goal Progress Summary */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Goal Progress</CardTitle>
                <CardDescription>Track your financial goals</CardDescription>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigate(ROUTES.GOALS)}
              >
                Manage Goals
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium">Emergency Fund</span>
                  <span className="text-muted-foreground">
                    ₹270,000 / ₹360,000
                  </span>
                </div>
                <div className="relative h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="absolute h-full bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-500"
                    style={{ width: '75%' }}
                  />
                </div>
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>75% complete</span>
                  <span>Target: Aug 2026</span>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium">New Car</span>
                  <span className="text-muted-foreground">
                    ₹350,000 / ₹1,200,000
                  </span>
                </div>
                <div className="relative h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="absolute h-full bg-gradient-to-r from-green-500 to-green-600 transition-all duration-500"
                    style={{ width: '29%' }}
                  />
                </div>
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>29% complete</span>
                  <span>Target: Dec 2027</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </PageContainer>
  );
}
