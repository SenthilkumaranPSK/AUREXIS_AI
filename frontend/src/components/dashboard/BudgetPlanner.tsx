import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { PiggyBank, Edit2, Check, X, AlertTriangle, TrendingUp, Loader2 } from "lucide-react";
import { toast } from "sonner";

interface BudgetItem {
  category: string;
  limit: number;
  spent: number;
  remaining: number;
  percentage: number;
  status: "good" | "warning" | "danger";
}

const STATUS_COLORS = {
  good:    { bar: "bg-success", text: "text-success", badge: "bg-success/10 text-success border-success/20" },
  warning: { bar: "bg-warning", text: "text-warning", badge: "bg-warning/10 text-warning border-warning/20" },
  danger:  { bar: "bg-danger",  text: "text-danger",  badge: "bg-danger/10 text-danger border-danger/20"   },
};

export default function BudgetPlanner() {
  const { currency } = useStore();
  const [budget, setBudget]     = useState<BudgetItem[]>([]);
  const [loading, setLoading]   = useState(true);
  const [saving, setSaving]     = useState(false);
  const [editId, setEditId]     = useState<string | null>(null);
  const [editVal, setEditVal]   = useState("");
  const [month, setMonth]       = useState("");

  const token = () => localStorage.getItem("access_token");

  const fetchBudget = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/user/budget", { headers: { Authorization: `Bearer ${token()}` } });
      const data = await res.json();
      if (data.success) { setBudget(data.budget); setMonth(data.month); }
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchBudget(); }, []);

  const startEdit = (cat: string, limit: number) => { setEditId(cat); setEditVal(String(limit)); };
  const cancelEdit = () => { setEditId(null); setEditVal(""); };

  const saveEdit = async (cat: string) => {
    const newLimit = parseFloat(editVal);
    if (isNaN(newLimit) || newLimit < 0) { toast.error("Enter a valid amount"); return; }
    setSaving(true);
    try {
      const updated = budget.map(b => ({ category: b.category, limit: b.category === cat ? newLimit : b.limit }));
      const res = await fetch("/api/user/budget", {
        method: "PUT",
        headers: { Authorization: `Bearer ${token()}`, "Content-Type": "application/json" },
        body: JSON.stringify({ budgets: updated }),
      });
      const data = await res.json();
      if (data.success) { toast.success(`${cat} budget updated`); fetchBudget(); }
    } catch (e) { toast.error("Failed to save"); }
    finally { setSaving(false); setEditId(null); }
  };

  const totalBudget  = budget.reduce((s, b) => s + b.limit, 0);
  const totalSpent   = budget.reduce((s, b) => s + b.spent, 0);
  const overBudget   = budget.filter(b => b.status === "danger").length;
  const nearLimit    = budget.filter(b => b.status === "warning").length;

  return (
    <div className="space-y-6">
      {/* Summary */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Total Budget",   value: formatCurrency(totalBudget, currency),  color: "text-foreground" },
          { label: "Total Spent",    value: formatCurrency(totalSpent, currency),   color: "text-warning"    },
          { label: "Remaining",      value: formatCurrency(totalBudget - totalSpent, currency), color: "text-success" },
          { label: "Over Budget",    value: `${overBudget} categories`,             color: overBudget > 0 ? "text-danger" : "text-success" },
        ].map((s, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.07 }}
            className="glass-card rounded-2xl p-4 border border-border"
          >
            <div className="text-[10px] text-muted-foreground mb-1">{s.label}</div>
            <div className={`text-base font-bold ${s.color}`}>{s.value}</div>
          </motion.div>
        ))}
      </div>

      {/* Overall progress */}
      <div className="glass-card rounded-2xl p-5 border border-border">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <PiggyBank className="w-4 h-4 text-primary" />
            <span className="text-sm font-semibold text-foreground">Monthly Budget Overview — {month}</span>
          </div>
          {(overBudget > 0 || nearLimit > 0) && (
            <div className="flex items-center gap-1.5 text-warning text-[11px]">
              <AlertTriangle className="w-3.5 h-3.5" />
              {overBudget > 0 ? `${overBudget} exceeded` : `${nearLimit} near limit`}
            </div>
          )}
        </div>
        <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${Math.min(100, (totalSpent / totalBudget) * 100)}%` }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className={`h-full rounded-full ${totalSpent > totalBudget ? "bg-danger" : totalSpent / totalBudget > 0.8 ? "bg-warning" : "bg-success"}`}
          />
        </div>
        <div className="flex justify-between mt-1.5 text-[10px] text-muted-foreground">
          <span>{formatCurrency(totalSpent, currency)} spent</span>
          <span>{((totalSpent / totalBudget) * 100).toFixed(1)}% of {formatCurrency(totalBudget, currency)}</span>
        </div>
      </div>

      {/* Category budgets */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {budget.map((item, i) => {
            const colors = STATUS_COLORS[item.status];
            const isEditing = editId === item.category;
            return (
              <motion.div key={item.category} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}
                className="glass-card rounded-2xl p-4 border border-border hover:border-primary/20 transition-all"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-foreground">{item.category}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full border font-medium ${colors.badge}`}>
                      {item.status === "good" ? "On Track" : item.status === "warning" ? "Near Limit" : "Exceeded"}
                    </span>
                  </div>
                  {isEditing ? (
                    <div className="flex items-center gap-1.5">
                      <input
                        type="number"
                        value={editVal}
                        onChange={e => setEditVal(e.target.value)}
                        className="w-24 px-2 py-1 text-xs rounded-lg border border-primary bg-background text-foreground outline-none"
                        autoFocus
                        onKeyDown={e => { if (e.key === "Enter") saveEdit(item.category); if (e.key === "Escape") cancelEdit(); }}
                      />
                      <button onClick={() => saveEdit(item.category)} disabled={saving}
                        className="p-1 rounded-lg bg-success/10 text-success hover:bg-success/20 transition-colors">
                        {saving ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Check className="w-3.5 h-3.5" />}
                      </button>
                      <button onClick={cancelEdit} className="p-1 rounded-lg bg-muted text-muted-foreground hover:bg-muted/80 transition-colors">
                        <X className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ) : (
                    <button onClick={() => startEdit(item.category, item.limit)}
                      className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors">
                      <Edit2 className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>

                {/* Progress bar */}
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden mb-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${item.percentage}%` }}
                    transition={{ duration: 0.6, ease: "easeOut", delay: i * 0.04 }}
                    className={`h-full rounded-full ${colors.bar}`}
                  />
                </div>

                <div className="flex justify-between text-[11px]">
                  <span className="text-muted-foreground">
                    Spent: <span className={`font-semibold ${colors.text}`}>{formatCurrency(item.spent, currency)}</span>
                  </span>
                  <span className="text-muted-foreground">
                    Limit: <span className="font-semibold text-foreground">{formatCurrency(item.limit, currency)}</span>
                  </span>
                  <span className="text-muted-foreground">
                    Left: <span className="font-semibold text-success">{formatCurrency(item.remaining, currency)}</span>
                  </span>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}
