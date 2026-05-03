import { useState } from "react";
import { Lock, Eye, EyeOff } from "lucide-react";

export function SecuritySettings() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-foreground mb-4">Security Settings</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-2">Current Password</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter current password"
                className="w-full px-4 py-2 pr-12 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <button
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-2">New Password</label>
            <input
              type="password"
              placeholder="Enter new password"
              className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-2">Confirm New Password</label>
            <input
              type="password"
              placeholder="Confirm new password"
              className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <button className="w-full px-4 py-2 rounded-xl bg-primary text-white font-semibold hover:opacity-90 transition-opacity">
            <Lock className="w-4 h-4 inline mr-2" />
            Change Password
          </button>
        </div>
      </div>

      <div className="pt-6 border-t border-border">
        <h3 className="text-lg font-semibold text-foreground mb-4">Two-Factor Authentication</h3>
        <div className="p-4 rounded-xl border border-border bg-muted/20">
          <div className="flex items-center justify-between mb-3">
            <div>
              <div className="text-sm font-semibold text-foreground">2FA Status</div>
              <div className="text-xs text-muted-foreground">Add an extra layer of security</div>
            </div>
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-warning/10 text-warning">
              Disabled
            </span>
          </div>
          <button className="w-full px-4 py-2 rounded-xl border border-primary text-primary font-semibold hover:bg-primary/10 transition-colors">
            Enable 2FA
          </button>
        </div>
      </div>
    </div>
  );
}
