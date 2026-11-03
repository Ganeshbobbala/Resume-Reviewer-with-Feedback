import React, { useState } from 'react';
import {
  Sparkles,
  ArrowRight,
  Target,
  Quote,
  Radio,
  Sliders,
  Compass,
  FileCheck2,
  ChevronRight
} from 'lucide-react';

/**
 * Scrolltide "Cosmos Dusk" Interface (https://www.scrolltide.co/#s-cosmos-dusk)
 * 
 * "A 16:9 footer that is a living painted photograph — indigo hills bleed into
 * paper like ink above a dusk field of cosmos, a man tunes a radio under a
 * hanging bulb as the camera slowly pushes in, and the links sit pinned in
 * the dark flowers."
 */
export default function InteractiveHeroScanner({
  onNavigateToDashboard,
  onNavigateToJobMatcher
}) {
  const [selectedFreq, setSelectedFreq] = useState('94.2');
  const [activeSignal, setActiveSignal] = useState('Frontend & Full Stack');

  const frequencies = [
    { freq: '88.5', label: 'Systems & Cloud', role: 'DevOps Engineer' },
    { freq: '94.2', label: 'Full Stack & Web', role: 'Full Stack Developer' },
    { freq: '99.8', label: 'Data & AI / ML', role: 'Data Scientist' },
    { freq: '104.6', label: 'Product & Design', role: 'UI/UX Designer' },
  ];

  return (
    <div className="relative w-full max-w-6xl mx-auto py-4 sm:py-10 px-2 sm:px-4 select-none animate-in fade-in duration-700 text-center">
      
      {/* 16:9 Cinematic Theater Stage */}
      <div className="relative w-full rounded-3xl overflow-hidden border border-indigo-900/50 bg-gradient-to-b from-[#080915] via-[#0d0f22] to-[#171226] shadow-2xl shadow-indigo-950/70 p-6 sm:p-12 lg:p-16">
        
        {/* Paper Grain & Watercolor Ink Texture Overlay */}
        <div 
          className="absolute inset-0 pointer-events-none opacity-20 mix-blend-overlay"
          style={{
            backgroundImage: `radial-gradient(circle at 50% 30%, rgba(251,191,36,0.15) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(99,102,241,0.2) 0%, transparent 50%)`,
          }}
        />

        {/* Cinematic Hanging Bulb with Filament Glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 flex flex-col items-center pointer-events-none z-20">
          {/* Wire */}
          <div className="w-[1.5px] h-12 sm:h-20 bg-gradient-to-b from-slate-700 via-amber-900/60 to-amber-700/80" />
          
          {/* Socket */}
          <div className="w-3.5 h-3.5 bg-gradient-to-b from-slate-800 to-amber-950 rounded-t-sm border-t border-amber-500/30" />
          
          {/* Glass Bulb with Glowing Filament */}
          <div className="relative -mt-0.5">
            <div className="w-5 h-6 rounded-b-full rounded-t-sm bg-amber-100/90 border border-amber-300/80 shadow-[0_0_24px_rgba(251,191,36,0.9),0_0_60px_rgba(245,158,11,0.5)] flex items-center justify-center">
              {/* Inner glowing filament loop */}
              <div className="w-2 h-2.5 rounded-full border border-amber-500/80 bg-amber-300 animate-pulse" />
            </div>
            
            {/* Volumetric pool of warm twilight light from the bulb */}
            <div className="absolute -top-6 -left-20 w-44 h-48 rounded-full bg-gradient-to-b from-amber-400/25 via-amber-300/10 to-transparent blur-2xl pointer-events-none" />
          </div>
        </div>

        {/* Distant Indigo Hills Bleeding into Paper (Layered SVG Horizon) */}
        <div className="absolute inset-x-0 bottom-0 h-64 sm:h-80 pointer-events-none overflow-hidden opacity-85">
          {/* Distant Hills Watercolor Bleed */}
          <svg
            className="absolute bottom-16 sm:bottom-24 w-full h-40 text-indigo-950/40"
            viewBox="0 0 1200 320"
            preserveAspectRatio="none"
            fill="currentColor"
          >
            <path d="M0,192 C150,120 350,240 500,160 C650,80 800,200 950,140 C1100,80 1150,120 1200,160 L1200,320 L0,320 Z" />
          </svg>

          {/* Midground Indigo Hills with Ink Bleed Softness */}
          <svg
            className="absolute bottom-10 sm:bottom-16 w-full h-48 text-[#141634]/70 blur-[1px]"
            viewBox="0 0 1200 320"
            preserveAspectRatio="none"
            fill="currentColor"
          >
            <path d="M0,224 C200,140 400,260 600,180 C800,100 1000,220 1200,160 L1200,320 L0,320 Z" />
          </svg>

          {/* Foreground Dusk Field of Cosmos Floral Silhouettes */}
          <svg
            className="absolute bottom-0 w-full h-32 sm:h-44 text-[#1a1329]"
            viewBox="0 0 1200 240"
            preserveAspectRatio="none"
            fill="currentColor"
          >
            {/* Field bed */}
            <path d="M0,140 C180,120 360,170 540,135 C720,100 900,160 1080,130 C1140,120 1180,135 1200,140 L1200,240 L0,240 Z" />
            
            {/* Cosmos flowers stems and blooms scattered across the field */}
            <g opacity="0.65" stroke="currentColor" strokeWidth="1.5">
              {/* Flower 1 */}
              <line x1="80" y1="145" x2="75" y2="70" />
              <circle cx="75" cy="68" r="7" fill="#3b224c" />
              <circle cx="75" cy="68" r="2.5" fill="#f59e0b" />
              
              {/* Flower 2 */}
              <line x1="160" y1="160" x2="165" y2="90" />
              <circle cx="165" cy="88" r="6" fill="#442a5a" />
              <circle cx="165" cy="88" r="2" fill="#fbbf24" />

              {/* Flower 3 */}
              <line x1="310" y1="150" x2="305" y2="60" />
              <circle cx="305" cy="58" r="8" fill="#361d47" />
              <circle cx="305" cy="58" r="3" fill="#f59e0b" />

              {/* Flower 4 */}
              <line x1="480" y1="140" x2="485" y2="75" />
              <circle cx="485" cy="73" r="6.5" fill="#4a2e63" />
              <circle cx="485" cy="73" r="2" fill="#fbbf24" />

              {/* Flower 5 */}
              <line x1="720" y1="130" x2="715" y2="55" />
              <circle cx="715" cy="53" r="8" fill="#391e4a" />
              <circle cx="715" cy="53" r="3" fill="#f59e0b" />

              {/* Flower 6 */}
              <line x1="890" y1="150" x2="895" y2="80" />
              <circle cx="895" cy="78" r="7" fill="#4c2f66" />
              <circle cx="895" cy="78" r="2.5" fill="#fbbf24" />

              {/* Flower 7 */}
              <line x1="1040" y1="135" x2="1035" y2="65" />
              <circle cx="1035" cy="63" r="7.5" fill="#381d49" />
              <circle cx="1035" cy="63" r="2.5" fill="#f59e0b" />

              {/* Flower 8 */}
              <line x1="1140" y1="145" x2="1145" y2="75" />
              <circle cx="1145" cy="73" r="6" fill="#452b5c" />
              <circle cx="1145" cy="73" r="2" fill="#fbbf24" />
            </g>
          </svg>
        </div>

        {/* Foreground Cinematic Hero Content */}
        <div className="relative z-10 max-w-4xl mx-auto pt-10 sm:pt-14 space-y-6 sm:space-y-8">
          
          {/* Subtle Filament Aura Header Pill */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-medium text-amber-200 bg-amber-950/40 border border-amber-500/30 backdrop-blur-md shadow-[0_0_15px_rgba(245,158,11,0.15)]">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse" />
            <span className="tracking-wide">Tuned to {selectedFreq} MHz • {activeSignal}</span>
          </div>

          {/* Living Painted Typography Headline */}
          <div className="space-y-3">
            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white leading-[1.08]">
              Transform Your Resume in the{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-rose-200 to-indigo-200 drop-shadow-[0_0_25px_rgba(251,191,36,0.2)]">
                Dusk of Career Discovery
              </span>
            </h1>
            <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed font-light">
              A living painted interface where AI precision meets human capability. Tune your profile against real hiring frequencies with explainable 0–100 scoring.
            </p>
          </div>

          {/* Interactive Vintage Radio Frequency Dial (A Man Tunes a Radio...) */}
          <div className="max-w-xl mx-auto p-4 rounded-2xl bg-[#0b0d1e]/80 border border-indigo-900/60 backdrop-blur-xl shadow-lg space-y-3">
            <div className="flex items-center justify-between text-[11px] font-semibold text-amber-300/80 px-1">
              <span className="flex items-center gap-1.5 uppercase tracking-wider">
                <Radio className="w-3.5 h-3.5 text-amber-400" /> Career Frequency Band
              </span>
              <span className="text-slate-400 font-mono">FM / MHz</span>
            </div>

            {/* Dial Tuner Bar with Frequency Stations */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {frequencies.map((item) => (
                <button
                  key={item.freq}
                  onClick={() => {
                    setSelectedFreq(item.freq);
                    setActiveSignal(item.label);
                  }}
                  className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer ${
                    selectedFreq === item.freq
                      ? 'bg-amber-500/15 border-amber-400/60 text-amber-200 shadow-[0_0_12px_rgba(245,158,11,0.2)]'
                      : 'bg-indigo-950/30 border-indigo-900/40 text-slate-400 hover:text-slate-200 hover:border-indigo-700/60'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-amber-400">{item.freq}</span>
                    {selectedFreq === item.freq && (
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-ping" />
                    )}
                  </div>
                  <span className="block text-[11px] font-medium mt-1 truncate">{item.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Pinned Links in the Dark Flowers (Actions) */}
          <div className="pt-2 flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={onNavigateToDashboard}
              className="inline-flex items-center gap-2.5 px-8 py-4 rounded-2xl bg-gradient-to-r from-amber-500 via-amber-400 to-amber-500 hover:from-amber-400 hover:to-amber-300 text-slate-950 font-bold text-sm shadow-[0_0_30px_rgba(245,158,11,0.35)] transition-all cursor-pointer transform hover:-translate-y-0.5 active:translate-y-0"
            >
              <Sparkles className="w-4 h-4 text-amber-950" />
              <span>Analyze Your Resume</span>
              <ArrowRight className="w-4 h-4 ml-0.5" />
            </button>

            <button
              onClick={onNavigateToJobMatcher}
              className="inline-flex items-center gap-2 px-7 py-4 rounded-2xl bg-[#0c0e22]/90 hover:bg-[#121533] text-slate-200 font-semibold text-sm border border-indigo-800/60 shadow-md backdrop-blur-md transition-all cursor-pointer hover:border-indigo-600 hover:text-white"
            >
              <Target className="w-4 h-4 text-amber-400" />
              <span>Match Specific Job Locus</span>
            </button>
          </div>

          {/* Pinned Botanical Links in the Dusk Cosmos Bed */}
          <div className="pt-6 pb-2 border-t border-indigo-900/40 flex flex-wrap items-center justify-center gap-2 text-xs text-slate-300">
            <span className="text-[11px] text-amber-300/70 font-semibold mr-1">Pinned tracks:</span>
            {[
              'Frontend Developer',
              'Full Stack Developer',
              'Backend Developer',
              'Data Scientist',
              'DevOps Engineer',
              'UI/UX Designer'
            ].map((role) => (
              <button
                key={role}
                onClick={onNavigateToDashboard}
                className="px-3 py-1.5 rounded-xl bg-indigo-950/40 hover:bg-indigo-900/60 border border-indigo-800/40 text-slate-300 hover:text-amber-200 transition-colors cursor-pointer text-[11px] backdrop-blur-md"
              >
                {role}
              </button>
            ))}
          </div>

        </div>
      </div>

      {/* Philosophy Quote Pinned Below the 16:9 Theater */}
      <div className="relative mt-10 p-8 sm:p-10 rounded-3xl bg-gradient-to-b from-[#0c0d1e]/90 to-[#120e24]/90 border border-indigo-900/50 shadow-xl max-w-3xl mx-auto overflow-hidden text-center group hover:border-indigo-800/70 transition-all backdrop-blur-md">
        
        {/* Subtle top amber filament accent line */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-48 h-1 bg-gradient-to-r from-transparent via-amber-400/80 to-transparent" />
        <div className="absolute -top-8 left-1/2 -translate-x-1/2 w-56 h-16 bg-amber-400/10 rounded-full blur-xl pointer-events-none" />

        {/* Vintage Quote Icon */}
        <div className="relative z-10 w-11 h-11 mx-auto mb-4 rounded-2xl bg-amber-950/50 text-amber-300 flex items-center justify-center border border-amber-500/30 shadow-xs group-hover:scale-105 transition-transform">
          <Quote className="w-5 h-5 text-amber-400" />
        </div>

        {/* Quote Text */}
        <blockquote className="relative z-10 text-base sm:text-lg lg:text-xl font-light text-slate-200 leading-relaxed italic max-w-2xl mx-auto">
          “A resume is more than a document; it is a story of what someone is capable of doing. Through our AI, we transform those capabilities into something tangible for every candidate striving toward their dream career.”
        </blockquote>

        {/* Attribution & Signature */}
        <div className="relative z-10 mt-5 flex items-center justify-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
          <span className="w-6 h-[1px] bg-slate-700" />
          <span className="text-amber-400 font-bold">Resume Reviewer</span>
          <span>•</span>
          <span>Our Guiding Philosophy</span>
          <span className="w-6 h-[1px] bg-slate-700" />
        </div>

        {/* Direct Action Link */}
        <div className="relative z-10 mt-6 pt-1">
          <button
            onClick={onNavigateToDashboard}
            className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-amber-950/40 hover:bg-amber-900/50 text-amber-200 font-semibold text-xs border border-amber-500/30 shadow-xs transition-all cursor-pointer hover:-translate-y-0.5"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>Discover Your Capabilities</span>
            <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
