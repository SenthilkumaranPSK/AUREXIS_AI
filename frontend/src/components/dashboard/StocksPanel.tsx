import { useMouseReactive } from "@/hooks/useMouseReactive";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { TrendingUp, TrendingDown, Loader2, BarChart2 } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

const COLORS = ["#3B82F6","#8B5CF6","#F59E0B","#10B981","#EC4899","#EF4444","#06B6D4"];

// Mock data for stocks
const generateMockStockData = (userId: string) => {
  return {
    holdingsCount: 5,
    totalValue: 450000,
    totalInvested: 380000,
    totalPnL: 70000,
    totalPnLPct: 18.4,
    holdings: [
      { symbol: "RELIANCE", companyName: "Reliance Industries Ltd", quantity: 50, currentValue: 150000, pnl: 25000, pnlPct: 20.0 },
      { symbol: "TCS", companyName: "Tata Consultancy Services", quantity: 30, currentValue: 120000, pnl: 18000, pnlPct: 17.6 },
      { symbol: "INFY", companyName: "Infosys Limited", quantity: 40, currentValue: 80000, pnl: 12000, pnlPct: 17.6 },
      { symbol: "HDFC", companyName: "HDFC Bank Limited", quantity: 25, currentValue: 60000, pnl: 8000, pnlPct: 15.4 },
      { symbol: "ICICI", companyName: "ICICI Bank Limited", quantity: 20, currentValue: 40000, pnl: 7000, pnlPct: 21.2 }
    ],
    sectorBreakdown: [
      { sector: "IT", value: 200000, pct: 44.4 },
      { sector: "Energy", value: 150000, pct: 33.3 },
      { sector: "Banking", value: 100000, pct: 22.2 }
    ]
  };
};

export default function StocksPanel() {
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 25, tiltIntensity: 2 });
  const { currentUser } = useStore();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser?.id) return;
    
    // Simulate API call with mock data
    setLoading(true);
    setTimeout(() => {
      setData(generateMockStockData(currentUser.id));
      setLoading(false);
    }, 500);
  }, [currentUser?.id]);

  if (loading) return (
    <div className="glass-card rounded-2xl p-6 border border-border flex items-center justify-center h-48">
      <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
    </div>
  );

  if (!data || data.holdingsCount === 0) return (
    <div className="glass-card rounded-2xl p-6 border border-border text-center text-muted-foreground text-sm">
      No stock holdings found for this user.
    </div>
  );

  const pnlPositive = data.totalPnL >= 0;

  return (
    <motion.div
      ref={ref}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-primary/10">
            <BarChart2 className="w-4 h-4 text-primary" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-foreground">Stock Portfolio</h3>
            <p className="text-[11px] text-muted-foreground">{data.holdingsCount} holdings · NSE/BSE</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-lg font-bold text-foreground tabular-nums">{formatCurrency(data.totalValue)}</div>
          <div className={`text-xs font-semibold flex items-center gap-1 justify-end ${pnlPositive ? "text-success" : "text-danger"}`}>
            {pnlPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
            {pnlPositive ? "+" : ""}{formatCurrency(data.totalPnL)} ({data.totalPnLPct}%)
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Holdings table */}
        <div className="lg:col-span-2 space-y-2">
          <div className="grid grid-cols-5 text-[10px] text-muted-foreground uppercase tracking-wider px-2 mb-1">
            <span className="col-span-2">Stock</span>
            <span className="text-right">Qty</span>
            <span className="text-right">Value</span>
            <span className="text-right">P&L</span>
          </div>
          {data.holdings.map((h: any, i: number) => (
            <motion.div key={h.symbol} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className="grid grid-cols-5 items-center p-2.5 rounded-xl bg-secondary/30 hover:bg-secondary/50 transition-all text-xs"
            >
              <div className="col-span-2">
                <div className="font-semibold text-foreground">{h.symbol}</div>
                <div className="text-[10px] text-muted-foreground truncate">{h.companyName}</div>
              </div>
              <div className="text-right text-muted-foreground">{h.quantity}</div>
              <div className="text-right font-medium text-foreground tabular-nums">{formatCurrency(h.currentValue)}</div>
              <div className={`text-right font-semibold tabular-nums ${h.pnl >= 0 ? "text-success" : "text-danger"}`}>
                {h.pnl >= 0 ? "+" : ""}{h.pnlPct}%
              </div>
            </motion.div>
          ))}
        </div>

        {/* Sector breakdown */}
        <div>
          <div className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider mb-3">Sector Allocation</div>
          <div className="w-full h-32 mb-3">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={data.sectorBreakdown} dataKey="value" cx="50%" cy="50%" innerRadius={28} outerRadius={52} strokeWidth={0} paddingAngle={2}>
                  {data.sectorBreakdown.map((_: any, i: number) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 8, fontSize: 11 }}
                  formatter={(v: number) => [formatCurrency(v)]} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-1.5">
            {data.sectorBreakdown.map((s: any, i: number) => (
              <div key={s.sector} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full" style={{ background: COLORS[i % COLORS.length] }} />
                  <span className="text-muted-foreground">{s.sector}</span>
                </div>
                <span className="font-medium text-foreground">{s.pct}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Summary row */}
      <div className="grid grid-cols-3 gap-3 mt-5 pt-4 border-t border-border">
        {[
          { label: "Invested",  value: formatCurrency(data.totalInvested) },
          { label: "Current",   value: formatCurrency(data.totalValue) },
          { label: "Total P&L", value: `${pnlPositive ? "+" : ""}${formatCurrency(data.totalPnL)}`, color: pnlPositive ? "text-success" : "text-danger" },
        ].map(s => (
          <div key={s.label} className="bg-muted/50 rounded-xl p-3 text-center border border-border">
            <div className="text-[10px] text-muted-foreground mb-1">{s.label}</div>
            <div className={`text-sm font-bold tabular-nums ${s.color || "text-foreground"}`}>{s.value}</div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
