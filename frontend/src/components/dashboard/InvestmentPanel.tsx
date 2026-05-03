import { useMouseReactive } from "@/hooks/useMouseReactive";
import { useEffect, useState } from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { useStore } from "@/store/useStore";
import { formatCurrency, getRiskBg } from "@/lib/formatters";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

const INVESTMENT_COLORS = ["#3B82F6", "#8B5CF6", "#F59E0B", "#10B981", "#EC4899", "#EF4444"];

export default function InvestmentPanel() {
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 25, tiltIntensity: 2 });
  const { currentUser } = useStore();
  const [loading, setLoading] = useState(false);

  // Use investment data from user profile
  const investments = currentUser?.investments || [];
  const totalValue = currentUser?.investmentValue || 0;
  
  // Transform investments data for the chart
  const portfolio = investments.map((inv: any, index: number) => ({
    ...inv,
    color: INVESTMENT_COLORS[index % INVESTMENT_COLORS.length],
    returns: inv.type === 'MF' ? 12.5 : inv.type === 'FD' ? 7.0 : inv.type === 'EPF' ? 8.15 : inv.type === 'Gold' ? 9.0 : 10.0,
    risk: inv.type === 'MF' ? 'High' : inv.type === 'FD' ? 'Low' : inv.type === 'EPF' ? 'Safe' : inv.type === 'Gold' ? 'Medium' : 'Medium'
  }));

  const avgReturns = portfolio.length > 0 
    ? portfolio.reduce((sum, p) => sum + (p.returns * p.allocation / 100), 0) 
    : 0;

  return (
    <motion.div
      ref={ref}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <h3 className="text-sm font-semibold text-foreground mb-1">Investment Portfolio</h3>
      <p className="text-xs text-muted-foreground mb-4">
        {portfolio.length > 0 ? `Total: ${formatCurrency(totalValue)} · Avg Returns: ${avgReturns.toFixed(1)}%` : "No investments found"}
      </p>

      {loading ? (
        <div className="h-32 flex items-center justify-center">
          <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />
        </div>
      ) : portfolio.length > 0 ? (
        <div className="flex items-start gap-6">
          <div className="w-32 h-32 shrink-0">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={portfolio} dataKey="allocation" cx="50%" cy="50%" innerRadius={30} outerRadius={55} strokeWidth={0} paddingAngle={2}>
                  {portfolio.map((p: any, i: number) => <Cell key={i} fill={p.color} />)}
                </Pie>
                <Tooltip contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 12, fontSize: 12 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex-1 space-y-2">
            {portfolio.map((inv: any, i: number) => (
              <div key={i} className="flex items-center gap-2 text-xs">
                <span className="w-2 h-2 rounded-full shrink-0" style={{ background: inv.color }} />
                <span className="text-foreground flex-1 truncate">{inv.name}</span>
                <span className={`px-1.5 py-0.5 rounded text-[9px] font-medium border ${getRiskBg(inv.risk)}`}>{inv.risk}</span>
                <span className={`font-mono ${inv.returns >= 0 ? "text-success" : "text-danger"}`}>
                  {inv.returns > 0 ? "+" : ""}{inv.returns.toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="h-32 flex items-center justify-center text-muted-foreground text-sm">
          No investment data available
        </div>
      )}
    </motion.div>
  );
}
