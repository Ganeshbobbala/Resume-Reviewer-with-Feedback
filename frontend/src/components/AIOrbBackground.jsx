import React, { useEffect, useRef } from 'react';

/**
 * AI Background Animation (Supports Daytime Productivity & Scrolltide Cosmos Dusk)
 * 
 * Features:
 *  - Ethereal daylight rays (dashboard view)
 *  - Atmospheric Cosmos Dusk celestial ink-bleed & golden firefly embers (hero view)
 *  - 100% GPU-accelerated canvas particles
 * 
 * Props:
 *  - state: 'idle' | 'processing' | 'completed'
 *  - isDusk: boolean (triggers Scrolltide Cosmos Dusk palette)
 */
export default function AIOrbBackground({ state = 'idle', isDusk = false }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', handleResize);

    // Floating crystal / golden dusk embers
    const particleCount = isDusk ? 36 : 48;
    const particles = Array.from({ length: particleCount }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * (isDusk ? 0.18 : 0.25),
      vy: (isDusk ? -0.08 : -0.15) - Math.random() * (isDusk ? 0.2 : 0.35),
      size: 0.9 + Math.random() * (isDusk ? 1.8 : 1.6),
      baseAlpha: isDusk ? 0.35 + Math.random() * 0.45 : 0.22 + Math.random() * 0.35,
      pulse: Math.random() * Math.PI * 2,
      pulseSpeed: 0.015 + Math.random() * 0.025,
    }));

    const focalX = () => width * 0.5;
    const focalY = () => 40;

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      const fX = focalX();
      const fY = focalY();

      // Background base
      if (isDusk) {
        const bgGrad = ctx.createLinearGradient(0, 0, 0, height);
        bgGrad.addColorStop(0, '#060713');
        bgGrad.addColorStop(0.35, '#0b0d1e');
        bgGrad.addColorStop(0.7, '#141126');
        bgGrad.addColorStop(1, '#191124');
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, width, height);
      } else {
        const bgGrad = ctx.createLinearGradient(0, 0, 0, height);
        bgGrad.addColorStop(0, '#ffffff');
        bgGrad.addColorStop(0.5, '#f8fafc');
        bgGrad.addColorStop(1, '#f1f5f9');
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, width, height);
      }

      // Draw particles
      particles.forEach((p) => {
        p.pulse += p.pulseSpeed;

        if (state === 'processing') {
          const dx = fX - p.x;
          const dy = fY - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;
          p.x += p.vx + (dx / dist) * 0.6;
          p.y += p.vy * 1.8 + (dy / dist) * 0.4;
        } else {
          p.x += p.vx + Math.sin(p.pulse) * 0.15;
          p.y += p.vy;
        }

        if (p.y < -10) {
          p.y = height + 10;
          p.x = Math.random() * width;
        }
        if (p.x < -10) p.x = width + 10;
        if (p.x > width + 10) p.x = -10;

        const distFromCenterBeam = Math.abs(p.x - fX) / (width * 0.5);
        const inBeamBoost = Math.max(0, 1 - distFromCenterBeam * 1.8);

        const pulseFactor = 0.7 + 0.3 * Math.sin(p.pulse);
        let alpha = p.baseAlpha * pulseFactor * (1 + inBeamBoost * 0.9);

        if (state === 'processing') {
          alpha = Math.min(0.9, alpha * 1.4);
        } else if (state === 'completed') {
          alpha = Math.min(0.85, alpha * 1.25);
        }

        let colorRGB;
        if (isDusk) {
          colorRGB = (p.size > 1.8) ? '251, 191, 36' : '192, 132, 252'; // warm golden firefly or cosmos lavender
        } else if (state === 'completed') {
          colorRGB = '16, 185, 129';
        } else if (state === 'processing') {
          colorRGB = '79, 70, 229';
        } else {
          colorRGB = inBeamBoost > 0.4 ? '99, 102, 241' : '14, 165, 233';
        }

        const glowRadius = p.size * (isDusk ? 3.0 : 2.5);
        const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, glowRadius);
        grad.addColorStop(0, `rgba(${colorRGB}, ${alpha})`);
        grad.addColorStop(0.5, `rgba(${colorRGB}, ${alpha * 0.35})`);
        grad.addColorStop(1, `rgba(${colorRGB}, 0)`);

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(p.x, p.y, glowRadius, 0, Math.PI * 2);
        ctx.fill();
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
    };
  }, [state, isDusk]);

  return (
    <div className={`fixed inset-0 pointer-events-none z-0 overflow-hidden select-none transition-colors duration-700 ${
      isDusk ? 'bg-[#060713]' : 'bg-slate-50'
    }`}>
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />

      {/* Atmospheric Aurora / Mist */}
      {isDusk ? (
        <>
          <div className="absolute -top-32 left-1/4 w-[540px] h-[540px] rounded-full bg-indigo-950/40 blur-[140px] pointer-events-none" />
          <div className="absolute -top-32 right-1/4 w-[540px] h-[540px] rounded-full bg-purple-950/30 blur-[140px] pointer-events-none" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[750px] h-[550px] rounded-full bg-amber-500/5 blur-[150px] pointer-events-none" />
        </>
      ) : (
        <>
          <div className="absolute inset-0 bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] [background-size:24px_24px] opacity-40" />
          <div
            className={`absolute -top-32 left-1/4 w-[540px] h-[540px] rounded-full blur-[140px] pointer-events-none transition-all duration-1000 ${
              state === 'processing'
                ? 'bg-cyan-200/60 scale-125'
                : state === 'completed'
                ? 'bg-emerald-200/50 scale-110'
                : 'bg-sky-200/40'
            }`}
          />
          <div
            className={`absolute -top-32 right-1/4 w-[540px] h-[540px] rounded-full blur-[140px] pointer-events-none transition-all duration-1000 ${
              state === 'processing'
                ? 'bg-indigo-200/60 scale-125'
                : state === 'completed'
                ? 'bg-teal-200/50 scale-110'
                : 'bg-indigo-100/50'
            }`}
          />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[750px] h-[550px] rounded-full bg-indigo-50/60 blur-[130px] pointer-events-none" />
        </>
      )}
    </div>
  );
}
