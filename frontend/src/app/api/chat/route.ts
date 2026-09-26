import { NextRequest, NextResponse } from "next/server";
import { logAuditTrail } from "@/lib/aws-cloudwatch";

export const dynamic = "force-dynamic";
export const maxDuration = 60;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const message = (body.message || body.text || "").trim();
    const patientId = body.patientId || body.patient_id || "priya.sharma@example.com";
    const patientName = body.patientName || "Priya Sharma";
    const language = body.language || body.source_lang || "en";
    
    if (!message) {
      return NextResponse.json({ error: "No message provided" }, { status: 400 });
    }

    // 1. Point directly to the Python Multi-Model Orchestrator
    const pythonServerUrl = "https://untie-send-transpose.ngrok-free.dev";
    const endpoint = pythonServerUrl.endsWith("/api/chat") ? pythonServerUrl : `${pythonServerUrl}/api/chat`;

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 45000); 

      const pyResponse = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true",
          "Bypass-Tunnel-Reminder": "true",
        },
        body: JSON.stringify({
          message,
          patient_id: patientId,
          source_lang: language,
          language: language
        }),
        signal: controller.signal,
      });
      clearTimeout(timeout);

      if (pyResponse.ok) {
        const pyData = await pyResponse.json();
        const responseText = pyData.response || pyData.text || pyData.patient_friendly_text || pyData.translated_text;

        await logAuditTrail({
          action: "CONVERSATIONAL_CHAT_QUERY",
          userId: "patient",
          patientId,
          details: { query: message, source: "python_orchestrator" },
          level: "INFO",
        });

        return NextResponse.json({
          success: true,
          response: responseText,
          detected_language: pyData.detected_language || pyData.detectedLanguage || language || "en",
          status: pyData.status || "COMPLETED",
          requiresApproval: pyData.requiresApproval || pyData.status === "PENDING_DOCTOR_APPROVAL",
          proposedAdvice: pyData.proposedAdvice || null,
          source: "MaternaCare Layered Architecture",
          audio_base64: pyData.audio_base64 || null,
          audio_format: pyData.audio_format || "audio/mp3",
        });
      } else {
        const errText = await pyResponse.text();
        console.error("Python backend error:", errText);
        return NextResponse.json({ 
          error: "Model API Error. Please check terminal logs.", 
          details: errText 
        }, { status: pyResponse.status });
      }
    } catch (colabErr: any) {
      console.error("Python Server Unreachable:", colabErr.message);
      return NextResponse.json({ 
        error: "AI Model Offline. Please ensure Python backend and Ngrok are running.",
        details: colabErr.message
      }, { status: 503 });
    }
  } catch (error) {
    console.error("Chat API error:", error);
    return NextResponse.json({ error: "Failed to process request" }, { status: 500 });
  }
}
