import React from "react";
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
  return (
    <section className="py-10 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto space-y-8">
      {/* Top Bar with Live AWS Sync Status */}
      <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 text-xs text-pink-300 font-semibold mb-3 border border-slate-700">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-ping"></span>
            Encrypted Medical Cloud Active
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-blue-400">
              <ClinicianIcon className="w-6 h-6" />
            </div>
            <span>Clinical Triage &amp; Risk Intelligence Portal</span>
          </h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Active Facility: Community Health Centre (CHC) &bull; Lead Clinician: Dr. Ananya Sen
          </p>
        </div>

        {/* Clinical Service Health Badges */}
        <div className="grid grid-cols-2 gap-2 text-[11px] bg-slate-800/80 border border-slate-700/80 rounded-2xl p-3">
          <div className="flex items-center gap-1.5 text-slate-300">
            <span className="text-green-400">●</span> Health Vault: Encrypted
          </div>
          <div className="flex items-center gap-1.5 text-slate-300">
            <span className="text-green-400">●</span> Health Records: Synced
          </div>
          <div className="flex items-center gap-1.5 text-slate-300">
            <span className="text-green-400">●</span> Audit Logging: Active
          </div>
          <div className="flex items-center gap-1.5 text-slate-300">
            <span className="text-green-400">●</span> AI Document OCR: Ready
          </div>
        </div>
      </div>

      {/* Active Triage Patient Card & Document AI Scanner */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Patient Profile & Health Memory */}
        <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl font-bold text-slate-900">
                Patient: {parentProfile.fullName}
              </h2>
              <p className="text-xs text-gray-500">
                Email/ID: {parentProfile.email} &bull; Age: {parentProfile.age}y &bull; Blood: {parentProfile.bloodGroup} &bull; Parity: {parentProfile.gravidity}/{parentProfile.parity}
              </p>
            </div>
            <div className="px-3.5 py-1.5 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-bold">
              Gestational Age: {parentProfile.gestationalWeeks} Weeks
            </div>
          </div>

          {/* Longitudinal Trajectory & Risk Intelligence */}
          <div className="p-4 rounded-2xl bg-amber-50/70 border border-amber-200">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-amber-900 uppercase tracking-wider">
                ⚠️ Temporal Risk Assessment (SHAP Explainability)
              </span>
              <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-amber-200 text-amber-900">
                High Priority Review
              </span>
            </div>
            <p className="text-xs text-amber-800 leading-relaxed mb-3">
              <strong>Contributing Factors:</strong> SBP increased by +24 mmHg in 14 days (118 &rarr; 142 mmHg) + Proteinuria (++) + Verified History of Preeclampsia in 2023.
            </p>
            <div className="w-full bg-amber-200/60 rounded-full h-2">
              <div className="bg-amber-600 h-2 rounded-full w-[78%]"></div>
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

          {/* Patient's Uploaded Records List */}
          {parentDocuments.length > 0 && (
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
              <span className="font-bold text-slate-800 text-xs block mb-2">
                Uploaded Patient Records &amp; Scans ({parentDocuments.length})
              </span>
              <div className="space-y-2">
                {parentDocuments.map((doc) => (
                  <div key={doc.id} className="p-3 rounded-xl bg-white border border-slate-200 text-xs space-y-2">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="text-pink-600 font-bold">📄</span>
                        <div>
                          <span className="font-semibold text-slate-800">{doc.file_name}</span>
                          <span className="text-[10px] text-gray-400 block">
                            {doc.created_at ? new Date(doc.created_at).toLocaleDateString() : "Recent"} &bull; Secure Cloud Verified
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
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
                            className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-white text-[11px] font-semibold transition-all"
                          >
                            ⬇ Download .MD
                          </button>
                        )}
                        {doc.public_url && (
                          <a
                            href={doc.public_url}
                            target="_blank"
                            rel="noreferrer"
                            className="text-[11px] font-semibold text-pink-600 hover:text-pink-700 underline"
                          >
                            View Original ↗
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Emergency Action Buttons */}
          <div className="pt-2 flex flex-wrap gap-3">
            <button
              onClick={onDispatchAmbulance}
              className="px-5 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-md shadow-red-500/20 transition-all flex items-center gap-2"
            >
              <AmbulanceIcon className="w-4 h-4 text-white" />
              <span>Dispatch to Ambulance &amp; Hospital Hub →</span>
            </button>
            <button
              onClick={() => alert("Exporting encrypted clinical handover report to Secure Medical Vault...")}
              className="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition-all"
            >
              Export Clinical Handover Summary
            </button>
          </div>
        </div>

        {/* Right Column: AI Medical Record Scanner */}
        <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 space-y-5">
          <div>
            <div className="flex items-center justify-between mb-1">
              <h3 className="text-base font-bold text-slate-900">
                Intelligent Medical Record Scanner
              </h3>
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-green-100 text-green-800 text-[10px] font-bold">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                Model 5 OCR Active
              </span>
            </div>
            <p className="text-xs text-gray-500">
              Upload multi-page paper discharge summaries or antenatal cards to extract 100% of all text into Markdown (.md).
            </p>
          </div>

          <form onSubmit={onUploadSubmit} className="space-y-4">
            <div className="border-2 border-dashed border-pink-200 rounded-2xl p-6 text-center bg-pink-50/30 hover:bg-pink-50/60 transition-colors">
              <input
                type="file"
                accept=".pdf,image/*"
                onChange={(e) => onFileChange(e.target.files?.[0] || null)}
                className="hidden"
                id="doc-upload"
              />
              <label htmlFor="doc-upload" className="cursor-pointer block">
                <div className="w-10 h-10 rounded-full bg-pink-100 text-pink-600 flex items-center justify-center mx-auto mb-2 font-bold text-lg">
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <span className="text-xs font-semibold text-pink-700 block">
                  {uploadFile ? uploadFile.name : "Choose PDF or Scan"}
                </span>
                <span className="text-[10px] text-gray-400 block mt-1">
                  Encrypted Cloud Storage &bull; Clinical AI Extraction
                </span>
              </label>
            </div>

            <button
              type="submit"
              disabled={!uploadFile || isUploading}
              className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-xs shadow-sm hover:from-pink-600 hover:to-rose-500 disabled:bg-gray-300 transition-all"
            >
              {isUploading ? "Uploading & Scanning Document..." : "Upload & Extract Clinical Data"}
            </button>
          </form>

          {/* OCR Results & Clinical Verification */}
          {uploadResult && (
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-800">
                  Extracted Clinical Tags
                </span>
                <span className="text-[10px] bg-green-100 text-green-800 font-semibold px-2 py-0.5 rounded-full">
                  Model 5 Verified
                </span>
              </div>

              <div className="space-y-1.5">
                {verifiedEntities.map((entity, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-2 rounded-lg bg-white border border-slate-200 text-xs text-slate-700 font-medium"
                  >
                    <span>✓ {entity}</span>
                  </div>
                ))}
              </div>

              {uploadResult.ocrMarkdown && (
                <div className="space-y-2 pt-2 border-t border-slate-200">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-800">Full Extracted .MD:</span>
                    <button
                      type="button"
                      onClick={() => {
                        const blob = new Blob([uploadResult.ocrMarkdown || ""], { type: "text/markdown;charset=utf-8;" });
                        const url = URL.createObjectURL(blob);
                        const link = document.createElement("a");
                        link.href = url;
                        const baseName = (uploadResult.fileName || "Medical_Report.pdf").replace(/\.[^/.]+$/, "");
                        link.download = `${baseName}_OCR_FULL_TEXT.md`;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        URL.revokeObjectURL(url);
                      }}
                      className="px-2.5 py-1 rounded-lg bg-green-700 hover:bg-green-800 text-white font-bold text-[10px] transition-all flex items-center gap-1 shadow-sm"
                    >
                      <span>⬇ Download .MD</span>
                    </button>
                  </div>
                  <pre className="p-3 rounded-xl bg-white border border-slate-200 text-[10px] font-mono text-slate-700 max-h-48 overflow-y-auto whitespace-pre-wrap leading-relaxed">
                    {uploadResult.ocrMarkdown}
                  </pre>
                </div>
              )}

              <button
                type="button"
                onClick={onCommitVerifiedHistory}
                className="w-full py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-all"
              >
                Verify &amp; Add to Patient Health Record →
              </button>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
