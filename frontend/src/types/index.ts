export type UserRole = "clinician" | "parent" | "ambulance";
export type AuthMode = "login" | "signup";

export interface ParentProfile {
  id?: string;
  fullName: string;
  age: string;
  phone: string;
  email: string;
  bloodGroup: string;
  gestationalWeeks: string;
  dueDate: string;
  gravidity: string;
  parity: string;
  emergencyContactName: string;
  emergencyContactRelation: string;
  emergencyContactPhone: string;
  preferredFacility: string;
  preferredLanguage: string;
  knownAllergies: string;
  medicalConditions: string;
  babyName: string;
}

export interface PatientDocument {
  id: string;
  file_name: string;
  file_key: string;
  s3_uri: string;
  public_url?: string;
  file_size?: number;
  status?: string;
  ocr_markdown?: string;
  extracted_entities?: {
    previousComplications?: string[];
    allergies?: string[];
    pastSurgeries?: string[];
    detectedVitals?: Record<string, string>;
  };
  created_at?: string;
}

export interface UploadedDocumentResult {
  fileKey: string;
  s3Uri: string;
  publicUrl: string;
  ocrMarkdown: string;
  extractedEntities: {
    previousComplications?: string[];
    allergies?: string[];
    pastSurgeries?: string[];
    detectedVitals?: Record<string, string>;
  };
  documentId?: string;
  fileName?: string;
  fileSize?: number;
  createdAt?: string;
}

export interface AwsServiceStatus {
  s3Bucket: string;
  database: string;
  cloudwatchLogGroup: string;
  ocrEngine: string;
}
