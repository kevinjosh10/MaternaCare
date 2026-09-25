# MaternaCare — AWS Cloud Architecture & AWS CLI Implementation Plan

This document outlines the complete step-by-step implementation plan for deploying the **MaternaCare** backend, Document AI pipeline, PostgreSQL database, and machine learning inference services on **Amazon Web Services (AWS)** using the **AWS CLI**.

---

## 🏗️ 1. Architecture Overview on AWS

```text
[ React Frontend (Vercel) ]
             │
             ▼ (HTTPS API Requests)
[ AWS Application Load Balancer / ECS Fargate (FastAPI) ]
             │
   ┌─────────┼─────────────────────────┬─────────────────────────┐
   ▼         ▼                         ▼                         ▼
[ S3 Bucket ]   [ RDS PostgreSQL ]   [ Amazon Textract ]   [ Secrets Manager ]
(Medical Records) (Health Memory & Vitals) (Document OCR)    (API Keys / DB Secrets)
   │                                                             │
   ▼                                                             ▼
[ CloudWatch Logs & Monitoring ]                     [ Twilio & Maps Integration ]
```

---

## 📋 2. Prerequisites

1. **AWS CLI v2** installed and configured:
   ```bash
   aws configure
   # Enter AWS Access Key ID, Secret Access Key, Region (e.g., ap-south-1 or us-east-1), output (json)
   ```
2. **Docker** installed locally for building container images.
3. Verify your identity:
   ```bash
   aws sts get-caller-identity
   ```

---

## 🚀 3. Step-by-Step AWS CLI Implementation

---

### Step 1: Set Up Environment Variables

Set default project variables to make commands reusable:

```bash
# Set your preferred AWS Region and Project Name
export AWS_REGION="ap-south-1"
export PROJECT_NAME="maternacare"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

---

### Step 2: Create S3 Buckets for Medical Documents & Model Artifacts

Create secure S3 storage for patient medical records (PDFs/Images) and ML model artifacts:

```bash
# 1. Create S3 Bucket
aws s3api create-bucket \
    --bucket "${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}" \
    --region ${AWS_REGION} \
    --create-bucket-configuration LocationConstraint=${AWS_REGION}

# 2. Enable Server-Side Encryption (AES256)
aws s3api put-bucket-encryption \
    --bucket "${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}" \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }'

# 3. Block Public Access (HIPAA / Data Privacy compliance)
aws s3api put-public-access-block \
    --bucket "${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}" \
    --public-access-block-configuration '{
        "BlockPublicAcls": true,
        "IgnorePublicAcls": true,
        "BlockPublicPolicy": true,
        "RestrictPublicBuckets": true
    }'

# 4. Set CORS Policy (For secure direct uploads from Vercel frontend if needed)
aws s3api put-bucket-cors \
    --bucket "${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}" \
    --cors-configuration '{
        "CORSRules": [{
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "PUT", "POST"],
            "AllowedOrigins": ["*"],
            "ExposeHeaders": ["ETag"]
        }]
    }'
```

---

### Step 3: Create IAM Roles for ECS & Application Services

Create execution and task roles with least-privilege policies:

```bash
# 1. Create ECS Task Execution Role (Allows ECS to pull images and write logs)
aws iam create-role \
    --role-name "${PROJECT_NAME}-ecs-execution-role" \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "ecs-tasks.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }'

# Attach standard ECS execution policy
aws iam attach-role-policy \
    --role-name "${PROJECT_NAME}-ecs-execution-role" \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# 2. Create ECS Task Role (Permissions for running container: S3 + Textract)
aws iam create-role \
    --role-name "${PROJECT_NAME}-ecs-task-role" \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "ecs-tasks.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }'

# 3. Attach custom S3 & Textract Policy to Task Role
aws iam put-role-policy \
    --role-name "${PROJECT_NAME}-ecs-task-role" \
    --policy-name "${PROJECT_NAME}-task-policy" \
    --policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::'"${PROJECT_NAME}"'-storage-'${AWS_ACCOUNT_ID}'",
                    "arn:aws:s3:::'"${PROJECT_NAME}"'-storage-'${AWS_ACCOUNT_ID}'/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "textract:DetectDocumentText",
                    "textract:AnalyzeDocument"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "secretsmanager:GetSecretValue"
                ],
                "Resource": "*"
            }
        ]
    }'
```

---

### Step 4: Configure AWS Secrets Manager

Store database credentials and external API tokens securely:

```bash
aws secretsmanager create-secret \
    --name "${PROJECT_NAME}/production/secrets" \
    --description "MaternaCare Production Secrets" \
    --secret-string '{
        "DATABASE_URL": "postgresql://maternacare_admin:StrongPassword123@<RDS_ENDPOINT>:5432/maternacare_db",
        "JWT_SECRET": "your-secure-random-jwt-key-for-auth",
        "TWILIO_ACCOUNT_SID": "your_twilio_sid",
        "TWILIO_AUTH_TOKEN": "your_twilio_token",
        "GOOGLE_MAPS_API_KEY": "your_google_maps_api_key",
        "JINA_API_KEY": "your_jina_key_if_used"
    }'
```

---

### Step 5: Provision Amazon RDS PostgreSQL Database

```bash
# 1. Create a Security Group for RDS
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text)

RDS_SG_ID=$(aws ec2 create-security-group \
    --group-name "${PROJECT_NAME}-rds-sg" \
    --description "Security group for MaternaCare PostgreSQL database" \
    --vpc-id ${VPC_ID} \
    --query "GroupId" --output text)

# 2. Allow Inbound PostgreSQL (Port 5432) from VPC
aws ec2 authorize-security-group-ingress \
    --group-id ${RDS_SG_ID} \
    --protocol tcp \
    --port 5432 \
    --cidr 0.0.0.0/0
    # Note: In strict production, restrict this CIDR to your ECS security group

# 3. Create the PostgreSQL Database Instance (Free-Tier Eligible db.t3.micro / db.t4g.micro)
aws rds create-db-instance \
    --db-instance-identifier "${PROJECT_NAME}-db" \
    --db-instance-class db.t4g.micro \
    --engine postgres \
    --engine-version 16.3 \
    --allocated-storage 20 \
    --master-username maternacare_admin \
    --master-user-password "StrongPassword123" \
    --db-name maternacare_db \
    --vpc-security-group-ids ${RDS_SG_ID} \
    --backup-retention-period 7 \
    --publicly-accessible \
    --no-multi-az
```

---

### Step 6: Create Amazon ECR Repository & Push Docker Image

```bash
# 1. Create ECR Repository
aws ecr create-repository \
    --repository-name "${PROJECT_NAME}-backend" \
    --image-scanning-configuration scanOnPush=true \
    --region ${AWS_REGION}

# 2. Authenticate Docker with ECR
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# 3. Build & Tag Docker Image
docker build -t ${PROJECT_NAME}-backend ./backend
docker tag ${PROJECT_NAME}-backend:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${PROJECT_NAME}-backend:latest

# 4. Push Image to ECR
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${PROJECT_NAME}-backend:latest
```

---

### Step 7: Create CloudWatch Log Group

```bash
aws logs create-log-group \
    --log-group-name "/ecs/${PROJECT_NAME}-backend" \
    --region ${AWS_REGION}
```

---

### Step 8: Deploy on Amazon ECS (Fargate)

```bash
# 1. Create ECS Cluster
aws ecs create-cluster \
    --cluster-name "${PROJECT_NAME}-cluster" \
    --region ${AWS_REGION}

# 2. Register ECS Task Definition
aws ecs register-task-definition \
    --family "${PROJECT_NAME}-backend-task" \
    --network-mode awsvpc \
    --requires-compatibilities FARGATE \
    --cpu "512" \
    --memory "1024" \
    --execution-role-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:role/${PROJECT_NAME}-ecs-execution-role" \
    --task-role-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:role/${PROJECT_NAME}-ecs-task-role" \
    --container-definitions '[
        {
            "name": "maternacare-backend",
            "image": "'"${AWS_ACCOUNT_ID}"'.dkr.ecr.'"${AWS_REGION}"'.amazonaws.com/'"${PROJECT_NAME}"'-backend:latest",
            "essential": true,
            "portMappings": [{
                "containerPort": 8000,
                "protocol": "tcp"
            }],
            "environment": [
                {"name": "AWS_REGION", "value": "'"${AWS_REGION}"'"},
                {"name": "S3_BUCKET_NAME", "value": "'"${PROJECT_NAME}"'-storage-'"${AWS_ACCOUNT_ID}"'"}
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/'"${PROJECT_NAME}"'-backend",
                    "awslogs-region": "'"${AWS_REGION}"'",
                    "awslogs-stream-prefix": "ecs"
                }
            }
        }
    ]'

# 3. Create Security Group for ECS Service
ECS_SG_ID=$(aws ec2 create-security-group \
    --group-name "${PROJECT_NAME}-ecs-sg" \
    --description "Security group for MaternaCare ECS tasks" \
    --vpc-id ${VPC_ID} \
    --query "GroupId" --output text)

# Allow Inbound Traffic on Port 8000
aws ec2 authorize-security-group-ingress \
    --group-id ${ECS_SG_ID} \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0

# 4. Get Default Subnet IDs
SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=${VPC_ID}" --query "Subnets[*].SubnetId" --output text | tr '\t' ',')

# 5. Run ECS Fargate Service
aws ecs create-service \
    --cluster "${PROJECT_NAME}-cluster" \
    --service-name "${PROJECT_NAME}-backend-service" \
    --task-definition "${PROJECT_NAME}-backend-task" \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[${SUBNET_IDS}],securityGroups=[${ECS_SG_ID}],assignPublicIp=ENABLED}"
```

---

## 🔍 4. Verification & Testing via AWS CLI

```bash
# 1. Check RDS Database Status
aws rds describe-db-instances \
    --db-instance-identifier "${PROJECT_NAME}-db" \
    --query "DBInstances[0].[DBInstanceStatus,Endpoint.Address]"

# 2. Check Running ECS Tasks & Public IP
TASK_ARN=$(aws ecs list-tasks --cluster "${PROJECT_NAME}-cluster" --query "taskArns[0]" --output text)
ENI_ID=$(aws ecs describe-tasks --cluster "${PROJECT_NAME}-cluster" --tasks ${TASK_ARN} --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" --output text)
PUBLIC_IP=$(aws ec2 describe-network-interfaces --network-interface-ids ${ENI_ID} --query "NetworkInterfaces[0].Association.PublicIp" --output text)

echo "Backend Live at: http://${PUBLIC_IP}:8000/docs"

# 3. Test Amazon Textract via CLI
aws textract detect-document-text \
    --document '{"S3Object":{"Bucket":"'"${PROJECT_NAME}"'-storage-'"${AWS_ACCOUNT_ID}"'","Name":"sample_prescription.pdf"}}'

# 4. View Live CloudWatch Logs
aws logs tail "/ecs/${PROJECT_NAME}-backend" --follow
```

---

## 🧹 5. Teardown & Cost Cleanup (Post-Hackathon)

To prevent unwanted cloud charges after the demo:

```bash
# 1. Delete ECS Service & Cluster
aws ecs update-service --cluster "${PROJECT_NAME}-cluster" --service "${PROJECT_NAME}-backend-service" --desired-count 0
aws ecs delete-service --cluster "${PROJECT_NAME}-cluster" --service "${PROJECT_NAME}-backend-service" --force
aws ecs delete-cluster --cluster "${PROJECT_NAME}-cluster"

# 2. Delete RDS Database Instance
aws rds delete-db-instance --db-instance-identifier "${PROJECT_NAME}-db" --skip-final-snapshot

# 3. Empty and Delete S3 Bucket
aws s3 rm "s3://${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}" --recursive
aws s3api delete-bucket --bucket "${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}"

# 4. Delete ECR Repository
aws ecr delete-repository --repository-name "${PROJECT_NAME}-backend" --force
```
