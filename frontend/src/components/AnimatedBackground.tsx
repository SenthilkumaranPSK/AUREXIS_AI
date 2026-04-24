import { useEffect, useRef } from "react";
import { useStore } from "@/store/useStore";

export default function AnimatedBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { isDark } = useStore();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;

    const orbs = [
      { r: 0.18, g: 0.42, b: 0.95, x: 0.15, y: 0.30, radius: 0.38, speed: 0.00018, ax: 0.12, ay: 0.10 },
      { r: 0.55, g: 0.25, b: 0.95, x: 0.80, y: 0.15, radius: 0.32, speed: 0.00024, ax: 0.10, ay: 0.14 },
      { r: 0.08, g: 0.75, b: 0.65, x: 0.70, y: 0.75, radius: 0.30, speed: 0.00020, ax: 0.14, ay: 0.09 },
      { r: 0.95, g: 0.65, b: 0.10, x: 0.30, y: 0.80, radius: 0.25, speed: 0.00015, ax: 0.08, ay: 0.12 },
      { r: 0.10, g: 0.50, b: 0.90, x: 0.55, y: 0.45, radius: 0.22, speed: 0.00022, ax: 0.16, ay: 0.08 },
    ];

    const resize = () => {
      canvas.width  = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    const draw = (ts: number) => {
      const W = canvas.width;
      const H = canvas.height;

      // Base background — dark navy or light white
      ctx.fillStyle = isDark ? "hsl(224, 40%, 5%)" : "hsl(220, 20%, 97%)";
      ctx.fillRect(0, 0, W, H);

      // Orb opacity is lower in light mode so it stays subtle
      const orbAlpha = isDark ? 1 : 0.45;

      orbs.forEach((orb, i) => {
        const phase = i * 1.3;
        const cx = (orb.x + Math.sin(ts * orb.speed + phase)       * orb.ax) * W;
        const cy = (orb.y + Math.cos(ts * orb.speed * 0.7 + phase) * orb.ay) * H;
        const rad = orb.radius * Math.min(W, H);

        const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, rad);
        grad.addColorStop(0,   `rgba(${Math.round(orb.r*255)},${Math.round(orb.g*255)},${Math.round(orb.b*255)}, ${0.18 * orbAlpha})`);
        grad.addColorStop(0.4, `rgba(${Math.round(orb.r*255)},${Math.round(orb.g*255)},${Math.round(orb.b*255)}, ${0.07 * orbAlpha})`);
        grad.addColorStop(1,   `rgba(${Math.round(orb.r*255)},${Math.round(orb.g*255)},${Math.round(orb.b*255)}, 0)`);

        ctx.globalCompositeOperation = isDark ? "screen" : "multiply";
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(cx, cy, rad, 0, Math.PI * 2);
        ctx.fill();
      });

      // Grid overlay
      ctx.globalCompositeOperation = "source-over";
      ctx.strokeStyle = isDark ? "rgba(255,255,255,0.018)" : "rgba(0,0,0,0.04)";
      ctx.lineWidth = 1;
      const gridSize = 40;
      for (let x = 0; x < W; x += gridSize) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
      }
      for (let y = 0; y < H; y += gridSize) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
      }

      // Vignette
      const vignette = ctx.createRadialGradient(W/2, H/2, H*0.2, W/2, H/2, H*0.85);
      if (isDark) {
        vignette.addColorStop(0, "rgba(0,0,0,0)");
        vignette.addColorStop(1, "rgba(0,0,0,0.55)");
      } else {
        vignette.addColorStop(0, "rgba(255,255,255,0)");
        vignette.addColorStop(1, "rgba(220,225,235,0.4)");
      }
      ctx.globalCompositeOperation = "source-over";
      ctx.fillStyle = vignette;
      ctx.fillRect(0, 0, W, H);

      animId = requestAnimationFrame(draw);
    };

    animId = requestAnimationFrame(draw);
    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);
    };
  }, [isDark]); // re-run when theme changes

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 w-full h-full pointer-events-none"
      style={{ zIndex: 0 }}
    />
  );
}
