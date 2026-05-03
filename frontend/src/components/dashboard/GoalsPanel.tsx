import { useMouseReactive } from "@/hooks/useMouseReactive";
import { useEffect, useState } from "react";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { motion } from "framer-motion";
import { Target, Loader2 } from "lucide-react";

export default function GoalsPanel() {
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 25, tiltIntensity: 2 });
  const { currentUser } = useStore();
  const [loading, setLoading] = useState(false);

  // Use goals data from user profile
  const goals = currentUser?.goals || [];

  return (
    <motion.div
      ref={ref}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
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
      ) : goals.length > 0 ? (
        <div className="space-y-4">
          {goals.map((goal: any) => {
            const progress = Math.round((goal.current / goal.target) * 100);
            const barColor = progress >= 80 ? "hsl(var(--success))"
              : progress >= 50 ? "hsl(var(--primary))"
              : "hsl(var(--warning))";
            
            // Calculate monthly savings needed (assuming 12 months to deadline)
            const remaining = goal.target - goal.current;
            const monthlySavingsNeeded = remaining / 12;
            
            return (
              <div key={goal.id}>
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">🎯</span>
                    <span className="text-xs font-medium text-foreground">{goal.name}</span>
                  </div>
                  <span className="text-xs font-bold text-foreground tabular-nums">{progress}%</span>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden mb-1.5">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className="h-full rounded-full"
                    style={{ background: barColor }}
                  />
                </div>
                <div className="flex justify-between text-[10px] text-muted-foreground">
                  <span>{formatCurrency(goal.current)} / {formatCurrency(goal.target)}</span>
                  <span>₹{(monthlySavingsNeeded / 1000).toFixed(0)}K/mo needed</span>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="h-24 flex items-center justify-center text-muted-foreground text-sm">
          No financial goals set
        </div>
      )}
    </motion.div>
  );
}
