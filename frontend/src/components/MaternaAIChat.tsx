"use client";

import React, { useState, useEffect, useRef } from "react";
import { ParentIcon } from "./icons/PortalIcons";

export function MaternaAIChat({ patientId = "PAT-DEMO-001" }: { patientId?: string }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{ sender: "user" | "ai"; text: string; isEmergency?: boolean; isBlocked?: boolean }[]>([
    { sender: "ai", text: "Hello! I am your MaternaCare AI. You can type or use your voice to ask me any medical questions." },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Try to grab SpeechRecognition API for the browser
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const SpeechRecognition = typeof window !== "undefined" ? (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition : null;
  const recognition = SpeechRecognition ? new SpeechRecognition() : null;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const toggleListen = () => {
    if (!recognition) {
      alert("Voice recognition is not supported in this browser. Please use Chrome.");
      return;
    }
    
    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "en-US";
      
      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);
      
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInputValue(transcript);
        // Automatically send after capturing voice
        handleSend(transcript);
      };
      
      recognition.start();
    }
  };

  const handleSend = async (textToSend?: string) => {
    const text = textToSend || inputValue;
    if (!text.trim()) return;

    setMessages((prev) => [...prev, { sender: "user", text }]);
    setInputValue("");
    setIsLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, patientId, language: "en" }),
      });
      
      const data = await res.json();
      
      if (data.status === "EMERGENCY_DISPATCHED") {
        setMessages((prev) => [...prev, { 
          sender: "ai", 
          text: data.response || "EMERGENCY DETECTED. Ambulance dispatched.",
          isEmergency: true 
        }]);
      } else if (data.requiresApproval || data.status === "PENDING_APPROVAL" || data.status === "PENDING_DOCTOR_APPROVAL") {
        setMessages((prev) => [...prev, { 
          sender: "ai", 
          text: data.response || "Your request has been forwarded to a doctor for review.",
          isBlocked: true
        }]);
      } else {
        setMessages((prev) => [...prev, { sender: "ai", text: data.response || "I have received your query." }]);
        
        // Optional: browser TTS
        if (typeof window !== "undefined" && window.speechSynthesis) {
          const utterance = new SpeechSynthesisUtterance(data.response);
          window.speechSynthesis.speak(utterance);
        }
      }
      
    } catch (error) {
      console.error(error);
      setMessages((prev) => [...prev, { sender: "ai", text: "Sorry, I could not connect to the Medical Brain." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Floating Action Button */}
      <button
        onClick={() => setIsOpen(true)}
        className={`fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-r from-pink-500 to-rose-500 text-white rounded-full shadow-2xl flex items-center justify-center hover:scale-105 transition-transform z-50 ${isOpen ? "hidden" : ""}`}
      >
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" /></svg>
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-[350px] sm:w-[400px] h-[500px] bg-white rounded-3xl shadow-2xl border border-pink-100 flex flex-col z-50 overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-pink-500 to-rose-500 p-4 text-white flex justify-between items-center">
            <div className="flex items-center gap-2">
              <ParentIcon className="w-6 h-6" />
              <h3 className="font-bold text-sm">MaternaCare AI Assistant</h3>
            </div>
            <button onClick={() => setIsOpen(false)} className="hover:text-pink-200">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div 
                  className={`max-w-[80%] rounded-2xl p-3 text-sm shadow-sm ${
                    msg.sender === "user" 
                      ? "bg-pink-600 text-white rounded-br-sm" 
                      : msg.isEmergency 
                        ? "bg-red-600 text-white font-bold rounded-bl-sm border-2 border-red-200 animate-pulse"
                        : msg.isBlocked
                          ? "bg-amber-100 text-amber-900 rounded-bl-sm border border-amber-300"
                          : "bg-white text-slate-800 rounded-bl-sm border border-slate-200"
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white rounded-2xl p-3 border border-slate-200 shadow-sm rounded-bl-sm text-xs text-gray-500 flex items-center gap-2">
                  <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce delay-75"></div>
                  <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce delay-150"></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-3 bg-white border-t border-slate-100 flex items-center gap-2">
            <button 
              onClick={toggleListen}
              className={`p-3 rounded-full flex-shrink-0 transition-colors ${
                isListening ? "bg-red-500 text-white animate-pulse" : "bg-pink-100 text-pink-600 hover:bg-pink-200"
              }`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" /></svg>
            </button>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask a medical question..."
              className="flex-1 px-4 py-2 bg-slate-100 rounded-full text-sm outline-none focus:ring-2 focus:ring-pink-500/50"
            />
            <button 
              onClick={() => handleSend()}
              className="p-3 bg-pink-600 text-white rounded-full hover:bg-pink-700 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
            </button>
          </div>
        </div>
      )}
    </>
  );
}
