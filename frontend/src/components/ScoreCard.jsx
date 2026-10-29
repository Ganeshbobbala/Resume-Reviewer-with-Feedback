import React, { useState } from 'react';
import { Award, Zap, Layers, Target, Search, Info, ChevronDown, ChevronUp, AlertCircle, ShieldCheck } from 'lucide-react';

export default function ScoreCard({
  score,
  skillScore,
  sectionScore,
  jobMatchScore,
  keywordScore,
  scoreBreakdown = {}
}) {
  const [showExplanation, setShowExplanation] = useState(false);

  let statusText = 'Poor';
  let statusColorClass = 'text-rose-700 bg-rose-50 border-rose-200';
  let strokeColor = '#f43f5e'; // rose-500

  if (score >= 80) {
    statusText = 'Excellent';
    statusColorClass = 'text-emerald-700 bg-emerald-50 border-emerald-200';
    strokeColor = '#10b981'; // emerald-500
  } else if (score >= 70) {
    statusText = 'Good';
    statusColorClass = 'text-indigo-700 bg-indigo-50 border-indigo-200';
    strokeColor = '#6366f1'; // indigo-500
  } else if (score >= 50) {
    statusText = 'Needs Improvement';
    statusColorClass = 'text-amber-700 bg-amber-50 border-amber-200';
    strokeColor = '#f59e0b'; // amber-500
  }

  // SVG Circular progress math
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const components = scoreBreakdown.components || {};

  return (
    <div className="bg-white/95 backdrop-blur-md rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <Award className="w-5 h-5 text-indigo-600" /> Overall Resume Score
        </h3>
        <span className={`text-xs font-bold px-2.5 py-1 rounded-full border ${statusColorClass}`}>
          {statusText}
        </span>
      </div>

      {/* Circular Progress Gauge */}
      <div className="flex flex-col items-center justify-center py-2">
        <div className="relative w-36 h-36 flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
            <circle
              cx="60"
              cy="60"
              r={radius}
              stroke="#e2e8f0"
              strokeWidth="10"
              fill="transparent"
            />
            <circle
              cx="60"
              cy="60"
              r={radius}
              stroke={strokeColor}
              strokeWidth="10"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          <div className="absolute flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-black text-slate-900 leading-none">{score}</span>
            <span className="text-xs font-semibold text-slate-400 mt-1">/ 100</span>
          </div>
        </div>
      </div>

      {/* Score Weight Breakdown */}
      <div className="grid grid-cols-2 gap-3 border-t border-slate-100 pt-4 text-xs">
        <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
          <span className="text-slate-500 font-medium flex items-center gap-1 mb-1">
            <Zap className="w-3.5 h-3.5 text-indigo-600" /> Skills (40%)
          </span>
          <span className="font-bold text-slate-900 text-sm">{skillScore} / 100</span>
        </div>

        <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
          <span className="text-slate-500 font-medium flex items-center gap-1 mb-1">
            <Layers className="w-3.5 h-3.5 text-indigo-600" /> Structure (30%)
          </span>
          <span className="font-bold text-slate-900 text-sm">{sectionScore} / 100</span>
        </div>

        <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
          <span className="text-slate-500 font-medium flex items-center gap-1 mb-1">
            <Target className="w-3.5 h-3.5 text-indigo-600" /> Job Match (20%)
          </span>
          <span className="font-bold text-slate-900 text-sm">{jobMatchScore}%</span>
        </div>

        <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
          <span className="text-slate-500 font-medium flex items-center gap-1 mb-1">
            <Search className="w-3.5 h-3.5 text-indigo-600" /> Keywords (10%)
          </span>
          <span className="font-bold text-slate-900 text-sm">{keywordScore} / 100</span>
        </div>
      </div>

      {/* Explainable Scoring Expander */}
      <div className="border-t border-slate-100 pt-3">
        <button
          onClick={() => setShowExplanation(!showExplanation)}
          className="w-full flex items-center justify-between text-xs font-bold text-indigo-700 hover:text-indigo-800 transition-colors py-1 cursor-pointer"
        >
          <span className="flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-indigo-600" />
            Transparent Scoring Breakdown
          </span>
          {showExplanation ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        {showExplanation && (
          <div className="mt-3 p-3.5 rounded-xl bg-indigo-50/50 border border-indigo-100 text-xs space-y-3 animate-in fade-in duration-200">
            <div className="space-y-2">
              {components.skill_match && (
                <div className="flex justify-between items-start">
                  <span className="text-slate-600 font-medium">Skills Component (40%):</span>
                  <span className="font-bold text-slate-900">{components.skill_match.contribution} pts</span>
                </div>
              )}
              {components.resume_structure && (
                <div className="flex justify-between items-start">
                  <span className="text-slate-600 font-medium">Structure Component (30%):</span>
                  <span className="font-bold text-slate-900">{components.resume_structure.contribution} pts</span>
                </div>
              )}
              {components.role_alignment && (
                <div className="flex justify-between items-start">
                  <span className="text-slate-600 font-medium">Role Alignment (20%):</span>
                  <span className="font-bold text-slate-900">{components.role_alignment.contribution} pts</span>
                </div>
              )}
              {components.impact_keywords && (
                <div className="flex justify-between items-start">
                  <span className="text-slate-600 font-medium">Keywords & Verbs (10%):</span>
                  <span className="font-bold text-slate-900">{components.impact_keywords.contribution} pts</span>
                </div>
              )}
            </div>

            <p className="text-[11px] text-slate-500 italic border-t border-indigo-100 pt-2 leading-relaxed">
              {scoreBreakdown.disclaimer ||
                "Diagnostic suitability score based on transparent heuristic rubrics. Not an official ATS score or guarantee of interview selection."}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
