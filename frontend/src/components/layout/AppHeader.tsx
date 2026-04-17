import { Search, Bell, Sun, Moon, LogOut } from "lucide-react";
import { useStore } from "@/store/useStore";
import { useNavigate } from "react-router-dom";
import { logout } from "@/lib/api";

export default function AppHeader() {
  const { currentUser, sessionId, isDark, setIsDark, setCurrentUser, setSessionId } = useStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    if (sessionId) { try { await logout(sessionId); } catch {} }
    setCurrentUser(null);
    setSessionId(null);
    navigate("/");
  };

  return (
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
        <button className="relative p-2 rounded-xl hover:bg-secondary text-muted-foreground hover:text-foreground transition-all">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-danger rounded-full ring-1 ring-background" />
        </button>

        {/* Divider */}
        <div className="w-px h-6 bg-border mx-2" />

        {/* User */}
        {currentUser && (
          <div className="flex items-center gap-2.5">
            <div className="relative shrink-0">
              <img src={currentUser.avatar} alt="" className="w-8 h-8 rounded-lg ring-1 ring-border" />
              <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-success rounded-full ring-2 ring-background" />
            </div>
            <div className="hidden sm:block">
              <div className="text-xs font-semibold text-foreground leading-none mb-0.5">{currentUser.name}</div>
              <div className="text-[10px] text-muted-foreground leading-none">{currentUser.occupation}</div>
            </div>
            <button
              onClick={handleLogout}
              className="p-1.5 rounded-lg hover:bg-danger/10 text-muted-foreground hover:text-danger transition-all ml-1"
              title="Sign out"
            >
              <LogOut className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
