import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useStore } from "@/store/useStore";
import { Bell, CheckCheck, Trash2, RefreshCw, AlertTriangle, TrendingUp, Wallet, ShieldCheck, Info, Loader2 } from "lucide-react";
import { toast } from "sonner";

interface Notification {
  id: number;
  type: "danger" | "warning" | "success" | "info";
  category: string;
  title: string;
  message: string;
  time: string;
  read: boolean;
}

const TYPE_CONFIG = {
  danger:  { icon: AlertTriangle, color: "text-danger",  bg: "bg-danger/10",  border: "border-danger/20"  },
  warning: { icon: AlertTriangle, color: "text-warning", bg: "bg-warning/10", border: "border-warning/20" },
  success: { icon: TrendingUp,    color: "text-success", bg: "bg-success/10", border: "border-success/20" },
  info:    { icon: Info,          color: "text-primary",  bg: "bg-primary/10", border: "border-primary/20" },
};

const CATEGORY_ICONS: Record<string, any> = {
  Budget:      Wallet,
  Transaction: TrendingUp,
  Wealth:      ShieldCheck,
  Investment:  TrendingUp,
};

export default function NotificationsPanel() {
  const { currentUser } = useStore();
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading]             = useState(true);
  const [filter, setFilter]               = useState<"all" | "unread">("all");
  const [unreadCount, setUnreadCount]     = useState(0);

  const token = () => localStorage.getItem("access_token");

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/user/smart-notifications", {
        headers: { Authorization: `Bearer ${token()}` },
      });
      const data = await res.json();
      if (data.success) {
        setNotifications(data.notifications);
        setUnreadCount(data.unread);
      }
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchNotifications(); }, []);

  const markAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    setUnreadCount(0);
    toast.success("All notifications marked as read");
  };

  const dismiss = (id: number) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
    toast.success("Notification dismissed");
  };

  const markRead = (id: number) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const displayed = filter === "unread" ? notifications.filter(n => !n.read) : notifications;

  return (
    <div className="space-y-6">
      {/* Header stats */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Total",    value: notifications.length,                                    color: "text-foreground" },
          { label: "Unread",   value: unreadCount,                                             color: unreadCount > 0 ? "text-warning" : "text-success" },
          { label: "Alerts",   value: notifications.filter(n => n.type === "danger").length,   color: "text-danger"  },
          { label: "Insights", value: notifications.filter(n => n.type === "success").length,  color: "text-success" },
        ].map((s, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.07 }}
            className="glass-card rounded-2xl p-4 border border-border text-center"
          >
            <div className={`text-2xl font-bold ${s.color}`}>{s.value}</div>
            <div className="text-[10px] text-muted-foreground mt-1">{s.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Controls */}
      <div className="glass-card rounded-2xl p-4 border border-border flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-2">
          <Bell className="w-4 h-4 text-primary" />
          <span className="text-sm font-semibold text-foreground">Smart Notifications</span>
          {unreadCount > 0 && (
            <span className="px-2 py-0.5 rounded-full bg-primary text-white text-[10px] font-bold">{unreadCount}</span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {/* Filter tabs */}
          <div className="flex rounded-xl border border-border overflow-hidden">
            {(["all", "unread"] as const).map(f => (
              <button key={f} onClick={() => setFilter(f)}
                className={`px-3 py-1.5 text-[11px] font-medium capitalize transition-colors ${
                  filter === f ? "bg-primary text-white" : "bg-muted/30 text-muted-foreground hover:bg-muted/60"
                }`}
              >
                {f}
              </button>
            ))}
          </div>
          <button onClick={markAllRead} disabled={unreadCount === 0}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-muted/40 border border-border text-[11px] text-muted-foreground hover:text-foreground hover:bg-muted transition-colors disabled:opacity-40"
          >
            <CheckCheck className="w-3.5 h-3.5" /> Mark all read
          </button>
          <button onClick={fetchNotifications}
            className="p-2 rounded-xl bg-muted/40 border border-border hover:bg-muted transition-colors">
            <RefreshCw className="w-3.5 h-3.5 text-muted-foreground" />
          </button>
        </div>
      </div>

      {/* Notification list */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
        </div>
      ) : displayed.length === 0 ? (
        <div className="glass-card rounded-2xl p-12 border border-border text-center">
          <Bell className="w-10 h-10 text-muted-foreground/30 mx-auto mb-3" />
          <p className="text-muted-foreground text-sm">No {filter === "unread" ? "unread " : ""}notifications</p>
        </div>
      ) : (
        <div className="space-y-3">
          <AnimatePresence>
            {displayed.map((notif, i) => {
              const cfg = TYPE_CONFIG[notif.type] || TYPE_CONFIG.info;
              const Icon = CATEGORY_ICONS[notif.category] || cfg.icon;
              return (
                <motion.div
                  key={notif.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20, height: 0 }}
                  transition={{ delay: i * 0.04 }}
                  onClick={() => !notif.read && markRead(notif.id)}
                  className={`glass-card rounded-2xl p-4 border ${cfg.border} cursor-pointer hover:bg-muted/10 transition-all ${!notif.read ? "ring-1 ring-primary/20" : "opacity-80"}`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`p-2 rounded-xl ${cfg.bg} shrink-0 mt-0.5`}>
                      <Icon className={`w-4 h-4 ${cfg.color}`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-sm font-semibold text-foreground">{notif.title}</span>
                        {!notif.read && (
                          <span className="w-2 h-2 rounded-full bg-primary shrink-0" />
                        )}
                        <span className={`ml-auto text-[10px] px-2 py-0.5 rounded-full border ${cfg.bg} ${cfg.color} ${cfg.border} font-medium shrink-0`}>
                          {notif.category}
                        </span>
                      </div>
                      <p className="text-xs text-muted-foreground leading-relaxed">{notif.message}</p>
                      <div className="flex items-center justify-between mt-2">
                        <span className="text-[10px] text-muted-foreground/60">{notif.time}</span>
                        <button
                          onClick={e => { e.stopPropagation(); dismiss(notif.id); }}
                          className="p-1 rounded-lg hover:bg-muted text-muted-foreground hover:text-danger transition-colors"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </div>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
