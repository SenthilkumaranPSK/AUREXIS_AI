import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { User, Mail, Phone, Briefcase, MapPin, Calendar, Edit2, Check, X, Camera, Shield, TrendingUp, Wallet, Heart, Loader2 } from "lucide-react";
import { toast } from "sonner";

export default function ProfilePage() {
  const { currentUser, setCurrentUser, currency } = useStore();
  const [editing, setEditing] = useState(false);
  const [saving, setSaving]   = useState(false);
  const [form, setForm]       = useState({
    name:       currentUser?.name       || "",
    email:      currentUser?.email      || "",
    phone:      currentUser?.phone      || "",
    occupation: currentUser?.occupation || "",
    location:   currentUser?.location   || "",
    age:        currentUser?.age        || 0,
  });

  useEffect(() => {
    if (currentUser) {
      setForm({
        name:       currentUser.name       || "",
        email:      currentUser.email      || "",
        phone:      currentUser.phone      || "",
        occupation: currentUser.occupation || "",
        location:   currentUser.location   || "",
        age:        currentUser.age        || 0,
      });
    }
  }, [currentUser]);

  const token = () => localStorage.getItem("access_token");

  const handleSave = async () => {
    setSaving(true);
    try {
      const res = await fetch("/api/user/profile", {
        method: "PUT",
        headers: { Authorization: `Bearer ${token()}`, "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (data.success) {
        // Update local store
        setCurrentUser({ ...currentUser!, ...form });
        toast.success("Profile updated successfully!");
        setEditing(false);
      } else {
        toast.error("Failed to update profile");
      }
    } catch (e) {
      toast.error("Network error. Changes saved locally.");
      setCurrentUser({ ...currentUser!, ...form });
      setEditing(false);
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setForm({
      name:       currentUser?.name       || "",
      email:      currentUser?.email      || "",
      phone:      currentUser?.phone      || "",
      occupation: currentUser?.occupation || "",
      location:   currentUser?.location   || "",
      age:        currentUser?.age        || 0,
    });
    setEditing(false);
  };

  if (!currentUser) return null;

  const stats = [
    { label: "Net Worth",     value: formatCurrency(currentUser.netWorth || 0, currency),      icon: Wallet,    color: "text-primary"  },
    { label: "Health Score",  value: `${currentUser.financialHealthScore || 0}/100`,            icon: Heart,     color: "text-success"  },
    { label: "Credit Score",  value: `${currentUser.creditScore || 0}`,                         icon: Shield,    color: "text-warning"  },
    { label: "Savings Rate",  value: `${currentUser.savingsRate || 0}%`,                        icon: TrendingUp, color: "text-success" },
  ];

  const fields = [
    { key: "name",       label: "Full Name",   icon: User,      type: "text"   },
    { key: "email",      label: "Email",       icon: Mail,      type: "email"  },
    { key: "phone",      label: "Phone",       icon: Phone,     type: "tel"    },
    { key: "occupation", label: "Occupation",  icon: Briefcase, type: "text"   },
    { key: "location",   label: "Location",    icon: MapPin,    type: "text"   },
    { key: "age",        label: "Age",         icon: Calendar,  type: "number" },
  ] as const;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Profile header card */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
        className="glass-card rounded-2xl p-6 border border-border"
      >
        <div className="flex items-start gap-6">
          {/* Avatar */}
          <div className="relative shrink-0">
            <div className="w-20 h-20 rounded-2xl overflow-hidden border-2 border-primary/30">
              {currentUser.avatar ? (
                <img src={currentUser.avatar} alt={currentUser.name} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full gradient-primary flex items-center justify-center">
                  <span className="text-2xl font-bold text-white">
                    {currentUser.name?.split(" ").map(n => n[0]).join("").slice(0, 2).toUpperCase()}
                  </span>
                </div>
              )}
            </div>
            <div className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-success border-2 border-background flex items-center justify-center">
              <div className="w-2 h-2 rounded-full bg-white" />
            </div>
          </div>

          {/* Info */}
          <div className="flex-1">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-xl font-bold text-foreground">{currentUser.name}</h2>
                <p className="text-sm text-muted-foreground mt-0.5">{currentUser.occupation} · {currentUser.location}</p>
                <div className="flex items-center gap-2 mt-2">
                  <span className="px-2.5 py-1 rounded-full bg-primary/10 text-primary text-[11px] font-semibold border border-primary/20">
                    {currentUser.riskLevel || "Moderate"} Risk
                  </span>
                  <span className="px-2.5 py-1 rounded-full bg-success/10 text-success text-[11px] font-semibold border border-success/20">
                    {currentUser.personalityTag || "Balanced Planner"}
                  </span>
                </div>
              </div>
              {!editing ? (
                <button onClick={() => setEditing(true)}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl gradient-primary text-white text-xs font-semibold hover:opacity-90 transition-opacity"
                >
                  <Edit2 className="w-3.5 h-3.5" /> Edit Profile
                </button>
              ) : (
                <div className="flex items-center gap-2">
                  <button onClick={handleCancel}
                    className="flex items-center gap-1.5 px-3 py-2 rounded-xl border border-border text-muted-foreground text-xs font-semibold hover:bg-muted transition-colors"
                  >
                    <X className="w-3.5 h-3.5" /> Cancel
                  </button>
                  <button onClick={handleSave} disabled={saving}
                    className="flex items-center gap-1.5 px-4 py-2 rounded-xl gradient-primary text-white text-xs font-semibold hover:opacity-90 transition-opacity disabled:opacity-60"
                  >
                    {saving ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Check className="w-3.5 h-3.5" />}
                    Save Changes
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Financial stats */}
      <div className="grid grid-cols-4 gap-4">
        {stats.map((s, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.07 }}
            className="glass-card rounded-2xl p-4 border border-border text-center"
          >
            <div className={`p-2 rounded-xl bg-muted/40 w-fit mx-auto mb-2`}>
              <s.icon className={`w-4 h-4 ${s.color}`} />
            </div>
            <div className={`text-lg font-bold ${s.color}`}>{s.value}</div>
            <div className="text-[10px] text-muted-foreground mt-0.5">{s.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Profile fields */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
        className="glass-card rounded-2xl p-6 border border-border"
      >
        <h3 className="text-sm font-semibold text-foreground mb-5">Personal Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {fields.map(({ key, label, icon: Icon, type }) => (
            <div key={key}>
              <label className="block text-[11px] font-medium text-muted-foreground mb-1.5">{label}</label>
              <div className="relative">
                <Icon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  type={type}
                  value={form[key]}
                  onChange={e => setForm(prev => ({ ...prev, [key]: type === "number" ? parseInt(e.target.value) || 0 : e.target.value }))}
                  disabled={!editing}
                  className={`w-full pl-9 pr-4 py-2.5 rounded-xl border text-sm transition-all outline-none ${
                    editing
                      ? "border-primary/40 bg-background text-foreground focus:ring-2 focus:ring-primary/20"
                      : "border-border bg-muted/20 text-foreground cursor-default"
                  }`}
                />
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Account info (read-only) */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
        className="glass-card rounded-2xl p-6 border border-border"
      >
        <h3 className="text-sm font-semibold text-foreground mb-5">Account Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            { label: "Account Number", value: currentUser.accountNumber || "•••• ••••" },
            { label: "Bank",           value: currentUser.bankName      || "N/A"       },
            { label: "Account Type",   value: currentUser.accountType   || "Savings"   },
            { label: "Bank Location",  value: currentUser.bankLocation  || "N/A"       },
          ].map(({ label, value }) => (
            <div key={label}>
              <label className="block text-[11px] font-medium text-muted-foreground mb-1.5">{label}</label>
              <div className="px-4 py-2.5 rounded-xl border border-border bg-muted/20 text-sm text-foreground">
                {value}
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
