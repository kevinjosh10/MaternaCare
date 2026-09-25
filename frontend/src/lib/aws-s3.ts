import { S3Client, PutObjectCommand, GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

export const s3Client = new S3Client({
  region: process.env.AWS_REGION || "ap-south-1",
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || "",
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || "",
  },
});

export const S3_BUCKET_NAME = process.env.S3_BUCKET_NAME || "maternacare-storage-100403449729";

/**
 * Uploads a medical document buffer to Amazon S3
 */
export async function uploadMedicalDocument(
  fileBuffer: Buffer,
  fileName: string,
  contentType: string,
  patientId: string
) {
  const fileKey = `patients/${patientId}/documents/${Date.now()}-${fileName}`;

  const command = new PutObjectCommand({
    Bucket: S3_BUCKET_NAME,
    Key: fileKey,
    Body: fileBuffer,
    ContentType: contentType,
    Metadata: {
      patientId,
      uploadedAt: new Date().toISOString(),
    },
  });

  await s3Client.send(command);

  return {
    fileKey,
    s3Uri: `s3://${S3_BUCKET_NAME}/${fileKey}`,
    publicUrl: `https://${S3_BUCKET_NAME}.s3.${process.env.AWS_REGION || "ap-south-1"}.amazonaws.com/${fileKey}`,
  };
}

/**
 * Generates a temporary pre-signed URL for secure viewing
 */
export async function getDocumentPresignedUrl(fileKey: string, expiresInSeconds = 3600) {
  const command = new GetObjectCommand({
    Bucket: S3_BUCKET_NAME,
    Key: fileKey,
  });

  return await getSignedUrl(s3Client, command, { expiresIn: expiresInSeconds });
}
