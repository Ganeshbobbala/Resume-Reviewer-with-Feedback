import React from 'react';
import { ThumbsUp, CheckCircle, Quote, Sparkles } from 'lucide-react';

export default function StrengthsCard({ strengths = [], verifiedStrengths = [] }) {
  const hasVerified = Array.isArray(verifiedStrengths) && verifiedStrengths.length > 0;

  return (
    <div className="bg-white/95 backdrop-blur-md rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center border border-emerald-200">
            <ThumbsUp className="w-4 h-4" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Your Strengths</h3>
        </div>
        {hasVerified && (
          <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200 inline-flex items-center gap-1">
            <Sparkles className="w-3 h-3" /> Evidence-Backed
          </span>
        )}
      </div>

      <ul className="space-y-3">
        {hasVerified ? (
          verifiedStrengths.map((item, idx) => (
            <li key={idx} className="p-3.5 rounded-xl bg-emerald-50/70 border border-emerald-200/90 text-xs space-y-1.5">
              <div className="flex items-start text-emerald-950 font-bold">
                <CheckCircle className="w-4 h-4 text-emerald-600 mr-2 mt-0.5 shrink-0" />
                <span>{item.strength}</span>
              </div>
              {item.supporting_excerpt && (
                <div className="flex items-start gap-1.5 text-[11px] text-emerald-800/90 italic pl-6 font-medium">
                  <Quote className="w-3 h-3 text-emerald-500 shrink-0 mt-0.5" />
                  <span>"{item.supporting_excerpt}"</span>
                </div>
              )}
            </li>
          ))
        ) : strengths.length > 0 ? (
          strengths.map((strength, idx) => (
            <li key={idx} className="flex items-start text-xs font-medium text-emerald-950 bg-emerald-50/80 p-3 rounded-xl border border-emerald-200/90">
              <CheckCircle className="w-4 h-4 text-emerald-600 mr-2.5 mt-0.5 shrink-0" />
              <span>{strength}</span>
            </li>
          ))
        ) : (
          <li className="text-xs text-slate-500 italic">No specific key strengths identified.</li>
        )}
      </ul>
    </div>
  );
}
