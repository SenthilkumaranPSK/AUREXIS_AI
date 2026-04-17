import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";

function getScoreLabel(score: number) {
  if (score >= 80) return { label: "Excellent", color: "hsl(var(--success))",  glow: "hsl(var(--success) / 0.3)" };
  if (score >= 60) return { label: "Good",      color: "hsl(var(--primary))",  glow: "hsl(var(--primary) / 0.3)" };
  if (score >= 40) return { label: "Fair",      color: "hsl(var(--warning))",  glow: "hsl(var(--warning) / 0.3)" };
  return               { label: "Poor",         color: "hsl(var(--danger))",   glow: "hsl(var(--danger) / 0.3)" };
}

export default function HealthScoreGauge() {
  const { currentUser } = useStore();
  if (!currentUser) return null;

  const score = currentUser.financialHealthScore;
  const r = 52;
  const circumference = 2 * Math.PI * r;
  const arcLength = circumference * 0.75;
  const offset = arcLength - (score / 100) * arcLength;
  const { label, color, glow } = getScoreLabel(score);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card rounded-2xl p-6 flex flex-col items-center border border-border"
    >
      <div className="text-[11px] font-semibold uppercase tracking-widest text-muted-foreground mb-5">
        Financial Health
      </div>

      <div className="relative w-40 h-40">
        <svg className="w-full h-full" viewBox="0 0 120 120">
          <circle
            cx="60" cy="60" r={r}
            fill="none" strokeWidth="7"
            stroke="hsl(var(--muted))"
            strokeLinecap="round"
            strokeDasharray={`${arcLength} ${circumference}`}
            strokeDashoffset={0}
            transform="rotate(135 60 60)"
          />
          <motion.circle
            cx="60" cy="60" r={r}
            fill="none" strokeWidth="7"
            stroke={color}
            strokeLinecap="round"
            strokeDasharray={`${arcLength} ${circumference}`}
            initial={{ strokeDashoffset: arcLength }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.8, ease: "easeOut", delay: 0.3 }}
            transform="rotate(135 60 60)"
            style={{ filter: `drop-shadow(0 0 6px ${glow})` }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.4 }}
            className="text-4xl font-bold tabular-nums"
            style={{ color }}
          >
            {score}
          </motion.span>
          <span className="text-[10px] text-muted-foreground font-medium">/ 100</span>
        </div>
      </div>

      <div
        className="mt-4 px-4 py-1.5 rounded-full text-xs font-semibold tracking-wide"
        style={{ background: `${color}18`, color, border: `1px solid ${color}30` }}
      >
        {label}
      </div>

      <div className="w-full mt-5 grid grid-cols-3 gap-2">
        {[
          { label: "Savings", value: `${currentUser.savingsRate}%` },
          { label: "Credit",  value: currentUser.creditScore },
          { label: "DTI",     value: `${(currentUser.debtToIncomeRatio * 100).toFixed(0)}%` },
        ].map((s) => (
          <div key={s.label} className="bg-muted/50 rounded-xl p-2 text-center border border-border">
            <div className="text-xs font-bold text-foreground">{s.value}</div>
            <div className="text-[9px] text-muted-foreground mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
