import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { motion } from "framer-motion";
import { Target } from "lucide-react";

export default function GoalsPanel() {
  const { currentUser } = useStore();
  if (!currentUser) return null;

  // Generate mock goals if not available
  const goals = currentUser.goals?.length ? currentUser.goals : [
    { id: "1", name: "Emergency Fund", icon: "🛡️", current: currentUser.emergencyFundMonths * currentUser.monthlyExpense, target: 6 * currentUser.monthlyExpense, monthlySavingsNeeded: 0 },
    { id: "2", name: "Car Purchase", icon: "🚗", current: currentUser.investmentValue * 0.3, target: 800000, monthlySavingsNeeded: 15000 },
    { id: "3", name: "Retirement", icon: "🏖️", current: currentUser.investmentValue, target: 5000000, monthlySavingsNeeded: 25000 },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Target className="w-4 h-4 text-primary" />
        <h3 className="text-sm font-semibold text-foreground">Financial Goals</h3>
      </div>
      <div className="space-y-4">
        {goals.map((goal) => {
          const progress = Math.round((goal.current / goal.target) * 100);
          return (
            <div key={goal.id}>
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-lg">{goal.icon}</span>
                  <span className="text-xs font-medium text-foreground">{goal.name}</span>
                </div>
                <span className="text-xs text-muted-foreground">{progress}%</span>
              </div>
              <div className="w-full h-2 bg-secondary rounded-full overflow-hidden mb-1.5">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${progress}%` }}
                  transition={{ duration: 1, ease: "easeOut" }}
                  className="h-full rounded-full gradient-primary"
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
    </motion.div>
  );
}
