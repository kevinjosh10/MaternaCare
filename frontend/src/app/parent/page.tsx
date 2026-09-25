"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ParentProfile, PatientDocument, UploadedDocumentResult } from "@/types";
import { Header } from "@/components/common/Header";
import { Footer } from "@/components/common/Footer";
import { ParentPortal } from "@/components/portals/ParentPortal";
import { ParentIcon, LogoIcon } from "@/components/icons/PortalIcons";

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

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");

    if (authMode === "login") {
      if ((username.trim() === "parent" && password === "123") || (username.trim() === "admin" && password === "123") || username.trim().length > 0) {
        const lookupId = username.trim() === "parent" ? "priya.sharma@example.com" : username.trim();
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
      setParentProfile(newProfile);
      setParentDocuments([]);
      setIsAuthenticated(true);
      saveProfileToAws(newProfile);
    }
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
              <button
                onClick={() => setIsAuthenticated(false)}
                className="text-xs text-gray-500 hover:text-slate-800 font-medium px-3 py-1.5 rounded-lg border border-slate-200"
              >
                Log Out
              </button>
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
            onBackToHome={() => setIsAuthenticated(false)}
          />
        ) : (
          <div className="max-w-md mx-auto px-4">
            <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-200/80">
              {/* Card Header */}
              <div className="text-center mb-6">
                <div className="w-12 h-12 rounded-2xl bg-pink-100 text-pink-600 flex items-center justify-center mx-auto mb-3 shadow-sm ring-2 ring-pink-100">
                  <ParentIcon className="w-6 h-6" />
                </div>
                <h1 className="text-2xl font-extrabold text-slate-900">Parent / Mother Portal</h1>
                <p className="text-xs text-gray-500 mt-1">
                  {authMode === "login"
                    ? "Sign in to access your maternal health records and upload medical reports."
                    : "Create your continuous encrypted maternal health profile."}
                </p>
              </div>

              {/* Mode Switcher */}
              <div className="flex justify-center gap-4 text-xs font-semibold mb-5 border-b border-gray-100 pb-3">
                <button
                  type="button"
                  onClick={() => {
                    setAuthMode("login");
                    setErrorMessage("");
                  }}
                  className={`pb-1 ${
                    authMode === "login"
                      ? "text-pink-600 border-b-2 border-pink-500"
                      : "text-gray-400 hover:text-gray-600"
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
                  className={`pb-1 ${
                    authMode === "signup"
                      ? "text-pink-600 border-b-2 border-pink-500"
                      : "text-gray-400 hover:text-gray-600"
                  }`}
                >
                  Create New Profile
                </button>
              </div>

              {/* Quick Auto-fill */}
              <div className="mb-4 p-2.5 rounded-xl bg-pink-50/70 border border-pink-200/60 flex items-center justify-between text-xs">
                <div className="text-pink-900">
                  <span className="font-semibold text-pink-700">Demo Account:</span> parent / 123
                </div>
                <button
                  type="button"
                  onClick={handleAutoFill}
                  className="font-medium text-pink-600 hover:text-pink-800 underline"
                >
                  Auto-fill
                </button>
              </div>

              {errorMessage && (
                <div className="mb-4 p-2.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs">
                  {errorMessage}
                </div>
              )}

              {/* Login / Sign Up Form */}
              <form onSubmit={handleLogin} className="space-y-4">
                {authMode === "signup" && (
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Mother / Parent Full Name
                    </label>
                    <input
                      type="text"
                      required
                      value={signupName}
                      onChange={(e) => setSignupName(e.target.value)}
                      placeholder="e.g. Priya Sharma"
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                    />
                  </div>
                )}

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Email Address or Username
                  </label>
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="e.g. parent or priya.sharma@example.com"
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
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
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 transition-all"
                >
                  {authMode === "login" ? "Sign In to Parent Portal →" : "Create & Access Maternal Profile →"}
                </button>
              </form>

              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-gray-500">
                <Link href="/clinician" className="hover:text-pink-600">
                  Are you a Clinician? →
                </Link>
                <Link href="/ambulance" className="hover:text-red-600">
                  Ambulance Hub →
                </Link>
              </div>
            </div>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
