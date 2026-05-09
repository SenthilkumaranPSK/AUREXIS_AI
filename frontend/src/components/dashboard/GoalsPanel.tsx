import { useMouseReactive } from "@/hooks/useMouseReactive";
import { useEffect, useState } from "react";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { motion } from "framer-motion";
import { Target, Loader2 } from "lucide-react";

export default function GoalsPanel() {
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 25, tiltIntensity: 2 });
  const { currentUser, currency } = useStore();
  const [loading, setLoading] = useState(false);

  // Use goals data from user profile
  const goals = currentUser?.goals || [];

  return (
    <motion.div
      ref={ref}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border h-full flex flex-col"
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-primary/10">
            <Target className="w-4 h-4 text-primary" />
          </div>
          <h3 className="text-sm font-semibold text-foreground">Financial Goals & Roadmap</h3>
        </div>
      </div>

      {loading ? (
        <div className="h-48 flex items-center justify-center">
          <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />
        </div>
      ) : goals.length > 0 ? (
        <div className="space-y-6">
          <div className="space-y-4">
            {goals.map((goal: any) => {
              const progress = Math.round((goal.current / goal.target) * 100);
              const barColor = progress >= 80 ? "hsl(var(--success))"
                : progress >= 50 ? "hsl(var(--primary))"
                : "hsl(var(--warning))";
              
              const remaining = goal.target - goal.current;
              const monthlySavingsNeeded = remaining / 12;
              
              return (
                <div key={goal.id} className="group">
                  <div className="flex items-center justify-between mb-1.5">
                    <div className="flex items-center gap-2">
                      <motion.span whileHover={{ scale: 1.2, rotate: 10 }}>🎯</motion.span>
                      <span className="text-xs font-semibold text-foreground">{goal.name}</span>
                    </div>
                    <span className="text-[10px] font-bold text-primary bg-primary/10 px-2 py-0.5 rounded-full">{progress}%</span>
                  </div>
                  <div className="w-full h-2 bg-muted rounded-full overflow-hidden mb-2 border border-border/50">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${progress}%` }}
                      transition={{ duration: 1.5, ease: "circOut" }}
                      className="h-full rounded-full shadow-[0_0_8px_rgba(var(--primary),0.3)]"
                      style={{ 
                        background: `linear-gradient(90deg, ${barColor}, #fff2)`,
                        boxShadow: `0 0 10px ${barColor}44`
                      }}
                    />
                  </div>
                  <div className="flex justify-between text-[10px] text-muted-foreground font-medium italic">
                    <span>{formatCurrency(goal.current, currency)} / {formatCurrency(goal.target, currency)}</span>
                    <span className="text-foreground">{formatCurrency(monthlySavingsNeeded, currency)}/mo needed</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* New Roadmap Visualization */}
          <div className="mt-8 pt-6 border-t border-border">
            <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-4">Achievement Timeline</div>
            <div className="relative h-12 flex items-center px-4">
              <div className="absolute left-0 right-0 h-0.5 bg-muted rounded-full" />
              {goals.map((goal: any, i: number) => {
                const pos = (i + 1) * (100 / (goals.length + 1));
                const progress = (goal.current / goal.target) * 100;
                const isAchieved = progress >= 100;
                
                return (
                  <motion.div 
                    key={goal.id}
                    className="absolute flex flex-col items-center group/dot"
                    style={{ left: `${pos}%` }}
                    whileHover={{ scale: 1.1 }}
                  >
                    <div className={`w-3 h-3 rounded-full border-2 border-background transition-all duration-500 ${isAchieved ? "bg-success scale-125" : "bg-primary"}`} />
                    <div className="absolute top-4 whitespace-nowrap opacity-0 group-hover/dot:opacity-100 transition-all duration-300">
                      <div className="glass-card px-2 py-1 rounded-md border border-border shadow-xl">
                        <span className="text-[9px] font-bold text-foreground">{goal.name}</span>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
              <div className="absolute right-0 w-2 h-2 rounded-full bg-success animate-pulse" />
            </div>
            <div className="flex justify-between mt-6 text-[9px] text-muted-foreground uppercase font-bold tracking-tighter">
              <span>Current</span>
              <span>2024 Milestones</span>
              <span>2025 Vision</span>
            </div>
          </div>
        </div>
      ) : (
        <div className="h-48 flex items-center justify-center text-muted-foreground text-sm flex-col gap-2">
          <Target className="w-8 h-8 opacity-10" />
          No financial goals set
        </div>
      )}
    </motion.div>
  );
}
