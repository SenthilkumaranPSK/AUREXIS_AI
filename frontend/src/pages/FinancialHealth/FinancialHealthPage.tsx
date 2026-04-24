/**
 * Financial Health Page
 * Detailed financial health analysis with sub-scores and trends
 */

import { PageContainer } from '@/components/layout/PageContainer';
import { ChartCard } from '@/components/cards/ChartCard';
import { StatCard } from '@/components/cards/StatCard';
import { RecommendationCard } from '@/components/cards/RecommendationCard';
import { FinancialHealthGauge } from '@/components/charts/FinancialHealthGauge';
import { TrendLineChart } from '@/components/charts/TrendLineChart';
import { Heart, TrendingUp, Shield, Wallet, PiggyBank } from 'lucide-react';

// Mock data
const healthScore = 85;
const subScores = {
  savings: 90,
  debt: 75,
  emergency: 85,
  investment: 80,
};

const healthTrend = [
  { month: 'Jan', income: 75000, expense: 55000 },
  { month: 'Feb', income: 75000, expense: 52000 },
  { month: 'Mar', income: 80000, expense: 54000 },
  { month: 'Apr', income: 75000, expense: 51000 },
  { month: 'May', income: 75000, expense: 53000 },
  { month: 'Jun', income: 85000, expense: 55000 },
];

const recommendations = [
  {
    title: 'Increase Emergency Fund',
    description: 'Your emergency fund covers 4 months of expenses. Aim for 6 months to improve financial security.',
    type: 'savings' as const,
    impact: 'Increase health score by 5 points',
    priority: 'high' as const,
  },
  {
    title: 'Optimize Debt Repayment',
    description: 'Consider consolidating high-interest debts to reduce monthly payments and save on interest.',
    type: 'risk' as const,
    impact: 'Save ₹5,000/month in interest',
    priority: 'medium' as const,
  },
  {
    title: 'Diversify Investments',
    description: 'Your portfolio is heavily weighted in stocks. Consider adding bonds or gold for better balance.',
    type: 'investment' as const,
    impact: 'Reduce portfolio risk by 15%',
    priority: 'medium' as const,
  },
];

export const FinancialHealthPage = () => {
  return (
    <PageContainer
      title="Financial Health"
      subtitle="Comprehensive analysis of your financial well-being"
      icon={Heart}
    >
      {/* Overall Health Score */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-1">
          <ChartCard title="Overall Health Score" subtitle="Based on multiple factors">
            <div className="flex justify-center py-4">
              <FinancialHealthGauge score={healthScore} size="lg" />
            </div>
          </ChartCard>
        </div>

        <div className="lg:col-span-2">
          <ChartCard title="Health Score Breakdown" subtitle="Individual component scores">
            <div className="grid grid-cols-2 gap-4 py-4">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 mb-2">
                  <PiggyBank className="w-8 h-8 text-green-600" />
                </div>
                <div className="text-2xl font-bold text-gray-900">{subScores.savings}</div>
                <div className="text-sm text-gray-500">Savings Rate</div>
              </div>
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 mb-2">
                  <Shield className="w-8 h-8 text-blue-600" />
                </div>
                <div className="text-2xl font-bold text-gray-900">{subScores.debt}</div>
                <div className="text-sm text-gray-500">Debt Management</div>
              </div>
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-orange-100 mb-2">
                  <Wallet className="w-8 h-8 text-orange-600" />
                </div>
                <div className="text-2xl font-bold text-gray-900">{subScores.emergency}</div>
                <div className="text-sm text-gray-500">Emergency Fund</div>
              </div>
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-purple-100 mb-2">
                  <TrendingUp className="w-8 h-8 text-purple-600" />
                </div>
                <div className="text-2xl font-bold text-gray-900">{subScores.investment}</div>
                <div className="text-sm text-gray-500">Investment Health</div>
              </div>
            </div>
          </ChartCard>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Savings Rate"
          value="32%"
          trend="up"
          trendValue="+3%"
          icon={PiggyBank}
          color="#10B981"
        />
        <StatCard
          title="Debt-to-Income"
          value="28%"
          trend="down"
          trendValue="-2%"
          icon={Shield}
          color="#3B82F6"
        />
        <StatCard
          title="Emergency Fund"
          value="4 months"
          trend="up"
          trendValue="+0.5"
          icon={Wallet}
          color="#F59E0B"
        />
        <StatCard
          title="Credit Score"
          value="750"
          trend="up"
          trendValue="+15"
          icon={TrendingUp}
          color="#8B5CF6"
        />
      </div>

      {/* Health Trend */}
      <div className="mb-6">
        <ChartCard
          title="Income vs Expense Trend"
          subtitle="Last 6 months performance"
        >
          <TrendLineChart data={healthTrend} height={300} />
        </ChartCard>
      </div>

      {/* Recommendations */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Personalized Recommendations
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {recommendations.map((rec, index) => (
            <RecommendationCard
              key={index}
              title={rec.title}
              description={rec.description}
              type={rec.type}
              impact={rec.impact}
              priority={rec.priority}
              onApply={() => {}}
              onDismiss={() => {}}
            />
          ))}
        </div>
      </div>
    </PageContainer>
  );
};
