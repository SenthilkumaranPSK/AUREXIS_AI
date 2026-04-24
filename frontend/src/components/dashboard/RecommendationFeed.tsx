import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { getUserRecommendations } from "@/lib/api";
import { Lightbulb, ArrowRight, Loader2 } from "lucide-react";

const typeColors: Record<string, string> = {
  savings:  "bg-success/10 text-success",
  safety:   "bg-primary/10 text-primary",
  debt:     "bg-danger/10 text-danger",
  invest:   "bg-primary/10 text-primary",
  credit:   "bg-warning/10 text-warning",
  planning: "bg-muted text-muted-foreground",
};

const typeDot: Record<string, string> = {
  savings:  "bg-success",
  safety:   "bg-primary",
  debt:     "bg-danger",
  invest:   "bg-primary",
  credit:   "bg-warning",
  planning: "bg-muted-foreground",
};

export default function RecommendationFeed() {
  const { currentUser } = useStore();
  const [recs, setRecs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser?.id) return;
    setLoading(true);
    getUserRecommendations(currentUser.id)
      .then(res => setRecs(res.recommendations))
      .catch(() => setRecs([]))
      .finally(() => setLoading(false));
  }, [currentUser?.id]);

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="w-4 h-4 text-warning" />
        <h3 className="text-sm font-semibold text-foreground">AI Recommendations</h3>
        {!loading && <span className="ml-auto text-[10px] text-muted-foreground">{recs.length} insights</span>}
      </div>

      {loading ? (
        <div className="h-24 flex items-center justify-center">
          <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />
        </div>
      ) : (
        <div className="space-y-2">
          {recs.map((rec, i) => (
            <motion.div key={i}
              initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className="flex items-center gap-3 p-3 rounded-xl bg-secondary/30 hover:bg-secondary/50 cursor-pointer group transition-all"
            >
              <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${typeDot[rec.type] || "bg-primary"}`} />
              <span className="text-xs text-foreground flex-1">{rec.text}</span>
              <span className={`text-[10px] px-2 py-0.5 rounded-md font-medium shrink-0 ${typeColors[rec.type] || typeColors.planning}`}>
                {rec.impact}
              </span>
              <ArrowRight className="w-3 h-3 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
            </motion.div>
          ))}
        </div>
      )}
    </motion.div>
  );
}
