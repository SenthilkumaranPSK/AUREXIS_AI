/**
 * Risk Analysis Page
 * Comprehensive financial risk assessment
 */

import { PageContainer } from '@/components/layout/PageContainer';
import { ChartCard } from '@/components/cards/ChartCard';
import { StatCard } from '@/components/cards/StatCard';
import { RiskCard } from '@/components/cards/RiskCard';
import { RiskMeter } from '@/components/charts/RiskMeter';
import { TrendLineChart } from '@/components/charts/TrendLineChart';
import { AlertTriangle, Shield, TrendingDown, CreditCard } from 'lucide-react';

// Mock data
const overallRisk = 35; // 0-100
const debtToIncome = 28;
const creditScore = 750;
const emergencyFund = 4; // months

const riskFactors = [
  {
    title: 'High Debt-to-Income Ratio',
    description: 'Your DTI ratio of 28% is approaching the recommended maximum of 30%. Consider reducing debt or increasing income.',
    level: 'medium' as const,
    impact: 'May affect loan approval and interest rates',
    mitigation: 'Pay down high-interest debt first, starting with credit cards',
  },
  {
    title: 'Insufficient Emergency Fund',
    description: 'Your emergency fund covers only 4 months of expenses. Financial experts recommend 6-12 months.',
    level: 'medium' as const,
    impact: 'Vulnerable to unexpected expenses or income loss',
    mitigation: 'Increase monthly savings by ₹5,000 to reach 6-month target in 8 months',
  },
  {
    title: 'Concentrated Investment Portfolio',
    description: 'Over 70% of your investments are in stocks, creating high market risk exposure.',
    level: 'high' as const,
    impact: 'Portfolio value could drop significantly during market downturns',
    mitigation: 'Diversify into bonds, gold, and real estate to reduce volatility',
  },
  {
    title: 'No Life Insurance',
    description: 'You don\'t have adequate life insurance coverage for your dependents.',
    level: 'critical' as const,
    impact: 'Family would face financial hardship in case of unexpected events',
    mitigation: 'Get term life insurance with coverage of at least 10x annual income',
  },
];

const riskTrend = [
  { month: 'Jan', income: 45, expense: 0, savings: 0 },
  { month: 'Feb', income: 42, expense: 0, savings: 0 },
  { month: 'Mar', income: 40, expense: 0, savings: 0 },
  { month: 'Apr', income: 38, expense: 0, savings: 0 },
  { month: 'May', income: 36, expense: 0, savings: 0 },
  { month: 'Jun', income: 35, expense: 0, savings: 0 },
];

export const RiskAnalysisPage = () => {
  return (
    <PageContainer
      title="Risk Analysis"
      subtitle="Comprehensive assessment of your financial risks"
      icon={AlertTriangle}
    >
      {/* Overall Risk Score */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-1">
          <ChartCard title="Overall Risk Score" subtitle="Lower is better">
            <div className="flex justify-center py-4">
              <RiskMeter score={overallRisk} size={200} />
            </div>
          </ChartCard>
        </div>

        <div className="lg:col-span-2">
          <ChartCard title="Risk Trend" subtitle="Last 6 months">
            <TrendLineChart data={riskTrend} height={250} />
          </ChartCard>
        </div>
      </div>

      {/* Key Risk Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Debt-to-Income"
          value={`${debtToIncome}%`}
          trend="down"
          trendValue="-2%"
          icon={TrendingDown}
          color="#F59E0B"
        />
        <StatCard
          title="Credit Score"
          value={creditScore.toString()}
          trend="up"
          trendValue="+15"
          icon={CreditCard}
          color="#10B981"
        />
        <StatCard
          title="Emergency Fund"
          value={`${emergencyFund} months`}
          trend="up"
          trendValue="+0.5"
          icon={Shield}
          color="#3B82F6"
        />
        <StatCard
          title="Risk Factors"
          value={riskFactors.length.toString()}
          trend="down"
          trendValue="-1"
          icon={AlertTriangle}
          color="#EF4444"
        />
      </div>

      {/* Risk Factors */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Identified Risk Factors
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {riskFactors.map((risk, index) => (
            <RiskCard
              key={index}
              title={risk.title}
              description={risk.description}
              level={risk.level}
              impact={risk.impact}
              mitigation={risk.mitigation}
              onViewDetails={() => {}}
            />
          ))}
        </div>
      </div>

      {/* Risk Mitigation Summary */}
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">
          Risk Mitigation Plan
        </h3>
        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-bold">
              1
            </div>
            <div>
              <p className="text-sm font-medium text-blue-900">Immediate Action (This Month)</p>
              <p className="text-sm text-blue-700">Get term life insurance and increase emergency fund contribution to ₹5,000/month</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-bold">
              2
            </div>
            <div>
              <p className="text-sm font-medium text-blue-900">Short-term (3-6 Months)</p>
              <p className="text-sm text-blue-700">Pay down credit card debt and diversify investment portfolio</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-bold">
              3
            </div>
            <div>
              <p className="text-sm font-medium text-blue-900">Long-term (6-12 Months)</p>
              <p className="text-sm text-blue-700">Achieve 6-month emergency fund and reduce DTI ratio below 25%</p>
            </div>
          </div>
        </div>
      </div>
    </PageContainer>
  );
};
