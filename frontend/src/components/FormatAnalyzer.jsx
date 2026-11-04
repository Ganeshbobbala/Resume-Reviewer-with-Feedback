import React, { useState, useRef } from 'react';
import { Layout, FileText, Check, X, AlertCircle, Loader2, UploadCloud, FileCheck } from 'lucide-react';
import { analyzeResumeFormat } from '../services/api';
import ResumeFormatCard from './ResumeFormatCard';

export default function FormatAnalyzer({ selectedFile, setSelectedFile }) {
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleFileValidation = (file) => {
    setError('');
    if (!file) return;

    const isPdf = file.name.toLowerCase().endsWith('.pdf') || file.type.includes('pdf');
    const isDocx = file.name.toLowerCase().endsWith('.docx') || file.type.includes('word') || file.type.includes('officedocument');

    if (!isPdf && !isDocx) {
      setError('Please upload a valid PDF (.pdf) or Word (.docx) document.');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('File size exceeds 10 MB limit.');
      return;
    }

    setSelectedFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileValidation(e.dataTransfer.files[0]);
    }
  };

  const handleAnalyzeFormat = async () => {
    if (!selectedFile) {
      setError('Please upload a resume (PDF or Word) before checking format.');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      const data = await analyzeResumeFormat(selectedFile);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze format.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="text-center space-y-3">
        <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Resume Format Analyzer
        </h2>
        <p className="text-sm sm:text-base text-slate-600 max-w-xl mx-auto">
          Check your resume structure, readability, sections, and content quality.
        </p>
      </div>

      {/* Error Notice */}
      {error && (
        <div className="w-full max-w-2xl mx-auto p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-center justify-between text-left shadow-sm">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
          <button onClick={() => setError('')} className="text-rose-600 hover:text-rose-800 cursor-pointer">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Upload Dropzone (Matches ResumeUpload Design & Sizing Exactly) */}
      <div className="w-full max-w-2xl mx-auto text-center">
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          onChange={(e) => {
            if (e.target.files && e.target.files[0]) {
              handleFileValidation(e.target.files[0]);
            }
          }}
          className="hidden"
        />

        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`relative cursor-pointer rounded-2xl border-2 border-dashed transition-all duration-300 p-8 sm:p-12 flex flex-col items-center justify-center backdrop-blur-md shadow-sm ${
            isDragging
              ? 'border-indigo-500 bg-indigo-50/60 ring-4 ring-indigo-500/10'
              : selectedFile
              ? 'border-emerald-400 bg-emerald-50/40'
              : 'border-slate-300 bg-white/95 hover:border-indigo-400 hover:bg-slate-50/80'
          }`}
        >
          {selectedFile ? (
            <div className="flex flex-col items-center space-y-3">
              <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 border border-emerald-200 flex items-center justify-center shadow-sm">
                <FileCheck className="w-8 h-8" />
              </div>
              <div>
                <p className="font-bold text-slate-900 text-base">{selectedFile.name}</p>
                <p className="text-xs text-slate-500 mt-0.5">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB Document
                </p>
              </div>
              <div className="flex items-center gap-2 mt-2">
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    fileInputRef.current?.click();
                  }}
                  className="text-xs font-semibold text-indigo-700 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-3 py-1.5 rounded-xl border border-indigo-200 transition-colors inline-flex items-center space-x-1 cursor-pointer shadow-xs"
                >
                  Change Resume
                </button>
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedFile(null);
                  }}
                  className="text-xs font-semibold text-rose-700 hover:text-rose-800 bg-rose-50 hover:bg-rose-100 px-3 py-1.5 rounded-xl border border-rose-200 transition-colors inline-flex items-center space-x-1 cursor-pointer shadow-xs"
                >
                  <X className="w-3.5 h-3.5 mr-1" /> Remove Document
                </button>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center space-y-4">
              <div className="w-16 h-16 rounded-2xl bg-indigo-50 text-indigo-600 border border-indigo-200 flex items-center justify-center shadow-sm">
                <UploadCloud className="w-8 h-8" />
              </div>
              <div>
                <p className="text-base sm:text-lg font-bold text-slate-900">
                  Drag & drop your resume (PDF or Word) here
                </p>
                <p className="text-sm text-slate-500 mt-1">or click to browse your files</p>
              </div>
              <div className="inline-flex items-center px-5 py-2.5 rounded-xl text-xs font-bold bg-indigo-600 text-white shadow-md shadow-indigo-600/20 hover:bg-indigo-700 transition-colors">
                Browse Resume
              </div>
              <p className="text-xs text-slate-400">PDF or DOCX files up to 10 MB</p>
            </div>
          )}
        </div>
      </div>

      {/* Action Button Card */}
      <div className="w-full max-w-2xl mx-auto text-center pt-2">
        <button
          onClick={handleAnalyzeFormat}
          disabled={!selectedFile || isLoading}
          className={`w-full sm:w-auto min-w-[240px] inline-flex items-center justify-center px-8 py-3.5 rounded-xl font-bold text-sm sm:text-base text-white transition-all shadow-md ${
            selectedFile && !isLoading
              ? 'bg-gradient-to-r from-emerald-600 via-indigo-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500 shadow-emerald-600/20 cursor-pointer hover:-translate-y-0.5'
              : 'bg-slate-200 text-slate-400 border border-slate-300 cursor-not-allowed'
          }`}
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin text-white" />
              Auditing Resume Format...
            </>
          ) : (
            <>
              <Layout className="w-5 h-5 mr-2" />
              Analyze Format Quality
            </>
          )}
        </button>
      </div>

      {/* Format Result Display */}
      {result && <ResumeFormatCard result={result} />}
    </div>
  );
}

