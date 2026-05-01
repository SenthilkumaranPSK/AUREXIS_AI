import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { getUserAlerts, getUserGoals, getUserHealth } from "@/lib/api";
import { ShieldCheck, Bell, Target, Calendar, Zap } from "lucide-react";

const riskColorMap: Record<string, string> = {
  Low:      "text-success  bg-success/10  border-success/20",
  Medium:   "text-warning  bg-warning/10  border-warning/20",
  High:     "text-danger   bg-danger/10   border-danger/20",
  Critical: "text-danger   bg-danger/15   border-danger/30",
};

const alertBgMap: Record<string, string> = {
  success: "border-success/20 bg-success/5",
  warning: "border-warning/20 bg-warning/5",
  danger:  "border-danger/20  bg-danger/5",
  info:    "border-primary/20 bg-primary/5",
};

const alertDotMap: Record<string, string> = {
  success: "bg-success",
  warning: "bg-warning",
  danger:  "bg-danger",
  info:    "bg-primary",
};

const cssColor: Record<string, string> = {
  success: "hsl(var(--success))",
  primary: "hsl(var(--primary))",
  warning: "hsl(var(--warning))",
  danger:  "hsl(var(--danger))",
};

export default function IntelligencePanel() {
  const { currentUser } = useStore();
  const [alerts, setAlerts]   = useState<any[]>([]);
  const [emis, setEmis]       = useState<any[]>([]);
  const [goals, setGoals]     = useState<any[]>([]);
  const [health, setHealth]   = useState<any>(null);

  useEffect(() => {
    if (!currentUser?.id) return;
    getUserAlerts(currentUser.id).then(r => { 
      // Handle both {alerts: [], emis: []} and [] formats
      if (Array.isArray(r)) {
        setAlerts(r);
        setEmis([]);
      } else if (r && typeof r === 'object') {
        setAlerts(r.alerts || []); 
        setEmis(r.emis || []); 
      }
    }).catch(() => {});
    
    getUserGoals(currentUser.id).then(r => {
      // Handle both {goals: []} and [] formats
      if (Array.isArray(r)) {
        setGoals(r);
      } else if (r && typeof r === 'object') {
        setGoals(r.goals || []);
      }
    }).catch(() => {});
    
    getUserHealth(currentUser.id).then(r => setHealth(r)).catch(() => {});
  }, [currentUser?.id]);

  if (!currentUser) return null;

  const scoreColor = health ? cssColor[health.color] || cssColor.primary : cssColor.primary;
  const healthScore = health?.overall ?? currentUser.financialHealthScore;

  return (
    <motion.aside initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
      className="w-[268px] shrink-0 h-[calc(100vh-64px)] sticky top-16 overflow-y-auto border-l border-border hidden xl:block"
    >
      <div className="p-4 space-y-3">

        {/* Profile */}
        <div className="glass-card rounded-2xl p-4 border border-border">
          <div className="flex items-center gap-3 mb-4">
            <div className="relative">
              <img src={currentUser.avatar} alt="" className="w-10 h-10 rounded-xl ring-1 ring-border" />
              <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-success rounded-full ring-1 ring-background" />
            </div>
            <div>
              <div className="text-xs font-semibold text-foreground">{currentUser.name}</div>
              <div className="text-[10px] text-muted-foreground">{currentUser.occupation}</div>
              {currentUser.location && <div className="text-[10px] text-muted-foreground/70">📍 {currentUser.location}</div>}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2">
            {[
              { label: "Net Worth", value: formatCurrency(currentUser.netWorth) },
              { label: "Credit",    value: String(currentUser.creditScore) },
              { label: "Income",    value: formatCurrency(currentUser.monthlyIncome) },
              { label: "Savings",   value: `${currentUser.savingsRate}%` },
            ].map(s => (
              <div key={s.label} className="bg-muted/50 rounded-xl p-2.5 border border-border">
                <div className="text-[9px] text-muted-foreground uppercase tracking-wider mb-1">{s.label}</div>
                <div className="text-xs font-bold text-foreground tabular-nums">{s.value}</div>
              </div>
            ))}
          </div>
          {currentUser.bankName && (
            <div className="mt-2 p-2.5 bg-muted/50 rounded-xl border border-border">
              <div className="text-[9px] text-muted-foreground uppercase tracking-wider mb-1">Bank Details</div>
              <div className="text-xs font-semibold text-foreground">{currentUser.bankName} · {currentUser.accountType}</div>
              <div className="text-[10px] text-muted-foreground">{currentUser.accountNumber} · {currentUser.bankLocation}</div>
              {currentUser.hasCreditCard && (
                <span className="inline-block mt-1 text-[9px] px-1.5 py-0.5 rounded bg-primary/10 text-primary font-medium">Credit Card</span>
              )}
            </div>
          )}
        </div>

        {/* Risk & Health */}
        <div className="glass-card rounded-2xl p-4 border border-border">
          <div className="flex items-center gap-2 mb-3">
            <ShieldCheck className="w-3.5 h-3.5 text-primary" />
            <span className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">Risk Profile</span>
          </div>
          <div className="flex items-center justify-between">
            <span className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold border ${riskColorMap[currentUser.riskLevel] || riskColorMap.Medium}`}>
              {currentUser.riskLevel} Risk
            </span>
            <div className="text-right">
              <div className="text-[10px] text-muted-foreground">Health Score</div>
              <div className="text-sm font-bold tabular-nums" style={{ color: scoreColor }}>
                {healthScore}<span className="text-[10px] text-muted-foreground">/100</span>
              </div>
            </div>
          </div>
          <div className="mt-3 h-1.5 bg-muted rounded-full overflow-hidden">
            <motion.div initial={{ width: 0 }} animate={{ width: `${healthScore}%` }}
              transition={{ duration: 1.2, ease: "easeOut", delay: 0.4 }}
              className="h-full rounded-full" style={{ background: scoreColor }}
            />
          </div>
        </div>

        {/* EMIs from backend */}
        {emis && emis.length > 0 && (
          <div className="glass-card rounded-2xl p-4 border border-border">
            <div className="flex items-center gap-2 mb-3">
              <Calendar className="w-3.5 h-3.5 text-warning" />
              <span className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">Upcoming EMIs</span>
            </div>
            <div className="space-y-2.5">
              {emis.map((emi, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div>
                    <div className="text-xs font-medium text-foreground">{emi.name}</div>
                    <div className="text-[10px] text-muted-foreground">{emi.dueDate}</div>
                  </div>
                  <span className="text-xs font-bold tabular-nums text-danger">{formatCurrency(emi.amount)}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Alerts from backend */}
        {alerts && alerts.length > 0 && (
          <div className="glass-card rounded-2xl p-4 border border-border">
            <div className="flex items-center gap-2 mb-3">
              <Bell className="w-3.5 h-3.5 text-danger" />
              <span className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">Alerts</span>
              <span className="ml-auto text-[9px] bg-danger/10 text-danger px-1.5 py-0.5 rounded-full font-semibold">{alerts.length}</span>
            </div>
            <div className="space-y-2">
              {alerts.slice(0, 4).map((alert) => (
                <div key={alert.id} className={`p-2.5 rounded-xl border text-xs ${alertBgMap[alert.type] || alertBgMap.info}`}>
                  <div className="flex items-center gap-1.5 mb-0.5">
                    <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${alertDotMap[alert.type] || alertDotMap.info}`} />
                    <span className="font-semibold text-foreground">{alert.title}</span>
                  </div>
                  <div className="text-[10px] text-muted-foreground ml-3">{alert.message}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Goals from backend */}
        {goals && goals.length > 0 && (

          <div className="glass-card rounded-2xl p-4 border border-border">
            <div className="flex items-center gap-2 mb-3">
              <Target className="w-3.5 h-3.5 text-success" />
              <span className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">Goals</span>
            </div>
            <div className="space-y-3">
              {goals.slice(0, 3).map((goal) => {
                const barColor = goal.progress >= 80 ? "hsl(var(--success))" : goal.progress >= 50 ? "hsl(var(--primary))" : "hsl(var(--warning))";
                return (
                  <div key={goal.id}>
                    <div className="flex justify-between items-center mb-1.5">
                      <span className="text-[11px] text-muted-foreground">{goal.icon} {goal.name}</span>
                      <span className="text-[11px] font-bold text-foreground tabular-nums">{goal.progress}%</span>
                    </div>
                    <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                      <motion.div initial={{ width: 0 }} animate={{ width: `${goal.progress}%` }}
                        transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
                        className="h-full rounded-full" style={{ background: barColor }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* AI Tip — generated from backend data */}
        <div className="rounded-2xl p-4 border border-warning/20 bg-warning/5">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-3.5 h-3.5 text-warning" />
            <span className="text-[11px] font-semibold text-warning uppercase tracking-wider">AI Tip</span>
          </div>
          <p className="text-[11px] text-muted-foreground leading-relaxed">
            Your savings rate of{" "}
            <span className="text-foreground font-semibold">{currentUser.savingsRate}%</span>{" "}
            {currentUser.savingsRate > 30
              ? "is excellent. Consider increasing SIP by 10% this year."
              : "is below target. Aim for 30% to build wealth faster."}
          </p>
        </div>

      </div>
    </motion.aside>
  );
}
