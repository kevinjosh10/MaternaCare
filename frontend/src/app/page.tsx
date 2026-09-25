"use client";

import React, { useState } from "react";

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

export default function Home() {
  // Modal & Portal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [userType, setUserType] = useState<"clinician" | "parent">("clinician");
  const [authMode, setAuthMode] = useState<"login" | "signup">("login");

  // Auth Inputs
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [signupName, setSignupName] = useState("");
  const [signupRole, setSignupRole] = useState("Frontline Health Worker");
  const [signupFacility, setSignupFacility] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  // Active Authenticated State
  const [loggedInRole, setLoggedInRole] = useState<"clinician" | "parent" | null>(null);

  // Parent Profile State
  const [parentProfile, setParentProfile] = useState<ParentProfile>(initialParentProfile);
  const [profileSaveSuccess, setProfileSaveSuccess] = useState(false);

  // Open modal helper
  const openAuthModal = (type: "clinician" | "parent", mode: "login" | "signup" = "login") => {
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
        setParentProfile((prev) => ({
          ...prev,
          fullName: signupName,
          email: `${username}@maternacare.org`,
        }));
        setLoggedInRole("parent");
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

  const handleSaveParentProfile = (e: React.FormEvent) => {
    e.preventDefault();
    setProfileSaveSuccess(true);
    setTimeout(() => setProfileSaveSuccess(false), 3500);
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
                {/* Mother and Child stylized heart / embrace */}
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

          <nav className="flex items-center gap-3 sm:gap-4">
            {loggedInRole === "parent" ? (
              <div className="flex items-center gap-3">
                <span className="text-xs font-semibold text-pink-700 bg-pink-50 px-3 py-1.5 rounded-full border border-pink-200">
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
                <span className="text-xs font-semibold text-slate-700 bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200">
                  Clinician: admin
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
                  className="text-sm font-medium text-pink-600 hover:text-pink-700 transition-colors px-2 py-1.5"
                >
                  Parent Portal
                </button>
                <button
                  onClick={() => openAuthModal("clinician", "login")}
                  className="text-sm font-medium text-gray-600 hover:text-slate-900 transition-colors px-2 py-1.5"
                >
                  Clinician Sign In
                </button>
                <button
                  onClick={() => openAuthModal("parent", "signup")}
                  className="rounded-full bg-gradient-to-r from-pink-500 to-rose-400 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:from-pink-600 hover:to-rose-500 transition-all"
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
        {/* If Parent is Logged In -> Render Parent Profile Dashboard */}
        {loggedInRole === "parent" ? (
          <section className="py-10 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
            {/* Header Banner */}
            <div className="bg-gradient-to-r from-pink-500 via-rose-400 to-pink-600 rounded-3xl p-6 sm:p-8 text-white shadow-lg shadow-pink-500/15 mb-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <span className="inline-block bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold mb-2">
                  Continuous Maternal &amp; Baby Journey
                </span>
                <h1 className="text-2xl sm:text-3xl font-extrabold">
                  Welcome, {parentProfile.fullName}
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
                    Keep your information up-to-date so clinical workers and emergency teams have your verified history.
                  </p>
                </div>
                {profileSaveSuccess && (
                  <div className="px-4 py-2 rounded-xl bg-green-50 border border-green-200 text-green-700 text-xs font-semibold flex items-center gap-2">
                    ✓ Profile successfully updated!
                  </div>
                )}
              </div>

              <form onSubmit={handleSaveParentProfile} className="space-y-8">
                {/* 1. Basic Personal Info */}
                <div>
                  <h3 className="text-sm font-bold text-pink-600 uppercase tracking-wider mb-4">
                    1. Personal Information
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
                    &larr; Back to Landing Page
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-3 rounded-full bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 transition-all"
                  >
                    Save Maternal Profile Changes
                  </button>
                </div>
              </form>
            </div>
          </section>
        ) : (
          /* Landing Page View */
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

                  {/* Call to Action Buttons */}
                  <div className="flex flex-wrap items-center justify-center gap-4">
                    <button
                      onClick={() => openAuthModal("parent", "login")}
                      className="rounded-full bg-gradient-to-r from-pink-500 to-rose-400 px-8 py-3.5 text-sm font-semibold text-white shadow-lg shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 transition-all"
                    >
                      Parent Portal &rarr;
                    </button>
                    <button
                      onClick={() => openAuthModal("clinician", "login")}
                      className="rounded-full bg-slate-900 px-8 py-3.5 text-sm font-semibold text-white shadow-md hover:bg-slate-800 transition-all"
                    >
                      Clinical Staff Login
                    </button>
                  </div>

                  {loggedInRole === "clinician" && (
                    <div className="mt-6 p-4 rounded-2xl bg-green-50 border border-green-200 text-green-800 text-xs font-semibold inline-block">
                      ✓ Logged in as Lead Clinician (admin) &bull; Ready for Patient Triage &amp; Document AI
                    </div>
                  )}
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

      {/* Interactive Auth Modal (Triggered by Button Clicks) */}
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

            {/* Portal Role Switcher */}
            <div className="flex bg-slate-100 p-1 rounded-2xl mb-4">
              <button
                type="button"
                onClick={() => {
                  setUserType("parent");
                  setErrorMessage("");
                }}
                className={`flex-1 py-2 text-xs sm:text-sm font-bold rounded-xl transition-all ${
                  userType === "parent"
                    ? "bg-white text-pink-600 shadow-sm"
                    : "text-slate-500 hover:text-slate-900"
                }`}
              >
                👶 Parent Portal
              </button>
              <button
                type="button"
                onClick={() => {
                  setUserType("clinician");
                  setErrorMessage("");
                }}
                className={`flex-1 py-2 text-xs sm:text-sm font-bold rounded-xl transition-all ${
                  userType === "clinician"
                    ? "bg-white text-slate-900 shadow-sm"
                    : "text-slate-500 hover:text-slate-900"
                }`}
              >
                🩺 Clinician Portal
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
                  : authMode === "login"
                  ? "Healthcare Staff Sign In"
                  : "Register Healthcare Staff"}
              </h2>
              <p className="text-xs text-gray-500 mt-1">
                {userType === "parent"
                  ? "Access your maternal journey and baby monitoring hub"
                  : "Access verified clinical decision support and referral center"}
              </p>
            </div>

            {/* Demo Quick Auto-Fill */}
            <div className="mb-4 p-2.5 rounded-xl bg-pink-50/70 border border-pink-200/60 flex items-center justify-between text-xs">
              <div className="text-pink-900">
                <span className="font-semibold text-pink-700">Demo Account:</span>{" "}
                {userType === "clinician" ? "admin / 123" : "parent / 123"}
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
                      {userType === "parent" ? "Mother / Parent Full Name" : "Clinician Full Name"}
                    </label>
                    <input
                      type="text"
                      required
                      value={signupName}
                      onChange={(e) => setSignupName(e.target.value)}
                      placeholder={userType === "parent" ? "e.g. Priya Sharma" : "e.g. Dr. Ananya Sen"}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                    />
                  </div>

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
                  {userType === "parent" ? "Username or Mobile Number" : "Username / Clinician ID"}
                </label>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder={userType === "parent" ? "e.g. parent" : "e.g. admin"}
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
                className="w-full mt-2 py-3 px-4 rounded-xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 transition-all"
              >
                {authMode === "login"
                  ? userType === "parent"
                    ? "Open Parent Portal &rarr;"
                    : "Sign In as Clinician &rarr;"
                  : "Create & Access Account"}
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
