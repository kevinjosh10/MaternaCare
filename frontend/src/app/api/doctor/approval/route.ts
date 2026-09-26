import { NextRequest, NextResponse } from "next/server";
import { logAuditTrail } from "@/lib/aws-cloudwatch";
import crypto from "crypto";

// In-memory persistent queue for Human-In-The-Loop approvals
export interface PendingApproval {
  id: string;
  patientId: string;
  patientName: string;
  gestationalWeeks: string;
  query: string;
  proposedAdvice: string;
  category: "MEDICATION" | "DIET_FOOD" | "CLINICAL_SYMPTOM" | "TRIAGE_ESCALATION";
  urgency: "HIGH" | "MEDIUM" | "ROUTINE";
  status: "PENDING_APPROVAL" | "APPROVED" | "REJECTED" | "MODIFIED";
  finalText?: string;
  reviewedBy?: string;
  createdAt: string;
  reviewedAt?: string;
}

export const globalApprovalsQueue: PendingApproval[] = [
  {
    id: "APP-1002",
    patientId: "priya.sharma@example.com",
    patientName: "Priya Sharma",
    gestationalWeeks: "32 Weeks",
    query: "Can I drink ginger and cinnamon tea for digestion?",
    proposedAdvice: "Mild ginger infusion is generally safe in moderation, but limit concentrated cinnamon supplements and ensure sodium restriction for blood pressure management.",
    category: "DIET_FOOD",
    urgency: "MEDIUM",
    status: "PENDING_APPROVAL",
    createdAt: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
  },
];

export async function GET() {
  return NextResponse.json({
    success: true,
    count: globalApprovalsQueue.length,
    pendingCount: globalApprovalsQueue.filter((a) => a.status === "PENDING_APPROVAL").length,
    approvals: globalApprovalsQueue,
  });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { approvalId, decision, editedText, reviewerName } = body;

    const approvalIndex = globalApprovalsQueue.findIndex((a) => a.id === approvalId);
    if (approvalIndex === -1) {
      return NextResponse.json({ error: "Approval request not found" }, { status: 404 });
    }

    const item = globalApprovalsQueue[approvalIndex];
    item.status = decision === "APPROVE" ? (editedText ? "MODIFIED" : "APPROVED") : "REJECTED";
    item.finalText = editedText || item.proposedAdvice;
    item.reviewedBy = reviewerName || "Dr. Ananya Sen (Lead Obstetrician)";
    item.reviewedAt = new Date().toISOString();

    await logAuditTrail({
      action: `DOCTOR_HITL_${decision}`,
      userId: item.reviewedBy,
      patientId: item.patientId,
      details: {
        approvalId: item.id,
        decision,
        finalText: item.finalText,
      },
      level: "INFO",
    });

    return NextResponse.json({
      success: true,
      message: `Recommendation ${item.status.toLowerCase()} successfully by ${item.reviewedBy}.`,
      approval: item,
    });
  } catch (error) {
    console.error("Doctor approval error:", error);
    return NextResponse.json({ error: "Failed to process doctor approval" }, { status: 500 });
  }
}
