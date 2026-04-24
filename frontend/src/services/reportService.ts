/**
 * Report Service
 * Handle report generation and downloads
 */

import { api } from './api';

export interface ReportRequest {
  report_type: 'financial_health' | 'expense_analysis' | 'savings_analysis' | 'risk_assessment' | 'goal_progress' | 'forecast';
  period: 'current_month' | 'last_month' | 'last_quarter' | 'custom';
  format: 'pdf' | 'csv' | 'excel';
  start_date?: string;
  end_date?: string;
}

export interface Report {
  id: string;
  name: string;
  type: string;
  format: string;
  size: string;
  created_at: string;
  download_url: string;
}

export const reportService = {
  /**
   * Generate report
   */
  generateReport: async (request: ReportRequest): Promise<Report> => {
    return api.post<Report>('/api/reports/generate', request);
  },

  /**
   * Get report list
   */
  getReports: async (): Promise<Report[]> => {
    return api.get<Report[]>('/api/reports');
  },

  /**
   * Download report
   */
  downloadReport: async (reportId: string): Promise<Blob> => {
    const response = await api.get(`/api/reports/${reportId}/download`, {
      responseType: 'blob',
    });
    return response as unknown as Blob;
  },

  /**
   * Delete report
   */
  deleteReport: async (reportId: string): Promise<void> => {
    return api.delete(`/api/reports/${reportId}`);
  },

  /**
   * Get report preview
   */
  getReportPreview: async (reportId: string): Promise<any> => {
    return api.get(`/api/reports/${reportId}/preview`);
  },
};

export default reportService;
