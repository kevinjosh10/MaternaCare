import { NextRequest, NextResponse } from "next/server";
import { uploadMedicalDocument } from "@/lib/aws-s3";
import { extractMedicalDocumentWithJina } from "@/lib/jina-ocr";
import { logAuditTrail } from "@/lib/aws-cloudwatch";

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get("file") as File | null;
    const patientId = (formData.get("patientId") as string) || "P-001";
    const userId = (formData.get("userId") as string) || "admin";

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 });
    }

    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    // 1. Upload to Amazon S3
    const s3Result = await uploadMedicalDocument(
      buffer,
      file.name,
      file.type,
      patientId
    );

    // 2. Perform OCR with Jina OCR v1
    const ocrResult = await extractMedicalDocumentWithJina(
      buffer,
      file.name,
      file.type
    );

    // 3. Log Audit Trail to AWS CloudWatch
    await logAuditTrail({
      action: "DOCUMENT_UPLOAD_AND_OCR",
      userId,
      patientId,
      details: {
        fileName: file.name,
        fileSize: file.size,
        s3Uri: s3Result.s3Uri,
        extractedFieldsCount: Object.keys(ocrResult.extractedEntities).length,
      },
      level: "INFO",
    });

    return NextResponse.json({
      success: true,
      fileKey: s3Result.fileKey,
      s3Uri: s3Result.s3Uri,
      publicUrl: s3Result.publicUrl,
      ocrMarkdown: ocrResult.markdown,
      extractedEntities: ocrResult.extractedEntities,
    });
  } catch (error) {
    console.error("Document upload & OCR failed:", error);
    return NextResponse.json(
      { error: "Failed to process medical document on AWS S3 & Jina OCR" },
      { status: 500 }
    );
  }
}
