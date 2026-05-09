import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  LineChart, Line, AreaChart, Area, Cell, PieChart, Pie
} from "recharts";
import { 
  TrendingUp, TrendingDown, Target, Brain, Activity, 
  PieChart as PieChartIcon, Zap, CheckCircle2, AlertCircle
} from "lucide-react";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { getAdvancedAnalytics } from "@/lib/api";


interface AnalyticsData {
  dashboard: {
    summary: {
      net_worth: number;
      monthly_income: number;
      monthly_expenses: number;
      monthly_savings: number;
      savings_rate: number;
    };
    top_insights: Array<{
      category: string;
      title: string;
      insight: string;
      impact: "high" | "medium" | "low";
      type: "positive" | "negative" | "info";
    }>;
    behavior_score: number;
    behavior_profile: string;
    patterns_detected: number;
    net_worth_trend: {
      metric: string;
      slope: number;
      change_pct: number;
      trend: string;
      volatility: number;
      forecast_next: number;
    } | null;
    strengths: string[];
    recommendations: string[];
  };
}

export default function AdvancedAnalyticsView() {
  const { currency } = useStore();
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getAdvancedAnalytics();
        if (result.success) {
          setData(result);
        }
      } catch (error) {
        console.error("Failed to fetch analytics:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[600px]">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full"
        />
      </div>
    );
  }

  if (!data) return null;

  const { dashboard } = data;

  return (
    <div className="space-y-8 pb-12">
      {/* Top Banner - Behavior Score */}
      <motion.div 
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="grid grid-cols-12 gap-6"
      >
        <motion.div 
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="col-span-12 lg:col-span-8 glass-card rounded-3xl p-8 border border-white/[0.05] relative overflow-hidden group"
        >
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -mr-32 -mt-32 transition-all group-hover:bg-primary/10" />
          
          <div className="flex flex-col md:flex-row items-center gap-8 relative z-10">
            <div className="relative">
              <svg className="w-32 h-32 transform -rotate-90">
                <circle
                  cx="64" cy="64" r="58"
                  fill="transparent"
                  stroke="currentColor"
                  strokeWidth="8"
                  className="text-white/5"
                />
                <motion.circle
                  cx="64" cy="64" r="58"
                  fill="transparent"
                  stroke="currentColor"
                  strokeWidth="8"
                  strokeDasharray={364.4}
                  initial={{ strokeDashoffset: 364.4 }}
                  animate={{ strokeDashoffset: 364.4 * (1 - (dashboard?.behavior_score || 0) / 100) }}
                  transition={{ duration: 1.5, delay: 0.2, ease: "easeOut" }}
                  className="text-primary"
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-bold text-foreground">{dashboard?.behavior_score || 0}</span>
                <span className="text-[10px] text-muted-foreground uppercase font-bold tracking-widest">Score</span>
              </div>
            </div>

            <div className="flex-1 text-center md:text-left">
              <div className="flex items-center justify-center md:justify-start gap-2 mb-2">
                <Brain className="w-5 h-5 text-primary" />
                <h2 className="text-xl font-bold text-foreground">Psychographic Profile</h2>
              </div>
              <p className="text-muted-foreground text-sm leading-relaxed max-w-lg">
                Your behavior indicates a <span className="text-primary font-bold">{dashboard.behavior_profile || "Balanced"}</span> profile. 
                You show strong discipline in {dashboard.strengths?.[0]?.toLowerCase() || "your current spending"} but could optimize your {dashboard.recommendations?.[0]?.split(' ').slice(0, 3).join(' ').toLowerCase() || "future savings"}.
              </p>
              
              <div className="flex flex-wrap gap-2 mt-6 justify-center md:justify-start">
                {dashboard.strengths?.slice(0, 3).map((s, i) => (
                  <span key={i} className="px-3 py-1.5 rounded-full bg-success/10 text-success text-[10px] font-bold border border-success/20 flex items-center gap-1.5">
                    <CheckCircle2 className="w-3 h-3" /> {s}
                  </span>
                ))}
                {(!dashboard.strengths || dashboard.strengths.length === 0) && (
                  <span className="text-[10px] text-muted-foreground italic">No behavior strengths recorded yet</span>
                )}
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.1, ease: "easeOut" }}
          className="col-span-12 lg:col-span-4 glass-card rounded-3xl p-8 border border-white/[0.05] flex flex-col justify-between"
        >
          <div>
            <div className="flex items-center gap-2 mb-6">
              <Zap className="w-5 h-5 text-warning" />
              <h2 className="text-lg font-bold text-foreground">Executive AI Summary</h2>
            </div>
            <div className="space-y-4">
              {dashboard.top_insights?.slice(0, 2).map((insight, i) => (
                <div key={i} className="flex gap-3">
                  <div className={`mt-1 w-1.5 h-1.5 rounded-full shrink-0 ${
                    insight.type === 'positive' ? 'bg-success' : insight.type === 'negative' ? 'bg-danger' : 'bg-primary'
                  }`} />
                  <div>
                    <div className="text-xs font-bold text-foreground">{insight.title}</div>
                    <div className="text-[11px] text-muted-foreground mt-0.5 leading-relaxed">{insight.insight}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <button className="w-full mt-6 py-3 rounded-xl bg-primary/10 hover:bg-primary/20 text-primary text-xs font-bold transition-all border border-primary/20">
            Download Deep Audit PDF
          </button>
        </motion.div>
      </motion.div>

      {/* Main Grid */}
      <motion.div 
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={{
          hidden: { opacity: 0 },
          visible: {
            opacity: 1,
            transition: {
              staggerChildren: 0.1
            }
          }
        }}
        className="grid grid-cols-12 gap-6"
      >
        {/* Trend Analysis */}
        <motion.div 
          variants={{
            hidden: { opacity: 0, y: 12 },
            visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" } }
          }}
          className="col-span-12 lg:col-span-8 glass-card rounded-3xl p-8 border border-white/[0.05]"
        >
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-2xl bg-primary/10">
                <Activity className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-foreground">Equity & Net Worth Momentum</h2>
                <p className="text-[11px] text-muted-foreground">Historical velocity vs 60-day projected trajectory</p>
              </div>
            </div>
            
            {dashboard.net_worth_trend && (
              <div className="text-right">
                <div className={`text-sm font-bold flex items-center justify-end gap-1 ${
                  dashboard.net_worth_trend.change_pct > 0 ? 'text-success' : 'text-danger'
                }`}>
                  {dashboard.net_worth_trend.change_pct > 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                  {Math.abs(dashboard.net_worth_trend.change_pct || 0).toFixed(1)}%
                </div>
                <div className="text-[10px] text-muted-foreground uppercase font-bold tracking-widest mt-0.5">MoM Velocity</div>
              </div>
            )}
          </div>

          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={[
                { name: 'Jan', value: 4500000, proj: 4500000 },
                { name: 'Feb', value: 4800000, proj: 4800000 },
                { name: 'Mar', value: 5200000, proj: 5200000 },
                { name: 'Apr', value: 5100000, proj: 5100000 },
                { name: 'May', value: null, proj: 5100000 },
                { name: 'Jun', value: null, proj: 5400000 },
                { name: 'Jul', value: null, proj: 5800000 },
              ]}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border) / 0.3)" />
                <XAxis 
                  dataKey="name" 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fontSize: 10, fill: 'hsl(var(--muted-foreground))' }}
                  dy={10}
                />
                <YAxis 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fontSize: 10, fill: 'hsl(var(--muted-foreground))' }}
                  tickFormatter={(v) => `₹${(v/100000).toFixed(0)}L`}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderRadius: '16px', border: '1px solid hsl(var(--border) / 0.1)' }}
                  itemStyle={{ fontSize: 12, fontWeight: 'bold' }}
                />
                <Area 
                  type="monotone" 
                  dataKey="value" 
                  stroke="hsl(var(--primary))" 
                  strokeWidth={3}
                  fillOpacity={1} 
                  fill="url(#colorValue)" 
                />
                <Area 
                  type="monotone" 
                  dataKey="proj" 
                  stroke="hsl(var(--primary))" 
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  fill="transparent"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Pattern Detection */}
        <motion.div 
          variants={{
            hidden: { opacity: 0, y: 12 },
            visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" } }
          }}
          className="col-span-12 lg:col-span-4 glass-card rounded-3xl p-8 border border-white/[0.05]"
        >
          <div className="flex items-center gap-3 mb-8">
            <div className="p-2.5 rounded-2xl bg-warning/10">
              <PieChartIcon className="w-5 h-5 text-warning" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-foreground">Spending DNA</h2>
              <p className="text-[11px] text-muted-foreground">Detected categorical anomalies</p>
            </div>
          </div>

          <div className="h-[220px] w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={[
                    { name: 'Lifestyle', value: 35, color: '#3B82F6' },
                    { name: 'Fixed', value: 45, color: '#8B5CF6' },
                    { name: 'Savings', value: 20, color: '#10B981' },
                  ]}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={8}
                  dataKey="value"
                >
                  {[0,1,2].map((i) => (
                    <Cell key={`cell-${i}`} fill={['#3B82F6', '#8B5CF6', '#10B981'][i]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-4 mt-6">
            <div className="p-4 rounded-2xl bg-muted/30 border border-border/50">
              <div className="flex items-center gap-2 mb-1">
                <AlertCircle className="w-3.5 h-3.5 text-warning" />
                <span className="text-xs font-bold text-foreground">Anomaly Detected</span>
              </div>
              <p className="text-[10px] text-muted-foreground leading-relaxed">
                Swiggy/Zomato spending is 42% higher than your peer group (Engineers in Chennai). Potential saving: ₹4,500/mo.
              </p>
            </div>
          </div>
        </motion.div>
      </motion.div>

      {/* Bottom Insights */}
      <motion.div 
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut", delay: 0.3 }}
        className="grid grid-cols-12 gap-6"
      >
        <div className="col-span-12 glass-card rounded-3xl p-8 border border-white/[0.05]">
          <div className="flex items-center gap-2 mb-8">
            <Activity className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-bold text-foreground">Strategic Recommendations</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {dashboard.recommendations.map((rec, i) => (
              <div key={i} className="p-6 rounded-2xl bg-white/[0.02] border border-white/[0.05] hover:border-primary/20 transition-all group">
                <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center text-primary mb-4 group-hover:scale-110 transition-transform">
                  {i + 1}
                </div>
                <p className="text-sm text-foreground/90 leading-relaxed">{rec}</p>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
}
