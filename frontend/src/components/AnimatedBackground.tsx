import { useEffect, useRef } from "react";
import { useStore } from "@/store/useStore";

export default function AnimatedBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { isDark } = useStore();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d", {
      alpha: false, // Disable alpha for better performance
      desynchronized: true, // Allow async rendering
    });
    if (!ctx) return;

    let animId: number;
    let lastTime = 0;
    const targetFPS = 60;
    const frameTime = 1000 / targetFPS;

    // Pre-calculate color strings for better performance
    const orbs = [
      { r: 0.18, g: 0.42, b: 0.95, x: 0.15, y: 0.30, radius: 0.38, speed: 0.00018, ax: 0.12, ay: 0.10 },
      { r: 0.55, g: 0.25, b: 0.95, x: 0.80, y: 0.15, radius: 0.32, speed: 0.00024, ax: 0.10, ay: 0.14 },
      { r: 0.08, g: 0.75, b: 0.65, x: 0.70, y: 0.75, radius: 0.30, speed: 0.00020, ax: 0.14, ay: 0.09 },
      { r: 0.95, g: 0.65, b: 0.10, x: 0.30, y: 0.80, radius: 0.25, speed: 0.00015, ax: 0.08, ay: 0.12 },
      { r: 0.10, g: 0.50, b: 0.90, x: 0.55, y: 0.45, radius: 0.22, speed: 0.00022, ax: 0.16, ay: 0.08 },
    ].map(orb => ({
      ...orb,
      r255: Math.round(orb.r * 255),
      g255: Math.round(orb.g * 255),
      b255: Math.round(orb.b * 255),
    }));

    const resize = () => {
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      
      // Set actual size in memory (scaled to account for extra pixel density)
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      
      // Scale context to ensure correct drawing operations
      ctx.scale(dpr, dpr);
      
      // Set display size (css pixels)
      canvas.style.width = `${rect.width}px`;
      canvas.style.height = `${rect.height}px`;
    };
    resize();
    window.addEventListener("resize", resize);

    // Cache static elements
    let gridCanvas: HTMLCanvasElement | null = null;
    let vignetteCanvas: HTMLCanvasElement | null = null;
    
    const createGridCache = (W: number, H: number) => {
      if (!gridCanvas) {
        gridCanvas = document.createElement('canvas');
      }
      gridCanvas.width = W;
      gridCanvas.height = H;
      const gridCtx = gridCanvas.getContext('2d');
      if (!gridCtx) return;
      
      gridCtx.strokeStyle = isDark ? "rgba(255,255,255,0.018)" : "rgba(0,0,0,0.04)";
      gridCtx.lineWidth = 1;
      const gridSize = 40;
      
      // Draw vertical lines
      for (let x = 0; x < W; x += gridSize) {
        gridCtx.beginPath();
        gridCtx.moveTo(x, 0);
        gridCtx.lineTo(x, H);
        gridCtx.stroke();
      }
      
      // Draw horizontal lines
      for (let y = 0; y < H; y += gridSize) {
        gridCtx.beginPath();
        gridCtx.moveTo(0, y);
        gridCtx.lineTo(W, y);
        gridCtx.stroke();
      }
    };
    
    const createVignetteCache = (W: number, H: number) => {
      if (!vignetteCanvas) {
        vignetteCanvas = document.createElement('canvas');
      }
      vignetteCanvas.width = W;
      vignetteCanvas.height = H;
      const vigCtx = vignetteCanvas.getContext('2d');
      if (!vigCtx) return;
      
      const vignette = vigCtx.createRadialGradient(W/2, H/2, H*0.2, W/2, H/2, H*0.85);
      if (isDark) {
        vignette.addColorStop(0, "rgba(0,0,0,0)");
        vignette.addColorStop(1, "rgba(0,0,0,0.55)");
      } else {
        vignette.addColorStop(0, "rgba(255,255,255,0)");
        vignette.addColorStop(1, "rgba(220,225,235,0.4)");
      }
      vigCtx.fillStyle = vignette;
      vigCtx.fillRect(0, 0, W, H);
    };

    let W = 0, H = 0;
    const updateCaches = () => {
      const rect = canvas.getBoundingClientRect();
      W = rect.width;
      H = rect.height;
      createGridCache(W, H);
      createVignetteCache(W, H);
    };
    updateCaches();

    const draw = (currentTime: number) => {
      // Frame rate limiting for consistent 60 FPS
      const deltaTime = currentTime - lastTime;
      
      if (deltaTime >= frameTime) {
        lastTime = currentTime - (deltaTime % frameTime);
        
        // Use will-change hint for better performance
        ctx.save();
        
        // Base background — dark navy or light white
        ctx.fillStyle = isDark ? "hsl(224, 40%, 5%)" : "hsl(220, 20%, 97%)";
        ctx.fillRect(0, 0, W, H);

        // Orb opacity is lower in light mode so it stays subtle
        const orbAlpha = isDark ? 1 : 0.45;

        // Draw orbs with optimized gradient creation
        orbs.forEach((orb, i) => {
          const phase = i * 1.3;
          const cx = (orb.x + Math.sin(currentTime * orb.speed + phase) * orb.ax) * W;
          const cy = (orb.y + Math.cos(currentTime * orb.speed * 0.7 + phase) * orb.ay) * H;
          const rad = orb.radius * Math.min(W, H);

          const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, rad);
          grad.addColorStop(0, `rgba(${orb.r255},${orb.g255},${orb.b255},${0.18 * orbAlpha})`);
          grad.addColorStop(0.4, `rgba(${orb.r255},${orb.g255},${orb.b255},${0.07 * orbAlpha})`);
          grad.addColorStop(1, `rgba(${orb.r255},${orb.g255},${orb.b255},0)`);

          ctx.globalCompositeOperation = isDark ? "screen" : "multiply";
          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.arc(cx, cy, rad, 0, Math.PI * 2);
          ctx.fill();
        });

        // Draw cached grid
        ctx.globalCompositeOperation = "source-over";
        if (gridCanvas) {
          ctx.drawImage(gridCanvas, 0, 0);
        }

        // Draw cached vignette
        if (vignetteCanvas) {
          ctx.drawImage(vignetteCanvas, 0, 0);
        }
        
        ctx.restore();
      }

      animId = requestAnimationFrame(draw);
    };

    animId = requestAnimationFrame(draw);
    
    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);
      gridCanvas = null;
      vignetteCanvas = null;
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
