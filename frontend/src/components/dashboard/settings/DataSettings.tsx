import { useState } from "react";
import { Download, RefreshCw, Database, Trash2, CheckCircle, Loader2 } from "lucide-react";
import { useStore } from "@/store/useStore";
import { toast } from "sonner";

export function DataSettings() {
  const { currentUser } = useStore();
  const [syncing, setSyncing] = useState(false);
  const [synced, setSynced] = useState(false);

  const handleExport = () => {
    const data = JSON.stringify({ user: currentUser, exportedAt: new Date().toISOString() }, null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `aurexis-data-${new Date().toISOString().split("T")[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success("Data exported successfully!");
  };

  const handleSync = async () => {
    setSyncing(true);
    await new Promise(r => setTimeout(r, 1500));
    setSyncing(false);
    setSynced(true);
    toast.success("Data synced successfully!");
    setTimeout(() => setSynced(false), 3000);
  };

  const handleClearData = () => {
    if (window.confirm("Are you sure? This will permanently delete all your financial data.")) {
      toast.error("Data cleared. Please log in again.");
      setTimeout(() => { localStorage.clear(); window.location.href = "/"; }, 1500);
    }
  };

  const handleDeleteAccount = () => {
    if (window.confirm("Are you absolutely sure? This cannot be undone.")) {
      toast.error("Account deleted.");
      setTimeout(() => { localStorage.clear(); window.location.href = "/"; }, 1500);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-foreground mb-4">Data Management</h3>
        <div className="space-y-3">
          <button
            onClick={handleExport}
            className="w-full flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20 hover:bg-muted/40 transition-colors"
          >
            <div className="flex items-center gap-3">
              <Download className="w-5 h-5 text-primary" />
              <div className="text-left">
                <div className="text-sm font-semibold text-foreground">Export All Data</div>
                <div className="text-xs text-muted-foreground">Download your complete financial data</div>
              </div>
            </div>
            <span className="text-xs text-muted-foreground">JSON</span>
          </button>

          <button
            onClick={handleSync}
            disabled={syncing}
            className="w-full flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20 hover:bg-muted/40 transition-colors disabled:opacity-60"
          >
            <div className="flex items-center gap-3">
              {syncing ? <Loader2 className="w-5 h-5 text-primary animate-spin" /> : synced ? <CheckCircle className="w-5 h-5 text-success" /> : <RefreshCw className="w-5 h-5 text-primary" />}
              <div className="text-left">
                <div className="text-sm font-semibold text-foreground">Sync Data</div>
                <div className="text-xs text-muted-foreground">{syncing ? "Syncing..." : synced ? "Synced!" : "Refresh from connected accounts"}</div>
              </div>
            </div>
            <span className={`text-xs ${synced ? "text-success" : "text-success"}`}>Active</span>
          </button>

          <div className="w-full flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20">
            <div className="flex items-center gap-3">
              <Database className="w-5 h-5 text-primary" />
              <div className="text-left">
                <div className="text-sm font-semibold text-foreground">Storage Usage</div>
                <div className="text-xs text-muted-foreground">2.4 MB of 100 MB used</div>
              </div>
            </div>
            <span className="text-xs text-muted-foreground">2.4%</span>
          </div>
        </div>
      </div>

      <div className="pt-6 border-t border-border">
        <h3 className="text-lg font-semibold text-foreground mb-4 text-danger">Danger Zone</h3>
        <div className="space-y-3">
          <button
            onClick={handleClearData}
            className="w-full flex items-center gap-3 p-4 rounded-xl border-2 border-danger/20 bg-danger/5 hover:bg-danger/10 transition-colors"
          >
            <Trash2 className="w-5 h-5 text-danger" />
            <div className="text-left">
              <div className="text-sm font-semibold text-danger">Clear All Data</div>
              <div className="text-xs text-muted-foreground">Permanently delete all your financial data</div>
            </div>
          </button>

          <button
            onClick={handleDeleteAccount}
            className="w-full flex items-center gap-3 p-4 rounded-xl border-2 border-danger/20 bg-danger/5 hover:bg-danger/10 transition-colors"
          >
            <Trash2 className="w-5 h-5 text-danger" />
            <div className="text-left">
              <div className="text-sm font-semibold text-danger">Delete Account</div>
              <div className="text-xs text-muted-foreground">Permanently delete your account and all data</div>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
}
