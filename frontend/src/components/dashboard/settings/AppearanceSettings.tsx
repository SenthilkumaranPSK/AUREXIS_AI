import { Sun, Moon, Monitor } from "lucide-react";

interface AppearanceSettingsProps {
  theme: "light" | "dark" | "system";
  setTheme: (theme: "light" | "dark" | "system") => void;
}

export function AppearanceSettings({ theme, setTheme }: AppearanceSettingsProps) {
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
}
