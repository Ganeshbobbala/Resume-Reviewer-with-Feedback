import React, { useState } from 'react';
import { ArrowRight, Copy, Check, Eye, GitCompare } from 'lucide-react';

/**
 * Computes simple word-level diff between original and improved statements.
 */
function computeWordDiff(original = '', improved = '') {
  const origWords = original.split(/\s+/).filter(Boolean);
  const imprWords = improved.split(/\s+/).filter(Boolean);

  const origSet = new Set(origWords.map(w => w.toLowerCase().replace(/[^a-z0-9]/g, '')));
  const imprSet = new Set(imprWords.map(w => w.toLowerCase().replace(/[^a-z0-9]/g, '')));

  const originalElements = origWords.map((word, idx) => {
    const clean = word.toLowerCase().replace(/[^a-z0-9]/g, '');
    const isRemoved = !imprSet.has(clean);
    return {
      word,
      type: isRemoved ? 'removed' : 'neutral'
    };
  });

  const improvedElements = imprWords.map((word, idx) => {
    const clean = word.toLowerCase().replace(/[^a-z0-9]/g, '');
    const isAdded = !origSet.has(clean);
    const isMetric = /[%+$\d]/.test(word) || /\[.*\]/.test(word);
    return {
      word,
      type: isAdded ? (isMetric ? 'metric' : 'added') : 'neutral'
    };
  });

  return { originalElements, improvedElements };
}

export default function BulletDiffViewer({
  originalBullet = '',
  improvedBullet = '',
  styleName = 'Executive Impact',
  tag = 'Recommended'
}) {
  const [showDiff, setShowDiff] = useState(true);
  const [copied, setCopied] = useState(false);

  const { originalElements, improvedElements } = computeWordDiff(originalBullet, improvedBullet);

  const handleCopy = () => {
    navigator.clipboard.writeText(improvedBullet);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="p-4 rounded-2xl bg-white border border-slate-200 hover:border-indigo-300 shadow-xs transition-all space-y-3">
      {/* Header bar */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-bold text-indigo-950">{styleName}</span>
          <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
            {tag}
          </span>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowDiff(!showDiff)}
            className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-semibold text-slate-500 hover:text-indigo-600 hover:bg-slate-100 transition-colors cursor-pointer"
            title="Toggle word-level diff highlight"
          >
            {showDiff ? <Eye className="w-3.5 h-3.5 text-indigo-600" /> : <GitCompare className="w-3.5 h-3.5" />}
            <span>{showDiff ? 'Highlight Diff' : 'Clean View'}</span>
          </button>

          <button
            onClick={handleCopy}
            className="inline-flex items-center gap-1 px-2.5 py-1 rounded text-xs font-semibold text-slate-700 hover:text-indigo-700 hover:bg-indigo-50 border border-slate-200 transition-colors cursor-pointer"
            title="Copy improved bullet point"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        </div>
      </div>

      {/* Side-by-side or stacked diff view */}
      {showDiff ? (
        <div className="space-y-2 text-xs">
          {/* Original Before */}
          <div className="p-2.5 rounded-xl bg-rose-50/50 border border-rose-100/80">
            <span className="text-[10px] font-bold text-rose-700 uppercase tracking-wider block mb-1">
              Before (Weak / Passive):
            </span>
            <p className="leading-relaxed">
              {originalElements.map((item, idx) => (
                <span
                  key={idx}
                  className={item.type === 'removed' ? 'line-through text-rose-600 font-semibold bg-rose-100/80 px-1 py-0.5 rounded mx-0.5' : 'text-slate-600 mr-1'}
                >
                  {item.word}{' '}
                </span>
              ))}
            </p>
          </div>

          {/* Improved After */}
          <div className="p-2.5 rounded-xl bg-emerald-50/50 border border-emerald-100/80">
            <span className="text-[10px] font-bold text-emerald-800 uppercase tracking-wider block mb-1">
              After (Action & Measured Outcome):
            </span>
            <p className="leading-relaxed font-medium">
              {improvedElements.map((item, idx) => (
                <span
                  key={idx}
                  className={
                    item.type === 'metric'
                      ? 'bg-amber-100 text-amber-900 font-bold px-1.5 py-0.5 rounded border border-amber-300 mx-0.5'
                      : item.type === 'added'
                      ? 'bg-emerald-100 text-emerald-900 font-semibold px-1 py-0.5 rounded mx-0.5'
                      : 'text-slate-800 mr-1'
                  }
                >
                  {item.word}{' '}
                </span>
              ))}
            </p>
          </div>
        </div>
      ) : (
        /* Clean text view */
        <p className="text-xs text-slate-800 leading-relaxed font-medium font-sans p-2">
          {improvedBullet}
        </p>
      )}
    </div>
  );
}

