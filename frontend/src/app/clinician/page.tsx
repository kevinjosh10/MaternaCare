"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ParentProfile, PatientDocument, UploadedDocumentResult } from "@/types";
import { Footer } from "@/components/common/Footer";
import { ClinicianPortal } from "@/components/portals/ClinicianPortal";
import { ClinicianIcon, LogoIcon } from "@/components/icons/PortalIcons";

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

export default function ClinicianPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  // Patient & Clinical State
  const [parentProfile, setParentProfile] = useState<ParentProfile>(initialParentProfile);
  const [parentDocuments, setParentDocuments] = useState<PatientDocument[]>([]);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<UploadedDocumentResult | null>(null);
  const [verifiedEntities, setVerifiedEntities] = useState<string[]>([]);

  const loadPatientProfile = async (identifier: string) => {
    try {
      const res = await fetch(`/api/patients/profile?id=${encodeURIComponent(identifier)}`);
      if (res.ok) {
        const data = await res.json();
        if (data.success && data.profile) {
          setParentProfile(data.profile);
          if (data.documents && Array.isArray(data.documents)) {
            setParentDocuments(data.documents);
          }
        }
      }
    } catch (err) {
      console.warn("RDS load note:", err);
    }
  };

  // Restore clinician auth from localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      const isAuth = localStorage.getItem("maternacare_clinician_auth") === "true" || localStorage.getItem("maternacare_auth_role") === "clinician";
      if (isAuth) {
        setIsAuthenticated(true);
      }
    }
    loadPatientProfile("priya.sharma@example.com");
  }, []);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");

    if ((username.trim() === "admin" && password === "123") || username.trim().length > 0) {
      if (typeof window !== "undefined") {
        localStorage.setItem("maternacare_clinician_auth", "true");
        localStorage.setItem("maternacare_auth_role", "clinician");
        localStorage.setItem("maternacare_auth_identifier", "admin");
      }
      setIsAuthenticated(true);
    } else {
      setErrorMessage("Invalid credentials. For Clinician demo use: admin / 123");
    }
  };

  const handleLogout = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("maternacare_clinician_auth");
      localStorage.removeItem("maternacare_auth_role");
      localStorage.removeItem("maternacare_auth_identifier");
    }
    setIsAuthenticated(false);
  };

  const handleAutoFill = () => {
    setUsername("admin");
    setPassword("123");
    setErrorMessage("");
  };

  const handleDocumentUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return;

    setIsUploading(true);
    const fileToUpload = uploadFile;
    const patientIdentifier = parentProfile.email || parentProfile.fullName;

    const formData = new FormData();
    formData.append("file", fileToUpload);
    formData.append("patientId", patientIdentifier);
    formData.append("patientName", parentProfile.fullName);
    formData.append("userId", "clinician");

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

        setParentDocuments((prev) => [newDoc, ...prev.filter((d) => d.file_name !== newDoc.file_name)]);
      }
    } catch (err) {
      console.error("Upload error:", err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleCommitVerifiedHistory = async () => {
    const updatedConditions = verifiedEntities.join(", ");
    const updated = {
      ...parentProfile,
      medicalConditions: parentProfile.medicalConditions
        ? `${parentProfile.medicalConditions}; ${updatedConditions}`
        : updatedConditions,
    };
    setParentProfile(updated);

    try {
      await fetch("/api/patients/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated),
      });
    } catch (e) {}

    alert("Verified history committed to trusted Maternal Health Profile!");
    setUploadResult(null);
    setUploadFile(null);
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
                onClick={handleLogout}
                className="text-xs text-gray-500 hover:text-slate-800 font-medium px-3 py-1.5 rounded-lg border border-slate-200 cursor-pointer"
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
          <ClinicianPortal
            parentProfile={parentProfile}
            parentDocuments={parentDocuments}
            uploadFile={uploadFile}
            isUploading={isUploading}
            uploadResult={uploadResult}
            verifiedEntities={verifiedEntities}
            onFileChange={setUploadFile}
            onUploadSubmit={handleDocumentUpload}
            onCommitVerifiedHistory={handleCommitVerifiedHistory}
            onDispatchAmbulance={() => (window.location.href = "/ambulance")}
          />
        ) : (
          <div className="max-w-md mx-auto px-4">
            <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-200/80">
              {/* Card Header */}
              <div className="text-center mb-6">
                <div className="w-12 h-12 rounded-2xl bg-slate-900 text-blue-400 flex items-center justify-center mx-auto mb-3 shadow-md">
                  <ClinicianIcon className="w-6 h-6" />
                </div>
                <h1 className="text-2xl font-extrabold text-slate-900">Clinician Triage Hub</h1>
                <p className="text-xs text-gray-500 mt-1">
                  Access patient longitudinal risk trajectories and intelligent clinical records.
                </p>
              </div>

              {/* Quick Auto-fill */}
              <div className="mb-4 p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                <div className="text-slate-700">
                  <span className="font-semibold text-slate-900">Demo Account:</span> admin / 123
                </div>
                <button
                  type="button"
                  onClick={handleAutoFill}
                  className="font-medium text-blue-600 hover:text-blue-800 underline"
                >
                  Auto-fill
                </button>
              </div>

              {errorMessage && (
                <div className="mb-4 p-2.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs">
                  {errorMessage}
                </div>
              )}

              {/* Login Form */}
              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Clinician Username or ID
                  </label>
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="e.g. admin"
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 outline-none"
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="block text-xs font-semibold text-slate-700">Password</label>
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="text-[11px] text-slate-600 hover:text-slate-800 font-medium"
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
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 outline-none"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full py-3 px-4 rounded-xl bg-slate-900 text-white font-bold text-sm shadow-md hover:bg-slate-800 transition-all"
                >
                  Sign In to Clinician Triage →
                </button>
              </form>

              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-gray-500">
                <Link href="/parent" className="hover:text-pink-600">
                  Mother / Parent Portal →
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
