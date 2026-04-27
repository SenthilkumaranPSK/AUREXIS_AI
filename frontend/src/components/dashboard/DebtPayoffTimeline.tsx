import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from "recharts";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { motion } from "framer-motion";
import { Calendar, Loader2 } from "lucide-react";

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card rounded-xl p-3 border border-border shadow-2xl text-xs min-w-[160px]">
      <div className="text-muted-foreground font-medium mb-2 uppercase tracking-wider text-[10px]">{label}</div>
      <div className="flex items-center justify-between gap-4 mb-1">
        <span className="text-muted-foreground">Principal</span>
        <span className="font-semibold text-foreground">{formatCurrency(payload[0]?.value || 0)}</span>
      </div>
      <div className="flex items-center justify-between gap-4">
        <span className="text-muted-foreground">Interest</span>
        <span className="font-semibold text-danger">{formatCurrency(payload[1]?.value || 0)}</span>
      </div>
    </div>
  );
};

export default function DebtPayoffTimeline() {
  const { currentUser } = useStore();
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [totalInterest, setTotalInterest] = useState(0);

  useEffect(() => {
    if (!currentUser) return;
    
    // Generate debt payoff timeline
    const totalDebt = currentUser.totalDebt;
    const monthlyPayment = currentUser.monthlyIncome * 0.15; // Assume 15% of income goes to debt
    const interestRate = 0.12 / 12; // 12% annual rate
    
    let remainingDebt = totalDebt;
    const timeline: any[] = [];
    let month = 0;
    let accumulatedInterest = 0;
    
    while (remainingDebt > 0 && month < 36) { // Max 3 years
      const interest = remainingDebt * interestRate;
      const principal = Math.min(monthlyPayment - interest, remainingDebt);
      
      if (principal <= 0) break; // Payment doesn't cover interest
      
      remainingDebt -= principal;
      accumulatedInterest += interest;
      
      timeline.push({
        month: `M${month + 1}`,
        principal: Math.round(principal),
        interest: Math.round(interest),
        remaining: Math.round(remainingDebt),
      });
      
      month++;
    }
    
    setData(timeline);
    setTotalInterest(Math.round(accumulatedInterest));
    setLoading(false);
  }, [currentUser]);

  if (loading) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-border h-96 flex items-center justify-center">
        <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (!data.length) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-border">
        <div className="flex items-center gap-2 mb-4">
          <div className="p-1.5 rounded-lg bg-success/10">
            <Calendar className="w-3.5 h-3.5 text-success" />
          </div>
          <h3 className="text-sm font-semibold text-foreground">Debt Payoff Timeline</h3>
        </div>
        <div className="text-center py-12 text-muted-foreground text-sm">
          No debt to track - you're debt free! 🎉
        </div>
      </div>
    );
  }

  const payoffMonths = data.length;
  const totalPaid = currentUser.totalDebt + totalInterest;

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-1.5 rounded-lg bg-danger/10">
              <Calendar className="w-3.5 h-3.5 text-danger" />
            </div>
            <h3 className="text-sm font-semibold text-foreground">Debt Payoff Timeline</h3>
          </div>
          <p className="text-[11px] text-muted-foreground ml-8">
            Projected payoff in {payoffMonths} months · {formatCurrency(totalInterest)} interest
          </p>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
          <XAxis 
            dataKey="month" 
            tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }} 
            axisLine={false} 
            tickLine={false} 
          />
          <YAxis 
            tick={{ fontSize: 9, fill: "hsl(var(--muted-foreground))" }} 
            axisLine={false} 
            tickLine={false}
            tickFormatter={(v) => `₹${(v/1000).toFixed(0)}k`} 
            width={48} 
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: "hsl(var(--muted))", opacity: 0.1 }} />
          <Bar dataKey="principal" stackId="a" fill="hsl(var(--primary))" radius={[0, 0, 4, 4]} />
          <Bar dataKey="interest" stackId="a" fill="hsl(var(--danger))" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>

      <div className="grid grid-cols-4 gap-3 mt-5 pt-5 border-t border-border">
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Total Debt</div>
          <div className="text-base font-bold text-danger">{formatCurrency(currentUser.totalDebt)}</div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Interest</div>
          <div className="text-base font-bold text-warning">{formatCurrency(totalInterest)}</div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Total Paid</div>
          <div className="text-base font-bold text-foreground">{formatCurrency(totalPaid)}</div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Payoff Time</div>
          <div className="text-base font-bold text-primary">{payoffMonths}m</div>
        </div>
      </div>

      <div className="mt-4 p-3 rounded-xl bg-primary/5 border border-primary/20">
        <div className="text-[10px] text-primary font-semibold mb-1">💡 Payoff Strategy</div>
        <div className="text-[11px] text-muted-foreground">
          Increase monthly payment by 20% to save {formatCurrency(totalInterest * 0.3)} in interest and payoff {Math.round(payoffMonths * 0.25)} months earlier.
        </div>
      </div>
    </motion.div>
  );
}
