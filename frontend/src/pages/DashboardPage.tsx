import { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Wallet, TrendingUp, TrendingDown, PiggyBank, CreditCard,
  Shield, Target, AlertTriangle, RefreshCw
} from "lucide-react";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import MetricCard from "@/components/dashboard/MetricCard";
import HealthScoreGauge from "@/components/dashboard/HealthScoreGauge";
import ForecastChart from "@/components/dashboard/ForecastChart";
import ExpenseBreakdown from "@/components/dashboard/ExpenseBreakdown";
import InvestmentPanel from "@/components/dashboard/InvestmentPanel";
import GoalsPanel from "@/components/dashboard/GoalsPanel";
import RecommendationFeed from "@/components/dashboard/RecommendationFeed";
import ScenarioSimulation from "@/components/dashboard/ScenarioSimulation";
import IntelligencePanel from "@/components/dashboard/IntelligencePanel";
import FloatingChat from "@/components/dashboard/FloatingChat";
import AppSidebar from "@/components/layout/AppSidebar";
import AppHeader from "@/components/layout/AppHeader";

function OverviewSection({ u }: { u: ReturnType<typeof useStore>["currentUser"] }) {
  if (!u) return null;
  return (
    <>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Net Worth" value={formatCurrency(u.netWorth)} icon={Wallet} variant="primary"
          trend={{ value: "4.2%", positive: true }} />
        <MetricCard title="Monthly Income" value={formatCurrency(u.monthlyIncome)} icon={TrendingUp} variant="success" />
        <MetricCard title="Monthly Expense" value={formatCurrency(u.monthlyExpense)} icon={TrendingDown} variant="danger" />
        <MetricCard title="Savings Rate" value={`${u.savingsRate}%`} icon={PiggyBank}
          variant={u.savingsRate > 30 ? "success" : "warning"}
          trend={{ value: "2.1%", positive: u.savingsRate > 30 }} />
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Total Debt" value={formatCurrency(u.totalDebt)} icon={CreditCard}
          variant={u.debtToIncomeRatio < 0.3 ? "success" : "danger"} subtitle={`DTI: ${(u.debtToIncomeRatio * 100).toFixed(1)}%`} />
        <MetricCard title="Investments" value={formatCurrency(u.investmentValue)} icon={TrendingUp} variant="primary"
          trend={{ value: "8.5%", positive: true }} />
        <MetricCard title="Emergency Fund" value={`${u.emergencyFundMonths} months`} icon={Shield}
          variant={u.emergencyFundMonths >= 6 ? "success" : u.emergencyFundMonths >= 3 ? "warning" : "danger"} />
        <MetricCard title="Goals Progress" value={`${(u.goals || []).length} active`} icon={Target} variant="primary"
          subtitle={`${u.goals?.length ? Math.round(u.goals.reduce((s, g) => s + (g.current / g.target), 0) / u.goals.length * 100) : 0}% avg completion`} />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <HealthScoreGauge />
        <div className="lg:col-span-2"><ForecastChart /></div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <ExpenseBreakdown />
        <InvestmentPanel />
      </div>
      <GoalsPanel />
      <ScenarioSimulation />
      <RecommendationFeed />
    </>
  );
}

function HealthSection({ u }: { u: ReturnType<typeof useStore>["currentUser"] }) {
  if (!u) return null;
  return (
    <>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Health Score" value={`${u.financialHealthScore}/100`} icon={Shield}
          variant={u.financialHealthScore >= 70 ? "success" : u.financialHealthScore >= 50 ? "warning" : "danger"} />
        <MetricCard title="Savings Rate" value={`${u.savingsRate}%`} icon={PiggyBank}
          variant={u.savingsRate > 30 ? "success" : "warning"} />
        <MetricCard title="Emergency Fund" value={`${u.emergencyFundMonths} months`} icon={Shield}
          variant={u.emergencyFundMonths >= 6 ? "success" : "warning"} />
        <MetricCard title="Credit Score" value={`${u.creditScore}`} icon={CreditCard}
          variant={u.creditScore >= 750 ? "success" : u.creditScore >= 650 ? "warning" : "danger"} />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <HealthScoreGauge />
        <div className="lg:col-span-2"><ForecastChart /></div>
      </div>
      <RecommendationFeed />
    </>
  );
}

function RiskSection({ u }: { u: ReturnType<typeof useStore>["currentUser"] }) {
  if (!u) return null;
  return (
    <>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Risk Level" value={u.riskLevel} icon={AlertTriangle}
          variant={u.riskLevel === "Low" ? "success" : u.riskLevel === "Medium" ? "warning" : "danger"} />
        <MetricCard title="Debt-to-Income" value={`${(u.debtToIncomeRatio * 100).toFixed(1)}%`} icon={CreditCard}
          variant={u.debtToIncomeRatio < 0.3 ? "success" : "danger"} />
        <MetricCard title="Total Debt" value={formatCurrency(u.totalDebt)} icon={CreditCard} variant="danger" />
        <MetricCard title="Credit Score" value={`${u.creditScore}`} icon={Shield}
          variant={u.creditScore >= 750 ? "success" : "warning"} />
      </div>
      <HealthScoreGauge />
      <RecommendationFeed />
    </>
  );
}

function SavingsSection({ u }: { u: ReturnType<typeof useStore>["currentUser"] }) {
  if (!u) return null;
  return (
    <>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Monthly Savings" value={formatCurrency(u.savings)} icon={PiggyBank} variant="success" />
        <MetricCard title="Savings Rate" value={`${u.savingsRate}%`} icon={PiggyBank}
          variant={u.savingsRate > 30 ? "success" : "warning"} />
        <MetricCard title="Emergency Fund" value={`${u.emergencyFundMonths} months`} icon={Shield}
          variant={u.emergencyFundMonths >= 6 ? "success" : "warning"} />
        <MetricCard title="Net Worth" value={formatCurrency(u.netWorth)} icon={Wallet} variant="primary" />
      </div>
      <ForecastChart />
      <GoalsPanel />
    </>
  );
}

function DebtSection({ u }: { u: ReturnType<typeof useStore>["currentUser"] }) {
  if (!u) return null;
  return (
    <>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Total Debt" value={formatCurrency(u.totalDebt)} icon={CreditCard} variant="danger" />
        <MetricCard title="Debt-to-Income" value={`${(u.debtToIncomeRatio * 100).toFixed(1)}%`} icon={CreditCard}
          variant={u.debtToIncomeRatio < 0.3 ? "success" : "danger"} />
        <MetricCard title="Monthly Income" value={formatCurrency(u.monthlyIncome)} icon={TrendingUp} variant="success" />
        <MetricCard title="Credit Score" value={`${u.creditScore}`} icon={Shield}
          variant={u.creditScore >= 750 ? "success" : "warning"} />
      </div>
      <ScenarioSimulation />
      <RecommendationFeed />
    </>
  );
}

const sectionMap: Record<string, (u: any) => JSX.Element | null> = {
  "/dashboard/health": (u) => <HealthSection u={u} />,
  "/dashboard/risk": (u) => <RiskSection u={u} />,
  "/dashboard/savings": (u) => <SavingsSection u={u} />,
  "/dashboard/debt": (u) => <DebtSection u={u} />,
  "/dashboard/investments": (u) => <><InvestmentPanel /><RecommendationFeed /></>,
  "/dashboard/goals": (u) => <GoalsPanel />,
  "/dashboard/forecasting": (u) => <ForecastChart />,
  "/dashboard/simulation": (u) => <ScenarioSimulation />,
  "/dashboard/alerts": (u) => <RecommendationFeed />,
  "/dashboard/reports": (u) => <><ForecastChart /><ExpenseBreakdown /></>,
  "/dashboard/settings": (u) => (
    <div className="glass-card rounded-2xl p-6 text-muted-foreground text-sm">
      Settings panel coming soon.
    </div>
  ),
};

const sectionTitles: Record<string, string> = {
  "/dashboard": "Financial Intelligence Overview",
  "/dashboard/health": "Financial Health",
  "/dashboard/risk": "Risk Analysis",
  "/dashboard/savings": "Savings",
  "/dashboard/debt": "Debt Management",
  "/dashboard/investments": "Investments",
  "/dashboard/goals": "Goals",
  "/dashboard/forecasting": "Forecasting",
  "/dashboard/simulation": "Scenario Simulation",
  "/dashboard/alerts": "Alerts & Recommendations",
  "/dashboard/reports": "Reports",
  "/dashboard/settings": "Settings",
};

export default function DashboardPage() {
  const { currentUser } = useStore();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (!currentUser) navigate("/");
  }, [currentUser, navigate]);

  if (!currentUser) return null;

  const u = currentUser;
  const path = location.pathname;
  const title = sectionTitles[path] || "Dashboard";
  const subtitle = path === "/dashboard" ? "Here's your financial intelligence overview" : `Viewing: ${title}`;

  const renderSection = () => {
    try {
      if (path === "/dashboard") return <OverviewSection u={u} />;
      const renderer = sectionMap[path];
      if (renderer) return renderer(u);
      return <OverviewSection u={u} />;
    } catch (e) {
      return (
        <div className="glass-card rounded-2xl p-8 flex flex-col items-center gap-4 text-center">
          <AlertTriangle className="w-10 h-10 text-warning" />
          <p className="text-muted-foreground text-sm">Something went wrong rendering this section.</p>
          <button onClick={() => navigate("/dashboard")}
            className="px-4 py-2 rounded-xl gradient-primary text-primary-foreground text-sm flex items-center gap-2">
            <RefreshCw className="w-4 h-4" /> Back to Overview
          </button>
        </div>
      );
    }
  };

  return (
    <div className="min-h-screen flex bg-transparent">
      <AppSidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <AppHeader />
        <div className="flex flex-1 min-h-0">
          <main className="flex-1 overflow-y-auto p-6 space-y-6">
            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
              <h1 className="text-2xl font-bold text-foreground">
                {path === "/dashboard" ? `Welcome back, ${u.name.split(" ")[0]}` : title}
              </h1>
              <p className="text-sm text-muted-foreground">{subtitle}</p>
            </motion.div>
            {renderSection()}
          </main>
          <IntelligencePanel />
        </div>
      </div>
      <FloatingChat />
    </div>
  );
}
