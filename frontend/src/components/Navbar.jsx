import React from 'react';
import {
  FileText,
  Sparkles,
  RefreshCw,
  LayoutDashboard,
  Target
} from 'lucide-react';

export default function Navbar({
  activeTab,
  setActiveTab,
  onReset,
  hasResult,
  aiState = 'idle'
}) {
  const isDusk = activeTab === 'hero';

  return (
    <header className={`sticky top-0 z-50 backdrop-blur-md transition-all duration-300 ${
      isDusk
        ? 'bg-[#080915]/85 border-b border-indigo-950/70 text-slate-100 shadow-md shadow-black/30'
        : 'bg-white/90 border-b border-slate-200 text-slate-900 shadow-sm'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo / Brand */}
          <div
            className="flex items-center space-x-3 cursor-pointer group shrink-0"
            onClick={() => setActiveTab('hero')}
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 via-indigo-600 to-indigo-700 flex items-center justify-center text-white shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform border border-amber-400/30">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <span className={`font-bold text-lg tracking-tight transition-colors ${
                isDusk ? 'text-white' : 'text-slate-900'
              }`}>
                Resume Reviewer
              </span>
            </div>
          </div>

          {/* Analysis Feature Nav Tabs */}
          <nav className="flex items-center space-x-1 sm:space-x-2 text-xs sm:text-sm font-medium">
            <button
              onClick={() => setActiveTab('hero')}
              className={`px-3 py-2 rounded-xl transition-all flex items-center gap-1.5 cursor-pointer ${
                activeTab === 'hero'
                  ? 'bg-amber-950/40 text-amber-300 border border-amber-500/40 font-bold shadow-xs'
                  : isDusk
                  ? 'text-slate-400 hover:text-slate-200 hover:bg-indigo-950/40'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Sparkles className="w-4 h-4 text-amber-400" />
              <span>Home</span>
            </button>

            <button
              onClick={() => setActiveTab('dashboard')}
              className={`px-3 py-2 rounded-xl transition-all flex items-center gap-1.5 cursor-pointer ${
                activeTab === 'dashboard'
                  ? 'bg-indigo-50 text-indigo-700 border border-indigo-200 font-bold shadow-sm'
                  : isDusk
                  ? 'text-slate-400 hover:text-slate-200 hover:bg-indigo-950/40'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <LayoutDashboard className="w-4 h-4 text-indigo-400 sm:text-indigo-600" />
              <span>Resume Analysis</span>
            </button>

            <button
              onClick={() => setActiveTab('job-matcher')}
              className={`px-3 py-2 rounded-xl transition-all flex items-center gap-1.5 cursor-pointer ${
                activeTab === 'job-matcher'
                  ? 'bg-indigo-50 text-indigo-700 border border-indigo-200 font-bold shadow-sm'
                  : isDusk
                  ? 'text-slate-400 hover:text-slate-200 hover:bg-indigo-950/40'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Target className="w-4 h-4 text-cyan-400 sm:text-cyan-600" />
              <span>Job Matcher</span>
            </button>
          </nav>

          {/* Right Links & Action */}
          <div className="flex items-center space-x-2 sm:space-x-3 text-xs">
            <button
              onClick={() => setActiveTab('how-it-works')}
              className={`hidden md:inline-block px-2 py-1 transition-colors cursor-pointer ${
                isDusk ? 'text-slate-400 hover:text-slate-200' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              How It Works
            </button>
            <button
              onClick={() => setActiveTab('about')}
              className={`hidden md:inline-block px-2 py-1 transition-colors cursor-pointer ${
                isDusk ? 'text-slate-400 hover:text-slate-200' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              About
            </button>

            {hasResult && activeTab === 'dashboard' && (
              <button
                onClick={onReset}
                className="inline-flex items-center px-3 py-1.5 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition-all border border-slate-200 cursor-pointer"
              >
                <RefreshCw className="w-3.5 h-3.5 mr-1 text-slate-500" />
                Reset
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
