import React from 'react';
import { Briefcase, ChevronDown } from 'lucide-react';

const ROLE_GROUPS = [
  {
    category: "Software Development",
    roles: [
      "Frontend Developer",
      "Backend Developer",
      "Full Stack Developer",
      "Java Developer"
    ]
  },
  {
    category: "Data & Artificial Intelligence",
    roles: [
      "Data Scientist",
      "ML Engineer",
      "Data Engineer"
    ]
  },
  {
    category: "Cloud, DevOps & Security",
    roles: [
      "DevOps Engineer",
      "Cloud Architect",
      "Cybersecurity Analyst"
    ]
  },
  {
    category: "Mobile & Quality Assurance",
    roles: [
      "Android Developer",
      "iOS Developer",
      "QA / Automation Engineer"
    ]
  },
  {
    category: "Design & Product",
    roles: [
      "UI/UX Designer",
      "Product Manager"
    ]
  }
];

export default function RoleSelector({
  targetRole = 'Frontend Developer',
  setTargetRole,
  analysisMode = 'with_role',
  setAnalysisMode
}) {
  const handleSelectChange = (e) => {
    const val = e.target.value;
    if (setAnalysisMode) setAnalysisMode('with_role');
    setTargetRole(val);
  };

  return (
    <div className="w-full max-w-lg mx-auto text-left space-y-2">
      <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
        <span className="flex items-center gap-1.5">
          <Briefcase className="w-3.5 h-3.5 text-indigo-600" />
          <span>Select Desired Engineering Role</span>
        </span>
        <span className="text-[11px] text-indigo-600 font-medium bg-indigo-50 px-2 py-0.5 rounded-full border border-indigo-100">
          15 Tracks Available
        </span>
      </div>

      <div className="relative">
        <select
          value={targetRole === 'auto' ? 'Frontend Developer' : targetRole}
          onChange={handleSelectChange}
          className="w-full appearance-none bg-white border border-slate-300 rounded-xl px-4 py-3 text-slate-900 font-semibold text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 shadow-sm transition-all cursor-pointer pr-10 hover:border-indigo-300"
        >
          {ROLE_GROUPS.map((group) => (
            <optgroup key={group.category} label={`── ${group.category} ──`}>
              {group.roles.map((role) => (
                <option key={role} value={role}>
                  {role}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
        
        <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-indigo-600">
          <ChevronDown className="w-4 h-4" />
        </div>
      </div>
      <p className="text-[11px] text-slate-500">
        Benchmarks your resume specifically against the core required skills and keywords for this target role.
      </p>
    </div>
  );
}
