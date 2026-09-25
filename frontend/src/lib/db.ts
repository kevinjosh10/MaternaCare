import { Pool } from "pg";

const globalForPg = globalThis as unknown as { pool: Pool };

export const db =
  globalForPg.pool ||
  new Pool({
    connectionString:
      process.env.DATABASE_URL ||
      "postgresql://maternacare_admin:MaternaCare2026Secure!@localhost:5432/maternacare_db",
    ssl: process.env.DATABASE_URL?.includes("rds.amazonaws.com")
      ? { rejectUnauthorized: false }
      : undefined,
  });

if (process.env.NODE_ENV !== "production") globalForPg.pool = db;

/**
 * Initializes database tables and schema migrations for MaternaCare
 */
export async function initializeDatabaseSchema() {
  const schemaQuery = `
    CREATE TABLE IF NOT EXISTS patients (
      id VARCHAR(128) PRIMARY KEY,
      full_name VARCHAR(255) NOT NULL,
      age INTEGER NOT NULL DEFAULT 25,
      phone VARCHAR(64),
      email VARCHAR(255),
      blood_group VARCHAR(10) DEFAULT 'O+',
      gestational_weeks INTEGER DEFAULT 12,
      due_date DATE,
      gravidity VARCHAR(10) DEFAULT 'G1',
      parity VARCHAR(10) DEFAULT 'P0',
      emergency_contact_name VARCHAR(255),
      emergency_contact_phone VARCHAR(64),
      emergency_contact_relation VARCHAR(64),
      preferred_facility VARCHAR(255),
      preferred_language VARCHAR(128),
      known_allergies TEXT,
      medical_conditions TEXT,
      baby_name VARCHAR(255),
      created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
      updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    ALTER TABLE patients ADD COLUMN IF NOT EXISTS email VARCHAR(255);
    ALTER TABLE patients ADD COLUMN IF NOT EXISTS emergency_contact_relation VARCHAR(64);
    ALTER TABLE patients ADD COLUMN IF NOT EXISTS preferred_facility VARCHAR(255);
    ALTER TABLE patients ADD COLUMN IF NOT EXISTS preferred_language VARCHAR(128);
    ALTER TABLE patients ADD COLUMN IF NOT EXISTS known_allergies TEXT;
    ALTER TABLE patients ADD COLUMN IF NOT EXISTS medical_conditions TEXT;
    ALTER TABLE patients ADD COLUMN IF NOT EXISTS baby_name VARCHAR(255);
    ALTER TABLE patients ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

    CREATE TABLE IF NOT EXISTS medical_documents (
      id VARCHAR(128) PRIMARY KEY,
      patient_id VARCHAR(128) REFERENCES patients(id) ON DELETE CASCADE,
      file_name VARCHAR(255) NOT NULL,
      file_key VARCHAR(512) NOT NULL,
      s3_uri VARCHAR(512) NOT NULL,
      public_url VARCHAR(1024),
      file_size INTEGER,
      status VARCHAR(32) DEFAULT 'VERIFIED',
      ocr_markdown TEXT,
      extracted_entities JSONB,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    ALTER TABLE medical_documents ADD COLUMN IF NOT EXISTS file_name VARCHAR(255);
    ALTER TABLE medical_documents ADD COLUMN IF NOT EXISTS public_url VARCHAR(1024);
    ALTER TABLE medical_documents ADD COLUMN IF NOT EXISTS file_size INTEGER;
    ALTER TABLE medical_documents ADD COLUMN IF NOT EXISTS extracted_entities JSONB;

    CREATE TABLE IF NOT EXISTS clinical_vitals (
      id VARCHAR(128) PRIMARY KEY,
      patient_id VARCHAR(128) REFERENCES patients(id) ON DELETE CASCADE,
      gestational_weeks INTEGER NOT NULL,
      systolic_bp INTEGER NOT NULL,
      diastolic_bp INTEGER NOT NULL,
      mean_arterial_pressure NUMERIC,
      heart_rate INTEGER,
      proteinuria VARCHAR(10),
      risk_score NUMERIC,
      risk_tier VARCHAR(32),
      recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
  `;

  try {
    await db.query(schemaQuery);
    console.log("[DB] Schema initialized & migrated successfully");
  } catch (error) {
    console.warn("[DB] Schema initialization note:", error);
  }
}
