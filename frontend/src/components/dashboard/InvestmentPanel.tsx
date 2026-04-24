import { useEffect, useState } from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { useStore } from "@/store/useStore";
import { formatCurrency, getRiskBg } from "@/lib/formatters";
import { getUserInvestments } from "@/lib/api";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

export default function InvestmentPanel() {
  const { currentUser } = useStore();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser?.id) return;
    setLoading(true);
    getUserInvestments(currentUser.id)
      .then(res => setData(res))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [currentUser?.id]);

  const portfolio = data?.portfolio || [];

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <h3 className="text-sm font-semibold text-foreground mb-1">Investment Portfolio</h3>
      <p className="text-xs text-muted-foreground mb-4">
        {data ? `Total: ${formatCurrency(data.totalValue)} · Avg Returns: ${data.avgReturns}%` : "Loading..."}
      </p>

      {loading ? (
        <div className="h-32 flex items-center justify-center">
          <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />
        </div>
      ) : (
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
                  {inv.returns > 0 ? "+" : ""}{inv.returns}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}
