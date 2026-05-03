import { useEffect, useState } from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { getMonthlyForecast } from "@/lib/api";
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
            <span className="text-muted-foreground capitalize">{p.dataKey}</span>
          </div>
          <span className="font-semibold text-foreground">{formatCurrency(p.value)}</span>
        </div>
      ))}
    </div>
  );
};

const legends = [
  { key: "income",  label: "Income",  color: "hsl(221 83% 58%)" },
  { key: "expense", label: "Expense", color: "hsl(0 72% 55%)" },
  { key: "savings", label: "Savings", color: "hsl(158 64% 42%)" },
];

// Generate mock forecast data based on user's current financial situation
const generateForecastData = (currentUser: any) => {
  const baseIncome = currentUser?.monthlyIncome || 75000;
  const baseExpense = currentUser?.monthlyExpense || 45000;
  const baseSavings = baseIncome - baseExpense;
  
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  
  return months.map((month, index) => {
    // Add some growth and variation
    const incomeGrowth = 1 + (index * 0.02); // 2% monthly growth
    const expenseGrowth = 1 + (index * 0.015); // 1.5% monthly growth
    
    const income = Math.round(baseIncome * incomeGrowth);
    const expense = Math.round(baseExpense * expenseGrowth);
    const savings = income - expense;
    
    return {
      month,
      income,
      expense,
      savings
    };
  });
};

export default function ForecastChart() {
  const { currentUser } = useStore();
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser?.id) return;
    
    setLoading(true);
    getMonthlyForecast()
      .then((response) => {
        const forecast = Array.isArray(response?.forecast) ? response.forecast : [];
        setData(forecast.length ? forecast.slice(-6) : generateForecastData(currentUser));
      })
      .catch(() => setData(generateForecastData(currentUser)))
      .finally(() => setLoading(false));
  }, [currentUser?.id]);

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-1.5 rounded-lg bg-primary/10">
              <TrendingUp className="w-3.5 h-3.5 text-primary" />
            </div>
            <h3 className="text-sm font-semibold text-foreground">Financial Forecast</h3>
          </div>
          <p className="text-[11px] text-muted-foreground ml-8">6-month projection · current trends</p>
        </div>
        <div className="flex gap-4">
          {legends.map(l => (
            <div key={l.key} className="flex items-center gap-1.5 text-[10px] text-muted-foreground">
              <span className="w-2 h-2 rounded-full" style={{ background: l.color }} />
              {l.label}
            </div>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="h-60 flex items-center justify-center">
          <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={240}>
          <AreaChart data={data} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
            <defs>
              <linearGradient id="gIncome" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%"   stopColor="hsl(221,83%,58%)" stopOpacity={0.25} />
                <stop offset="100%" stopColor="hsl(221,83%,58%)" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="gSavings" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%"   stopColor="hsl(158,64%,42%)" stopOpacity={0.20} />
                <stop offset="100%" stopColor="hsl(158,64%,42%)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
            <XAxis dataKey="month" tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))", fontFamily: "Inter" }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 9, fill: "hsl(var(--muted-foreground))", fontFamily: "Inter" }} axisLine={false} tickLine={false} tickFormatter={(v) => `₹${(v/1000).toFixed(0)}k`} width={48} />
            <Tooltip content={<CustomTooltip />} cursor={{ stroke: "hsl(var(--border))", strokeWidth: 1 }} />
            <Area type="monotone" dataKey="income"  stroke="hsl(221,83%,58%)" fill="url(#gIncome)"  strokeWidth={2} dot={false} />
            <Area type="monotone" dataKey="expense" stroke="hsl(0,72%,55%)"   fill="transparent"    strokeWidth={1.5} strokeDasharray="5 3" dot={false} />
            <Area type="monotone" dataKey="savings" stroke="hsl(158,64%,42%)" fill="url(#gSavings)" strokeWidth={2} dot={false} />
          </AreaChart>
        </ResponsiveContainer>
      )}
    </motion.div>
  );
}
