import { useEffect, useState } from "react";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { getUserGoals } from "@/lib/api";
import { motion } from "framer-motion";
import { Target, Loader2 } from "lucide-react";

export default function GoalsPanel() {
  const { currentUser } = useStore();
  const [goals, setGoals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser?.id) return;
    setLoading(true);
    getUserGoals(currentUser.id)
      .then(res => setGoals(res.goals))
      .catch(() => setGoals([]))
      .finally(() => setLoading(false));
  }, [currentUser?.id]);

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <div className="flex items-center gap-2 mb-4">
        <Target className="w-4 h-4 text-primary" />
        <h3 className="text-sm font-semibold text-foreground">Financial Goals</h3>
      </div>

      {loading ? (
        <div className="h-24 flex items-center justify-center">
          <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />
        </div>
      ) : (
        <div className="space-y-4">
          {goals.map((goal) => {
            const barColor = goal.progress >= 80 ? "hsl(var(--success))"
              : goal.progress >= 50 ? "hsl(var(--primary))"
              : "hsl(var(--warning))";
            return (
              <div key={goal.id}>
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{goal.icon}</span>
                    <span className="text-xs font-medium text-foreground">{goal.name}</span>
                  </div>
                  <span className="text-xs font-bold text-foreground tabular-nums">{goal.progress}%</span>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden mb-1.5">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${goal.progress}%` }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className="h-full rounded-full"
                    style={{ background: barColor }}
                  />
                </div>
                <div className="flex justify-between text-[10px] text-muted-foreground">
                  <span>{formatCurrency(goal.current)} / {formatCurrency(goal.target)}</span>
                  <span>₹{(goal.monthlySavingsNeeded / 1000).toFixed(0)}K/mo needed</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </motion.div>
  );
}
