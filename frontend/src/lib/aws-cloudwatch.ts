import {
  CloudWatchLogsClient,
  CreateLogStreamCommand,
  PutLogEventsCommand,
  DescribeLogStreamsCommand,
} from "@aws-sdk/client-cloudwatch-logs";

export const cloudwatchClient = new CloudWatchLogsClient({
  region: process.env.AWS_REGION || "ap-south-1",
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || "",
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || "",
  },
});

export const LOG_GROUP_NAME =
  process.env.CLOUDWATCH_LOG_GROUP || "/maternacare/application-logs";

/**
 * Sends structured clinical audit and system logs to AWS CloudWatch
 */
export async function logAuditTrail(event: {
  action: string;
  userId?: string;
  patientId?: string;
  details: Record<string, unknown>;
  level?: "INFO" | "WARN" | "ERROR" | "EMERGENCY_DISPATCH";
}) {
  const logStreamName = `audit-${new Date().toISOString().slice(0, 10)}`;

  try {
    // 1. Ensure log stream exists
    const describeStream = new DescribeLogStreamsCommand({
      logGroupName: LOG_GROUP_NAME,
      logStreamNamePrefix: logStreamName,
    });
    const streamInfo = await cloudwatchClient.send(describeStream);
    const streamExists = streamInfo.logStreams?.some(
      (s) => s.logStreamName === logStreamName
    );

    if (!streamExists) {
      await cloudwatchClient.send(
        new CreateLogStreamCommand({
          logGroupName: LOG_GROUP_NAME,
          logStreamName: logStreamName,
        })
      );
    }

    // 2. Put Log Event
    const payload = {
      timestamp: Date.now(),
      level: event.level || "INFO",
      action: event.action,
      userId: event.userId || "anonymous",
      patientId: event.patientId || "N/A",
      details: event.details,
    };

    const putCommand = new PutLogEventsCommand({
      logGroupName: LOG_GROUP_NAME,
      logStreamName: logStreamName,
      logEvents: [
        {
          timestamp: Date.now(),
          message: JSON.stringify(payload),
        },
      ],
    });

    await cloudwatchClient.send(putCommand);
  } catch (err) {
    // Fail-safe: Local fallback logging if CloudWatch is unavailable
    console.log("[AuditLog Fallback]", JSON.stringify(event), err);
  }
}
