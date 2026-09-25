import React from "react";
import { AmbulanceIcon } from "@/components/icons/PortalIcons";

interface AmbulancePortalProps {
  onBackToHome: () => void;
}

export function AmbulancePortal({ onBackToHome }: AmbulancePortalProps) {
  return (
    <section className="py-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-red-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-2xl border border-red-900/50 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-600/30 text-red-300 text-xs font-bold mb-3 border border-red-500/40">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-ping"></span>
            AMBULANCE &amp; HOSPITAL DISPATCH UNIT
          </div>
          <h1 className="text-2xl sm:text-3xl font-black tracking-tight flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-red-600/40 border border-red-500/50 flex items-center justify-center text-red-300">
              <AmbulanceIcon className="w-6 h-6" />
            </div>
            <span>Ambulance &amp; Hospital Portal</span>
          </h1>
          <p className="text-slate-300 text-xs sm:text-sm mt-1">
            Ready to receive live emergency referral transmissions from primary health centres.
          </p>
        </div>

        <button
          onClick={onBackToHome}
          className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-semibold border border-white/20 transition-all"
        >
          ← Back to Home
        </button>
      </div>

      {/* Clean Action Buttons & Dispatch Controls */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
        <div>
          <h2 className="text-lg font-bold text-slate-900">Emergency Dispatch Actions</h2>
          <p className="text-xs text-gray-500 mt-0.5">
            Control dispatch acknowledgment, hospital reception status, and communications.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <button
            onClick={() => alert("Emergency Referral Stream Initialized. Listening for incoming clinician dispatches...")}
            className="p-5 rounded-2xl bg-red-50 hover:bg-red-100/80 border border-red-200 text-left transition-all group"
          >
            <div className="w-10 h-10 rounded-xl bg-red-600 text-white flex items-center justify-center mb-3 shadow-md shadow-red-500/20 group-hover:scale-105 transition-transform">
              <AmbulanceIcon className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-bold text-red-950">Acknowledge Active Referral</h3>
            <p className="text-xs text-red-800/80 mt-1">
              Accept incoming patient transfer and notify sending facility.
            </p>
          </button>

          <button
            onClick={() => alert("GPS coordinates broadcasted to receiving hospital network.")}
            className="p-5 rounded-2xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-left transition-all group"
          >
            <div className="w-10 h-10 rounded-xl bg-slate-900 text-white flex items-center justify-center mb-3 shadow-md group-hover:scale-105 transition-transform">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 className="text-sm font-bold text-slate-900">Update En-Route GPS Status</h3>
            <p className="text-xs text-gray-500 mt-1">
              Broadcast real-time transit telemetry to receiving hospital.
            </p>
          </button>

          <button
            onClick={() => alert("Checking hospital bed and NICU readiness status...")}
            className="p-5 rounded-2xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-left transition-all group"
          >
            <div className="w-10 h-10 rounded-xl bg-slate-900 text-white flex items-center justify-center mb-3 shadow-md group-hover:scale-105 transition-transform">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h3 className="text-sm font-bold text-slate-900">Check Hospital Bed Readiness</h3>
            <p className="text-xs text-gray-500 mt-1">
              Verify NICU and emergency obstetric bed availability.
            </p>
          </button>

          <button
            onClick={() => alert("Initiating emergency direct line to Primary Health Centre...")}
            className="p-5 rounded-2xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-left transition-all group"
          >
            <div className="w-10 h-10 rounded-xl bg-slate-900 text-white flex items-center justify-center mb-3 shadow-md group-hover:scale-105 transition-transform">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
            </div>
            <h3 className="text-sm font-bold text-slate-900">Direct Emergency Telephony Call</h3>
            <p className="text-xs text-gray-500 mt-1">
              Connect directly to sending clinician or on-duty doctor.
            </p>
          </button>
        </div>

        <div className="pt-4 border-t border-slate-100 flex justify-between items-center text-xs text-gray-500">
          <span>Status: Awaiting Dispatch Trigger</span>
          <span>AWS CloudWatch: Connected</span>
        </div>
      </div>
    </section>
  );
}
