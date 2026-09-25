"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Footer } from "@/components/common/Footer";
import { AmbulancePortal } from "@/components/portals/AmbulancePortal";
import { AmbulanceIcon, LogoIcon } from "@/components/icons/PortalIcons";

export default function AmbulancePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");

    if (
      (username.trim() === "ambulance" && password === "123") ||
      (username.trim() === "hospital" && password === "123") ||
      (username.trim() === "admin" && password === "123")
    ) {
      setIsAuthenticated(true);
    } else {
      setErrorMessage("Invalid credentials. For Ambulance & Hospital demo use: ambulance / 123");
    }
  };

  const handleAutoFill = () => {
    setUsername("ambulance");
    setPassword("123");
    setErrorMessage("");
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
          <AmbulancePortal onBackToHome={() => setIsAuthenticated(false)} />
        ) : (
          <div className="max-w-md mx-auto px-4">
            <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-xl border border-red-100">
              {/* Card Header */}
              <div className="text-center mb-6">
                <div className="w-12 h-12 rounded-2xl bg-red-600 text-white flex items-center justify-center mx-auto mb-3 shadow-md shadow-red-500/20">
                  <AmbulanceIcon className="w-6 h-6" />
                </div>
                <h1 className="text-2xl font-extrabold text-slate-900">Ambulance &amp; Hospital Hub</h1>
                <p className="text-xs text-gray-500 mt-1">
                  108 Emergency Dispatch, Pre-Arrival Triage &amp; Bed Readiness.
                </p>
              </div>

              {/* Quick Auto-fill */}
              <div className="mb-4 p-2.5 rounded-xl bg-red-50/70 border border-red-200/60 flex items-center justify-between text-xs">
                <div className="text-red-900">
                  <span className="font-semibold text-red-700">Demo Account:</span> ambulance / 123
                </div>
                <button
                  type="button"
                  onClick={handleAutoFill}
                  className="font-medium text-red-600 hover:text-red-800 underline"
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
                    Ambulance Unit ID / Hospital ID
                  </label>
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="e.g. ambulance or ALS-Unit-108"
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-red-500/20 focus:border-red-500 outline-none"
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="block text-xs font-semibold text-slate-700">Password</label>
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="text-[11px] text-red-600 hover:text-red-700 font-medium"
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
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-red-500/20 focus:border-red-500 outline-none"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full py-3 px-4 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-sm shadow-md shadow-red-500/20 transition-all"
                >
                  Access Dispatch &amp; Hospital Hub →
                </button>
              </form>

              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-gray-500">
                <Link href="/parent" className="hover:text-pink-600">
                  Parent / Mother Portal →
                </Link>
                <Link href="/clinician" className="hover:text-slate-800">
                  Clinician Triage →
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
