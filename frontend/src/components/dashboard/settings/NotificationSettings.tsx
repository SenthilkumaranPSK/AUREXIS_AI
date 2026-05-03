import { Mail, Bell, Smartphone, AlertCircle, TrendingUp, Calendar } from "lucide-react";

export interface NotificationType {
  email: boolean;
  push: boolean;
  sms: boolean;
  alerts: boolean;
  recommendations: boolean;
  reports: boolean;
}

interface NotificationSettingsProps {
  notifications: NotificationType;
  setNotifications: (notifications: NotificationType) => void;
}

export function NotificationSettings({ notifications, setNotifications }: NotificationSettingsProps) {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-foreground mb-4">Notification Preferences</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20">
            <div className="flex items-center gap-3">
              <Mail className="w-5 h-5 text-primary" />
              <div>
                <div className="text-sm font-semibold text-foreground">Email Notifications</div>
                <div className="text-xs text-muted-foreground">Receive updates via email</div>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={notifications.email}
                onChange={(e) => setNotifications({ ...notifications, email: e.target.checked })}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20">
            <div className="flex items-center gap-3">
              <Bell className="w-5 h-5 text-primary" />
              <div>
                <div className="text-sm font-semibold text-foreground">Push Notifications</div>
                <div className="text-xs text-muted-foreground">Browser push notifications</div>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={notifications.push}
                onChange={(e) => setNotifications({ ...notifications, push: e.target.checked })}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20">
            <div className="flex items-center gap-3">
              <Smartphone className="w-5 h-5 text-primary" />
              <div>
                <div className="text-sm font-semibold text-foreground">SMS Notifications</div>
                <div className="text-xs text-muted-foreground">Text message alerts</div>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={notifications.sms}
                onChange={(e) => setNotifications({ ...notifications, sms: e.target.checked })}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-primary" />
              <div>
                <div className="text-sm font-semibold text-foreground">Financial Alerts</div>
                <div className="text-xs text-muted-foreground">Budget limits, unusual spending</div>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={notifications.alerts}
                onChange={(e) => setNotifications({ ...notifications, alerts: e.target.checked })}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20">
            <div className="flex items-center gap-3">
              <TrendingUp className="w-5 h-5 text-primary" />
              <div>
                <div className="text-sm font-semibold text-foreground">Recommendations</div>
                <div className="text-xs text-muted-foreground">AI-powered financial advice</div>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={notifications.recommendations}
                onChange={(e) => setNotifications({ ...notifications, recommendations: e.target.checked })}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20">
            <div className="flex items-center gap-3">
              <Calendar className="w-5 h-5 text-primary" />
              <div>
                <div className="text-sm font-semibold text-foreground">Monthly Reports</div>
                <div className="text-xs text-muted-foreground">Automated monthly summaries</div>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={notifications.reports}
                onChange={(e) => setNotifications({ ...notifications, reports: e.target.checked })}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}
