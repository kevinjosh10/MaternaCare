# MaternaCare — 100% Free-Tier AWS Cloud Architecture & AWS CLI Plan

This plan is optimized specifically for **Zero Cloud Costs ($0.00 / month)** by utilizing **Vercel** for frontend and serverless API hosting, and strictly **100% Free-Tier AWS Services** for database, file storage, logging, and container registry.

---

## 🏗️ 1. Cost-Optimized Free Architecture

```text
[ React / Next.js App + Serverless Backend (Vercel - 100% Free) ]
                           │
   ┌───────────────────────┼─────────────────────────┬─────────────────────────┐
   ▼                       ▼                         ▼                         ▼
[ Amazon S3 ]      [ Amazon RDS ]           [ CloudWatch Logs ]       [ Amazon ECR ]
(Medical Records & (PostgreSQL db.t3.micro  (Centralized Audit &      (Container Image
 Processed OCR)     750 hrs/month Free)      App Logs - 5GB Free)      Registry - 500MB)
   │                       │                         │
   └───────────────────────┴─────────────────────────┘
                           │
                           ▼
          [ Jina OCR v1 (Hugging Face / API) ]
```

---

## 💰 2. Free Tier Guarantee Breakdown

| Service | Free Tier Allowance | Our Usage | Cost |
| :--- | :--- | :--- | :--- |
| **Vercel** | Unlimited deployments & serverless API routes | App hosting & API handlers | **$0.00** |
| **Amazon S3** | 5 GB Standard Storage + 20,000 GET / 2,000 PUT requests | Patient scans, PDFs, OCR output | **$0.00** |
| **Amazon RDS (Postgres)** | 750 hours/month on `db.t3.micro` or `db.t4g.micro` | Patient Health Memory & Referrals | **$0.00** |
| **Amazon CloudWatch** | 5 GB Log ingestion & metric monitoring | Application & audit logging | **$0.00** |
| **Amazon ECR** | 500 MB private container storage | Storing microservice Docker images | **$0.00** |
| **Jina OCR v1** | Free community/tier extraction credits | Document to Markdown OCR | **$0.00** |
| **Total Estimated Cost**| | | **$0.00 / mo** |

---

## 🚀 3. AWS CLI Commands (Copy-Paste Ready)

### Step 1: Set Project Variables in Terminal

```bash
export AWS_REGION="ap-south-1"  # or us-east-1
export PROJECT_NAME="maternacare"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

---

### Step 2: Create Amazon S3 Bucket for Medical Documents

```bash
# 1. Create S3 Storage Bucket
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

# 3. Block Unwanted Public Access
aws s3api put-public-access-block \
    --bucket "${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}" \
    --public-access-block-configuration '{
        "BlockPublicAcls": true,
        "IgnorePublicAcls": true,
        "BlockPublicPolicy": true,
        "RestrictPublicBuckets": true
    }'

# 4. Set CORS Policy (For direct uploads from Vercel)
aws s3api put-bucket-cors \
    --bucket "${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}" \
    --cors-configuration '{
        "CORSRules": [{
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "PUT", "POST", "HEAD"],
            "AllowedOrigins": ["*"],
            "ExposeHeaders": ["ETag"]
        }]
    }'
```

---

### Step 3: Provision Amazon RDS PostgreSQL Database (100% Free Tier)

```bash
# 1. Get Default VPC ID
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text)

# 2. Create Security Group for RDS
RDS_SG_ID=$(aws ec2 create-security-group \
    --group-name "${PROJECT_NAME}-rds-sg" \
    --description "Security group for MaternaCare PostgreSQL RDS instance" \
    --vpc-id ${VPC_ID} \
    --query "GroupId" --output text)

# 3. Allow Inbound PostgreSQL (Port 5432) from Anywhere for Vercel Serverless Connection
aws ec2 authorize-security-group-ingress \
    --group-id ${RDS_SG_ID} \
    --protocol tcp \
    --port 5432 \
    --cidr 0.0.0.0/0

# 4. Launch Free-Tier PostgreSQL Instance (db.t3.micro or db.t4g.micro)
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

### Step 4: Create CloudWatch Log Group for Application & Audit Logs

```bash
# Create dedicated log stream for Vercel backend logs & triage audit trail
aws logs create-log-group \
    --log-group-name "/maternacare/application-logs" \
    --region ${AWS_REGION}
```

---

### Step 5: Create Amazon ECR (Elastic Container Registry)

```bash
# Create free 500MB private repository for microservice / model containers
aws ecr create-repository \
    --repository-name "${PROJECT_NAME}-backend" \
    --image-scanning-configuration scanOnPush=true \
    --region ${AWS_REGION}
```

---

### Step 6: Create an IAM User for Vercel Integration

Create a programmatic IAM user with access keys to allow Vercel to read/write to S3, RDS, and CloudWatch:

```bash
# 1. Create IAM User
aws iam create-user --user-name "${PROJECT_NAME}-vercel-app"

# 2. Attach S3 & CloudWatch Policy
aws iam put-user-policy \
    --user-name "${PROJECT_NAME}-vercel-app" \
    --policy-name "${PROJECT_NAME}-vercel-policy" \
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
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "logs:DescribeLogStreams"
                ],
                "Resource": "arn:aws:logs:'"${AWS_REGION}"':'"${AWS_ACCOUNT_ID}"':log-group:/maternacare/application-logs:*"
            }
        ]
    }'

# 3. Generate Access Key for Vercel Environment Variables
aws iam create-access-key --user-name "${PROJECT_NAME}-vercel-app"
```

---

## 🔑 4. Vercel Environment Variables Configuration

In your **Vercel Project Settings &rarr; Environment Variables**, add these keys:

```ini
# AWS S3 Storage & Credentials
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=<YOUR_IAM_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<YOUR_IAM_SECRET_ACCESS_KEY>
S3_BUCKET_NAME=maternacare-storage-<YOUR_ACCOUNT_ID>

# Amazon RDS PostgreSQL Connection String
DATABASE_URL=postgresql://maternacare_admin:StrongPassword123@<RDS_ENDPOINT_ADDRESS>:5432/maternacare_db

# Document AI & Services
JINA_API_KEY=your_jina_key_here
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
```

---

## 🔍 5. Verification Commands via AWS CLI

```bash
# 1. Get RDS Endpoint Address (Paste into DATABASE_URL)
aws rds describe-db-instances \
    --db-instance-identifier "${PROJECT_NAME}-db" \
    --query "DBInstances[0].[DBInstanceStatus,Endpoint.Address]" \
    --output table

# 2. Test S3 Bucket Listing
aws s3 ls "s3://${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}"

# 3. View Live CloudWatch Logs
aws logs tail "/maternacare/application-logs" --follow
```

---

## 🧹 6. Teardown / Cleanup Commands (Post-Demo)

```bash
# 1. Delete RDS Database
aws rds delete-db-instance --db-instance-identifier "${PROJECT_NAME}-db" --skip-final-snapshot

# 2. Empty & Delete S3 Bucket
aws s3 rm "s3://${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}" --recursive
aws s3api delete-bucket --bucket "${PROJECT_NAME}-storage-${AWS_ACCOUNT_ID}"

# 3. Delete CloudWatch Log Group & ECR
aws logs delete-log-group --log-group-name "/maternacare/application-logs"
aws ecr delete-repository --repository-name "${PROJECT_NAME}-backend" --force

# 4. Delete IAM User
aws iam delete-user-policy --user-name "${PROJECT_NAME}-vercel-app" --policy-name "${PROJECT_NAME}-vercel-policy"
aws iam delete-access-key --user-name "${PROJECT_NAME}-vercel-app" --access-key-id <KEY_ID>
aws iam delete-user --user-name "${PROJECT_NAME}-vercel-app"
```
