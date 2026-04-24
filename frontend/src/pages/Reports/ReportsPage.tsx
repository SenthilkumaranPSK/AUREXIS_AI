/**
 * Reports Page
 * Generate and download financial reports
 */

import { useState } from 'react';
import { PageContainer } from '@/components/layout/PageContainer';
import { StatCard } from '@/components/cards/StatCard';
import { FileText, Download, Calendar, Clock, CheckCircle, FileSpreadsheet } from 'lucide-react';

// Mock data
const reportTypes = [
  {
    id: 'financial-health',
    name: 'Financial Health Summary',
    description: 'Comprehensive overview of your financial well-being',
    icon: CheckCircle,
    color: '#10B981',
    lastGenerated: '2 days ago',
  },
  {
    id: 'expense-analysis',
    name: 'Expense Analysis Report',
    description: 'Detailed breakdown of spending patterns and categories',
    icon: FileSpreadsheet,
    color: '#F59E0B',
    lastGenerated: '1 week ago',
  },
  {
    id: 'savings-analysis',
    name: 'Savings Analysis Report',
    description: 'Savings trends, rates, and goal progress',
    icon: FileText,
    color: '#3B82F6',
    lastGenerated: '3 days ago',
  },
  {
    id: 'risk-assessment',
    name: 'Risk Assessment Report',
    description: 'Comprehensive risk analysis and mitigation strategies',
    icon: FileText,
    color: '#EF4444',
    lastGenerated: '5 days ago',
  },
  {
    id: 'goal-progress',
    name: 'Goal Progress Report',
    description: 'Track progress towards all financial goals',
    icon: FileText,
    color: '#8B5CF6',
    lastGenerated: '1 day ago',
  },
  {
    id: 'forecast-report',
    name: 'Forecast Report',
    description: 'ML-powered predictions for the next 6 months',
    icon: FileText,
    color: '#EC4899',
    lastGenerated: '4 days ago',
  },
];

const historicalReports = [
  {
    id: '1',
    name: 'Monthly Financial Report - June 2026',
    type: 'Monthly Summary',
    date: 'Jun 30, 2026',
    size: '2.4 MB',
    format: 'PDF',
  },
  {
    id: '2',
    name: 'Quarterly Report - Q2 2026',
    type: 'Quarterly Summary',
    date: 'Jun 30, 2026',
    size: '3.8 MB',
    format: 'PDF',
  },
  {
    id: '3',
    name: 'Expense Analysis - May 2026',
    type: 'Expense Analysis',
    date: 'May 31, 2026',
    size: '1.9 MB',
    format: 'PDF',
  },
  {
    id: '4',
    name: 'Tax Planning Report - FY 2025-26',
    type: 'Tax Report',
    date: 'Apr 15, 2026',
    size: '2.1 MB',
    format: 'PDF',
  },
  {
    id: '5',
    name: 'Investment Portfolio - Q1 2026',
    type: 'Investment Report',
    date: 'Mar 31, 2026',
    size: '2.7 MB',
    format: 'PDF',
  },
];

export const ReportsPage = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('current-month');
  const [selectedFormat, setSelectedFormat] = useState('pdf');

  return (
    <PageContainer
      title="Reports"
      subtitle="Generate and download comprehensive financial reports"
      icon={FileText}
    >
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Total Reports"
          value="24"
          trend="up"
          trendValue="+3"
          icon={FileText}
          color="#3B82F6"
        />
        <StatCard
          title="This Month"
          value="6"
          trend="neutral"
          icon={Calendar}
          color="#10B981"
        />
        <StatCard
          title="Last Generated"
          value="1 day ago"
          trend="neutral"
          icon={Clock}
          color="#F59E0B"
        />
        <StatCard
          title="Total Size"
          value="48.2 MB"
          trend="up"
          trendValue="+2.4 MB"
          icon={Download}
          color="#8B5CF6"
        />
      </div>

      {/* Report Generator */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Generate New Report
        </h3>

        {/* Period Selection */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Report Period
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { value: 'current-month', label: 'Current Month' },
              { value: 'last-month', label: 'Last Month' },
              { value: 'last-quarter', label: 'Last Quarter' },
              { value: 'custom', label: 'Custom Range' },
            ].map((period) => (
              <button
                key={period.value}
                onClick={() => setSelectedPeriod(period.value)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedPeriod === period.value
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {period.label}
              </button>
            ))}
          </div>
        </div>

        {/* Format Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Export Format
          </label>
          <div className="flex gap-3">
            {[
              { value: 'pdf', label: 'PDF' },
              { value: 'csv', label: 'CSV' },
              { value: 'excel', label: 'Excel' },
            ].map((format) => (
              <button
                key={format.value}
                onClick={() => setSelectedFormat(format.value)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedFormat === format.value
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {format.label}
              </button>
            ))}
          </div>
        </div>

        {/* Report Types */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Select Report Type
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {reportTypes.map((report) => {
              const Icon = report.icon;
              return (
                <button
                  key={report.id}
                  onClick={() => {}}
                  className="p-4 rounded-lg border-2 border-gray-200 hover:border-blue-600 hover:bg-blue-50 text-left transition-all group"
                >
                  <div className="flex items-start gap-3 mb-2">
                    <div
                      className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                      style={{ backgroundColor: `${report.color}20` }}
                    >
                      <Icon className="w-5 h-5" style={{ color: report.color }} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-semibold text-gray-900 mb-1">
                        {report.name}
                      </h4>
                      <p className="text-xs text-gray-600 mb-2">
                        {report.description}
                      </p>
                      <p className="text-xs text-gray-500">
                        Last: {report.lastGenerated}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center justify-end mt-3">
                    <span className="text-xs font-medium text-blue-600 group-hover:text-blue-700">
                      Generate →
                    </span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Historical Reports */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Historical Reports</h3>
          <p className="text-sm text-gray-500 mt-1">Previously generated reports</p>
        </div>
        <div className="divide-y divide-gray-200">
          {historicalReports.map((report) => (
            <div
              key={report.id}
              className="p-6 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-start gap-4 flex-1">
                  <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                    <FileText className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-semibold text-gray-900 mb-1">
                      {report.name}
                    </h4>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {report.date}
                      </span>
                      <span>{report.size}</span>
                      <span className="px-2 py-0.5 rounded bg-gray-100 text-gray-700 font-medium">
                        {report.format}
                      </span>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => {}}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  <Download className="w-4 h-4" />
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </PageContainer>
  );
};
