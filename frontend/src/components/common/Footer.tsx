import React from "react";

export function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200/80 py-8">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-gray-500">
        <p>&copy; {new Date().getFullYear()} MaternaCare — AI-Powered Maternal &amp; Neonatal Continuity Platform.</p>
      </div>
    </footer>
  );
}
