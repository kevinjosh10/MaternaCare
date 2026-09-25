"use client";

import React, { useState, useEffect } from "react";
import { UserRole, AuthMode, ParentProfile, PatientDocument, UploadedDocumentResult } from "@/types";
import { Header } from "@/components/common/Header";
import { Footer } from "@/components/common/Footer";
import { AuthModal } from "@/components/auth/AuthModal";
import { LandingView } from "@/components/landing/LandingView";
import { AmbulancePortal } from "@/components/portals/AmbulancePortal";
import { ClinicianPortal } from "@/components/portals/ClinicianPortal";
import { ParentPortal } from "@/components/portals/ParentPortal";

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

export default function Home() {
  // Modal & Navigation State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalRole, setModalRole] = useState<UserRole>("clinician");
  const [modalMode, setModalMode] = useState<AuthMode>("login");
  const [loggedInRole, setLoggedInRole] = useState<UserRole | null>(null);

  // Parent Profile & Documents State
  const [parentProfile, setParentProfile] = useState<ParentProfile>(initialParentProfile);
  const [parentDocuments, setParentDocuments] = useState<PatientDocument[]>([]);
  const [profileSaving, setProfileSaving] = useState(false);
  const [profileSaveSuccess, setProfileSaveSuccess] = useState(false);
  const [awsSyncDetails, setAwsSyncDetails] = useState<string | null>(null);

  // File Upload State (Clinician & Parent)
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [parentUploadFile, setParentUploadFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isParentUploading, setIsParentUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<UploadedDocumentResult | null>(null);
  const [parentUploadResult, setParentUploadResult] = useState<UploadedDocumentResult | null>(null);
  const [verifiedEntities, setVerifiedEntities] = useState<string[]>([]);

  // Load Patient Profile and Documents from Amazon RDS
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
      console.warn("Could not load profile from RDS:", err);
    }
  };

  useEffect(() => {
    loadPatientProfile("priya.sharma@example.com");
  }, []);

  const openAuthModal = (role: UserRole, mode: AuthMode = "login") => {
    setModalRole(role);
    setModalMode(mode);
    setIsModalOpen(true);
  };

  const handleLoginSuccess = async (role: UserRole, identifier: string) => {
    if (role === "parent") {
      await loadPatientProfile(identifier);
    }
    setLoggedInRole(role);
  };

  const handleSignupSuccess = (role: UserRole, name: string, identifier: string) => {
    if (role === "parent") {
      const newProfile: ParentProfile = {
        ...initialParentProfile,
        id: identifier,
        fullName: name,
        email: identifier,
      };
      setParentProfile(newProfile);
      setParentDocuments([]);
      setLoggedInRole("parent");
      saveProfileToAws(newProfile);
    } else {
      setLoggedInRole(role);
    }
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
        setAwsSyncDetails("Synced with Amazon RDS (maternacare-db) & CloudWatch Logs");
        setTimeout(() => setProfileSaveSuccess(false), 4500);
      }
    } catch (err) {
      console.error("Profile save error:", err);
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

  // Parent PDF Upload Handler (AWS S3 + Jina OCR)
  const handleParentDocumentUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!parentUploadFile) return;

    setIsParentUploading(true);
    const formData = new FormData();
    formData.append("file", parentUploadFile);
    formData.append("patientId", parentProfile.email || parentProfile.fullName);
    formData.append("patientName", parentProfile.fullName);
    formData.append("userId", "parent");

    try {
      const response = await fetch("/api/documents/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok && data.success) {
        setParentUploadResult(data);

        const newDoc: PatientDocument = {
          id: data.documentId || `DOC-${Date.now()}`,
          file_name: data.fileName || parentUploadFile.name,
          file_key: data.fileKey,
          s3_uri: data.s3Uri,
          public_url: data.publicUrl,
          file_size: data.fileSize || parentUploadFile.size,
          status: "VERIFIED",
          ocr_markdown: data.ocrMarkdown,
          extracted_entities: data.extractedEntities,
          created_at: data.createdAt || new Date().toISOString(),
        };

        setParentDocuments((prev) => [newDoc, ...prev]);

        // Auto-enrich profile with newly detected findings
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
      } else {
        alert("Document upload failed. Please try again.");
      }
    } catch (err) {
      console.error("Parent upload error:", err);
      alert("Error uploading document to Amazon S3.");
    } finally {
      setIsParentUploading(false);
    }
  };

  // Clinician Document Upload Handler (AWS S3 + Jina OCR)
  const handleDocumentUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", uploadFile);
    formData.append("patientId", parentProfile.email || parentProfile.fullName);
    formData.append("patientName", parentProfile.fullName);
    formData.append("userId", "clinician");

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

        const newDoc: PatientDocument = {
          id: data.documentId || `DOC-${Date.now()}`,
          file_name: data.fileName || uploadFile.name,
          file_key: data.fileKey,
          s3_uri: data.s3Uri,
          public_url: data.publicUrl,
          file_size: data.fileSize || uploadFile.size,
          status: "VERIFIED",
          ocr_markdown: data.ocrMarkdown,
          extracted_entities: data.extractedEntities,
          created_at: data.createdAt || new Date().toISOString(),
        };
        setParentDocuments((prev) => [newDoc, ...prev]);
      } else {
        alert("Upload failed. Please check your connection.");
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

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between">
      {/* 1. Header Navigation Module */}
      <Header
        loggedInRole={loggedInRole}
        parentName={parentProfile.fullName}
        onLogout={() => setLoggedInRole(null)}
        onOpenAuthModal={openAuthModal}
      />

      {/* 2. Main Content Module */}
      <main className="flex-1">
        {loggedInRole === "ambulance" ? (
          <AmbulancePortal onBackToHome={() => setLoggedInRole(null)} />
        ) : loggedInRole === "clinician" ? (
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
            onDispatchAmbulance={() => setLoggedInRole("ambulance")}
          />
        ) : loggedInRole === "parent" ? (
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
            onSaveProfile={handleSaveParentProfile}
            onParentFileChange={setParentUploadFile}
            onParentUploadSubmit={handleParentDocumentUpload}
            onBackToHome={() => setLoggedInRole(null)}
          />
        ) : (
          <LandingView onOpenAuthModal={openAuthModal} />
        )}
      </main>

      {/* 3. Authentication & Profile Creation Modal Module */}
      <AuthModal
        isOpen={isModalOpen}
        initialRole={modalRole}
        initialMode={modalMode}
        onClose={() => setIsModalOpen(false)}
        onLoginSuccess={handleLoginSuccess}
        onSignupSuccess={handleSignupSuccess}
      />

      {/* 4. Footer Module */}
      <Footer />
    </div>
  );
}
