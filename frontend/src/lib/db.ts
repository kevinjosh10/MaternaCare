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
 * Initializes database tables for MaternaCare
 */
export async function initializeDatabaseSchema() {
  const schemaQuery = `
    CREATE TABLE IF NOT EXISTS patients (
      id VARCHAR(64) PRIMARY KEY,
      full_name VARCHAR(255) NOT NULL,
      age INTEGER NOT NULL,
      phone VARCHAR(64),
      blood_group VARCHAR(10),
      gestational_weeks INTEGER,
      due_date DATE,
      gravidity VARCHAR(10),
      parity VARCHAR(10),
      emergency_contact_name VARCHAR(255),
      emergency_contact_phone VARCHAR(64),
      created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS medical_documents (
      id VARCHAR(64) PRIMARY KEY,
      patient_id VARCHAR(64) REFERENCES patients(id),
      file_key VARCHAR(512) NOT NULL,
      s3_uri VARCHAR(512) NOT NULL,
      status VARCHAR(32) DEFAULT 'PENDING_VERIFICATION',
      ocr_markdown TEXT,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS clinical_vitals (
      id VARCHAR(64) PRIMARY KEY,
      patient_id VARCHAR(64) REFERENCES patients(id),
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
    console.log("[DB] Schema initialized successfully");
  } catch (error) {
    console.warn("[DB] Schema initialization error (will retry upon connection):", error);
  }
}
