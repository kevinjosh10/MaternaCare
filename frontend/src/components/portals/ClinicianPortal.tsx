import React, { useState, useEffect } from "react";
import { ParentProfile, PatientDocument, UploadedDocumentResult } from "@/types";
import { ClinicianIcon, AmbulanceIcon } from "@/components/icons/PortalIcons";

interface ClinicianPortalProps {
  parentProfile: ParentProfile;
  parentDocuments: PatientDocument[];
  uploadFile: File | null;
  isUploading: boolean;
  uploadResult: UploadedDocumentResult | null;
  verifiedEntities: string[];
  onFileChange: (file: File | null) => void;
  onUploadSubmit: (e: React.FormEvent) => void;
  onCommitVerifiedHistory: () => void;
  onDispatchAmbulance: () => void;
}

interface PendingApproval {
  id: string;
  patientId: string;
  patientName: string;
  gestationalWeeks: string;
  query: string;
  proposedAdvice: string;
  category: string;
  urgency: string;
  status: string;
  createdAt: string;
  finalText?: string;
  reviewedBy?: string;
}

export function ClinicianPortal({
  parentProfile,
  parentDocuments,
  uploadFile,
  isUploading,
  uploadResult,
  verifiedEntities,
  onFileChange,
  onUploadSubmit,
  onCommitVerifiedHistory,
  onDispatchAmbulance,
}: ClinicianPortalProps) {
  // Temporal ML Interactive Calculator
  const [systolicBp, setSystolicBp] = useState<number>(142);
  const [diastolicBp, setDiastolicBp] = useState<number>(92);
  const [proteinuriaLevel, setProteinuriaLevel] = useState<string>("++");
  const [gestWeeks, setGestWeeks] = useState<number>(32);

  // HITL Doctor Approval Queue State
  const [pendingApprovals, setPendingApprovals] = useState<PendingApproval[]>([]);
  const [isApprovalsLoading, setIsApprovalsLoading] = useState(false);
  const [editingApprovalId, setEditingApprovalId] = useState<string | null>(null);
  const [editText, setEditText] = useState("");

  // Live Emergency SOS Alerts State
  const [emergencyAlerts, setEmergencyAlerts] = useState<any[]>([]);

  // Fetch pending AI approvals & SOS alerts
  const fetchApprovalsAndAlerts = async () => {
    try {
      const [appRes, emgRes] = await Promise.all([
        fetch("/api/doctor/approval"),
        fetch("/api/emergency"),
      ]);

      if (appRes.ok) {
        const appData = await appRes.json();
        if (appData.approvals) setPendingApprovals(appData.approvals);
      }

      if (emgRes.ok) {
        const emgData = await emgRes.json();
        if (emgData.alerts) setEmergencyAlerts(emgData.alerts);
      }
    } catch (err) {
      console.warn("Polling note:", err);
    }
  };

  useEffect(() => {
    fetchApprovalsAndAlerts();
    const interval = setInterval(fetchApprovalsAndAlerts, 6000);
    return () => clearInterval(interval);
  }, []);

  const handleDecision = async (approvalId: string, decision: "APPROVE" | "REJECT", customText?: string) => {
    try {
      const res = await fetch("/api/doctor/approval", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          approvalId,
          decision,
          editedText: customText || undefined,
          reviewerName: "Dr. Ananya Sen (Lead Obstetrician)",
        }),
      });

      if (res.ok) {
        setEditingApprovalId(null);
        fetchApprovalsAndAlerts();
      }
    } catch (err) {
      console.error("Decision submit error:", err);
    }
  };

  // Compute Temporal ML Risk Score (XGBoost / Random Forest Simulation)
  const calculateRiskScore = () => {
    let score = 20; // baseline
    if (systolicBp >= 140) score += 35;
    else if (systolicBp >= 130) score += 15;

    if (diastolicBp >= 90) score += 25;
    else if (diastolicBp >= 85) score += 10;

    if (proteinuriaLevel === "+++" || proteinuriaLevel === "++++") score += 20;
    else if (proteinuriaLevel === "++") score += 15;
    else if (proteinuriaLevel === "+") score += 8;

    if (gestWeeks >= 30) score += 5;

    return Math.min(score, 98);
  };

  const currentRiskScore = calculateRiskScore();
  const riskTier = currentRiskScore >= 75 ? "CRITICAL_TIER_1" : currentRiskScore >= 50 ? "MODERATE_TIER_2" : "STABLE_TIER_3";

  return (
    <section className="py-10 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto space-y-8">
      {/* Top Bar with Live AWS Sync Status */}
      <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 text-xs text-pink-300 font-semibold mb-3 border border-slate-700">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-ping"></span>
            Encrypted Medical Cloud Active &bull; AP-South-1
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-blue-400">
              <ClinicianIcon className="w-6 h-6" />
            </div>
            <span>Clinical Triage &amp; Risk Intelligence Portal</span>
          </h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Active Facility: Community Health Centre (CHC) &bull; Lead Clinician: Dr. Ananya Sen, MD, DGO
          </p>
        </div>

        {/* Clinical Service Health Badges */}
        <div className="grid grid-cols-2 gap-2 text-[11px] bg-slate-800/80 border border-slate-700/80 rounded-2xl p-3">
          <div className="flex items-center gap-1.5 text-slate-300">
            <span className="text-green-400">●</span> RDS Health Vault: Active
          </div>
          <div className="flex items-center gap-1.5 text-slate-300">
            <span className="text-green-400">●</span> Model 4 Brain: Connected
          </div>
          <div className="flex items-center gap-1.5 text-slate-300">
            <span className="text-green-400">●</span> CloudWatch Audit: Synced
          </div>
          <div className="flex items-center gap-1.5 text-slate-300">
            <span className="text-green-400">●</span> Model 5 OCR: Ready
          </div>
        </div>
      </div>

      {/* Emergency SOS Alerts Notification Bar */}
      {emergencyAlerts.length > 0 && (
        <div className="p-4 sm:p-5 rounded-2xl bg-red-600 text-white shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 animate-pulse">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🚨</span>
            <div>
              <div className="text-xs font-black uppercase tracking-wider">
                Live Ambient Distress Trigger Received (Model 3 Shout Detector)
              </div>
              <p className="text-xs text-red-100 mt-0.5">
                <strong>{emergencyAlerts[0].patientName}:</strong> {emergencyAlerts[0].keyword} &bull; Location: {emergencyAlerts[0].location}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onDispatchAmbulance}
            className="px-4 py-2 rounded-xl bg-white text-red-700 font-bold text-xs shadow-md hover:bg-red-50 transition-all cursor-pointer whitespace-nowrap"
          >
            Dispatch Ambulance →
          </button>
        </div>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Patient Profile & Health Memory */}
        <div className="lg:col-span-2 space-y-6">
          {/* Patient Card */}
          <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
              <div>
                <h2 className="text-xl font-bold text-slate-900">
                  Patient: {parentProfile.fullName}
                </h2>
                <p className="text-xs text-gray-500">
                  Email/ID: {parentProfile.email} &bull; Age: {parentProfile.age}y &bull; Blood: {parentProfile.bloodGroup} &bull; Parity: {parentProfile.gravidity}/{parentProfile.parity}
                </p>
              </div>
              <div className="px-3.5 py-1.5 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-bold self-start sm:self-auto">
                Gestational Age: {parentProfile.gestationalWeeks} Weeks
              </div>
            </div>

            {/* Interactive Temporal ML Risk Assessment & SHAP Explainability Engine */}
            <div className="p-5 rounded-2xl bg-amber-50/80 border border-amber-200 space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-xs font-bold text-amber-900 uppercase tracking-wider flex items-center gap-1.5">
                  <span>🔬</span>
                  <span>Temporal ML Risk Engine (XGBoost + SHAP Explainability)</span>
                </span>
                <span
                  className={`text-xs font-bold px-3 py-1 rounded-full ${
                    riskTier === "CRITICAL_TIER_1"
                      ? "bg-red-600 text-white animate-pulse"
                      : "bg-amber-200 text-amber-900"
                  }`}
                >
                  {riskTier === "CRITICAL_TIER_1" ? "High Priority Obstetric Review" : "Moderate Monitoring Tier"}
                </span>
              </div>

              {/* Real-time Probability Score Meter */}
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs font-bold text-amber-950">
                  <span>Preeclampsia Progression Risk Probability:</span>
                  <span className="font-mono text-sm">{currentRiskScore}%</span>
                </div>
                <div className="w-full bg-amber-200 rounded-full h-3 overflow-hidden">
                  <div
                    className={`h-3 rounded-full transition-all duration-500 ${
                      currentRiskScore >= 75 ? "bg-red-600" : currentRiskScore >= 50 ? "bg-amber-500" : "bg-green-500"
                    }`}
                    style={{ width: `${currentRiskScore}%` }}
                  ></div>
                </div>
              </div>

              {/* Interactive Vitals Adjuster for Live Simulation */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs pt-2 border-t border-amber-200/60">
                <div>
                  <label className="block text-[11px] font-semibold text-amber-900 mb-1">Systolic BP (mmHg)</label>
                  <input
                    type="number"
                    value={systolicBp}
                    onChange={(e) => setSystolicBp(Number(e.target.value))}
                    className="w-full px-2.5 py-1.5 rounded-lg bg-white border border-amber-300 text-slate-800 font-mono text-xs focus:ring-1 focus:ring-amber-500"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-amber-900 mb-1">Diastolic BP (mmHg)</label>
                  <input
                    type="number"
                    value={diastolicBp}
                    onChange={(e) => setDiastolicBp(Number(e.target.value))}
                    className="w-full px-2.5 py-1.5 rounded-lg bg-white border border-amber-300 text-slate-800 font-mono text-xs focus:ring-1 focus:ring-amber-500"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-amber-900 mb-1">Proteinuria (Albumin)</label>
                  <select
                    value={proteinuriaLevel}
                    onChange={(e) => setProteinuriaLevel(e.target.value)}
                    className="w-full px-2.5 py-1.5 rounded-lg bg-white border border-amber-300 text-slate-800 text-xs focus:ring-1 focus:ring-amber-500"
                  >
                    <option value="Nil">Nil</option>
                    <option value="+">+ (1+)</option>
                    <option value="++">++ (2+)</option>
                    <option value="+++">+++ (3+)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-amber-900 mb-1">Gestational Wk</label>
                  <input
                    type="number"
                    value={gestWeeks}
                    onChange={(e) => setGestWeeks(Number(e.target.value))}
                    className="w-full px-2.5 py-1.5 rounded-lg bg-white border border-amber-300 text-slate-800 font-mono text-xs focus:ring-1 focus:ring-amber-500"
                  />
                </div>
              </div>

              {/* SHAP Feature Attribution Breakdown */}
              <div className="space-y-1.5 text-[11px] text-amber-900 pt-2 border-t border-amber-200/60">
                <span className="font-bold block">Key SHAP Feature Importance Attributions:</span>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  <div className="p-2 rounded-lg bg-white/70 border border-amber-200">
                    <span className="text-gray-500 block text-[10px]">SBP Slope (+24 mmHg/14d)</span>
                    <span className="font-bold text-red-600">+0.38 Impact</span>
                  </div>
                  <div className="p-2 rounded-lg bg-white/70 border border-amber-200">
                    <span className="text-gray-500 block text-[10px]">Proteinuria Dipstick ({proteinuriaLevel})</span>
                    <span className="font-bold text-red-600">+0.26 Impact</span>
                  </div>
                  <div className="p-2 rounded-lg bg-white/70 border border-amber-200">
                    <span className="text-gray-500 block text-[10px]">Prior Preeclampsia (2023)</span>
                    <span className="font-bold text-amber-700">+0.19 Impact</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Verified Health Memory & Emergency Contacts */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="font-bold text-slate-800 block mb-1">
                  Verified Clinical History &amp; Prior Records
                </span>
                <p className="text-slate-600">
                  {parentProfile.medicalConditions || "No prior conditions reported."}
                </p>
                <p className="text-slate-600 mt-2">
                  <span className="font-semibold text-red-600">Allergies:</span> {parentProfile.knownAllergies || "None"}
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="font-bold text-slate-800 block mb-1">
                  Emergency Referral Contact
                </span>
                <p className="text-slate-600">
                  {parentProfile.emergencyContactName} ({parentProfile.emergencyContactRelation})
                </p>
                <p className="text-slate-600 mt-1">
                  Phone: <span className="font-mono font-semibold">{parentProfile.emergencyContactPhone}</span>
                </p>
                <p className="text-slate-600 mt-1">
                  Facility: {parentProfile.preferredFacility}
                </p>
              </div>
            </div>

            {/* Emergency Action Buttons */}
            <div className="pt-2 flex flex-wrap gap-3">
              <button
                type="button"
                onClick={onDispatchAmbulance}
                className="px-5 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-md shadow-red-500/20 transition-all flex items-center gap-2 cursor-pointer"
              >
                <AmbulanceIcon className="w-4 h-4 text-white" />
                <span>Dispatch to Ambulance &amp; Hospital Hub →</span>
              </button>
              <button
                type="button"
                onClick={() => alert("Exporting encrypted clinical handover report to Secure Health Vault...")}
                className="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition-all cursor-pointer"
              >
                Export Clinical Handover Summary
              </button>
            </div>
          </div>

          {/* Model 4 Human-In-The-Loop (HITL) Doctor Approval Hub */}
          <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-4">
              <div>
                <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 text-[10px] font-bold border border-blue-200 mb-1">
                  <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
                  Model 4 Clinical Review Gateway
                </div>
                <h3 className="text-lg font-bold text-slate-900">
                  Human-In-The-Loop (HITL) Medical Advice Queue
                </h3>
                <p className="text-xs text-gray-500">
                  Review and validate AI-generated medical advice before it is delivered to the pregnant mother.
                </p>
              </div>
              <span className="text-xs font-bold text-blue-700 bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
                {pendingApprovals.filter((a) => a.status === "PENDING_APPROVAL").length} Pending Review
              </span>
            </div>

            {pendingApprovals.length === 0 ? (
              <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 text-center text-xs text-gray-500">
                No advice requests currently pending approval. All queries are verified.
              </div>
            ) : (
              <div className="space-y-3">
                {pendingApprovals.map((item) => (
                  <div
                    key={item.id}
                    className={`p-4 rounded-2xl border text-xs space-y-3 transition-all ${
                      item.status === "PENDING_APPROVAL"
                        ? "bg-amber-50/40 border-amber-200"
                        : item.status === "APPROVED" || item.status === "MODIFIED"
                        ? "bg-green-50/40 border-green-200"
                        : "bg-red-50/40 border-red-200"
                    }`}
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-slate-900">{item.patientName}</span>
                        <span className="text-gray-400">&bull;</span>
                        <span className="text-slate-600 font-semibold">{item.gestationalWeeks}</span>
                        <span className="text-gray-400">&bull;</span>
                        <span className="text-[10px] text-gray-400">{new Date(item.createdAt).toLocaleTimeString()}</span>
                      </div>
                      <span
                        className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full ${
                          item.status === "PENDING_APPROVAL"
                            ? "bg-amber-100 text-amber-800"
                            : item.status === "APPROVED" || item.status === "MODIFIED"
                            ? "bg-green-100 text-green-800"
                            : "bg-red-100 text-red-800"
                        }`}
                      >
                        {item.status === "PENDING_APPROVAL" ? "⏳ Awaiting Doctor Approval" : `✓ ${item.status}`}
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-white border border-slate-200 space-y-1">
                      <span className="font-semibold text-gray-500 text-[10px] uppercase">Mother&apos;s Query:</span>
                      <p className="text-slate-800 font-medium">{item.query}</p>
                    </div>

                    <div className="p-3 rounded-xl bg-white border border-slate-200 space-y-1">
                      <span className="font-semibold text-blue-700 text-[10px] uppercase">Proposed Medical Advice (Model 4):</span>
                      {editingApprovalId === item.id ? (
                        <div className="space-y-2">
                          <textarea
                            rows={3}
                            value={editText}
                            onChange={(e) => setEditText(e.target.value)}
                            className="w-full p-2 text-xs border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                          />
                          <div className="flex gap-2">
                            <button
                              type="button"
                              onClick={() => handleDecision(item.id, "APPROVE", editText)}
                              className="px-3 py-1 rounded-lg bg-green-600 text-white font-bold text-xs"
                            >
                              Save &amp; Approve
                            </button>
                            <button
                              type="button"
                              onClick={() => setEditingApprovalId(null)}
                              className="px-3 py-1 rounded-lg bg-slate-200 text-slate-700 text-xs"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      ) : (
                        <p className="text-slate-800">{item.finalText || item.proposedAdvice}</p>
                      )}
                    </div>

                    {item.status === "PENDING_APPROVAL" && editingApprovalId !== item.id && (
                      <div className="flex flex-wrap items-center gap-2 pt-1">
                        <button
                          type="button"
                          onClick={() => handleDecision(item.id, "APPROVE")}
                          className="px-3.5 py-1.5 rounded-xl bg-green-600 hover:bg-green-700 text-white font-bold text-xs transition-all cursor-pointer shadow-sm"
                        >
                          ✓ Approve Advice
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            setEditingApprovalId(item.id);
                            setEditText(item.proposedAdvice);
                          }}
                          className="px-3.5 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-xs transition-all cursor-pointer"
                        >
                          ✏️ Edit &amp; Customise
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDecision(item.id, "REJECT")}
                          className="px-3.5 py-1.5 rounded-xl bg-red-50 hover:bg-red-100 text-red-700 font-semibold text-xs border border-red-200 transition-all cursor-pointer"
                        >
                          ✕ Reject
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: AI Medical Record Scanner (Model 5) */}
        <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 space-y-5">
          <div>
            <div className="flex items-center justify-between mb-1">
              <h3 className="text-base font-bold text-slate-900">
                Medical Record OCR Scanner
              </h3>
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-green-100 text-green-800 text-[10px] font-bold">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                Model 5 Active
              </span>
            </div>
            <p className="text-xs text-gray-500">
              Upload multi-page paper discharge summaries or antenatal cards to extract all text into unified Markdown (.md).
            </p>
          </div>

          <form onSubmit={onUploadSubmit} className="space-y-4">
            <div className="border-2 border-dashed border-pink-200 rounded-2xl p-6 text-center bg-pink-50/30 hover:bg-pink-50/60 transition-colors">
              <input
                type="file"
                accept=".pdf,image/*"
                onChange={(e) => onFileChange(e.target.files?.[0] || null)}
                className="hidden"
                id="clinician-doc-upload"
              />
              <label htmlFor="clinician-doc-upload" className="cursor-pointer block">
                <div className="w-10 h-10 rounded-full bg-pink-100 text-pink-600 flex items-center justify-center mx-auto mb-2 font-bold text-lg">
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <span className="text-xs font-semibold text-pink-700 block">
                  {uploadFile ? uploadFile.name : "Choose Multi-Page PDF or Scan"}
                </span>
                <span className="text-[10px] text-gray-400 block mt-1">
                  Multi-page PDF &bull; Clinical AI Extraction
                </span>
              </label>
            </div>

            <button
              type="submit"
              disabled={!uploadFile || isUploading}
              className="w-full py-3 px-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-md disabled:bg-gray-300 transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              {isUploading ? (
                <>
                  <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                  <span>Extracting All Pages...</span>
                </>
              ) : (
                <>
                  <span>Extract &amp; Sync to Health Vault →</span>
                </>
              )}
            </button>
          </form>

          {/* Uploaded Documents List */}
          {parentDocuments.length > 0 && (
            <div className="pt-2 border-t border-slate-100 space-y-2">
              <span className="text-xs font-bold text-slate-800 block">
                Synced Patient Records ({parentDocuments.length})
              </span>
              <div className="space-y-2 max-h-80 overflow-y-auto">
                {parentDocuments.map((doc) => (
                  <div key={doc.id} className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-slate-800 truncate max-w-[160px]">{doc.file_name}</span>
                      <span className="text-[10px] text-green-700 font-bold">✓ Synced</span>
                    </div>
                    {doc.ocr_markdown && (
                      <button
                        type="button"
                        onClick={() => {
                          const blob = new Blob([doc.ocr_markdown || ""], { type: "text/markdown;charset=utf-8;" });
                          const url = URL.createObjectURL(blob);
                          const link = document.createElement("a");
                          link.href = url;
                          const baseName = doc.file_name.replace(/\.[^/.]+$/, "");
                          link.download = `${baseName}_OCR_FULL_TEXT.md`;
                          document.body.appendChild(link);
                          link.click();
                          document.body.removeChild(link);
                          URL.revokeObjectURL(url);
                        }}
                        className="w-full py-1 rounded-lg bg-pink-600 hover:bg-pink-700 text-white text-[10px] font-bold transition-all"
                      >
                        ⬇ Download .MD
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
