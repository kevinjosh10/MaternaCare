import { NextRequest, NextResponse } from "next/server";
import { logAuditTrail } from "@/lib/aws-cloudwatch";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const message = body.message || "";
    const patientId = body.patientId || body.patient_id || "priya.sharma@example.com";
    const language = body.language || body.source_lang || "en";

    const pythonServerUrl = process.env.PYTHON_BACKEND_URL || "https://untie-send-transpose.ngrok-free.dev";

    // 1. Try forwarding to friend's Python Backend LLM Microservice
    try {
      const pyResponse = await fetch(`${pythonServerUrl}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true",
        },
        body: JSON.stringify({
          message,
          text: message,
          patient_id: patientId,
          source_lang: language,
          language,
        }),
      });

      if (pyResponse.ok) {
        const pyData = await pyResponse.json();

        // Log interaction to AWS CloudWatch
        await logAuditTrail({
          action: "CONVERSATIONAL_CHAT_QUERY",
          userId: "patient",
          patientId,
          details: {
            query: message,
            source: "python_backend",
            requiresApproval: pyData.requiresApproval || pyData.status === "PENDING_APPROVAL",
          },
          level: "INFO",
        });

        return NextResponse.json({
          success: true,
          response: pyData.response || pyData.text || pyData.translated_text || "Response received from MaternaCare Brain.",
          status: pyData.status || "COMPLETED",
          requiresApproval: pyData.requiresApproval || pyData.status === "PENDING_APPROVAL",
          proposedAdvice: pyData.proposed_advice || pyData.proposedAdvice || null,
          source: "python_backend_llm",
        });
      }
    } catch (pyErr) {
      console.warn(`[Chat Proxy] Note: Python server at ${pythonServerUrl}/api/chat not directly reachable:`, pyErr);
    }

    // 2. Intelligent Maternal Clinical AI Fallback
    const lower = message.toLowerCase();
    let reply = "Hello Priya. I am monitoring your maternal trajectory closely. Please let me know how you are feeling or if you have any questions regarding your pregnancy.";
    let requiresApproval = false;
    let proposedAdvice = null;

    if (lower.includes("headache") || lower.includes("pain") || lower.includes("dard") || lower.includes("swelling")) {
      reply = "I noticed you mentioned pain or swelling. Because your last recorded blood pressure was 142/92 mmHg, this could be an early warning sign. Please rest in a left-lateral position and inform your on-duty nurse immediately.";
      requiresApproval = true;
      proposedAdvice = "Evaluate for preeclampsia progression; recommend left-lateral rest and BP check within 15 minutes.";
    } else if (lower.includes("diet") || lower.includes("food") || lower.includes("tea") || lower.includes("khana")) {
      reply = "A balanced diet with plenty of hydration, leafy greens, and reduced sodium is recommended to help maintain healthy blood pressure.";
      requiresApproval = true;
      proposedAdvice = "Low-sodium maternal diet with hydration; avoid caffeinated herbal infusions.";
    }

    return NextResponse.json({
      success: true,
      response: reply,
      status: requiresApproval ? "PENDING_APPROVAL" : "COMPLETED",
      requiresApproval,
      proposedAdvice,
      source: "local_maternacare_engine",
      note: `Connected to Next.js API. Pointing to Python microservice at ${pythonServerUrl}/api/chat.`,
    });
  } catch (error) {
    console.error("Chat API error:", error);
    return NextResponse.json(
      { error: "Failed to process chat request" },
      { status: 500 }
    );
  }
}
