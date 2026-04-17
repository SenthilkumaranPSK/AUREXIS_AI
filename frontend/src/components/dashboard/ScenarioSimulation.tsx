import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { formatCurrency, formatFullCurrency } from "@/lib/formatters";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { FlaskConical, TrendingDown, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react";

export default function ScenarioSimulation() {
  const { currentUser, simulationParams, setSimulationParams } = useStore();
  if (!currentUser) return null;

  const { newLoanAmount, salaryIncrease, jobLoss, vacationExpense, housePurchase, carPurchase, investmentIncrease } = simulationParams;

  // Mock upcoming EMIs if not available
  const upcomingEMIs = currentUser.upcomingEMIs || [];

  // Simulation logic
  const newIncome = jobLoss ? 0 : currentUser.monthlyIncome * (1 + salaryIncrease / 100);
  const newExpense = currentUser.monthlyExpense + vacationExpense / 12 + (housePurchase ? 25000 : 0) + (carPurchase ? 15000 : 0);
  const newEMI = upcomingEMIs.reduce((s, e) => s + e.amount, 0) + (newLoanAmount > 0 ? newLoanAmount * 0.01 : 0);
  const newSavings = newIncome - newExpense - newEMI + investmentIncrease;
  const newDebtRatio = newIncome > 0 ? ((currentUser.totalDebt + newLoanAmount) / (newIncome * 12)) * 100 : 100;
  const newRisk = jobLoss ? 95 : Math.min(100, Math.max(0, 100 - currentUser.financialHealthScore + (newDebtRatio > 40 ? 20 : 0) + (newSavings < 0 ? 30 : 0)));

  const isPositive = newSavings > 0 && newDebtRatio < 40;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6"
    >
      <div className="flex items-center gap-2 mb-5">
        <FlaskConical className="w-4 h-4 text-primary" />
        <h3 className="text-sm font-semibold text-foreground">Scenario Simulator</h3>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Controls */}
        <div className="space-y-5">
          <div>
            <div className="flex justify-between text-xs mb-2">
              <span className="text-muted-foreground">New Loan Amount</span>
              <span className="text-foreground font-medium">{formatCurrency(newLoanAmount)}</span>
            </div>
            <Slider value={[newLoanAmount]} min={0} max={5000000} step={100000}
              onValueChange={([v]) => setSimulationParams({ newLoanAmount: v })} />
          </div>
          <div>
            <div className="flex justify-between text-xs mb-2">
              <span className="text-muted-foreground">Salary Increase</span>
              <span className="text-foreground font-medium">{salaryIncrease}%</span>
            </div>
            <Slider value={[salaryIncrease]} min={0} max={50} step={5}
              onValueChange={([v]) => setSimulationParams({ salaryIncrease: v })} />
          </div>
          <div>
            <div className="flex justify-between text-xs mb-2">
              <span className="text-muted-foreground">Vacation Expense</span>
              <span className="text-foreground font-medium">{formatCurrency(vacationExpense)}</span>
            </div>
            <Slider value={[vacationExpense]} min={0} max={500000} step={25000}
              onValueChange={([v]) => setSimulationParams({ vacationExpense: v })} />
          </div>
          <div>
            <div className="flex justify-between text-xs mb-2">
              <span className="text-muted-foreground">Extra Investment/mo</span>
              <span className="text-foreground font-medium">{formatCurrency(investmentIncrease)}</span>
            </div>
            <Slider value={[investmentIncrease]} min={0} max={50000} step={2500}
              onValueChange={([v]) => setSimulationParams({ investmentIncrease: v })} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground">Job Loss Scenario</span>
            <Switch checked={jobLoss} onCheckedChange={(v) => setSimulationParams({ jobLoss: v })} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground">House Purchase (+₹25K EMI)</span>
            <Switch checked={housePurchase} onCheckedChange={(v) => setSimulationParams({ housePurchase: v })} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground">Car Purchase (+₹15K EMI)</span>
            <Switch checked={carPurchase} onCheckedChange={(v) => setSimulationParams({ carPurchase: v })} />
          </div>
        </div>

        {/* Results */}
        <div className="space-y-3">
          <div className="text-xs font-medium text-muted-foreground mb-2">Simulated Impact</div>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-secondary/50 rounded-xl p-3">
              <div className="text-[10px] text-muted-foreground mb-1">New Monthly Savings</div>
              <div className={`text-lg font-bold ${newSavings >= 0 ? "text-success" : "text-danger"}`}>
                {newSavings >= 0 ? "+" : ""}{formatCurrency(Math.abs(newSavings))}
              </div>
            </div>
            <div className="bg-secondary/50 rounded-xl p-3">
              <div className="text-[10px] text-muted-foreground mb-1">New EMI Burden</div>
              <div className="text-lg font-bold text-foreground">{formatCurrency(newEMI)}/mo</div>
            </div>
            <div className="bg-secondary/50 rounded-xl p-3">
              <div className="text-[10px] text-muted-foreground mb-1">Risk Score</div>
              <div className={`text-lg font-bold ${newRisk < 40 ? "text-success" : newRisk < 70 ? "text-warning" : "text-danger"}`}>
                {Math.round(newRisk)}%
              </div>
            </div>
            <div className="bg-secondary/50 rounded-xl p-3">
              <div className="text-[10px] text-muted-foreground mb-1">Debt Ratio</div>
              <div className={`text-lg font-bold ${newDebtRatio < 30 ? "text-success" : newDebtRatio < 50 ? "text-warning" : "text-danger"}`}>
                {newDebtRatio.toFixed(1)}%
              </div>
            </div>
          </div>

          <div className={`rounded-xl p-4 mt-3 ${isPositive ? "bg-success/5 border border-success/20" : "bg-danger/5 border border-danger/20"}`}>
            <div className="flex items-center gap-2 mb-2">
              {isPositive ? <CheckCircle className="w-4 h-4 text-success" /> : <AlertTriangle className="w-4 h-4 text-danger" />}
              <span className={`text-xs font-semibold ${isPositive ? "text-success" : "text-danger"}`}>
                {isPositive ? "Financially Viable" : "High Risk Scenario"}
              </span>
            </div>
            <p className="text-[11px] text-muted-foreground leading-relaxed">
              {isPositive
                ? "This scenario maintains positive cash flow and manageable debt levels. Consider proceeding with caution."
                : "This scenario may strain your finances. Consider reducing loan amounts or delaying major purchases."}
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
