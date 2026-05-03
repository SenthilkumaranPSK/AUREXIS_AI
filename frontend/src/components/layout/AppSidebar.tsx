import { useNavigate, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useMouseReactive } from "@/hooks/useMouseReactive";
import {
  LayoutDashboard, Heart, ShieldAlert, PiggyBank, CreditCard,
  TrendingUp, Target, LineChart, FlaskConical, Bell, FileText,
  Settings, Sparkles, ChevronLeft, ChevronRight
} from "lucide-react";
import { useStore } from "@/store/useStore";

const navItems = [
  { icon: LayoutDashboard, label: "Overview",        path: "/dashboard",             group: "main" },
  { icon: Heart,           label: "Financial Health", path: "/dashboard/health",      group: "main" },
  { icon: ShieldAlert,     label: "Risk Analysis",    path: "/dashboard/risk",        group: "main" },
  { icon: PiggyBank,       label: "Savings",          path: "/dashboard/savings",     group: "finance" },
  { icon: CreditCard,      label: "Debt",             path: "/dashboard/debt",        group: "finance" },
  { icon: TrendingUp,      label: "Investments",      path: "/dashboard/investments", group: "finance" },
  { icon: Target,          label: "Goals",            path: "/dashboard/goals",       group: "finance" },
  { icon: LineChart,       label: "Forecasting",      path: "/dashboard/forecasting", group: "tools" },
  { icon: FlaskConical,    label: "Scenarios",        path: "/dashboard/simulation",  group: "tools" },
  { icon: Bell,            label: "Alerts",           path: "/dashboard/alerts",      group: "tools" },
  { icon: FileText,        label: "Reports",          path: "/dashboard/reports",     group: "tools" },
  { icon: Settings,        label: "Settings",         path: "/dashboard/settings",    group: "tools" },
];

const groups = [
  { key: "main",    label: "OVERVIEW" },
  { key: "finance", label: "FINANCE" },
  { key: "tools",   label: "TOOLS" },
];

export default function AppSidebar() {
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 50, tiltIntensity: 1 });
  const { sidebarOpen, setSidebarOpen } = useStore();
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <motion.aside
      ref={ref}
      style={{ x, y, rotateX, rotateY, background: "hsl(var(--card) / 0.75)", backdropFilter: "blur(24px)" }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      animate={{ width: sidebarOpen ? 232 : 64 }}
      transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}
      className="h-screen sticky top-0 border-r border-border/30 flex flex-col z-30 overflow-hidden shrink-0"
    >
      {/* Logo */}
      <div className="h-16 flex items-center gap-3 px-4 border-b border-white/[0.05] shrink-0">
        <div className="w-8 h-8 rounded-xl gradient-primary glow-primary flex items-center justify-center shrink-0">
          <Sparkles className="w-4 h-4 text-white" />
        </div>
        <AnimatePresence>
          {sidebarOpen && (
            <motion.div
              initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -8 }}
              transition={{ duration: 0.15 }}
              className="overflow-hidden"
            >
              <div className="text-sm font-bold text-foreground tracking-widest whitespace-nowrap">AUREXIS</div>
              <div className="text-[9px] text-muted-foreground tracking-[0.2em] whitespace-nowrap">AI FINANCE</div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Nav */}
      <nav className="flex-1 py-4 overflow-y-auto overflow-x-hidden">
        {groups.map((group) => {
          const items = navItems.filter(i => i.group === group.key);
          return (
            <div key={group.key} className="mb-4">
              <AnimatePresence>
                {sidebarOpen && (
                  <motion.div
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                    className="px-4 mb-1.5"
                  >
                    <span className="text-[9px] font-semibold tracking-[0.15em] text-muted-foreground/60">{group.label}</span>
                  </motion.div>
                )}
              </AnimatePresence>
              <div className="px-2 space-y-0.5">
                {items.map((item) => {
                  const isActive = item.path === "/dashboard"
                    ? location.pathname === "/dashboard"
                    : location.pathname.startsWith(item.path);
                  return (
                    <button
                      key={item.path}
                      onClick={() => navigate(item.path)}
                      title={!sidebarOpen ? item.label : undefined}
                      className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 group relative ${
                        isActive
                          ? "bg-primary/15 text-primary border border-primary/20"
                          : "text-muted-foreground hover:text-foreground hover:bg-secondary/60"
                      }`}
                    >
                      {isActive && (
                        <motion.div
                          layoutId="activeIndicator"
                          className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 rounded-r-full bg-primary"
                        />
                      )}
                      <item.icon className={`w-4 h-4 shrink-0 transition-colors ${isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground"}`} />
                      <AnimatePresence>
                        {sidebarOpen && (
                          <motion.span
                            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                            className="whitespace-nowrap"
                          >
                            {item.label}
                          </motion.span>
                        )}
                      </AnimatePresence>
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </nav>

      {/* Toggle */}
      <div className="p-3 border-t border-white/[0.05] shrink-0">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="w-full flex items-center justify-center p-2 rounded-xl hover:bg-secondary/60 text-muted-foreground hover:text-foreground transition-all"
        >
          {sidebarOpen ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </button>
      </div>
    </motion.aside>
  );
}
