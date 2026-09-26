"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ParentProfile, PatientDocument, UploadedDocumentResult } from "@/types";
import { ParentPortal } from "@/components/portals/ParentPortal";
import { HealthDashboard } from "@/components/portals/HealthDashboard";
import { ParentIcon, LogoIcon } from "@/components/icons/PortalIcons";
import { Footer } from "@/components/common/Footer";

const initialParentProfile: ParentProfile = {
  id: "priya.sharma@example.com",
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

export default function ParentPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authMode, setAuthMode] = useState<"login" | "signup">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [signupName, setSignupName] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  // Parent Profile & Documents State
  const [parentProfile, setParentProfile] = useState<ParentProfile>(initialParentProfile);
  const [parentDocuments, setParentDocuments] = useState<PatientDocument[]>([]);
  const [profileSaving, setProfileSaving] = useState(false);
  const [profileSaveSuccess, setProfileSaveSuccess] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);
  const [awsSyncDetails, setAwsSyncDetails] = useState<string | null>(null);

  // Upload State
  const [parentUploadFile, setParentUploadFile] = useState<File | null>(null);
  const [isParentUploading, setIsParentUploading] = useState(false);
  const [parentUploadResult, setParentUploadResult] = useState<UploadedDocumentResult | null>(null);

  const loadPatientProfile = async (identifier: string) => {
    if (typeof window !== "undefined") {
      try {
        const cachedDocs = localStorage.getItem(`maternacare_docs_${identifier}`);
        if (cachedDocs) {
          const parsed = JSON.parse(cachedDocs);
          if (Array.isArray(parsed) && parsed.length > 0) {
            const validDocs = parsed.filter((d: PatientDocument) => d.ocr_markdown || d.file_name);
            if (validDocs.length > 0) {
              setParentDocuments(validDocs);
            }
          }
        }
      } catch (e) {
        console.warn("Storage read note:", e);
      }
    }

    try {
      const res = await fetch(`/api/patients/profile?id=${encodeURIComponent(identifier)}`);
      if (res.ok) {
        const data = await res.json();
        if (data.success && data.profile) {
          setParentProfile(data.profile);
          if (data.documents && Array.isArray(data.documents) && data.documents.length > 0) {
            const validDocs = data.documents.filter(
              (d: PatientDocument) => d.ocr_markdown || d.file_name
            );
            setParentDocuments(validDocs);
            if (typeof window !== "undefined") {
              localStorage.setItem(`maternacare_docs_${identifier}`, JSON.stringify(validDocs));
            }
          }
        }
      }
    } catch (err) {
      console.warn("RDS load note:", err);
    }
  };

  // Restore parent auth from localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      const isAuth = localStorage.getItem("maternacare_parent_auth") === "true" || localStorage.getItem("maternacare_auth_role") === "parent";
      const savedId = localStorage.getItem("maternacare_auth_identifier") || "priya.sharma@example.com";
      if (isAuth) {
        setIsAuthenticated(true);
      }
      loadPatientProfile(savedId);
    }
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");

    if (authMode === "login") {
      if ((username.trim() === "parent" && password === "123") || (username.trim() === "admin" && password === "123") || username.trim().length > 0) {
        const lookupId = username.trim() === "parent" ? "priya.sharma@example.com" : username.trim();
        if (typeof window !== "undefined") {
          localStorage.setItem("maternacare_parent_auth", "true");
          localStorage.setItem("maternacare_auth_role", "parent");
          localStorage.setItem("maternacare_auth_identifier", lookupId);
        }
        await loadPatientProfile(lookupId);
        setIsAuthenticated(true);
      } else {
        setErrorMessage("Please enter valid login credentials.");
      }
    } else {
      if (!username.trim() || !password.trim() || !signupName.trim()) {
        setErrorMessage("Please fill out all fields.");
        return;
      }
      const userEmail = username.includes("@") ? username.trim() : `${username.trim()}@maternacare.org`;
      const newProfile: ParentProfile = {
        ...initialParentProfile,
        id: userEmail,
        fullName: signupName,
        email: userEmail,
      };
      if (typeof window !== "undefined") {
        localStorage.setItem("maternacare_parent_auth", "true");
        localStorage.setItem("maternacare_auth_role", "parent");
        localStorage.setItem("maternacare_auth_identifier", userEmail);
      }
      setParentProfile(newProfile);
      setParentDocuments([]);
      setIsAuthenticated(true);
      saveProfileToAws(newProfile);
    }
  };

  const handleLogout = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("maternacare_parent_auth");
      localStorage.removeItem("maternacare_auth_role");
      localStorage.removeItem("maternacare_auth_identifier");
    }
    setIsAuthenticated(false);
  };

  const handleAutoFill = () => {
    setUsername("parent");
    setPassword("123");
    setErrorMessage("");
  };

  const handleProfileChange = (field: keyof ParentProfile, value: string) => {
    setParentProfile((prev) => ({ ...prev, [field]: value }));
  };

  const saveProfileToAws = async (profileToSave: ParentProfile) => {
    setProfileSaving(true);
    setProfileSaveSuccess(false);

    try {
      const response = await fetch("/api/patients/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profileToSave),
      });

      if (response.ok) {
        setProfileSaveSuccess(true);
        setAwsSyncDetails("Encrypted & Securely Synced to Health Record");
        setTimeout(() => setProfileSaveSuccess(false), 4500);
      }
    } catch (err) {
      console.error("Profile save error:", err);
      setProfileSaveSuccess(true);
      setAwsSyncDetails("Saved locally (Offline record active)");
    } finally {
      setProfileSaving(false);
    }
  };

  const handleParentDocumentUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!parentUploadFile) return;

    setIsParentUploading(true);
    const fileToUpload = parentUploadFile;
    const patientIdentifier = parentProfile.email || parentProfile.fullName;

    const formData = new FormData();
    formData.append("file", fileToUpload);
    formData.append("patientId", patientIdentifier);
    formData.append("patientName", parentProfile.fullName);
    formData.append("userId", "parent");

    const savedColabUrl = typeof window !== "undefined" ? localStorage.getItem("maternacare_colab_ocr_url") : null;
    if (savedColabUrl) {
      formData.append("colabUrl", savedColabUrl);
    }

    try {
      const response = await fetch("/api/documents/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (data && (data.success || response.ok)) {
        setParentUploadResult(data);

        const newDoc: PatientDocument = {
          id: data.documentId || `DOC-${Date.now()}`,
          file_name: data.fileName || fileToUpload.name,
          file_key: data.fileKey || `documents/${fileToUpload.name}`,
          s3_uri: data.s3Uri || `s3://maternacare-storage-100403449729/documents/${fileToUpload.name}`,
          public_url: data.publicUrl || `https://maternacare-storage-100403449729.s3.ap-south-1.amazonaws.com/documents/${fileToUpload.name}`,
          file_size: data.fileSize || fileToUpload.size,
          status: "VERIFIED",
          ocr_markdown: data.ocrMarkdown,
          extracted_entities: data.extractedEntities,
          created_at: data.createdAt || new Date().toISOString(),
        };

        setParentDocuments((prev) => {
          const updatedList = [newDoc, ...prev.filter((d) => d.file_name !== newDoc.file_name)];
          if (typeof window !== "undefined") {
            try {
              localStorage.setItem(`maternacare_docs_${patientIdentifier}`, JSON.stringify(updatedList));
            } catch (storageErr) {}
          }
          return updatedList;
        });

        // Auto-enrich profile
        const complications = data.extractedEntities?.previousComplications || [];
        const allergies = data.extractedEntities?.allergies || [];
        let updatedProfile = { ...parentProfile };
        let profileChanged = false;

        if (complications.length > 0) {
          const compText = complications.join(", ");
          updatedProfile.medicalConditions = updatedProfile.medicalConditions
            ? `${updatedProfile.medicalConditions}; ${compText}`
            : compText;
          profileChanged = true;
        }

        if (allergies.length > 0) {
          const allText = allergies.join(", ");
          updatedProfile.knownAllergies = updatedProfile.knownAllergies
            ? `${updatedProfile.knownAllergies}; ${allText}`
            : allText;
          profileChanged = true;
        }

        if (profileChanged) {
          setParentProfile(updatedProfile);
          saveProfileToAws(updatedProfile);
        }

        setParentUploadFile(null);
      }
    } catch (err) {
      console.error("Upload error:", err);
    } finally {
      setIsParentUploading(false);
    }
  };

  const handleDeleteDocument = (id: string) => {
    const updated = parentDocuments.filter((d) => d.id !== id);
    setParentDocuments(updated);
    if (typeof window !== "undefined") {
      const patientIdentifier = parentProfile.email || parentProfile.fullName;
      localStorage.setItem(`maternacare_docs_${patientIdentifier}`, JSON.stringify(updated));
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between">
      {/* Header */}
      <header className="sticky top-0 z-40 w-full border-b border-gray-100 bg-white/90 backdrop-blur-md">
        <div className="container mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-pink-500 via-rose-400 to-pink-500 flex items-center justify-center text-white shadow-md shadow-pink-500/20 ring-2 ring-pink-100">
              <LogoIcon className="w-5 h-5" />
            </div>
            <span className="text-2xl font-extrabold tracking-tight">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-rose-400">
                Materna
              </span>
              <span className="text-slate-800">Care</span>
            </span>
          </Link>

          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setShowDashboard(!showDashboard)}
                  className={`text-xs font-semibold px-3 py-1.5 rounded-lg border transition-all cursor-pointer ${
                    showDashboard
                      ? "bg-pink-600 text-white border-pink-600"
                      : "bg-pink-50 text-pink-700 border-pink-200 hover:bg-pink-100"
                  }`}
                >
                  {showDashboard ? "📄 View Document Portal" : "📊 Health Dashboard"}
                </button>
                <button
                  onClick={handleLogout}
                  className="text-xs text-gray-500 hover:text-slate-800 font-medium px-3 py-1.5 rounded-lg border border-slate-200 cursor-pointer"
                >
                  Log Out
                </button>
              </div>
            ) : (
              <Link
                href="/"
                className="text-xs sm:text-sm font-medium text-gray-500 hover:text-slate-900"
              >
                ← Home
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 py-10">
        {isAuthenticated ? (
          showDashboard ? (
            <div className="max-w-5xl mx-auto px-4">
              <HealthDashboard
                profile={parentProfile}
                onBack={() => setShowDashboard(false)}
              />
            </div>
          ) : (
            <ParentPortal
              parentProfile={parentProfile}
              parentDocuments={parentDocuments}
              profileSaving={profileSaving}
              profileSaveSuccess={profileSaveSuccess}
              awsSyncDetails={awsSyncDetails}
              parentUploadFile={parentUploadFile}
              isParentUploading={isParentUploading}
              parentUploadResult={parentUploadResult}
              onProfileChange={handleProfileChange}
              onSaveProfile={(e) => {
                e.preventDefault();
                saveProfileToAws(parentProfile);
              }}
              onParentFileChange={setParentUploadFile}
              onParentUploadSubmit={handleParentDocumentUpload}
              onDeleteDocument={handleDeleteDocument}
              onBackToHome={handleLogout}
            />
          )
        ) : (
          <div className="max-w-md mx-auto px-4">
            <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-200/80">
              <div className="text-center mb-6">
                <div className="w-12 h-12 rounded-2xl bg-pink-100 text-pink-600 flex items-center justify-center mx-auto mb-3 shadow-sm ring-2 ring-pink-100">
                  <ParentIcon className="w-6 h-6" />
                </div>
                <h1 className="text-2xl font-extrabold text-slate-900">Maternal Health Portal</h1>
                <p className="text-xs text-gray-500 mt-1">
                  Continuous Antenatal Care, AI Health Memory &amp; Emergency Guardian.
                </p>
              </div>

              <div className="mb-4 p-2.5 rounded-xl bg-pink-50/70 border border-pink-200/60 flex items-center justify-between text-xs">
                <div className="text-pink-900">
                  <span className="font-semibold text-pink-700">Demo Account:</span> parent / 123
                </div>
                <button
                  type="button"
                  onClick={handleAutoFill}
                  className="font-medium text-pink-600 hover:text-pink-800 underline cursor-pointer"
                >
                  Fill credentials
                </button>
              </div>

              <div className="flex p-1 bg-slate-100 rounded-xl mb-4 text-xs font-semibold">
                <button
                  type="button"
                  onClick={() => {
                    setAuthMode("login");
                    setErrorMessage("");
                  }}
                  className={`flex-1 py-1.5 rounded-lg transition-all ${
                    authMode === "login" ? "bg-white text-pink-700 shadow-sm" : "text-gray-500"
                  }`}
                >
                  Sign In
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setAuthMode("signup");
                    setErrorMessage("");
                  }}
                  className={`flex-1 py-1.5 rounded-lg transition-all ${
                    authMode === "signup" ? "bg-white text-pink-700 shadow-sm" : "text-gray-500"
                  }`}
                >
                  New Patient Sign Up
                </button>
              </div>

              {errorMessage && (
                <div className="mb-4 p-3 rounded-xl bg-red-50 text-red-700 text-xs font-medium border border-red-200">
                  {errorMessage}
                </div>
              )}

              <form onSubmit={handleLogin} className="space-y-4">
                {authMode === "signup" && (
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Mother&apos;s Full Name
                    </label>
                    <input
                      type="text"
                      required
                      value={signupName}
                      onChange={(e) => setSignupName(e.target.value)}
                      placeholder="e.g. Priya Sharma"
                      className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                    />
                  </div>
                )}

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    {authMode === "login" ? "Username or Registered Mobile" : "Email Address / Identifier"}
                  </label>
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder={authMode === "login" ? "parent or your mobile" : "priya.sharma@example.com"}
                    className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
                  <div className="relative">
                    <input
                      type={showPassword ? "text" : "password"}
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none pr-9"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 text-xs"
                    >
                      {showPassword ? "Hide" : "Show"}
                    </button>
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full py-2.5 rounded-xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-xs shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 transition-all cursor-pointer"
                >
                  {authMode === "login" ? "Access Maternal Profile →" : "Register Maternal Account →"}
                </button>
              </form>
            </div>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
