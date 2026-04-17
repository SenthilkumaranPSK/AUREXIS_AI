import { motion } from "framer-motion";
import { Lightbulb, ArrowRight } from "lucide-react";

const recommendations = [
  { text: "Reduce entertainment expenses by 15%", impact: "Save ₹900/mo", type: "savings" },
  { text: "Increase emergency fund contributions", impact: "₹6mo buffer", type: "safety" },
  { text: "Avoid taking new loans this quarter", impact: "Lower risk", type: "debt" },
  { text: "Increase SIP by ₹5,000/month", impact: "+₹2.1L in 3yr", type: "invest" },
  { text: "Reduce credit card utilization below 30%", impact: "+20 credit", type: "credit" },
  { text: "Delay major purchase by 3 months", impact: "Better timing", type: "planning" },
  { text: "Rebalance investment portfolio", impact: "Lower risk", type: "invest" },
];

const typeColors: Record<string, string> = {
  savings: "bg-success/10 text-success",
  safety:  "bg-primary/10 text-primary",
  debt:    "bg-danger/10 text-danger",
  invest:  "bg-primary/10 text-primary",
  credit:  "bg-warning/10 text-warning",
  planning:"bg-muted text-muted-foreground",
};

export default function RecommendationFeed() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="w-4 h-4 text-warning" />
        <h3 className="text-sm font-semibold text-foreground">AI Recommendations</h3>
      </div>
      <div className="space-y-2">
        {recommendations.map((rec, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className="flex items-center gap-3 p-3 rounded-xl bg-secondary/30 hover:bg-secondary/50 cursor-pointer group transition-all"
          >
            <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${typeColors[rec.type]?.includes("text-success") ? "bg-success" : typeColors[rec.type]?.includes("text-danger") ? "bg-danger" : typeColors[rec.type]?.includes("text-warning") ? "bg-warning" : "bg-primary"}`} />
            <span className="text-xs text-foreground flex-1">{rec.text}</span>
            <span className={`text-[10px] px-2 py-0.5 rounded-md font-medium ${typeColors[rec.type]}`}>{rec.impact}</span>
            <ArrowRight className="w-3 h-3 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
