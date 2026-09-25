import React, { useState } from "react";
import { ParentProfile, PatientDocument, UploadedDocumentResult } from "@/types";
import { ParentIcon } from "@/components/icons/PortalIcons";

interface ParentPortalProps {
  parentProfile: ParentProfile;
  parentDocuments: PatientDocument[];
  profileSaving: boolean;
  profileSaveSuccess: boolean;
  awsSyncDetails: string | null;
  parentUploadFile: File | null;
  isParentUploading: boolean;
  parentUploadResult: UploadedDocumentResult | null;
  onProfileChange: (field: keyof ParentProfile, value: string) => void;
  onSaveProfile: (e: React.FormEvent) => void;
  onParentFileChange: (file: File | null) => void;
  onParentUploadSubmit: (e: React.FormEvent) => void;
  onBackToHome: () => void;
}

export function ParentPortal({
  parentProfile,
  parentDocuments,
  profileSaving,
  profileSaveSuccess,
  awsSyncDetails,
  parentUploadFile,
  isParentUploading,
  parentUploadResult,
  onProfileChange,
  onSaveProfile,
  onParentFileChange,
  onParentUploadSubmit,
  onBackToHome,
}: ParentPortalProps) {
  const [expandedDocId, setExpandedDocId] = useState<string | null>(null);

  return (
    <section className="py-10 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto space-y-8">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-pink-500 via-rose-400 to-pink-600 rounded-3xl p-6 sm:p-8 text-white shadow-lg shadow-pink-500/15 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <span className="inline-block bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold mb-2">
            Continuous Maternal &amp; Baby Journey
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold flex items-center gap-2.5">
            <ParentIcon className="w-8 h-8 text-white" />
            <span>Welcome, {parentProfile.fullName}</span>
          </h1>
          <p className="text-pink-100 text-sm mt-1">
            Gestational Week:{" "}
            <span className="font-bold text-white">{parentProfile.gestationalWeeks} Weeks</span>{" "}
            | Expected Due Date:{" "}
            <span className="font-bold text-white">{parentProfile.dueDate}</span>
          </p>
        </div>

        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-4 text-center min-w-[160px]">
          <div className="text-xs text-pink-100 font-medium">Baby Status</div>
          <div className="text-lg font-bold mt-0.5">{parentProfile.babyName || "Baby On The Way"}</div>
          <span className="inline-block mt-1 text-[11px] bg-green-400/30 text-white px-2 py-0.5 rounded-full font-medium">
            Healthy Trajectory
          </span>
        </div>
      </div>

      {/* Document Upload & Medical Reports Section */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm p-6 sm:p-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-4">
          <div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <span>📄</span>
              <span>Upload Medical Reports &amp; Scans</span>
            </h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Upload lab reports, ultrasound scans, or antenatal cards to automatically update your continuous health profile.
            </p>
          </div>
          <span className="text-xs font-semibold text-pink-700 bg-pink-50 px-3 py-1 rounded-full border border-pink-200 self-start sm:self-auto">
            Encrypted Health Vault
          </span>
        </div>

        {/* Upload Dropzone */}
        <form onSubmit={onParentUploadSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
          <div className="md:col-span-2 border-2 border-dashed border-pink-300 rounded-2xl p-6 text-center bg-pink-50/20 hover:bg-pink-50/50 transition-all cursor-pointer">
            <input
              type="file"
              accept=".pdf,image/*"
              onChange={(e) => onParentFileChange(e.target.files?.[0] || null)}
              className="hidden"
              id="parent-doc-upload"
            />
            <label htmlFor="parent-doc-upload" className="cursor-pointer block">
              <div className="w-12 h-12 rounded-2xl bg-pink-100 text-pink-600 flex items-center justify-center mx-auto mb-2 font-bold text-xl shadow-sm">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <span className="text-sm font-bold text-slate-800 block">
                {parentUploadFile ? parentUploadFile.name : "Click to select Medical PDF or Ultrasound Image"}
              </span>
              <span className="text-xs text-gray-400 block mt-1">
                {parentUploadFile
                  ? `${(parentUploadFile.size / 1024).toFixed(1)} KB — Ready to upload`
                  : "Supports PDF, JPG, PNG &bull; Auto-extracts vitals, allergies &amp; risk factors"}
              </span>
            </label>
          </div>

          <div className="space-y-3">
            <button
              type="submit"
              disabled={!parentUploadFile || isParentUploading}
              className="w-full py-3.5 px-4 rounded-2xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 disabled:bg-gray-300 transition-all flex items-center justify-center gap-2"
            >
              {isParentUploading ? (
                <>
                  <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                  <span>Scanning &amp; Reading Document...</span>
                </>
              ) : (
                <>
                  <span>Upload &amp; Add to Profile →</span>
                </>
              )}
            </button>
            <p className="text-[11px] text-gray-500 text-center">
              Files are protected with bank-grade encryption and saved to your continuous medical history.
            </p>
          </div>
        </form>

        {/* Upload Success Notice */}
        {parentUploadResult && (
          <div className="p-4 rounded-2xl bg-green-50 border border-green-200 text-green-800 text-xs space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold flex items-center gap-1.5">
                <span>✓</span> Report successfully uploaded &amp; attached to your maternal profile!
              </span>
              <span className="text-[10px] font-mono bg-green-200/60 px-2 py-0.5 rounded-full">
                Encrypted &amp; Synced
              </span>
            </div>
            {parentUploadResult.extractedEntities && (
              <div className="text-[11px] text-green-900 bg-white/70 p-2.5 rounded-xl border border-green-200">
                <strong>AI Extracted Findings:</strong>{" "}
                {Object.keys(parentUploadResult.extractedEntities).length > 0 ? (
                  <span>
                    {parentUploadResult.extractedEntities.previousComplications?.join(", ") || ""}
                    {parentUploadResult.extractedEntities.allergies
                      ? ` | Allergies: ${parentUploadResult.extractedEntities.allergies.join(", ")}`
                      : ""}
                  </span>
                ) : (
                  "Text extracted cleanly. Your clinical memory is updated."
                )}
              </div>
            )}
          </div>
        )}

        {/* List of Uploaded Documents */}
        <div>
          <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center justify-between">
            <span>Your Uploaded Reports &amp; Medical Files ({parentDocuments.length})</span>
            <span className="text-xs font-normal text-gray-500">Secure Medical Cloud</span>
          </h3>

          {parentDocuments.length === 0 ? (
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 text-center text-xs text-gray-500">
              No documents uploaded yet. Upload your ultrasound scans, blood test results, or prescription slips above to build your unbroken medical memory.
            </div>
          ) : (
            <div className="space-y-3">
              {parentDocuments.map((doc) => (
                <div
                  key={doc.id}
                  className="p-4 rounded-2xl bg-slate-50 hover:bg-slate-100/80 border border-slate-200 transition-all space-y-2"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-xl bg-pink-100 text-pink-600 flex items-center justify-center font-bold text-sm">
                        PDF
                      </div>
                      <div>
                        <div className="text-xs font-bold text-slate-900">{doc.file_name}</div>
                        <div className="text-[11px] text-gray-500">
                          {doc.created_at ? new Date(doc.created_at).toLocaleDateString() : "Recent"} &bull;{" "}
                          {doc.file_size ? `${(doc.file_size / 1024).toFixed(1)} KB` : "Stored"} &bull; Status:{" "}
                          <span className="text-green-700 font-semibold">{doc.status || "VERIFIED"}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      {doc.ocr_markdown && (
                        <button
                          type="button"
                          onClick={() => setExpandedDocId(expandedDocId === doc.id ? null : doc.id)}
                          className="px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-700 text-xs font-medium hover:bg-slate-50"
                        >
                          {expandedDocId === doc.id ? "Hide Extracted Text" : "View Extracted Summary"}
                        </button>
                      )}
                      {doc.public_url && (
                        <a
                          href={doc.public_url}
                          target="_blank"
                          rel="noreferrer"
                          className="px-3 py-1.5 rounded-lg bg-pink-600 hover:bg-pink-700 text-white text-xs font-semibold shadow-sm transition-all"
                        >
                          Open File ↗
                        </a>
                      )}
                    </div>
                  </div>

                  {/* Expandable OCR text preview */}
                  {expandedDocId === doc.id && doc.ocr_markdown && (
                    <div className="mt-2 p-3 rounded-xl bg-white border border-slate-200 text-[11px] font-mono text-slate-700 max-h-48 overflow-y-auto whitespace-pre-wrap">
                      {doc.ocr_markdown}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Profile Update Form */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-6 mb-6">
          <div>
            <h2 className="text-xl font-bold text-slate-900">Maternal &amp; Parent Profile</h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Protected with bank-grade encryption and synchronized across your care continuum.
            </p>
          </div>
          {profileSaveSuccess && (
            <div className="px-4 py-2 rounded-xl bg-green-50 border border-green-200 text-green-700 text-xs font-semibold flex items-center gap-2">
              ✓ {awsSyncDetails || "Profile successfully updated!"}
            </div>
          )}
        </div>

        <form onSubmit={onSaveProfile} className="space-y-8">
          {/* 1. Basic Personal Info */}
          <div>
            <h3 className="text-sm font-bold text-pink-600 uppercase tracking-wider mb-4 flex items-center gap-2">
              <ParentIcon className="w-4 h-4 text-pink-500" />
              <span>1. Personal Information</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  required
                  value={parentProfile.fullName}
                  onChange={(e) => onProfileChange("fullName", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Age (Years)
                </label>
                <input
                  type="number"
                  required
                  value={parentProfile.age}
                  onChange={(e) => onProfileChange("age", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Blood Group
                </label>
                <select
                  value={parentProfile.bloodGroup}
                  onChange={(e) => onProfileChange("bloodGroup", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm bg-white focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                >
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Primary Contact Phone
                </label>
                <input
                  type="tel"
                  value={parentProfile.phone}
                  onChange={(e) => onProfileChange("phone", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Email Address / Unique ID
                </label>
                <input
                  type="email"
                  value={parentProfile.email}
                  onChange={(e) => onProfileChange("email", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Preferred Language
                </label>
                <input
                  type="text"
                  value={parentProfile.preferredLanguage}
                  onChange={(e) => onProfileChange("preferredLanguage", e.target.value)}
                  placeholder="e.g. English, Hindi, Spanish"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
            </div>
          </div>

          {/* 2. Pregnancy & Clinical Timeline */}
          <div>
            <h3 className="text-sm font-bold text-pink-600 uppercase tracking-wider mb-4">
              2. Pregnancy &amp; Gestational Details
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Current Gestational Week
                </label>
                <input
                  type="number"
                  value={parentProfile.gestationalWeeks}
                  onChange={(e) => onProfileChange("gestationalWeeks", e.target.value)}
                  placeholder="e.g. 32"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Estimated Due Date (EDD)
                </label>
                <input
                  type="date"
                  value={parentProfile.dueDate}
                  onChange={(e) => onProfileChange("dueDate", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Gravidity (Total Pregnancies)
                </label>
                <input
                  type="text"
                  value={parentProfile.gravidity}
                  onChange={(e) => onProfileChange("gravidity", e.target.value)}
                  placeholder="e.g. G2"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Parity (Past Deliveries)
                </label>
                <input
                  type="text"
                  value={parentProfile.parity}
                  onChange={(e) => onProfileChange("parity", e.target.value)}
                  placeholder="e.g. P1"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
            </div>
          </div>

          {/* 3. Emergency Contacts & Medical History */}
          <div>
            <h3 className="text-sm font-bold text-pink-600 uppercase tracking-wider mb-4">
              3. Emergency Referral &amp; Medical History
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Emergency Contact Name
                </label>
                <input
                  type="text"
                  value={parentProfile.emergencyContactName}
                  onChange={(e) => onProfileChange("emergencyContactName", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Relation
                </label>
                <input
                  type="text"
                  value={parentProfile.emergencyContactRelation}
                  onChange={(e) => onProfileChange("emergencyContactRelation", e.target.value)}
                  placeholder="e.g. Spouse / Mother"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Emergency Contact Phone
                </label>
                <input
                  type="tel"
                  value={parentProfile.emergencyContactPhone}
                  onChange={(e) => onProfileChange("emergencyContactPhone", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Known Drug / Food Allergies
                </label>
                <input
                  type="text"
                  value={parentProfile.knownAllergies}
                  onChange={(e) => onProfileChange("knownAllergies", e.target.value)}
                  placeholder="e.g. Penicillin, Sulfa drugs"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Preferred Referral / Delivery Facility
                </label>
                <input
                  type="text"
                  value={parentProfile.preferredFacility}
                  onChange={(e) => onProfileChange("preferredFacility", e.target.value)}
                  placeholder="e.g. District Civil Hospital"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
            </div>

            <div className="mt-4">
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Past Medical / Surgical Conditions
              </label>
              <textarea
                rows={2}
                value={parentProfile.medicalConditions}
                onChange={(e) => onProfileChange("medicalConditions", e.target.value)}
                placeholder="e.g. Previous C-section, Asthma, Gestational Diabetes"
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
              />
            </div>
          </div>

          {/* 4. Baby Continuity Section */}
          <div>
            <h3 className="text-sm font-bold text-pink-600 uppercase tracking-wider mb-4">
              4. Baby &amp; Newborn Monitoring Registry
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Baby Nickname / Full Name
                </label>
                <input
                  type="text"
                  value={parentProfile.babyName}
                  onChange={(e) => onProfileChange("babyName", e.target.value)}
                  placeholder="e.g. Baby Aarav"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  First-Year Monitoring Enrollment
                </label>
                <div className="h-10 flex items-center px-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 font-medium">
                  ✓ Auto-enrolled for 1W, 6W, 3M, 6M, 9M, 12M Checkups
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-4">
            <button
              type="button"
              onClick={onBackToHome}
              className="text-sm font-semibold text-slate-500 hover:text-slate-800"
            >
              ← Back to Landing Page
            </button>
            <button
              type="submit"
              disabled={profileSaving}
              className="px-6 py-3 rounded-full bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 disabled:bg-gray-400 transition-all flex items-center gap-2"
            >
              {profileSaving ? "Saving to Secure Profile..." : "Save Maternal Profile"}
            </button>
          </div>
        </form>
      </div>
    </section>
  );
}
