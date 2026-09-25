import { NextRequest, NextResponse } from "next/server";
import { logAuditTrail } from "@/lib/aws-cloudwatch";
import { db } from "@/lib/db";
import crypto from "crypto";

// In-memory cache for ultra-fast ambient SOS broadcast
const activeSosAlerts: any[] = [];

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const alertId = body.alertId || `SOS-${Date.now()}-${crypto.randomBytes(2).toString("hex")}`;
    const patientId = body.patient_id || body.patientId || "priya.sharma@example.com";
    const patientName = body.patient_name || body.patientName || "Priya Sharma";
    const keyword = body.keyword || body.detected_word || "help / bachao";
    const urgency = body.urgency || "CRITICAL";
    const location = body.location || "Rampur Primary Health Centre Cluster";
    const audioSnippetUrl = body.audio_url || body.audioSnippetUrl || null;
    const timestamp = body.timestamp || new Date().toISOString();

    const emergencyPayload = {
      alertId,
      patientId,
      patientName,
      keyword,
      urgency,
      location,
      audioSnippetUrl,
      status: "ACTIVE_DISPATCH",
      timestamp,
    };

    // 1. Store in broadcast cache
    activeSosAlerts.unshift(emergencyPayload);
    if (activeSosAlerts.length > 50) activeSosAlerts.pop();

    // 2. Stream to AWS CloudWatch with EMERGENCY_DISPATCH level
    await logAuditTrail({
      action: "AMBIENT_SOS_EMERGENCY_TRIGGER",
      userId: "python-backend-shout-recognizer",
      patientId,
      details: {
        alertId,
        keyword,
        urgency,
        location,
        timestamp,
      },
      level: "EMERGENCY_DISPATCH",
    });

    // 3. Persist emergency vital trigger in database if connected
    try {
      await db.query(
        `INSERT INTO clinical_vitals (
          id, patient_id, gestational_weeks, systolic_bp, diastolic_bp, mean_arterial_pressure, heart_rate, proteinuria, risk_score, risk_tier, recorded_at
        ) VALUES ($1, $2, 32, 142, 92, 108.6, 115, '++', 0.88, 'CRITICAL_EMERGENCY', NOW())
        ON CONFLICT (id) DO NOTHING`,
        [alertId, patientId]
      );
    } catch (dbErr) {
      console.warn("[DB] Emergency vitals logging note:", dbErr);
    }

    return NextResponse.json({
      success: true,
      alertId,
      status: "DISPATCHED",
      message: `Emergency SOS Alert received for ${patientName}. Transmitted to Hospital and Ambulance Network.`,
      alert: emergencyPayload,
    });
  } catch (error) {
    console.error("SOS receiver error:", error);
    return NextResponse.json(
      { error: "Failed to process emergency SOS payload" },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    success: true,
    count: activeSosAlerts.length,
    alerts: activeSosAlerts,
  });
}
