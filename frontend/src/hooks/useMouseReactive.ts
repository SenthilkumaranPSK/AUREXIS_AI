import { useRef, MouseEvent } from "react";
import { useMotionValue, useSpring, useTransform, MotionValue, useReducedMotion } from "framer-motion";

interface MouseReactiveConfig {
  sensitivity?: number;
  stiffness?: number;
  damping?: number;
  tiltIntensity?: number;
}

interface MouseReactiveReturn {
  ref: React.RefObject<HTMLDivElement>;
  x: MotionValue<number>;
  y: MotionValue<number>;
  rotateX: MotionValue<number>;
  rotateY: MotionValue<number>;
  handleMouseMove: (e: MouseEvent<HTMLDivElement>) => void;
  handleMouseLeave: () => void;
}

/**
 * Custom hook for mouse-reactive animations
 * Creates smooth parallax and tilt effects based on mouse position
 * 
 * @param config - Configuration options
 * @returns Object with ref, motion values, and event handlers
 */
export function useMouseReactive(config: MouseReactiveConfig = {}): MouseReactiveReturn {
  const {
    sensitivity = 35,
    stiffness = 75,
    damping = 25,
    tiltIntensity = 1.5
  } = config;

  const ref = useRef<HTMLDivElement>(null);
  const shouldReduceMotion = useReducedMotion();
  
  // Mouse tracking motion values
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  // Spring physics for smooth animations
  const springConfig = { stiffness, damping };
  const x = useSpring(mouseX, springConfig);
  const y = useSpring(mouseY, springConfig);

  // Convert to 2D-only translation to completely eliminate Chrome 3D text blur
  const rotateX = useTransform(y, [-20, 20], [0, 0]);
  const rotateY = useTransform(x, [-20, 20], [0, 0]);

  const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
    if (!ref.current || shouldReduceMotion) return;
    
    const rect = ref.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    // Calculate mouse position relative to element center
    mouseX.set((e.clientX - centerX) / sensitivity);
    mouseY.set((e.clientY - centerY) / sensitivity);
  };

  const handleMouseLeave = () => {
    // Reset to center position
    mouseX.set(0);
    mouseY.set(0);
  };

  return {
    ref,
    x,
    y,
    rotateX,
    rotateY,
    handleMouseMove,
    handleMouseLeave
  };
}
