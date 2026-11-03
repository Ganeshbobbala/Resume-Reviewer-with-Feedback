import React from 'react';
import {
  Sparkles,
  ArrowRight,
  Target,
  Quote
} from 'lucide-react';

/**
 * Minimalist, High-End Designer Hero Interface
 * Clean, spacious, and focused solely on the core value:
 * AI Resume Review & Job Description Matching.
 */
export default function InteractiveHeroScanner({
  onNavigateToDashboard,
  onNavigateToJobMatcher
}) {
  return (
    <div className="relative w-full max-w-5xl mx-auto py-8 sm:py-16 px-4 select-none animate-in fade-in duration-500 text-center">
      
      {/* 1. Category Pill */}
      <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold bg-indigo-50/90 text-indigo-700 border border-indigo-200/80 shadow-xs mb-6 backdrop-blur-md">
        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
        <span>Next-Generation Resume Reviewer</span>
      </div>

      {/* 2. Bold Designer Headline */}
      <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold text-slate-900 tracking-tight leading-[1.1] max-w-4xl mx-auto mb-6">
        Transform Your Resume with{' '}
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 via-indigo-700 to-cyan-600">
          Explainable AI
        </span>
      </h1>

      {/* 3. Subtitle */}
      <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed mb-8">
        Instant Machine Learning role classification, transparent 0–100 scoring, and precision job description alignment tailored for modern tech careers.
      </p>

      {/* 4. Sleek Hero Action Buttons */}
      <div className="flex flex-wrap items-center justify-center gap-3.5 mb-12 sm:mb-16">
        <button
          onClick={onNavigateToDashboard}
          className="inline-flex items-center gap-2 px-7 py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md shadow-indigo-600/25 transition-all cursor-pointer hover:-translate-y-0.5 active:translate-y-0"
        >
          <Sparkles className="w-4 h-4 text-amber-300" />
          <span>Analyze Resume</span>
          <ArrowRight className="w-4 h-4 ml-0.5" />
        </button>

        <button
          onClick={onNavigateToJobMatcher}
          className="inline-flex items-center gap-2 px-6 py-3.5 rounded-2xl bg-white hover:bg-slate-50 text-slate-700 font-semibold text-sm border border-slate-200 shadow-xs transition-all cursor-pointer hover:border-slate-300"
        >
          <Target className="w-4 h-4 text-cyan-600" />
          <span>Compare Job Description</span>
        </button>
      </div>

      {/* 5. Inspirational Philosophy & Mission Quote */}
      <div className="relative p-8 sm:p-10 rounded-3xl bg-white/90 backdrop-blur-md border border-slate-200/90 shadow-sm max-w-3xl mx-auto overflow-hidden text-center group hover:shadow-md transition-all">
        {/* Radiant Ambient Glow & Top Accent Line */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-48 h-1 bg-gradient-to-r from-transparent via-indigo-500 to-transparent" />
        <div className="absolute -top-10 left-1/2 -translate-x-1/2 w-56 h-20 bg-indigo-100/40 rounded-full blur-2xl pointer-events-none" />

        {/* Quote Icon */}
        <div className="relative z-10 w-11 h-11 mx-auto mb-4 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center border border-indigo-100 shadow-xs group-hover:scale-105 transition-transform">
          <Quote className="w-5 h-5 text-indigo-600" />
        </div>

        {/* Quote Body */}
        <blockquote className="relative z-10 text-base sm:text-lg lg:text-xl font-medium text-slate-800 leading-relaxed italic max-w-2xl mx-auto">
          “A resume is more than a document; it is a story of what someone is capable of doing. Through our AI, we transform those capabilities into something tangible for every candidate striving toward their dream career.”
        </blockquote>

        {/* Attribution & Signature */}
        <div className="relative z-10 mt-5 flex items-center justify-center gap-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">
          <span className="w-6 h-[1px] bg-slate-300" />
          <span className="text-indigo-600 font-bold">Resume Reviewer</span>
          <span>•</span>
          <span>Our Guiding Philosophy</span>
          <span className="w-6 h-[1px] bg-slate-300" />
        </div>

        {/* Direct Action Link */}
        <div className="relative z-10 mt-6 pt-1">
          <button
            onClick={onNavigateToDashboard}
            className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-semibold text-xs border border-indigo-200/80 shadow-xs transition-all cursor-pointer hover:-translate-y-0.5"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            <span>Discover Your Capabilities</span>
            <ArrowRight className="w-3.5 h-3.5 ml-0.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
