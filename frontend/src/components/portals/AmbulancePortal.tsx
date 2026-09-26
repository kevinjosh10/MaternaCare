import React, { useState, useEffect } from "react";
import { AmbulanceIcon } from "@/components/icons/PortalIcons";

interface AmbulancePortalProps {
  onBackToHome: () => void;
}

export function AmbulancePortal({ onBackToHome }: AmbulancePortalProps) {
  const [activeAlerts, setActiveAlerts] = useState<any[]>([]);
  const [transitStatus, setTransitStatus] = useState<string>("READY_ON_STANDBY");
  const [etaMinutes, setEtaMinutes] = useState<number>(14);
  const [hospitalBedConfirmed, setHospitalBedConfirmed] = useState<boolean>(false);
  const [isAwaitingTransfer, setIsAwaitingTransfer] = useState<boolean>(false);

  // Poll for live emergency alerts from Model 3 (Shout Recognizer)
  const fetchEmergencyAlerts = async () => {
    try {
      const res = await fetch("/api/emergency");
      if (res.ok) {
        const data = await res.json();
        if (data.alerts && data.alerts.length > 0) {
          setActiveAlerts(data.alerts);
        }
      }
    } catch (e) {
      console.warn("Emergency poll note:", e);
    }
  };

  useEffect(() => {
    fetchEmergencyAlerts();
    const timer = setInterval(fetchEmergencyAlerts, 5000);
    return () => clearInterval(timer);
  }, []);

  const handleAcknowledge = () => {
    setIsAwaitingTransfer(true);
    setTransitStatus("DISPATCHED_EN_ROUTE");
    alert("Emergency referral accepted. Ambulance Driver accepted. GPS navigation route locked directly to patient coordinates.");
  };

  return (
    <section className="py-10 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-red-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-2xl border border-red-900/50 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-600/30 text-red-300 text-xs font-bold mb-3 border border-red-500/40">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-ping"></span>
            AMBULANCE &amp; HOSPITAL EMERGENCY DISPATCH UNIT
          </div>
          <h1 className="text-2xl sm:text-3xl font-black tracking-tight flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-red-600/40 border border-red-500/50 flex items-center justify-center text-red-300">
              <AmbulanceIcon className="w-6 h-6" />
            </div>
            <span>Emergency Referral &amp; Transport Hub</span>
          </h1>
          <p className="text-slate-300 text-xs sm:text-sm mt-1">
            Receiving live emergency telemetry from Model 3 (Ambient Distress Detector) and Primary Health Centres.
          </p>
        </div>

        <button
          type="button"
          onClick={onBackToHome}
          className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-semibold border border-white/20 transition-all cursor-pointer"
        >
          ← Back to Main Dashboard
        </button>
      </div>

      {/* Live Active Emergency Transmission Card */}
      <div className="p-6 rounded-3xl bg-red-50 border-2 border-red-300 shadow-md space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-red-600 animate-ping"></span>
            <span className="font-extrabold text-red-950 text-base">
              Incoming High-Risk Obstetric Emergency
            </span>
          </div>
          <span className="px-3 py-1 rounded-full bg-red-600 text-white text-xs font-bold uppercase">
            Critical Tier 1 Referral
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-3 rounded-xl bg-white border border-red-200">
            <span className="text-gray-500 text-[10px] uppercase font-bold block">Patient Details</span>
            <span className="font-bold text-slate-900 text-sm block mt-0.5">Priya Sharma (27y)</span>
            <span className="text-gray-600">32+4 Weeks &bull; Blood: O+</span>
          </div>
          <div className="p-3 rounded-xl bg-white border border-red-200">
            <span className="text-gray-500 text-[10px] uppercase font-bold block">Primary Clinical Trigger</span>
            <span className="font-bold text-red-700 text-sm block mt-0.5">Severe Hypertensive Spike (142/92)</span>
            <span className="text-gray-600">Proteinuria (++) &bull; Headache</span>
          </div>
          <div className="p-3 rounded-xl bg-white border border-red-200">
            <span className="text-gray-500 text-[10px] uppercase font-bold block">Designated Receiving Centre</span>
            <span className="font-bold text-slate-900 text-sm block mt-0.5">District Women&apos;s &amp; Children&apos;s Hospital</span>
            <span className="text-green-700 font-semibold">NICU &amp; Obstetric Bed Ready</span>
          </div>
        </div>

        {/* Transit Status Bar */}
        <div className="p-4 rounded-2xl bg-white border border-red-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <span className="text-xs font-bold text-slate-900">Transit Status:</span>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 text-xs font-bold">
                {transitStatus}
              </span>
              <span className="text-xs text-gray-500">&bull; Estimated Arrival: <strong className="text-slate-900">{etaMinutes} mins</strong></span>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={handleAcknowledge}
              className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-md transition-all cursor-pointer"
            >
              ✓ Acknowledge &amp; Dispatch Unit
            </button>
            <button
              type="button"
              onClick={() => {
                setHospitalBedConfirmed(true);
                alert("Confirmed: Level-3 NICU Bed & Obstetric OT reserved at District Hospital.");
              }}
              className={`px-4 py-2 rounded-xl text-xs font-bold border transition-all cursor-pointer ${
                hospitalBedConfirmed ? "bg-green-600 text-white border-green-600" : "bg-white text-slate-800 border-slate-300 hover:bg-slate-50"
              }`}
            >
              {hospitalBedConfirmed ? "✓ Bed & NICU Reserved" : "Confirm Hospital Bed"}
            </button>
          </div>
        </div>
      </div>

      {/* Emergency Telephony & Dispatch Controls */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
        <div>
          <h2 className="text-lg font-bold text-slate-900">Emergency Dispatch Controls &amp; Telemetry</h2>
          <p className="text-xs text-gray-500 mt-0.5">
            Real-time ambulance network coordination and clinical telephony gateway.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <button
            type="button"
            onClick={() => {
              setEtaMinutes(Math.max(2, etaMinutes - 3));
              alert("Broadcasting live telemetry: Lat 26.8467° N, Long 80.9462° E. Traffic cleared via emergency corridor.");
            }}
            className="p-5 rounded-2xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-left transition-all group cursor-pointer"
          >
            <div className="w-10 h-10 rounded-xl bg-slate-900 text-white flex items-center justify-center mb-3 shadow-md group-hover:scale-105 transition-transform">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 className="text-sm font-bold text-slate-900">Transmit Live GPS Telemetry</h3>
            <p className="text-xs text-gray-500 mt-1">
              Broadcast active corridor coordinates and traffic routing to receiving hospital.
            </p>
          </button>

          <button
            type="button"
            onClick={() => alert("Dialing Emergency Telephony Gateway: Connecting to Dr. Ananya Sen (Lead Obstetrician)...")}
            className="p-5 rounded-2xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-left transition-all group cursor-pointer"
          >
            <div className="w-10 h-10 rounded-xl bg-red-600 text-white flex items-center justify-center mb-3 shadow-md group-hover:scale-105 transition-transform">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
            </div>
            <h3 className="text-sm font-bold text-slate-900">Direct Emergency Telephony Call</h3>
            <p className="text-xs text-gray-500 mt-1">
              Connect directly with sending Primary Health Centre or attending doctor.
            </p>
          </button>
        </div>

        <div className="pt-4 border-t border-slate-100 flex justify-between items-center text-xs text-gray-500">
          <span>Emergency Broadcast Channel: Active</span>
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-green-500"></span> 100% Cloud Synchronized</span>
        </div>
      </div>
    </section>
  );
}
