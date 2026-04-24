/**
 * Alerts Page
 * All notifications and alerts center
 */

import { useState } from 'react';
import { PageContainer } from '@/components/layout/PageContainer';
import { StatCard } from '@/components/cards/StatCard';
import { AlertCard } from '@/components/cards/AlertCard';
import { Bell, AlertTriangle, AlertCircle, Info, CheckCircle } from 'lucide-react';

// Mock data
const alerts = [
  {
    id: '1',
    title: 'High Spending Alert',
    message: 'Your spending this month is 15% higher than average. Consider reviewing your expenses.',
    severity: 'critical' as const,
    timestamp: '2 hours ago',
    category: 'spending',
  },
  {
    id: '2',
    title: 'Goal Milestone Reached',
    message: 'Congratulations! You\'ve reached 80% of your Emergency Fund goal.',
    severity: 'success' as const,
    timestamp: '5 hours ago',
    category: 'goal',
  },
  {
    id: '3',
    title: 'Bill Payment Due',
    message: 'Your electricity bill of ₹3,000 is due in 3 days.',
    severity: 'warning' as const,
    timestamp: '1 day ago',
    category: 'bill',
  },
  {
    id: '4',
    title: 'Investment Opportunity',
    message: 'Based on your risk profile, consider investing in diversified mutual funds.',
    severity: 'info' as const,
    timestamp: '2 days ago',
    category: 'investment',
  },
  {
    id: '5',
    title: 'Credit Score Updated',
    message: 'Your credit score has increased by 15 points to 750.',
    severity: 'success' as const,
    timestamp: '3 days ago',
    category: 'credit',
  },
  {
    id: '6',
    title: 'Unusual Transaction Detected',
    message: 'A transaction of ₹15,000 was detected. If this wasn\'t you, please review immediately.',
    severity: 'critical' as const,
    timestamp: '4 days ago',
    category: 'security',
  },
  {
    id: '7',
    title: 'Savings Rate Decreased',
    message: 'Your savings rate has dropped to 28% this month from 32% last month.',
    severity: 'warning' as const,
    timestamp: '5 days ago',
    category: 'savings',
  },
  {
    id: '8',
    title: 'Monthly Report Ready',
    message: 'Your financial report for June 2026 is now available for download.',
    severity: 'info' as const,
    timestamp: '1 week ago',
    category: 'report',
  },
];

export const AlertsPage = () => {
  const [filter, setFilter] = useState<'all' | 'critical' | 'warning' | 'info' | 'success'>('all');

  const filteredAlerts = alerts.filter(alert => {
    if (filter === 'all') return true;
    return alert.severity === filter;
  });

  const criticalCount = alerts.filter(a => a.severity === 'critical').length;
  const warningCount = alerts.filter(a => a.severity === 'warning').length;
  const infoCount = alerts.filter(a => a.severity === 'info').length;
  const successCount = alerts.filter(a => a.severity === 'success').length;

  return (
    <PageContainer
      title="Alerts Center"
      subtitle="All your notifications and alerts in one place"
      icon={Bell}
    >
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Critical"
          value={criticalCount.toString()}
          trend="neutral"
          icon={AlertTriangle}
          color="#EF4444"
        />
        <StatCard
          title="Warnings"
          value={warningCount.toString()}
          trend="neutral"
          icon={AlertCircle}
          color="#F59E0B"
        />
        <StatCard
          title="Info"
          value={infoCount.toString()}
          trend="neutral"
          icon={Info}
          color="#3B82F6"
        />
        <StatCard
          title="Success"
          value={successCount.toString()}
          trend="neutral"
          icon={CheckCircle}
          color="#10B981"
        />
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-4 mb-6 overflow-x-auto">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${
            filter === 'all'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          All ({alerts.length})
        </button>
        <button
          onClick={() => setFilter('critical')}
          className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${
            filter === 'critical'
              ? 'bg-red-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Critical ({criticalCount})
        </button>
        <button
          onClick={() => setFilter('warning')}
          className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${
            filter === 'warning'
              ? 'bg-orange-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Warnings ({warningCount})
        </button>
        <button
          onClick={() => setFilter('info')}
          className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${
            filter === 'info'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Info ({infoCount})
        </button>
        <button
          onClick={() => setFilter('success')}
          className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${
            filter === 'success'
              ? 'bg-green-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Success ({successCount})
        </button>
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {filteredAlerts.length > 0 ? (
          filteredAlerts.map((alert) => (
            <AlertCard
              key={alert.id}
              title={alert.title}
              message={alert.message}
              severity={alert.severity}
              timestamp={alert.timestamp}
              onDismiss={() => {}}
              onAction={() => {}}
            />
          ))
        ) : (
          <div className="text-center py-12">
            <Bell className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No alerts</h3>
            <p className="text-gray-500">You don't have any {filter} alerts at the moment.</p>
          </div>
        )}
      </div>
    </PageContainer>
  );
};
