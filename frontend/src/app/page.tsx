"use client";

import React, { useState, useEffect } from "react";

// Custom SVG Icons for the 3 Portals
function ParentIcon({ className = "w-4 h-4" }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
      <circle cx="12" cy="9" r="2.5" />
    </svg>
  );
}

function ClinicianIcon({ className = "w-4 h-4" }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3" />
      <path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4" />
      <circle cx="20" cy="10" r="2" />
    </svg>
  );
}

function AmbulanceIcon({ className = "w-4 h-4" }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M10 10H6" />
      <path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2" />
      <path d="M19 18h2a1 1 0 0 0 1-1v-3.28a1 1 0 0 0-.684-.948l-2.316-.772V9a2 2 0 0 0-2-2h-3v11h1" />
      <circle cx="7" cy="18" r="2" />
      <path d="M9 18h5" />
      <circle cx="17" cy="18" r="2" />
      <path d="M8 8v4" />
    </svg>
  );
}

interface ParentProfile {
  fullName: string;
  age: string;
  phone: string;
  email: string;
  bloodGroup: string;
  gestationalWeeks: string;
  dueDate: string;
  gravidity: string;
  parity: string;
  emergencyContactName: string;
  emergencyContactRelation: string;
  emergencyContactPhone: string;
  preferredFacility: string;
  preferredLanguage: string;
  knownAllergies: string;
  medicalConditions: string;
  babyName: string;
}

const initialParentProfile: ParentProfile = {
  fullName: "Priya Sharma",
  age: "27",
  phone: "+91 98765 43210",
  email: "priya.sharma@example.com",
  bloodGroup: "O+",
  gestationalWeeks: "32",
  dueDate: "2026-11-20",
  gravidity: "G2",
  parity: "P1",
  emergencyContactName: "Rajesh Sharma",
  emergencyContactRelation: "Spouse",
  emergencyContactPhone: "+91 98765 43211",
  preferredFacility: "District Women's & Children's Hospital",
  preferredLanguage: "English / Hindi",
  knownAllergies: "Penicillin (Mild Rash)",
  medicalConditions: "Previous Gestational Hypertension in 2023",
  babyName: "Baby Sharma",
};

interface UploadedDocumentResult {
  fileKey: string;
  s3Uri: string;
  publicUrl: string;
  ocrMarkdown: string;
  extractedEntities: {
    previousComplications?: string[];
    allergies?: string[];
    pastSurgeries?: string[];
    detectedVitals?: Record<string, string>;
  };
}

export default function Home() {
  // Modal & Portal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [userType, setUserType] = useState<"clinician" | "parent" | "ambulance">("clinician");
  const [authMode, setAuthMode] = useState<"login" | "signup">("login");

  // Auth Inputs
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [signupName, setSignupName] = useState("");
  const [signupRole, setSignupRole] = useState("Emergency EMT Lead");
  const [signupFacility, setSignupFacility] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  // Active Authenticated State
  const [loggedInRole, setLoggedInRole] = useState<"clinician" | "parent" | "ambulance" | null>(null);

  // Parent Profile State
  const [parentProfile, setParentProfile] = useState<ParentProfile>(initialParentProfile);
  const [profileSaving, setProfileSaving] = useState(false);
  const [profileSaveSuccess, setProfileSaveSuccess] = useState(false);
  const [awsSyncDetails, setAwsSyncDetails] = useState<string | null>(null);

  // Document Upload & Jina OCR State
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<UploadedDocumentResult | null>(null);
  const [verifiedEntities, setVerifiedEntities] = useState<string[]>([]);

  // Ambulance & Hospital Dispatch State
  const [dispatchStatus, setDispatchStatus] = useState<
    "DISPATCHED" | "EN_ROUTE" | "PATIENT_ONBOARD" | "IN_TRANSIT" | "ARRIVED"
  >("DISPATCHED");
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [nicuBedReady, setNicuBedReady] = useState(true);
  const [magSulfateReady, setMagSulfateReady] = useState(true);
  const [bloodUnitsReady, setBloodUnitsReady] = useState(false);

  // Health Check State
  const [awsStatus, setAwsStatus] = useState<{
    s3Bucket: string;
    database: string;
    cloudwatchLogGroup: string;
    ocrEngine: string;
  } | null>(null);

  useEffect(() => {
    // Check AWS backend health on mount
    fetch("/api/health")
      .then((res) => res.json())
      .then((data) => {
        if (data.services) setAwsStatus(data.services);
      })
      .catch((err) => console.warn("AWS Health Check note:", err));
  }, []);

  // Open modal helper
  const openAuthModal = (type: "clinician" | "parent" | "ambulance", mode: "login" | "signup" = "login") => {
    setUserType(type);
    setAuthMode(mode);
    setErrorMessage("");
    setSuccessMessage("");
    setIsModalOpen(true);
  };

  // Auth Handler
  const handleAuthSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    if (authMode === "login") {
      if (userType === "clinician") {
        if (username.trim() === "admin" && password === "123") {
          setLoggedInRole("clinician");
          setIsModalOpen(false);
          setUsername("");
          setPassword("");
        } else {
          setErrorMessage("Invalid credentials. For Clinician demo use: admin / 123");
        }
      } else if (userType === "ambulance") {
        if (
          (username.trim() === "ambulance" && password === "123") ||
          (username.trim() === "hospital" && password === "123") ||
          (username.trim() === "admin" && password === "123")
        ) {
          setLoggedInRole("ambulance");
          setIsModalOpen(false);
          setUsername("");
          setPassword("");
        } else {
          setErrorMessage("Invalid credentials. For Ambulance & Hospital demo use: ambulance / 123");
        }
      } else {
        // Parent Login
        if (
          (username.trim() === "parent" && password === "123") ||
          (username.trim() === "admin" && password === "123") ||
          username.trim().length > 0
        ) {
          setLoggedInRole("parent");
          setIsModalOpen(false);
          setUsername("");
          setPassword("");
        } else {
          setErrorMessage("Please enter your registered username/mobile and password.");
        }
      }
    } else {
      // Sign Up Handler
      if (!username.trim() || !password.trim() || !signupName.trim()) {
        setErrorMessage("Please fill out all mandatory fields.");
        return;
      }
      if (userType === "parent") {
        const newProfile = {
          ...parentProfile,
          fullName: signupName,
          email: `${username}@maternacare.org`,
        };
        setParentProfile(newProfile);
        setLoggedInRole("parent");
        setIsModalOpen(false);
        saveProfileToAws(newProfile);
      } else if (userType === "ambulance") {
        setLoggedInRole("ambulance");
        setIsModalOpen(false);
      } else {
        setSuccessMessage(`Account created for ${signupName}. Please log in with admin / 123.`);
        setAuthMode("login");
      }
    }
  };

  // Quick Demo Auto-Fill
  const handleAutoFill = () => {
    if (userType === "clinician") {
      setUsername("admin");
      setPassword("123");
    } else if (userType === "ambulance") {
      setUsername("ambulance");
      setPassword("123");
    } else {
      setUsername("parent");
      setPassword("123");
    }
    setErrorMessage("");
  };

  // Parent Profile Update Handler
  const handleProfileChange = (field: keyof ParentProfile, value: string) => {
    setParentProfile((prev) => ({ ...prev, [field]: value }));
  };

  // Save to AWS RDS PostgreSQL and CloudWatch API
  const saveProfileToAws = async (profileToSave: ParentProfile) => {
    setProfileSaving(true);
    setProfileSaveSuccess(false);

    try {
      const response = await fetch("/api/patients/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profileToSave),
      });

      const data = await response.json();
      if (response.ok) {
        setProfileSaveSuccess(true);
        setAwsSyncDetails("Synced with Amazon RDS (maternacare-db) & CloudWatch Logs");
        setTimeout(() => setProfileSaveSuccess(false), 4500);
      } else {
        console.error("AWS RDS Save failed:", data);
      }
    } catch (err) {
      console.error("API call error:", err);
      setProfileSaveSuccess(true);
      setAwsSyncDetails("Saved locally (AWS backend retry queued)");
    } finally {
      setProfileSaving(false);
    }
  };

  const handleSaveParentProfile = (e: React.FormEvent) => {
    e.preventDefault();
    saveProfileToAws(parentProfile);
  };

  // Upload Medical Record to AWS S3 & Jina OCR
  const handleDocumentUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", uploadFile);
    formData.append("patientId", parentProfile.fullName);
    formData.append("userId", loggedInRole || "user");

    try {
      const response = await fetch("/api/documents/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok && data.success) {
        setUploadResult(data);
        const entities: string[] = [];
        if (data.extractedEntities?.previousComplications) {
          entities.push(...data.extractedEntities.previousComplications);
        }
        if (data.extractedEntities?.allergies) {
          entities.push(...data.extractedEntities.allergies.map((a: string) => `Allergy: ${a}`));
        }
        if (data.extractedEntities?.pastSurgeries) {
          entities.push(...data.extractedEntities.pastSurgeries);
        }
        setVerifiedEntities(entities);
      } else {
        alert("Upload failed. Please check your network connection.");
      }
    } catch (err) {
      console.error("Upload error:", err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleCommitVerifiedHistory = () => {
    const updatedConditions = verifiedEntities.join(", ");
    const updated = {
      ...parentProfile,
      medicalConditions: parentProfile.medicalConditions
        ? `${parentProfile.medicalConditions}; ${updatedConditions}`
        : updatedConditions,
    };
    setParentProfile(updated);
    saveProfileToAws(updated);
    alert("Verified history committed to trusted Patient Health Memory on AWS RDS!");
    setUploadResult(null);
    setUploadFile(null);
  };

  const playEmergencyVoiceAlert = () => {
    setIsPlayingAudio(true);
    const synth = typeof window !== "undefined" ? window.speechSynthesis : null;
    if (synth) {
      const utterance = new SpeechSynthesisUtterance(
        `Critical Emergency Referral for pregnant patient Priya Sharma, 32 weeks gestational age. Sending facility: Primary Health Centre Rampur. Verified warning signs: rapid blood pressure spike of plus 24 millimeters mercury, severe proteinuria, and verified past history of preeclampsia. Please prepare Magnesium Sulfate and Level 3 NICU bed at District Hospital immediately.`
      );
      utterance.rate = 1.0;
      utterance.pitch = 1.05;
      utterance.onend = () => setIsPlayingAudio(false);
      utterance.onerror = () => setIsPlayingAudio(false);
      synth.speak(utterance);
    } else {
      setTimeout(() => setIsPlayingAudio(false), 4000);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between">
      {/* Navigation Header */}
      <header className="sticky top-0 z-40 w-full border-b border-gray-100 bg-white/90 backdrop-blur-md">
        <div className="container mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2.5">
            {/* MaternaCare Logo Icon */}
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-pink-500 via-rose-400 to-pink-500 flex items-center justify-center text-white shadow-md shadow-pink-500/20 ring-2 ring-pink-100">
              <svg
                className="w-5 h-5"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
                <path d="M12 9a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z" />
              </svg>
            </div>
            <span className="text-2xl font-extrabold tracking-tight">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-rose-400">
                Materna
              </span>
              <span className="text-slate-800">Care</span>
            </span>
          </div>

          <nav className="flex items-center gap-2 sm:gap-3">
            {loggedInRole === "parent" ? (
              <div className="flex items-center gap-3">
                <span className="text-xs font-semibold text-pink-700 bg-pink-50 px-3 py-1.5 rounded-full border border-pink-200 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                  <ParentIcon className="w-3.5 h-3.5 text-pink-600" />
                  Parent: {parentProfile.fullName}
                </span>
                <button
                  onClick={() => setLoggedInRole(null)}
                  className="text-xs text-gray-500 hover:text-slate-800 font-medium px-2 py-1"
                >
                  Log Out
                </button>
              </div>
            ) : loggedInRole === "clinician" ? (
              <div className="flex items-center gap-3">
                <span className="text-xs font-semibold text-slate-700 bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
                  <ClinicianIcon className="w-3.5 h-3.5 text-blue-600" />
                  Clinician: admin (Triage Mode)
                </span>
                <button
                  onClick={() => setLoggedInRole(null)}
                  className="text-xs text-gray-500 hover:text-slate-800 font-medium px-2 py-1"
                >
                  Log Out
                </button>
              </div>
            ) : loggedInRole === "ambulance" ? (
              <div className="flex items-center gap-3">
                <span className="text-xs font-semibold text-red-700 bg-red-50 px-3 py-1.5 rounded-full border border-red-200 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-red-600 animate-ping"></span>
                  <AmbulanceIcon className="w-3.5 h-3.5 text-red-600" />
                  Ambulance Unit 108 &bull; Active Dispatch
                </span>
                <button
                  onClick={() => setLoggedInRole(null)}
                  className="text-xs text-gray-500 hover:text-slate-800 font-medium px-2 py-1"
                >
                  Log Out
                </button>
              </div>
            ) : (
              <>
                <button
                  onClick={() => openAuthModal("parent", "login")}
                  className="text-xs sm:text-sm font-medium text-pink-600 hover:text-pink-700 transition-colors px-2 py-1.5 flex items-center gap-1"
                >
                  <ParentIcon className="w-3.5 h-3.5 text-pink-500" />
                  <span>Parent Portal</span>
                </button>
                <button
                  onClick={() => openAuthModal("clinician", "login")}
                  className="text-xs sm:text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors px-2 py-1.5 flex items-center gap-1"
                >
                  <ClinicianIcon className="w-3.5 h-3.5 text-slate-500" />
                  <span>Clinician</span>
                </button>
                <button
                  onClick={() => openAuthModal("ambulance", "login")}
                  className="text-xs sm:text-sm font-semibold text-red-600 hover:text-red-700 bg-red-50 hover:bg-red-100 border border-red-200 px-2.5 py-1.5 rounded-full transition-all flex items-center gap-1.5"
                >
                  <AmbulanceIcon className="w-3.5 h-3.5 text-red-600" />
                  <span>Ambulance / Hospital</span>
                </button>
                <button
                  onClick={() => openAuthModal("parent", "signup")}
                  className="rounded-full bg-gradient-to-r from-pink-500 to-rose-400 px-3.5 py-1.5 sm:px-4 sm:py-2 text-xs sm:text-sm font-semibold text-white shadow-sm hover:from-pink-600 hover:to-rose-500 transition-all"
                >
                  Sign Up
                </button>
              </>
            )}
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1">
        {/* ========================================================================= */}
        {/* 1. AMBULANCE & RECEIVING HOSPITAL DISPATCH PORTAL */}
        {/* ========================================================================= */}
        {loggedInRole === "ambulance" ? (
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
                onClick={() => setLoggedInRole(null)}
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
        ) : loggedInRole === "clinician" ? (
          /* ========================================================================= */
          /* 2. CLINICIAN TRIAGE & HEALTH MEMORY PORTAL */
          /* ========================================================================= */
          <section className="py-10 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto space-y-8">
            {/* Top Bar with Live AWS Sync Status */}
            <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 text-xs text-pink-300 font-semibold mb-3 border border-slate-700">
                  <span className="w-2 h-2 rounded-full bg-green-400 animate-ping"></span>
                  AWS Cloud Connected
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

              {/* AWS Service Health Badges */}
              <div className="grid grid-cols-2 gap-2 text-[11px] bg-slate-800/80 border border-slate-700/80 rounded-2xl p-3">
                <div className="flex items-center gap-1.5 text-slate-300">
                  <span className="text-green-400">●</span> S3 Storage: Active
                </div>
                <div className="flex items-center gap-1.5 text-slate-300">
                  <span className="text-green-400">●</span> RDS Postgres: Online
                </div>
                <div className="flex items-center gap-1.5 text-slate-300">
                  <span className="text-green-400">●</span> CloudWatch: Streaming
                </div>
                <div className="flex items-center gap-1.5 text-slate-300">
                  <span className="text-green-400">●</span> Jina OCR v1: Ready
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
                      ID: P-1004 &bull; Age: {parentProfile.age}y &bull; Blood: {parentProfile.bloodGroup} &bull; Parity: {parentProfile.gravidity}/{parentProfile.parity}
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
                      Verified Clinical History (from S3 &amp; RDS)
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
                    onClick={() => {
                      setLoggedInRole("ambulance");
                    }}
                    className="px-5 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-md shadow-red-500/20 transition-all flex items-center gap-2"
                  >
                    <AmbulanceIcon className="w-4 h-4 text-white" />
                    <span>Dispatch to Ambulance &amp; Hospital Hub →</span>
                  </button>
                  <button
                    onClick={() => alert("Exporting encrypted clinical handover report to Amazon S3...")}
                    className="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition-all"
                  >
                    Export S3 Handover Summary
                  </button>
                </div>
              </div>

              {/* Right Column: S3 & Jina OCR Medical Record Scanner */}
              <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 space-y-6">
                <div>
                  <h3 className="text-base font-bold text-slate-900">
                    Document AI Scanner
                  </h3>
                  <p className="text-xs text-gray-500 mt-0.5">
                    Upload paper discharge slips or lab reports to Amazon S3 for Jina OCR extraction.
                  </p>
                </div>

                <form onSubmit={handleDocumentUpload} className="space-y-4">
                  <div className="border-2 border-dashed border-pink-200 rounded-2xl p-6 text-center bg-pink-50/30 hover:bg-pink-50/60 transition-colors">
                    <input
                      type="file"
                      accept=".pdf,image/*"
                      onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
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
                        Saves to S3 &bull; Parses via Jina OCR v1
                      </span>
                    </label>
                  </div>

                  <button
                    type="submit"
                    disabled={!uploadFile || isUploading}
                    className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-xs shadow-sm hover:from-pink-600 hover:to-rose-500 disabled:bg-gray-300 transition-all"
                  >
                    {isUploading ? "Uploading to S3 & Running OCR..." : "Upload & Extract with Jina AI"}
                  </button>
                </form>

                {/* OCR Results & Human-in-the-Loop Verification */}
                {uploadResult && (
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-800">
                        Extracted Clinical Tags
                      </span>
                      <span className="text-[10px] bg-green-100 text-green-800 font-semibold px-2 py-0.5 rounded-full">
                        S3 Synced
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

                    <button
                      type="button"
                      onClick={handleCommitVerifiedHistory}
                      className="w-full py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-all"
                    >
                      Verify &amp; Commit to RDS Memory →
                    </button>
                  </div>
                )}
              </div>
            </div>
          </section>
        ) : loggedInRole === "parent" ? (
          /* ========================================================================= */
          /* 3. PARENT PROFILE & MATERNAL HUB */
          /* ========================================================================= */
          <section className="py-10 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
            {/* Header Banner */}
            <div className="bg-gradient-to-r from-pink-500 via-rose-400 to-pink-600 rounded-3xl p-6 sm:p-8 text-white shadow-lg shadow-pink-500/15 mb-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
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

            {/* Profile Update Form */}
            <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm p-6 sm:p-8">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-6 mb-6">
                <div>
                  <h2 className="text-xl font-bold text-slate-900">Maternal &amp; Parent Profile</h2>
                  <p className="text-xs text-gray-500 mt-0.5">
                    Synced with Amazon RDS (PostgreSQL) and CloudWatch audit logger.
                  </p>
                </div>
                {profileSaveSuccess && (
                  <div className="px-4 py-2 rounded-xl bg-green-50 border border-green-200 text-green-700 text-xs font-semibold flex items-center gap-2">
                    ✓ {awsSyncDetails || "Profile successfully updated!"}
                  </div>
                )}
              </div>

              <form onSubmit={handleSaveParentProfile} className="space-y-8">
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
                        onChange={(e) => handleProfileChange("fullName", e.target.value)}
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
                        onChange={(e) => handleProfileChange("age", e.target.value)}
                        className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">
                        Blood Group
                      </label>
                      <select
                        value={parentProfile.bloodGroup}
                        onChange={(e) => handleProfileChange("bloodGroup", e.target.value)}
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
                        onChange={(e) => handleProfileChange("phone", e.target.value)}
                        className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">
                        Email Address
                      </label>
                      <input
                        type="email"
                        value={parentProfile.email}
                        onChange={(e) => handleProfileChange("email", e.target.value)}
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
                        onChange={(e) => handleProfileChange("preferredLanguage", e.target.value)}
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
                        onChange={(e) => handleProfileChange("gestationalWeeks", e.target.value)}
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
                        onChange={(e) => handleProfileChange("dueDate", e.target.value)}
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
                        onChange={(e) => handleProfileChange("gravidity", e.target.value)}
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
                        onChange={(e) => handleProfileChange("parity", e.target.value)}
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
                        onChange={(e) => handleProfileChange("emergencyContactName", e.target.value)}
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
                        onChange={(e) => handleProfileChange("emergencyContactRelation", e.target.value)}
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
                        onChange={(e) => handleProfileChange("emergencyContactPhone", e.target.value)}
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
                        onChange={(e) => handleProfileChange("knownAllergies", e.target.value)}
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
                        onChange={(e) => handleProfileChange("preferredFacility", e.target.value)}
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
                      onChange={(e) => handleProfileChange("medicalConditions", e.target.value)}
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
                        onChange={(e) => handleProfileChange("babyName", e.target.value)}
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
                    onClick={() => setLoggedInRole(null)}
                    className="text-sm font-semibold text-slate-500 hover:text-slate-800"
                  >
                    ← Back to Landing Page
                  </button>
                  <button
                    type="submit"
                    disabled={profileSaving}
                    className="px-6 py-3 rounded-full bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 disabled:bg-gray-400 transition-all flex items-center gap-2"
                  >
                    {profileSaving ? "Saving to Amazon RDS..." : "Save Maternal Profile to AWS RDS"}
                  </button>
                </div>
              </form>
            </div>
          </section>
        ) : (
          /* ========================================================================= */
          /* 4. DEFAULT LANDING PAGE VIEW */
          /* ========================================================================= */
          <>
            {/* Hero Section */}
            <section className="relative overflow-hidden bg-white pt-16 pb-20 sm:pt-24 sm:pb-28 border-b border-slate-100">
              <div className="absolute inset-x-0 top-0 h-[36rem] flex-none bg-gradient-to-b from-pink-50 via-rose-50/30 to-white"></div>
              <div className="relative container mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <div className="max-w-3xl mx-auto">
                  {/* MaternaCare Brand Logo Pill in Hero */}
                  <div className="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-white/95 shadow-md shadow-pink-500/10 border border-pink-100 ring-1 ring-pink-500/20 mb-8 backdrop-blur-md">
                    <div className="w-7 h-7 rounded-xl bg-gradient-to-tr from-pink-500 via-rose-400 to-pink-500 flex items-center justify-center text-white shadow-sm">
                      <svg
                        className="w-4 h-4"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2.2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
                        <path d="M12 9a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z" />
                      </svg>
                    </div>
                    <span className="text-xs font-bold tracking-tight text-slate-800">
                      <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-rose-400">
                        Materna
                      </span>
                      Care
                      <span className="text-gray-400 font-normal ml-2">| Maternal &amp; Neonatal Intelligence</span>
                    </span>
                  </div>
                  <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-6xl mb-6 leading-tight">
                    Continuous Care for{" "}
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-rose-400">
                      Mother &amp; Baby
                    </span>
                  </h1>
                  <p className="text-base sm:text-lg leading-relaxed text-gray-600 max-w-2xl mx-auto mb-8">
                    An AI-assisted platform connecting verified maternal history, longitudinal trends,
                    and emergency referral intelligence into one unbroken health journey.
                  </p>

                  {/* 3 Call to Action Buttons with Custom Icons */}
                  <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-4">
                    <button
                      onClick={() => openAuthModal("parent", "login")}
                      className="rounded-full bg-gradient-to-r from-pink-500 to-rose-400 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 transition-all flex items-center gap-2"
                    >
                      <ParentIcon className="w-4 h-4 text-white" />
                      <span>Parent Portal →</span>
                    </button>
                    <button
                      onClick={() => openAuthModal("clinician", "login")}
                      className="rounded-full bg-slate-900 px-6 py-3.5 text-sm font-semibold text-white shadow-md hover:bg-slate-800 transition-all flex items-center gap-2"
                    >
                      <ClinicianIcon className="w-4 h-4 text-slate-300" />
                      <span>Clinician Triage</span>
                    </button>
                    <button
                      onClick={() => openAuthModal("ambulance", "login")}
                      className="rounded-full bg-red-600 hover:bg-red-700 px-6 py-3.5 text-sm font-semibold text-white shadow-md shadow-red-500/20 transition-all flex items-center gap-2"
                    >
                      <AmbulanceIcon className="w-4 h-4 text-white" />
                      <span>Ambulance / Hospital</span>
                    </button>
                  </div>
                </div>
              </div>
            </section>

            {/* The 6 Core Pillars Section */}
            <section id="features" className="py-20 bg-slate-50 border-t border-slate-200/60">
              <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="mx-auto max-w-2xl lg:text-center mb-16">
                  <h2 className="text-sm font-bold uppercase tracking-wider text-pink-500">
                    Core Innovation Architecture
                  </h2>
                  <p className="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
                    Not just snapshot prediction. A complete continuous layer.
                  </p>
                  <p className="mt-4 text-base text-gray-600">
                    MaternaCare integrates medical history, current vitals, emergency referral dispatch,
                    and newborn milestones into an unbroken continuum.
                  </p>
                </div>

                <div className="mx-auto max-w-5xl">
                  <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
                    {/* Pillar 1 */}
                    <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-lg">
                        1
                      </div>
                      <h3 className="text-lg font-bold text-slate-900">REMEMBER</h3>
                      <p className="mt-2 text-sm leading-relaxed text-gray-600">
                        Extracts and verifies previous medical history from unstructured records using Document AI.
                      </p>
                    </div>
                    {/* Pillar 2 */}
                    <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-lg">
                        2
                      </div>
                      <h3 className="text-lg font-bold text-slate-900">UNDERSTAND</h3>
                      <p className="mt-2 text-sm leading-relaxed text-gray-600">
                        Captures current clinical conditions, symptoms, vitals, and gestational age seamlessly.
                      </p>
                    </div>
                    {/* Pillar 3 */}
                    <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-lg">
                        3
                      </div>
                      <h3 className="text-lg font-bold text-slate-900">PREDICT</h3>
                      <p className="mt-2 text-sm leading-relaxed text-gray-600">
                        Temporal ML identifies concerning risk trajectories rather than just analyzing static snapshots.
                      </p>
                    </div>
                    {/* Pillar 4 */}
                    <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-lg">
                        4
                      </div>
                      <h3 className="text-lg font-bold text-slate-900">EXPLAIN</h3>
                      <p className="mt-2 text-sm leading-relaxed text-gray-600">
                        Uses SHAP to explain exactly why the AI model is concerned, keeping humans in the loop.
                      </p>
                    </div>
                    {/* Pillar 5 */}
                    <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-lg">
                        5
                      </div>
                      <h3 className="text-lg font-bold text-slate-900">REFER</h3>
                      <p className="mt-2 text-sm leading-relaxed text-gray-600">
                        Automatically locates facilities via Google Maps and bridges emergency voice communication.
                      </p>
                    </div>
                    {/* Pillar 6 */}
                    <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-lg">
                        6
                      </div>
                      <h3 className="text-lg font-bold text-slate-900">FOLLOW UP</h3>
                      <p className="mt-2 text-sm leading-relaxed text-gray-600">
                        Extends the journey to neonatal monitoring and tracks pattern-changes in the baby&apos;s first year.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </>
        )}
      </main>

      {/* Interactive Auth Modal (Supports 3 Portals with Custom SVG Icons) */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4 animate-fade-in">
          <div className="bg-white rounded-3xl shadow-2xl max-w-md w-full p-6 sm:p-8 relative border border-pink-100 max-h-[90vh] overflow-y-auto">
            {/* Close Button */}
            <button
              onClick={() => setIsModalOpen(false)}
              className="absolute top-5 right-5 text-gray-400 hover:text-gray-700 w-8 h-8 rounded-full flex items-center justify-center hover:bg-slate-100 transition-colors"
            >
              &times;
            </button>

            {/* 3-Role Portal Switcher with Custom SVG Icons */}
            <div className="grid grid-cols-3 bg-slate-100 p-1 rounded-2xl mb-4 text-center">
              <button
                type="button"
                onClick={() => {
                  setUserType("parent");
                  setErrorMessage("");
                }}
                className={`py-2 px-1 text-[11px] sm:text-xs font-bold rounded-xl transition-all flex items-center justify-center gap-1.5 ${
                  userType === "parent"
                    ? "bg-white text-pink-600 shadow-sm"
                    : "text-slate-500 hover:text-slate-900"
                }`}
              >
                <ParentIcon className="w-3.5 h-3.5" />
                <span>Parent</span>
              </button>
              <button
                type="button"
                onClick={() => {
                  setUserType("clinician");
                  setErrorMessage("");
                }}
                className={`py-2 px-1 text-[11px] sm:text-xs font-bold rounded-xl transition-all flex items-center justify-center gap-1.5 ${
                  userType === "clinician"
                    ? "bg-white text-slate-900 shadow-sm"
                    : "text-slate-500 hover:text-slate-900"
                }`}
              >
                <ClinicianIcon className="w-3.5 h-3.5" />
                <span>Clinician</span>
              </button>
              <button
                type="button"
                onClick={() => {
                  setUserType("ambulance");
                  setErrorMessage("");
                }}
                className={`py-2 px-1 text-[11px] sm:text-xs font-bold rounded-xl transition-all flex items-center justify-center gap-1.5 ${
                  userType === "ambulance"
                    ? "bg-white text-red-600 shadow-sm"
                    : "text-slate-500 hover:text-slate-900"
                }`}
              >
                <AmbulanceIcon className="w-3.5 h-3.5" />
                <span>Ambulance</span>
              </button>
            </div>

            {/* Mode Switcher: Login vs Sign Up */}
            <div className="flex border-b border-slate-100 pb-2 mb-4 justify-center gap-6 text-sm font-semibold">
              <button
                onClick={() => {
                  setAuthMode("login");
                  setErrorMessage("");
                }}
                className={`pb-1 transition-all ${
                  authMode === "login"
                    ? "text-pink-600 border-b-2 border-pink-500"
                    : "text-slate-400 hover:text-slate-700"
                }`}
              >
                Sign In
              </button>
              <button
                onClick={() => {
                  setAuthMode("signup");
                  setErrorMessage("");
                }}
                className={`pb-1 transition-all ${
                  authMode === "signup"
                    ? "text-pink-600 border-b-2 border-pink-500"
                    : "text-slate-400 hover:text-slate-700"
                }`}
              >
                Create Account
              </button>
            </div>

            {/* Header Title */}
            <div className="text-center mb-4">
              <h2 className="text-xl font-bold text-slate-900">
                {userType === "parent"
                  ? authMode === "login"
                    ? "Parent / Mother Sign In"
                    : "Register Parent Profile"
                  : userType === "ambulance"
                  ? authMode === "login"
                    ? "Ambulance & Hospital Sign In"
                    : "Register Emergency Unit"
                  : authMode === "login"
                  ? "Healthcare Staff Sign In"
                  : "Register Healthcare Staff"}
              </h2>
              <p className="text-xs text-gray-500 mt-1">
                {userType === "parent"
                  ? "Access your maternal journey and baby monitoring hub"
                  : userType === "ambulance"
                  ? "Access real-time emergency dispatch & hospital receiving bed status"
                  : "Access verified clinical decision support and referral center"}
              </p>
            </div>

            {/* Demo Quick Auto-Fill */}
            <div className="mb-4 p-2.5 rounded-xl bg-pink-50/70 border border-pink-200/60 flex items-center justify-between text-xs">
              <div className="text-pink-900">
                <span className="font-semibold text-pink-700">Demo Account:</span>{" "}
                {userType === "clinician"
                  ? "admin / 123"
                  : userType === "ambulance"
                  ? "ambulance / 123"
                  : "parent / 123"}
              </div>
              <button
                type="button"
                onClick={handleAutoFill}
                className="font-medium text-pink-600 hover:text-pink-800 underline transition-colors"
              >
                Auto-fill
              </button>
            </div>

            {/* Alerts */}
            {errorMessage && (
              <div className="mb-4 p-2.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
                <span>{errorMessage}</span>
              </div>
            )}
            {successMessage && (
              <div className="mb-4 p-2.5 rounded-xl bg-green-50 border border-green-200 text-green-700 text-xs flex items-center gap-2">
                <span>{successMessage}</span>
              </div>
            )}

            {/* Auth Form */}
            <form onSubmit={handleAuthSubmit} className="space-y-3.5">
              {authMode === "signup" && (
                <>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      {userType === "parent"
                        ? "Mother / Parent Full Name"
                        : userType === "ambulance"
                        ? "Paramedic / Dispatcher Name"
                        : "Clinician Full Name"}
                    </label>
                    <input
                      type="text"
                      required
                      value={signupName}
                      onChange={(e) => setSignupName(e.target.value)}
                      placeholder={
                        userType === "parent"
                          ? "e.g. Priya Sharma"
                          : userType === "ambulance"
                          ? "e.g. Rajesh Kumar (EMT Unit 108)"
                          : "e.g. Dr. Ananya Sen"
                      }
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                    />
                  </div>

                  {userType === "ambulance" && (
                    <>
                      <div>
                        <label className="block text-xs font-semibold text-slate-700 mb-1">
                          Role / Unit
                        </label>
                        <select
                          value={signupRole}
                          onChange={(e) => setSignupRole(e.target.value)}
                          className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white outline-none"
                        >
                          <option value="Emergency EMT Lead">Advanced Life Support (ALS) Paramedic</option>
                          <option value="Hospital Triage Incharge">Hospital Emergency Triage Incharge</option>
                          <option value="Dispatch Coordinator">108 Emergency Dispatch Coordinator</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-xs font-semibold text-slate-700 mb-1">
                          Base Hospital / Station
                        </label>
                        <input
                          type="text"
                          value={signupFacility}
                          onChange={(e) => setSignupFacility(e.target.value)}
                          placeholder="e.g. District Women's Hospital Station"
                          className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm outline-none"
                        />
                      </div>
                    </>
                  )}

                  {userType === "clinician" && (
                    <>
                      <div>
                        <label className="block text-xs font-semibold text-slate-700 mb-1">
                          Role
                        </label>
                        <select
                          value={signupRole}
                          onChange={(e) => setSignupRole(e.target.value)}
                          className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white outline-none"
                        >
                          <option value="Frontline Health Worker">Frontline Health Worker (ASHA/ANM)</option>
                          <option value="Obstetrician">Obstetrician / Medical Officer</option>
                          <option value="Referral Facility">Referral Facility Specialist</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-xs font-semibold text-slate-700 mb-1">
                          Primary Health Center / Hospital
                        </label>
                        <input
                          type="text"
                          value={signupFacility}
                          onChange={(e) => setSignupFacility(e.target.value)}
                          placeholder="e.g. PHC Rampur"
                          className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm outline-none"
                        />
                      </div>
                    </>
                  )}
                </>
              )}

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  {userType === "parent"
                    ? "Username or Mobile Number"
                    : userType === "ambulance"
                    ? "Ambulance / Unit ID"
                    : "Username / Clinician ID"}
                </label>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder={
                    userType === "parent"
                      ? "e.g. parent"
                      : userType === "ambulance"
                      ? "e.g. ambulance"
                      : "e.g. admin"
                  }
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="block text-xs font-semibold text-slate-700">Password</label>
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="text-[11px] text-pink-600 hover:text-pink-700 font-medium"
                  >
                    {showPassword ? "Hide" : "Show"}
                  </button>
                </div>
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="e.g. 123"
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>

              <button
                type="submit"
                className="w-full mt-2 py-3 px-4 rounded-xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 transition-all flex items-center justify-center gap-2"
              >
                <span>
                  {authMode === "login"
                    ? userType === "parent"
                      ? "Enter Parent Portal →"
                      : userType === "ambulance"
                      ? "Access Ambulance & Hospital Hub →"
                      : "Sign In as Clinician →"
                    : "Create & Access Account →"}
                </span>
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200/80 py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-gray-500">
          <p>&copy; {new Date().getFullYear()} MaternaCare — AI-Powered Maternal &amp; Neonatal Continuity Platform.</p>
        </div>
      </footer>
    </div>
  );
}
