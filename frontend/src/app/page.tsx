"use client";

import React, { useState } from "react";

export default function Home() {
  const [authMode, setAuthMode] = useState<"login" | "signup">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [facilityName, setFacilityName] = useState("");
  const [role, setRole] = useState("frontline");
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    if (username.trim() === "admin" && password === "123") {
      setSuccessMessage("Login successful! Welcome back to MaternaCare Portal.");
      setIsLoggedIn(true);
    } else {
      setErrorMessage("Invalid credentials. Please use username: admin and password: 123");
    }
  };

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    if (!username.trim() || !password.trim() || !fullName.trim()) {
      setErrorMessage("Please fill out all required fields.");
      return;
    }

    setSuccessMessage(`Account created for ${fullName}! You can now sign in with admin / 123.`);
    setAuthMode("login");
  };

  const fillDemoCredentials = () => {
    setUsername("admin");
    setPassword("123");
    setErrorMessage("");
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between">
      {/* Navigation */}
      <header className="sticky top-0 z-50 w-full border-b border-gray-100 bg-white/85 backdrop-blur-md">
        <div className="container mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold tracking-tight">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-rose-400">
                Materna
              </span>
              <span className="text-slate-800">Care</span>
            </span>
          </div>
          <nav className="hidden md:flex gap-6 items-center">
            <a
              href="#auth-section"
              className="text-sm font-medium text-gray-600 hover:text-pink-500 transition-colors"
            >
              Sign In
            </a>
            <a
              href="#features"
              className="text-sm font-medium text-gray-600 hover:text-pink-500 transition-colors"
            >
              Features
            </a>
            <a
              href="#workflow"
              className="text-sm font-medium text-gray-600 hover:text-pink-500 transition-colors"
            >
              Clinical Workflow
            </a>
            <a
              href="#auth-section"
              className="rounded-full bg-slate-900 px-5 py-2 text-sm font-medium text-white shadow-sm hover:bg-slate-800 transition-all"
            >
              Access Portal
            </a>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden bg-white pt-16 pb-12 sm:pt-24 sm:pb-16 border-b border-slate-100">
          <div className="absolute inset-x-0 top-0 h-[32rem] flex-none bg-gradient-to-b from-pink-50 via-rose-50/30 to-white"></div>
          <div className="relative container mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="max-w-3xl mx-auto">
              <span className="inline-flex items-center rounded-full bg-pink-100 px-3.5 py-1 text-xs font-semibold text-pink-700 ring-1 ring-inset ring-pink-600/10 mb-6">
                HT-06: Maternal &amp; Neonatal Referral Intelligence
              </span>
              <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-6xl mb-6 leading-tight">
                Continuous Care for{" "}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-rose-400">
                  Mother &amp; Baby
                </span>
              </h1>
              <p className="text-base sm:text-lg leading-relaxed text-gray-600 max-w-2xl mx-auto">
                An AI-assisted continuity platform connecting verified medical history,
                longitudinal trends, and emergency referral intelligence into one unbroken health journey.
              </p>
            </div>
          </div>
        </section>

        {/* Auth Section (Centered Directly Under Hero) */}
        <section id="auth-section" className="py-12 px-4 sm:px-6 lg:px-8 -mt-8 relative z-10">
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-3xl shadow-xl shadow-pink-100/50 border border-pink-100/80 p-6 sm:p-8 backdrop-blur-sm">
              {/* Tab Header */}
              <div className="flex bg-slate-100 p-1 rounded-2xl mb-6">
                <button
                  type="button"
                  onClick={() => {
                    setAuthMode("login");
                    setErrorMessage("");
                    setSuccessMessage("");
                  }}
                  className={`flex-1 py-2 text-sm font-semibold rounded-xl transition-all ${
                    authMode === "login"
                      ? "bg-white text-slate-900 shadow-sm"
                      : "text-slate-500 hover:text-slate-900"
                  }`}
                >
                  Log In
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setAuthMode("signup");
                    setErrorMessage("");
                    setSuccessMessage("");
                  }}
                  className={`flex-1 py-2 text-sm font-semibold rounded-xl transition-all ${
                    authMode === "signup"
                      ? "bg-white text-slate-900 shadow-sm"
                      : "text-slate-500 hover:text-slate-900"
                  }`}
                >
                  Sign Up
                </button>
              </div>

              {/* Title & Badge */}
              <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-slate-900">
                  {authMode === "login" ? "Welcome Back" : "Create Account"}
                </h2>
                <p className="text-xs text-gray-500 mt-1">
                  {authMode === "login"
                    ? "Enter your authorized healthcare credentials"
                    : "Register as a healthcare provider or referral facility"}
                </p>
              </div>

              {/* Demo Hint Banner */}
              <div className="mb-5 p-3 rounded-2xl bg-pink-50 border border-pink-200/70 flex items-center justify-between text-xs">
                <div className="text-pink-900">
                  <span className="font-semibold text-pink-700">Demo Access:</span> admin / 123
                </div>
                <button
                  type="button"
                  onClick={fillDemoCredentials}
                  className="font-medium text-pink-600 hover:text-pink-800 underline transition-colors"
                >
                  Auto-fill
                </button>
              </div>

              {/* Status Notifications */}
              {errorMessage && (
                <div className="mb-5 p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
                  <svg
                    className="w-4 h-4 shrink-0 text-red-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <span>{errorMessage}</span>
                </div>
              )}

              {successMessage && (
                <div className="mb-5 p-3 rounded-xl bg-green-50 border border-green-200 text-green-700 text-xs flex items-center gap-2">
                  <svg
                    className="w-4 h-4 shrink-0 text-green-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <span>{successMessage}</span>
                </div>
              )}

              {isLoggedIn ? (
                <div className="text-center py-4 space-y-4">
                  <div className="w-16 h-16 bg-pink-100 text-pink-600 rounded-full flex items-center justify-center mx-auto text-2xl font-bold">
                    ✓
                  </div>
                  <h3 className="text-lg font-bold text-slate-800">Healthcare Worker Verified</h3>
                  <p className="text-xs text-gray-500">
                    Logged in as <span className="font-semibold text-slate-700">admin</span> (Lead Clinician)
                  </p>
                  <div className="pt-2 flex flex-col gap-2">
                    <button
                      type="button"
                      onClick={() => alert("Redirecting to Patient Triage Dashboard...")}
                      className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-semibold text-sm shadow-md hover:from-pink-600 hover:to-rose-500 transition-all"
                    >
                      Enter Triage Dashboard &rarr;
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setIsLoggedIn(false);
                        setSuccessMessage("");
                      }}
                      className="text-xs text-gray-500 hover:text-gray-700 py-1"
                    >
                      Sign Out
                    </button>
                  </div>
                </div>
              ) : authMode === "login" ? (
                /* Login Form */
                <form onSubmit={handleLogin} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Username / ID
                    </label>
                    <input
                      type="text"
                      required
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      placeholder="e.g. admin"
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500/30 focus:border-pink-500 transition-all"
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
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500/30 focus:border-pink-500 transition-all"
                    />
                  </div>

                  <div className="flex items-center justify-between text-xs text-gray-500 pt-1">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        defaultChecked
                        className="rounded border-gray-300 text-pink-500 focus:ring-pink-400"
                      />
                      <span>Remember facility</span>
                    </label>
                    <a href="#auth-section" className="text-pink-600 hover:underline">
                      Need help?
                    </a>
                  </div>

                  <button
                    type="submit"
                    className="w-full mt-2 py-3 px-4 rounded-xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-semibold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 focus:outline-none focus:ring-2 focus:ring-pink-500/40 transition-all"
                  >
                    Sign In to Portal
                  </button>
                </form>
              ) : (
                /* Signup Form */
                <form onSubmit={handleSignup} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Full Name
                    </label>
                    <input
                      type="text"
                      required
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      placeholder="Dr. Sarah Johnson"
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500/30 focus:border-pink-500 transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Clinical Role
                    </label>
                    <select
                      value={role}
                      onChange={(e) => setRole(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500/30 focus:border-pink-500 bg-white transition-all"
                    >
                      <option value="frontline">Frontline Healthcare Worker / ASHA / ANM</option>
                      <option value="clinician">Obstetrician / Medical Officer</option>
                      <option value="referral">Referral Facility Specialist</option>
                      <option value="admin">Hospital Administrator</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Facility / Health Center Name
                    </label>
                    <input
                      type="text"
                      value={facilityName}
                      onChange={(e) => setFacilityName(e.target.value)}
                      placeholder="Community Health Centre (CHC) North"
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500/30 focus:border-pink-500 transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Username
                    </label>
                    <input
                      type="text"
                      required
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      placeholder="Choose a username"
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500/30 focus:border-pink-500 transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Password
                    </label>
                    <input
                      type="password"
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Choose a secure password"
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500/30 focus:border-pink-500 transition-all"
                    />
                  </div>

                  <button
                    type="submit"
                    className="w-full mt-2 py-3 px-4 rounded-xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-semibold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 focus:outline-none focus:ring-2 focus:ring-pink-500/40 transition-all"
                  >
                    Register Provider Account
                  </button>
                </form>
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
                Most systems evaluate risk as an isolated event. MaternaCare integrates medical history, current vitals, and referral workflows into an unbroken continuum.
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
                  <p className="mt-2 text-base leading-relaxed text-gray-600">
                    Extends the journey to neonatal monitoring and tracks pattern-changes in the baby&apos;s first year.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200/80 py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-gray-500">
          <p>&copy; {new Date().getFullYear()} MaternaCare — AI-Powered Maternal &amp; Neonatal Referral Intelligence (HT-06).</p>
        </div>
      </footer>
    </div>
  );
}
