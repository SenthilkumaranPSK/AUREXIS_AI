/**
 * Goals Page
 * Financial goals tracking and management
 */

import { useState } from 'react';
import { PageContainer } from '@/components/layout/PageContainer';
import { ChartCard } from '@/components/cards/ChartCard';
import { StatCard } from '@/components/cards/StatCard';
import { GoalCard } from '@/components/cards/GoalCard';
import { SavingsAreaChart } from '@/components/charts/SavingsAreaChart';
import { GoalProgressBars } from '@/components/charts/GoalProgressBars';
import { Target, Plus, TrendingUp, Calendar, CheckCircle } from 'lucide-react';

// Mock data
const totalGoals = 5;
const activeGoals = 3;
const completedGoals = 2;
const totalTarget = 500000;
const totalSaved = 285000;

const goals = [
  {
    id: '1',
    name: 'Emergency Fund',
    targetAmount: 150000,
    currentAmount: 120000,
    deadline: 'Dec 2026',
    category: 'Savings',
    monthlyRequired: 5000,
  },
  {
    id: '2',
    name: 'New Car',
    targetAmount: 800000,
    currentAmount: 250000,
    deadline: 'Jun 2027',
    category: 'Purchase',
    monthlyRequired: 45833,
  },
  {
    id: '3',
    name: 'Vacation to Europe',
    targetAmount: 200000,
    currentAmount: 85000,
    deadline: 'Dec 2026',
    category: 'Travel',
    monthlyRequired: 19167,
  },
  {
    id: '4',
    name: 'Home Down Payment',
    targetAmount: 1000000,
    currentAmount: 350000,
    deadline: 'Dec 2027',
    category: 'Real Estate',
    monthlyRequired: 36111,
  },
  {
    id: '5',
    name: 'Retirement Fund',
    targetAmount: 5000000,
    currentAmount: 1200000,
    deadline: 'Dec 2045',
    category: 'Retirement',
    monthlyRequired: 16139,
  },
];

const savingsData = [
  { month: 'Jan', savings: 180000, target: 200000 },
  { month: 'Feb', savings: 200000, target: 220000 },
  { month: 'Mar', savings: 225000, target: 240000 },
  { month: 'Apr', savings: 245000, target: 260000 },
  { month: 'May', savings: 265000, target: 280000 },
  { month: 'Jun', savings: 285000, target: 300000 },
];

const progressData = goals.slice(0, 4).map(goal => ({
  id: goal.id,
  name: goal.name,
  current: goal.currentAmount,
  target: goal.targetAmount,
}));

export const GoalsPage = () => {
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  const filteredGoals = goals.filter(goal => {
    if (filter === 'active') return (goal.currentAmount / goal.targetAmount) < 1;
    if (filter === 'completed') return (goal.currentAmount / goal.targetAmount) >= 1;
    return true;
  });

  return (
    <PageContainer
      title="Financial Goals"
      subtitle="Track and manage your financial objectives"
      icon={Target}
      action={
        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
          <Plus className="w-4 h-4" />
          Add New Goal
        </button>
      }
    >
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Total Goals"
          value={totalGoals.toString()}
          trend="up"
          trendValue="+1"
          icon={Target}
          color="#3B82F6"
        />
        <StatCard
          title="Active Goals"
          value={activeGoals.toString()}
          trend="neutral"
          icon={TrendingUp}
          color="#10B981"
        />
        <StatCard
          title="Completed"
          value={completedGoals.toString()}
          trend="up"
          trendValue="+1"
          icon={CheckCircle}
          color="#8B5CF6"
        />
        <StatCard
          title="Overall Progress"
          value={`${((totalSaved / totalTarget) * 100).toFixed(1)}%`}
          trend="up"
          trendValue="+5%"
          icon={Calendar}
          color="#F59E0B"
        />
      </div>

      {/* Savings Growth */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <ChartCard
          title="Savings Growth"
          subtitle="Actual vs Target over time"
        >
          <SavingsAreaChart data={savingsData} height={300} showTarget={true} />
        </ChartCard>

        <ChartCard
          title="Goal Progress Overview"
          subtitle="Top 4 goals by priority"
        >
          <div className="py-4">
            <GoalProgressBars goals={progressData} showValues={true} />
          </div>
        </ChartCard>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'all'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          All Goals ({totalGoals})
        </button>
        <button
          onClick={() => setFilter('active')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'active'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Active ({activeGoals})
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'completed'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Completed ({completedGoals})
        </button>
      </div>

      {/* Goals Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredGoals.map((goal) => (
          <GoalCard
            key={goal.id}
            {...goal}
            onEdit={(id) => {}}
            onDelete={(id) => {}}
          />
        ))}
      </div>
    </PageContainer>
  );
};
