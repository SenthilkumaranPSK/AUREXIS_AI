/**
 * Services Index
 * Export all services
 */

export { api, handleApiError } from './api';
export { authService } from './authService';
export { financialService } from './financialService';
export { forecastService } from './forecastService';
export { chatService } from './chatService';
export { reportService } from './reportService';

export type { LoginCredentials, SignupData, AuthResponse, User } from './authService';
export type {
  FinancialHealthScore,
  Expense,
  Income,
  Goal,
  Alert,
  Recommendation,
} from './financialService';
export type {
  ForecastData,
  ForecastResponse,
  ScenarioInput,
  ScenarioResult,
} from './forecastService';
export type { ChatMessage, ChatSession, ChatResponse } from './chatService';
export type { ReportRequest, Report } from './reportService';
