import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useStore } from "@/store/useStore";
import { Sparkles, ArrowRight, X, CheckCircle } from "lucide-react";

interface TourStep {
  target: string;
  title: string;
  content: string;
  position: "top" | "bottom" | "left" | "right";
}

const TOUR_STEPS: TourStep[] = [
  {
    target: "dashboard-header",
    title: "Intelligence Hub",
    content: "Welcome to AUREXIS AI. This is your central command for financial intelligence.",
    position: "bottom"
  },
  {
    target: "ml-forecast-chart",
    title: "Predictive Analytics",
    content: "Our Machine Learning engine forecasts your next 6 months of cash flow with 96%+ accuracy.",
    position: "top"
  },
  {
    target: "risk-audit-panel",
    title: "Deep Risk Auditing",
    content: "We calculate CVaR and VaR to simulate extreme market conditions and protect your wealth.",
    position: "left"
  },
  {
    target: "privacy-badge",
    title: "Military-Grade Privacy",
    content: "All AI processing is done locally on your machine. Your data never leaves your sight.",
    position: "bottom"
  }
];

export default function ProductTour() {
  const [currentStep, setCurrentStep] = useState(-1);
  const { currentUser } = useStore();

  useEffect(() => {
    // Start tour automatically for new users (simulated)
    const hasSeenTour = localStorage.getItem("hasSeenTour");
    if (!hasSeenTour) {
      const timer = setTimeout(() => setCurrentStep(0), 2000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleNext = () => {
    if (currentStep < TOUR_STEPS.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleComplete();
    }
  };

  const handleComplete = () => {
    setCurrentStep(-1);
    localStorage.setItem("hasSeenTour", "true");
  };

  if (currentStep === -1) return null;

  const step = TOUR_STEPS[currentStep];

  return (
    <div className="fixed inset-0 z-[100] pointer-events-none">
      <div className="absolute inset-0 bg-background/40 backdrop-blur-[2px] pointer-events-auto" onClick={handleComplete} />
      
      <AnimatePresence mode="wait">
        <motion.div
          key={currentStep}
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: 20 }}
          className="absolute z-[101] pointer-events-auto w-[320px] glass-card p-6 rounded-2xl border-2 border-primary shadow-2xl"
          style={{
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)"
          }}
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="p-1.5 rounded-lg bg-primary/20">
                <Sparkles className="w-4 h-4 text-primary" />
              </div>
              <span className="text-xs font-bold text-muted-foreground">Step {currentStep + 1} of {TOUR_STEPS.length}</span>
            </div>
            <button onClick={handleComplete} className="p-1 hover:bg-muted rounded-full transition-colors">
              <X className="w-4 h-4 text-muted-foreground" />
            </button>
          </div>

          <h3 className="text-lg font-bold text-foreground mb-2">{step.title}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed mb-6">
            {step.content}
          </p>

          <div className="flex items-center justify-between">
            <div className="flex gap-1">
              {TOUR_STEPS.map((_, i) => (
                <div key={i} className={`w-1.5 h-1.5 rounded-full transition-all ${i === currentStep ? "w-4 bg-primary" : "bg-muted"}`} />
              ))}
            </div>
            <button
              onClick={handleNext}
              className="px-4 py-2 rounded-xl gradient-primary text-white text-xs font-bold flex items-center gap-2 hover:opacity-90 transition-opacity"
            >
              {currentStep === TOUR_STEPS.length - 1 ? (
                <>Finish Tour <CheckCircle className="w-3.5 h-3.5" /></>
              ) : (
                <>Next <ArrowRight className="w-3.5 h-3.5" /></>
              )}
            </button>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
