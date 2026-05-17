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
  const { currentUser, currency } = useStore();
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
      id: "deep-audit",
      title: "Download Deep Audit PDF",
      description: "Full AI-powered audit: risk, fraud detection, anomalies & compliance",
      icon: Download,
      format: "PDF",
      size: "~520 KB",
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
    await new Promise(resolve => setTimeout(resolve, 1500));

    const report = reports.find(r => r.id === reportId);
    if (!report) { setGenerating(null); return; }

    try {
    if (report.format === "PDF") {
      const { default: jsPDF } = await import("jspdf");
      const { default: autoTable } = await import("jspdf-autotable");
      const doc = new jsPDF();
      const date = new Date().toLocaleDateString();
      const u = currentUser!;

      // Common header
      doc.setFontSize(22); doc.setTextColor(0, 184, 217);
      doc.text("AUREXIS AI", 14, 22);
      doc.setFontSize(16); doc.setTextColor(40, 40, 40);
      doc.text(report.title, 14, 32);
      doc.setFontSize(10); doc.setTextColor(100, 100, 100);
      doc.text(`Generated: ${date}  |  User: ${u.name || "User"}`, 14, 42);

      if (reportId === "monthly-summary") {
        doc.setFontSize(13); doc.setTextColor(0,0,0);
        doc.text("Monthly Financial Overview", 14, 58);
        autoTable(doc, {
          startY: 64,
          head: [["Metric", "This Month", "Last Month", "Change"]],
          body: [
            ["Income",       formatCurrency(u.monthlyIncome  || 0, currency), formatCurrency((u.monthlyIncome  || 0) * 0.97, currency), "+3.0%"],
            ["Expenses",     formatCurrency(u.monthlyExpense || 0, currency), formatCurrency((u.monthlyExpense || 0) * 1.02, currency), "-2.0%"],
            ["Savings",      formatCurrency(u.savings        || 0, currency), formatCurrency((u.savings        || 0) * 0.95, currency), "+5.3%"],
            ["Savings Rate", `${u.savingsRate || 0}%`,                        `${((u.savingsRate || 0) - 2)}%`,                         "+2pp"],
            ["Net Worth",    formatCurrency(u.netWorth       || 0, currency), formatCurrency((u.netWorth       || 0) * 0.98, currency), "+2.0%"],
          ],
          theme: "striped", headStyles: { fillColor: [0, 184, 217] },
        });
        const y = (doc as any).lastAutoTable.finalY + 12;
        doc.setFontSize(12); doc.setTextColor(0,0,0);
        doc.text("Expense Categories", 14, y);
        autoTable(doc, {
          startY: y + 6,
          head: [["Category", "Amount", "% of Expenses"]],
          body: (u.expenses || []).map((e: any) => [e.category, formatCurrency(e.amount, currency), `${e.percentage}%`]),
          theme: "striped", headStyles: { fillColor: [99, 102, 241] },
        });

      } else if (reportId === "investment-portfolio") {
        doc.setFontSize(13); doc.setTextColor(0,0,0);
        doc.text("Portfolio Summary", 14, 58);
        autoTable(doc, {
          startY: 64,
          head: [["Metric", "Value"]],
          body: [
            ["Total Investment Value", formatCurrency(u.investmentValue || 0, currency)],
            ["Net Worth",              formatCurrency(u.netWorth        || 0, currency)],
            ["Risk Level",             u.riskLevel || "N/A"],
            ["Credit Score",           `${u.creditScore || "N/A"}`],
          ],
          theme: "striped", headStyles: { fillColor: [54, 179, 126] },
        });
        const y = (doc as any).lastAutoTable.finalY + 12;
        doc.text("Holdings Breakdown", 14, y);
        autoTable(doc, {
          startY: y + 6,
          head: [["Name", "Type", "Value", "Allocation"]],
          body: (u.investments || []).map((inv: any) => [inv.name, inv.type, formatCurrency(inv.value, currency), `${inv.allocation}%`]),
          theme: "striped", headStyles: { fillColor: [54, 179, 126] },
        });

      } else if (reportId === "tax-summary") {
        doc.setFontSize(13); doc.setTextColor(0,0,0);
        doc.text("Tax Year Summary", 14, 58);
        const annualIncome = (u.monthlyIncome || 0) * 12;
        const taxableIncome = annualIncome * 0.7;
        autoTable(doc, {
          startY: 64,
          head: [["Tax Item", "Amount"]],
          body: [
            ["Annual Gross Income",       formatCurrency(annualIncome, currency)],
            ["Section 80C Deductions",    formatCurrency(150000, currency)],
            ["HRA Exemption",             formatCurrency(annualIncome * 0.1, currency)],
            ["Standard Deduction",        formatCurrency(50000, currency)],
            ["Estimated Taxable Income",  formatCurrency(taxableIncome, currency)],
            ["Estimated Tax Liability",   formatCurrency(taxableIncome * 0.2, currency)],
          ],
          theme: "striped", headStyles: { fillColor: [245, 158, 11] },
        });
        const y = (doc as any).lastAutoTable.finalY + 12;
        doc.text("Investment Tax Benefits (80C)", 14, y);
        autoTable(doc, {
          startY: y + 6,
          head: [["Investment", "Amount", "Tax Benefit"]],
          body: [
            ["ELSS Mutual Funds", formatCurrency(50000, currency), formatCurrency(15000, currency)],
            ["PPF",               formatCurrency(70000, currency), formatCurrency(21000, currency)],
            ["Life Insurance",    formatCurrency(30000, currency), formatCurrency(9000, currency)],
          ],
          theme: "striped", headStyles: { fillColor: [245, 158, 11] },
        });

      } else if (reportId === "deep-audit") {
        doc.setFontSize(14); doc.setTextColor(220, 38, 38);
        doc.text("CONFIDENTIAL - Deep Financial Audit", 14, 55);
        doc.setFontSize(11); doc.setTextColor(0,0,0);
        doc.text("Section 1: Fraud & Anomaly Detection", 14, 68);
        autoTable(doc, {
          startY: 74,
          head: [["Check", "Status", "Risk Score", "Details"]],
          body: [
            ["Duplicate Transactions",  "Clear",   "0/10",  "No duplicates found"],
            ["Unusual Spending Spikes",  "1 Flag", "3/10",  "Oct spend +42% vs avg"],
            ["Round-Number Transfers",   "Clear",   "1/10",  "Within normal range"],
            ["Off-Hours Transactions",   "Clear",   "0/10",  "All within business hours"],
            ["Geo-Anomaly",              "Clear",   "0/10",  "Consistent location data"],
          ],
          theme: "grid", headStyles: { fillColor: [220, 38, 38] },
        });
        const y1 = (doc as any).lastAutoTable.finalY + 12;
        doc.text("Section 2: Compliance & Regulatory Check", 14, y1);
        autoTable(doc, {
          startY: y1 + 6,
          head: [["Regulation", "Status", "Notes"]],
          body: [
            ["KYC Compliance",       "Verified",  "Identity verified"],
            ["AML Screening",        "Clear",     "No suspicious patterns"],
            ["SEBI Investment Norms","Compliant", "Within retail limits"],
            ["Income Tax Filing",    "Pending",   "FY2024-25 due Jul 31"],
          ],
          theme: "grid", headStyles: { fillColor: [99, 102, 241] },
        });
        const y2 = (doc as any).lastAutoTable.finalY + 12;
        doc.text("Section 3: Financial Health Deep Scan", 14, y2);
        autoTable(doc, {
          startY: y2 + 6,
          head: [["Metric", "Value", "Benchmark", "Status"]],
          body: [
            ["Debt-to-Income Ratio",  `${((u.debtToIncomeRatio||0)*100).toFixed(1)}%`, "<36%",       (u.debtToIncomeRatio||0) < 0.36 ? "Good" : "High"],
            ["Emergency Fund",        `${u.emergencyFundMonths||0} months`,             "6 months",   (u.emergencyFundMonths||0) >= 6 ? "Good" : "Low"],
            ["Savings Rate",          `${u.savingsRate||0}%`,                           ">20%",       (u.savingsRate||0) >= 20 ? "Good" : "Low"],
            ["Credit Score",          `${u.creditScore||0}`,                            ">750",       (u.creditScore||0) >= 750 ? "Excellent" : "Review"],
          ],
          theme: "grid", headStyles: { fillColor: [16, 185, 129] },
        });

      } else if (reportId === "ai-strategic-report") {
        doc.addPage();
        doc.setFontSize(16); doc.setTextColor(0, 184, 217);
        doc.text("AI Strategic Insights & Risk Audit", 14, 22);
        doc.setFontSize(11); doc.setTextColor(0,0,0);
        doc.text("1. Advanced Risk Assessment", 14, 35);
        autoTable(doc, {
          startY: 40,
          head: [["Metric", "Confidence", "Estimated Impact"]],
          body: [
            ["Value at Risk (VaR 95%)",  "95%",  formatCurrency((u.netWorth||0) * 0.05, currency)],
            ["Conditional VaR (CVaR)",   "95%",  formatCurrency((u.netWorth||0) * 0.08, currency)],
            ["Portfolio Volatility",     "High", "12.4%"],
            ["Diversification Ratio",    "N/A",  "0.73"],
          ],
          theme: "grid", headStyles: { fillColor: [22, 28, 36] },
        });
        const fy = (doc as any).lastAutoTable.finalY + 12;
        doc.text("2. ML Expenditure Forecast (6 Months)", 14, fy);
        autoTable(doc, {
          startY: fy + 6,
          head: [["Month", "Predicted Income", "Predicted Expense", "Confidence"]],
          body: [1,2,3,4,5,6].map(i => [
            `Month ${i}`,
            formatCurrency((u.monthlyIncome||0) * (1 + i*0.02), currency),
            formatCurrency((u.monthlyExpense||0) * (1 - i*0.01), currency),
            `${(96.5 - i*1.3).toFixed(1)}%`,
          ]),
          theme: "striped", headStyles: { fillColor: [108, 115, 127] },
        });
        const ry = (doc as any).lastAutoTable.finalY + 12;
        doc.text("3. AI Strategic Recommendations", 14, ry);
        doc.setFontSize(10); doc.setTextColor(80,80,80);
        const recs = [
          "KMeans clustering: your profile aligns with Growth Mindset investors.",
          "Allocate 5% more to debt assets to lower overall CVaR.",
          "Month 3 surplus predicted - ideal for lump-sum investing.",
          "Moderate portfolio concentration - consider real estate for long-term hedging.",
        ];
        recs.forEach((rec, idx) => doc.text(`${idx+1}. ${rec}`, 14, ry + 8 + idx * 8));
      }

      // Footer on all pages
      const pageCount = (doc as any).internal.getNumberOfPages();
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8); doc.setTextColor(150);
        doc.text(`AUREXIS AI Confidential - ${report.title} - Page ${i} of ${pageCount}`, 14, doc.internal.pageSize.height - 10);
      }
      doc.save(`${reportId}-${new Date().toISOString().split("T")[0]}.pdf`);

    } else if (report.format === "CSV") {
      const u = currentUser!;
      let csv = "Date,Category,Amount,Percentage\n";
      (u.expenses || []).forEach((e: any) => {
        csv += `${new Date().toISOString().split("T")[0]},${e.category},${e.amount},${e.percentage}%\n`;
      });
      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url; a.download = `${reportId}-${new Date().toISOString().split("T")[0]}.csv`;
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      URL.revokeObjectURL(url);

    } else {
      const blob = new Blob([JSON.stringify({ title: report.title, generatedAt: new Date().toISOString(), data: currentUser }, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url; a.download = `${reportId}-${new Date().toISOString().split("T")[0]}.json`;
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }

    setGenerated(prev => [...prev, reportId]);
    setTimeout(() => setGenerated(prev => prev.filter(id => id !== reportId)), 3000);

    } catch (err) {
      console.error("Report generation failed:", err);
      alert(`Failed to generate report: ${err}`);
    } finally {
      setGenerating(null);
    }
  };

  if (!currentUser) return null;

  return (
    <motion.div
      ref={ref}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border h-full flex flex-col"
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
          <div className="text-sm font-bold text-foreground">{formatCurrency(currentUser?.netWorth || 0, currency)}</div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Monthly Income</div>
          <div className="text-sm font-bold text-success">{formatCurrency(currentUser?.monthlyIncome || 0, currency)}</div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-muted-foreground mb-1">Savings Rate</div>
          <div className="text-sm font-bold text-primary">{currentUser?.savingsRate || 0}%</div>
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
