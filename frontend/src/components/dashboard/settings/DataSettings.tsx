import { Download, RefreshCw, Database, Trash2 } from "lucide-react";

export function DataSettings() {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-foreground mb-4">Data Management</h3>
        <div className="space-y-3">
          <button className="w-full flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20 hover:bg-muted/40 transition-colors">
            <div className="flex items-center gap-3">
              <Download className="w-5 h-5 text-primary" />
              <div className="text-left">
                <div className="text-sm font-semibold text-foreground">Export All Data</div>
                <div className="text-xs text-muted-foreground">Download your complete financial data</div>
              </div>
            </div>
            <span className="text-xs text-muted-foreground">JSON</span>
          </button>

          <button className="w-full flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20 hover:bg-muted/40 transition-colors">
            <div className="flex items-center gap-3">
              <RefreshCw className="w-5 h-5 text-primary" />
              <div className="text-left">
                <div className="text-sm font-semibold text-foreground">Sync Data</div>
                <div className="text-xs text-muted-foreground">Refresh from connected accounts</div>
              </div>
            </div>
            <span className="text-xs text-success">Active</span>
          </button>

          <button className="w-full flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20 hover:bg-muted/40 transition-colors">
            <div className="flex items-center gap-3">
              <Database className="w-5 h-5 text-primary" />
              <div className="text-left">
                <div className="text-sm font-semibold text-foreground">Storage Usage</div>
                <div className="text-xs text-muted-foreground">2.4 MB of 100 MB used</div>
              </div>
            </div>
            <span className="text-xs text-muted-foreground">2.4%</span>
          </button>
        </div>
      </div>

      <div className="pt-6 border-t border-border">
        <h3 className="text-lg font-semibold text-foreground mb-4 text-danger">Danger Zone</h3>
        <div className="space-y-3">
          <button className="w-full flex items-center gap-3 p-4 rounded-xl border-2 border-danger/20 bg-danger/5 hover:bg-danger/10 transition-colors">
            <Trash2 className="w-5 h-5 text-danger" />
            <div className="text-left">
              <div className="text-sm font-semibold text-danger">Clear All Data</div>
              <div className="text-xs text-muted-foreground">Permanently delete all your financial data</div>
            </div>
          </button>

          <button className="w-full flex items-center gap-3 p-4 rounded-xl border-2 border-danger/20 bg-danger/5 hover:bg-danger/10 transition-colors">
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
