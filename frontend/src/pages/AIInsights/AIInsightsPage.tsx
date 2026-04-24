/**
 * AI Insights Page
 * AI-generated observations and pattern detection
 */

import { PageContainer } from '@/components/layout/PageContainer';
import { StatCard } from '@/components/cards/StatCard';
import { Sparkles, TrendingUp, AlertCircle, Target, Lightbulb } from 'lucide-react';

// Mock data
const insights = [
  {
    id: '1',
    category: 'Spending Pattern',
    title: 'Weekend Spending Spike Detected',
    description: 'Your spending increases by 35% on weekends, primarily on dining and entertainment. Consider setting a weekend budget to maintain your savings goals.',
    impact: 'High',
    confidence: 92,
    icon: TrendingUp,
    color: '#F59E0B',
    actionable: true,
    recommendation: 'Set a weekend spending limit of ₹5,000',
  },
  {
    id: '2',
    category: 'Savings Behavior',
    title: 'Consistent Savings Pattern',
    description: 'You\'ve maintained a 30%+ savings rate for 6 consecutive months. This disciplined approach puts you ahead of 85% of users in your income bracket.',
    impact: 'Positive',
    confidence: 95,
    icon: Target,
    color: '#10B981',
    actionable: false,
    recommendation: null,
  },
  {
    id: '3',
    category: 'Risk Alert',
    title: 'Emergency Fund Below Recommended',
    description: 'Your emergency fund covers only 4 months of expenses. Financial experts recommend 6-12 months. A sudden income loss could impact your financial stability.',
    impact: 'High',
    confidence: 88,
    icon: AlertCircle,
    color: '#EF4444',
    actionable: true,
    recommendation: 'Increase monthly emergency fund contribution by ₹5,000',
  },
  {
    id: '4',
    category: 'Income Trend',
    title: 'Income Growth Trajectory',
    description: 'Your income has grown by 12% over the past year, outpacing inflation. This trend suggests strong career progression and earning potential.',
    impact: 'Positive',
    confidence: 90,
    icon: TrendingUp,
    color: '#10B981',
    actionable: false,
    recommendation: null,
  },
  {
    id: '5',
    category: 'Expense Optimization',
    title: 'Subscription Overlap Detected',
    description: 'You have 3 streaming subscriptions with overlapping content. Consolidating to 2 subscriptions could save ₹500/month (₹6,000/year).',
    impact: 'Medium',
    confidence: 85,
    icon: Lightbulb,
    color: '#3B82F6',
    actionable: true,
    recommendation: 'Review and cancel redundant subscriptions',
  },
  {
    id: '6',
    category: 'Goal Progress',
    title: 'On Track for Major Goals',
    description: 'Based on current savings rate, you\'re projected to achieve your Emergency Fund goal 2 months ahead of schedule and Car Purchase goal on time.',
    impact: 'Positive',
    confidence: 87,
    icon: Target,
    color: '#10B981',
    actionable: false,
    recommendation: null,
  },
  {
    id: '7',
    category: 'Spending Anomaly',
    title: 'Unusual Healthcare Spending',
    description: 'Healthcare expenses increased by 150% this month. If this is a one-time event, no action needed. If recurring, consider reviewing health insurance coverage.',
    impact: 'Medium',
    confidence: 78,
    icon: AlertCircle,
    color: '#F59E0B',
    actionable: true,
    recommendation: 'Review health insurance coverage adequacy',
  },
  {
    id: '8',
    category: 'Investment Behavior',
    title: 'Diversification Improving',
    description: 'You\'ve successfully reduced stock concentration from 75% to 65% over the past quarter. Continue this trend to achieve optimal risk-adjusted returns.',
    impact: 'Positive',
    confidence: 91,
    icon: TrendingUp,
    color: '#10B981',
    actionable: false,
    recommendation: null,
  },
];

const patterns = [
  {
    pattern: 'Monthly Cycle',
    description: 'Spending peaks in the first week after salary credit, then stabilizes',
    frequency: 'Every month',
  },
  {
    pattern: 'Seasonal Variation',
    description: 'Higher expenses during festival months (Oct-Dec)',
    frequency: 'Annually',
  },
  {
    pattern: 'Impulse Purchases',
    description: 'Online shopping increases during sale events',
    frequency: 'Quarterly',
  },
];

export const AIInsightsPage = () => {
  const totalInsights = insights.length;
  const actionableInsights = insights.filter(i => i.actionable).length;
  const positiveInsights = insights.filter(i => i.impact === 'Positive').length;
  const avgConfidence = Math.round(insights.reduce((sum, i) => sum + i.confidence, 0) / insights.length);

  return (
    <PageContainer
      title="AI Insights"
      subtitle="Intelligent observations and pattern detection from your financial data"
      icon={Sparkles}
    >
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Total Insights"
          value={totalInsights.toString()}
          trend="up"
          trendValue="+2"
          icon={Sparkles}
          color="#8B5CF6"
        />
        <StatCard
          title="Actionable"
          value={actionableInsights.toString()}
          trend="neutral"
          icon={Lightbulb}
          color="#F59E0B"
        />
        <StatCard
          title="Positive Trends"
          value={positiveInsights.toString()}
          trend="up"
          trendValue="+1"
          icon={TrendingUp}
          color="#10B981"
        />
        <StatCard
          title="Avg Confidence"
          value={`${avgConfidence}%`}
          trend="neutral"
          icon={Target}
          color="#3B82F6"
        />
      </div>

      {/* AI Notice */}
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-600 text-white flex items-center justify-center">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-sm font-semibold text-purple-900 mb-1">
              AI-Powered Analysis
            </h4>
            <p className="text-sm text-purple-700">
              These insights are generated by analyzing your financial behavior patterns, spending trends, and comparing with similar user profiles. 
              Confidence scores indicate the reliability of each observation.
            </p>
          </div>
        </div>
      </div>

      {/* Insights Grid */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Personalized Insights
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {insights.map((insight) => {
            const Icon = insight.icon;
            const impactColor = 
              insight.impact === 'Positive' ? 'green' :
              insight.impact === 'High' ? 'red' :
              'orange';

            return (
              <div
                key={insight.id}
                className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow"
              >
                {/* Header */}
                <div className="flex items-start gap-3 mb-3">
                  <div
                    className="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center"
                    style={{ backgroundColor: `${insight.color}20` }}
                  >
                    <Icon className="w-5 h-5" style={{ color: insight.color }} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-medium text-gray-500">
                        {insight.category}
                      </span>
                      <span
                        className={`text-xs font-semibold px-2 py-0.5 rounded bg-${impactColor}-100 text-${impactColor}-700`}
                      >
                        {insight.impact}
                      </span>
                    </div>
                    <h4 className="text-base font-semibold text-gray-900">
                      {insight.title}
                    </h4>
                  </div>
                </div>

                {/* Description */}
                <p className="text-sm text-gray-600 mb-3">
                  {insight.description}
                </p>

                {/* Recommendation */}
                {insight.actionable && insight.recommendation && (
                  <div className="bg-blue-50 rounded-lg p-3 mb-3">
                    <p className="text-xs font-medium text-blue-700 mb-1">
                      Recommended Action
                    </p>
                    <p className="text-sm text-blue-900">
                      {insight.recommendation}
                    </p>
                  </div>
                )}

                {/* Footer */}
                <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                  <div className="flex items-center gap-2">
                    <div className="w-full bg-gray-200 rounded-full h-1.5 w-20">
                      <div
                        className="bg-purple-600 h-1.5 rounded-full"
                        style={{ width: `${insight.confidence}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-500">
                      {insight.confidence}% confidence
                    </span>
                  </div>
                  {insight.actionable && (
                    <button className="text-xs font-medium text-blue-600 hover:text-blue-700">
                      Take Action →
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Detected Patterns */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Detected Patterns
        </h3>
        <div className="space-y-4">
          {patterns.map((pattern, index) => (
            <div
              key={index}
              className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-sm font-bold">
                {index + 1}
              </div>
              <div className="flex-1">
                <h4 className="text-sm font-semibold text-gray-900 mb-1">
                  {pattern.pattern}
                </h4>
                <p className="text-sm text-gray-600 mb-2">
                  {pattern.description}
                </p>
                <span className="text-xs text-gray-500">
                  Frequency: {pattern.frequency}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </PageContainer>
  );
};
