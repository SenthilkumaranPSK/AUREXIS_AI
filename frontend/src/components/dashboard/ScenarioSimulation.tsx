import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { formatCurrency } from "@/lib/formatters";
import { runSimulation, sendChatMessage } from "@/lib/api";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { FlaskConical, AlertTriangle, CheckCircle, Loader2, Bot, Send, User } from "lucide-react";
import { useMouseReactive } from "@/hooks/useMouseReactive";

export default function ScenarioSimulation() {
  const { currentUser, simulationParams, setSimulationParams } = useStore();
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const { ref, x, y, rotateX, rotateY, handleMouseMove, handleMouseLeave } = useMouseReactive({ sensitivity: 25, tiltIntensity: 2 });

  // AI Chat State
  const [chatInput, setChatInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [messages, setMessages] = useState([
    { role: "ai", text: "Welcome to the Scenario Simulator. You can manipulate the fiscal parameters manually, or instruct me to model a specific financial event." }
  ]);

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

  const handleChatSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const currentInput = chatInput.toLowerCase();
    setMessages(prev => [...prev, { role: "user", text: chatInput }]);
    setChatInput("");
    setIsTyping(true);

    let fallbackResponse = "Based on this scenario, I recommend keeping a close eye on your debt-to-income ratio. Feel free to tweak the sliders manually!";
    const updatedParams = { ...simulationParams };

    if (currentInput.includes("house") || currentInput.includes("home")) {
      updatedParams.housePurchase = true;
      fallbackResponse = "I've simulated a House Purchase scenario. Notice how the new EMI changes your monthly savings and debt ratio.";
    } else if (currentInput.includes("car")) {
      updatedParams.carPurchase = true;
      fallbackResponse = "I've enabled the Car Purchase scenario. A new EMI has been added to your monthly commitments.";
    } else if (currentInput.includes("job") || currentInput.includes("fired") || currentInput.includes("lose")) {
      updatedParams.jobLoss = true;
      fallbackResponse = "I've activated the Job Loss scenario. This is high risk unless your emergency fund can carry your monthly expenses.";
    } else if (currentInput.includes("loan") || currentInput.includes("borrow")) {
      updatedParams.newLoanAmount = 500000;
      fallbackResponse = "I've added a new ₹500,000 loan to your simulation. Watch your debt ratio closely.";
    } else if (currentInput.includes("vacation") || currentInput.includes("trip")) {
      updatedParams.vacationExpense = 150000;
      fallbackResponse = "I've factored in a ₹150,000 vacation expense. Make sure your surplus cash can absorb it.";
    } else if (currentInput.includes("salary") || currentInput.includes("raise") || currentInput.includes("promotion")) {
      updatedParams.salaryIncrease = 20;
      fallbackResponse = "I've increased your salary by 20% in the simulation so you can compare the cash-flow impact.";
    }

    setSimulationParams(updatedParams);

    try {
      const scenarioSummary = [
        `loan=${updatedParams.newLoanAmount}`,
        `salaryIncrease=${updatedParams.salaryIncrease}%`,
        `jobLoss=${updatedParams.jobLoss}`,
        `vacationExpense=${updatedParams.vacationExpense}`,
        `housePurchase=${updatedParams.housePurchase}`,
        `carPurchase=${updatedParams.carPurchase}`,
        `investmentIncrease=${updatedParams.investmentIncrease}`,
      ].join(", ");

      const response = await sendChatMessage({
        message: `Assess this financial scenario in 2-3 concise sentences with focus on cash flow, debt, and risk. User request: "${chatInput}". Scenario: ${scenarioSummary}.`,
        conversation_history: messages.slice(-4).map((message) => ({
          role: message.role === "ai" ? "assistant" : message.role,
          content: message.text,
        })),
      });

      const aiResponse = response?.success && response?.response?.content
        ? response.response.content
        : fallbackResponse;

      setMessages(prev => [...prev, { role: "ai", text: aiResponse }]);
    } catch {
      setMessages(prev => [...prev, { role: "ai", text: fallbackResponse }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <motion.div 
      ref={ref}
      style={{ x, y, rotateX, rotateY }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      initial={{ opacity: 0, y: 12 }} 
      animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 border border-border"
    >
      <div className="flex items-center gap-2 mb-5">
        <FlaskConical className="w-4 h-4 text-primary" />
        <h3 className="text-sm font-semibold text-foreground">Scenario Simulator</h3>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
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

        {/* AI Advisor Chat */}
        <div className="flex flex-col border border-border rounded-xl bg-background/50 h-[400px]">
          <div className="p-3 border-b border-border flex items-center gap-2 bg-muted/20 rounded-t-xl">
            <Bot className="w-4 h-4 text-primary" />
            <span className="text-xs font-semibold">AI Simulator Advisor</span>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-4 flex flex-col">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex gap-2.5 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
                <div className={`w-6 h-6 rounded-lg shrink-0 flex items-center justify-center mt-0.5 ${msg.role === "user" && !currentUser?.avatar ? "bg-primary/15" : msg.role === "ai" ? "gradient-primary" : ""}`}>
                  {msg.role === "user" ? (
                    currentUser?.avatar ? (
                      <img src={currentUser.avatar} alt="User" className="w-full h-full rounded-lg object-cover" />
                    ) : (
                      <User className="w-3 h-3 text-primary" />
                    )
                  ) : (
                    <Bot className="w-3 h-3 text-white" />
                  )}
                </div>
                <div className={`text-[11px] p-2.5 rounded-xl max-w-[85%] ${
                  msg.role === "user" 
                    ? "bg-primary text-primary-foreground rounded-tr-sm" 
                    : "bg-muted text-foreground rounded-tl-sm border border-border"
                }`}>
                  {msg.text}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-muted text-muted-foreground p-2.5 rounded-xl rounded-tl-sm border border-border flex items-center gap-1">
                  <span className="w-1 h-1 bg-current rounded-full animate-bounce" />
                  <span className="w-1 h-1 bg-current rounded-full animate-bounce delay-75" />
                  <span className="w-1 h-1 bg-current rounded-full animate-bounce delay-150" />
                </div>
              </div>
            )}
          </div>

          <form onSubmit={handleChatSubmit} className="p-3 border-t border-border flex gap-2">
            <input 
              type="text" 
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="e.g. Simulate buying a car"
              className="flex-1 bg-muted/50 border border-border rounded-lg px-3 py-1.5 text-xs text-foreground focus:outline-none focus:border-primary transition-colors"
            />
            <button 
              type="submit" 
              disabled={!chatInput.trim() || isTyping}
              className="p-1.5 bg-primary text-primary-foreground rounded-lg disabled:opacity-50 hover:bg-primary/90 transition-colors"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>

      </div>
    </motion.div>
  );
}
