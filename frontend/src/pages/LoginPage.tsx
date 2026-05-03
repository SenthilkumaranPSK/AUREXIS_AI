import { useState } from "react";
import { motion } from "framer-motion";
import { useMouseReactive } from "@/hooks/useMouseReactive";
import { Brain, TrendingUp, Zap, Lock, BarChart3, Users, ArrowRight, CheckCircle2, Shield } from "lucide-react";
import { useStore } from "@/store/useStore";
import { useNavigate } from "react-router-dom";
import { login } from "@/lib/api";
import type { UserProfile } from "@/types/finance";

const features = [
  { icon: TrendingUp, label: "Risk Forecasting",   desc: "Predictive analysis" },
  { icon: Zap,        label: "Scenario Sim",        desc: "What-if modeling" },
  { icon: BarChart3,  label: "Investment Intel",    desc: "Smart allocation" },
  { icon: Shield,     label: "Secure & Local",      desc: "Your data stays yours" },
];

const trustBadges = ["Local AI Processing", "Explainable Insights", "Real-time Analysis"];

export default function LoginPage() {
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 40, tiltIntensity: 3 });
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");
  const [loading, setLoading]   = useState(false);
  const { setCurrentUser, setSessionId } = useStore();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    if (!username || !password) {
      setError("Please enter both username and password.");
      setLoading(false);
      return;
    }
    try {
      const response = await login({ username, password });
      const user = response.data?.user ?? response.user;
      const sessionId = response.data?.session_id ?? (user ? `session_${user.id}` : null);

      if (response.success && user && sessionId) {
        setCurrentUser(user as UserProfile);
        setSessionId(sessionId);
        navigate("/dashboard");
      } else {
        setError("Login failed. Please try again.");
      }
    } catch (err: any) {
      if (err.message?.includes("Failed to fetch") || err.message?.includes("NetworkError")) {
        setError("Cannot connect to backend. Make sure server.py is running on port 8000.");
      } else if (err.message?.includes("401")) {
        setError("Invalid credentials. Username and password must match.");
      } else {
        setError(err.message || "Unknown error");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex overflow-hidden">
      {/* Left panel */}
      <div className="hidden lg:flex lg:w-[46%] xl:w-[42%] flex-col justify-between p-12 xl:p-16 relative">
        <div className="relative z-10">
          {/* Logo */}
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="flex items-center gap-3 mb-14">
            <div className="w-11 h-11 rounded-2xl gradient-primary glow-primary flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="text-lg font-black text-foreground tracking-[0.15em]">AUREXIS</div>
              <div className="text-[10px] text-muted-foreground tracking-[0.3em] font-medium">AI FINANCE</div>
            </div>
          </motion.div>

          {/* Headline */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <h1 className="text-5xl xl:text-6xl font-black text-foreground leading-[1.05] mb-6">
              Your Financial<br />
              <span className="text-gradient">Intelligence</span><br />
              Command Center
            </h1>
            <p className="text-muted-foreground text-lg leading-relaxed max-w-md font-medium">
              AI-powered insights, real-time risk analysis, and personalized financial guidance — all running locally.
            </p>
          </motion.div>

          {/* Feature grid */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="grid grid-cols-2 gap-3 mt-12">
            {features.map((f, i) => (
              <div key={i} className="glass-card rounded-2xl p-5 border border-border hover:border-primary/30 transition-all group cursor-default">
                <div className="w-9 h-9 rounded-xl bg-primary/12 flex items-center justify-center mb-3 group-hover:bg-primary/18 transition-colors">
                  <f.icon className="w-4.5 h-4.5 text-primary" />
                </div>
                <div className="text-sm font-bold text-foreground">{f.label}</div>
                <div className="text-xs text-muted-foreground mt-1">{f.desc}</div>
              </div>
            ))}
          </motion.div>
        </div>

        {/* Trust badges */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }} className="relative z-10 flex flex-wrap gap-5">
          {trustBadges.map((b, i) => (
            <div key={i} className="flex items-center gap-2 text-xs text-muted-foreground font-medium">
              <CheckCircle2 className="w-4 h-4 text-success" />
              {b}
            </div>
          ))}
        </motion.div>
      </div>

      {/* Right panel */}
      <div className="flex-1 flex flex-col items-center justify-center p-6 lg:p-12 relative z-10">
        {/* Mobile logo */}
        <div className="lg:hidden flex items-center gap-3 mb-10">
          <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <span className="text-lg font-black text-foreground tracking-[0.15em]">AUREXIS</span>
        </div>

        <motion.div 
          ref={ref}
          style={{ x, y, rotateX, rotateY }}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          initial={{ opacity: 0, y: 20, scale: 0.98 }} 
          animate={{ opacity: 1, y: 0, scale: 1 }} 
          transition={{ duration: 0.4 }} 
          className="w-full max-w-[420px]"
        >
          <div className="glass-card rounded-3xl p-10 border border-border shadow-2xl">
            <div className="mb-8">
              <h2 className="text-3xl font-bold text-foreground mb-2">Welcome back</h2>
              <p className="text-sm text-muted-foreground">Sign in to your financial dashboard</p>
            </div>

            <form onSubmit={handleLogin} autoComplete="off" className="space-y-5">
              {/* Username */}
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Username</label>
                <div className="relative">
                  <Users className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground/50" />
                  <input
                    type="text"
                    placeholder="Enter your name"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    autoComplete="off"
                    className="w-full pl-11 pr-4 py-3.5 bg-secondary/60 border border-border rounded-xl text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-primary/60 focus:bg-secondary/80 transition-all font-medium"
                  />
                </div>
              </div>

              {/* Password */}
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Password</label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground/50" />
                  <input
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="new-password"
                    className="w-full pl-11 pr-4 py-3.5 bg-secondary/60 border border-border rounded-xl text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-primary/60 focus:bg-secondary/80 transition-all font-medium"
                  />
                </div>
              </div>

              {/* Error */}
              {error && (
                <motion.div initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }}
                  className="flex items-center gap-2 p-3.5 rounded-xl bg-danger/10 border border-danger/30 text-xs text-danger font-medium"
                >
                  <span className="w-2 h-2 rounded-full bg-danger shrink-0" />
                  {error}
                </motion.div>
              )}

              {/* Submit */}
              <button
                type="submit"
                disabled={loading}
                className="w-full py-4 mt-3 gradient-primary rounded-xl text-sm font-bold text-white flex items-center justify-center gap-2 hover:opacity-90 active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed glow-primary shadow-lg"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Authenticating...
                  </>
                ) : (
                  <>
                    Access Dashboard
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>
          </div>


        </motion.div>
      </div>
    </div>
  );
}
