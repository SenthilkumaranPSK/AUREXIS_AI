import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { Loader2 } from "lucide-react";

const cssColor: Record<string, string> = {
  success: "hsl(var(--success))",
  primary: "hsl(var(--primary))",
  warning: "hsl(var(--warning))",
  danger:  "hsl(var(--danger))",
};

// Generate health data based on user's financial metrics
const generateHealthData = (currentUser: any) => {
  const score = currentUser?.financialHealthScore || 50;
  const savingsRate = currentUser?.savingsRate || 0;
  const emergencyFund = currentUser?.emergencyFundMonths || 0;
  const debtRatio = currentUser?.debtToIncomeRatio || 0;
  
  let color = "danger";
  let label = "Needs Improvement";
  
  if (score >= 80) {
    color = "success";
    label = "Excellent";
  } else if (score >= 70) {
    color = "primary";
    label = "Good";
  } else if (score >= 50) {
    color = "warning";
    label = "Fair";
  }
  
  return {
    overall: score,
    color,
    label,
    subScores: [
      {
        name: "Savings Rate",
        score: Math.min(100, savingsRate * 3), // Scale savings rate
        color: savingsRate > 20 ? "success" : savingsRate > 10 ? "warning" : "danger",
        detail: `${savingsRate}% of income`
      },
      {
        name: "Emergency Fund",
        score: Math.min(100, (emergencyFund / 6) * 100), // 6 months is 100%
        color: emergencyFund >= 6 ? "success" : emergencyFund >= 3 ? "warning" : "danger",
        detail: `${emergencyFund} months`
      },
      {
        name: "Debt Management",
        score: Math.max(0, 100 - (debtRatio * 200)), // Lower debt ratio = higher score
        color: debtRatio < 0.3 ? "success" : debtRatio < 0.5 ? "warning" : "danger",
        detail: `${(debtRatio * 100).toFixed(0)}% DTI ratio`
      },
      {
        name: "Investment Growth",
        score: 75, // Mock score
        color: "primary",
        detail: "Portfolio diversified"
      }
    ]
  };
};

export default function HealthScoreGauge() {
  const { currentUser } = useStore();
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser?.id) return;
    
    // Simulate API call with generated health data
    setLoading(true);
    setTimeout(() => {
      setHealth(generateHealthData(currentUser));
      setLoading(false);
    }, 400);
  }, [currentUser?.id]);

  if (loading) return (
    <div className="glass-card rounded-2xl p-6 flex items-center justify-center border border-border h-64">
      <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
    </div>
  );

  if (!health) return null;

  const score = health.overall;
  const color = cssColor[health.color] || cssColor.primary;
  const glow  = `${color.replace(")", " / 0.3)")}`;
  const r = 52;
  const circumference = 2 * Math.PI * r;
  const arcLength = circumference * 0.75;
  const offset = arcLength - (score / 100) * arcLength;

  return (
    <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
      className="glass-card rounded-2xl p-6 flex flex-col items-center border border-border"
    >
      <div className="text-[11px] font-semibold uppercase tracking-widest text-muted-foreground mb-5">
        Financial Health
      </div>

      <div className="relative w-40 h-40">
        <svg className="w-full h-full" viewBox="0 0 120 120">
          <circle cx="60" cy="60" r={r} fill="none" strokeWidth="7"
            stroke="hsl(var(--muted))" strokeLinecap="round"
            strokeDasharray={`${arcLength} ${circumference}`}
            strokeDashoffset={0} transform="rotate(135 60 60)"
          />
          <motion.circle cx="60" cy="60" r={r} fill="none" strokeWidth="7"
            stroke={color} strokeLinecap="round"
            strokeDasharray={`${arcLength} ${circumference}`}
            initial={{ strokeDashoffset: arcLength }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.8, ease: "easeOut", delay: 0.3 }}
            transform="rotate(135 60 60)"
            style={{ filter: `drop-shadow(0 0 6px ${glow})` }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.4 }}
            className="text-4xl font-bold tabular-nums" style={{ color }}
          >
            {score}
          </motion.span>
          <span className="text-[10px] text-muted-foreground font-medium">/ 100</span>
        </div>
      </div>

      <div className="mt-4 px-4 py-1.5 rounded-full text-xs font-semibold tracking-wide"
        style={{ background: `${color}18`, color, border: `1px solid ${color}30` }}
      >
        {health.label}
      </div>

      {/* Sub-scores from backend */}
      <div className="w-full mt-5 grid grid-cols-2 gap-2">
        {health.subScores?.map((s: any) => (
          <div key={s.name} className="bg-muted/50 rounded-xl p-2 border border-border">
            <div className="flex justify-between items-center mb-1">
              <span className="text-[9px] text-muted-foreground">{s.name}</span>
              <span className="text-[9px] font-bold" style={{ color: cssColor[s.color] }}>{s.score}</span>
            </div>
            <div className="h-1 bg-muted rounded-full overflow-hidden">
              <div className="h-full rounded-full" style={{ width: `${s.score}%`, background: cssColor[s.color] }} />
            </div>
            <div className="text-[9px] text-muted-foreground mt-1">{s.detail}</div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
