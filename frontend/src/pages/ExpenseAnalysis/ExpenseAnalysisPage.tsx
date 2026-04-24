/**
 * Expense Analysis Page
 * Deep dive into spending patterns and categories
 */

import { PageContainer } from '@/components/layout/PageContainer';
import { ChartCard } from '@/components/cards/ChartCard';
import { StatCard } from '@/components/cards/StatCard';
import { TransactionCard } from '@/components/cards/TransactionCard';
import { ExpenseDonut } from '@/components/charts/ExpenseDonut';
import { CategoryStackedBar } from '@/components/charts/CategoryStackedBar';
import { TopExpensesBar } from '@/components/charts/TopExpensesBar';
import { SpendingHeatmap } from '@/components/charts/SpendingHeatmap';
import { TrendingDown, ShoppingCart, Home, Car, Utensils } from 'lucide-react';

// Mock data
const totalExpenses = 55000;
const avgMonthly = 52000;
const highestCategory = 'Housing';
const lowestCategory = 'Entertainment';

const categoryData = [
  { name: 'Housing', value: 18000, percentage: 32.7 },
  { name: 'Food', value: 12000, percentage: 21.8 },
  { name: 'Transport', value: 8000, percentage: 14.5 },
  { name: 'Utilities', value: 5000, percentage: 9.1 },
  { name: 'Entertainment', value: 4000, percentage: 7.3 },
  { name: 'Healthcare', value: 3500, percentage: 6.4 },
  { name: 'Shopping', value: 2500, percentage: 4.5 },
  { name: 'Others', value: 2000, percentage: 3.6 },
];

const monthlyTrend = [
  { month: 'Jan', Housing: 18000, Food: 11000, Transport: 7500, Utilities: 5000, Entertainment: 3500, Others: 5000 },
  { month: 'Feb', Housing: 18000, Food: 10500, Transport: 7000, Utilities: 4800, Entertainment: 4000, Others: 4700 },
  { month: 'Mar', Housing: 18000, Food: 12000, Transport: 8500, Utilities: 5200, Entertainment: 4500, Others: 5800 },
  { month: 'Apr', Housing: 18000, Food: 11500, Transport: 7800, Utilities: 5000, Entertainment: 3800, Others: 4900 },
  { month: 'May', Housing: 18000, Food: 12500, Transport: 8200, Utilities: 5100, Entertainment: 4200, Others: 5000 },
  { month: 'Jun', Housing: 18000, Food: 12000, Transport: 8000, Utilities: 5000, Entertainment: 4000, Others: 5000 },
];

const topExpenses = [
  { name: 'Rent Payment', amount: 18000, category: 'Housing' },
  { name: 'Grocery Shopping', amount: 8000, category: 'Food' },
  { name: 'Fuel & Maintenance', amount: 5000, category: 'Transport' },
  { name: 'Dining Out', amount: 4000, category: 'Food' },
  { name: 'Electricity Bill', amount: 3000, category: 'Utilities' },
  { name: 'Internet & Mobile', amount: 2000, category: 'Utilities' },
  { name: 'Movie & Streaming', amount: 1500, category: 'Entertainment' },
  { name: 'Gym Membership', amount: 1200, category: 'Healthcare' },
];

const recentTransactions = [
  { id: '1', description: 'Rent Payment', amount: 18000, type: 'expense' as const, category: 'Housing', date: 'Jun 1, 2026', merchant: 'Property Manager' },
  { id: '2', description: 'Grocery Store', amount: 3500, type: 'expense' as const, category: 'Food', date: 'Jun 15, 2026', merchant: 'BigBasket' },
  { id: '3', description: 'Fuel Station', amount: 2000, type: 'expense' as const, category: 'Transport', date: 'Jun 18, 2026', merchant: 'Indian Oil' },
  { id: '4', description: 'Restaurant', amount: 1500, type: 'expense' as const, category: 'Food', date: 'Jun 20, 2026', merchant: 'Cafe Coffee Day' },
];

const heatmapData = Array.from({ length: 84 }, (_, i) => ({
  date: `Day ${i + 1}`,
  amount: Math.floor(Math.random() * 5000),
}));

export const ExpenseAnalysisPage = () => {
  return (
    <PageContainer
      title="Expense Analysis"
      subtitle="Detailed breakdown of your spending patterns"
      icon={TrendingDown}
    >
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Total Expenses"
          value={`₹${totalExpenses.toLocaleString()}`}
          trend="down"
          trendValue="-5%"
          icon={TrendingDown}
          color="#EF4444"
        />
        <StatCard
          title="Avg Monthly"
          value={`₹${avgMonthly.toLocaleString()}`}
          trend="down"
          trendValue="-2%"
          icon={ShoppingCart}
          color="#F59E0B"
        />
        <StatCard
          title="Highest Category"
          value={highestCategory}
          trend="neutral"
          icon={Home}
          color="#3B82F6"
        />
        <StatCard
          title="Lowest Category"
          value={lowestCategory}
          trend="neutral"
          icon={Utensils}
          color="#10B981"
        />
      </div>

      {/* Category Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <ChartCard title="Expense by Category" subtitle="Current month distribution">
          <ExpenseDonut data={categoryData} height={300} />
        </ChartCard>

        <ChartCard title="Top Expenses" subtitle="Largest transactions this month">
          <TopExpensesBar data={topExpenses} height={300} maxItems={8} />
        </ChartCard>
      </div>

      {/* Monthly Trend */}
      <div className="mb-6">
        <ChartCard
          title="Category Spending Trend"
          subtitle="Last 6 months breakdown"
        >
          <CategoryStackedBar
            data={monthlyTrend}
            categories={['Housing', 'Food', 'Transport', 'Utilities', 'Entertainment', 'Others']}
            height={350}
          />
        </ChartCard>
      </div>

      {/* Spending Heatmap */}
      <div className="mb-6">
        <ChartCard
          title="Daily Spending Pattern"
          subtitle="Last 12 weeks activity"
        >
          <SpendingHeatmap data={heatmapData} height={180} />
        </ChartCard>
      </div>

      {/* Recent Transactions */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Recent Transactions
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recentTransactions.map((transaction) => (
            <TransactionCard
              key={transaction.id}
              {...transaction}
              onClick={(id) => {}}
            />
          ))}
        </div>
      </div>
    </PageContainer>
  );
};
