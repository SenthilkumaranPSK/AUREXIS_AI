import { useState, useRef, useEffect, MouseEvent } from "react";
import { motion, AnimatePresence, useMotionValue, useSpring, useTransform } from "framer-motion";
import { MessageCircle, X, Send, Sparkles, Bot, User, Maximize2, Minimize2 } from "lucide-react";
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
  const [isFullscreen, setIsFullscreen] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const chatRef = useRef<HTMLDivElement>(null);

  // Mouse tracking for interactive animations
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const springConfig = { stiffness: 150, damping: 15 };
  const x = useSpring(mouseX, springConfig);
  const y = useSpring(mouseY, springConfig);

  const transformX = useTransform(x, [-10, 10], [-2, 2]);
  const transformY = useTransform(y, [-10, 10], [-2, 2]);
  const transformRotateX = useTransform(y, [-10, 10], [1, -1]);
  const transformRotateY = useTransform(x, [-10, 10], [-1, 1]);

  const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
    if (!chatRef.current) return;
    const rect = chatRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    mouseX.set((e.clientX - centerX) / 30);
    mouseY.set((e.clientY - centerY) / 30);
  };

  const handleMouseLeave = () => {
    mouseX.set(0);
    mouseY.set(0);
  };

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, typing]);

  // Auto-warmup Ollama on load so it's instantly fast during the presentation
  useEffect(() => {
    sendChatMessage({
      user_id: "system-warmup",
      message: "ping",
      conversation_history: []
    }).catch(() => {}); // Silently fail if not running
  }, []);

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
            key="chat-bubble"
            initial={{ scale: 0, opacity: 0 }} 
            animate={{ scale: 1, opacity: 1 }} 
            exit={{ scale: 0, opacity: 0 }}
            whileHover={{ scale: 1.08, rotate: 5 }} 
            whileTap={{ scale: 0.92 }}
            transition={{ type: "spring", stiffness: 400, damping: 20 }}
            onClick={() => setChatOpen(true)}
            className="fixed bottom-6 right-6 w-14 h-14 rounded-2xl gradient-primary glow-primary flex items-center justify-center z-[100] shadow-2xl"
          >
            <MessageCircle className="w-6 h-6 text-white" />
          </motion.button>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {chatOpen && (
          <>
            {/* Backdrop blur for fullscreen mode */}
            {isFullscreen && (
              <motion.div
                key="chat-backdrop"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3, ease: "easeInOut" }}
                className="fixed inset-0 bg-background/80 backdrop-blur-md z-[99]"
                onClick={() => setIsFullscreen(false)}
              />
            )}

            <motion.div
              ref={chatRef}
              key="chat-window"
              initial={{ 
                opacity: 0, 
                scale: 0.85
              }}
              animate={{ 
                opacity: 1, 
                scale: 1
              }}
              exit={{ 
                opacity: 0, 
                scale: 0.85
              }}
              style={{
                x: isFullscreen ? 0 : transformX,
                y: isFullscreen ? 0 : transformY,
                rotateX: isFullscreen ? 0 : transformRotateX,
                rotateY: isFullscreen ? 0 : transformRotateY
              }}
              onMouseMove={handleMouseMove}
              onMouseLeave={handleMouseLeave}
              transition={{ 
                type: "spring", 
                stiffness: 300, 
                damping: 30,
                opacity: { duration: 0.2 }
              }}
              className={`flex flex-col z-[100] bg-card rounded-2xl overflow-hidden shadow-2xl glass-card border border-border ${
                isFullscreen 
                  ? "fixed inset-0 m-auto w-[min(900px,90vw)] h-[min(700px,85vh)]" 
                  : "fixed bottom-6 right-6 w-[380px] h-[580px]"
              }`}
            >
              {/* Header */}
              <div className="px-4 py-3.5 border-b border-border flex items-center justify-between shrink-0 bg-card/50 backdrop-blur-sm">
                <div className="flex items-center gap-2.5">
                  <motion.div 
                    className="w-8 h-8 rounded-xl gradient-primary flex items-center justify-center"
                    animate={{ rotate: [0, 5, -5, 0] }}
                    transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
                  >
                    <Sparkles className="w-4 h-4 text-white" />
                  </motion.div>
                  <div>
                    <div className="text-xs font-bold text-foreground tracking-wide">AUREXIS AI</div>
                    <div className={`text-[10px] flex items-center gap-1 mt-0.5 ${connected ? "text-success" : "text-warning"}`}>
                      <motion.span 
                        className={`w-1.5 h-1.5 rounded-full ${connected ? "bg-success" : "bg-warning"}`}
                        animate={{ scale: [1, 1.2, 1], opacity: [1, 0.7, 1] }}
                        transition={{ duration: 2, repeat: Infinity }}
                      />
                      {connected ? "Ollama · Local AI Active" : "Offline"}
                      {connected && (
                        <span className="ml-1.5 px-1.5 py-0.5 rounded bg-success/20 text-success text-[8px] font-bold tracking-wider uppercase border border-success/30">
                          Privacy Secured
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-1">
                  <motion.button 
                    onClick={() => setIsFullscreen(!isFullscreen)} 
                    className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-all"
                    title={isFullscreen ? "Exit fullscreen" : "Fullscreen"}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                  >
                    <motion.div
                      key={isFullscreen ? "minimize" : "maximize"}
                      initial={{ rotate: -90, opacity: 0 }}
                      animate={{ rotate: 0, opacity: 1 }}
                      exit={{ rotate: 90, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                    </motion.div>
                  </motion.button>
                  <motion.button 
                    onClick={() => setChatOpen(false)} 
                    className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-all"
                    whileHover={{ scale: 1.1, rotate: 90 }}
                    whileTap={{ scale: 0.9 }}
                  >
                    <X className="w-4 h-4" />
                  </motion.button>
                </div>
              </div>

            {/* Messages */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4 scroll-smooth">
              {messages.map((msg, i) => (
                <motion.div 
                  key={i} 
                  initial={{ opacity: 0, y: 12, scale: 0.95 }} 
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ 
                    type: "spring", 
                    stiffness: 400, 
                    damping: 25,
                    delay: i * 0.05 
                  }}
                  className={`flex gap-2.5 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}
                >
                  <motion.div 
                    className={`w-6 h-6 rounded-lg shrink-0 flex items-center justify-center mt-0.5 ${msg.role === "user" && !currentUser?.avatar ? "bg-primary/15" : msg.role === "assistant" ? "gradient-primary" : ""}`}
                    whileHover={{ scale: 1.1, rotate: 5 }}
                    transition={{ type: "spring", stiffness: 400 }}
                  >
                    {msg.role === "user" ? (
                      currentUser?.avatar ? (
                        <img src={currentUser.avatar} alt="User" className="w-full h-full rounded-lg object-cover" />
                      ) : (
                        <User className="w-3 h-3 text-primary" />
                      )
                    ) : (
                      <Bot className="w-3 h-3 text-white" />
                    )}
                  </motion.div>
                  <motion.div 
                    className={`${isFullscreen ? "max-w-[85%]" : "max-w-[78%]"} px-3.5 py-2.5 rounded-2xl text-xs leading-relaxed whitespace-pre-wrap ${
                      msg.role === "user"
                        ? "bg-primary/15 text-foreground rounded-tr-sm border border-primary/20"
                        : "bg-muted text-foreground rounded-tl-sm border border-border"
                    }`}
                    whileHover={{ scale: 1.01 }}
                    transition={{ type: "spring", stiffness: 400 }}
                  >
                    {msg.content}
                  </motion.div>
                </motion.div>
              ))}

              {typing && (
                <motion.div 
                  className="flex gap-2.5"
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -12 }}
                  transition={{ type: "spring", stiffness: 400, damping: 25 }}
                >
                  <div className="w-6 h-6 rounded-lg gradient-primary shrink-0 flex items-center justify-center">
                    <Bot className="w-3 h-3 text-white" />
                  </div>
                  <div className="bg-muted border border-border px-4 py-3 rounded-2xl rounded-tl-sm flex items-center gap-1.5">
                    {[0, 0.15, 0.3].map((delay, i) => (
                      <motion.span key={i} className="w-1.5 h-1.5 rounded-full bg-muted-foreground"
                        animate={{ 
                          opacity: [0.3, 1, 0.3], 
                          scale: [0.8, 1.2, 0.8],
                          y: [0, -4, 0]
                        }}
                        transition={{ duration: 1, repeat: Infinity, delay }}
                      />
                    ))}
                    <span className="text-[10px] text-muted-foreground ml-1">Thinking...</span>
                  </div>
                </motion.div>
              )}
            </div>

            {/* Suggestions */}
            {messages.length <= 1 && (
              <motion.div 
                className="px-4 pb-2 flex flex-wrap gap-1.5"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3, duration: 0.4 }}
              >
                {suggestions.map((s, i) => (
                  <motion.button 
                    key={i} 
                    onClick={() => send(s)}
                    className="px-2.5 py-1.5 rounded-lg text-[10px] font-medium bg-muted text-muted-foreground hover:bg-secondary hover:text-foreground transition-all border border-border"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.4 + i * 0.05, type: "spring", stiffness: 400 }}
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    {s}
                  </motion.button>
                ))}
              </motion.div>
            )}

            {/* Input */}
            <motion.div 
              className="p-3 border-t border-border shrink-0"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.3 }}
            >
              <div className="flex items-center gap-2 bg-muted rounded-xl px-3.5 py-2.5 border border-border focus-within:border-primary/40 focus-within:ring-2 focus-within:ring-primary/20 transition-all">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send(input)}
                  placeholder="Ask about your finances..."
                  className="flex-1 bg-transparent text-xs text-foreground placeholder:text-muted-foreground outline-none"
                />
                <motion.button 
                  onClick={() => send(input)} 
                  disabled={!input.trim() || typing}
                  className="w-7 h-7 rounded-lg gradient-primary flex items-center justify-center hover:opacity-90 transition-all disabled:opacity-30 disabled:cursor-not-allowed shrink-0"
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <Send className="w-3 h-3 text-white" />
                </motion.button>
              </div>
            </motion.div>
          </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
