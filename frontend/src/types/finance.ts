export type RiskLevel = "Low" | "Medium" | "High" | "Critical";
export type PersonalityTag = "Conservative Saver" | "High Spender" | "Debt Heavy" | "Investor" | "Goal Focused" | "Risky Profile" | "Balanced Planner" | "New Earner";

export interface UserProfile {
  id: string;
  name: string;
  avatar: string;
  occupation: string;
  age: number;
  monthlyIncome: number;
  monthlyExpense: number;
  netWorth: number;
  savings: number;
  totalDebt: number;
  riskLevel: RiskLevel;
  personalityTag: PersonalityTag;
  lastActive: string;
  creditScore: number;
  emergencyFundMonths: number;
  investmentValue: number;
  savingsRate: number;
  debtToIncomeRatio: number;
  financialHealthScore: number;
  goals: FinancialGoal[];
  monthlyData: MonthlyData[];
  expenses: ExpenseCategory[];
  investments: InvestmentAsset[];
  upcomingEMIs: EMIReminder[];
  alerts: Alert[];
}

export interface FinancialGoal {
  id: string;
  name: string;
  target: number;
  current: number;
  deadline: string;
  icon: string;
  monthlySavingsNeeded: number;
}

export interface MonthlyData {
  month: string;
  income: number;
  expense: number;
  savings: number;
  netWorth: number;
  debt: number;
}

export interface ExpenseCategory {
  category: string;
  amount: number;
  percentage: number;
  trend: "up" | "down" | "stable";
  color: string;
}

export interface InvestmentAsset {
  name: string;
  type: "Equity" | "Debt" | "Gold" | "Real Estate" | "Crypto" | "FD" | "PPF" | "MF" | "EPF" | "NPS";
  value: number;
  allocation: number;
  returns: number;
  risk: RiskLevel | "Safe";
}

export interface EMIReminder {
  name: string;
  amount: number;
  dueDate: string;
  type: string;
}

export interface Alert {
  id: string;
  type: "warning" | "danger" | "info" | "success";
  title: string;
  message: string;
  timestamp: string;
}

export interface SimulationParams {
  newLoanAmount: number;
  salaryIncrease: number;
  jobLoss: boolean;
  vacationExpense: number;
  housePurchase: boolean;
  carPurchase: boolean;
  investmentIncrease: number;
}

export interface SimulationResult {
  newEMI: number;
  newSavingsForecast: number;
  newRiskScore: number;
  newDebtRatio: number;
  financialImpact: string;
  recommendation: string;
}
