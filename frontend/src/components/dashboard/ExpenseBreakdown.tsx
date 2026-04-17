import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { motion } from "framer-motion";

export default function ExpenseBreakdown() {
  const { currentUser } = useStore();
  if (!currentUser) return null;

  // Generate mock expenses if not available
  const expenses = currentUser.expenses || [
    { category: "Housing", amount: currentUser.monthlyExpense * 0.35, color: "hsl(217,91%,60%)", trend: "up" },
    { category: "Food", amount: currentUser.monthlyExpense * 0.20, color: "hsl(152,69%,45%)", trend: "stable" },
    { category: "Transport", amount: currentUser.monthlyExpense * 0.15, color: "hsl(45,93%,47%)", trend: "down" },
    { category: "Utilities", amount: currentUser.monthlyExpense * 0.10, color: "hsl(280,65%,50%)", trend: "stable" },
    { category: "Other", amount: currentUser.monthlyExpense * 0.20, color: "hsl(0,84%,60%)", trend: "up" },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6"
    >
      <h3 className="text-sm font-semibold text-foreground mb-1">Spending Breakdown</h3>
      <p className="text-xs text-muted-foreground mb-4">Monthly expense categories</p>
      <div className="flex items-center gap-6">
        <div className="w-40 h-40">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={expenses}
                dataKey="amount"
                nameKey="category"
                cx="50%" cy="50%"
                innerRadius={40} outerRadius={65}
                paddingAngle={3}
                strokeWidth={0}
              >
                {expenses.map((e, i) => (
                  <Cell key={i} fill={e.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 12, fontSize: 12 }}
                formatter={(value: number) => [formatCurrency(value)]}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="flex-1 space-y-2">
          {expenses.map((e, i) => (
            <div key={i} className="flex items-center gap-2 text-xs">
              <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: e.color }} />
              <span className="text-muted-foreground flex-1">{e.category}</span>
              <span className="font-medium text-foreground">{formatCurrency(e.amount)}</span>
              <span className={`text-[10px] ${e.trend === "up" ? "text-danger" : e.trend === "down" ? "text-success" : "text-muted-foreground"}`}>
                {e.trend === "up" ? "↑" : e.trend === "down" ? "↓" : "→"}
              </span>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
