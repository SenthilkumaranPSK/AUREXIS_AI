export const formatCurrency = (amount: number, currency: 'INR' | 'USD' = 'INR'): string => {
  if (amount === undefined || amount === null || isNaN(amount)) return currency === 'INR' ? "₹0" : "$0";
  
  const sym = currency === 'INR' ? '₹' : '$';
  const locale = currency === 'INR' ? 'en-IN' : 'en-US';
  
  if (currency === 'USD') {
    if (amount >= 1000000) return `$${(amount / 1000000).toFixed(1)}M`;
    if (amount >= 1000) return `$${(amount / 1000).toFixed(1)}K`;
    return `$${amount.toLocaleString(locale)}`;
  }

  if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(1)}Cr`;
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(1)}L`;
  if (amount >= 1000) return `₹${(amount / 1000).toFixed(1)}K`;
  return `₹${amount.toLocaleString(locale)}`;
};

export const formatFullCurrency = (amount: number, currency: 'INR' | 'USD' = 'INR'): string => {
  if (amount === undefined || amount === null || isNaN(amount)) return currency === 'INR' ? "₹0" : "$0";
  const sym = currency === 'INR' ? '₹' : '$';
  const locale = currency === 'INR' ? 'en-IN' : 'en-US';
  return `${sym}${amount.toLocaleString(locale)}`;
};

export const getRiskColor = (risk: string): string => {
  switch (risk) {
    case "Low": return "text-success";
    case "Medium": return "text-warning";
    case "High": return "text-danger";
    case "Critical": return "text-danger";
    default: return "text-muted-foreground";
  }
};

export const getRiskBg = (risk: string): string => {
  switch (risk) {
    case "Low": return "bg-success/10 text-success border-success/20";
    case "Medium": return "bg-warning/10 text-warning border-warning/20";
    case "High": return "bg-danger/10 text-danger border-danger/20";
    case "Critical": return "bg-danger/10 text-danger border-danger/20";
    default: return "bg-muted text-muted-foreground";
  }
};

export const getScoreColor = (score: number): string => {
  if (score >= 80) return "text-success";
  if (score >= 60) return "text-warning";
  return "text-danger";
};

export const getScoreGradient = (score: number): string => {
  if (score >= 80) return "from-success to-emerald-400";
  if (score >= 60) return "from-warning to-amber-400";
  return "from-danger to-red-400";
};
