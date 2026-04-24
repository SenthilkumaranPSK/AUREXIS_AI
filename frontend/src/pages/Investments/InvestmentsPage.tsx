/**
 * Investments Page
 * Portfolio tracking and investment analysis
 */

import { PageContainer } from '@/components/layout/PageContainer';
import { ChartCard } from '@/components/cards/ChartCard';
import { StatCard } from '@/components/cards/StatCard';
import { InvestmentTreemap } from '@/components/charts/InvestmentTreemap';
import { TrendLineChart } from '@/components/charts/TrendLineChart';
import { PieChart, TrendingUp, DollarSign, Percent, AlertTriangle } from 'lucide-react';

// Mock data
const totalInvestment = 850000;
const currentValue = 925000;
const returns = 75000;
const returnPercentage = 8.82;

const assetAllocation = [
  { name: 'Stocks', value: 370000 },
  { name: 'Mutual Funds', value: 250000 },
  { name: 'Bonds', value: 150000 },
  { name: 'Gold', value: 100000 },
  { name: 'Real Estate', value: 50000 },
  { name: 'Cash', value: 5000 },
];

const portfolioPerformance = [
  { month: 'Jan', income: 800000, expense: 0 },
  { month: 'Feb', income: 820000, expense: 0 },
  { month: 'Mar', income: 850000, expense: 0 },
  { month: 'Apr', income: 880000, expense: 0 },
  { month: 'May', income: 900000, expense: 0 },
  { month: 'Jun', income: 925000, expense: 0 },
];

const holdings = [
  { name: 'HDFC Bank', type: 'Stock', quantity: 50, buyPrice: 1500, currentPrice: 1650, value: 82500, returns: 10 },
  { name: 'Reliance Industries', type: 'Stock', quantity: 100, buyPrice: 2400, currentPrice: 2550, value: 255000, returns: 6.25 },
  { name: 'ICICI Prudential Bluechip', type: 'Mutual Fund', quantity: 1000, buyPrice: 75, currentPrice: 82, value: 82000, returns: 9.33 },
  { name: 'SBI Magnum Gilt Fund', type: 'Bond', quantity: 500, buyPrice: 300, currentPrice: 310, value: 155000, returns: 3.33 },
  { name: 'Gold ETF', type: 'Gold', quantity: 20, buyPrice: 4800, currentPrice: 5000, value: 100000, returns: 4.17 },
];

export const InvestmentsPage = () => {
  return (
    <PageContainer
      title="Investment Portfolio"
      subtitle="Track and analyze your investment performance"
      icon={PieChart}
    >
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Total Investment"
          value={`₹${(totalInvestment / 100000).toFixed(1)}L`}
          trend="neutral"
          icon={DollarSign}
          color="#3B82F6"
        />
        <StatCard
          title="Current Value"
          value={`₹${(currentValue / 100000).toFixed(1)}L`}
          trend="up"
          trendValue="+8.8%"
          icon={TrendingUp}
          color="#10B981"
        />
        <StatCard
          title="Total Returns"
          value={`₹${returns.toLocaleString()}`}
          trend="up"
          trendValue={`+${returnPercentage}%`}
          icon={Percent}
          color="#8B5CF6"
        />
        <StatCard
          title="Risk Level"
          value="Moderate"
          trend="neutral"
          icon={AlertTriangle}
          color="#F59E0B"
        />
      </div>

      {/* Asset Allocation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <ChartCard
          title="Asset Allocation"
          subtitle="Portfolio distribution by asset class"
        >
          <InvestmentTreemap data={assetAllocation} height={350} />
        </ChartCard>

        <ChartCard
          title="Portfolio Performance"
          subtitle="Last 6 months value growth"
        >
          <TrendLineChart 
            data={portfolioPerformance} 
            height={350}
          />
        </ChartCard>
      </div>

      {/* Holdings Table */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden mb-6">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Holdings</h3>
          <p className="text-sm text-gray-500 mt-1">Detailed breakdown of your investments</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Quantity
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Buy Price
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Current Price
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Value
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Returns
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {holdings.map((holding, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{holding.name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                      {holding.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                    {holding.quantity}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                    ₹{holding.buyPrice.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                    ₹{holding.currentPrice.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium text-gray-900">
                    ₹{holding.value.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    <span className={`font-medium ${holding.returns >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {holding.returns >= 0 ? '+' : ''}{holding.returns.toFixed(2)}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Investment Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-5">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center">
              <PieChart className="w-4 h-4" />
            </div>
            <h4 className="font-semibold text-blue-900">Diversification</h4>
          </div>
          <p className="text-sm text-blue-700 mb-2">
            Your portfolio is well-diversified across 6 asset classes, reducing overall risk exposure.
          </p>
          <p className="text-xs text-blue-600">Risk Score: Moderate</p>
        </div>

        <div className="bg-green-50 border border-green-200 rounded-lg p-5">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center">
              <TrendingUp className="w-4 h-4" />
            </div>
            <h4 className="font-semibold text-green-900">Performance</h4>
          </div>
          <p className="text-sm text-green-700 mb-2">
            Your portfolio has generated 8.82% returns, outperforming the market average of 7.5%.
          </p>
          <p className="text-xs text-green-600">Above Market Average</p>
        </div>

        <div className="bg-orange-50 border border-orange-200 rounded-lg p-5">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-full bg-orange-600 text-white flex items-center justify-center">
              <AlertTriangle className="w-4 h-4" />
            </div>
            <h4 className="font-semibold text-orange-900">Recommendation</h4>
          </div>
          <p className="text-sm text-orange-700 mb-2">
            Consider increasing bond allocation to 25% for better risk-adjusted returns as you approach retirement.
          </p>
          <p className="text-xs text-orange-600">Rebalancing Suggested</p>
        </div>
      </div>
    </PageContainer>
  );
};
