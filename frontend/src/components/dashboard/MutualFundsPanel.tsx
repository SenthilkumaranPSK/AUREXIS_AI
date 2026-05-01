import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { TrendingUp, TrendingDown, Loader2, PieChart as PieIcon } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

const COLORS = ["#3B82F6","#10B981","#F59E0B","#8B5CF6","#EC4899","#EF4444"];

const riskColor: Record<string, string> = {
  "High":              "bg-danger/10 text-danger border-danger/20",
  "Moderate":          "bg-warning/10 text-warning border-warning/20",
  "Low-Moderate":      "bg-primary/10 text-primary border-primary/20",
  "Low To Moderate":   "bg-primary/10 text-primary border-primary/20",
  "Low":               "bg-success/10 text-success border-success/20",
};

// Mock data for mutual funds
const generateMockMutualFundData = (userId: string) => {
  return {
    schemesCount: 4,
    totalValue: 320000,
    totalInvested: 280000,
    totalPnL: 40000,
    totalPnLPct: 14.3,
    avgXIRR: 12.8,
    holdings: [
      { 
        isin: "INF090I01239", 
        schemeName: "SBI Bluechip Fund - Direct Growth", 
        folioId: "12345678", 
        sipMonths: 24, 
        riskLevel: "High",
        investedValue: 120000,
        currentValue: 140000,
        pnl: 20000,
        pnlPct: 16.7,
        xirr: 14.2
      },
      { 
        isin: "INF204K01424", 
        schemeName: "HDFC Mid-Cap Opportunities Fund - Direct Growth", 
        folioId: "87654321", 
        sipMonths: 18, 
        riskLevel: "High",
        investedValue: 90000,
        currentValue: 98000,
        pnl: 8000,
        pnlPct: 8.9,
        xirr: 9.5
      },
      { 
        isin: "INF846K01238", 
        schemeName: "ICICI Prudential Balanced Advantage Fund - Direct Growth", 
        folioId: "11223344", 
        sipMonths: 12, 
        riskLevel: "Moderate",
        investedValue: 50000,
        currentValue: 58000,
        pnl: 8000,
        pnlPct: 16.0,
        xirr: 15.2
      },
      { 
        isin: "INF109K01424", 
        schemeName: "Axis Long Term Equity Fund - Direct Growth", 
        folioId: "55667788", 
        sipMonths: 6, 
        riskLevel: "High",
        investedValue: 20000,
        currentValue: 24000,
        pnl: 4000,
        pnlPct: 20.0,
        xirr: 18.5
      }
    ],
    assetBreakdown: [
      { assetClass: "Large Cap", value: 140000, pct: 43.8 },
      { assetClass: "Mid Cap", value: 98000, pct: 30.6 },
      { assetClass: "Balanced", value: 58000, pct: 18.1 },
      { assetClass: "ELSS", value: 24000, pct: 7.5 }
    ]
  };
};

export default function MutualFundsPanel() {
  const { currentUser } = useStore();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser?.id) return;
    
    // Simulate API call with mock data
    setLoading(true);
    setTimeout(() => {
      setData(generateMockMutualFundData(currentUser.id));
      setLoading(false);
    }, 700);
  }, [currentUser?.id]);

  if (loading) return (
    <div className="glass-card rounded-2xl p-6 border border-border flex items-center justify-center h-48">
      <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
    </div>
  );

  if (!data || data.schemesCount === 0) return (
    <div className="glass-card rounded-2xl p-6 border border-border text-center text-muted-foreground text-sm">
      No mutual fund holdings found for this user.
    </div>
  );

  const pnlPositive = data.totalPnL >= 0;

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-success/10">
            <PieIcon className="w-4 h-4 text-success" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-foreground">Mutual Funds</h3>
            <p className="text-[11px] text-muted-foreground">{data.schemesCount} schemes · Avg XIRR {data.avgXIRR}%</p>
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
        {/* Scheme list */}
        <div className="lg:col-span-2 space-y-2">
          {data.holdings.map((h: any, i: number) => (
            <motion.div key={h.isin} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className="p-3 rounded-xl bg-secondary/30 hover:bg-secondary/50 transition-all"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1 mr-3">
                  <div className="text-xs font-semibold text-foreground leading-tight">{h.schemeName}</div>
                  <div className="text-[10px] text-muted-foreground mt-0.5">{h.folioId} · {h.sipMonths} SIPs</div>
                </div>
                <span className={`text-[9px] px-1.5 py-0.5 rounded border font-medium shrink-0 ${riskColor[h.riskLevel] || riskColor["Moderate"]}`}>
                  {h.riskLevel}
                </span>
              </div>
              <div className="grid grid-cols-4 gap-2 text-[10px]">
                <div>
                  <div className="text-muted-foreground">Invested</div>
                  <div className="font-semibold text-foreground tabular-nums">{formatCurrency(h.investedValue)}</div>
                </div>
                <div>
                  <div className="text-muted-foreground">Current</div>
                  <div className="font-semibold text-foreground tabular-nums">{formatCurrency(h.currentValue)}</div>
                </div>
                <div>
                  <div className="text-muted-foreground">P&L</div>
                  <div className={`font-semibold tabular-nums ${h.pnl >= 0 ? "text-success" : "text-danger"}`}>
                    {h.pnl >= 0 ? "+" : ""}{h.pnlPct}%
                  </div>
                </div>
                <div>
                  <div className="text-muted-foreground">XIRR</div>
                  <div className="font-semibold text-primary tabular-nums">{h.xirr}%</div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Asset class breakdown */}
        <div>
          <div className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider mb-3">Asset Class</div>
          <div className="w-full h-32 mb-3">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={data.assetBreakdown} dataKey="value" cx="50%" cy="50%" innerRadius={28} outerRadius={52} strokeWidth={0} paddingAngle={2}>
                  {data.assetBreakdown.map((_: any, i: number) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 8, fontSize: 11 }}
                  formatter={(v: number) => [formatCurrency(v)]} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-1.5">
            {data.assetBreakdown.map((a: any, i: number) => (
              <div key={a.assetClass} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full" style={{ background: COLORS[i % COLORS.length] }} />
                  <span className="text-muted-foreground">{a.assetClass}</span>
                </div>
                <span className="font-medium text-foreground">{a.pct}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-3 gap-3 mt-5 pt-4 border-t border-border">
        {[
          { label: "Invested",  value: formatCurrency(data.totalInvested) },
          { label: "Current",   value: formatCurrency(data.totalValue) },
          { label: "Avg XIRR",  value: `${data.avgXIRR}%`, color: "text-primary" },
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
