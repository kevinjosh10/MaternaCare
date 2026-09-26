import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { logAuditTrail } from "@/lib/aws-cloudwatch";

export async function DELETE(
  req: NextRequest,
  context: { params: Promise<{ id: string }> }
) {
  try {
    const { id: docId } = await context.params;
    if (!docId) {
      return NextResponse.json({ error: "Missing document ID" }, { status: 400 });
    }

    await db.query("DELETE FROM medical_documents WHERE id = $1", [docId]);

    await logAuditTrail({
      action: "DOCUMENT_DELETED",
      userId: "parent",
      patientId: "priya.sharma@example.com",
      details: { docId },
      level: "WARN",
    });

    return NextResponse.json({ success: true });
  } catch (err) {
    console.error("[Delete Document Error]", err);
    return NextResponse.json({ error: "Failed to delete document" }, { status: 500 });
  }
}
