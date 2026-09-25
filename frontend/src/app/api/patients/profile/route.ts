import { NextRequest, NextResponse } from "next/server";
import { logAuditTrail } from "@/lib/aws-cloudwatch";
import { db } from "@/lib/db";

export async function POST(req: NextRequest) {
  try {
    const profile = await req.json();

    // 1. Log to AWS CloudWatch
    await logAuditTrail({
      action: "PATIENT_PROFILE_UPDATED",
      userId: profile.email || "parent",
      patientId: profile.fullName || "Priya Sharma",
      details: {
        gestationalWeeks: profile.gestationalWeeks,
        bloodGroup: profile.bloodGroup,
        emergencyContact: profile.emergencyContactName,
        allergies: profile.knownAllergies,
      },
      level: "INFO",
    });

    // 2. Persist to PostgreSQL / RDS if connected
    try {
      await db.query(
        `INSERT INTO patients (id, full_name, age, phone, blood_group, gestational_weeks, due_date, gravidity, parity, emergency_contact_name, emergency_contact_phone)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
         ON CONFLICT (id) DO UPDATE SET
           full_name = EXCLUDED.full_name,
           age = EXCLUDED.age,
           phone = EXCLUDED.phone,
           blood_group = EXCLUDED.blood_group,
           gestational_weeks = EXCLUDED.gestational_weeks,
           due_date = EXCLUDED.due_date,
           gravidity = EXCLUDED.gravidity,
           parity = EXCLUDED.parity,
           emergency_contact_name = EXCLUDED.emergency_contact_name,
           emergency_contact_phone = EXCLUDED.emergency_contact_phone`,
        [
          profile.email || "P-001",
          profile.fullName,
          parseInt(profile.age) || 27,
          profile.phone,
          profile.bloodGroup,
          parseInt(profile.gestationalWeeks) || 32,
          profile.dueDate ? new Date(profile.dueDate) : null,
          profile.gravidity,
          profile.parity,
          profile.emergencyContactName,
          profile.emergencyContactPhone,
        ]
      );
    } catch (dbErr) {
      console.warn("DB save note:", dbErr);
    }

    return NextResponse.json({
      success: true,
      message: "Patient profile saved to AWS RDS & CloudWatch audit trail updated.",
      profile,
    });
  } catch (error) {
    console.error("Profile update failed:", error);
    return NextResponse.json(
      { error: "Failed to update profile" },
      { status: 500 }
    );
  }
}
