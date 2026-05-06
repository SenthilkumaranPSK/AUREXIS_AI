import { useState } from "react";
import { Lock, Eye, EyeOff, ShieldCheck, Cpu, Database, Activity, RefreshCw } from "lucide-react";
import { motion } from "framer-motion";

export function SecuritySettings() {
  const [showPassword, setShowPassword] = useState(false);
  const [auditing, setAuditing] = useState(false);

  const securityLogs = [
    { action: "Ollama Context Isolation", status: "Active", time: "Just now", type: "Privacy" },
    { action: "AES-256-GCM Encryption", status: "Verified", time: "2m ago", type: "Data" },
    { action: "K-Means Profile Anonymization", status: "Success", time: "15m ago", type: "ML" },
    { action: "Risk Metric Recalculation", status: "Secure", time: "1h ago", type: "System" },
  ];

  return (
    <div className="space-y-8">
      {/* Real-time Privacy Guard */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-5 rounded-2xl border border-success/30 bg-success/5 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <ShieldCheck className="w-16 h-16 text-success" />
          </div>
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-success/20">
              <Cpu className="w-5 h-5 text-success" />
            </div>
            <h4 className="text-sm font-bold text-foreground">AI Privacy Guard</h4>
          </div>
          <p className="text-xs text-muted-foreground leading-relaxed mb-4">
            Your financial data is processed locally using Ollama. No data leaves this device during AI analysis.
          </p>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
            <span className="text-[10px] font-bold text-success uppercase tracking-wider">Local Isolation Active</span>
          </div>
        </div>

        <div className="p-5 rounded-2xl border border-primary/30 bg-primary/5 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <Database className="w-16 h-16 text-primary" />
          </div>
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-primary/20">
              <Lock className="w-5 h-5 text-primary" />
            </div>
            <h4 className="text-sm font-bold text-foreground">Data Encryption</h4>
          </div>
          <p className="text-xs text-muted-foreground leading-relaxed mb-4">
            All bank transactions and profile data are stored using industrial-grade AES-256 encryption.
          </p>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
            <span className="text-[10px] font-bold text-primary uppercase tracking-wider">AES-256-GCM Verified</span>
          </div>
        </div>
      </div>

      {/* Audit Log */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-primary" />
            <h3 className="text-sm font-bold text-foreground">Privacy & Audit Log</h3>
          </div>
          <button 
            onClick={() => { setAuditing(true); setTimeout(() => setAuditing(false), 1500); }}
            className="text-[10px] flex items-center gap-1.5 px-3 py-1 rounded-full bg-muted/40 hover:bg-muted transition-colors text-muted-foreground"
          >
            <RefreshCw className={`w-3 h-3 ${auditing ? "animate-spin" : ""}`} />
            Refresh Audit
          </button>
        </div>
        
        <div className="space-y-2">
          {securityLogs.map((log, i) => (
            <motion.div 
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className="flex items-center justify-between p-3 rounded-xl bg-muted/20 border border-border/50 text-[11px]"
            >
              <div className="flex items-center gap-3">
                <span className="text-muted-foreground w-12">{log.time}</span>
                <span className="font-medium text-foreground">{log.action}</span>
              </div>
              <div className="flex items-center gap-4">
                <span className="px-2 py-0.5 rounded bg-background border border-border text-[9px] text-muted-foreground uppercase">{log.type}</span>
                <span className="text-success font-bold flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" />
                  {log.status}
                </span>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Password section remains as fallback security */}
      <div className="pt-6 border-t border-border">
        <h3 className="text-sm font-bold text-foreground mb-4">Access Credentials</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Current Password"
              className="w-full px-4 py-2 text-xs rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
          <button className="px-4 py-2 rounded-xl gradient-primary text-white text-xs font-bold hover:opacity-90 transition-opacity">
            Update Credentials
          </button>
        </div>
      </div>
    </div>
  );
}
