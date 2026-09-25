import { NextResponse } from "next/server";
import { S3_BUCKET_NAME } from "@/lib/aws-s3";
import { LOG_GROUP_NAME } from "@/lib/aws-cloudwatch";

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    services: {
      awsRegion: process.env.AWS_REGION || "ap-south-1",
      s3Bucket: S3_BUCKET_NAME,
      cloudwatchLogGroup: LOG_GROUP_NAME,
      ocrEngine: "jina-ocr-v1",
      database: "Amazon RDS PostgreSQL 16 (Free Tier)",
    },
  });
}
