import React, { useState, useEffect } from 'react';
import { Settings, X, Sparkles, Key, Check, ShieldAlert } from 'lucide-react';

export default function AiSettingsModal({ isOpen, onClose }) {
  const [provider, setProvider] = useState('rule_based');
  const [apiKey, setApiKey] = useState('');
  const [isSaved, setIsSaved] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setProvider(localStorage.getItem('ai_provider') || 'rule_based');
      setApiKey(localStorage.getItem('ai_api_key') || '');
      setIsSaved(false);
    }
  }, [isOpen]);

  const handleSave = () => {
    localStorage.setItem('ai_provider', provider);
    if (apiKey.trim()) {
      localStorage.setItem('ai_api_key', apiKey.trim());
    } else {
      localStorage.removeItem('ai_api_key');
    }
    setIsSaved(true);
    setTimeout(() => {
      setIsSaved(false);
      onClose();
    }, 1000);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 animate-in fade-in duration-200">
      <div className="bg-white rounded-3xl border border-slate-200 shadow-2xl max-w-md w-full p-6 sm:p-7 space-y-5">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center space-x-2.5">
            <div className="w-9 h-9 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center border border-indigo-200">
              <Settings className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-900">AI Intelligence Settings</h3>
              <p className="text-xs text-slate-500">Configure LLM feedback engine</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Engine Selection */}
        <div className="space-y-3">
          <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
            Select AI Feedback Engine:
          </label>

          {/* Option 1: Rule-Based (Default) */}
          <div
            onClick={() => setProvider('rule_based')}
            className={`p-3.5 rounded-2xl border cursor-pointer transition-all ${
              provider === 'rule_based'
                ? 'border-indigo-600 bg-indigo-50/50 ring-2 ring-indigo-500/10'
                : 'border-slate-200 hover:border-slate-300 bg-white'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="font-bold text-xs text-slate-900 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                Local Heuristic Engine (Free & Offline)
              </span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                Recommended
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
              Fast, deterministic, hallucination-free career rubric feedback with 100% privacy. No API key required.
            </p>
          </div>

          {/* Option 2: Google Gemini */}
          <div
            onClick={() => setProvider('gemini')}
            className={`p-3.5 rounded-2xl border cursor-pointer transition-all ${
              provider === 'gemini'
                ? 'border-indigo-600 bg-indigo-50/50 ring-2 ring-indigo-500/10'
                : 'border-slate-200 hover:border-slate-300 bg-white'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="font-bold text-xs text-slate-900">
                Google Gemini 1.5 Flash
              </span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-cyan-50 text-cyan-700 border border-cyan-200">
                Live LLM
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
              Deep, nuanced creative bullet rewrites using Google's lightweight multimodal model.
            </p>
          </div>

          {/* Option 3: OpenAI */}
          <div
            onClick={() => setProvider('openai')}
            className={`p-3.5 rounded-2xl border cursor-pointer transition-all ${
              provider === 'openai'
                ? 'border-indigo-600 bg-indigo-50/50 ring-2 ring-indigo-500/10'
                : 'border-slate-200 hover:border-slate-300 bg-white'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="font-bold text-xs text-slate-900">
                OpenAI GPT-4o-mini
              </span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-violet-50 text-violet-700 border border-violet-200">
                Live LLM
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
              Industry standard executive rephrasing and structured critiques.
            </p>
          </div>
        </div>

        {/* API Key Input (if not rule-based) */}
        {provider !== 'rule_based' && (
          <div className="space-y-1.5 pt-1 animate-in fade-in duration-200">
            <label className="text-xs font-bold text-slate-700 flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Key className="w-3.5 h-3.5 text-indigo-600" />
                {provider === 'gemini' ? 'Gemini API Key' : 'OpenAI API Key'}:
              </span>
              <span className="text-[10px] text-slate-400 font-normal">Stored locally in browser</span>
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder={provider === 'gemini' ? 'AIzaSy...' : 'sk-...'}
              className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <p className="text-[10px] text-slate-500 italic">
              Your API key never leaves your browser except when sent directly to the AI service.
            </p>
          </div>
        )}

        {/* Save Button */}
        <div className="pt-2 flex items-center justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors cursor-pointer"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs shadow-md shadow-indigo-600/20 transition-all cursor-pointer"
          >
            {isSaved ? <Check className="w-4 h-4 text-emerald-300" /> : <Settings className="w-4 h-4" />}
            <span>{isSaved ? 'Saved!' : 'Save Settings'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}

