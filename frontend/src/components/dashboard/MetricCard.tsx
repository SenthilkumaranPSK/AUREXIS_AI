import { ReactNode } from "react";
import { motion } from "framer-motion";
import { LucideIcon, TrendingUp, TrendingDown } from "lucide-react";
import { useMouseReactive } from "@/hooks/useMouseReactive";

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
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({
    sensitivity: 20,
    tiltIntensity: 2
  });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      whileHover={{ y: -4 }}
      transition={{ type: "spring", stiffness: 400, damping: 25 }}
      className={`glass-card rounded-2xl p-5 border ${borderColor[variant]} transition-all duration-300 group cursor-default relative overflow-hidden hover:shadow-lg`}
    >
      {/* Top row */}
      <div className="flex items-start justify-between mb-4">
        <motion.div 
          className={`p-2.5 rounded-xl ${iconBg[variant]}`}
          whileHover={{ scale: 1.15, rotate: 5 }}
          transition={{ type: "spring", stiffness: 400 }}
        >
          <Icon className={`w-4 h-4 ${iconColor[variant]}`} />
        </motion.div>
        {trend && (
          <motion.div 
            className={`flex items-center gap-1 text-[10px] font-semibold px-2 py-1 rounded-lg ${
              trend.positive
                ? "bg-success/10 text-success"
                : "bg-danger/10 text-danger"
            }`}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            {trend.positive ? <TrendingUp className="w-2.5 h-2.5" /> : <TrendingDown className="w-2.5 h-2.5" />}
            {trend.value}
          </motion.div>
        )}
      </div>

      {/* Value */}
      <motion.div
        className="text-2xl font-bold tracking-tight mb-0.5 tabular-nums"
        style={{ color: variant === "default" ? "hsl(var(--foreground))" : accentColor[variant] }}
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1, type: "spring", stiffness: 400 }}
      >
        {value}
      </motion.div>

      {/* Title */}
      <div className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider">{title}</div>

      {subtitle && <div className="text-[10px] text-muted-foreground/60 mt-1">{subtitle}</div>}

      {/* Bottom accent line on hover */}
      <motion.div
        className="absolute bottom-0 left-4 right-4 h-px rounded-full"
        style={{ background: `linear-gradient(90deg, transparent, ${accentColor[variant]}, transparent)` }}
        initial={{ opacity: 0, scaleX: 0 }}
        whileHover={{ opacity: 1, scaleX: 1 }}
        transition={{ duration: 0.3 }}
      />

      {children}
    </motion.div>
  );
}
