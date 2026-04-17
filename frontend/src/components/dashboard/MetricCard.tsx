import { ReactNode } from "react";
import { motion } from "framer-motion";
import { LucideIcon, TrendingUp, TrendingDown } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string;
  subtitle?: string;
  icon: LucideIcon;
  trend?: { value: string; positive: boolean };
  variant?: "default" | "success" | "danger" | "warning" | "primary" | "gold";
  children?: ReactNode;
}

const accentColor = {
  default:  "hsl(var(--muted-foreground))",
  success:  "hsl(var(--success))",
  danger:   "hsl(var(--danger))",
  warning:  "hsl(var(--warning))",
  primary:  "hsl(var(--primary))",
  gold:     "hsl(var(--warning))",
};

const iconBg = {
  default:  "bg-muted",
  success:  "bg-success/10",
  danger:   "bg-danger/10",
  warning:  "bg-warning/10",
  primary:  "bg-primary/10",
  gold:     "bg-warning/10",
};

const iconColor = {
  default:  "text-muted-foreground",
  success:  "text-success",
  danger:   "text-danger",
  warning:  "text-warning",
  primary:  "text-primary",
  gold:     "text-warning",
};

const borderColor = {
  default:  "border-border",
  success:  "border-success/20",
  danger:   "border-danger/20",
  warning:  "border-warning/20",
  primary:  "border-primary/20",
  gold:     "border-warning/20",
};

export default function MetricCard({ title, value, subtitle, icon: Icon, trend, variant = "default", children }: MetricCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -2, transition: { duration: 0.2 } }}
      className={`glass-card rounded-2xl p-5 border ${borderColor[variant]} transition-all duration-300 group cursor-default relative overflow-hidden`}
    >
      {/* Top row */}
      <div className="flex items-start justify-between mb-4">
        <div className={`p-2.5 rounded-xl ${iconBg[variant]} transition-transform duration-300 group-hover:scale-110`}>
          <Icon className={`w-4 h-4 ${iconColor[variant]}`} />
        </div>
        {trend && (
          <div className={`flex items-center gap-1 text-[10px] font-semibold px-2 py-1 rounded-lg ${
            trend.positive
              ? "bg-success/10 text-success"
              : "bg-danger/10 text-danger"
          }`}>
            {trend.positive ? <TrendingUp className="w-2.5 h-2.5" /> : <TrendingDown className="w-2.5 h-2.5" />}
            {trend.value}
          </div>
        )}
      </div>

      {/* Value */}
      <div
        className="text-2xl font-bold tracking-tight mb-0.5 tabular-nums"
        style={{ color: variant === "default" ? "hsl(var(--foreground))" : accentColor[variant] }}
      >
        {value}
      </div>

      {/* Title */}
      <div className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider">{title}</div>

      {subtitle && <div className="text-[10px] text-muted-foreground/60 mt-1">{subtitle}</div>}

      {/* Bottom accent line on hover */}
      <div
        className="absolute bottom-0 left-4 right-4 h-px rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        style={{ background: `linear-gradient(90deg, transparent, ${accentColor[variant]}, transparent)` }}
      />

      {children}
    </motion.div>
  );
}
