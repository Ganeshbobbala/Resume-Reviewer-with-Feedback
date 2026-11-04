/**
 * Professional Resume Audit Report Generator
 * Exports a publication-quality diagnostic report for printing or saving as PDF.
 */
export function generatePdfReport(result, filename = 'Resume') {
  if (!result) return;

  const score = result.resume_score || 0;
  const targetRole = result.target_role || 'Target Role';
  const predictedRole = result.predicted_category || 'General Engineering';
  const skillScore = result.skill_score || 0;
  const sectionScore = result.section_score || 0;
  const jobMatchScore = result.job_match_score || 0;
  const keywordScore = result.keyword_score || 0;
  const detectedSkills = result.detected_skills || [];
  const missingSkills = result.missing_skills || [];
  const strengths = result.strengths || [];
  const weaknesses = result.weaknesses || [];
  const recommendations = result.recommendations || [];
  const rewrites = result.bullet_rewrites || [];
  const citations = result.rag_citations || [];

  const statusColor = score >= 80 ? '#10b981' : score >= 60 ? '#6366f1' : '#f59e0b';
  const statusLabel = score >= 80 ? 'Competitive' : score >= 60 ? 'Good Potential' : 'Needs Optimization';

  const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Resume Audit Report - ${filename}</title>
  <style>
    @page { size: A4; margin: 15mm; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      color: #1e293b;
      margin: 0;
      padding: 20px;
      font-size: 13px;
      line-height: 1.5;
      background: #ffffff;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 15px;
      margin-bottom: 20px;
    }
    .logo-title {
      font-size: 22px;
      font-weight: 800;
      color: #312e81;
    }
    .meta {
      font-size: 11px;
      color: #64748b;
      text-align: right;
    }
    .score-banner {
      display: flex;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 20px;
      align-items: center;
      justify-content: space-between;
    }
    .score-box {
      text-align: center;
      padding-right: 25px;
      border-right: 1px solid #e2e8f0;
    }
    .score-number {
      font-size: 40px;
      font-weight: 900;
      color: ${statusColor};
      line-height: 1;
    }
    .score-label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      color: #475569;
      margin-top: 4px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      flex: 1;
      padding-left: 20px;
    }
    .metric-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 8px 12px;
    }
    .metric-val {
      font-size: 16px;
      font-weight: 800;
      color: #0f172a;
    }
    .metric-name {
      font-size: 10px;
      color: #64748b;
      font-weight: 600;
      text-transform: uppercase;
    }
    h2 {
      font-size: 15px;
      font-weight: 800;
      color: #1e1b4b;
      margin: 18px 0 8px 0;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 4px;
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      margin: 2px 4px 2px 0;
    }
    .badge-blue { background: #e0e7ff; color: #3730a3; }
    .badge-amber { background: #fef3c7; color: #92400e; }
    .section-list {
      margin: 0;
      padding-left: 18px;
    }
    .section-list li {
      margin-bottom: 5px;
    }
    .rewrite-card {
      background: #f8fafc;
      border-left: 3px solid #6366f1;
      padding: 10px;
      border-radius: 4px;
      margin-bottom: 8px;
      font-size: 12px;
    }
    .disclaimer {
      font-size: 10px;
      color: #94a3b8;
      margin-top: 25px;
      border-top: 1px solid #e2e8f0;
      padding-top: 8px;
      font-style: italic;
    }
    @media print {
      body { padding: 0; }
      .no-print { display: none; }
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="logo-title">Resume Audit & Diagnostic Report</div>
      <div style="font-size: 12px; color: #475569; margin-top: 2px;">
        Evaluated for <strong>${targetRole}</strong> &bull; File: <strong>${filename}</strong>
      </div>
    </div>
    <div class="meta">
      <div>Report Date: ${new Date().toLocaleDateString()}</div>
      <div>ML Track: ${predictedRole}</div>
    </div>
  </div>

  <div class="score-banner">
    <div class="score-box">
      <div class="score-number">${score}</div>
      <div class="score-label">${statusLabel} (/100)</div>
    </div>
    <div class="grid">
      <div class="metric-card">
        <div class="metric-val">${skillScore}/100</div>
        <div class="metric-name">Skills (40%)</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">${sectionScore}/100</div>
        <div class="metric-name">Structure (30%)</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">${jobMatchScore}%</div>
        <div class="metric-name">Job Match (20%)</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">${keywordScore}/100</div>
        <div class="metric-name">Keywords (10%)</div>
      </div>
    </div>
  </div>

  <h2>1. Skills Alignment</h2>
  <div>
    <strong>Detected Skills (${detectedSkills.length}):</strong><br/>
    ${detectedSkills.map(s => `<span class="badge badge-blue">${s}</span>`).join(' ') || 'None detected'}
  </div>
  ${missingSkills.length > 0 ? `
  <div style="margin-top: 8px;">
    <strong style="color: #92400e;">Recommended Skills to Add (${missingSkills.length}):</strong><br/>
    ${missingSkills.map(s => `<span class="badge badge-amber">+ ${s}</span>`).join(' ')}
  </div>` : ''}

  <h2>2. Key Strengths</h2>
  <ul class="section-list">
    ${strengths.map(s => `<li>${s}</li>`).join('') || '<li>Balanced baseline structure detected.</li>'}
  </ul>

  <h2>3. High-Priority Action Items</h2>
  <ul class="section-list">
    ${recommendations.map(r => `<li>${r}</li>`).join('') || '<li>Review resume metrics and quantify outcomes.</li>'}
  </ul>

  ${rewrites.length > 0 ? `
  <h2>4. Model Bullet Point Rewrites</h2>
  ${rewrites.slice(0, 3).map((rw, i) => `
    <div class="rewrite-card">
      <div style="color: #991b1b; text-decoration: line-through; margin-bottom: 3px;">Original: ${rw.original_bullet}</div>
      <div style="color: #065f46; font-weight: 600;">Improved: ${rw.improved_bullet}</div>
    </div>
  `).join('')}
  ` : ''}

  ${citations.length > 0 ? `
  <h2>5. Grounded Career Standards & Citations</h2>
  <ul class="section-list" style="font-size: 11px;">
    ${citations.slice(0, 2).map(c => `<li><strong>${c.source_title} (${c.section}):</strong> ${c.key_principle}</li>`).join('')}
  </ul>
  ` : ''}

  <div class="disclaimer">
    Diagnostic evaluation generated by Resume Reviewer AI System. This report is an educational heuristic assessment weighted on skills (40%), structure (30%), role fit (20%), and keywords (10%). It does not represent an official ATS hiring guarantee.
  </div>
</body>
</html>`;

  // Trigger print-to-PDF window
  const printWindow = window.open('', '_blank');
  if (printWindow) {
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => {
      printWindow.print();
    }, 400);
  } else {
    // Fallback: download HTML report file
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Resume_Audit_Report_${filename.replace(/\.[^/.]+$/, "")}.html`;
    a.click();
    URL.revokeObjectURL(url);
  }
}

