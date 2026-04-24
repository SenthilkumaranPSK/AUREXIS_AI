import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { runSimulation } from "@/lib/api";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { FlaskConical, AlertTriangle, CheckCircle, Loader2 } from "lucide-react";

export default function ScenarioSimulation() {
  const { currentUser, simulationParams, setSimulationParams } = useStore();
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const { newLoanAmount, salaryIncrease, jobLoss, vacationExpense, housePurchase, carPurchase, investmentIncrease } = simulationParams;

  useEffect(() => {
    if (!currentUser?.id) return;
    setLoading(true);
    runSimulation(currentUser.id, {
      new_loan: newLoanAmount,
      salary_increase: salaryIncrease,
      job_loss: jobLoss,
      vacation_expense: vacationExpense,
      house_purchase: housePurchase,
      car_purchase: carPurchase,
      investment_increase: investmentIncrease,
    })
      .then(res => setResult(res))
      .catch(() => setResult(null))
      .finally(() => setLoading(false));
  }, [currentUser?.id, newLoanAmount, salaryIncrease, jobLoss, vacationExpense, housePurchase, carPurchase, investmentIncrease]);

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <div className="flex items-center gap-2 mb-5">
        <FlaskConical className="w-4 h-4 text-primary" />
        <h3 className="text-sm font-semibold text-foreground">Scenario Simulator</h3>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Controls */}
        <div className="space-y-5">
          {[
            { label: "New Loan Amount",    key: "newLoanAmount",      min: 0, max: 5000000, step: 100000, display: formatCurrency(newLoanAmount) },
            { label: "Salary Increase",    key: "salaryIncrease",     min: 0, max: 50,      step: 5,      display: `${salaryIncrease}%` },
            { label: "Vacation Expense",   key: "vacationExpense",    min: 0, max: 500000,  step: 25000,  display: formatCurrency(vacationExpense) },
            { label: "Extra Investment/mo",key: "investmentIncrease", min: 0, max: 50000,   step: 2500,   display: formatCurrency(investmentIncrease) },
          ].map(({ label, key, min, max, step, display }) => (
            <div key={key}>
              <div className="flex justify-between text-xs mb-2">
                <span className="text-muted-foreground">{label}</span>
                <span className="text-foreground font-medium">{display}</span>
              </div>
              <Slider
                value={[(simulationParams as any)[key]]}
                min={min} max={max} step={step}
                onValueChange={([v]) => setSimulationParams({ [key]: v })}
              />
            </div>
          ))}

          {[
            { label: "Job Loss Scenario",         key: "jobLoss" },
            { label: "House Purchase (+₹25K EMI)", key: "housePurchase" },
            { label: "Car Purchase (+₹15K EMI)",   key: "carPurchase" },
          ].map(({ label, key }) => (
            <div key={key} className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">{label}</span>
              <Switch
                checked={(simulationParams as any)[key]}
                onCheckedChange={(v) => setSimulationParams({ [key]: v })}
              />
            </div>
          ))}
        </div>

        {/* Results */}
        <div className="space-y-3">
          <div className="text-xs font-medium text-muted-foreground mb-2">
            Simulated Impact {loading && <Loader2 className="inline w-3 h-3 animate-spin ml-1" />}
          </div>

          {result && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "New Monthly Savings", value: formatCurrency(Math.abs(result.newSavings)), color: result.newSavings >= 0 ? "text-success" : "text-danger", prefix: result.newSavings >= 0 ? "+" : "-" },
                  { label: "New EMI Burden",       value: `${formatCurrency(result.newEMI)}/mo`,      color: "text-foreground", prefix: "" },
                  { label: "Risk Score",           value: `${result.newRiskScore}%`,                  color: result.newRiskScore < 40 ? "text-success" : result.newRiskScore < 70 ? "text-warning" : "text-danger", prefix: "" },
                  { label: "Debt Ratio",           value: `${result.newDebtRatio}%`,                  color: result.newDebtRatio < 30 ? "text-success" : result.newDebtRatio < 50 ? "text-warning" : "text-danger", prefix: "" },
                ].map(({ label, value, color, prefix }) => (
                  <div key={label} className="bg-secondary/50 rounded-xl p-3">
                    <div className="text-[10px] text-muted-foreground mb-1">{label}</div>
                    <div className={`text-lg font-bold ${color}`}>{prefix}{value}</div>
                  </div>
                ))}
              </div>

              <div className={`rounded-xl p-4 mt-3 border ${result.isViable ? "bg-success/5 border-success/20" : "bg-danger/5 border-danger/20"}`}>
                <div className="flex items-center gap-2 mb-2">
                  {result.isViable
                    ? <CheckCircle className="w-4 h-4 text-success" />
                    : <AlertTriangle className="w-4 h-4 text-danger" />
                  }
                  <span className={`text-xs font-semibold ${result.isViable ? "text-success" : "text-danger"}`}>
                    {result.isViable ? "Financially Viable" : "High Risk Scenario"}
                  </span>
                </div>
                <p className="text-[11px] text-muted-foreground leading-relaxed">{result.advice}</p>
              </div>
            </>
          )}
        </div>
      </div>
    </motion.div>
  );
}
