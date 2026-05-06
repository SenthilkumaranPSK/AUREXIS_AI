import { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Wallet, TrendingUp, TrendingDown, PiggyBank, CreditCard,
  Shield, Target, AlertTriangle, RefreshCw, ArrowRight,
  Heart, ShieldAlert, FlaskConical, Bell, Sparkles
} from "lucide-react";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { useMouseReactive } from "@/hooks/useMouseReactive";
import MetricCard from "@/components/dashboard/MetricCard";
import HealthScoreGauge from "@/components/dashboard/HealthScoreGauge";
import HealthRadarChart from "@/components/dashboard/HealthRadarChart";
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
import StocksPanel from "@/components/dashboard/StocksPanel";
import MutualFundsPanel from "@/components/dashboard/MutualFundsPanel";
import MLForecastChart from "@/components/dashboard/MLForecastChart";
import SavingsTrendChart from "@/components/dashboard/SavingsTrendChart";
import DebtPayoffTimeline from "@/components/dashboard/DebtPayoffTimeline";
import RiskIndicators from "@/components/dashboard/RiskIndicators";
import ReportsExport from "@/components/dashboard/ReportsExport";
import SettingsPanel from "@/components/dashboard/SettingsPanel";
import ProductTour from "@/components/dashboard/ProductTour";

// Quick summary card — shows a snapshot with a "View Details" link
function SummaryCard({
  icon: Icon, title, value, sub, color, path, navigate
}: {
  icon: any; title: string; value: string; sub: string;
  color: string; path: string; navigate: (p: string) => void;
}) {
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({
    sensitivity: 20,
    tiltIntensity: 2
  });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20, scale: 0.95 }} 
      animate={{ opacity: 1, y: 0, scale: 1 }}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      whileHover={{ y: -4 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: "spring", stiffness: 400, damping: 25 }}
      onClick={() => navigate(path)}
      className="glass-card rounded-2xl p-5 border border-border cursor-pointer group transition-all duration-200 hover:border-primary/30 hover:shadow-lg"
    >
      <div className="flex items-start justify-between mb-3">
        <motion.div 
          className={`p-2 rounded-xl ${color}`}
          whileHover={{ rotate: 5, scale: 1.1 }}
          transition={{ type: "spring", stiffness: 400 }}
        >
          <Icon className="w-4 h-4" />
        </motion.div>
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 0, x: 0 }}
          whileHover={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.2 }}
        >
          <ArrowRight className="w-3.5 h-3.5 text-muted-foreground" />
        </motion.div>
      </div>
      <motion.div 
        className="text-xl font-bold text-foreground tabular-nums mb-0.5"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
      >
        {value}
      </motion.div>
      <div className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">{title}</div>
      <div className="text-[10px] text-muted-foreground/60 mt-1">{sub}</div>
    </motion.div>
  );
}

import { UserProfile } from "@/types/finance";

function OverviewSection({ u }: { u: UserProfile }) {
  const navigate = useNavigate();
  if (!u) return null;

  const avgGoalPct = u.goals?.length
    ? Math.round(u.goals.reduce((s, g) => s + (g.current / g.target), 0) / u.goals.length * 100)
    : 0;

  return (
    <>
      {/* Key metrics - Summary only */}
      <motion.div 
        className="grid grid-cols-2 lg:grid-cols-4 gap-4"
        initial="hidden"
        animate="visible"
        variants={{
          hidden: { opacity: 0 },
          visible: {
            opacity: 1,
            transition: {
              staggerChildren: 0.1
            }
          }
        }}
      >
        <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
          <MetricCard title="Net Worth"      value={formatCurrency(u.netWorth)}      icon={Wallet}      variant="primary" trend={{ value: "4.2%", positive: true }} />
        </motion.div>
        <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
          <MetricCard title="Monthly Income" value={formatCurrency(u.monthlyIncome)} icon={TrendingUp}  variant="success" />
        </motion.div>
        <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
          <MetricCard title="Monthly Expense"value={formatCurrency(u.monthlyExpense)}icon={TrendingDown} variant="danger" />
        </motion.div>
        <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
          <MetricCard title="Savings Rate"   value={`${u.savingsRate}%`}             icon={PiggyBank}   variant={u.savingsRate > 30 ? "success" : "warning"} trend={{ value: "2.1%", positive: u.savingsRate > 30 }} />
        </motion.div>
      </motion.div>

      {/* Quick summary cards — click to navigate */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-foreground">Quick Summary</h2>
          <span className="text-[11px] text-muted-foreground">Click any card to explore</span>
        </div>
        <motion.div 
          className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-3"
          initial="hidden"
          animate="visible"
          variants={{
            hidden: { opacity: 0 },
            visible: {
              opacity: 1,
              transition: {
                staggerChildren: 0.08,
                delayChildren: 0.3
              }
            }
          }}
        >
          <motion.div variants={{ hidden: { opacity: 0, scale: 0.8 }, visible: { opacity: 1, scale: 1 } }}>
            <SummaryCard icon={Heart}       title="Health"      value={`${u.financialHealthScore}/100`}   sub="Financial health score"          color="bg-success/10 text-success"  path="/dashboard/health"     navigate={navigate} />
          </motion.div>
          <motion.div variants={{ hidden: { opacity: 0, scale: 0.8 }, visible: { opacity: 1, scale: 1 } }}>
            <SummaryCard icon={ShieldAlert} title="Risk"        value={u.riskLevel}                        sub={`DTI: ${(u.debtToIncomeRatio*100).toFixed(0)}%`} color="bg-warning/10 text-warning"  path="/dashboard/risk"       navigate={navigate} />
          </motion.div>
          <motion.div variants={{ hidden: { opacity: 0, scale: 0.8 }, visible: { opacity: 1, scale: 1 } }}>
            <SummaryCard icon={TrendingUp}  title="Investments" value={formatCurrency(u.investmentValue)} sub="Portfolio value"                 color="bg-primary/10 text-primary"  path="/dashboard/investments" navigate={navigate} />
          </motion.div>
          <motion.div variants={{ hidden: { opacity: 0, scale: 0.8 }, visible: { opacity: 1, scale: 1 } }}>
            <SummaryCard icon={Target}      title="Goals"       value={`${avgGoalPct}%`}                   sub={`${u.goals?.length || 0} active goals`} color="bg-success/10 text-success"  path="/dashboard/goals"      navigate={navigate} />
          </motion.div>
          <motion.div variants={{ hidden: { opacity: 0, scale: 0.8 }, visible: { opacity: 1, scale: 1 } }}>
            <SummaryCard icon={CreditCard}  title="Debt"        value={formatCurrency(u.totalDebt)}        sub="Total outstanding"               color="bg-danger/10 text-danger"    path="/dashboard/debt"       navigate={navigate} />
          </motion.div>
          <motion.div variants={{ hidden: { opacity: 0, scale: 0.8 }, visible: { opacity: 1, scale: 1 } }}>
            <SummaryCard icon={FlaskConical}title="Simulator"   value="What-if"                            sub="Run scenario analysis"           color="bg-primary/10 text-primary"  path="/dashboard/simulation" navigate={navigate} />
          </motion.div>
        </motion.div>
      </motion.div>

      {/* Recent alerts preview */}
      {u.alerts?.length > 0 && (
        <div className="glass-card rounded-2xl p-5 border border-border">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Bell className="w-4 h-4 text-warning" />
              <span className="text-sm font-semibold text-foreground">Recent Alerts</span>
            </div>
            <button onClick={() => navigate("/dashboard/alerts")}
              className="text-[11px] text-primary flex items-center gap-1 hover:underline">
              View all <ArrowRight className="w-3 h-3" />
            </button>
          </div>
          <div className="space-y-2">
            {u.alerts.slice(0, 2).map(a => (
              <div key={a.id} className={`flex items-start gap-2.5 p-2.5 rounded-xl border text-xs ${
                a.type === "warning" ? "bg-warning/5 border-warning/20" :
                a.type === "danger"  ? "bg-danger/5  border-danger/20"  :
                a.type === "success" ? "bg-success/5 border-success/20" :
                "bg-primary/5 border-primary/20"
              }`}>
                <span className={`w-1.5 h-1.5 rounded-full mt-1 shrink-0 ${
                  a.type === "warning" ? "bg-warning" : a.type === "danger" ? "bg-danger" :
                  a.type === "success" ? "bg-success" : "bg-primary"
                }`} />
                <div>
                  <div className="font-semibold text-foreground">{a.title}</div>
                  <div className="text-muted-foreground text-[10px]">{a.message}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}

function HealthSection({ u }: { u: UserProfile }) {
  if (!u) return null;
  return (
    <>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Health Score"   value={`${u.financialHealthScore}/100`} icon={Shield}    variant={u.financialHealthScore >= 70 ? "success" : u.financialHealthScore >= 50 ? "warning" : "danger"} />
        <MetricCard title="Savings Rate"   value={`${u.savingsRate}%`}             icon={PiggyBank} variant={u.savingsRate > 30 ? "success" : "warning"} />
        <MetricCard title="Emergency Fund" value={`${u.emergencyFundMonths} months`} icon={Shield}  variant={u.emergencyFundMonths >= 6 ? "success" : "warning"} />
        <MetricCard title="Credit Score"   value={`${u.creditScore}`}              icon={CreditCard} variant={u.creditScore >= 750 ? "success" : u.creditScore >= 650 ? "warning" : "danger"} />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <HealthScoreGauge />
        <HealthRadarChart />
      </div>
      <RecommendationFeed />
    </>
  );
}

function RiskSection({ u }: { u: UserProfile }) {
  console.log("RiskSection rendering with user:", u);
  
  if (!u) {
    console.error("RiskSection: No user data");
    return <div className="text-danger">No user data available</div>;
  }
  
  try {
    return (
      <>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard title="Risk Level"     value={u.riskLevel}                                        icon={AlertTriangle} variant={u.riskLevel === "Low" ? "success" : u.riskLevel === "Medium" ? "warning" : "danger"} />
          <MetricCard title="Debt-to-Income" value={`${(u.debtToIncomeRatio * 100).toFixed(1)}%`}       icon={CreditCard}    variant={u.debtToIncomeRatio < 0.3 ? "success" : "danger"} />
          <MetricCard title="Total Debt"     value={formatCurrency(u.totalDebt)}                        icon={CreditCard}    variant="danger" />
          <MetricCard title="Credit Score"   value={`${u.creditScore}`}                                 icon={Shield}        variant={u.creditScore >= 750 ? "success" : "warning"} />
        </div>
        <RiskIndicators />
        <RecommendationFeed />
      </>
    );
  } catch (error) {
    console.error("RiskSection error:", error);
    return <div className="text-danger">Error rendering risk section: {String(error)}</div>;
  }
}

function SavingsSection({ u }: { u: UserProfile }) {
  if (!u) return null;
  return (
    <>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Monthly Savings" value={formatCurrency(u.savings)}          icon={PiggyBank} variant="success" />
        <MetricCard title="Savings Rate"    value={`${u.savingsRate}%`}                icon={PiggyBank} variant={u.savingsRate > 30 ? "success" : "warning"} />
        <MetricCard title="Emergency Fund"  value={`${u.emergencyFundMonths} months`}  icon={Shield}    variant={u.emergencyFundMonths >= 6 ? "success" : "warning"} />
        <MetricCard title="Net Worth"       value={formatCurrency(u.netWorth)}         icon={Wallet}    variant="primary" />
      </div>
      <SavingsTrendChart />
      <GoalsPanel />
    </>
  );
}

function DebtSection({ u }: { u: UserProfile }) {
  if (!u) return null;
  return (
    <>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Total Debt"      value={formatCurrency(u.totalDebt)}                  icon={CreditCard} variant="danger" />
        <MetricCard title="Debt-to-Income"  value={`${(u.debtToIncomeRatio * 100).toFixed(1)}%`} icon={CreditCard} variant={u.debtToIncomeRatio < 0.3 ? "success" : "danger"} />
        <MetricCard title="Monthly Income"  value={formatCurrency(u.monthlyIncome)}              icon={TrendingUp} variant="success" />
        <MetricCard title="Credit Score"    value={`${u.creditScore}`}                           icon={Shield}     variant={u.creditScore >= 750 ? "success" : "warning"} />
      </div>
      <DebtPayoffTimeline />
      <RecommendationFeed />
    </>
  );
}

const sectionMap: Record<string, (u: any) => JSX.Element | null> = {
  "/dashboard/health":      (u) => <HealthSection u={u} />,
  "/dashboard/risk":        (u) => <RiskSection u={u} />,
  "/dashboard/savings":     (u) => <SavingsSection u={u} />,
  "/dashboard/debt":        (u) => <DebtSection u={u} />,
  "/dashboard/investments": ()  => <><InvestmentPanel /><StocksPanel /><MutualFundsPanel /><RecommendationFeed /></>,
  "/dashboard/goals":       ()  => <GoalsPanel />,
  "/dashboard/forecasting": ()  => <><ForecastChart /><MLForecastChart /></>,
  "/dashboard/simulation":  ()  => <ScenarioSimulation />,
  "/dashboard/alerts":      ()  => <RecommendationFeed />,
  "/dashboard/reports":     ()  => <><ReportsExport /><ExpenseBreakdown /></>,
  "/dashboard/settings":    ()  => <SettingsPanel />,
};

const sectionTitles: Record<string, string> = {
  "/dashboard":             "Overview",
  "/dashboard/health":      "Financial Health",
  "/dashboard/risk":        "Risk Analysis",
  "/dashboard/savings":     "Savings",
  "/dashboard/debt":        "Debt Management",
  "/dashboard/investments": "Investments",
  "/dashboard/goals":       "Goals",
  "/dashboard/forecasting": "Forecasting",
  "/dashboard/simulation":  "Scenario Simulation",
  "/dashboard/alerts":      "Alerts & Recommendations",
  "/dashboard/reports":     "Reports",
  "/dashboard/settings":    "Settings",
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

  const renderSection = () => {
    try {
      if (path === "/dashboard") return <OverviewSection u={u} />;
      const renderer = sectionMap[path];
      if (renderer) return renderer(u);
      return <OverviewSection u={u} />;
    } catch {
      return (
        <div className="glass-card rounded-2xl p-8 flex flex-col items-center gap-4 text-center border border-border">
          <AlertTriangle className="w-10 h-10 text-warning" />
          <p className="text-muted-foreground text-sm">Something went wrong rendering this section.</p>
          <button onClick={() => navigate("/dashboard")}
            className="px-4 py-2 rounded-xl gradient-primary text-white text-sm flex items-center gap-2">
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
            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} id="dashboard-header">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-2xl font-bold text-foreground">
                    {path === "/dashboard" ? `Welcome back, ${u.name.split(" ")[0]}` : title}
                  </h1>
                  <p className="text-sm text-muted-foreground">
                    {path === "/dashboard" ? "Your financial intelligence at a glance" : `Viewing: ${title}`}
                  </p>
                </div>
                {path === "/dashboard" && (
                  <button 
                    onClick={() => { localStorage.removeItem("hasSeenTour"); window.location.reload(); }}
                    className="px-4 py-2 rounded-xl bg-muted/40 hover:bg-muted text-muted-foreground text-xs font-bold flex items-center gap-2 transition-all border border-border/50"
                  >
                    <Sparkles className="w-3.5 h-3.5 text-primary" />
                    Take Tour
                  </button>
                )}
              </div>
            </motion.div>
            
            <div id={path === "/dashboard/forecasting" ? "ml-forecast-chart" : ""}>
              {renderSection()}
            </div>
          </main>
          {path === "/dashboard" && <IntelligencePanel />}
        </div>
      </div>
      <FloatingChat />
      <ProductTour />
    </div>
  );
}
