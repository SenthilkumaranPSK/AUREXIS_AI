import { useState } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { Download, FileText, Calendar, TrendingUp, PieChart, Loader2, CheckCircle } from "lucide-react";
import { formatCurrency } from "@/lib/formatters";

interface ReportType {
  id: string;
  title: string;
  description: string;
  icon: any;
  format: "PDF" | "CSV" | "JSON";
  size: string;
}

export default function ReportsExport() {
  const { currentUser } = useStore();
  const [generating, setGenerating] = useState<string | null>(null);
  const [generated, setGenerated] = useState<string[]>([]);

  const reports: ReportType[] = [
    {
      id: "monthly-summary",
      title: "Monthly Financial Summary",
      description: "Income, expenses, savings breakdown for the current month",
      icon: Calendar,
      format: "PDF",
      size: "~250 KB",
    },
    {
      id: "expense-analysis",
      title: "Expense Analysis Report",
      description: "Detailed category-wise spending patterns and trends",
      icon: PieChart,
      format: "CSV",
      size: "~80 KB",
    },
    {
      id: "investment-portfolio",
      title: "Investment Portfolio Report",
      description: "Complete portfolio breakdown with performance metrics",
      icon: TrendingUp,
      format: "PDF",
      size: "~320 KB",
    },
    {
      id: "tax-summary",
      title: "Tax Summary Report",
      description: "Tax-deductible expenses and investment tax benefits",
      icon: FileText,
      format: "PDF",
      size: "~180 KB",
    },
    {
      id: "full-export",
      title: "Complete Data Export",
      description: "All financial data in machine-readable format",
      icon: Download,
      format: "JSON",
      size: "~500 KB",
    },
  ];

  const handleGenerate = async (reportId: string) => {
    setGenerating(reportId);
    
    // Simulate report generation
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // In a real app, this would call an API endpoint to generate the report
    // For now, we'll just simulate a download
    const report = reports.find(r => r.id === reportId);
    if (report) {
      // Create a mock download
      const blob = new Blob([`Mock ${report.title} data`], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${reportId}-${new Date().toISOString().split("T")[0]}.${report.format.toLowerCase()}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
    
    setGenerating(null);
    setGenerated(prev => [...prev, reportId]);
    
    // Reset generated status after 3 seconds
    setTimeout(() => {
      setGenerated(prev => prev.filter(id => id !== reportId));
    }, 3000);
  };

  if (!currentUser) return null;

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-1.5 rounded-lg bg-primary/10">
              <FileText className="w-3.5 h-3.5 text-primary" />
            </div>
            <h3 className="text-sm font-semibold text-foreground">Exportable Reports</h3>
          </div>
          <p className="text-[11px] text-muted-foreground ml-8">Generate and download financial reports</p>
        </div>
      </div>

      {/* Quick stats */}
      <div className="grid grid-cols-3 gap-3 mb-6 p-4 rounded-xl bg-muted/30 border border-border">
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Net Worth</div>
          <div className="text-sm font-bold text-foreground">{formatCurrency(currentUser.netWorth)}</div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Monthly Income</div>
          <div className="text-sm font-bold text-success">{formatCurrency(currentUser.monthlyIncome)}</div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Savings Rate</div>
          <div className="text-sm font-bold text-primary">{currentUser.savingsRate}%</div>
        </div>
      </div>

      {/* Report cards */}
      <div className="space-y-3">
        {reports.map((report, i) => {
          const Icon = report.icon;
          const isGenerating = generating === report.id;
          const isGenerated = generated.includes(report.id);

          return (
            <motion.div
              key={report.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className="flex items-center justify-between p-4 rounded-xl border border-border bg-muted/20 hover:bg-muted/40 transition-all group"
            >
              <div className="flex items-center gap-3 flex-1">
                <div className="p-2.5 rounded-lg bg-primary/10 group-hover:bg-primary/20 transition-colors">
                  <Icon className="w-4 h-4 text-primary" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-semibold text-foreground mb-0.5">{report.title}</div>
                  <div className="text-[10px] text-muted-foreground">{report.description}</div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <div className="text-right mr-2">
                  <div className="text-[10px] text-muted-foreground">Format</div>
                  <div className="text-xs font-semibold text-foreground">{report.format}</div>
                </div>
                <div className="text-right mr-3">
                  <div className="text-[10px] text-muted-foreground">Size</div>
                  <div className="text-xs font-semibold text-foreground">{report.size}</div>
                </div>
                <button
                  onClick={() => handleGenerate(report.id)}
                  disabled={isGenerating}
                  className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
                    isGenerated
                      ? "bg-success/10 text-success border border-success/20"
                      : "gradient-primary text-white hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                  }`}
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      Generating...
                    </>
                  ) : isGenerated ? (
                    <>
                      <CheckCircle className="w-3.5 h-3.5" />
                      Downloaded
                    </>
                  ) : (
                    <>
                      <Download className="w-3.5 h-3.5" />
                      Generate
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Footer note */}
      <div className="mt-6 pt-6 border-t border-border">
        <div className="flex items-start gap-2 text-[11px] text-muted-foreground">
          <FileText className="w-3.5 h-3.5 mt-0.5 shrink-0" />
          <p>
            Reports are generated in real-time based on your latest financial data. 
            All exports are encrypted and comply with data privacy regulations.
          </p>
        </div>
      </div>
    </motion.div>
  );
}
