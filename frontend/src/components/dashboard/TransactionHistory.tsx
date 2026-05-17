import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { Search, Filter, ArrowUpCircle, ArrowDownCircle, RefreshCw, TrendingUp, TrendingDown, Wallet } from "lucide-react";

interface Transaction {
  id: string;
  date: string;
  narration: string;
  amount: number;
  type: string;
  mode: string;
  balance: number;
  category: string;
  bank: string;
}

const CATEGORY_COLORS: Record<string, string> = {
  Income:           "bg-success/10 text-success border-success/20",
  Housing:          "bg-blue-500/10 text-blue-400 border-blue-500/20",
  Investment:       "bg-purple-500/10 text-purple-400 border-purple-500/20",
  Food:             "bg-orange-500/10 text-orange-400 border-orange-500/20",
  Shopping:         "bg-pink-500/10 text-pink-400 border-pink-500/20",
  "Loan EMI":       "bg-red-500/10 text-red-400 border-red-500/20",
  Utilities:        "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
  Transport:        "bg-cyan-500/10 text-cyan-400 border-cyan-500/20",
  Entertainment:    "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
  Healthcare:       "bg-teal-500/10 text-teal-400 border-teal-500/20",
  Insurance:        "bg-slate-500/10 text-slate-400 border-slate-500/20",
  "Cash Withdrawal":"bg-amber-500/10 text-amber-400 border-amber-500/20",
  Others:           "bg-muted text-muted-foreground border-border",
};

const CATEGORIES = ["All", "Income", "Housing", "Food", "Shopping", "Investment", "Loan EMI", "Utilities", "Transport", "Entertainment", "Healthcare", "Others"];

export default function TransactionHistory() {
  const { currentUser, currency } = useStore();
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [filtered, setFiltered]         = useState<Transaction[]>([]);
  const [loading, setLoading]           = useState(true);
  const [search, setSearch]             = useState("");
  const [category, setCategory]         = useState("All");
  const [typeFilter, setTypeFilter]     = useState("All");
  const [totalCredit, setTotalCredit]   = useState(0);
  const [totalDebit, setTotalDebit]     = useState(0);

  const fetchTransactions = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      const params = new URLSearchParams();
      if (category !== "All") params.set("category", category);
      if (typeFilter !== "All") params.set("txn_type", typeFilter);
      if (search) params.set("search", search);
      params.set("limit", "200");

      const res = await fetch(`/api/user/transactions?${params}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (data.success) {
        setTransactions(data.transactions);
        setFiltered(data.transactions);
        setTotalCredit(data.total_credit);
        setTotalDebit(data.total_debit);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchTransactions(); }, [category, typeFilter]);

  useEffect(() => {
    if (!search) { setFiltered(transactions); return; }
    const s = search.toLowerCase();
    setFiltered(transactions.filter(t =>
      t.narration.toLowerCase().includes(s) || t.category.toLowerCase().includes(s)
    ));
  }, [search, transactions]);

  return (
    <div className="space-y-6">
      {/* Summary cards */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: "Total Credits", value: totalCredit, icon: ArrowUpCircle, color: "text-success", bg: "bg-success/10" },
          { label: "Total Debits",  value: totalDebit,  icon: ArrowDownCircle, color: "text-danger",  bg: "bg-danger/10"  },
          { label: "Net Flow",      value: totalCredit - totalDebit, icon: Wallet, color: totalCredit - totalDebit >= 0 ? "text-success" : "text-danger", bg: "bg-primary/10" },
        ].map((card, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
            className="glass-card rounded-2xl p-5 border border-border"
          >
            <div className="flex items-center gap-3 mb-2">
              <div className={`p-2 rounded-xl ${card.bg}`}>
                <card.icon className={`w-4 h-4 ${card.color}`} />
              </div>
              <span className="text-xs text-muted-foreground font-medium">{card.label}</span>
            </div>
            <div className={`text-xl font-bold tabular-nums ${card.color}`}>
              {formatCurrency(Math.abs(card.value), currency)}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Filters */}
      <div className="glass-card rounded-2xl p-4 border border-border flex flex-wrap gap-3 items-center">
        <div className="flex items-center gap-2 flex-1 min-w-[200px] bg-muted/40 rounded-xl px-3 py-2 border border-border">
          <Search className="w-4 h-4 text-muted-foreground shrink-0" />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search transactions..."
            className="bg-transparent text-xs text-foreground placeholder:text-muted-foreground outline-none flex-1"
          />
        </div>
        <select value={typeFilter} onChange={e => setTypeFilter(e.target.value)}
          className="bg-muted/40 border border-border rounded-xl px-3 py-2 text-xs text-foreground outline-none"
        >
          {["All", "CREDIT", "DEBIT", "INSTALLMENT", "INTEREST"].map(t => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
        <button onClick={fetchTransactions} className="p-2 rounded-xl bg-muted/40 border border-border hover:bg-muted transition-colors">
          <RefreshCw className="w-4 h-4 text-muted-foreground" />
        </button>
      </div>

      {/* Category pills */}
      <div className="flex flex-wrap gap-2">
        {CATEGORIES.map(cat => (
          <button key={cat} onClick={() => setCategory(cat)}
            className={`px-3 py-1.5 rounded-full text-[11px] font-medium border transition-all ${
              category === cat ? "gradient-primary text-white border-transparent" : "bg-muted/30 text-muted-foreground border-border hover:bg-muted/60"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Transaction table */}
      <div className="glass-card rounded-2xl border border-border overflow-hidden">
        <div className="px-5 py-4 border-b border-border flex items-center justify-between">
          <h3 className="text-sm font-semibold text-foreground">
            {filtered.length} Transaction{filtered.length !== 1 ? "s" : ""}
          </h3>
          <span className="text-[11px] text-muted-foreground">Sorted by latest</span>
        </div>

        {loading ? (
          <div className="p-8 flex items-center justify-center">
            <RefreshCw className="w-5 h-5 animate-spin text-muted-foreground" />
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-8 text-center text-muted-foreground text-sm">No transactions found</div>
        ) : (
          <div className="divide-y divide-border">
            {filtered.map((txn, i) => (
              <motion.div key={txn.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: Math.min(i * 0.02, 0.3) }}
                className="flex items-center gap-4 px-5 py-3.5 hover:bg-muted/20 transition-colors"
              >
                {/* Icon */}
                <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 ${txn.type === "CREDIT" ? "bg-success/10" : "bg-danger/10"}`}>
                  {txn.type === "CREDIT"
                    ? <TrendingUp className="w-4 h-4 text-success" />
                    : <TrendingDown className="w-4 h-4 text-danger" />
                  }
                </div>

                {/* Details */}
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-semibold text-foreground truncate">{txn.narration}</div>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-[10px] text-muted-foreground">{txn.date}</span>
                    <span className="text-[10px] text-muted-foreground">·</span>
                    <span className="text-[10px] text-muted-foreground">{txn.mode}</span>
                    <span className="text-[10px] text-muted-foreground">·</span>
                    <span className="text-[10px] text-muted-foreground">{txn.bank}</span>
                  </div>
                </div>

                {/* Category */}
                <span className={`text-[10px] px-2 py-0.5 rounded-full border font-medium shrink-0 ${CATEGORY_COLORS[txn.category] || CATEGORY_COLORS.Others}`}>
                  {txn.category}
                </span>

                {/* Amount */}
                <div className="text-right shrink-0">
                  <div className={`text-sm font-bold tabular-nums ${txn.type === "CREDIT" ? "text-success" : "text-foreground"}`}>
                    {txn.type === "CREDIT" ? "+" : "-"}{formatCurrency(txn.amount, currency)}
                  </div>
                  {txn.balance > 0 && (
                    <div className="text-[10px] text-muted-foreground">Bal: {formatCurrency(txn.balance, currency)}</div>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
