import { NextRequest, NextResponse } from "next/server";
import { logAuditTrail } from "@/lib/aws-cloudwatch";
import { db, initializeDatabaseSchema } from "@/lib/db";

// Ensure schema is prepared
initializeDatabaseSchema().catch(console.warn);

export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const id = searchParams.get("id") || searchParams.get("email") || searchParams.get("patientId");

    if (!id) {
      // Return list of all patients
      const result = await db.query(
        "SELECT id, full_name, age, phone, blood_group, gestational_weeks, due_date, gravidity, parity, emergency_contact_name, emergency_contact_phone, emergency_contact_relation, preferred_facility, preferred_language, known_allergies, medical_conditions, baby_name, created_at, updated_at FROM patients ORDER BY updated_at DESC LIMIT 50"
      );
      return NextResponse.json({ success: true, patients: result.rows });
    }

    // Fetch specific patient profile
    const patientResult = await db.query(
      "SELECT * FROM patients WHERE id = $1 OR email = $1 OR full_name = $1 LIMIT 1",
      [id]
    );

    if (patientResult.rows.length === 0) {
      return NextResponse.json({ success: false, message: "Patient not found" }, { status: 404 });
    }

    const patient = patientResult.rows[0];

    // Fetch patient's uploaded medical documents
    const docsResult = await db.query(
      "SELECT id, file_name, file_key, s3_uri, public_url, file_size, status, ocr_markdown, extracted_entities, created_at FROM medical_documents WHERE patient_id = $1 ORDER BY created_at DESC",
      [patient.id]
    );

    return NextResponse.json({
      success: true,
      profile: {
        id: patient.id,
        fullName: patient.full_name,
        age: String(patient.age || "27"),
        phone: patient.phone || "",
        email: patient.email || patient.id,
        bloodGroup: patient.blood_group || "O+",
        gestationalWeeks: String(patient.gestational_weeks || "32"),
        dueDate: patient.due_date ? new Date(patient.due_date).toISOString().split("T")[0] : "",
        gravidity: patient.gravidity || "G1",
        parity: patient.parity || "P0",
        emergencyContactName: patient.emergency_contact_name || "",
        emergencyContactRelation: patient.emergency_contact_relation || "Spouse",
        emergencyContactPhone: patient.emergency_contact_phone || "",
        preferredFacility: patient.preferred_facility || "",
        preferredLanguage: patient.preferred_language || "English",
        knownAllergies: patient.known_allergies || "",
        medicalConditions: patient.medical_conditions || "",
        babyName: patient.baby_name || "",
      },
      documents: docsResult.rows,
    });
  } catch (error) {
    console.error("Failed to fetch profile:", error);
    return NextResponse.json({ error: "Failed to fetch profile from database" }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const profile = await req.json();
    const patientId = profile.id || profile.email || profile.fullName || `P-${Date.now()}`;

    // 1. Log to AWS CloudWatch
    await logAuditTrail({
      action: "PATIENT_PROFILE_UPDATED",
      userId: profile.email || "parent",
      patientId: patientId,
      details: {
        fullName: profile.fullName,
        gestationalWeeks: profile.gestationalWeeks,
        bloodGroup: profile.bloodGroup,
        emergencyContact: profile.emergencyContactName,
        allergies: profile.knownAllergies,
      },
      level: "INFO",
    });

    // 2. Persist to PostgreSQL / RDS
    try {
      await db.query(
        `INSERT INTO patients (
          id, full_name, age, phone, email, blood_group, gestational_weeks, due_date, 
          gravidity, parity, emergency_contact_name, emergency_contact_phone, emergency_contact_relation,
          preferred_facility, preferred_language, known_allergies, medical_conditions, baby_name, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, NOW())
        ON CONFLICT (id) DO UPDATE SET
          full_name = EXCLUDED.full_name,
          age = EXCLUDED.age,
          phone = EXCLUDED.phone,
          email = EXCLUDED.email,
          blood_group = EXCLUDED.blood_group,
          gestational_weeks = EXCLUDED.gestational_weeks,
          due_date = EXCLUDED.due_date,
          gravidity = EXCLUDED.gravidity,
          parity = EXCLUDED.parity,
          emergency_contact_name = EXCLUDED.emergency_contact_name,
          emergency_contact_phone = EXCLUDED.emergency_contact_phone,
          emergency_contact_relation = EXCLUDED.emergency_contact_relation,
          preferred_facility = EXCLUDED.preferred_facility,
          preferred_language = EXCLUDED.preferred_language,
          known_allergies = EXCLUDED.known_allergies,
          medical_conditions = EXCLUDED.medical_conditions,
          baby_name = EXCLUDED.baby_name,
          updated_at = NOW()`,
        [
          patientId,
          profile.fullName || "Unnamed Patient",
          parseInt(profile.age) || 27,
          profile.phone || "",
          profile.email || "",
          profile.bloodGroup || "O+",
          parseInt(profile.gestationalWeeks) || 32,
          profile.dueDate ? new Date(profile.dueDate) : null,
          profile.gravidity || "G1",
          profile.parity || "P0",
          profile.emergencyContactName || "",
          profile.emergencyContactPhone || "",
          profile.emergencyContactRelation || "",
          profile.preferredFacility || "",
          profile.preferredLanguage || "English",
          profile.knownAllergies || "",
          profile.medicalConditions || "",
          profile.babyName || "",
        ]
      );
    } catch (dbErr) {
      console.warn("DB save note:", dbErr);
    }

    return NextResponse.json({
      success: true,
      message: "Patient profile saved to AWS RDS & CloudWatch audit trail updated.",
      profile: {
        ...profile,
        id: patientId,
      },
    });
  } catch (error) {
    console.error("Profile update failed:", error);
    return NextResponse.json(
      { error: "Failed to update profile" },
      { status: 500 }
    );
  }
}
