import React, { useState } from "react";
import { UserRole, AuthMode, ParentProfile } from "@/types";
import { ParentIcon, ClinicianIcon, AmbulanceIcon } from "@/components/icons/PortalIcons";

interface AuthModalProps {
  isOpen: boolean;
  initialRole: UserRole;
  initialMode: AuthMode;
  onClose: () => void;
  onLoginSuccess: (role: UserRole, identifier: string) => void;
  onSignupSuccess: (role: UserRole, name: string, identifier: string) => void;
}

export function AuthModal({
  isOpen,
  initialRole,
  initialMode,
  onClose,
  onLoginSuccess,
  onSignupSuccess,
}: AuthModalProps) {
  const [userType, setUserType] = useState<UserRole>(initialRole);
  const [authMode, setAuthMode] = useState<AuthMode>(initialMode);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [signupName, setSignupName] = useState("");
  const [signupRole, setSignupRole] = useState("Emergency EMT Lead");
  const [signupFacility, setSignupFacility] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  if (!isOpen) return null;

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

  const handleAuthSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    if (authMode === "login") {
      if (userType === "clinician") {
        if (username.trim() === "admin" && password === "123") {
          onLoginSuccess("clinician", "admin");
          onClose();
        } else {
          setErrorMessage("Invalid credentials. For Clinician demo use: admin / 123");
        }
      } else if (userType === "ambulance") {
        if (
          (username.trim() === "ambulance" && password === "123") ||
          (username.trim() === "hospital" && password === "123") ||
          (username.trim() === "admin" && password === "123")
        ) {
          onLoginSuccess("ambulance", "ambulance");
          onClose();
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
          const lookupId = username.trim() === "parent" ? "priya.sharma@example.com" : username.trim();
          onLoginSuccess("parent", lookupId);
          onClose();
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
        const userEmail = username.includes("@") ? username.trim() : `${username.trim()}@maternacare.org`;
        onSignupSuccess("parent", signupName, userEmail);
        onClose();
      } else if (userType === "ambulance") {
        onSignupSuccess("ambulance", signupName, username);
        onClose();
      } else {
        setSuccessMessage(`Account created for ${signupName}. Please log in with admin / 123.`);
        setAuthMode("login");
      }
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
      <div className="w-full max-w-md bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border border-gray-100 relative animate-in fade-in zoom-in-95 duration-200">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 text-gray-400 hover:text-gray-600 p-1.5 rounded-full hover:bg-gray-100 transition-colors"
        >
          ✕
        </button>

        {/* Modal Portal Selector */}
        <div className="flex p-1 bg-slate-100 rounded-2xl mb-6">
          <button
            type="button"
            onClick={() => {
              setUserType("parent");
              setErrorMessage("");
            }}
            className={`flex-1 py-2 rounded-xl text-xs font-semibold transition-all flex items-center justify-center gap-1.5 ${
              userType === "parent"
                ? "bg-white text-pink-600 shadow-sm"
                : "text-gray-500 hover:text-gray-900"
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
            className={`flex-1 py-2 rounded-xl text-xs font-semibold transition-all flex items-center justify-center gap-1.5 ${
              userType === "clinician"
                ? "bg-white text-slate-900 shadow-sm"
                : "text-gray-500 hover:text-gray-900"
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
            className={`flex-1 py-2 rounded-xl text-xs font-semibold transition-all flex items-center justify-center gap-1.5 ${
              userType === "ambulance"
                ? "bg-white text-red-600 shadow-sm"
                : "text-gray-500 hover:text-gray-900"
            }`}
          >
            <AmbulanceIcon className="w-3.5 h-3.5" />
            <span>Ambulance</span>
          </button>
        </div>

        {/* Modal Title */}
        <div className="text-center mb-5">
          <h3 className="text-xl font-bold text-slate-900">
            {authMode === "login"
              ? userType === "parent"
                ? "Parent / Mother Portal"
                : userType === "ambulance"
                ? "Ambulance & Hospital Dispatch"
                : "Clinician Triage Hub"
              : userType === "parent"
              ? "Create Maternal Profile"
              : "Register Clinician Account"}
          </h3>
          <p className="text-xs text-gray-500 mt-1">
            {authMode === "login"
              ? "Sign in to access your continuous health record on AWS."
              : "Register your profile and store on Amazon RDS & S3."}
          </p>
        </div>

        {/* Mode Switcher */}
        <div className="flex justify-center gap-4 text-xs font-semibold mb-4 border-b border-gray-100 pb-3">
          <button
            type="button"
            onClick={() => {
              setAuthMode("login");
              setErrorMessage("");
              setSuccessMessage("");
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
              setSuccessMessage("");
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

        {/* Quick Auto-fill for Demonstration */}
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
                ? "Email or Mobile Number"
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
                  ? "e.g. parent or priya.sharma@example.com"
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
                : "Create & Access Maternal Profile →"}
            </span>
          </button>
        </form>
      </div>
    </div>
  );
}
