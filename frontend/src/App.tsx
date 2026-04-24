import { useEffect } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { useStore } from "@/store/useStore";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { ErrorBoundary } from "@/components/common/ErrorBoundary";
import LoginPage from "./pages/LoginPage";
import NotFound from "./pages/NotFound";
import AnimatedBackground from "./components/AnimatedBackground";

// Import all pages
import { DashboardPage } from "./pages/Dashboard/DashboardPage";
import { FinancialHealthPage } from "./pages/FinancialHealth/FinancialHealthPage";
import { ExpenseAnalysisPage } from "./pages/ExpenseAnalysis/ExpenseAnalysisPage";
import { GoalsPage } from "./pages/Goals/GoalsPage";
import { RiskAnalysisPage } from "./pages/RiskAnalysis/RiskAnalysisPage";
import { AlertsPage } from "./pages/Alerts/AlertsPage";
import { ForecastingPage } from "./pages/Forecasting/ForecastingPage";
import { ScenarioSimulationPage } from "./pages/ScenarioSimulation/ScenarioSimulationPage";
import { InvestmentsPage } from "./pages/Investments/InvestmentsPage";
import { ReportsPage } from "./pages/Reports/ReportsPage";
import { AIInsightsPage } from "./pages/AIInsights/AIInsightsPage";
import { ChatPage } from "./pages/Chat/ChatPage";
import { ProfilePage } from "./pages/Profile/ProfilePage";
import { SecurityPage } from "./pages/Security/SecurityPage";
import { SettingsPage } from "./pages/Settings/SettingsPage";

const queryClient = new QueryClient();

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const { isDark } = useStore();
  useEffect(() => {
    document.documentElement.classList.toggle("dark", isDark);
  }, [isDark]);
  return <>{children}</>;
}

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <ThemeProvider>
        <ErrorBoundary>
          <AnimatedBackground />
          <div className="relative z-10">
            <Toaster />
            <Sonner />
            <BrowserRouter>
              <Routes>
                {/* Auth Routes */}
                <Route path="/login" element={<LoginPage />} />
                
                {/* Dashboard Routes */}
                <Route element={<DashboardLayout />}>
                  <Route path="/" element={<DashboardPage />} />
                  <Route path="/financial-health" element={<FinancialHealthPage />} />
                  <Route path="/expense-analysis" element={<ExpenseAnalysisPage />} />
                  <Route path="/forecasting" element={<ForecastingPage />} />
                  <Route path="/goals" element={<GoalsPage />} />
                  <Route path="/risk-analysis" element={<RiskAnalysisPage />} />
                  <Route path="/scenario-simulation" element={<ScenarioSimulationPage />} />
                  <Route path="/investments" element={<InvestmentsPage />} />
                  <Route path="/reports" element={<ReportsPage />} />
                  <Route path="/alerts" element={<AlertsPage />} />
                  <Route path="/ai-insights" element={<AIInsightsPage />} />
                  <Route path="/chat" element={<ChatPage />} />
                  <Route path="/profile" element={<ProfilePage />} />
                  <Route path="/security" element={<SecurityPage />} />
                  <Route path="/settings" element={<SettingsPage />} />
                </Route>

                {/* Fallback */}
                <Route path="*" element={<NotFound />} />
              </Routes>
            </BrowserRouter>
          </div>
        </ErrorBoundary>
      </ThemeProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
