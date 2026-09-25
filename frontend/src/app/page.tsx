import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <header className="sticky top-0 z-50 w-full border-b border-gray-100 bg-white/80 backdrop-blur-md">
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
            <a href="#features" className="text-sm font-medium text-gray-600 hover:text-pink-500 transition-colors">Features</a>
            <a href="#workflow" className="text-sm font-medium text-gray-600 hover:text-pink-500 transition-colors">How it Works</a>
            <a href="#about" className="text-sm font-medium text-gray-600 hover:text-pink-500 transition-colors">About</a>
            <button className="rounded-full bg-slate-900 px-5 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-slate-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-900 transition-all">
              Go to Dashboard
            </button>
          </nav>
        </div>
      </header>

      <main>
        {/* Hero Section */}
        <section className="relative overflow-hidden bg-white pt-24 pb-32 sm:pt-32 sm:pb-40">
          <div className="absolute inset-x-0 top-0 h-[40rem] flex-none bg-gradient-to-b from-pink-50 to-white"></div>
          <div className="relative container mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="max-w-3xl mx-auto">
              <span className="inline-flex items-center rounded-full bg-pink-100 px-3 py-1 text-sm font-medium text-pink-700 ring-1 ring-inset ring-pink-600/10 mb-6">
                HT-06: Maternal & Neonatal Intelligence
              </span>
              <h1 className="text-5xl font-extrabold tracking-tight text-slate-900 sm:text-7xl mb-8">
                Continuity of care for{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-rose-400">
                  Mother & Baby
                </span>
              </h1>
              <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto">
                An AI-assisted clinical decision support and referral platform that connects verified medical history, longitudinal trends, and emergency communication into one continuous health journey.
              </p>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <a
                  href="#"
                  className="rounded-full bg-pink-500 px-8 py-3.5 text-sm font-semibold text-white shadow-sm hover:bg-pink-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-pink-500 transition-all"
                >
                  Start Triage
                </a>
                <a href="#features" className="text-sm font-semibold leading-6 text-slate-900 flex items-center gap-1 hover:text-pink-500 transition-colors">
                  Explore Features <span aria-hidden="true">→</span>
                </a>
              </div>
            </div>
          </div>
        </section>

        {/* The 6 Core Pillars Section */}
        <section id="features" className="py-24 sm:py-32 bg-slate-50">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-2xl lg:text-center mb-16">
              <h2 className="text-base font-semibold leading-7 text-pink-500">The Core Innovation</h2>
              <p className="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
                Not just prediction. A complete continuous layer.
              </p>
              <p className="mt-6 text-lg leading-8 text-gray-600">
                Most systems focus on detecting a risk at one point in time. MaternaCare connects the patient's history, current condition, and referral workflow together.
              </p>
            </div>

            <div className="mx-auto max-w-5xl mt-16 sm:mt-20 lg:mt-24">
              <div className="grid grid-cols-1 gap-12 sm:grid-cols-2 lg:grid-cols-3">
                {/* Pillar 1 */}
                <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-xl">
                    1
                  </div>
                  <h3 className="text-xl font-semibold leading-7 text-slate-900">REMEMBER</h3>
                  <p className="mt-2 text-base leading-7 text-gray-600">
                    Extracts and verifies previous medical history from unstructured records using Document AI.
                  </p>
                </div>
                {/* Pillar 2 */}
                <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-xl">
                    2
                  </div>
                  <h3 className="text-xl font-semibold leading-7 text-slate-900">UNDERSTAND</h3>
                  <p className="mt-2 text-base leading-7 text-gray-600">
                    Captures current clinical conditions, symptoms, vitals, and gestational age seamlessly.
                  </p>
                </div>
                {/* Pillar 3 */}
                <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-xl">
                    3
                  </div>
                  <h3 className="text-xl font-semibold leading-7 text-slate-900">PREDICT</h3>
                  <p className="mt-2 text-base leading-7 text-gray-600">
                    Temporal ML identifies concerning risk trajectories rather than just analyzing static snapshots.
                  </p>
                </div>
                {/* Pillar 4 */}
                <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-xl">
                    4
                  </div>
                  <h3 className="text-xl font-semibold leading-7 text-slate-900">EXPLAIN</h3>
                  <p className="mt-2 text-base leading-7 text-gray-600">
                    Uses SHAP to explain exactly why the AI model is concerned, keeping humans in the loop.
                  </p>
                </div>
                {/* Pillar 5 */}
                <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-xl">
                    5
                  </div>
                  <h3 className="text-xl font-semibold leading-7 text-slate-900">REFER</h3>
                  <p className="mt-2 text-base leading-7 text-gray-600">
                    Automatically locates facilities via Google Maps and bridges emergency voice communication.
                  </p>
                </div>
                {/* Pillar 6 */}
                <div className="relative p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-pink-100 text-pink-600 mb-4 font-bold text-xl">
                    6
                  </div>
                  <h3 className="text-xl font-semibold leading-7 text-slate-900">FOLLOW UP</h3>
                  <p className="mt-2 text-base leading-7 text-gray-600">
                    Extends the journey to neonatal monitoring and tracks pattern-changes in the baby's first year.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-white py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="bg-slate-900 rounded-3xl p-8 sm:p-16 text-center shadow-xl">
              <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                Ready to transform maternal referral intelligence?
              </h2>
              <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-300">
                Deploy MaternaCare directly to Vercel and AWS to experience the end-to-end continuous health journey for Mothers and Newborns.
              </p>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <a
                  href="#"
                  className="rounded-full bg-pink-500 px-8 py-3.5 text-sm font-semibold text-white shadow-sm hover:bg-pink-400 transition-all focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-pink-500"
                >
                  Deploy the System
                </a>
                <a href="#" className="text-sm font-semibold leading-6 text-white hover:text-pink-300 transition-colors">
                  View GitHub Repo <span aria-hidden="true">→</span>
                </a>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-500">
          <p>© {new Date().getFullYear()} MaternaCare. Built for HT-06.</p>
        </div>
      </footer>
    </div>
  );
}
