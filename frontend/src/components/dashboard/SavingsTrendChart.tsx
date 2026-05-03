import { useMouseReactive } from "@/hooks/useMouseReactive";
import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Area, AreaChart } from "recharts";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { motion } from "framer-motion";
import { TrendingUp, Loader2 } from "lucide-react";

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card rounded-xl p-3 border border-border shadow-2xl text-xs min-w-[160px]">
      <div className="text-muted-foreground font-medium mb-2 uppercase tracking-wider text-[10px]">{label}</div>
      {payload.map((p: any) => (
        <div key={p.dataKey} className="flex items-center justify-between gap-4 mb-1">
          <div className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full" style={{ background: p.color }} />
            <span className="text-muted-foreground capitalize">{p.name}</span>
          </div>
          <span className="font-semibold text-foreground">{formatCurrency(p.value)}</span>
        </div>
      ))}
    </div>
  );
};

export default function SavingsTrendChart() {
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 25, tiltIntensity: 2 });
  const { currentUser } = useStore();
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser) return;
    
    // Generate savings trend data from user profile
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"];
    const baseIncome = currentUser.monthlyIncome;
    const baseExpense = currentUser.monthlyExpense;
    const baseSavings = currentUser.savings;
    
    const trendData = months.map((month, i) => {
      const variance = (Math.random() - 0.5) * 0.1; // ±10% variance
      const income = baseIncome * (1 + variance);
      const expense = baseExpense * (1 + variance * 0.8);
      const savings = income - expense;
      const cumulative = baseSavings + (savings * (i + 1));
      
      return {
        month,
        savings: Math.round(savings),
        cumulative: Math.round(cumulative),
        target: Math.round(baseIncome * 0.3), // 30% savings target
      };
    });
    
    setData(trendData);
    setLoading(false);
  }, [currentUser]);

  if (loading) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-border h-80 flex items-center justify-center">
        <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const currentSavings = data[data.length - 1]?.savings || 0;
  const targetSavings = data[data.length - 1]?.target || 0;
  const savingsGap = currentSavings - targetSavings;
  const isOnTrack = savingsGap >= 0;

  return (
    <motion.div
      ref={ref}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-1.5 rounded-lg bg-success/10">
              <TrendingUp className="w-3.5 h-3.5 text-success" />
            </div>
            <h3 className="text-sm font-semibold text-foreground">Savings Growth Trend</h3>
          </div>
          <p className="text-[11px] text-muted-foreground ml-8">Monthly savings vs target · 6 months</p>
        </div>
        <div className={`px-3 py-1.5 rounded-full text-xs font-semibold ${
          isOnTrack ? "bg-success/10 text-success" : "bg-warning/10 text-warning"
        }`}>
          {isOnTrack ? "On Track" : "Below Target"}
        </div>
      </div>

      <ResponsiveContainer width="100%" height={240}>
        <AreaChart data={data} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
          <defs>
            <linearGradient id="gSavings" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="hsl(158,64%,42%)" stopOpacity={0.3} />
              <stop offset="100%" stopColor="hsl(158,64%,42%)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
          <XAxis dataKey="month" tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fontSize: 9, fill: "hsl(var(--muted-foreground))" }} axisLine={false} tickLine={false}
            tickFormatter={(v) => `₹${(v/1000).toFixed(0)}k`} width={48} />
          <Tooltip content={<CustomTooltip />} cursor={{ stroke: "hsl(var(--border))", strokeWidth: 1 }} />
          <Area type="monotone" dataKey="savings" name="Actual Savings" stroke="hsl(158,64%,42%)" fill="url(#gSavings)" strokeWidth={2.5} dot={{ r: 3, fill: "hsl(158,64%,42%)" }} />
          <Line type="monotone" dataKey="target" name="Target" stroke="hsl(43,96%,56%)" strokeWidth={2} strokeDasharray="5 5" dot={false} />
        </AreaChart>
      </ResponsiveContainer>

      <div className="grid grid-cols-3 gap-3 mt-5 pt-5 border-t border-border">
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Current Month</div>
          <div className="text-lg font-bold text-success">{formatCurrency(currentSavings)}</div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Target</div>
          <div className="text-lg font-bold text-warning">{formatCurrency(targetSavings)}</div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Gap</div>
          <div className={`text-lg font-bold ${isOnTrack ? "text-success" : "text-danger"}`}>
            {isOnTrack ? "+" : ""}{formatCurrency(savingsGap)}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
