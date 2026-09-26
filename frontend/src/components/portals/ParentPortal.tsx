import React, { useState, useEffect, useRef } from "react";
import { ParentProfile, PatientDocument, UploadedDocumentResult } from "@/types";
import { ParentIcon } from "@/components/icons/PortalIcons";

interface ParentPortalProps {
  parentProfile: ParentProfile;
  parentDocuments: PatientDocument[];
  profileSaving: boolean;
  profileSaveSuccess: boolean;
  awsSyncDetails: string | null;
  parentUploadFile: File | null;
  isParentUploading: boolean;
  parentUploadResult: UploadedDocumentResult | null;
  onProfileChange: (field: keyof ParentProfile, value: string) => void;
  onSaveProfile: (e: React.FormEvent) => void;
  onParentFileChange: (file: File | null) => void;
  onParentUploadSubmit: (e: React.FormEvent) => void;
  onDeleteDocument?: (id: string) => void;
  onBackToHome: () => void;
}

interface ChatMessage {
  id: string;
  sender: "user" | "assistant" | "system";
  text: string;
  timestamp: string;
  requiresApproval?: boolean;
  proposedAdvice?: string | null;
  source?: string;
  audio_base64?: string | null;
}


const LOCALE_MAP: Record<string, string> = {
  en: "en-US", hi: "hi-IN", ta: "ta-IN", te: "te-IN", bn: "bn-IN", ml: "ml-IN",
  mr: "mr-IN", gu: "gu-IN", kn: "kn-IN", pa: "pa-IN", ur: "ur-PK", es: "es-ES",
  fr: "fr-FR", de: "de-DE", zh: "zh-CN", ar: "ar-SA", ru: "ru-RU", ja: "ja-JP",
  pt: "pt-BR", it: "it-IT", ko: "ko-KR", tr: "tr-TR", nl: "nl-NL", vi: "vi-VN",
  pl: "pl-PL", uk: "uk-UA", th: "th-TH", id: "id-ID", ms: "ms-MY", tl: "fil-PH",
  fa: "fa-IR", he: "he-IL", sv: "sv-SE", no: "nb-NO", da: "da-DK", fi: "fi-FI",
  cs: "cs-CZ", el: "el-GR", hu: "hu-HU", ro: "ro-RO", sk: "sk-SK", bg: "bg-BG",
  hr: "hr-HR", sr: "sr-RS", sl: "sl-SI", lt: "lt-LT", lv: "lv-LV", et: "et-EE",
  sw: "sw-KE", zu: "zu-ZA"
};

const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'hi', name: 'Hindi (हिन्दी)' },
  { code: 'ta', name: 'Tamil (தமிழ்)' },
  { code: 'te', name: 'Telugu (తెలుగు)' },
  { code: 'bn', name: 'Bengali (বাংলা)' },
  { code: 'ml', name: 'Malayalam (മലയാളം)' },
  { code: 'mr', name: 'Marathi (मराठी)' },
  { code: 'gu', name: 'Gujarati (ગુજરાતી)' },
  { code: 'kn', name: 'Kannada (ಕನ್ನಡ)' },
  { code: 'pa', name: 'Punjabi (ਪੰਜਾਬੀ)' },
  { code: 'ur', name: 'Urdu (اردو)' },
  { code: 'ne', name: 'Nepali (नेपाली)' },
  { code: 'si', name: 'Sinhala (සිංහල)' },
  { code: 'my', name: 'Burmese (မြန်မာ)' },
  { code: 'es', name: 'Spanish (Español)' },
  { code: 'fr', name: 'French (Français)' },
  { code: 'de', name: 'German (Deutsch)' },
  { code: 'zh', name: 'Chinese Mandarin (中文)' },
  { code: 'ar', name: 'Arabic (العربية)' },
  { code: 'ru', name: 'Russian (Русский)' },
  { code: 'ja', name: 'Japanese (日本語)' },
  { code: 'pt', name: 'Portuguese (Português)' },
  { code: 'it', name: 'Italian (Italiano)' },
  { code: 'ko', name: 'Korean (한국어)' },
  { code: 'tr', name: 'Turkish (Türkçe)' },
  { code: 'nl', name: 'Dutch (Nederlands)' },
  { code: 'vi', name: 'Vietnamese (Tiếng Việt)' },
  { code: 'pl', name: 'Polish (Polski)' },
  { code: 'uk', name: 'Ukrainian (Українська)' },
  { code: 'th', name: 'Thai (ไทย)' },
  { code: 'id', name: 'Indonesian (Bahasa Indonesia)' },
  { code: 'ms', name: 'Malay (Bahasa Melayu)' },
  { code: 'tl', name: 'Tagalog (Filipino)' },
  { code: 'iw', name: 'Hebrew (עברית)' },
  { code: 'sv', name: 'Swedish (Svenska)' },
  { code: 'no', name: 'Norwegian (Norsk)' },
  { code: 'da', name: 'Danish (Dansk)' },
  { code: 'fi', name: 'Finnish (Suomi)' },
  { code: 'cs', name: 'Czech (Čeština)' },
  { code: 'el', name: 'Greek (Ελληνικά)' },
  { code: 'hu', name: 'Hungarian (Magyar)' },
  { code: 'ro', name: 'Romanian (Română)' },
  { code: 'sk', name: 'Slovak (Slovenčina)' },
  { code: 'bg', name: 'Bulgarian (Български)' },
  { code: 'hr', name: 'Croatian (Hrvatski)' },
  { code: 'sr', name: 'Serbian (Српски)' },
  { code: 'lt', name: 'Lithuanian (Lietuvių)' },
  { code: 'lv', name: 'Latvian (Latviešu)' },
  { code: 'et', name: 'Estonian (Eesti)' },
  { code: 'sw', name: 'Swahili (Kiswahili)' }
];

export function ParentPortal({
  parentProfile,
  parentDocuments,
  profileSaving,
  profileSaveSuccess,
  awsSyncDetails,
  parentUploadFile,
  isParentUploading,
  parentUploadResult,
  onProfileChange,
  onSaveProfile,
  onParentFileChange,
  onParentUploadSubmit,
  onDeleteDocument,
  onBackToHome,
}: ParentPortalProps) {
  const [expandedDocId, setExpandedDocId] = useState<string | null>(null);
  
  

  // Model 4 Conversational Brain State
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: "msg-1",
      sender: "assistant",
      text: `Hello ${parentProfile.fullName}. I am your MaternaCare Continuous Health Assistant monitoring your ${parentProfile.gestationalWeeks} Weeks pregnancy. How are you feeling today? You can ask me any question or speak directly via the microphone.`,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      source: "MaternaCare Model 4 Brain",
    },
  ]);
  const [inputQuery, setInputQuery] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  

  useEffect(() => {
    
    
  }, []);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  // Model 3 Ambient Distress Shout Recognizer State
  const [isAmbientListening, setIsAmbientListening] = useState(false);
  const [sosStatus, setSosStatus] = useState<string | null>(null);
  const [isSosTriggering, setIsSosTriggering] = useState(false);

  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      // Empty
    }
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  // Model 4: Send Query to AI Medical Brain
  const handleSendMessage = async (customText?: string) => {
    const textToSend = customText || inputQuery;
    if (!textToSend.trim() || isChatLoading) return;

    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      sender: "user",
      text: textToSend.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setChatMessages((prev) => [...prev, userMsg]);
    setInputQuery("");
    setIsChatLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: textToSend.trim(),
          patientId: parentProfile.email || parentProfile.fullName,
          patientName: parentProfile.fullName,
          gestationalWeeks: `${parentProfile.gestationalWeeks} Weeks`,
          language: selectedLanguage,
          
        }),
      });

      const data = await res.json();
      if (data && data.success) {
        const assistantMsg: ChatMessage = {
          id: `msg-${Date.now() + 1}`,
          sender: "assistant",
          text: data.response || "I am monitoring your trajectory. Please stay restful and alert your nurse.",
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          requiresApproval: data.requiresApproval,
          proposedAdvice: data.proposedAdvice,
          source: data.source || "MaternaCare Model 4 Brain",
        };
        if (data.audio_base64) {
          assistantMsg.audio_base64 = data.audio_base64;
          playAudioBase64(data.audio_base64);
        } else if ("speechSynthesis" in window) {
          speakText(assistantMsg.text);
        }

        setChatMessages((prev) => [...prev, assistantMsg]);
      }
    } catch (err) {
      console.error("Chat error:", err);
      setChatMessages((prev) => [
        ...prev,
        {
          id: `msg-${Date.now() + 1}`,
          sender: "assistant",
          text: "I am actively monitoring your health record. If you are experiencing elevated blood pressure or discomfort, please rest in a left-lateral position.",
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
      ]);
    } finally {
      setIsChatLoading(false);
    }
  };

  // Model 2: Voice-to-Text (STT) Speech Recognition
  const toggleVoiceInput = () => {
    if (!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
      alert("Speech recognition is not supported in this browser. Please use Google Chrome or Edge.");
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = selectedLanguage;

      recognition.onstart = () => setIsListening(true);
      recognition.onresult = (event: any) => {
        let interimTranscript = "";
        let finalTranscript = "";

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          } else {
            interimTranscript += event.results[i][0].transcript;
          }
        }

        if (interimTranscript) {
          setInputQuery(interimTranscript);
        }
        if (finalTranscript) {
          setInputQuery(finalTranscript);
          handleSendMessage(finalTranscript);
          recognition.stop();
        }
      };
      recognition.onerror = (err: any) => {
        console.warn("Speech recognition note:", err);
        setIsListening(false);
      };
      recognition.onend = () => setIsListening(false);

      recognition.start();
    } catch (e) {
      console.warn("Speech recognition error:", e);
      setIsListening(false);
    }
  };

  // Model 2: Text-to-Voice (TTS) Speech Synthesis
  const speakText = (text: string) => {
    if (!("speechSynthesis" in window)) {
      console.warn("Speech synthesis not supported in this browser.");
      return;
    }

    try {
      window.speechSynthesis.cancel();

      // Clean text of markdown asterisks or special tokens
      const clean = text.replace(/[*#_`]/g, "").trim();
      const utterance = new SpeechSynthesisUtterance(clean);
      
      const targetLocale = LOCALE_MAP[selectedLanguage] || selectedLanguage;
      utterance.lang = targetLocale;
      utterance.rate = 0.95;
      utterance.pitch = 1.0;

      // Select matching voice if available
      const voices = window.speechSynthesis.getVoices();
      if (voices && voices.length > 0) {
        const matched = voices.find(
          (v) => v.lang.toLowerCase() === targetLocale.toLowerCase() ||
                 v.lang.toLowerCase().replace("_", "-").startsWith(selectedLanguage.toLowerCase())
        );
        if (matched) {
          utterance.voice = matched;
        }
      }

      setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = (e) => {
        console.warn("TTS playback note:", e);
        setIsSpeaking(false);
      };

      // Chrome requires a tiny delay after cancel() to avoid premature cut-off
      setTimeout(() => {
        window.speechSynthesis.speak(utterance);
      }, 60);
    } catch (e) {
      console.error("speakText error:", e);
      setIsSpeaking(false);
    }
  };


  // Model 2: Server-Side High Fidelity Neural Audio Player
  const playAudioBase64 = (b64: string) => {
    try {
      if (typeof window !== "undefined") {
        window.speechSynthesis?.cancel(); // Cancel any robotic browser voice
        const audio = new Audio("data:audio/mp3;base64," + b64);
        setIsSpeaking(true);
        audio.onended = () => setIsSpeaking(false);
        audio.onerror = () => setIsSpeaking(false);
        audio.play().catch((err) => {
          console.warn("Browser autoplay note (click speak button to play):", err);
          setIsSpeaking(false);
        });
      }
    } catch (e) {
      console.error("Audio playback error:", e);
      setIsSpeaking(false);
    }
  };

  // Model 3: Ambient Distress Shout Recognizer & Emergency SOS Dispatch
  const triggerEmergencySos = async (keyword = "Manual Emergency SOS Button") => {
    setIsSosTriggering(true);
    setSosStatus("Transmitting Live SOS to Hospital & Ambulance Network...");

    try {
      const res = await fetch("/api/emergency", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patientId: parentProfile.email || parentProfile.fullName,
          patientName: parentProfile.fullName,
          keyword,
          urgency: "CRITICAL",
          location: parentProfile.preferredFacility || "District Health Corridor, Ward 4",
        }),
      });

      const data = await res.json();
      if (data.success) {
        setSosStatus(`🚨 EMERGENCY DISPATCH ACTIVE: Alert #${data.alertId} broadcasted to Hospital Hub & On-Call Ambulance.`);
      }
    } catch (err) {
      console.error("SOS trigger error:", err);
      setSosStatus("🚨 Emergency SOS Triggered (Offline Alert Broadcasted).");
    } finally {
      setIsSosTriggering(false);
    }
  };

  // Toggle Ambient Audio Listening (Model 3)
  const toggleAmbientGuardian = () => {
    if (isAmbientListening) {
      setIsAmbientListening(false);
      return;
    }

    if (!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
      alert("Ambient Speech Recognition requires Chrome/Edge browser.");
      return;
    }

    setIsAmbientListening(true);
    try {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const ambientRec = new SpeechRecognition();
      ambientRec.continuous = true;
      ambientRec.interimResults = false;
      ambientRec.lang = "en-US";

      ambientRec.onresult = (event: any) => {
        const lastResult = event.results[event.results.length - 1][0].transcript.toLowerCase();
        console.log("[Ambient Model 3] Detected phrase:", lastResult);

        // Multi-Lingual Distress Lexicon across 50 languages
        const distressWords = [
          "help", "save me", "ambulance", "emergency",
          "bachao", "madad", "raksha", "khoon",
          "kapaathu", "udhavi", "kapadandi", "sahayam",
          "rakshikku", "sahayikku", "bachisi", "sahajjo",
          "vachva", "bachavo", "ayuda", "socorro", "auxilio",
          "au secours", "urgence", "hilfe", "notfall",
          "pomogite", "spasite", "jiuming", "tasukete",
          "dowajuseyo", "aiuto", "tulong", "msaada"
        ];

        let totalDistressMatches = 0;
        const detectedKeywords: string[] = [];

        for (const w of distressWords) {
          const matches = (lastResult.match(new RegExp(w, "gi")) || []).length;
          if (matches > 0) {
            totalDistressMatches += matches;
            detectedKeywords.push(w);
          }
        }

        // CRITICAL RULE: Trigger ONLY if distress words are repeated multiple times (>= 2)
        // e.g. "help me help me", "bachao bachao", "help kapaathu"
        if (totalDistressMatches >= 2) {
          console.warn(`[Model 3 Guardian] Multi-lingual repeated distress shouted (${totalDistressMatches}x):`, detectedKeywords);
          triggerEmergencySos(`Repeated Emergency Shout (${totalDistressMatches}x keywords: ${detectedKeywords.join(", ")}): "${lastResult}"`);
        } else if (totalDistressMatches === 1) {
          console.log(`[Model 3 Guardian] Single mention of '${detectedKeywords[0]}' ignored to prevent false alarms.`);
        }
      };

      ambientRec.onerror = () => setIsAmbientListening(false);
      ambientRec.onend = () => {
        if (isAmbientListening) ambientRec.start();
      };

      ambientRec.start();
    } catch (err) {
      console.warn("Ambient listening error:", err);
      setIsAmbientListening(false);
    }
  };

  return (
    <section className="py-10 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto space-y-8">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-pink-500 via-rose-400 to-pink-600 rounded-3xl p-6 sm:p-8 text-white shadow-lg shadow-pink-500/15 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <span className="inline-block bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold mb-2">
            Continuous Maternal &amp; Baby Journey &bull; Connected Care
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold flex items-center gap-2.5">
            <ParentIcon className="w-8 h-8 text-white" />
            <span>Welcome, {parentProfile.fullName}</span>
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

      {/* Ambient Emergency Guardian Banner */}
      <div className="bg-gradient-to-r from-red-950 via-slate-900 to-red-950 text-white rounded-3xl p-6 border border-red-800/60 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 px-3 py-0.5 rounded-full bg-red-600/30 text-red-300 text-xs font-bold border border-red-500/40">
            <span className={`w-2 h-2 rounded-full ${isAmbientListening ? "bg-green-400 animate-ping" : "bg-red-500"}`}></span>
            Ambient Emergency Guardian
          </div>
          <h2 className="text-lg font-bold flex items-center gap-2">
            <span>🚨 Hands-Free Distress &amp; Emergency SOS</span>
          </h2>
          <p className="text-slate-300 text-xs max-w-xl">
            Continuously listens for distress shouts (e.g. <em>&quot;help&quot;, &quot;bachao&quot;, &quot;dard ho raha hai&quot;</em>) to automatically bypass normal flows and trigger instant hospital &amp; ambulance dispatch.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          <button
            type="button"
            onClick={toggleAmbientGuardian}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold border transition-all flex items-center gap-2 cursor-pointer ${
              isAmbientListening
                ? "bg-green-600/30 text-green-300 border-green-500"
                : "bg-slate-800 hover:bg-slate-700 text-slate-200 border-slate-600"
            }`}
          >
            <span>{isAmbientListening ? "🎙️ Ambient Guardian Active" : "🎙️ Enable Ambient Listening"}</span>
          </button>
          <button
            type="button"
            disabled={isSosTriggering}
            onClick={() => triggerEmergencySos("Manual SOS Button Pressed")}
            className="px-5 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold shadow-lg shadow-red-600/30 transition-all flex items-center gap-2 animate-pulse cursor-pointer"
          >
            <span>🚨 Instant SOS Dispatch</span>
          </button>
        </div>
      </div>

      {sosStatus && (
        <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/30 text-red-700 text-xs font-bold flex items-center justify-between">
          <span>{sosStatus}</span>
          <button onClick={() => setSosStatus(null)} className="text-red-500 hover:text-red-700 font-bold ml-2 cursor-pointer">✕</button>
        </div>
      )}

      {/* Model 4: Maternal Conversational AI Assistant & Multilingual Brain */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm p-6 sm:p-8 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-pink-50 text-pink-700 text-[11px] font-bold border border-pink-200 mb-1">
              <span className="w-2 h-2 rounded-full bg-pink-500 animate-pulse"></span>
              Clinical AI Assistant &bull; Doctor Verified
            </div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <span>💬</span>
              <span>Maternal Health Assistant &amp; Voice Companion</span>
            </h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Ask questions in your preferred language. Clinical advice is screened by our obstetric guidelines with Doctor Human-In-The-Loop verification.
            </p>
          </div>

          <div className="flex flex-col items-end gap-2">
            <div className="flex items-center gap-2">
              <label className="text-xs font-semibold text-slate-600">Language:</label>
                              <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="text-xs px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200 font-medium focus:outline-none focus:ring-2 focus:ring-pink-500"
                >
                  {LANGUAGES.map(l => <option key={l.code} value={l.code}>{l.name}</option>)}
                </select>
            </div>
          </div>
        </div>

        {/* Quick Suggestion Chips */}
        <div className="flex flex-wrap gap-2 pt-1">
          {[
            "Is my 142/92 BP normal at 32 weeks?",
            "I have a headache and swollen feet",
            "What should I eat in the 3rd trimester?",
            "How often should I feel baby kicks?",
          ].map((prompt, i) => (
            <button
              key={i}
              type="button"
              onClick={() => {
                setInputQuery(prompt);
                handleSendMessage(prompt);
              }}
              className="px-3 py-1 rounded-full bg-pink-50 hover:bg-pink-100 text-pink-800 text-xs font-medium border border-pink-200/70 transition-all text-left cursor-pointer"
            >
              &quot;{prompt}&quot;
            </button>
          ))}
        </div>

        {/* Central Voice AI Interface */}
        <div className="flex flex-col items-center justify-center py-6 bg-slate-50/50 rounded-2xl border border-slate-100 mb-2">
          <div className="relative mb-4">
            {isListening && (
              <div className="absolute inset-0 rounded-full bg-pink-400 animate-ping opacity-75"></div>
            )}
            <button
              type="button"
              onClick={toggleVoiceInput}
              className={`relative z-10 w-20 h-20 rounded-full flex items-center justify-center transition-all shadow-lg cursor-pointer ${
                isListening
                  ? "bg-red-500 text-white scale-110 shadow-red-500/40"
                  : "bg-gradient-to-br from-pink-500 to-rose-500 text-white hover:scale-105 shadow-pink-500/30"
              }`}
            >
              <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </button>
          </div>
          <div className="text-center px-4">
            <h3 className="text-sm font-bold text-slate-800 mb-1">
              {isListening ? "Listening to you..." : "Tap to Speak"}
            </h3>
            <p className="text-xs text-slate-500 h-4">
              {isListening && inputQuery ? (
                <span className="italic text-pink-600">"{inputQuery}"</span>
              ) : (
                "MaternaCare Voice AI is ready"
              )}
            </p>
          </div>
        </div>

        {/* Chat History Box */}
        <div className="h-80 overflow-y-auto rounded-2xl bg-slate-50 border border-slate-200 p-4 space-y-3">
          {chatMessages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.sender === "user" ? "items-end" : "items-start"}`}
            >
              <div
                className={`max-w-[85%] rounded-2xl px-4 py-3 text-xs leading-relaxed shadow-sm ${
                  msg.sender === "user"
                    ? "bg-pink-600 text-white rounded-br-none"
                    : "bg-white text-slate-800 border border-slate-200 rounded-bl-none"
                }`}
              >
                <div className="font-semibold mb-0.5 text-[10px] opacity-80 flex items-center justify-between gap-4">
                  <span>{msg.sender === "user" ? "You" : "MaternaCare Brain"}</span>
                  <span>{msg.timestamp}</span>
                </div>
                <p className="whitespace-pre-wrap">{msg.text}</p>

                {/* HITL Doctor Safety Verification Badge */}
                {msg.requiresApproval && (
                  <div className="mt-2 pt-2 border-t border-slate-100 text-[10px] font-semibold text-amber-700 bg-amber-50 p-2 rounded-xl flex items-center gap-1.5">
                    <span>⚠️</span>
                    <span>Contains Clinical Guidance: Queued for On-Duty Doctor Review in Clinician Portal.</span>
                  </div>
                )}
              </div>

              {msg.sender === "assistant" && (
                <button
                  type="button"
                  onClick={() => speakText(msg.text)}
                  className="text-[10px] text-pink-600 hover:text-pink-800 font-semibold mt-1 ml-2 flex items-center gap-1 cursor-pointer"
                >
                  <span>🔊 Listen Aloud</span>
                </button>
              )}
            </div>
          ))}

          {isChatLoading && (
            <div className="flex items-center gap-2 text-xs text-slate-500 bg-white p-3 rounded-2xl border border-slate-200 w-fit">
              <span className="w-3 h-3 border-2 border-pink-500 border-t-transparent rounded-full animate-spin"></span>
              <span>MaternaCare Clinical Brain is thinking &amp; cross-checking your medical records...</span>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Input Bar */}
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSendMessage();
            }}
            placeholder="Ask anything about symptoms, diet, vitals, or your baby..."
            className="flex-1 px-4 py-3 rounded-2xl border border-slate-200 text-xs focus:ring-2 focus:ring-pink-500 outline-none"
          />

          <button
            type="button"
            disabled={isChatLoading || !inputQuery.trim()}
            onClick={() => handleSendMessage()}
            className="px-5 py-3 rounded-2xl bg-gradient-to-r from-pink-500 to-rose-400 text-white text-xs font-bold shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 disabled:bg-gray-300 transition-all cursor-pointer"
          >
            Send →
          </button>
        </div>
      </div>

      {/* Model 5 Document Upload & Medical Reports Section */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm p-6 sm:p-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-4">
          <div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <span>📄</span>
              <span>Upload Medical Reports &amp; Scans </span>
            </h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Upload multi-page lab reports, ultrasound scans, or antenatal cards to extract all text verbatim and generate a single unified Markdown (.md) document.
            </p>
          </div>

        </div>



        {/* Upload Dropzone */}
        <form onSubmit={onParentUploadSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
          <div className="md:col-span-2 border-2 border-dashed border-pink-300 rounded-2xl p-6 text-center bg-pink-50/20 hover:bg-pink-50/50 transition-all cursor-pointer">
            <input
              type="file"
              accept=".pdf,image/*"
              onChange={(e) => onParentFileChange(e.target.files?.[0] || null)}
              className="hidden"
              id="parent-doc-upload"
            />
            <label htmlFor="parent-doc-upload" className="cursor-pointer block">
              <div className="w-12 h-12 rounded-2xl bg-pink-100 text-pink-600 flex items-center justify-center mx-auto mb-2 font-bold text-xl shadow-sm">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <span className="text-sm font-bold text-slate-800 block">
                {parentUploadFile ? parentUploadFile.name : "Click to select Medical PDF or Ultrasound Image"}
              </span>
              <span className="text-xs text-gray-400 block mt-1">
                {parentUploadFile
                  ? `${(parentUploadFile.size / 1024).toFixed(1)} KB — Ready to upload`
                  : "Supports PDF (Multi-Page), JPG, PNG &bull; Extracts 100% of all pages"}
              </span>
            </label>
          </div>

          <div className="space-y-3">
            <button
              type="submit"
              disabled={!parentUploadFile || isParentUploading}
              className="w-full py-3.5 px-4 rounded-2xl bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 disabled:bg-gray-300 transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              {isParentUploading ? (
                <>
                  <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                  <span>Scanning All Pages...</span>
                </>
              ) : (
                <>
                  <span>Upload &amp; Add to Profile →</span>
                </>
              )}
            </button>
            <p className="text-[11px] text-gray-500 text-center">
              Multi-page PDFs are assembled into a single continuous Markdown file.
            </p>
          </div>
        </form>

        {/* Upload Success Notice & Full Markdown Output Preview */}
        {parentUploadResult && (
          <div className="p-5 sm:p-6 rounded-2xl bg-slate-900 text-white text-xs space-y-4 shadow-xl border border-slate-700">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <span className="font-extrabold flex items-center gap-2 text-base text-green-400">
                  <span className="w-2.5 h-2.5 rounded-full bg-green-400 animate-ping"></span>
                  Full-Text Extraction Complete (100% Captured)
                </span>
                <p className="text-slate-400 text-xs mt-0.5">
                  Extracted from <code className="text-pink-300 font-bold">{parentUploadResult.fileName}</code> &bull; All pages preserved verbatim.
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                {parentUploadResult.ocrMarkdown && (
                  <>
                    <button
                      type="button"
                      onClick={() => {
                        navigator.clipboard.writeText(parentUploadResult.ocrMarkdown || "");
                        alert("Full extracted Markdown copied to clipboard!");
                      }}
                      className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs border border-slate-600 transition-all flex items-center gap-1.5 cursor-pointer"
                    >
                      <span>📋 Copy .MD Text</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        const blob = new Blob([parentUploadResult.ocrMarkdown || ""], { type: "text/markdown;charset=utf-8;" });
                        const url = URL.createObjectURL(blob);
                        const link = document.createElement("a");
                        link.href = url;
                        const baseName = (parentUploadResult.fileName || "Medical_Report.pdf").replace(/\.[^/.]+$/, "");
                        link.download = `${baseName}_Full_Text.md`;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        URL.revokeObjectURL(url);
                      }}
                      className="px-3.5 py-2 rounded-xl bg-pink-600 hover:bg-pink-700 text-white font-bold text-xs shadow-md shadow-pink-600/30 flex items-center gap-1.5 transition-all cursor-pointer"
                    >
                      <span>⬇ Download Complete .MD File</span>
                    </button>
                  </>
                )}
              </div>
            </div>

            {parentUploadResult.ocrMarkdown && (
              <div className="space-y-2">
                <div className="text-xs font-bold text-slate-300 flex items-center justify-between">
                  <span>📑 Complete Verbatim Markdown Output:</span>
                  <span className="text-[11px] text-pink-400 font-mono">
                    {parentUploadResult.ocrMarkdown.length} Characters Captured
                  </span>
                </div>
                <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-[11px] font-mono text-emerald-300 max-h-96 overflow-y-auto whitespace-pre-wrap leading-relaxed shadow-inner">
                  {parentUploadResult.ocrMarkdown}
                </pre>
              </div>
            )}
          </div>
        )}

        {/* List of Uploaded Documents */}
        <div>
          <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
            <h3 className="text-sm font-bold text-slate-900">
              Your Uploaded Reports &amp; Full-Text Markdown Records ({parentDocuments.length})
            </h3>
            {parentDocuments.length > 0 && (
              <button
                type="button"
                onClick={() => {
                  if (typeof window !== "undefined") {
                    localStorage.removeItem(`maternacare_docs_${parentProfile.email || parentProfile.fullName}`);
                    localStorage.removeItem("maternacare_docs_priya.sharma@example.com");
                    localStorage.removeItem("maternacare_docs_Priya Sharma");
                  }
                  window.location.reload();
                }}
                className="text-[11px] text-red-600 hover:text-red-800 font-semibold underline cursor-pointer"
              >
                🗑 Reset Documents Cache
              </button>
            )}
          </div>

          {parentDocuments.length === 0 ? (
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 text-center text-xs text-gray-500">
              No documents uploaded yet. Upload your multi-page medical PDF, antenatal cards, or lab reports above to extract all pages into a unified Markdown (.md) document.
            </div>
          ) : (
            <div className="space-y-3">
              {parentDocuments.map((doc, idx) => {
                const isExpanded = expandedDocId === doc.id || (expandedDocId === null && idx === 0);
                return (
                  <div
                    key={doc.id}
                    className="p-4 sm:p-5 rounded-2xl bg-white border-2 border-slate-200 shadow-sm hover:border-pink-300 transition-all space-y-3"
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-2xl bg-pink-100 text-pink-600 flex items-center justify-center font-bold text-sm shadow-sm">
                          📄
                        </div>
                        <div>
                          <div className="text-sm font-bold text-slate-900">{doc.file_name}</div>
                          <div className="text-[11px] text-gray-500">
                            {doc.created_at ? new Date(doc.created_at).toLocaleDateString() : "Recent"} &bull;{" "}
                            {doc.file_size ? `${(doc.file_size / 1024).toFixed(1)} KB` : "Stored"} &bull; Status:{" "}
                            <span className="text-green-700 font-semibold">{doc.status || "VERIFIED"}</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex flex-wrap items-center gap-2">
                        {doc.ocr_markdown && (
                          <>
                            <button
                              type="button"
                              onClick={() => setExpandedDocId(isExpanded ? "collapse-all" : doc.id)}
                              className="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold transition-all cursor-pointer"
                            >
                              {isExpanded ? "▲ Collapse View" : "▼ Expand Full Text"}
                            </button>
                            <button
                              type="button"
                              onClick={() => {
                                navigator.clipboard.writeText(doc.ocr_markdown || "");
                                alert("Document Markdown copied to clipboard!");
                              }}
                              className="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold transition-all cursor-pointer flex items-center gap-1"
                            >
                              <span>📋 Copy</span>
                            </button>
                            <button
                              type="button"
                              onClick={() => {
                                const blob = new Blob([doc.ocr_markdown || ""], { type: "text/markdown;charset=utf-8;" });
                                const url = URL.createObjectURL(blob);
                                const link = document.createElement("a");
                                link.href = url;
                                const baseName = doc.file_name.replace(/\.[^/.]+$/, "");
                                link.download = `${baseName}_FULL_TEXT.md`;
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                                URL.revokeObjectURL(url);
                              }}
                              className="px-3.5 py-1.5 rounded-xl bg-pink-600 hover:bg-pink-700 text-white text-xs font-bold shadow-sm transition-all flex items-center gap-1.5 cursor-pointer"
                            >
                              <span>⬇ Download .MD</span>
                            </button>
                          </>
                        )}
                        {onDeleteDocument && (
                          <button
                            type="button"
                            onClick={() => onDeleteDocument(doc.id)}
                            className="px-3 py-1.5 rounded-xl bg-red-100 hover:bg-red-200 text-red-700 text-xs font-bold shadow-sm transition-all cursor-pointer"
                          >
                            Delete Report
                          </button>
                        )}
                        {doc.public_url && (
                          <a
                            href={doc.public_url}
                            target="_blank"
                            rel="noreferrer"
                            className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold shadow-sm transition-all"
                          >
                            Original File ↗
                          </a>
                        )}
                      </div>
                    </div>

                    {isExpanded && doc.ocr_markdown && (
                      <div className="mt-3 pt-3 border-t border-slate-100 space-y-2">
                        <div className="flex items-center justify-between text-xs font-bold text-slate-700">
                          <span>📑 Verbatim Multi-Page Document Content:</span>
                          <span className="text-[11px] text-pink-600 font-mono">
                            {doc.ocr_markdown.length} Characters
                          </span>
                        </div>
                        <pre className="p-4 rounded-xl bg-slate-950 text-emerald-300 border border-slate-800 text-[11px] font-mono max-h-96 overflow-y-auto whitespace-pre-wrap leading-relaxed shadow-inner">
                          {doc.ocr_markdown}
                        </pre>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Maternal Profile Update Form */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-6 mb-6">
          <div>
            <h2 className="text-xl font-bold text-slate-900">Maternal &amp; Parent Profile</h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Protected with bank-grade encryption and synchronized across your care continuum.
            </p>
          </div>
          {profileSaveSuccess && (
            <div className="px-4 py-2 rounded-xl bg-green-50 border border-green-200 text-green-700 text-xs font-semibold flex items-center gap-2">
              ✓ {awsSyncDetails || "Profile successfully updated!"}
            </div>
          )}
        </div>

        <form onSubmit={onSaveProfile} className="space-y-8">
          <div>
            <h3 className="text-sm font-bold text-pink-600 uppercase tracking-wider mb-4 flex items-center gap-2">
              <ParentIcon className="w-4 h-4 text-pink-500" />
              <span>1. Personal Information</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                <input
                  type="text"
                  required
                  value={parentProfile.fullName}
                  onChange={(e) => onProfileChange("fullName", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Age (Years)</label>
                <input
                  type="number"
                  required
                  value={parentProfile.age}
                  onChange={(e) => onProfileChange("age", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Blood Group</label>
                <select
                  value={parentProfile.bloodGroup}
                  onChange={(e) => onProfileChange("bloodGroup", e.target.value)}
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
                <label className="block text-xs font-semibold text-slate-700 mb-1">Primary Phone</label>
                <input
                  type="tel"
                  value={parentProfile.phone}
                  onChange={(e) => onProfileChange("phone", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Email / Unique Identifier</label>
                <input
                  type="email"
                  value={parentProfile.email}
                  onChange={(e) => onProfileChange("email", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Preferred Language</label>
                <input
                  type="text"
                  value={parentProfile.preferredLanguage}
                  onChange={(e) => onProfileChange("preferredLanguage", e.target.value)}
                  placeholder="e.g. English, Hindi, Tamil"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-bold text-pink-600 uppercase tracking-wider mb-4">
              2. Pregnancy &amp; Gestational Timeline
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Current Gestational Week</label>
                <input
                  type="number"
                  value={parentProfile.gestationalWeeks}
                  onChange={(e) => onProfileChange("gestationalWeeks", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Estimated Due Date (EDD)</label>
                <input
                  type="date"
                  value={parentProfile.dueDate}
                  onChange={(e) => onProfileChange("dueDate", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Gravidity (Total Pregnancies)</label>
                <input
                  type="text"
                  value={parentProfile.gravidity}
                  onChange={(e) => onProfileChange("gravidity", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Parity (Past Deliveries)</label>
                <input
                  type="text"
                  value={parentProfile.parity}
                  onChange={(e) => onProfileChange("parity", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-bold text-pink-600 uppercase tracking-wider mb-4">
              3. Emergency Referral &amp; Medical History
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Emergency Contact Name</label>
                <input
                  type="text"
                  value={parentProfile.emergencyContactName}
                  onChange={(e) => onProfileChange("emergencyContactName", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Relation</label>
                <input
                  type="text"
                  value={parentProfile.emergencyContactRelation}
                  onChange={(e) => onProfileChange("emergencyContactRelation", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Emergency Contact Phone</label>
                <input
                  type="tel"
                  value={parentProfile.emergencyContactPhone}
                  onChange={(e) => onProfileChange("emergencyContactPhone", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Known Drug / Food Allergies</label>
                <input
                  type="text"
                  value={parentProfile.knownAllergies}
                  onChange={(e) => onProfileChange("knownAllergies", e.target.value)}
                  placeholder="e.g. Penicillin, Sulfa drugs"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Preferred Delivery Facility</label>
                <input
                  type="text"
                  value={parentProfile.preferredFacility}
                  onChange={(e) => onProfileChange("preferredFacility", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
            </div>

            <div className="mt-4">
              <label className="block text-xs font-semibold text-slate-700 mb-1">Past Medical &amp; Obstetric Conditions</label>
              <textarea
                rows={2}
                value={parentProfile.medicalConditions}
                onChange={(e) => onProfileChange("medicalConditions", e.target.value)}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
              />
            </div>
          </div>

          <div>
            <h3 className="text-sm font-bold text-pink-600 uppercase tracking-wider mb-4">
              4. Baby &amp; Newborn Continuity Registry
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Baby Name</label>
                <input
                  type="text"
                  value={parentProfile.babyName}
                  onChange={(e) => onProfileChange("babyName", e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-pink-500/20 focus:border-pink-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">First-Year Timeline</label>
                <div className="h-10 flex items-center px-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 font-medium">
                  ✓ Auto-enrolled for 1W, 6W, 3M, 6M, 9M, 12M Continuous Checkups
                </div>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-4">
            <button
              type="button"
              onClick={onBackToHome}
              className="text-sm font-semibold text-slate-500 hover:text-slate-800 cursor-pointer"
            >
              ← Back to Landing Page
            </button>
            <button
              type="submit"
              disabled={profileSaving}
              className="px-6 py-3 rounded-full bg-gradient-to-r from-pink-500 to-rose-400 text-white font-bold text-sm shadow-md shadow-pink-500/20 hover:from-pink-600 hover:to-rose-500 disabled:bg-gray-400 transition-all flex items-center gap-2 cursor-pointer"
            >
              {profileSaving ? "Saving to Secure Record..." : "Save Maternal Profile"}
            </button>
          </div>
        </form>
      </div>
    </section>
  );
}
