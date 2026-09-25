import React from "react";
import Link from "next/link";
import { UserRole } from "@/types";
import { ParentIcon, ClinicianIcon, AmbulanceIcon, LogoIcon } from "@/components/icons/PortalIcons";

interface HeaderProps {
  loggedInRole: UserRole | null;
  parentName: string;
  onLogout: () => void;
  onOpenAuthModal?: (role: UserRole, mode?: "login" | "signup") => void;
}

export function Header({
  loggedInRole,
  parentName,
  onLogout,
}: HeaderProps) {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-gray-100 bg-white/90 backdrop-blur-md">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2.5">
          {/* MaternaCare Logo Icon */}
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

        <nav className="flex items-center gap-2 sm:gap-3">
          {loggedInRole === "parent" ? (
            <div className="flex items-center gap-3">
              <span className="text-xs font-semibold text-pink-700 bg-pink-50 px-3 py-1.5 rounded-full border border-pink-200 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                <ParentIcon className="w-3.5 h-3.5 text-pink-600" />
                Parent: {parentName}
              </span>
              <button
                onClick={onLogout}
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
                onClick={onLogout}
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
                onClick={onLogout}
                className="text-xs text-gray-500 hover:text-slate-800 font-medium px-2 py-1"
              >
                Log Out
              </button>
            </div>
          ) : (
            <>
              <Link
                href="/parent"
                className="text-xs sm:text-sm font-medium text-pink-600 hover:text-pink-700 transition-colors px-2 py-1.5 flex items-center gap-1"
              >
                <ParentIcon className="w-3.5 h-3.5 text-pink-500" />
                <span>Parent Portal</span>
              </Link>
              <Link
                href="/clinician"
                className="text-xs sm:text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors px-2 py-1.5 flex items-center gap-1"
              >
                <ClinicianIcon className="w-3.5 h-3.5 text-slate-500" />
                <span>Clinician</span>
              </Link>
              <Link
                href="/ambulance"
                className="text-xs sm:text-sm font-semibold text-red-600 hover:text-red-700 bg-red-50 hover:bg-red-100 border border-red-200 px-2.5 py-1.5 rounded-full transition-all flex items-center gap-1.5"
              >
                <AmbulanceIcon className="w-3.5 h-3.5 text-red-600" />
                <span>Ambulance / Hospital</span>
              </Link>
              <Link
                href="/parent"
                className="rounded-full bg-gradient-to-r from-pink-500 to-rose-400 px-3.5 py-1.5 sm:px-4 sm:py-2 text-xs sm:text-sm font-semibold text-white shadow-sm hover:from-pink-600 hover:to-rose-500 transition-all"
              >
                Sign Up
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
