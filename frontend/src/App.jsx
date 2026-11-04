import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ResumeUpload from './components/ResumeUpload';
import LoadingState from './components/LoadingState';
import ScoreCard from './components/ScoreCard';
import SkillsCard from './components/SkillsCard';
import JobMatchCard from './components/JobMatchCard';
import ResumeSectionsCard from './components/ResumeSectionsCard';
import StrengthsCard from './components/StrengthsCard';
import WeaknessesCard from './components/WeaknessesCard';
import RecommendationsCard from './components/RecommendationsCard';
import DetailedFeedbackCard from './components/DetailedFeedbackCard';
import AtsTextInspector from './components/AtsTextInspector';
import JobDescriptionMatcher from './components/JobDescriptionMatcher';
import FormatAnalyzer from './components/FormatAnalyzer';
import HowItWorks from './components/HowItWorks';
import About from './components/About';
import AIOrbBackground from './components/AIOrbBackground';
import InteractiveHeroScanner from './components/InteractiveHeroScanner';
import RealTimeResumeUpdater from './components/RealTimeResumeUpdater';
import HistoryDrawer from './components/HistoryDrawer';
import ErrorBoundary from './components/ErrorBoundary';
import { analyzeResume } from './services/api';
import { generatePdfReport } from './services/reportGenerator';

import {
  Award,
  Target,
  Bot,
  Cpu,
  Sparkles,
  ArrowRight,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  X,
  Download
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('hero'); // 'hero', 'dashboard', 'job-matcher', 'how-it-works', 'about'
  const [selectedFile, setSelectedFile] = useState(null);
  const [targetRole, setTargetRole] = useState('auto');
  const [analysisMode, setAnalysisMode] = useState('without_role'); // 'with_role' | 'without_role'
  const [isLoading, setIsLoading] = useState(false);
  const [aiState, setAiState] = useState('idle'); // 'idle', 'processing', 'completed'
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);

  const handleAnalyze = async (fileOverride = null) => {
    const fileToUse = fileOverride || selectedFile;
    if (!fileToUse) {
      setError('Please upload a resume PDF file before analyzing.');
      return;
    }

    setError('');
    setIsLoading(true);
    setAiState('processing');
    setActiveTab('dashboard'); // Seamlessly transition to dashboard view

    try {
      const roleToSend = analysisMode === 'without_role' ? 'auto' : targetRole;
      const data = await analyzeResume(fileToUse, roleToSend);
      setResult(data);
      setAiState('completed');
      setActiveTab('dashboard');
    } catch (err) {
      setError(err.message || 'Failed to analyze resume. Please try again.');
      setAiState('idle');
      setActiveTab('dashboard');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setResult(null);
    setError('');
    setIsLoading(false);
    setAiState('idle');
    setActiveTab('hero');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 relative flex flex-col font-sans selection:bg-indigo-600 selection:text-white">
      {/* Background AI Light Animation (Volumetric Light & Floating Crystal Particles) */}
      <AIOrbBackground state={aiState} />

      {/* Header Navigation with Analysis Feature Tabs */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onReset={handleReset}
        hasResult={Boolean(result)}
        aiState={aiState}
        onOpenHistory={() => setIsHistoryOpen(true)}
      />

      <main className="relative z-10 flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
        {/* Global Error Banner */}
        {error && activeTab !== 'dashboard' && (
          <div className="mb-6 p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-center justify-between text-left shadow-sm animate-in fade-in duration-300">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-rose-600 shrink-0" />
              <span>{error}</span>
            </div>
            <button onClick={() => setError('')} className="text-rose-600 hover:text-rose-800 cursor-pointer">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        <ErrorBoundary onReset={handleReset}>
          {/* Major Feature Tab Views */}
          {activeTab === 'hero' ? (
            <InteractiveHeroScanner
              onNavigateToDashboard={() => setActiveTab('dashboard')}
              onNavigateToJobMatcher={() => setActiveTab('job-matcher')}
              onNavigateToHowItWorks={() => setActiveTab('how-it-works')}
            />
          ) : activeTab === 'job-matcher' ? (
          <JobDescriptionMatcher
            selectedFile={selectedFile}
            setSelectedFile={setSelectedFile}
          />
        ) : activeTab === 'format-analyzer' ? (
          <FormatAnalyzer
            selectedFile={selectedFile}
            setSelectedFile={setSelectedFile}
          />
        ) : activeTab === 'how-it-works' ? (
          <HowItWorks onGetStarted={() => setActiveTab('hero')} />
        ) : activeTab === 'about' ? (
          <About onGetStarted={() => setActiveTab('hero')} />
        ) : isLoading ? (
          /* State 1: Loading State */
          <div className="py-12 flex justify-center items-center">
            <LoadingState />
          </div>
        ) : result ? (
          /* State 2: Dashboard Results State (Resume Analysis) */
          <div className="space-y-8 animate-in fade-in duration-500">
            {/* Top Bar Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/90 backdrop-blur-md pb-6">
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 shadow-sm inline-flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> Analysis Complete
                  </span>
                  {result.is_auto_role || result.analysis_mode === 'without_target_role' ? (
                    <span className="text-xs font-bold uppercase tracking-wider text-indigo-700 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-200 shadow-sm inline-flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-amber-500" /> Without Target Role (Auto-Detected)
                    </span>
                  ) : (
                    <span className="text-xs font-bold uppercase tracking-wider text-cyan-700 bg-cyan-50 px-3 py-1 rounded-full border border-cyan-200 shadow-sm inline-flex items-center gap-1.5">
                      <Target className="w-3.5 h-3.5 text-cyan-600" /> Target Role: {result.target_role}
                    </span>
                  )}
                </div>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mt-2">
                  Resume Analysis Dashboard
                </h2>
                <p className="text-sm text-slate-500 mt-1">
                  Evaluation results for <span className="font-semibold text-slate-800">{selectedFile?.name || 'Resume'}</span>
                  {result.is_auto_role || result.analysis_mode === 'without_target_role' ? (
                    <span> • Auto-detected best fit track: <span className="font-semibold text-indigo-600">{result.target_role}</span></span>
                  ) : (
                    <span> tailored for <span className="font-semibold text-indigo-600">{result.target_role}</span></span>
                  )}
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2 sm:gap-3">
                <button
                  onClick={() => generatePdfReport(result, selectedFile?.name || 'Resume')}
                  className="inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-white hover:bg-slate-50 text-indigo-700 font-semibold text-xs border border-indigo-200 shadow-sm transition-all cursor-pointer"
                  title="Export a printable PDF diagnostic audit report"
                >
                  <Download className="w-4 h-4 mr-1.5 text-indigo-600" />
                  Export PDF Report
                </button>

                <button
                  onClick={() => setActiveTab('job-matcher')}
                  className="inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-cyan-50 hover:bg-cyan-100 text-cyan-700 font-semibold text-xs border border-cyan-200 shadow-sm transition-all cursor-pointer"
                >
                  <Target className="w-4 h-4 mr-1.5 text-cyan-600" />
                  Match Job Description
                </button>

                <button
                  onClick={handleReset}
                  className="inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-md shadow-indigo-600/20 transition-all cursor-pointer"
                >
                  <RefreshCw className="w-4 h-4 mr-1.5" />
                  Analyze Another
                </button>
              </div>
            </div>

            {/* Real-Time Live Resume Evaluator & Optimizer */}
            <RealTimeResumeUpdater
              selectedFile={selectedFile}
              setSelectedFile={setSelectedFile}
              targetRole={targetRole}
              setTargetRole={setTargetRole}
              analysisMode={analysisMode}
              setAnalysisMode={setAnalysisMode}
              result={result}
              setResult={setResult}
              setAiState={setAiState}
            />

            {/* Top Summary Cards (4 Cards) */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
              {/* Card 1: Resume Score */}
              <div className="bg-white/90 backdrop-blur-md rounded-2xl p-5 border border-slate-200/90 shadow-sm hover:shadow-md transition-all duration-300 flex items-center justify-between group">
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Resume Score</p>
                  <p className="text-2xl sm:text-3xl font-black text-slate-900 mt-1">
                    {result.resume_score} <span className="text-sm font-medium text-slate-400">/ 100</span>
                  </p>
                </div>
                <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center border border-indigo-200 group-hover:scale-105 transition-transform">
                  <Award className="w-6 h-6" />
                </div>
              </div>

              {/* Card 2: Job Match */}
              <div className="bg-white/90 backdrop-blur-md rounded-2xl p-5 border border-slate-200/90 shadow-sm hover:shadow-md transition-all duration-300 flex items-center justify-between group">
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Job Match</p>
                  <p className="text-2xl sm:text-3xl font-black text-indigo-600 mt-1">
                    {result.job_match_score}%
                  </p>
                </div>
                <div className="w-12 h-12 rounded-2xl bg-violet-50 text-violet-600 flex items-center justify-center border border-violet-200 group-hover:scale-105 transition-transform">
                  <Target className="w-6 h-6" />
                </div>
              </div>

              {/* Card 3: Predicted Role */}
              <div className="bg-white/90 backdrop-blur-md rounded-2xl p-5 border border-slate-200/90 shadow-sm hover:shadow-md transition-all duration-300 flex items-center justify-between group">
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Predicted Role</p>
                  <p className="text-base font-bold text-slate-900 mt-1 truncate max-w-[150px]" title={result.predicted_category}>
                    {result.predicted_category}
                  </p>
                </div>
                <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center border border-emerald-200 group-hover:scale-105 transition-transform">
                  <Bot className="w-6 h-6" />
                </div>
              </div>

              {/* Card 4: Skills Detected */}
              <div className="bg-white/90 backdrop-blur-md rounded-2xl p-5 border border-slate-200/90 shadow-sm hover:shadow-md transition-all duration-300 flex items-center justify-between group">
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Skills Detected</p>
                  <p className="text-2xl sm:text-3xl font-black text-slate-900 mt-1">
                    {result.detected_skills?.length || 0}
                  </p>
                </div>
                <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center border border-amber-200 group-hover:scale-105 transition-transform">
                  <Cpu className="w-6 h-6" />
                </div>
              </div>
            </div>

            {/* Row 1: Score Gauge & Job Match Breakdown */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ScoreCard
                score={result.resume_score}
                skillScore={result.skill_score}
                sectionScore={result.section_score}
                jobMatchScore={result.job_match_score}
                keywordScore={result.keyword_score}
                scoreBreakdown={result.score_breakdown}
              />
              <JobMatchCard
                targetRole={result.target_role}
                jobMatchScore={result.job_match_score}
                matchedSkills={result.matched_skills}
                missingSkills={result.missing_skills}
                isAutoRole={result.is_auto_role}
              />
            </div>

            {/* Row 2: Skills Overview & Structure Analysis */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <SkillsCard
                detectedSkills={result.detected_skills}
                missingSkills={result.missing_skills}
              />
              <ResumeSectionsCard sections={result.sections} />
            </div>

            {/* Row 3: Strengths & Areas to Improve */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <StrengthsCard
                strengths={result.strengths}
                verifiedStrengths={result.llm_feedback?.verified_strengths}
              />
              <WeaknessesCard weaknesses={result.weaknesses} />
            </div>

            {/* Row 4: Recommendations Card */}
            <RecommendationsCard recommendations={result.recommendations} />

            {/* Row 5: ATS Contact & Raw Text Inspector */}
            <AtsTextInspector
              contactInfo={result.contact_info}
              rawText={result.extracted_text}
            />

            {/* Row 6: Deep Multi-Dimensional Feedback Hub */}
            <DetailedFeedbackCard
              detailedFeedback={result.detailed_feedback}
              targetRole={result.target_role}
              recommendations={result.recommendations}
              llmFeedback={result.llm_feedback}
              ragCitations={result.rag_citations}
              scoreBreakdown={result.score_breakdown}
            />

            {/* Bottom Navigation Buttons */}
            <div className="pt-6 flex flex-wrap items-center justify-center gap-4">
              <button
                onClick={() => setActiveTab('job-matcher')}
                className="inline-flex items-center px-6 py-3 rounded-xl bg-cyan-50 hover:bg-cyan-100 text-cyan-700 font-semibold text-sm shadow-sm border border-cyan-200 transition-all cursor-pointer"
              >
                <Target className="w-4 h-4 mr-2 text-cyan-600" />
                Match Specific Job Description
              </button>

              <button
                onClick={handleReset}
                className="inline-flex items-center px-6 py-3 rounded-xl bg-white hover:bg-slate-50 text-slate-700 font-semibold text-sm shadow-sm border border-slate-200 transition-all cursor-pointer"
              >
                <RefreshCw className="w-4 h-4 mr-2 text-slate-500" />
                Analyze Another Resume
              </button>
            </div>
          </div>
        ) : (
          /* State 3: Upload & Landing Screen (Resume Analysis Tab) */
          <div className="space-y-8 py-4 max-w-3xl mx-auto">
            <ResumeUpload
              selectedFile={selectedFile}
              setSelectedFile={setSelectedFile}
              error={error}
              setError={setError}
              onAutoAnalyze={handleAnalyze}
            />

            {/* Analyze Button */}
            <div className="text-center pt-2">
              <button
                onClick={handleAnalyze}
                disabled={!selectedFile}
                className={`w-full sm:w-auto min-w-[240px] inline-flex items-center justify-center px-8 py-4 rounded-xl text-base font-bold text-white transition-all duration-300 shadow-xl ${
                  selectedFile
                    ? 'bg-gradient-to-r from-indigo-600 via-indigo-500 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 shadow-indigo-500/30 hover:shadow-cyan-500/40 cursor-pointer transform hover:-translate-y-0.5 active:translate-y-0'
                    : 'bg-slate-200 text-slate-400 border border-slate-300 cursor-not-allowed shadow-none'
                }`}
              >
                Analyze Resume <ArrowRight className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" />
              </button>
            </div>
          </div>
        )}
        </ErrorBoundary>
      </main>

      {/* Footer */}
      <footer className="relative z-10 bg-white/90 backdrop-blur-md border-t border-slate-200 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4">
          <p>© {new Date().getFullYear()} Resume Reviewer. AI-Powered Resume Analysis & Job Matcher.</p>
        </div>
      </footer>

      {/* Supabase History Drawer */}
      <HistoryDrawer
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        onLoadReview={(loadedReview) => {
          setResult(loadedReview);
          setActiveTab('dashboard');
        }}
      />
    </div>
  );
}
