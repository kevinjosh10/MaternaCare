import React from "react";
import Link from "next/link";
import { UserRole } from "@/types";
import { ParentIcon, ClinicianIcon, AmbulanceIcon, LogoIcon } from "@/components/icons/PortalIcons";

interface LandingViewProps {
  onOpenAuthModal?: (role: UserRole, mode?: "login" | "signup") => void;
}

export function LandingView({ onOpenAuthModal }: LandingViewProps) {
  return (
    <>
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-white pt-16 pb-20 sm:pt-24 sm:pb-28 border-b border-slate-100">
        <div className="absolute inset-x-0 top-0 h-[38rem] flex-none bg-gradient-to-b from-pink-50 via-rose-50/30 to-white"></div>
        <div className="relative container mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="max-w-4xl mx-auto">
            {/* MaternaCare Brand Logo Pill in Hero - Prominent & Big */}
            <div className="inline-flex items-center gap-3.5 sm:gap-4 px-5 sm:px-7 py-2.5 sm:py-3.5 rounded-full bg-white/95 shadow-xl shadow-pink-500/10 border border-pink-200/80 ring-2 ring-pink-500/20 mb-8 backdrop-blur-md hover:scale-[1.02] transition-transform">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-2xl bg-gradient-to-tr from-pink-500 via-rose-400 to-pink-500 flex items-center justify-center text-white shadow-md shadow-pink-500/30 ring-2 ring-pink-100">
                <LogoIcon className="w-6 h-6 sm:w-7 sm:h-7" />
              </div>
              <div className="flex flex-wrap items-center text-left">
                <span className="text-lg sm:text-2xl font-black tracking-tight">
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 via-rose-400 to-pink-600">
                    Materna
                  </span>
                  <span className="text-slate-800">Care</span>
                </span>
                <span className="hidden sm:inline-block mx-3 text-pink-300 font-light text-xl">|</span>
                <span className="text-xs sm:text-sm font-bold text-pink-900/80 tracking-wide uppercase block sm:inline">
                  Maternal &amp; Neonatal Intelligence
                </span>
              </div>
            </div>

            <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-6xl lg:text-7xl mb-6 leading-tight">
              Continuous Care for
              <span className="block mt-0.5 sm:mt-1 pb-1 flowing-gradient-text font-black tracking-tight">
                Mother &amp; Baby
              </span>
            </h1>
            <p className="text-base sm:text-lg leading-relaxed text-gray-600 max-w-2xl mx-auto mb-8">
              An AI-assisted platform connecting verified maternal history, longitudinal trends,
              and emergency referral intelligence into one unbroken health journey.
            </p>

            {/* 3 Call to Action Buttons with Direct Routes */}
            <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-4">
              <Link
                href="/parent"
                className="rounded-full bg-gradient-to-r from-pink-500 to-rose-400 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 hover:scale-105 transition-all flex items-center gap-2"
              >
                <ParentIcon className="w-4 h-4 text-white" />
                <span>Parent Portal →</span>
              </Link>
              <Link
                href="/clinician"
                className="rounded-full bg-slate-900 px-6 py-3.5 text-sm font-semibold text-white shadow-md hover:bg-slate-800 hover:scale-105 transition-all flex items-center gap-2"
              >
                <ClinicianIcon className="w-4 h-4 text-slate-300" />
                <span>Clinician Triage</span>
              </Link>
              <Link
                href="/ambulance"
                className="rounded-full bg-red-600 hover:bg-red-700 px-6 py-3.5 text-sm font-semibold text-white shadow-md shadow-red-500/20 hover:scale-105 transition-all flex items-center gap-2"
              >
                <AmbulanceIcon className="w-4 h-4 text-white" />
                <span>Ambulance / Hospital</span>
              </Link>
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
                  Extracts and verifies previous medical history from unstructured records using Intelligent Medical AI Scanning.
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
                <h3 className="text-lg font-bold text-slate-900">COMMUNICATE</h3>
                <p className="mt-2 text-sm leading-relaxed text-gray-600">
                  Produces instant, auditable clinical handovers with pre-arrival checklists for emergency triage.
                </p>
              </div>
              {/* Pillar 5 */}
              <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-lg">
                  5
                </div>
                <h3 className="text-lg font-bold text-slate-900">ACT</h3>
                <p className="mt-2 text-sm leading-relaxed text-gray-600">
                  Ambulance and hospital routing intelligence with real-time pre-arrival readiness checklists.
                </p>
              </div>
              {/* Pillar 6 */}
              <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-lg">
                  6
                </div>
                <h3 className="text-lg font-bold text-slate-900">CONTINUE</h3>
                <p className="mt-2 text-sm leading-relaxed text-gray-600">
                  Bridges maternal history directly to newborn first-year health monitoring.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
