import React, { useState } from 'react';
import {
  FileSearch,
  Mail,
  Phone,
  Linkedin,
  Github,
  Globe,
  AlertTriangle,
  CheckCircle2,
  Copy,
  Check,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

export default function AtsTextInspector({ contactInfo = {}, rawText = '' }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [copied, setCopied] = useState(false);

  const {
    email,
    phone,
    linkedin,
    github,
    portfolio,
    hygiene_alerts = [],
    total_words = 0,
    total_characters = 0
  } = contactInfo;

  const handleCopy = () => {
    if (!rawText) return;
    navigator.clipboard.writeText(rawText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const detectedCount = [email, phone, linkedin, github, portfolio].filter(Boolean).length;

  return (
    <div className="bg-white/95 backdrop-blur-md rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-50 text-cyan-600 border border-cyan-200 flex items-center justify-center shadow-xs">
            <FileSearch className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              ATS Parser & Contact Info Inspector
            </h3>
            <p className="text-xs text-slate-500">
              See exactly how automated recruiter Applicant Tracking Systems (ATS) read your document
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <span className="px-3 py-1 rounded-full font-bold bg-slate-100 text-slate-700 border border-slate-200">
            {detectedCount} / 5 Contact Fields Detected
          </span>
        </div>
      </div>

      {/* Contact Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {/* Email */}
        <div className={`p-3 rounded-xl border text-xs flex items-center space-x-2.5 ${
          email ? 'bg-emerald-50/70 border-emerald-200 text-emerald-950' : 'bg-slate-50 border-slate-200 text-slate-400'
        }`}>
          <Mail className={`w-4 h-4 shrink-0 ${email ? 'text-emerald-600' : 'text-slate-400'}`} />
          <div className="min-w-0 flex-1">
            <span className="text-[10px] font-bold uppercase tracking-wider block opacity-75">Email</span>
            <span className="font-semibold truncate block" title={email || 'Not detected'}>
              {email || 'Missing'}
            </span>
          </div>
        </div>

        {/* Phone */}
        <div className={`p-3 rounded-xl border text-xs flex items-center space-x-2.5 ${
          phone ? 'bg-emerald-50/70 border-emerald-200 text-emerald-950' : 'bg-slate-50 border-slate-200 text-slate-400'
        }`}>
          <Phone className={`w-4 h-4 shrink-0 ${phone ? 'text-emerald-600' : 'text-slate-400'}`} />
          <div className="min-w-0 flex-1">
            <span className="text-[10px] font-bold uppercase tracking-wider block opacity-75">Phone</span>
            <span className="font-semibold truncate block" title={phone || 'Not detected'}>
              {phone || 'Missing'}
            </span>
          </div>
        </div>

        {/* LinkedIn */}
        <div className={`p-3 rounded-xl border text-xs flex items-center space-x-2.5 ${
          linkedin ? 'bg-indigo-50/70 border-indigo-200 text-indigo-950' : 'bg-slate-50 border-slate-200 text-slate-400'
        }`}>
          <Linkedin className={`w-4 h-4 shrink-0 ${linkedin ? 'text-indigo-600' : 'text-slate-400'}`} />
          <div className="min-w-0 flex-1">
            <span className="text-[10px] font-bold uppercase tracking-wider block opacity-75">LinkedIn</span>
            <span className="font-semibold truncate block" title={linkedin || 'Not detected'}>
              {linkedin || 'Missing'}
            </span>
          </div>
        </div>

        {/* GitHub */}
        <div className={`p-3 rounded-xl border text-xs flex items-center space-x-2.5 ${
          github ? 'bg-violet-50/70 border-violet-200 text-violet-950' : 'bg-slate-50 border-slate-200 text-slate-400'
        }`}>
          <Github className={`w-4 h-4 shrink-0 ${github ? 'text-violet-600' : 'text-slate-400'}`} />
          <div className="min-w-0 flex-1">
            <span className="text-[10px] font-bold uppercase tracking-wider block opacity-75">GitHub</span>
            <span className="font-semibold truncate block" title={github || 'Not detected'}>
              {github || 'Missing'}
            </span>
          </div>
        </div>

        {/* Portfolio */}
        <div className={`p-3 rounded-xl border text-xs flex items-center space-x-2.5 ${
          portfolio ? 'bg-cyan-50/70 border-cyan-200 text-cyan-950' : 'bg-slate-50 border-slate-200 text-slate-400'
        }`}>
          <Globe className={`w-4 h-4 shrink-0 ${portfolio ? 'text-cyan-600' : 'text-slate-400'}`} />
          <div className="min-w-0 flex-1">
            <span className="text-[10px] font-bold uppercase tracking-wider block opacity-75">Portfolio</span>
            <span className="font-semibold truncate block" title={portfolio || 'Not detected'}>
              {portfolio || 'Missing'}
            </span>
          </div>
        </div>

        {/* Word Count */}
        <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs flex items-center space-x-2.5 text-slate-700">
          <CheckCircle2 className="w-4 h-4 text-slate-500 shrink-0" />
          <div className="min-w-0 flex-1">
            <span className="text-[10px] font-bold uppercase tracking-wider block text-slate-400">Word Density</span>
            <span className="font-bold text-slate-900">
              {total_words || rawText.split(/\s+/).filter(Boolean).length} words ({total_characters || rawText.length} chars)
            </span>
          </div>
        </div>
      </div>

      {/* Hygiene Warnings */}
      {hygiene_alerts.length > 0 && (
        <div className="space-y-2 pt-1">
          <span className="text-xs font-bold text-amber-800 uppercase tracking-wider flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600" /> ATS Parsing Hygiene Alerts:
          </span>
          <div className="space-y-1.5">
            {hygiene_alerts.map((alert, idx) => (
              <div key={idx} className="p-2.5 rounded-lg bg-amber-50/70 border border-amber-200 text-xs text-amber-900 flex items-start gap-2">
                <span className="font-bold text-amber-700">&bull;</span>
                <span>{alert}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Raw Extracted Plain Text Accordion */}
      <div className="border-t border-slate-100 pt-3">
        <div className="flex items-center justify-between">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="inline-flex items-center gap-1.5 text-xs font-bold text-indigo-700 hover:text-indigo-800 cursor-pointer"
          >
            <span>{isExpanded ? 'Hide Raw ATS Extracted Text' : 'Inspect Raw ATS Extracted Text'}</span>
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {isExpanded && (
            <button
              onClick={handleCopy}
              className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold cursor-pointer border border-slate-200 transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy Plain Text'}</span>
            </button>
          )}
        </div>

        {isExpanded && (
          <div className="mt-3">
            <pre className="p-4 rounded-xl bg-slate-900 text-slate-100 text-xs font-mono max-h-80 overflow-y-auto whitespace-pre-wrap leading-relaxed shadow-inner">
              {rawText || 'No text extracted.'}
            </pre>
            <p className="text-[11px] text-slate-400 mt-2 italic">
              Tip: If words from two columns are mixed together in the same line above, ATS parsers will misread your experience. Use a single-column layout for maximum ATS compatibility.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

