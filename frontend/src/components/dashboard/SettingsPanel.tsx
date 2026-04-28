import { useState } from "react";
import { motion } from "framer-motion";
import { 
  User, Bell, Shield, Palette, Globe, Database, 
  Download, Trash2, Lock, Eye, EyeOff, Save, 
  RefreshCw, Mail, Smartphone, Moon, Sun, Monitor,
  DollarSign, Calendar, TrendingUp, AlertCircle
} from "lucide-react";

interface SettingsSection {
  id: string;
  title: string;
  icon: any;
}

const sections: SettingsSection[] = [
  { id: "profile", title: "Profile", icon: User },
  { id: "notifications", title: "Notifications", icon: Bell },
  { id: "security", title: "Security & Privacy", icon: Shield },
  { id: "appearance", title: "Appearance", icon: Palette },
  { id: "preferences", title: "Preferences", icon: Globe },
  { id: "data", title: "Data & Storage", icon: Database },
];

export default function SettingsPanel() {
  const [activeSection, setActiveSection] = useState("profile");
  const [showPassword, setShowPassword] = useState(false);
  const [theme, setTheme] = useState<"light" | "dark" | "system">("system");
  const [currency, setCurrency] = useState("INR");
  const [language, setLanguage] = useState("en");
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    sms: false,
    alerts: true,
    recommendations: true,
    reports: false,
  });

  const [profile, setProfile] = useState({
    name: "Imayavarman",
    email: "imayavarman@example.com",
    phone: "+91 1111111111",
    occupation: "Software Engineer",
    location: "Chennai, India",
  });

  const handleSave = () => {
    // Save settings logic here
    alert("Settings saved successfully!");
  };

  const renderSection = () => {
    switch (activeSection) {
      case "profile":
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Profile Information</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Full Name</label>
                  <input
                    type="text"
                    value={profile.name}
                    onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                    className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Email</label>
                  <input
                    type="email"
                    value={profile.email}
                    onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                    className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Phone</label>
                  <input
                    type="tel"
                    value={profile.phone}
                    onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                    className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Occupation</label>
                  <input
                    type="text"
                    value={profile.occupation}
                    onChange={(e) => setProfile({ ...profile, occupation: e.target.value })}
                    className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Location</label>
                  <input
                    type="text"
                    value={profile.location}
                    onChange={(e) => setProfile({ ...profile, location: e.target.value })}
                    className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>
              </div>
            </div>
          </div>
        );

      case "notifications":
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

      case "security":
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

      case "appearance":
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Theme</h3>
              <div className="grid grid-cols-3 gap-3">
                <button
                  onClick={() => setTheme("light")}
                  className={`p-4 rounded-xl border-2 transition-all ${
                    theme === "light" ? "border-primary bg-primary/10" : "border-border bg-muted/20"
                  }`}
                >
                  <Sun className="w-6 h-6 mx-auto mb-2 text-foreground" />
                  <div className="text-sm font-semibold text-foreground">Light</div>
                </button>
                <button
                  onClick={() => setTheme("dark")}
                  className={`p-4 rounded-xl border-2 transition-all ${
                    theme === "dark" ? "border-primary bg-primary/10" : "border-border bg-muted/20"
                  }`}
                >
                  <Moon className="w-6 h-6 mx-auto mb-2 text-foreground" />
                  <div className="text-sm font-semibold text-foreground">Dark</div>
                </button>
                <button
                  onClick={() => setTheme("system")}
                  className={`p-4 rounded-xl border-2 transition-all ${
                    theme === "system" ? "border-primary bg-primary/10" : "border-border bg-muted/20"
                  }`}
                >
                  <Monitor className="w-6 h-6 mx-auto mb-2 text-foreground" />
                  <div className="text-sm font-semibold text-foreground">System</div>
                </button>
              </div>
            </div>

            <div className="pt-6 border-t border-border">
              <h3 className="text-lg font-semibold text-foreground mb-4">Display Options</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20">
                  <div>
                    <div className="text-sm font-semibold text-foreground">Compact Mode</div>
                    <div className="text-xs text-muted-foreground">Reduce spacing and padding</div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" />
                    <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
                  </label>
                </div>
                <div className="flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20">
                  <div>
                    <div className="text-sm font-semibold text-foreground">Animations</div>
                    <div className="text-xs text-muted-foreground">Enable smooth transitions</div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" defaultChecked className="sr-only peer" />
                    <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
                  </label>
                </div>
              </div>
            </div>
          </div>
        );

      case "preferences":
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Regional Settings</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Currency</label>
                  <select
                    value={currency}
                    onChange={(e) => setCurrency(e.target.value)}
                    className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  >
                    <option value="INR">₹ Indian Rupee (INR)</option>
                    <option value="USD">$ US Dollar (USD)</option>
                    <option value="EUR">€ Euro (EUR)</option>
                    <option value="GBP">£ British Pound (GBP)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Language</label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  >
                    <option value="en">English</option>
                    <option value="hi">हिन्दी (Hindi)</option>
                    <option value="ta">தமிழ் (Tamil)</option>
                    <option value="te">తెలుగు (Telugu)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Date Format</label>
                  <select className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary">
                    <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                    <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                    <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                  </select>
                </div>
              </div>
            </div>

            <div className="pt-6 border-t border-border">
              <h3 className="text-lg font-semibold text-foreground mb-4">Financial Preferences</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Default View</label>
                  <select className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary">
                    <option value="overview">Overview</option>
                    <option value="health">Financial Health</option>
                    <option value="savings">Savings</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Fiscal Year Start</label>
                  <select className="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary">
                    <option value="april">April (India)</option>
                    <option value="january">January</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        );

      case "data":
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

      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Settings Navigation */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {sections.map((section) => {
          const Icon = section.icon;
          return (
            <button
              key={section.id}
              onClick={() => setActiveSection(section.id)}
              className={`p-4 rounded-xl border-2 transition-all ${
                activeSection === section.id
                  ? "border-primary bg-primary/10"
                  : "border-border bg-muted/20 hover:bg-muted/40"
              }`}
            >
              <Icon className={`w-5 h-5 mx-auto mb-2 ${
                activeSection === section.id ? "text-primary" : "text-muted-foreground"
              }`} />
              <div className={`text-xs font-semibold ${
                activeSection === section.id ? "text-primary" : "text-foreground"
              }`}>
                {section.title}
              </div>
            </button>
          );
        })}
      </div>

      {/* Settings Content */}
      <motion.div
        key={activeSection}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="glass-card rounded-2xl p-6 border border-border"
      >
        {renderSection()}
      </motion.div>

      {/* Save Button */}
      <div className="flex justify-end gap-3">
        <button className="px-6 py-2 rounded-xl border border-border text-foreground font-semibold hover:bg-muted/40 transition-colors">
          Cancel
        </button>
        <button
          onClick={handleSave}
          className="px-6 py-2 rounded-xl gradient-primary text-white font-semibold hover:opacity-90 transition-opacity flex items-center gap-2"
        >
          <Save className="w-4 h-4" />
          Save Changes
        </button>
      </div>
    </div>
  );
}
