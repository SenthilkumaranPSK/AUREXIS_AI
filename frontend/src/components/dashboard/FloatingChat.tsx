import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageCircle, X, Send, Sparkles, Bot, User } from "lucide-react";
import { useStore } from "@/store/useStore";
import { sendChatMessage } from "@/lib/api";

interface Message { role: "user" | "assistant"; content: string; }

const suggestions = [
  "How can I reduce spending?",
  "Analyse my risk exposure",
  "Should I take a new loan?",
  "Optimise my portfolio",
  "Build a savings plan",
];

export default function FloatingChat() {
  const { chatOpen, setChatOpen, currentUser } = useStore();
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: `Hi ${currentUser?.name?.split(" ")[0] || "there"}! I'm AUREXIS AI. Ask me anything about your finances.` },
  ]);
  const [input, setInput]         = useState("");
  const [typing, setTyping]       = useState(false);
  const [connected, setConnected] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, typing]);

  const send = async (text: string) => {
    if (!text.trim() || typing) return;
    setMessages(prev => [...prev, { role: "user", content: text }]);
    setInput("");
    setTyping(true);
    try {
      const res = await sendChatMessage({
        user_id: currentUser?.id || currentUser?.name || "guest",
        message: text,
        conversation_history: messages.slice(-6).map(m => ({ role: m.role, content: m.content })),
      });
      if (res.success) {
        const d = res.response;
        let content = d.content;
        if (d.insights?.length)        content += "\n\n💡 " + d.insights.join(" · ");
        if (d.recommendations?.length) content += "\n\n✅ " + d.recommendations.join(" · ");
        setMessages(prev => [...prev, { role: "assistant", content }]);
        setConnected(true);
      } else throw new Error("failed");
    } catch {
      setConnected(false);
      setMessages(prev => [...prev, { role: "assistant", content: "⚠️ Could not reach Ollama. Make sure it's running with `ollama serve`." }]);
    } finally {
      setTyping(false);
    }
  };

  return (
    <>
      <AnimatePresence>
        {!chatOpen && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0, opacity: 0 }}
            whileHover={{ scale: 1.08 }} whileTap={{ scale: 0.95 }}
            onClick={() => setChatOpen(true)}
            className="fixed bottom-6 right-6 w-14 h-14 rounded-2xl gradient-primary glow-primary flex items-center justify-center z-50 shadow-2xl"
          >
            <MessageCircle className="w-6 h-6 text-white" />
          </motion.button>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {chatOpen && (
          <motion.div
            initial={{ opacity: 0, y: 24, scale: 0.94 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 24, scale: 0.94 }}
            transition={{ type: "spring", stiffness: 300, damping: 28 }}
            className="fixed bottom-6 right-6 w-[380px] h-[580px] flex flex-col z-50 rounded-2xl overflow-hidden shadow-2xl glass-card border border-border"
          >
            {/* Header */}
            <div className="px-4 py-3.5 border-b border-border flex items-center justify-between shrink-0">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl gradient-primary flex items-center justify-center">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <div>
                  <div className="text-xs font-bold text-foreground tracking-wide">AUREXIS AI</div>
                  <div className={`text-[10px] flex items-center gap-1 ${connected ? "text-success" : "text-warning"}`}>
                    <span className={`w-1.5 h-1.5 rounded-full ${connected ? "bg-success" : "bg-warning"}`} />
                    {connected ? "Ollama · deepseek-v3.1:671b" : "Offline"}
                  </div>
                </div>
              </div>
              <button onClick={() => setChatOpen(false)} className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-all">
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Messages */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((msg, i) => (
                <motion.div key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-2.5 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}
                >
                  <div className={`w-6 h-6 rounded-lg shrink-0 flex items-center justify-center mt-0.5 ${msg.role === "user" ? "bg-primary/15" : "gradient-primary"}`}>
                    {msg.role === "user" ? <User className="w-3 h-3 text-primary" /> : <Bot className="w-3 h-3 text-white" />}
                  </div>
                  <div className={`max-w-[78%] px-3.5 py-2.5 rounded-2xl text-xs leading-relaxed whitespace-pre-wrap ${
                    msg.role === "user"
                      ? "bg-primary/15 text-foreground rounded-tr-sm border border-primary/20"
                      : "bg-muted text-foreground rounded-tl-sm border border-border"
                  }`}>
                    {msg.content}
                  </div>
                </motion.div>
              ))}

              {typing && (
                <div className="flex gap-2.5">
                  <div className="w-6 h-6 rounded-lg gradient-primary shrink-0 flex items-center justify-center">
                    <Bot className="w-3 h-3 text-white" />
                  </div>
                  <div className="bg-muted border border-border px-4 py-3 rounded-2xl rounded-tl-sm flex items-center gap-1.5">
                    {[0, 0.15, 0.3].map((delay, i) => (
                      <motion.span key={i} className="w-1.5 h-1.5 rounded-full bg-muted-foreground"
                        animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1, 0.8] }}
                        transition={{ duration: 1, repeat: Infinity, delay }}
                      />
                    ))}
                    <span className="text-[10px] text-muted-foreground ml-1">Thinking...</span>
                  </div>
                </div>
              )}
            </div>

            {/* Suggestions */}
            {messages.length <= 1 && (
              <div className="px-4 pb-2 flex flex-wrap gap-1.5">
                {suggestions.map((s, i) => (
                  <button key={i} onClick={() => send(s)}
                    className="px-2.5 py-1.5 rounded-lg text-[10px] font-medium bg-muted text-muted-foreground hover:bg-secondary hover:text-foreground transition-all border border-border"
                  >
                    {s}
                  </button>
                ))}
              </div>
            )}

            {/* Input */}
            <div className="p-3 border-t border-border shrink-0">
              <div className="flex items-center gap-2 bg-muted rounded-xl px-3.5 py-2.5 border border-border focus-within:border-primary/40 transition-all">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send(input)}
                  placeholder="Ask about your finances..."
                  className="flex-1 bg-transparent text-xs text-foreground placeholder:text-muted-foreground outline-none"
                />
                <button onClick={() => send(input)} disabled={!input.trim() || typing}
                  className="w-7 h-7 rounded-lg gradient-primary flex items-center justify-center hover:opacity-90 transition-all disabled:opacity-30 disabled:cursor-not-allowed shrink-0"
                >
                  <Send className="w-3 h-3 text-white" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
