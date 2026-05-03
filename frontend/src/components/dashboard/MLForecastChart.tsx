import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { getMLForecast } from "@/lib/api";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from "recharts";
import { Loader2, Brain, ChevronDown } from "lucide-react";
import { useMouseReactive } from "@/hooks/useMouseReactive";

const MODEL_COLORS: Record<string, string> = {
  ARIMA:            "hsl(221 83% 58%)",
  LSTM:             "hsl(280 70% 60%)",
  RandomForest:     "hsl(158 64% 42%)",
  GradientBoosting: "hsl(43 96% 56%)",
  Ensemble:         "hsl(0 72% 55%)",
};

const MODEL_LABELS: Record<string, string> = {
  ARIMA:            "ARIMA",
  LSTM:             "LSTM",
  RandomForest:     "Random Forest",
  GradientBoosting: "Gradient Boosting",
  Ensemble:         "Ensemble",
};

type MetricKey = "income" | "expense" | "savings";

export default function MLForecastChart() {
  const { currentUser } = useStore();
  const [data, setData]         = useState<any>(null);
  const [loading, setLoading]   = useState(true);
  const [metric, setMetric]     = useState<MetricKey>("savings");
  const [activeModels, setActiveModels] = useState<string[]>(["Ensemble", "ARIMA", "RandomForest"]);
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 25, tiltIntensity: 2 });

  useEffect(() => {
    if (!currentUser?.id) return;
    setLoading(true);
    getMLForecast(6)
      .then(res => setData(res))
      .catch(err => {
        console.error("ML Forecast Error:", err);
        setData(null);
      })
      .finally(() => setLoading(false));
  }, [currentUser?.id]);

  const toggleModel = (model: string) => {
    setActiveModels(prev =>
      prev.includes(model) ? prev.filter(m => m !== model) : [...prev, model]
    );
  };

  const buildChartData = () => {
    if (!data || !data[metric]) return [];
    const fc = data[metric];
    return fc.months.map((month: string, i: number) => {
      const point: any = { month };
      Object.keys(fc.models).forEach(model => {
        if (activeModels.includes(model)) {
          point[model] = fc.models[model][i];
        }
      });
      return point;
    });
  };

  return (
    <motion.div 
      ref={ref}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      initial={{ opacity: 0, y: 12 }} 
      animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-primary/10">
            <Brain className="w-4 h-4 text-primary" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-foreground">ML Forecast Models</h3>
            <p className="text-[11px] text-muted-foreground">ARIMA · LSTM · Random Forest · Gradient Boosting</p>
          </div>
        </div>

        {/* Metric selector */}
        <div className="flex gap-1.5">
          {(["income", "expense", "savings"] as MetricKey[]).map(m => (
            <button key={m} onClick={() => setMetric(m)}
              className={`px-2.5 py-1 rounded-lg text-[11px] font-medium capitalize transition-all ${
                metric === m ? "gradient-primary text-white" : "bg-secondary text-muted-foreground hover:text-foreground"
              }`}
            >
              {m}
            </button>
          ))}
        </div>
      </div>

      {/* Model accuracy badges */}
      {data?.modelAccuracy && (
        <div className="flex flex-wrap gap-2 mb-4">
          {Object.entries(data.modelAccuracy).map(([model, acc]: [string, any]) => (
            <button key={model} onClick={() => toggleModel(model)}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-medium border transition-all ${
                activeModels.includes(model)
                  ? "border-transparent text-white"
                  : "bg-muted text-muted-foreground border-border opacity-50"
              }`}
              style={activeModels.includes(model) ? { background: MODEL_COLORS[model] } : {}}
            >
              <span>{MODEL_LABELS[model]}</span>
              <span className="opacity-80">{acc}%</span>
            </button>
          ))}
        </div>
      )}

      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <div className="text-center">
            <Loader2 className="w-6 h-6 animate-spin text-muted-foreground mx-auto mb-2" />
            <p className="text-xs text-muted-foreground">Synthesizing predictive models...</p>
          </div>
        </div>
      ) : !data ? (
        <div className="h-64 flex items-center justify-center text-muted-foreground text-sm">
          Insufficient historical telemetry for accurate forecasting.
        </div>
      ) : (
        <>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={buildChartData()} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
              <XAxis dataKey="month" tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 9, fill: "hsl(var(--muted-foreground))" }} axisLine={false} tickLine={false}
                tickFormatter={(v) => `₹${(v/1000).toFixed(0)}k`} width={48} />
              <Tooltip
                contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 10, fontSize: 11 }}
                formatter={(v: number, name: string) => [formatCurrency(v), MODEL_LABELS[name] || name]}
              />
              {activeModels.map(model => (
                <Line key={model} type="monotone" dataKey={model}
                  stroke={MODEL_COLORS[model]} strokeWidth={model === "Ensemble" ? 2.5 : 1.5}
                  dot={false} strokeDasharray={model === "Ensemble" ? undefined : "4 2"}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>

          {/* Stats row */}
          <div className="grid grid-cols-4 gap-2 mt-4 pt-4 border-t border-border">
            {Object.entries(data.modelAccuracy || {}).slice(0, 4).map(([model, acc]: [string, any]) => (
              <div key={model} className="bg-muted/50 rounded-xl p-2.5 text-center border border-border">
                <div className="text-[9px] text-muted-foreground mb-1">{MODEL_LABELS[model]}</div>
                <div className="text-sm font-bold tabular-nums" style={{ color: MODEL_COLORS[model] }}>{acc}%</div>
                <div className="text-[9px] text-muted-foreground">Confidence</div>
              </div>
            ))}
          </div>

          <p className="text-[10px] text-muted-foreground mt-3 text-center">
            Predictive model synthesized using {data.dataPoints} months of transactional telemetry · {data.note}
          </p>
        </>
      )}
    </motion.div>
  );
}
