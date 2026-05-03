import { Search, Bell, Sun, Moon, LogOut, User, Mail, Briefcase, MapPin, Calendar, CreditCard, Shield } from "lucide-react";
import { useStore } from "@/store/useStore";
import { useNavigate } from "react-router-dom";
import { logout } from "@/lib/api";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { formatCurrency } from "@/lib/formatters";

export default function AppHeader() {
  const { currentUser, sessionId, isDark, setIsDark, setCurrentUser, setSessionId, notifications } = useStore();
  const navigate = useNavigate();
  const [profileOpen, setProfileOpen] = useState(false);

  const handleLogout = async () => {
    if (sessionId) { try { await logout(sessionId); } catch {} }
    setCurrentUser(null);
    setSessionId(null);
    navigate("/");
  };

  const handleNotificationClick = () => {
    navigate("/dashboard/alerts");
  };

  const unreadCount = 0; // notifications?.filter(n => !n.is_read).length || 0;

  return (
    <>
      <header
        className="h-16 border-b border-border flex items-center justify-between px-6 sticky top-0 z-20"
        style={{ background: "hsl(var(--background) / 0.80)", backdropFilter: "blur(24px)" }}
      >
        {/* Search */}
        <div className="flex items-center gap-3 flex-1 max-w-lg">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
            <input
              placeholder="Search assets, transactions, reports..."
              className="w-full pl-9 pr-4 py-2 bg-secondary/60 rounded-xl text-xs text-foreground placeholder:text-muted-foreground border border-border focus:outline-none focus:border-primary/50 focus:bg-secondary transition-all"
            />
          </div>
        </div>

        {/* Right */}
        <div className="flex items-center gap-1 ml-4">
          {/* Theme */}
          <button
            onClick={() => setIsDark(!isDark)}
            className="p-2 rounded-xl hover:bg-secondary text-muted-foreground hover:text-foreground transition-all"
            title={isDark ? "Switch to light mode" : "Switch to dark mode"}
          >
            {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>

          {/* Notifications */}
          <button 
            onClick={handleNotificationClick}
            className="relative p-2 rounded-xl hover:bg-secondary text-muted-foreground hover:text-foreground transition-all"
            title="View notifications"
          >
            <Bell className="w-4 h-4" />
            {unreadCount > 0 && (
              <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-danger rounded-full ring-1 ring-background" />
            )}
          </button>

          {/* Divider */}
          <div className="w-px h-6 bg-border mx-2" />

          {/* User */}
          {currentUser && (
            <button
              onClick={() => setProfileOpen(true)}
              className="flex items-center gap-2.5 p-1.5 rounded-xl hover:bg-secondary transition-all"
            >
              <div className="relative shrink-0">
                <img src={currentUser.avatar} alt="" className="w-8 h-8 rounded-lg ring-1 ring-border" />
                <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-success rounded-full ring-2 ring-background" />
              </div>
              <div className="hidden sm:block text-left">
                <div className="text-xs font-semibold text-foreground leading-none mb-0.5">{currentUser.name}</div>
                <div className="text-[10px] text-muted-foreground leading-none">{currentUser.occupation}</div>
              </div>
            </button>
          )}
        </div>
      </header>

      {/* User Profile Sidebar */}
      <AnimatePresence>
        {profileOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 bg-background/80 backdrop-blur-sm z-[60]"
              onClick={() => {
                console.log("Backdrop clicked");
                setProfileOpen(false);
              }}
            />

            {/* Sidebar */}
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              className="fixed right-0 top-0 h-full w-[380px] bg-card border-l border-border shadow-2xl z-[70] overflow-y-auto"
            >
              {currentUser && (
                <div className="p-6">
                  {/* Header */}
                  <motion.div 
                    className="flex items-start justify-between mb-6"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1, duration: 0.5 }}
                  >
                    <div>
                      <h2 className="text-lg font-bold text-foreground mb-1">Profile</h2>
                      <p className="text-xs text-muted-foreground">Your account information</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        console.log("Close button clicked");
                        setProfileOpen(false);
                      }}
                      className="p-2 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground transition-all cursor-pointer"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </motion.div>

                  {/* Avatar & Name */}
                  <motion.div 
                    className="flex flex-col items-center mb-6 pb-6 border-b border-border pointer-events-auto"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.2, type: "spring", stiffness: 300 }}
                  >
                    <motion.div 
                      className="relative mb-4"
                      whileHover={{ scale: 1.05 }}
                      transition={{ type: "spring", stiffness: 400 }}
                    >
                      <img src={currentUser.avatar} alt="" className="w-20 h-20 rounded-2xl ring-2 ring-border" />
                      <motion.span 
                        className="absolute -bottom-1 -right-1 w-4 h-4 bg-success rounded-full ring-2 ring-card"
                        animate={{ scale: [1, 1.2, 1] }}
                        transition={{ duration: 2, repeat: Infinity }}
                      />
                    </motion.div>
                    <motion.h3 
                      className="text-lg font-bold text-foreground mb-1"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.3, duration: 0.5 }}
                    >
                      {currentUser.name}
                    </motion.h3>
                    <motion.p 
                      className="text-sm text-muted-foreground mb-3"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.35, duration: 0.5 }}
                    >
                      {currentUser.occupation}
                    </motion.p>
                    <motion.div 
                      className="flex items-center gap-2"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.4, duration: 0.5 }}
                    >
                      <motion.span 
                        className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          currentUser.riskLevel === "Low" ? "bg-success/10 text-success" :
                          currentUser.riskLevel === "Medium" ? "bg-warning/10 text-warning" :
                          "bg-danger/10 text-danger"
                        }`}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        {currentUser.riskLevel} Risk
                      </motion.span>
                      <motion.span 
                        className="px-3 py-1 rounded-full text-xs font-semibold bg-primary/10 text-primary"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        {currentUser.personalityTag}
                      </motion.span>
                    </motion.div>
                  </motion.div>

                  {/* Details */}
                  <motion.div 
                    className="space-y-4 mb-6 pointer-events-auto"
                    initial="hidden"
                    animate="visible"
                    variants={{
                      hidden: { opacity: 0 },
                      visible: {
                        opacity: 1,
                        transition: {
                          staggerChildren: 0.08,
                          delayChildren: 0.5
                        }
                      }
                    }}
                  >
                    {[
                      { icon: Mail, label: "Email", value: currentUser.email, color: "primary" },
                      { icon: Briefcase, label: "Occupation", value: currentUser.occupation, color: "success" },
                      ...(currentUser.location ? [{ icon: MapPin, label: "Location", value: currentUser.location, color: "warning" }] : []),
                      ...(currentUser.age ? [{ icon: Calendar, label: "Age", value: `${currentUser.age} years`, color: "primary" }] : [])
                    ].map((item, index) => (
                      <motion.div 
                        key={index}
                        className="flex items-center gap-3 p-3 rounded-xl bg-secondary/50 pointer-events-auto"
                        variants={{
                          hidden: { opacity: 0, x: -20 },
                          visible: { opacity: 1, x: 0 }
                        }}
                        whileHover={{ x: 4, backgroundColor: "hsl(var(--secondary) / 0.7)" }}
                        transition={{ type: "spring", stiffness: 400 }}
                      >
                        <motion.div 
                          className={`p-2 rounded-lg bg-${item.color}/10`}
                          whileHover={{ rotate: 5, scale: 1.1 }}
                        >
                          <item.icon className={`w-4 h-4 text-${item.color}`} />
                        </motion.div>
                        <motion.div 
                          className="flex-1 min-w-0"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 0.1, duration: 0.5 }}
                        >
                          <div className="text-[10px] text-muted-foreground uppercase tracking-wider mb-0.5">{item.label}</div>
                          <div className="text-xs font-medium text-foreground truncate">{item.value}</div>
                        </motion.div>
                      </motion.div>
                    ))}
                  </motion.div>

                  {/* Financial Summary */}
                  <motion.div 
                    className="mb-6 p-4 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 border border-primary/20 pointer-events-auto"
                    initial={{ opacity: 0, y: 20, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    transition={{ delay: 0.7, type: "spring", stiffness: 300, duration: 0.5 }}
                    whileHover={{ scale: 1.02 }}
                  >
                    <motion.h4 
                      className="text-xs font-semibold text-foreground mb-3 flex items-center gap-2"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.75, duration: 0.5 }}
                    >
                      <CreditCard className="w-3.5 h-3.5" />
                      Financial Summary
                    </motion.h4>
                    <motion.div 
                      className="grid grid-cols-2 gap-3"
                      initial="hidden"
                      animate="visible"
                      variants={{
                        hidden: { opacity: 0 },
                        visible: {
                          opacity: 1,
                          transition: {
                            staggerChildren: 0.1,
                            delayChildren: 0.8
                          }
                        }
                      }}
                    >
                      {[
                        { label: "Net Worth", value: formatCurrency(currentUser.netWorth) },
                        { label: "Credit Score", value: currentUser.creditScore },
                        { label: "Monthly Income", value: formatCurrency(currentUser.monthlyIncome) },
                        { label: "Savings Rate", value: `${currentUser.savingsRate}%` }
                      ].map((item, index) => (
                        <motion.div
                          key={index}
                          variants={{
                            hidden: { opacity: 0, scale: 0.8 },
                            visible: { opacity: 1, scale: 1 }
                          }}
                          whileHover={{ scale: 1.05 }}
                        >
                          <div className="text-[10px] text-muted-foreground mb-1">{item.label}</div>
                          <div className="text-sm font-bold text-foreground">{item.value}</div>
                        </motion.div>
                      ))}
                    </motion.div>
                  </motion.div>

                  {/* Bank Info */}
                  {currentUser.bankName && (
                    <motion.div 
                      className="mb-6 p-4 rounded-xl bg-secondary/50 border border-border pointer-events-auto"
                      initial={{ opacity: 0, y: 20, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      transition={{ delay: 0.9, type: "spring", stiffness: 300, duration: 0.5 }}
                      whileHover={{ scale: 1.02 }}
                    >
                      <motion.h4 
                        className="text-xs font-semibold text-foreground mb-3 flex items-center gap-2"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.95, duration: 0.5 }}
                      >
                        <Shield className="w-3.5 h-3.5" />
                        Bank Account
                      </motion.h4>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-[10px] text-muted-foreground">Bank</span>
                          <span className="text-xs font-medium text-foreground">{currentUser.bankName}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-[10px] text-muted-foreground">Account</span>
                          <span className="text-xs font-medium text-foreground">{currentUser.accountNumber}</span>
                        </div>
                        {currentUser.accountType && (
                          <div className="flex justify-between">
                            <span className="text-[10px] text-muted-foreground">Type</span>
                            <span className="text-xs font-medium text-foreground">{currentUser.accountType}</span>
                          </div>
                        )}
                      </div>
                    </motion.div>
                  )}

                  {/* Actions */}
                  <div className="space-y-2 mt-6">
                    <button
                      type="button"
                      onClick={() => {
                        console.log("Edit Profile clicked");
                        setProfileOpen(false);
                        navigate("/dashboard/settings");
                      }}
                      className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-secondary hover:bg-secondary/80 text-foreground font-medium text-sm transition-all cursor-pointer"
                    >
                      <User className="w-4 h-4" />
                      Edit Profile
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        console.log("Sign Out clicked");
                        setProfileOpen(false);
                        handleLogout();
                      }}
                      className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-danger/10 hover:bg-danger/20 text-danger font-medium text-sm transition-all cursor-pointer"
                    >
                      <LogOut className="w-4 h-4" />
                      Sign Out
                    </button>
                  </div>
                </div>
              )}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
