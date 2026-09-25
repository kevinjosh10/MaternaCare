import React from "react";
import { ParentProfile } from "@/types";
import { ParentIcon } from "@/components/icons/PortalIcons";

export function HealthDashboard({ profile, onBack }: { profile: ParentProfile, onBack: () => void }) {
  return (
    <section className="py-10 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-pink-500 via-rose-400 to-pink-600 rounded-3xl p-6 sm:p-8 text-white shadow-lg shadow-pink-500/15 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <span className="inline-block bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold mb-2">
            Maternal Health Dashboard
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold flex items-center gap-2.5">
            <ParentIcon className="w-8 h-8 text-white" />
            <span>{profile.fullName}'s Health Overview</span>
          </h1>
          <p className="text-pink-100 text-sm mt-1">
            Gestational Week: <span className="font-bold text-white">{profile.gestationalWeeks} Weeks</span> | Due Date: <span className="font-bold text-white">{profile.dueDate}</span>
          </p>
        </div>
        <button onClick={onBack} className="bg-white/20 hover:bg-white/30 backdrop-blur-md border border-white/30 rounded-xl px-4 py-2 text-sm font-semibold transition-all">
          Edit Profile & Documents
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Vitals & Conditions Card */}
        <div className="md:col-span-2 bg-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-200/80">
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2 mb-6">
            <span>❤️</span>
            <span>Clinical Summary</span>
          </h2>
          
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="p-4 rounded-2xl bg-pink-50 border border-pink-100">
              <div className="text-xs text-pink-600 font-bold mb-1">Blood Group</div>
              <div className="text-lg font-extrabold text-slate-900">{profile.bloodGroup}</div>
            </div>
            <div className="p-4 rounded-2xl bg-pink-50 border border-pink-100">
              <div className="text-xs text-pink-600 font-bold mb-1">Obstetric History</div>
              <div className="text-lg font-extrabold text-slate-900">{profile.gravidity} {profile.parity}</div>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <div className="text-sm font-bold text-slate-700 mb-2">Medical Conditions</div>
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 text-slate-800 text-sm font-medium">
                {profile.medicalConditions || "None reported"}
              </div>
            </div>
            <div>
              <div className="text-sm font-bold text-slate-700 mb-2">Known Allergies</div>
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 text-slate-800 text-sm font-medium">
                {profile.knownAllergies || "None reported"}
              </div>
            </div>
          </div>
        </div>

        {/* AI Action Card */}
        <div className="bg-gradient-to-b from-slate-900 to-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-700 text-white flex flex-col justify-between">
          <div>
            <div className="w-12 h-12 rounded-2xl bg-pink-500/20 text-pink-400 flex items-center justify-center mb-4">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" /></svg>
            </div>
            <h3 className="text-lg font-bold mb-2">MaternaCare Medical Brain</h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-6">
              Our 5-Model Core Brain is fully initialized with your latest profile and documents. You can communicate with the AI instantly using your voice.
            </p>
          </div>
          
          <button 
            onClick={() => {
              const aiBtn = document.getElementById('materna-ai-chat-btn');
              if (aiBtn) aiBtn.click();
              else alert('AI Chat Assistant is ready! Click the pink floating button in the bottom right corner.');
            }}
            className="w-full py-4 rounded-2xl bg-pink-600 hover:bg-pink-700 text-white font-bold text-sm shadow-lg shadow-pink-600/30 transition-all flex items-center justify-center gap-2"
          >
            Start Voice Consultation
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" /></svg>
          </button>
        </div>
      </div>
    </section>
  );
}
