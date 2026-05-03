import { useState, useEffect, ElementType } from "react";
import { useStore } from "@/store/useStore";
import { motion } from "framer-motion";
import { 
  User, Bell, Shield, Palette, Globe, Database, Save
} from "lucide-react";

import { ProfileSettings } from "./settings/ProfileSettings";
import { NotificationSettings } from "./settings/NotificationSettings";
import { SecuritySettings } from "./settings/SecuritySettings";
import { AppearanceSettings } from "./settings/AppearanceSettings";
import { PreferenceSettings } from "./settings/PreferenceSettings";
import { DataSettings } from "./settings/DataSettings";

interface SettingsSection {
  id: string;
  title: string;
  icon: ElementType;
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

  const { currentUser, setCurrentUser } = useStore();

  const [profile, setProfile] = useState({
    name: currentUser?.name || "",
    email: currentUser?.email || "",
    phone: currentUser?.phone || "",
    occupation: currentUser?.occupation || "",
    location: currentUser?.location || "",
  });

  // Update profile when currentUser changes
  useEffect(() => {
    if (currentUser) {
      setProfile({
        name: currentUser.name || "",
        email: currentUser.email || "",
        phone: currentUser.phone || "",
        occupation: currentUser.occupation || "",
        location: currentUser.location || "",
      });
    }
  }, [currentUser]);

  const handleSave = async () => {
    try {
      // Here you would typically make an API call to save settings to the backend
      // await fetch("/api/user/settings", { method: "PUT", body: JSON.stringify({ profile, notifications, theme, currency, language }) });
      
      // Update local store
      if (currentUser) {
        setCurrentUser({
          ...currentUser,
          name: profile.name,
          email: profile.email,
          phone: profile.phone,
          occupation: profile.occupation,
          location: profile.location,
        });
      }
      alert("Settings saved successfully!");
    } catch (error) {
      console.error("Failed to save settings:", error);
      alert("Failed to save settings. Please try again.");
    }
  };

  const renderSection = () => {
    switch (activeSection) {
      case "profile":
        return <ProfileSettings profile={profile} setProfile={setProfile} />;
      case "notifications":
        return <NotificationSettings notifications={notifications} setNotifications={setNotifications} />;
      case "security":
        return <SecuritySettings />;
      case "appearance":
        return <AppearanceSettings theme={theme} setTheme={setTheme} />;
      case "preferences":
        return <PreferenceSettings currency={currency} setCurrency={setCurrency} language={language} setLanguage={setLanguage} />;
      case "data":
        return <DataSettings />;
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
