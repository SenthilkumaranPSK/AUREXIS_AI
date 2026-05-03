import { useMouseReactive } from "@/hooks/useMouseReactive";
import { useEffect, useState } from "react";
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from "recharts";
import { useStore } from "@/store/useStore";
import { motion } from "framer-motion";
import { Loader2, Activity } from "lucide-react";

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  const data = payload[0].payload;
  return (
    <div className="glass-card rounded-xl p-3 border border-border shadow-2xl text-xs min-w-[140px]">
      <div className="font-semibold text-foreground mb-1">{data.factor}</div>
      <div className="flex items-center justify-between gap-3">
        <span className="text-muted-foreground">Score</span>
        <span className="font-bold text-primary">{data.value}/100</span>
      </div>
    </div>
  );
};

// Generate radar chart data based on user's financial metrics
const generateRadarData = (currentUser: any) => {
  const savingsRate = currentUser?.savingsRate || 0;
  const emergencyFund = currentUser?.emergencyFundMonths || 0;
  const debtRatio = currentUser?.debtToIncomeRatio || 0;
  const healthScore = currentUser?.financialHealthScore || 50;
  
  return [
    {
      factor: "Savings",
      value: Math.min(100, savingsRate * 3), // Scale savings rate
      fullMark: 100,
    },
    {
      factor: "Emergency Fund",
      value: Math.min(100, (emergencyFund / 6) * 100), // 6 months is 100%
      fullMark: 100,
    },
    {
      factor: "Debt Management",
      value: Math.max(0, 100 - (debtRatio * 200)), // Lower debt ratio = higher score
      fullMark: 100,
    },
    {
      factor: "Investment",
      value: 75, // Mock investment score
      fullMark: 100,
    },
    {
      factor: "Planning",
      value: Math.min(100, healthScore + 10), // Slightly higher than overall health
      fullMark: 100,
    },
    {
      factor: "Risk Management",
      value: emergencyFund >= 3 ? 80 : 45, // Based on emergency fund
      fullMark: 100,
    }
  ];
};

export default function HealthRadarChart() {
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 25, tiltIntensity: 2 });
  const { currentUser } = useStore();
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser?.id) return;
    
    // Simulate API call with generated radar data
    setLoading(true);
    setTimeout(() => {
      setData(generateRadarData(currentUser));
      setLoading(false);
    }, 600);
  }, [currentUser?.id]);

  if (loading) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-border h-96 flex items-center justify-center">
        <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (!data.length) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-border h-96 flex items-center justify-center text-muted-foreground text-sm">
        No health data available
      </div>
    );
  }

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
            <div className="p-1.5 rounded-lg bg-primary/10">
              <Activity className="w-3.5 h-3.5 text-primary" />
            </div>
            <h3 className="text-sm font-semibold text-foreground">Health Factor Analysis</h3>
          </div>
          <p className="text-[11px] text-muted-foreground ml-8">Multi-dimensional health breakdown</p>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <RadarChart data={data} margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
          <PolarGrid stroke="hsl(var(--border))" />
          <PolarAngleAxis 
            dataKey="factor" 
            tick={{ fontSize: 11, fill: "hsl(var(--foreground))", fontWeight: 500 }}
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]} 
            tick={{ fontSize: 9, fill: "hsl(var(--muted-foreground))" }}
          />
          <Radar 
            name="Health Score" 
            dataKey="value" 
            stroke="hsl(var(--primary))" 
            fill="hsl(var(--primary))" 
            fillOpacity={0.3}
            strokeWidth={2}
          />
          <Tooltip content={<CustomTooltip />} />
        </RadarChart>
      </ResponsiveContainer>

      <div className="grid grid-cols-2 gap-2 mt-4">
        {data.map((item, i) => (
          <div key={i} className="bg-muted/50 rounded-xl p-2.5 border border-border">
            <div className="flex justify-between items-center mb-1">
              <span className="text-[10px] text-muted-foreground font-medium">{item.factor}</span>
              <span className="text-xs font-bold text-primary">{item.value}</span>
            </div>
            <div className="h-1 bg-muted rounded-full overflow-hidden">
              <div 
                className="h-full rounded-full bg-primary transition-all duration-500" 
                style={{ width: `${item.value}%` }} 
              />
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
