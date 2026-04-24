/**
 * Scenario Simulation Page
 * What-if analysis for financial decisions
 */

import { useState } from 'react';
import { PageContainer } from '@/components/layout/PageContainer';
import { ChartCard } from '@/components/cards/ChartCard';
import { StatCard } from '@/components/cards/StatCard';
import { ScenarioComparison } from '@/components/charts/ScenarioComparison';
import { GitCompare, TrendingUp, TrendingDown, AlertCircle, CheckCircle } from 'lucide-react';

// Mock data
const baselineData = {
  monthlyIncome: 75000,
  monthlyExpense: 55000,
  monthlySavings: 20000,
  healthScore: 85,
  savingsRate: 26.7,
  emergencyFund: 4,
};

const scenarios = [
  {
    id: 'salary-increase',
    name: 'Salary Increase (10%)',
    description: 'What if you get a 10% salary raise?',
    icon: TrendingUp,
    color: '#10B981',
    changes: {
      monthlyIncome: 82500,
      monthlyExpense: 55000,
      monthlySavings: 27500,
      healthScore: 88,
      savingsRate: 33.3,
      emergencyFund: 4.5,
    },
  },
  {
    id: 'new-emi',
    name: 'New Car EMI',
    description: 'What if you take a car loan with ₹15,000 EMI?',
    icon: TrendingDown,
    color: '#EF4444',
    changes: {
      monthlyIncome: 75000,
      monthlyExpense: 70000,
      monthlySavings: 5000,
      healthScore: 72,
      savingsRate: 6.7,
      emergencyFund: 3,
    },
  },
  {
    id: 'reduce-expenses',
    name: 'Reduce Expenses (20%)',
    description: 'What if you cut discretionary spending by 20%?',
    icon: CheckCircle,
    color: '#3B82F6',
    changes: {
      monthlyIncome: 75000,
      monthlyExpense: 44000,
      monthlySavings: 31000,
      healthScore: 92,
      savingsRate: 41.3,
      emergencyFund: 5,
    },
  },
  {
    id: 'emergency-expense',
    name: 'Emergency Expense',
    description: 'What if you face a ₹50,000 emergency?',
    icon: AlertCircle,
    color: '#F59E0B',
    changes: {
      monthlyIncome: 75000,
      monthlyExpense: 55000,
      monthlySavings: 20000,
      healthScore: 78,
      savingsRate: 26.7,
      emergencyFund: 3.2,
    },
  },
];

export const ScenarioSimulationPage = () => {
  const [selectedScenario, setSelectedScenario] = useState(scenarios[0]);

  const comparisonData = [
    {
      category: 'Income',
      current: baselineData.monthlyIncome,
      projected: selectedScenario.changes.monthlyIncome,
    },
    {
      category: 'Expenses',
      current: baselineData.monthlyExpense,
      projected: selectedScenario.changes.monthlyExpense,
    },
    {
      category: 'Savings',
      current: baselineData.monthlySavings,
      projected: selectedScenario.changes.monthlySavings,
    },
  ];

  const calculateImpact = () => {
    const incomeDiff = selectedScenario.changes.monthlyIncome - baselineData.monthlyIncome;
    const expenseDiff = selectedScenario.changes.monthlyExpense - baselineData.monthlyExpense;
    const savingsDiff = selectedScenario.changes.monthlySavings - baselineData.monthlySavings;
    const healthDiff = selectedScenario.changes.healthScore - baselineData.healthScore;

    return { incomeDiff, expenseDiff, savingsDiff, healthDiff };
  };

  const impact = calculateImpact();

  return (
    <PageContainer
      title="Scenario Simulation"
      subtitle="Explore what-if scenarios for better financial decisions"
      icon={GitCompare}
    >
      {/* Scenario Selection */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Select a Scenario
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {scenarios.map((scenario) => {
            const Icon = scenario.icon;
            const isSelected = selectedScenario.id === scenario.id;
            
            return (
              <button
                key={scenario.id}
                onClick={() => setSelectedScenario(scenario)}
                className={`p-4 rounded-lg border-2 text-left transition-all ${
                  isSelected
                    ? 'border-blue-600 bg-blue-50'
                    : 'border-gray-200 bg-white hover:border-gray-300'
                }`}
              >
                <div className="flex items-center gap-3 mb-2">
                  <div
                    className="w-10 h-10 rounded-lg flex items-center justify-center"
                    style={{ backgroundColor: `${scenario.color}20` }}
                  >
                    <Icon className="w-5 h-5" style={{ color: scenario.color }} />
                  </div>
                  <h4 className="font-semibold text-gray-900 text-sm">
                    {scenario.name}
                  </h4>
                </div>
                <p className="text-xs text-gray-600">{scenario.description}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Current vs Projected */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Income Impact"
          value={impact.incomeDiff >= 0 ? `+₹${impact.incomeDiff.toLocaleString()}` : `-₹${Math.abs(impact.incomeDiff).toLocaleString()}`}
          trend={impact.incomeDiff >= 0 ? 'up' : 'down'}
          trendValue={`${((impact.incomeDiff / baselineData.monthlyIncome) * 100).toFixed(1)}%`}
          icon={TrendingUp}
          color={impact.incomeDiff >= 0 ? '#10B981' : '#EF4444'}
        />
        <StatCard
          title="Expense Impact"
          value={impact.expenseDiff >= 0 ? `+₹${impact.expenseDiff.toLocaleString()}` : `-₹${Math.abs(impact.expenseDiff).toLocaleString()}`}
          trend={impact.expenseDiff <= 0 ? 'up' : 'down'}
          trendValue={`${((impact.expenseDiff / baselineData.monthlyExpense) * 100).toFixed(1)}%`}
          icon={TrendingDown}
          color={impact.expenseDiff <= 0 ? '#10B981' : '#EF4444'}
        />
        <StatCard
          title="Savings Impact"
          value={impact.savingsDiff >= 0 ? `+₹${impact.savingsDiff.toLocaleString()}` : `-₹${Math.abs(impact.savingsDiff).toLocaleString()}`}
          trend={impact.savingsDiff >= 0 ? 'up' : 'down'}
          trendValue={`${((impact.savingsDiff / baselineData.monthlySavings) * 100).toFixed(1)}%`}
          icon={CheckCircle}
          color={impact.savingsDiff >= 0 ? '#10B981' : '#EF4444'}
        />
        <StatCard
          title="Health Score Impact"
          value={impact.healthDiff >= 0 ? `+${impact.healthDiff}` : `${impact.healthDiff}`}
          trend={impact.healthDiff >= 0 ? 'up' : 'down'}
          trendValue={`${impact.healthDiff >= 0 ? '+' : ''}${impact.healthDiff} points`}
          icon={AlertCircle}
          color={impact.healthDiff >= 0 ? '#10B981' : '#EF4444'}
        />
      </div>

      {/* Comparison Chart */}
      <div className="mb-6">
        <ChartCard
          title="Current vs Projected Comparison"
          subtitle={selectedScenario.description}
        >
          <ScenarioComparison
            data={comparisonData}
            height={300}
            currentLabel="Current"
            projectedLabel="Projected"
          />
        </ChartCard>
      </div>

      {/* Detailed Impact Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Current Situation
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Monthly Income</span>
              <span className="text-sm font-semibold text-gray-900">
                ₹{baselineData.monthlyIncome.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Monthly Expenses</span>
              <span className="text-sm font-semibold text-gray-900">
                ₹{baselineData.monthlyExpense.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Monthly Savings</span>
              <span className="text-sm font-semibold text-gray-900">
                ₹{baselineData.monthlySavings.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between items-center pt-3 border-t">
              <span className="text-sm text-gray-600">Health Score</span>
              <span className="text-sm font-semibold text-gray-900">
                {baselineData.healthScore}/100
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Savings Rate</span>
              <span className="text-sm font-semibold text-gray-900">
                {baselineData.savingsRate}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Emergency Fund</span>
              <span className="text-sm font-semibold text-gray-900">
                {baselineData.emergencyFund} months
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Projected Situation
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Monthly Income</span>
              <span className="text-sm font-semibold text-gray-900">
                ₹{selectedScenario.changes.monthlyIncome.toLocaleString()}
                <span className={`ml-2 text-xs ${impact.incomeDiff >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  ({impact.incomeDiff >= 0 ? '+' : ''}{impact.incomeDiff.toLocaleString()})
                </span>
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Monthly Expenses</span>
              <span className="text-sm font-semibold text-gray-900">
                ₹{selectedScenario.changes.monthlyExpense.toLocaleString()}
                <span className={`ml-2 text-xs ${impact.expenseDiff <= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  ({impact.expenseDiff >= 0 ? '+' : ''}{impact.expenseDiff.toLocaleString()})
                </span>
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Monthly Savings</span>
              <span className="text-sm font-semibold text-gray-900">
                ₹{selectedScenario.changes.monthlySavings.toLocaleString()}
                <span className={`ml-2 text-xs ${impact.savingsDiff >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  ({impact.savingsDiff >= 0 ? '+' : ''}{impact.savingsDiff.toLocaleString()})
                </span>
              </span>
            </div>
            <div className="flex justify-between items-center pt-3 border-t">
              <span className="text-sm text-gray-600">Health Score</span>
              <span className="text-sm font-semibold text-gray-900">
                {selectedScenario.changes.healthScore}/100
                <span className={`ml-2 text-xs ${impact.healthDiff >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  ({impact.healthDiff >= 0 ? '+' : ''}{impact.healthDiff})
                </span>
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Savings Rate</span>
              <span className="text-sm font-semibold text-gray-900">
                {selectedScenario.changes.savingsRate}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Emergency Fund</span>
              <span className="text-sm font-semibold text-gray-900">
                {selectedScenario.changes.emergencyFund} months
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendation */}
      <div className={`rounded-lg border-l-4 p-5 ${
        impact.healthDiff >= 0
          ? 'bg-green-50 border-green-600'
          : 'bg-red-50 border-red-600'
      }`}>
        <h4 className={`font-semibold mb-2 ${
          impact.healthDiff >= 0 ? 'text-green-900' : 'text-red-900'
        }`}>
          {impact.healthDiff >= 0 ? 'Positive Impact' : 'Negative Impact'}
        </h4>
        <p className={`text-sm ${
          impact.healthDiff >= 0 ? 'text-green-700' : 'text-red-700'
        }`}>
          {impact.healthDiff >= 0
            ? `This scenario would improve your financial health by ${impact.healthDiff} points. Your savings would increase by ₹${impact.savingsDiff.toLocaleString()} per month, helping you achieve your goals faster.`
            : `This scenario would decrease your financial health by ${Math.abs(impact.healthDiff)} points. Your savings would decrease by ₹${Math.abs(impact.savingsDiff).toLocaleString()} per month, potentially delaying your financial goals.`
          }
        </p>
      </div>
    </PageContainer>
  );
};
