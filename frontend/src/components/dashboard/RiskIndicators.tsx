import { useMouseReactive } from "@/hooks/useMouseReactive";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { AlertTriangle, Shield, TrendingDown, CreditCard, AlertCircle } from "lucide-react";
import { formatCurrency } from "@/lib/formatters";

interface RiskIndicator {
  id: string;
  title: string;
  value: string;
  status: "low" | "medium" | "high" | "critical";
  description: string;
  icon: any;
  recommendation: string;
}

export default function RiskIndicators() {
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 25, tiltIntensity: 2 });
  const { currentUser } = useStore();
  const [indicators, setIndicators] = useState<RiskIndicator[]>([]);

  console.log("RiskIndicators rendering, currentUser:", currentUser);

  useEffect(() => {
    if (!currentUser) {
      console.warn("RiskIndicators: No current user");
      return;
    }

    try {
      const u = currentUser;
      const dti = u.debtToIncomeRatio * 100;
      const emergencyMonths = u.emergencyFundMonths;
      const savingsRate = u.savingsRate;
      const creditScore = u.creditScore;

      console.log("RiskIndicators data:", { dti, emergencyMonths, savingsRate, creditScore });

      const risks: RiskIndicator[] = [
      {
        id: "dti",
        title: "Debt-to-Income Ratio",
        value: `${dti.toFixed(1)}%`,
        status: dti < 30 ? "low" : dti < 40 ? "medium" : dti < 50 ? "high" : "critical",
        description: `Your debt payments are ${dti.toFixed(0)}% of your monthly income`,
        icon: CreditCard,
        recommendation: dti > 30 
          ? "Consider debt consolidation or increase income to reduce DTI below 30%"
          : "Excellent debt management - maintain current levels",
      },
      {
        id: "emergency",
        title: "Emergency Fund Coverage",
        value: `${emergencyMonths.toFixed(1)} months`,
        status: emergencyMonths >= 6 ? "low" : emergencyMonths >= 3 ? "medium" : emergencyMonths >= 1 ? "high" : "critical",
        description: `You have ${emergencyMonths.toFixed(1)} months of expenses saved`,
        icon: Shield,
        recommendation: emergencyMonths < 6
          ? `Build emergency fund to 6 months (${formatCurrency(u.monthlyExpense * 6)})`
          : "Strong emergency fund - you're well protected",
      },
      {
        id: "savings",
        title: "Savings Rate",
        value: `${savingsRate}%`,
        status: savingsRate >= 30 ? "low" : savingsRate >= 20 ? "medium" : savingsRate >= 10 ? "high" : "critical",
        description: `You're saving ${savingsRate}% of your income monthly`,
        icon: TrendingDown,
        recommendation: savingsRate < 30
          ? `Increase savings rate to 30% by reducing expenses by ${formatCurrency((30 - savingsRate) * u.monthlyIncome / 100)}`
          : "Excellent savings discipline - keep it up!",
      },
      {
        id: "credit",
        title: "Credit Score Risk",
        value: `${creditScore}`,
        status: creditScore >= 750 ? "low" : creditScore >= 650 ? "medium" : creditScore >= 550 ? "high" : "critical",
        description: `Your credit score is ${creditScore >= 750 ? "excellent" : creditScore >= 650 ? "good" : "needs improvement"}`,
        icon: AlertCircle,
        recommendation: creditScore < 750
          ? "Pay bills on time, reduce credit utilization, and avoid new credit inquiries"
          : "Excellent credit - maintain payment discipline",
      },
    ];

    console.log("RiskIndicators: Setting", risks.length, "indicators");
    setIndicators(risks);
  } catch (error) {
    console.error("RiskIndicators error:", error);
  }
  }, [currentUser]);

  const statusConfig = {
    low: {
      color: "success",
      bg: "bg-success/10",
      border: "border-success/20",
      text: "text-success",
      label: "Low Risk",
    },
    medium: {
      color: "warning",
      bg: "bg-warning/10",
      border: "border-warning/20",
      text: "text-warning",
      label: "Medium Risk",
    },
    high: {
      color: "danger",
      bg: "bg-danger/10",
      border: "border-danger/20",
      text: "text-danger",
      label: "High Risk",
    },
    critical: {
      color: "danger",
      bg: "bg-danger/20",
      border: "border-danger/30",
      text: "text-danger",
      label: "Critical Risk",
    },
  };

  return (
    <motion.div
      ref={ref}
      id="risk-audit-panel"
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <div className="flex items-center gap-2 mb-6">
        <div className="p-1.5 rounded-lg bg-warning/10">
          <AlertTriangle className="w-3.5 h-3.5 text-warning" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-foreground">Risk Indicators</h3>
          <p className="text-[11px] text-muted-foreground">Real-time financial risk assessment</p>
        </div>
      </div>

      <div className="space-y-4">
        {indicators.map((indicator, i) => {
          const config = statusConfig[indicator.status];
          const Icon = indicator.icon;

          return (
            <motion.div
              key={indicator.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`p-4 rounded-xl border ${config.bg} ${config.border}`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2.5">
                  <div className={`p-2 rounded-lg ${config.bg}`}>
                    <Icon className={`w-4 h-4 ${config.text}`} />
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-foreground">{indicator.title}</div>
                    <div className="text-[10px] text-muted-foreground">{indicator.description}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-lg font-bold ${config.text} tabular-nums`}>{indicator.value}</div>
                  <div className={`text-[9px] font-semibold uppercase tracking-wider ${config.text}`}>
                    {config.label}
                  </div>
                </div>
              </div>

              {/* Risk level bar */}
              <div className="mb-3">
                <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      indicator.status === "low" ? "bg-success" :
                      indicator.status === "medium" ? "bg-warning" :
                      "bg-danger"
                    }`}
                    style={{
                      width: indicator.status === "low" ? "25%" :
                             indicator.status === "medium" ? "50%" :
                             indicator.status === "high" ? "75%" : "100%"
                    }}
                  />
                </div>
              </div>

              {/* Recommendation */}
              <div className={`text-[11px] ${config.text} font-medium`}>
                💡 {indicator.recommendation}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Overall risk summary */}
      <div className="mt-6 pt-6 border-t border-border">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-[10px] text-muted-foreground uppercase tracking-wider mb-1">Overall Risk Level</div>
            <div className="text-lg font-bold text-foreground">
              {currentUser?.riskLevel || "Medium"}
            </div>
          </div>
          <div className={`px-4 py-2 rounded-full text-xs font-semibold ${
            currentUser?.riskLevel === "Low" ? "bg-success/10 text-success" :
            currentUser?.riskLevel === "Medium" ? "bg-warning/10 text-warning" :
            "bg-danger/10 text-danger"
          }`}>
            {indicators.filter(i => i.status === "high" || i.status === "critical").length} High Risk Areas
          </div>
        </div>
      </div>
    </motion.div>
  );
}
