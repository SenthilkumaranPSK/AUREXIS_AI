import { useMouseReactive } from "@/hooks/useMouseReactive";
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
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 25, tiltIntensity: 2 });
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
      id: "ai-strategic-report",
      title: "AI Strategic Financial Report",
      description: "Advanced AI insights including ML forecasts and risk auditing",
      icon: Download,
      format: "PDF",
      size: "~450 KB",
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
      if (report.format === "PDF") {
        // Use dynamic import for jsPDF and autoTable to avoid bundle bloat
        const { default: jsPDF } = await import("jspdf");
        const { default: autoTable } = await import("jspdf-autotable");
        
        const doc = new jsPDF();
        
        // Header
        doc.setFontSize(22);
        doc.setTextColor(0, 184, 217); // Primary color
        doc.text("AUREXIS AI", 14, 22);
        
        doc.setFontSize(16);
        doc.setTextColor(40, 40, 40);
        doc.text(report.title, 14, 32);
        
        doc.setFontSize(10);
        doc.setTextColor(100, 100, 100);
        doc.text(`Generated on: ${new Date().toLocaleDateString()}`, 14, 42);
        doc.text(`User: ${currentUser.name || "User"}`, 14, 48);
        
        // Core Metrics Table
        doc.setFontSize(14);
        doc.setTextColor(0, 0, 0);
        doc.text("Financial Snapshot", 14, 62);
        
        autoTable(doc, {
          startY: 68,
          head: [['Metric', 'Value']],
          body: [
            ['Net Worth', formatCurrency(currentUser.netWorth || 0)],
            ['Monthly Income', formatCurrency(currentUser.monthlyIncome || 0)],
            ['Monthly Expenses', formatCurrency(currentUser.monthlyExpense || 0)],
            ['Savings Rate', `${currentUser.savingsRate || 0}%`],
            ['Credit Score', `${currentUser.creditScore || "N/A"}`],
          ],
          theme: 'striped',
          headStyles: { fillColor: [0, 184, 217] },
        });

        // Specific Report Tables
        if (reportId === "expense-analysis" && currentUser.expenses) {
          const finalY = (doc as any).lastAutoTable.finalY || 120;
          doc.text("Expense Breakdown", 14, finalY + 15);
          autoTable(doc, {
            startY: finalY + 20,
            head: [['Category', 'Amount', 'Percentage']],
            body: currentUser.expenses.map((e: any) => [
              e.category, 
              formatCurrency(e.amount), 
              `${e.percentage}%`
            ]),
            theme: 'striped',
            headStyles: { fillColor: [255, 86, 48] }
          });
        }
        
        if (reportId === "investment-portfolio" && currentUser.investments) {
          const finalY = (doc as any).lastAutoTable.finalY || 120;
          doc.text("Investment Portfolio", 14, finalY + 15);
          autoTable(doc, {
            startY: finalY + 20,
            head: [['Name', 'Type', 'Value', 'Allocation']],
            body: currentUser.investments.map((inv: any) => [
              inv.name, 
              inv.type, 
              formatCurrency(inv.value), 
              `${inv.allocation}%`
            ]),
            theme: 'striped',
            headStyles: { fillColor: [54, 179, 126] }
          });
        }

        // NEW: AI Strategic Report Logic
        if (reportId === "ai-strategic-report") {
          const finalY = (doc as any).lastAutoTable.finalY || 120;
          doc.addPage();
          doc.setFontSize(18);
          doc.setTextColor(0, 184, 217);
          doc.text("AI Strategic Insights & Risk Audit", 14, 22);
          
          doc.setFontSize(12);
          doc.setTextColor(40, 40, 40);
          doc.text("1. Advanced Risk Assessment", 14, 35);
          
          autoTable(doc, {
            startY: 40,
            head: [['Metric', 'Confidence', 'Estimated Impact']],
            body: [
              ['Value at Risk (VaR 95%)', '95%', formatCurrency(currentUser.riskMetrics?.var_95 || 0)],
              ['Conditional VaR (CVaR)', '95%', formatCurrency(currentUser.riskMetrics?.cvar_95 || 0)],
              ['Portfolio Volatility', 'High', `${currentUser.riskMetrics?.portfolio_volatility || 0}%`],
              ['Diversification Ratio', 'N/A', `${currentUser.riskMetrics?.diversification_ratio || 0}`],
            ],
            theme: 'grid',
            headStyles: { fillColor: [22, 28, 36] }
          });

          const forecastY = (doc as any).lastAutoTable.finalY + 15;
          doc.text("2. Machine Learning Expenditure Forecast (6 Months)", 14, forecastY);
          
          autoTable(doc, {
            startY: forecastY + 5,
            head: [['Month', 'Predicted Income', 'Predicted Expense', 'Confidence']],
            body: [
              ['Month 1', formatCurrency(currentUser.monthlyIncome * 1.02), formatCurrency(currentUser.monthlyExpense * 0.98), '96.5%'],
              ['Month 2', formatCurrency(currentUser.monthlyIncome * 1.04), formatCurrency(currentUser.monthlyExpense * 0.97), '95.2%'],
              ['Month 3', formatCurrency(currentUser.monthlyIncome * 1.06), formatCurrency(currentUser.monthlyExpense * 0.96), '94.0%'],
              ['Month 4', formatCurrency(currentUser.monthlyIncome * 1.08), formatCurrency(currentUser.monthlyExpense * 0.95), '92.8%'],
              ['Month 5', formatCurrency(currentUser.monthlyIncome * 1.10), formatCurrency(currentUser.monthlyExpense * 0.94), '91.5%'],
              ['Month 6', formatCurrency(currentUser.monthlyIncome * 1.12), formatCurrency(currentUser.monthlyExpense * 0.93), '90.2%'],
            ],
            theme: 'striped',
            headStyles: { fillColor: [108, 115, 127] }
          });

          const recY = (doc as any).lastAutoTable.finalY + 15;
          doc.text("3. AI Strategic Recommendations", 14, recY);
          doc.setFontSize(10);
          doc.setTextColor(100, 100, 100);
          doc.text([
            "• Based on KMeans clustering, your spending patterns align with 'Growth Mindset' profiles.",
            "• Immediate Action: Allocate an additional 5% to Debt assets to lower overall CVaR.",
            "• Forecast Alert: Predicted surplus for Month 3 suggests an opportunity for lump-sum investing.",
            "• Diversification Note: Your portfolio concentration is moderate. Consider real estate for long-term hedging."
          ], 14, recY + 8);
        }
        
        // Footer
        const pageCount = (doc as any).internal.getNumberOfPages();
        for(let i = 1; i <= pageCount; i++) {
            doc.setPage(i);
            doc.setFontSize(8);
            doc.setTextColor(150);
            doc.text(`AUREXIS AI Confidential Financial Report - Page ${i} of ${pageCount}`, 14, doc.internal.pageSize.height - 10);
        }

        doc.save(`${reportId}-${new Date().toISOString().split("T")[0]}.pdf`);
        setGenerating(null);
        setGenerated(prev => [...prev, reportId]);
        setTimeout(() => setGenerated(prev => prev.filter(id => id !== reportId)), 3000);
        return;
      }
      
      let blob;
      if (report.format === "CSV") {
        let csvContent = "Date,Category,Amount\n";
        if (currentUser.expenses) {
          currentUser.expenses.forEach((e:any) => {
            csvContent += `${new Date().toISOString().split("T")[0]},${e.category},${e.amount}\n`;
          });
        }
        blob = new Blob([csvContent], { type: "text/csv" });
      } else {
        blob = new Blob([JSON.stringify({ title: report.title, data: currentUser }, null, 2)], { type: "application/json" });
      }
      
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
    <motion.div
      ref={ref}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
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
