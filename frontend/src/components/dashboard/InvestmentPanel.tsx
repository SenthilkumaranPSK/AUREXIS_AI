import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { useStore } from "@/store/useStore";
import { formatCurrency, getRiskBg } from "@/lib/formatters";
import { motion } from "framer-motion";

export default function InvestmentPanel() {
  const { currentUser } = useStore();
  if (!currentUser) return null;

  // Generate mock investments if not available
  const investments = currentUser.investments || [
    { name: "Equity Mutual Fund", allocation: 40, returns: 12.5, risk: "High" },
    { name: "Debt Fund", allocation: 25, returns: 7.2, risk: "Low" },
    { name: "Gold ETF", allocation: 15, returns: 8.0, risk: "Medium" },
    { name: "Index Fund", allocation: 20, returns: 10.5, risk: "Medium" },
  ];
  const totalReturns = investments.reduce((sum, inv) => sum + inv.returns * inv.allocation / 100, 0);
  const colors = ["#3B82F6", "#8B5CF6", "#F59E0B", "#10B981", "#EC4899", "#EF4444", "#06B6D4"];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6"
    >
      <h3 className="text-sm font-semibold text-foreground mb-1">Investment Portfolio</h3>
      <p className="text-xs text-muted-foreground mb-4">
        Total: {formatCurrency(currentUser.investmentValue)} · Avg Returns: {totalReturns.toFixed(1)}%
      </p>
      <div className="flex items-start gap-6">
        <div className="w-32 h-32 shrink-0">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={investments} dataKey="allocation" cx="50%" cy="50%" innerRadius={30} outerRadius={55} strokeWidth={0} paddingAngle={2}>
                {investments.map((_, i) => <Cell key={i} fill={colors[i % colors.length]} />)}
              </Pie>
              <Tooltip contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 12, fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="flex-1 space-y-2">
          {investments.map((inv, i) => (
            <div key={i} className="flex items-center gap-2 text-xs">
              <span className="w-2 h-2 rounded-full shrink-0" style={{ background: colors[i % colors.length] }} />
              <span className="text-foreground flex-1 truncate">{inv.name}</span>
              <span className={`px-1.5 py-0.5 rounded text-[9px] font-medium border ${getRiskBg(inv.risk)}`}>{inv.risk}</span>
              <span className={`font-mono ${inv.returns >= 0 ? "text-success" : "text-danger"}`}>{inv.returns > 0 ? "+" : ""}{inv.returns}%</span>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
