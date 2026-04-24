/**
 * Forecasting Page
 * ML-powered financial predictions and projections
 */

import { PageContainer } from '@/components/layout/PageContainer';
import { ChartCard } from '@/components/cards/ChartCard';
import { StatCard } from '@/components/cards/StatCard';
import { ForecastChart } from '@/components/charts/ForecastChart';
import { TrendLineChart } from '@/components/charts/TrendLineChart';
import { TrendingUp, Target, DollarSign, Calendar } from 'lucide-react';

// Mock data - Historical + Forecast
const incomeForecast = [
  { month: 'Jan', actual: 75000 },
  { month: 'Feb', actual: 75000 },
  { month: 'Mar', actual: 80000 },
  { month: 'Apr', actual: 75000 },
  { month: 'May', actual: 75000 },
  { month: 'Jun', actual: 85000 },
  { month: 'Jul', forecast: 78000, upperBound: 82000, lowerBound: 74000 },
  { month: 'Aug', forecast: 79000, upperBound: 84000, lowerBound: 74000 },
  { month: 'Sep', forecast: 80000, upperBound: 86000, lowerBound: 74000 },
  { month: 'Oct', forecast: 81000, upperBound: 88000, lowerBound: 74000 },
  { month: 'Nov', forecast: 82000, upperBound: 90000, lowerBound: 74000 },
  { month: 'Dec', forecast: 83000, upperBound: 92000, lowerBound: 74000 },
];

const expenseForecast = [
  { month: 'Jan', actual: 55000 },
  { month: 'Feb', actual: 52000 },
  { month: 'Mar', actual: 54000 },
  { month: 'Apr', actual: 51000 },
  { month: 'May', actual: 53000 },
  { month: 'Jun', actual: 55000 },
  { month: 'Jul', forecast: 54000, upperBound: 58000, lowerBound: 50000 },
  { month: 'Aug', forecast: 54500, upperBound: 59000, lowerBound: 50000 },
  { month: 'Sep', forecast: 55000, upperBound: 60000, lowerBound: 50000 },
  { month: 'Oct', forecast: 55500, upperBound: 61000, lowerBound: 50000 },
  { month: 'Nov', forecast: 56000, upperBound: 62000, lowerBound: 50000 },
  { month: 'Dec', forecast: 56500, upperBound: 63000, lowerBound: 50000 },
];

const savingsForecast = [
  { month: 'Jan', actual: 20000 },
  { month: 'Feb', actual: 23000 },
  { month: 'Mar', actual: 26000 },
  { month: 'Apr', actual: 24000 },
  { month: 'May', actual: 22000 },
  { month: 'Jun', actual: 30000 },
  { month: 'Jul', forecast: 24000, upperBound: 28000, lowerBound: 20000 },
  { month: 'Aug', forecast: 24500, upperBound: 29000, lowerBound: 20000 },
  { month: 'Sep', forecast: 25000, upperBound: 30000, lowerBound: 20000 },
  { month: 'Oct', forecast: 25500, upperBound: 31000, lowerBound: 20000 },
  { month: 'Nov', forecast: 26000, upperBound: 32000, lowerBound: 20000 },
  { month: 'Dec', forecast: 26500, upperBound: 33000, lowerBound: 20000 },
];

const netWorthProjection = [
  { month: 'Jan', income: 1200000, expense: 0 },
  { month: 'Feb', income: 1223000, expense: 0 },
  { month: 'Mar', income: 1249000, expense: 0 },
  { month: 'Apr', income: 1273000, expense: 0 },
  { month: 'May', income: 1295000, expense: 0 },
  { month: 'Jun', income: 1325000, expense: 0 },
  { month: 'Jul', income: 1349000, expense: 0 },
  { month: 'Aug', income: 1373500, expense: 0 },
  { month: 'Sep', income: 1398500, expense: 0 },
  { month: 'Oct', income: 1424000, expense: 0 },
  { month: 'Nov', income: 1450000, expense: 0 },
  { month: 'Dec', income: 1476500, expense: 0 },
];

export const ForecastingPage = () => {
  return (
    <PageContainer
      title="Financial Forecasting"
      subtitle="ML-powered predictions for your financial future"
      icon={TrendingUp}
    >
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Projected Income"
          value="₹83,000"
          trend="up"
          trendValue="+10%"
          icon={DollarSign}
          color="#10B981"
        />
        <StatCard
          title="Projected Expenses"
          value="₹56,500"
          trend="up"
          trendValue="+3%"
          icon={TrendingUp}
          color="#F59E0B"
        />
        <StatCard
          title="Projected Savings"
          value="₹26,500"
          trend="up"
          trendValue="+20%"
          icon={Target}
          color="#3B82F6"
        />
        <StatCard
          title="Forecast Period"
          value="6 months"
          trend="neutral"
          icon={Calendar}
          color="#8B5CF6"
        />
      </div>

      {/* ML Confidence Notice */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-bold">
            AI
          </div>
          <div>
            <h4 className="text-sm font-semibold text-blue-900 mb-1">
              Machine Learning Forecast
            </h4>
            <p className="text-sm text-blue-700">
              These predictions are generated using advanced ML algorithms analyzing your historical financial data. 
              Confidence intervals show the range of possible outcomes. Actual results may vary based on your financial decisions.
            </p>
          </div>
        </div>
      </div>

      {/* Income Forecast */}
      <div className="mb-6">
        <ChartCard
          title="Income Forecast"
          subtitle="Next 6 months projection with confidence intervals"
        >
          <ForecastChart 
            data={incomeForecast} 
            height={300} 
            showConfidenceInterval={true}
            currentMonth="Jun"
          />
        </ChartCard>
      </div>

      {/* Expense Forecast */}
      <div className="mb-6">
        <ChartCard
          title="Expense Forecast"
          subtitle="Predicted spending patterns"
        >
          <ForecastChart 
            data={expenseForecast} 
            height={300} 
            showConfidenceInterval={true}
            currentMonth="Jun"
          />
        </ChartCard>
      </div>

      {/* Savings Forecast */}
      <div className="mb-6">
        <ChartCard
          title="Savings Forecast"
          subtitle="Expected savings accumulation"
        >
          <ForecastChart 
            data={savingsForecast} 
            height={300} 
            showConfidenceInterval={true}
            currentMonth="Jun"
          />
        </ChartCard>
      </div>

      {/* Net Worth Projection */}
      <div className="mb-6">
        <ChartCard
          title="Net Worth Projection"
          subtitle="12-month wealth accumulation forecast"
        >
          <TrendLineChart data={netWorthProjection} height={300} />
        </ChartCard>
      </div>

      {/* Forecast Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-green-50 border border-green-200 rounded-lg p-5">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center">
              <TrendingUp className="w-4 h-4" />
            </div>
            <h4 className="font-semibold text-green-900">Positive Trend</h4>
          </div>
          <p className="text-sm text-green-700 mb-2">
            Your income is projected to grow by 10% over the next 6 months, indicating positive career progression.
          </p>
          <p className="text-xs text-green-600">Confidence: 85%</p>
        </div>

        <div className="bg-orange-50 border border-orange-200 rounded-lg p-5">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-full bg-orange-600 text-white flex items-center justify-center">
              <Target className="w-4 h-4" />
            </div>
            <h4 className="font-semibold text-orange-900">Watch Expenses</h4>
          </div>
          <p className="text-sm text-orange-700 mb-2">
            Expenses are expected to increase by 3%. Consider reviewing discretionary spending to maintain savings rate.
          </p>
          <p className="text-xs text-orange-600">Confidence: 78%</p>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-5">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center">
              <DollarSign className="w-4 h-4" />
            </div>
            <h4 className="font-semibold text-blue-900">Savings Growth</h4>
          </div>
          <p className="text-sm text-blue-700 mb-2">
            Your savings are projected to increase by 20%, putting you on track to achieve your financial goals.
          </p>
          <p className="text-xs text-blue-600">Confidence: 82%</p>
        </div>
      </div>
    </PageContainer>
  );
};
