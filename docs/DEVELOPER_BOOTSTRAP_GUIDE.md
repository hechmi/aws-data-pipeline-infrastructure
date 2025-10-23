# AWS Glue Data Pipeline - Developer Bootstrap Guide

This guide helps you set up a complete AWS Glue data pipeline environment from scratch. You'll go from zero to a working demo in about 30-45 minutes.

## 🍴 Fork Repositories First

**IMPORTANT**: Before starting, you need to fork the repositories to your own GitHub account.

### 1. Fork the Infrastructure Repository

1. Go to: **[aws-glue-pipeline-infrastructure](https://github.com/YOUR_GITHUB_USERNAME/aws-glue-pipeline-infrastructure)**
2. Click the **"Fork"** button in the top-right corner
3. Select your GitHub account as the destination
4. **Optional**: Change the repository name if you prefer (e.g., `my-glue-infrastructure`)

### 2. Fork the Application Repository

1. Go to: **[aws-data-pipeline-applications](https://github.com/YOUR_GITHUB_USERNAME/aws-data-pipeline-applications)**
2. Click the **"Fork"** button in the top-right corner
3. Select your GitHub account as the destination
4. **Optional**: Change the repository name if you prefer (e.g., `my-glue-applications`)

### 3. Note Your Repository Names

After forking, note down your repository names and URLs. You'll need them for the variable configuration:
- Infrastructure repo: `https://github.com/YOUR_USERNAME/YOUR_INFRA_REPO_NAME`
- Application repo: `https://github.com/YOUR_USERNAME/YOUR_APP_REPO_NAME`

---

## 🔧 Variable Configuration

**IMPORTANT**: Before starting, customize these variables with your specific values. All commands in this guide use these variables.

### Required Variables

Copy and customize these variables in your terminal:

```bash
# ===== CUSTOMIZE THESE VALUES =====
export PIPELINE_ACCOUNT="YOUR_PIPELINE_ACCOUNT_ID"    # Replace with your pipeline account ID
export DEV_ACCOUNT="YOUR_DEV_ACCOUNT_ID"              # Replace with your dev account ID  
export PROD_ACCOUNT="YOUR_PROD_ACCOUNT_ID"            # Replace with your prod account ID
export AWS_REGION="YOUR_PREFERRED_REGION"             # Replace with your preferred region (e.g., us-west-2)
export GITHUB_USERNAME="YOUR_GITHUB_USERNAME"         # Replace with your GitHub username

# ===== REPOSITORY NAMES (customize if you renamed them) =====
export INFRA_REPO_NAME="aws-glue-pipeline-infrastructure"    # Change if you renamed the fork
export APP_REPO_NAME="aws-data-pipeline-applications"        # Change if you renamed the fork

# ===== AUTO-GENERATED VALUES =====
export REGION_SUFFIX="${AWS_REGION##*-}"  # Extracts 'west' from 'us-west-2'
export INFRA_REPO_URL="https://github.com/${GITHUB_USERNAME}/${INFRA_REPO_NAME}.git"
export APP_REPO_URL="https://github.com/${GITHUB_USERNAME}/${APP_REPO_NAME}.git"
export INPUT_BUCKET="glue-input-dev-${DEV_ACCOUNT}"
export OUTPUT_BUCKET="glue-output-dev-${DEV_ACCOUNT}"
```

### Variable Validation

Run these commands to verify your variables are set correctly:

```bash
# Check all variables are set
echo "Pipeline Account: $PIPELINE_ACCOUNT"
echo "Dev Account: $DEV_ACCOUNT" 
echo "Prod Account: $PROD_ACCOUNT"
echo "Region: $AWS_REGION"
echo "GitHub Username: $GITHUB_USERNAME"
echo "Infrastructure Repo: $INFRA_REPO_URL"
echo "Application Repo: $APP_REPO_URL"
echo "Input Bucket: $INPUT_BUCKET"
echo "Output Bucket: $OUTPUT_BUCKET"
```

### Example Configuration

Here's how the variables look when populated with example values:

```bash
# Example values (replace with your own)
export PIPELINE_ACCOUNT="123456789012"
export DEV_ACCOUNT="123456789013"
export PROD_ACCOUNT="123456789014"
export AWS_REGION="us-west-2"
export GITHUB_USERNAME="your-username"
```

---
## ⚡ Quick Start Checklist

**Total Time**: ~30-45 minutes

### Prerequisites ✅
- [ ] AWS account access with admin permissions for 3 accounts
- [ ] **GitHub account** - Create a free account at [GitHub.com](https://github.com) if you don't have one
- [ ] **Linux machine** (preferred) or macOS (for Windows users: [WSL2 Setup Guide](https://docs.microsoft.com/en-us/windows/wsl/install))
- [ ] Internet connection

### Setup Steps ⏱️
- [ ] **Fork Repositories** (2 min): Fork both repositories to your GitHub account
- [ ] **Variables** (2 min): Configure your account numbers and GitHub username
- [ ] **Local Environment** (10 min): Install Kiro IDE, AWS CLI, CDK, Python
- [ ] **AWS Keys** (5 min): Create access keys for all three AWS accounts
- [ ] **AWS Profiles** (5 min): Configure AWS CLI profiles for all accounts
- [ ] **Repositories** (3 min): Clone infrastructure and application repos
- [ ] **Configuration** (5 min): Update config files with your account numbers
- [ ] **GitHub Connection** (5 min): Create CodeStar connection and update pipeline code
- [ ] **Bootstrap** (10 min): CDK bootstrap all accounts
- [ ] **Deploy** (5 min): Deploy pipelines
- [ ] **Test Data Pipeline** (3 min): Upload CSV, verify Parquet output
- [ ] **Test CI/CD** (2 min): Make code change, verify pipeline triggers

---

## 🛠️ Local Environment Setup

### 1. Install Kiro IDE

Download and install **[Kiro IDE](https://kiro.ai)** from the official website. Once installed:

1. **Open Kiro IDE**
2. **Create New Workspace**: File → New Workspace
3. **Set Workspace Location**: Choose a directory for your AWS Glue projects

### 2. Install AWS CLI

**Installation Guide**: [AWS CLI Installation Instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

```bash
# Linux (Ubuntu/Debian)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Linux (using pip)
pip3 install awscli

# macOS (using Homebrew)
brew install awscli

# Windows (using MSI installer - see link above)

# Verify installation
aws --version
# Expected output: aws-cli/2.x.x Python/3.x.x
```

### 3. Install Python and Virtual Environment

```bash
# Linux (Ubuntu/Debian) - Install Python if not available
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Linux (CentOS/RHEL/Fedora)
sudo yum install python3 python3-pip

# macOS (Python should be pre-installed, or use Homebrew)
brew install python3

# Check Python version (3.9+ required)
python3 --version

# Create virtual environment for the project
python3 -m venv aws-glue-env

# Activate virtual environment
source aws-glue-env/bin/activate

# Verify activation (should show virtual env in prompt)
which python3
```

### 4. Install AWS CDK

**Installation Guide**: [AWS CDK Getting Started](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)

```bash
# Install Node.js (required for CDK)
# Linux (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Linux (CentOS/RHEL/Fedora)
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# macOS (using Homebrew)
brew install node

# Windows: Download from https://nodejs.org/

# Install CDK globally
npm install -g aws-cdk

# Verify installation
cdk --version
# Expected output: 2.x.x (build xxxxxx)
```

### 5. Configure Git

**GitHub Account**: Create a free account at [GitHub.com](https://github.com) to get started.

```bash
# Install Git (if not already installed)
# Linux (Ubuntu/Debian)
sudo apt install git

# Linux (CentOS/RHEL/Fedora)
sudo yum install git

# macOS (using Homebrew)
brew install git

# Set up Git (if not already configured)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

### Verification Commands

```bash
# Verify all tools are installed
echo "=== Tool Versions ==="
aws --version
python3 --version
node --version
npm --version
cdk --version
git --version

# Check virtual environment
echo "=== Python Environment ==="
which python3
echo $VIRTUAL_ENV
```

---

## 🔑 Create AWS Access Keys

Before configuring AWS CLI profiles, you need to create access keys for each AWS account.

### 1. Create Access Keys for Each Account

**AWS Documentation**: [Managing Access Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)

For **each of your 3 AWS accounts** (Pipeline, Dev, Prod), follow these steps:

1. **Sign in to AWS Console**: Go to [AWS Console](https://console.aws.amazon.com/)
2. **Navigate to IAM**: Search for "IAM" in the services menu
3. **Go to Users**: Click on "Users" in the left sidebar
4. **Select Your User**: Click on your IAM user (or create one if needed)
5. **Security Credentials Tab**: Click on the "Security credentials" tab
6. **Create Access Key**: Click "Create access key"
7. **Choose Use Case**: Select "Command Line Interface (CLI)"
8. **Download Keys**: Save the Access Key ID and Secret Access Key securely

### 2. Required Permissions

Each IAM user needs specific permissions for this AWS Glue pipeline setup. You have two options:

#### Option A: AdministratorAccess (Easiest)
For initial setup and learning:
1. **In IAM Users**: Select your user
2. **Permissions Tab**: Click "Add permissions"
3. **Attach Policies**: Search for "AdministratorAccess"
4. **Attach Policy**: Select and attach the policy

#### Option B: Specific Permissions (More Secure)
For production or security-conscious environments, create a custom policy with these permissions:

**Pipeline Account** needs:
- `iam:*` (for cross-account roles)
- `codepipeline:*`
- `codebuild:*`
- `codecommit:*` (if using CodeCommit)
- `s3:*` (for CDK assets)
- `cloudformation:*`
- `sts:AssumeRole`

**Dev/Prod Accounts** need:
- `glue:*`
- `s3:*`
- `lambda:*`
- `iam:*` (for service roles)
- `cloudformation:*`
- `logs:*`
- `events:*` (for EventBridge rules)

**Custom Policy Example**: [AWS Glue Service Permissions](https://docs.aws.amazon.com/glue/latest/dg/attach-policy-iam-user.html)

**Security Note**: Start with AdministratorAccess for setup, then restrict permissions later. See [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).

### 3. Organize Your Keys

Keep track of your access keys for each account:

```
Pipeline Account (YOUR_PIPELINE_ACCOUNT_ID):
- Access Key ID: AKIA...
- Secret Access Key: ...

Dev Account (YOUR_DEV_ACCOUNT_ID):
- Access Key ID: AKIA...
- Secret Access Key: ...

Prod Account (YOUR_PROD_ACCOUNT_ID):
- Access Key ID: AKIA...
- Secret Access Key: ...
```

---

## 🔐 AWS Account Configuration

### 1. AWS CLI Profile Setup

You need to configure AWS CLI profiles for all three accounts. Replace the account numbers with your actual values.

#### Option 1: Using AWS Configure Commands

```bash
# Configure pipeline account profile
aws configure set aws_access_key_id YOUR_PIPELINE_ACCESS_KEY --profile pipeline-${REGION_SUFFIX}
aws configure set aws_secret_access_key YOUR_PIPELINE_SECRET_KEY --profile pipeline-${REGION_SUFFIX}
aws configure set region ${AWS_REGION} --profile pipeline-${REGION_SUFFIX}
aws configure set output json --profile pipeline-${REGION_SUFFIX}

# Configure dev account profile
aws configure set aws_access_key_id YOUR_DEV_ACCESS_KEY --profile dev-${REGION_SUFFIX}
aws configure set aws_secret_access_key YOUR_DEV_SECRET_KEY --profile dev-${REGION_SUFFIX}
aws configure set region ${AWS_REGION} --profile dev-${REGION_SUFFIX}
aws configure set output json --profile dev-${REGION_SUFFIX}

# Configure prod account profile
aws configure set aws_access_key_id YOUR_PROD_ACCESS_KEY --profile prod-${REGION_SUFFIX}
aws configure set aws_secret_access_key YOUR_PROD_SECRET_KEY --profile prod-${REGION_SUFFIX}
aws configure set region ${AWS_REGION} --profile prod-${REGION_SUFFIX}
aws configure set output json --profile prod-${REGION_SUFFIX}
```

#### Option 2: Direct Config File Editing

Edit `~/.aws/config` file:

```ini
[profile pipeline-west]
region = us-west-2
output = json

[profile dev-west]
region = us-west-2
output = json

[profile prod-west]
region = us-west-2
output = json
```

Edit `~/.aws/credentials` file:

```ini
[pipeline-west]
aws_access_key_id = YOUR_PIPELINE_ACCESS_KEY
aws_secret_access_key = YOUR_PIPELINE_SECRET_KEY

[dev-west]
aws_access_key_id = YOUR_DEV_ACCESS_KEY
aws_secret_access_key = YOUR_DEV_SECRET_KEY

[prod-west]
aws_access_key_id = YOUR_PROD_ACCESS_KEY
aws_secret_access_key = YOUR_PROD_SECRET_KEY
```

#### Verify Profile Configuration

```bash
# List all configured profiles
aws configure list-profiles

# Check specific profile configuration
aws configure list --profile pipeline-${REGION_SUFFIX}
aws configure list --profile dev-${REGION_SUFFIX}
aws configure list --profile prod-${REGION_SUFFIX}
```

### 2. Verify AWS Account Access

```bash
# Test pipeline account access
aws sts get-caller-identity --profile pipeline-${REGION_SUFFIX}
# Expected output should show Account: ${PIPELINE_ACCOUNT}

# Test dev account access
aws sts get-caller-identity --profile dev-${REGION_SUFFIX}
# Expected output should show Account: ${DEV_ACCOUNT}

# Test prod account access
aws sts get-caller-identity --profile prod-${REGION_SUFFIX}
# Expected output should show Account: ${PROD_ACCOUNT}
```

### 3. Required Permissions

Each account needs the following permissions:
- **Pipeline Account**: AdministratorAccess (for deploying to other accounts)
- **Dev Account**: AdministratorAccess (for resource creation)
- **Prod Account**: AdministratorAccess (for resource creation)

### 4. Troubleshooting Authentication

**Problem**: `Unable to locate credentials`
```bash
# Solution: Check profile configuration
aws configure list --profile pipeline-${REGION_SUFFIX}
```

**Problem**: `Access Denied`
```bash
# Solution: Verify account permissions
aws iam get-user --profile pipeline-${REGION_SUFFIX}
```

**Problem**: `Invalid region`
```bash
# Solution: Check region configuration
aws configure get region --profile pipeline-${REGION_SUFFIX}
```

---##
 📁 Repository Setup

### 1. Clone Repositories

Clone both repositories to your local machine:

```bash
# Create project directory
mkdir aws-glue-pipeline-project
cd aws-glue-pipeline-project

# Clone infrastructure repository
git clone ${INFRA_REPO_URL}

# Clone application repository  
git clone ${APP_REPO_URL}

# Verify repositories were cloned
ls -la
# You should see:
# aws-glue-pipeline-infrastructure/
# aws-data-pipeline-applications/
```

### 2. Repository Structure

After cloning, your directory structure should look like:

```
aws-glue-pipeline-project/
├── aws-glue-pipeline-infrastructure/
│   ├── app.py                          # CDK app entry point
│   ├── aws_glue_cdk_baseline/          # Infrastructure stacks
│   ├── default-config.yaml             # Configuration file
│   └── requirements.txt                # Dependencies
└── aws-data-pipeline-applications/
    ├── app.py                          # CDK app entry point
    ├── aws_glue_applications/          # Application stacks
    ├── job_scripts/                    # Glue job scripts
    ├── default-config.yaml             # Configuration file
    └── requirements.txt                # Dependencies
```

### 3. Install Dependencies

Install Python dependencies for both repositories:

```bash
# Install infrastructure dependencies
cd aws-glue-pipeline-infrastructure
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install application dependencies
cd ../aws-data-pipeline-applications
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Return to project root
cd ..
```



### 5. Verify Repository Setup

```bash
# Check repository status
cd aws-glue-pipeline-infrastructure
git status
git remote -v

cd ../aws-data-pipeline-applications  
git status
git remote -v

# Verify dependencies are installed
python3 -c "import aws_cdk; print('CDK imported successfully')"
```

### 6. Making Changes and Committing

When you make changes to trigger pipelines:

```bash
# Example: Make a change to infrastructure
cd aws-glue-pipeline-infrastructure
echo "# Demo comment - $(date)" >> app.py

# Commit and push
git add app.py
git commit -m "Demo: Trigger infrastructure pipeline"
git push origin main
```

---## ⚙️ Conf
iguration Customization

### 1. Configuration Files Overview

Both repositories have `default-config.yaml` files that need to be updated with your account numbers:

- `aws-glue-pipeline-infrastructure/default-config.yaml`
- `aws-data-pipeline-applications/default-config.yaml`

### 2. Update Infrastructure Configuration

Edit `aws-glue-pipeline-infrastructure/default-config.yaml`:

```yaml
pipelineAccount:
  awsAccountId: ${PIPELINE_ACCOUNT}
  awsRegion: ${AWS_REGION}

devAccount:
  awsAccountId: ${DEV_ACCOUNT}
  awsRegion: ${AWS_REGION}

prodAccount:
  awsAccountId: ${PROD_ACCOUNT}
  awsRegion: ${AWS_REGION}

dev:
  jobs:
    ProcessLegislators:
      inputLocation: s3://awsglue-datasets/examples/us-legislators/all/persons.json

prod:
  jobs:
    ProcessLegislators:
      inputLocation: s3://awsglue-datasets/examples/us-legislators/all/persons.json
```

### 3. Update Application Configuration

Edit `aws-data-pipeline-applications/default-config.yaml`:

```yaml
pipelineAccount:
  awsAccountId: ${PIPELINE_ACCOUNT}
  awsRegion: ${AWS_REGION}

devAccount:
  awsAccountId: ${DEV_ACCOUNT}
  awsRegion: ${AWS_REGION}

prodAccount:
  awsAccountId: ${PROD_ACCOUNT}
  awsRegion: ${AWS_REGION}

# Application configuration
applications:
  dev:
    jobs:
      ProcessLegislators:
        inputLocation: "s3://awsglue-datasets/examples/us-legislators/all"
        outputLocation: "s3://glue-data-pipeline-dev-${DEV_ACCOUNT}/output/"
      FileProcessor:
        description: "Processes files uploaded to input bucket automatically"
  prod:
    jobs:
      ProcessLegislators:
        inputLocation: "s3://awsglue-datasets/examples/us-legislators/all"
        outputLocation: "s3://glue-data-pipeline-prod-${PROD_ACCOUNT}/output/"
      FileProcessor:
        description: "Processes files uploaded to input bucket automatically"
```

### 4. Configuration Update Commands

Use these commands to update the configuration files with your variables:

```bash
# Update infrastructure configuration
cd aws-glue-pipeline-infrastructure
sed -i.bak "s/YOUR_PIPELINE_ACCOUNT_ID/${PIPELINE_ACCOUNT}/g" default-config.yaml
sed -i.bak "s/YOUR_DEV_ACCOUNT_ID/${DEV_ACCOUNT}/g" default-config.yaml
sed -i.bak "s/YOUR_PROD_ACCOUNT_ID/${PROD_ACCOUNT}/g" default-config.yaml
sed -i.bak "s/us-west-2/${AWS_REGION}/g" default-config.yaml

# Update application configuration
cd ../aws-data-pipeline-applications
sed -i.bak "s/YOUR_PIPELINE_ACCOUNT_ID/${PIPELINE_ACCOUNT}/g" default-config.yaml
sed -i.bak "s/YOUR_DEV_ACCOUNT_ID/${DEV_ACCOUNT}/g" default-config.yaml
sed -i.bak "s/YOUR_PROD_ACCOUNT_ID/${PROD_ACCOUNT}/g" default-config.yaml
sed -i.bak "s/us-west-2/${AWS_REGION}/g" default-config.yaml

cd ..
```

### 5. Verify Configuration Changes

```bash
# Check infrastructure configuration
echo "=== Infrastructure Config ==="
grep -E "awsAccountId|awsRegion" aws-glue-pipeline-infrastructure/default-config.yaml

# Check application configuration  
echo "=== Application Config ==="
grep -E "awsAccountId|awsRegion" aws-data-pipeline-applications/default-config.yaml

# Verify account numbers match your variables
echo "Expected Pipeline Account: $PIPELINE_ACCOUNT"
echo "Expected Dev Account: $DEV_ACCOUNT"
echo "Expected Prod Account: $PROD_ACCOUNT"
echo "Expected Region: $AWS_REGION"
```

### 6. Resource Naming Convention

With your configuration, these resources will be created:

**S3 Buckets**:
- Input: `glue-input-dev-${DEV_ACCOUNT}`
- Output: `glue-output-dev-${DEV_ACCOUNT}`
- Assets: `glue-assets-v2-dev-${DEV_ACCOUNT}`

**Glue Jobs**:
- `FileProcessorV2-dev`
- `ProcessLegislators-dev`

**Lambda Functions**:
- `DevStage-Infrastructure-GlueTriggerLambda*`

**Pipelines**:
- `GlueInfraPipeline`
- `GlueAppPipeline`

### 7. Configuration Checklist

- [ ] Infrastructure `default-config.yaml` updated with your account numbers
- [ ] Application `default-config.yaml` updated with your account numbers
- [ ] All account IDs match your variables
- [ ] Region is set to your preferred region
- [ ] No syntax errors in YAML files

---

## ✅ Configuration Validation

After completing all the setup steps above, run this validation to ensure everything is configured correctly:

```bash
# Validate all variables are set
if [[ -z "$PIPELINE_ACCOUNT" || -z "$DEV_ACCOUNT" || -z "$PROD_ACCOUNT" || -z "$AWS_REGION" || -z "$GITHUB_USERNAME" ]]; then
    echo "❌ ERROR: Some variables are not set. Please check your configuration."
else
    echo "✅ All variables are configured"
    echo "Pipeline Account: $PIPELINE_ACCOUNT"
    echo "Dev Account: $DEV_ACCOUNT"
    echo "Prod Account: $PROD_ACCOUNT"
    echo "Region: $AWS_REGION"
    echo "GitHub Username: $GITHUB_USERNAME"
    echo "Infrastructure Repo: $INFRA_REPO_URL"
    echo "Application Repo: $APP_REPO_URL"
fi

# Validate AWS CLI profiles
echo "=== AWS CLI Profile Validation ==="
aws configure list --profile pipeline-${REGION_SUFFIX}
aws configure list --profile dev-${REGION_SUFFIX}
aws configure list --profile prod-${REGION_SUFFIX}

# Validate repository clones
echo "=== Repository Validation ==="
ls -la aws-glue-pipeline-infrastructure/ aws-data-pipeline-applications/

# Validate configuration files
echo "=== Configuration Files Validation ==="
grep -E "awsAccountId|awsRegion" aws-glue-pipeline-infrastructure/default-config.yaml
grep -E "awsAccountId|awsRegion" aws-data-pipeline-applications/default-config.yaml
```

**Expected Output**: 
- All variables should show your actual values, not placeholders
- AWS CLI profiles should show your configured regions and credentials
- Repository directories should exist
- Configuration files should show your account numbers

---

## 🔗 Create GitHub Connection

Before deploying the pipelines, you need to create a CodeStar connection to GitHub and update the pipeline code to use your repositories.

### 1. Create CodeStar Connection to GitHub

**AWS Documentation**: [CodeStar Connections](https://docs.aws.amazon.com/codepipeline/latest/userguide/connections-github.html)

1. **Sign in to Pipeline Account**: Use your pipeline account credentials
2. **Go to CodePipeline Console**: Navigate to [CodePipeline Console](https://console.aws.amazon.com/codesuite/codepipeline/)
3. **Settings → Connections**: Click on "Settings" in the left sidebar, then "Connections"
4. **Create Connection**: Click "Create connection"
5. **Select GitHub**: Choose "GitHub" as the provider
6. **Connection Name**: Enter a name like `github-connection`
7. **Connect to GitHub**: Click "Connect to GitHub"
8. **Authorize AWS**: Authorize AWS Connector for GitHub in the popup
9. **Complete Connection**: The connection status should show "Available"

### 2. Note Your Connection ARN

After creating the connection, copy the **Connection ARN**. It will look like:
```
arn:aws:codestar-connections:YOUR_REGION:YOUR_PIPELINE_ACCOUNT:connection/12345678-1234-1234-1234-123456789012
```

### 3. Update Pipeline Code with Your Connection

You need to update the pipeline stack code to use your GitHub connection and repositories.

#### Update Infrastructure Pipeline

Edit `aws-glue-pipeline-infrastructure/aws_glue_cdk_baseline/pipeline_stack.py`:

Find the constants at the top of the file and update them:

```python
# TODO: Replace these placeholders with your actual values
GITHUB_REPO = "YOUR_GITHUB_USERNAME/YOUR_INFRASTRUCTURE_REPO_NAME"  # Update this
GITHUB_BRANCH = "main"
GITHUB_CONNECTION_ARN = "arn:aws:codeconnections:YOUR_REGION:YOUR_PIPELINE_ACCOUNT:connection/YOUR_CONNECTION_ID"  # Update this
```

**Example**:
```python
GITHUB_REPO = "john-doe/my-glue-infrastructure"
GITHUB_BRANCH = "main"
GITHUB_CONNECTION_ARN = "arn:aws:codeconnections:us-west-2:123456789012:connection/12345678-1234-1234-1234-123456789012"
```

#### Update Application Pipeline

Edit `aws-data-pipeline-applications/aws_glue_applications/app_pipeline_stack.py`:

Find the constants at the top of the file and update them:

```python
# TODO: Replace these placeholders with your actual values
GITHUB_REPO = "YOUR_GITHUB_USERNAME/YOUR_APPLICATION_REPO_NAME"  # Update this
GITHUB_BRANCH = "main"
GITHUB_CONNECTION_ARN = "arn:aws:codeconnections:YOUR_REGION:YOUR_PIPELINE_ACCOUNT:connection/YOUR_CONNECTION_ID"  # Update this
```

**Example**:
```python
GITHUB_REPO = "john-doe/my-glue-applications"
GITHUB_BRANCH = "main"
GITHUB_CONNECTION_ARN = "arn:aws:codeconnections:us-west-2:123456789012:connection/12345678-1234-1234-1234-123456789012"
```

### 4. Commit and Push Changes

After updating both pipeline files:

```bash
# Update infrastructure pipeline
cd aws-glue-pipeline-infrastructure
git add aws_glue_cdk_baseline/pipeline_stack.py
git commit -m "Update pipeline to use personal GitHub connection"
git push origin main

# Update application pipeline
cd ../aws-data-pipeline-applications
git add aws_glue_applications/app_pipeline_stack.py
git commit -m "Update pipeline to use personal GitHub connection"
git push origin main
```

### 5. Verify Connection

```bash
# Check your connection in AWS CLI
aws codestar-connections list-connections --profile pipeline-${REGION_SUFFIX}
```

**Expected Output**: Your connection should show status "AVAILABLE"

---

## 🚀 Initial Deployment

### 1. CDK Bootstrap (Required First Step)

Bootstrap CDK in all three accounts. This creates the necessary infrastructure for CDK deployments.

```bash
# Bootstrap pipeline account
cdk bootstrap aws://${PIPELINE_ACCOUNT}/${AWS_REGION} --profile pipeline-${REGION_SUFFIX} \
    --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess

# Bootstrap dev account (with trust to pipeline account)
cdk bootstrap aws://${DEV_ACCOUNT}/${AWS_REGION} --profile dev-${REGION_SUFFIX} \
    --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess \
    --trust ${PIPELINE_ACCOUNT}

# Bootstrap prod account (with trust to pipeline account)  
cdk bootstrap aws://${PROD_ACCOUNT}/${AWS_REGION} --profile prod-${REGION_SUFFIX} \
    --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess \
    --trust ${PIPELINE_ACCOUNT}
```

**Expected Output**: Each bootstrap should complete with "✅ Environment aws://ACCOUNT/REGION bootstrapped"

### 2. Deploy Infrastructure Pipeline

Deploy the infrastructure pipeline first (creates S3 buckets, IAM roles, Lambda functions):

```bash
cd aws-glue-pipeline-infrastructure

# Deploy infrastructure pipeline
cdk deploy --profile pipeline-${REGION_SUFFIX}

# When prompted "Do you wish to deploy these changes (y/n)?" type: y
```

**Expected Duration**: ~5-8 minutes

**What Gets Created**:
- Infrastructure pipeline in pipeline account
- S3 buckets in dev and prod accounts
- IAM roles and policies
- Lambda trigger functions
- Glue databases

### 3. Deploy Application Pipeline

Deploy the application pipeline (creates Glue jobs):

```bash
cd ../aws-data-pipeline-applications

# Deploy application pipeline
cdk deploy --profile pipeline-${REGION_SUFFIX}

# When prompted "Do you wish to deploy these changes (y/n)?" type: y
```

**Expected Duration**: ~3-5 minutes

**What Gets Created**:
- Application pipeline in pipeline account
- Glue jobs in dev and prod accounts
- Job scripts uploaded to S3

### 4. Verify Deployments in AWS Console

#### Check Pipeline Account Resources

**CodePipeline Console**: 
```
https://${AWS_REGION}.console.aws.amazon.com/codesuite/codepipeline/pipelines
```

You should see:
- `GlueInfraPipeline` - Status: Succeeded
- `GlueAppPipeline` - Status: Succeeded

#### Check Dev Account Resources

**S3 Console**:
```
https://s3.console.aws.amazon.com/s3/buckets?region=${AWS_REGION}
```

You should see buckets:
- `glue-input-dev-${DEV_ACCOUNT}`
- `glue-output-dev-${DEV_ACCOUNT}`
- `glue-assets-v2-dev-${DEV_ACCOUNT}`

**Glue Console**:
```
https://${AWS_REGION}.console.aws.amazon.com/glue/home?region=${AWS_REGION}#/v2/etl-jobs
```

You should see jobs:
- `FileProcessorV2-dev`
- `ProcessLegislators-dev`

### 5. Verify Using CLI Commands

```bash
# Check pipeline status
aws codepipeline get-pipeline-state --name "GlueInfraPipeline" --profile pipeline-${REGION_SUFFIX} \
    --query 'stageStates[].{Stage:stageName,Status:latestExecution.status}' --output table

aws codepipeline get-pipeline-state --name "GlueAppPipeline" --profile pipeline-${REGION_SUFFIX} \
    --query 'stageStates[].{Stage:stageName,Status:latestExecution.status}' --output table

# Check S3 buckets
aws s3 ls --profile dev-${REGION_SUFFIX} | grep glue

# Check Glue jobs
aws glue get-jobs --profile dev-${REGION_SUFFIX} \
    --query 'Jobs[].Name' --output table
```

### 6. Troubleshooting Common Issues

**Problem**: `CDK bootstrap failed`
```bash
# Solution: Check AWS credentials and permissions
aws sts get-caller-identity --profile pipeline-${REGION_SUFFIX}
```

**Problem**: `Stack already exists`
```bash
# Solution: Check existing stacks
aws cloudformation list-stacks --profile pipeline-${REGION_SUFFIX} \
    --query 'StackSummaries[?StackStatus!=`DELETE_COMPLETE`].StackName'
```

**Problem**: `Access denied during deployment`
```bash
# Solution: Verify cross-account trust is set up
aws sts assume-role --role-arn arn:aws:iam::${DEV_ACCOUNT}:role/cdk-* \
    --role-session-name test --profile pipeline-${REGION_SUFFIX}
```

**Problem**: `Region mismatch errors`
```bash
# Solution: Verify all profiles use the same region
aws configure get region --profile pipeline-${REGION_SUFFIX}
aws configure get region --profile dev-${REGION_SUFFIX}
aws configure get region --profile prod-${REGION_SUFFIX}
```

### 7. Deployment Success Checklist

- [ ] CDK bootstrap completed for all 3 accounts
- [ ] Infrastructure pipeline deployed successfully
- [ ] Application pipeline deployed successfully
- [ ] Both pipelines show "Succeeded" status in AWS Console
- [ ] S3 buckets created in dev account
- [ ] Glue jobs created in dev account
- [ ] No error messages in CloudFormation stacks

---## 🧪 End-to-
End Testing

### 1. Create Test Data

Create a sample CSV file to test the data pipeline:

```bash
# Create test CSV file
cat > sales_data.csv << EOF
order_id,product_name,category,quantity,unit_price,total_amount,customer_name,order_date,region
ORD-001,Wireless Headphones,Electronics,2,99.99,199.98,John Smith,2024-10-20,North America
ORD-002,Coffee Maker,Appliances,1,149.50,149.50,Sarah Johnson,2024-10-21,Europe
ORD-003,Running Shoes,Sports,1,129.99,129.99,Mike Chen,2024-10-22,Asia Pacific
ORD-004,Laptop Stand,Office,3,45.00,135.00,Emma Davis,2024-10-23,North America
ORD-005,Bluetooth Speaker,Electronics,1,79.99,79.99,Alex Wilson,2024-10-23,Europe
EOF

# Verify file was created
ls -la sales_data.csv
cat sales_data.csv
```

### 2. Upload Test File to S3

```bash
# Upload CSV file to input bucket
aws s3 cp sales_data.csv s3://${INPUT_BUCKET}/ --profile dev-${REGION_SUFFIX}

# Verify upload
aws s3 ls s3://${INPUT_BUCKET}/ --profile dev-${REGION_SUFFIX}
```

**Expected Output**: You should see `sales_data.csv` listed in the bucket.

### 3. Monitor Lambda Trigger

The file upload automatically triggers a Lambda function. Check the logs:

```bash
# Find the Lambda function name
aws lambda list-functions --profile dev-${REGION_SUFFIX} \
    --query 'Functions[?contains(FunctionName, `GlueTrigger`)].FunctionName' --output text

# Get recent log events (replace FUNCTION_NAME with actual name from above)
aws logs describe-log-streams \
    --log-group-name "/aws/lambda/FUNCTION_NAME" \
    --profile dev-${REGION_SUFFIX} \
    --order-by LastEventTime --descending --max-items 1 \
    --query 'logStreams[0].logStreamName' --output text

# View log events (replace LOG_STREAM_NAME with output from above)
aws logs get-log-events \
    --log-group-name "/aws/lambda/FUNCTION_NAME" \
    --log-stream-name "LOG_STREAM_NAME" \
    --profile dev-${REGION_SUFFIX} \
    --query 'events[-5:].message' --output text
```

**Expected Output**: You should see messages like:
- "File uploaded: s3://INPUT_BUCKET/sales_data.csv"
- "Started CSV to Iceberg job: jr_xxxxx for file: sales_data.csv"

### 4. Monitor Glue Job Execution

```bash
# Check Glue job status
aws glue get-job-runs --job-name "FileProcessorV2-dev" --profile dev-${REGION_SUFFIX} \
    --max-results 1 \
    --query 'JobRuns[0].{Status:JobRunState,Started:StartedOn,Completed:CompletedOn,Duration:ExecutionTime}' \
    --output table

# Keep checking until status shows "SUCCEEDED" (usually takes 1-2 minutes)
```

**Expected Statuses**:
1. `STARTING` → `RUNNING` → `SUCCEEDED`
2. Duration: ~60-120 seconds

### 5. Verify Processed Output

```bash
# Check output bucket for processed files
aws s3 ls s3://${OUTPUT_BUCKET}/ --profile dev-${REGION_SUFFIX} --recursive

# You should see a folder like: sales_data_processed/
# Download the processed file
aws s3 cp s3://${OUTPUT_BUCKET}/sales_data_processed/ ./output/ --recursive --profile dev-${REGION_SUFFIX}

# List downloaded files
ls -la output/
```

**Expected Output**: 
- Folder: `sales_data_processed/`
- File: `part-00000-*.snappy.parquet`

### 6. Verify Data Transformation

If you have Python pandas installed, you can verify the processed data:

```bash
# Install pandas and pyarrow (if not already installed)
pip install pandas pyarrow

# Read and display the processed Parquet file
python3 -c "
import pandas as pd
import glob

# Find the parquet file
parquet_files = glob.glob('output/*.parquet')
if parquet_files:
    df = pd.read_parquet(parquet_files[0])
    print('📊 PROCESSED DATA:')
    print('=' * 50)
    print(df.to_string(index=False))
    print()
    print('📋 FILE INFO:')
    print(f'Rows: {len(df)}')
    print(f'Columns: {list(df.columns)}')
    print()
    print('🔍 METADATA COLUMNS ADDED:')
    for col in df.columns:
        if col not in ['order_id', 'product_name', 'category', 'quantity', 'unit_price', 'total_amount', 'customer_name', 'order_date', 'region']:
            print(f'  - {col}: {df[col].iloc[0]}')
else:
    print('No parquet files found')
"
```

**Expected Output**: 
- Original 9 columns + 3 metadata columns (processed_at, source_file, processing_job)
- Same 5 rows of data
- Metadata showing processing timestamp and job information

### 7. Clean Up Test Data

```bash
# Remove test files from S3 buckets
aws s3 rm s3://${INPUT_BUCKET}/sales_data.csv --profile dev-${REGION_SUFFIX}
aws s3 rm s3://${OUTPUT_BUCKET}/sales_data_processed/ --recursive --profile dev-${REGION_SUFFIX}

# Remove local files
rm -f sales_data.csv
rm -rf output/

# Verify cleanup
aws s3 ls s3://${INPUT_BUCKET}/ --profile dev-${REGION_SUFFIX}
aws s3 ls s3://${OUTPUT_BUCKET}/ --profile dev-${REGION_SUFFIX}
```

### 8. End-to-End Test Success Criteria

✅ **Test Passed If**:
- CSV file uploaded successfully to input bucket
- Lambda function triggered and started Glue job
- Glue job completed with "SUCCEEDED" status
- Processed Parquet file created in output bucket
- Output file contains original data + metadata columns
- All test data cleaned up successfully

❌ **Test Failed If**:
- File upload fails (check AWS credentials)
- Lambda doesn't trigger (check S3 event notifications)
- Glue job fails (check job logs in AWS Console)
- No output file created (check job configuration)
- Output file missing metadata (check job script)

---#
# 🔄 CI/CD Pipeline Testing

### 1. Test Infrastructure Pipeline

Trigger the infrastructure pipeline by making a code change:

```bash
cd aws-glue-pipeline-infrastructure

# Add a comment to trigger the pipeline
echo "# Demo comment added for pipeline demonstration - $(date)" >> app.py

# Commit and push the change
git add app.py
git commit -m "Demo: Trigger infrastructure pipeline"
git push origin main
```

### 2. Monitor Infrastructure Pipeline

```bash
# Check pipeline status
aws codepipeline get-pipeline-state --name "GlueInfraPipeline" --profile pipeline-${REGION_SUFFIX} \
    --query 'stageStates[].{Stage:stageName,Status:latestExecution.status}' --output table

# Get latest execution details
aws codepipeline list-pipeline-executions --pipeline-name "GlueInfraPipeline" --profile pipeline-${REGION_SUFFIX} \
    --max-items 1 \
    --query 'pipelineExecutionSummaries[0].{Status:status,StartTime:startTime,ExecutionId:pipelineExecutionId}' \
    --output table
```

**Expected Pipeline Stages**:
1. `Source` → `Succeeded` (pulls code from GitHub)
2. `Build` → `Succeeded` (CDK synth and validation)
3. `UpdatePipeline` → `Succeeded` (self-updating pipeline)
4. `Assets` → `Succeeded` (uploads CDK assets)
5. `DevStage` → `Succeeded` (deploys to dev account)
6. `ProdStage` → `Succeeded` (deploys to prod account)

**Expected Duration**: ~5-8 minutes

### 3. Test Application Pipeline

Trigger the application pipeline by making a change to the application code:

```bash
cd ../aws-data-pipeline-applications

# Add a comment to trigger the pipeline
echo "# Demo comment added for application pipeline demonstration - $(date)" >> app.py

# Commit and push the change
git add app.py
git commit -m "Demo: Trigger application pipeline"
git push origin main
```

### 4. Monitor Application Pipeline

```bash
# Check pipeline status
aws codepipeline get-pipeline-state --name "GlueAppPipeline" --profile pipeline-${REGION_SUFFIX} \
    --query 'stageStates[].{Stage:stageName,Status:latestExecution.status}' --output table

# Get latest execution details
aws codepipeline list-pipeline-executions --pipeline-name "GlueAppPipeline" --profile pipeline-${REGION_SUFFIX} \
    --max-items 1 \
    --query 'pipelineExecutionSummaries[0].{Status:status,StartTime:startTime,ExecutionId:pipelineExecutionId}' \
    --output table
```

**Expected Pipeline Stages**:
1. `Source` → `Succeeded` (pulls code from GitHub)
2. `Build` → `Succeeded` (CDK synth and validation)
3. `UpdatePipeline` → `Succeeded` (self-updating pipeline)
4. `Assets` → `Succeeded` (uploads job scripts)
5. `DevAppStage` → `Succeeded` (deploys jobs to dev)
6. `ProdAppStage` → `Succeeded` (deploys jobs to prod)

**Expected Duration**: ~3-5 minutes

### 5. View Pipelines in AWS Console

**Infrastructure Pipeline**:
```
https://${AWS_REGION}.console.aws.amazon.com/codesuite/codepipeline/pipelines/GlueInfraPipeline/view
```

**Application Pipeline**:
```
https://${AWS_REGION}.console.aws.amazon.com/codesuite/codepipeline/pipelines/GlueAppPipeline/view
```

### 6. Verify Deployments

After both pipelines complete, verify the deployments worked:

```bash
# Check that Glue jobs are still working after deployment
aws glue get-jobs --profile dev-${REGION_SUFFIX} \
    --query 'Jobs[].Name' --output table

# Check S3 buckets are still accessible
aws s3 ls s3://${INPUT_BUCKET} --profile dev-${REGION_SUFFIX}
aws s3 ls s3://${OUTPUT_BUCKET} --profile dev-${REGION_SUFFIX}

# Optionally: Run another end-to-end data test to confirm everything still works
```

### 7. Understanding the GitOps Workflow

**What Just Happened**:

1. **Code Change**: You modified `app.py` files
2. **Git Push**: Changes pushed to GitHub repositories
3. **Webhook Trigger**: GitHub webhooks automatically triggered pipelines
4. **Pipeline Execution**: AWS CodePipeline executed deployment stages
5. **Multi-Account Deployment**: Changes deployed to dev and prod accounts
6. **Self-Updating**: Pipelines can update themselves

**Key Benefits**:
- **Automated**: No manual deployment steps
- **Auditable**: All changes tracked in Git
- **Rollback**: Can revert to previous Git commits
- **Multi-Account**: Consistent deployment across environments
- **Self-Healing**: Pipelines update their own infrastructure

### 8. Troubleshooting Pipeline Issues

**Problem**: Pipeline doesn't trigger after git push
```bash
# Solution: Check GitHub webhook configuration
git log --oneline -1  # Should show your recent commit
```

**Problem**: Pipeline fails at Build stage
```bash
# Solution: Check build logs in CodeBuild
aws codebuild list-builds-for-project --project-name "GlueInfraPipeline-Build" --profile pipeline-${REGION_SUFFIX}
```

**Problem**: Pipeline fails at Deploy stage
```bash
# Solution: Check CloudFormation stack events
aws cloudformation describe-stack-events --stack-name "DevStage-Infrastructure" --profile dev-${REGION_SUFFIX}
```

**Problem**: Access denied errors
```bash
# Solution: Verify cross-account roles are working
aws sts get-caller-identity --profile pipeline-${REGION_SUFFIX}
```

### 9. CI/CD Test Success Criteria

✅ **Test Passed If**:
- Infrastructure pipeline triggered by code change
- All infrastructure pipeline stages succeeded
- Application pipeline triggered by code change  
- All application pipeline stages succeeded
- Resources still accessible after deployment
- No errors in CloudFormation stacks

❌ **Test Failed If**:
- Pipeline doesn't trigger (check GitHub webhooks)
- Build stage fails (check CDK syntax)
- Deploy stage fails (check permissions)
- Resources become inaccessible (check stack updates)

---## 
📚 Quick Reference

### Essential Commands

```bash
# === VARIABLE SETUP ===
export PIPELINE_ACCOUNT="YOUR_PIPELINE_ACCOUNT"
export DEV_ACCOUNT="YOUR_DEV_ACCOUNT"
export PROD_ACCOUNT="YOUR_PROD_ACCOUNT"
export AWS_REGION="us-west-2"
export GITHUB_USERNAME="YOUR_USERNAME"
export REGION_SUFFIX="${AWS_REGION##*-}"

# === AWS CLI VERIFICATION ===
aws sts get-caller-identity --profile pipeline-${REGION_SUFFIX}
aws sts get-caller-identity --profile dev-${REGION_SUFFIX}
aws sts get-caller-identity --profile prod-${REGION_SUFFIX}

# === CDK BOOTSTRAP ===
cdk bootstrap aws://${PIPELINE_ACCOUNT}/${AWS_REGION} --profile pipeline-${REGION_SUFFIX} --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess
cdk bootstrap aws://${DEV_ACCOUNT}/${AWS_REGION} --profile dev-${REGION_SUFFIX} --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess --trust ${PIPELINE_ACCOUNT}
cdk bootstrap aws://${PROD_ACCOUNT}/${AWS_REGION} --profile prod-${REGION_SUFFIX} --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess --trust ${PIPELINE_ACCOUNT}

# === DEPLOYMENT ===
cd aws-glue-pipeline-infrastructure && cdk deploy --profile pipeline-${REGION_SUFFIX}
cd ../aws-data-pipeline-applications && cdk deploy --profile pipeline-${REGION_SUFFIX}

# === DATA PIPELINE TEST ===
aws s3 cp test_file.csv s3://glue-input-dev-${DEV_ACCOUNT}/ --profile dev-${REGION_SUFFIX}
aws glue get-job-runs --job-name "FileProcessorV2-dev" --profile dev-${REGION_SUFFIX} --max-results 1
aws s3 ls s3://glue-output-dev-${DEV_ACCOUNT}/ --profile dev-${REGION_SUFFIX} --recursive

# === CI/CD PIPELINE TEST ===
git add . && git commit -m "Demo change" && git push origin main
aws codepipeline get-pipeline-state --name "GlueInfraPipeline" --profile pipeline-${REGION_SUFFIX}
aws codepipeline get-pipeline-state --name "GlueAppPipeline" --profile pipeline-${REGION_SUFFIX}

# === CLEANUP ===
aws s3 rm s3://glue-input-dev-${DEV_ACCOUNT}/ --recursive --profile dev-${REGION_SUFFIX}
aws s3 rm s3://glue-output-dev-${DEV_ACCOUNT}/ --recursive --profile dev-${REGION_SUFFIX}
```

### AWS Console URLs

Replace `${AWS_REGION}` with your region (e.g., `us-west-2`):

**Pipeline Account**:
- CodePipeline: `https://${AWS_REGION}.console.aws.amazon.com/codesuite/codepipeline/pipelines`
- CloudFormation: `https://${AWS_REGION}.console.aws.amazon.com/cloudformation/home`

**Dev Account**:
- S3 Buckets: `https://s3.console.aws.amazon.com/s3/buckets?region=${AWS_REGION}`
- Glue Jobs: `https://${AWS_REGION}.console.aws.amazon.com/glue/home#/v2/etl-jobs`
- Lambda Functions: `https://${AWS_REGION}.console.aws.amazon.com/lambda/home#/functions`
- CloudWatch Logs: `https://${AWS_REGION}.console.aws.amazon.com/cloudwatch/home#logsV2:log-groups`

### Resource Names Reference

**S3 Buckets**:
- Input: `glue-input-dev-${DEV_ACCOUNT}`
- Output: `glue-output-dev-${DEV_ACCOUNT}`
- Assets: `glue-assets-v2-dev-${DEV_ACCOUNT}`

**Glue Jobs**:
- `FileProcessorV2-dev`
- `ProcessLegislators-dev`

**Pipelines**:
- `GlueInfraPipeline`
- `GlueAppPipeline`

**Lambda Functions**:
- `DevStage-Infrastructure-GlueTriggerLambda*`

---

## 🔧 Troubleshooting

### Authentication Issues

**Problem**: `Unable to locate credentials`
```bash
# Check AWS CLI configuration
aws configure list --profile pipeline-${REGION_SUFFIX}
aws configure list --profile dev-${REGION_SUFFIX}
aws configure list --profile prod-${REGION_SUFFIX}

# Reconfigure if needed
aws configure --profile pipeline-${REGION_SUFFIX}
```

**Problem**: `Access Denied`
```bash
# Verify account access
aws sts get-caller-identity --profile pipeline-${REGION_SUFFIX}

# Check if you're using the right account
echo "Expected: ${PIPELINE_ACCOUNT}"
```

**Problem**: `Region not found`
```bash
# Check region configuration
aws configure get region --profile pipeline-${REGION_SUFFIX}

# Should match your AWS_REGION variable
echo "Expected: ${AWS_REGION}"
```

### CDK Bootstrap Issues

**Problem**: `Bootstrap stack already exists`
```bash
# Check existing bootstrap stacks
aws cloudformation list-stacks --profile pipeline-${REGION_SUFFIX} \
    --query 'StackSummaries[?contains(StackName, `CDKToolkit`)].{Name:StackName,Status:StackStatus}'

# If needed, delete and re-bootstrap
aws cloudformation delete-stack --stack-name CDKToolkit --profile pipeline-${REGION_SUFFIX}
```

**Problem**: `Trust relationship error`
```bash
# Verify trust relationship
aws sts assume-role \
    --role-arn arn:aws:iam::${DEV_ACCOUNT}:role/cdk-hnb659fds-deploy-role-${DEV_ACCOUNT}-${AWS_REGION} \
    --role-session-name test \
    --profile pipeline-${REGION_SUFFIX}
```

### Deployment Issues

**Problem**: `Stack update failed`
```bash
# Check CloudFormation events
aws cloudformation describe-stack-events \
    --stack-name InfraPipelineStack \
    --profile pipeline-${REGION_SUFFIX} \
    --query 'StackEvents[0:5].{Time:Timestamp,Status:ResourceStatus,Reason:ResourceStatusReason}'
```

**Problem**: `Resource already exists`
```bash
# Check for existing resources
aws s3 ls --profile dev-${REGION_SUFFIX} | grep glue
aws glue get-jobs --profile dev-${REGION_SUFFIX}
```

### Pipeline Issues

**Problem**: `Pipeline not triggering`
```bash
# Check recent commits
git log --oneline -5

# Check recent changes
git show --name-only

# Check pipeline exists
aws codepipeline get-pipeline --name "GlueInfraPipeline" --profile pipeline-${REGION_SUFFIX}
```

**Problem**: `Build stage failing`
```bash
# Check build logs
aws codebuild list-builds-for-project \
    --project-name "GlueInfraPipeline-Build" \
    --profile pipeline-${REGION_SUFFIX}

# Get build details
aws codebuild batch-get-builds \
    --ids "BUILD_ID_FROM_ABOVE" \
    --profile pipeline-${REGION_SUFFIX}
```

### Data Pipeline Issues

**Problem**: `Lambda not triggering`
```bash
# Check S3 event notifications
aws s3api get-bucket-notification-configuration \
    --bucket glue-input-dev-${DEV_ACCOUNT} \
    --profile dev-${REGION_SUFFIX}

# Check Lambda function exists
aws lambda list-functions --profile dev-${REGION_SUFFIX} \
    --query 'Functions[?contains(FunctionName, `GlueTrigger`)].FunctionName'
```

**Problem**: `Glue job failing`
```bash
# Check job run details
aws glue get-job-run \
    --job-name "FileProcessorV2-dev" \
    --run-id "JOB_RUN_ID" \
    --profile dev-${REGION_SUFFIX}

# Check job logs in CloudWatch
aws logs describe-log-groups \
    --log-group-name-prefix "/aws-glue/jobs" \
    --profile dev-${REGION_SUFFIX}
```

### Health Check Commands

```bash
# === SYSTEM HEALTH CHECK ===
echo "=== Tool Versions ==="
aws --version
cdk --version
python3 --version
git --version

echo "=== AWS Access ==="
aws sts get-caller-identity --profile pipeline-${REGION_SUFFIX} --query 'Account' --output text
aws sts get-caller-identity --profile dev-${REGION_SUFFIX} --query 'Account' --output text
aws sts get-caller-identity --profile prod-${REGION_SUFFIX} --query 'Account' --output text

echo "=== S3 Buckets ==="
aws s3 ls --profile dev-${REGION_SUFFIX} | grep glue

echo "=== Glue Jobs ==="
aws glue get-jobs --profile dev-${REGION_SUFFIX} --query 'Jobs[].Name' --output text

echo "=== Pipelines ==="
aws codepipeline list-pipelines --profile pipeline-${REGION_SUFFIX} --query 'pipelines[].name' --output text
```

### Getting Help

1. **AWS Documentation**: [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/)
2. **CDK Documentation**: [AWS CDK Developer Guide](https://docs.aws.amazon.com/cdk/)
3. **GitHub Issues**: Check repository issues for known problems
4. **AWS Support**: Use AWS Support if you have a support plan
5. **Community**: AWS re:Post community forums

---

## 🎉 Congratulations!

You've successfully set up a complete AWS Glue data pipeline with CI/CD! You now have:

✅ **Working Data Pipeline**: CSV files automatically processed to Parquet
✅ **GitOps Workflow**: Code changes trigger automated deployments  
✅ **Multi-Account Setup**: Separate dev and prod environments
✅ **Monitoring**: Full observability with CloudWatch logs
✅ **Scalable Architecture**: Serverless and event-driven

### Next Steps

1. **Customize Job Scripts**: Modify Glue jobs for your specific data processing needs
2. **Add More Environments**: Extend to staging or other environments
3. **Enhance Monitoring**: Add CloudWatch alarms and SNS notifications
4. **Security Hardening**: Implement least-privilege IAM policies
5. **Cost Optimization**: Set up S3 lifecycle policies and Glue job optimization

### Key Takeaways

- **Infrastructure as Code**: All resources defined in CDK
- **Event-Driven**: No manual intervention required for data processing
- **GitOps**: All changes tracked and deployed via Git
- **Multi-Account**: Production isolation and security
- **Serverless**: Pay only for what you use

### Final System Validation 🎯

Run these commands to verify your complete setup is working:

```bash
# All these should work without errors:
aws sts get-caller-identity --profile pipeline-${REGION_SUFFIX}
aws sts get-caller-identity --profile dev-${REGION_SUFFIX}
aws sts get-caller-identity --profile prod-${REGION_SUFFIX}
aws s3 ls s3://${INPUT_BUCKET} --profile dev-${REGION_SUFFIX}
aws s3 ls s3://${OUTPUT_BUCKET} --profile dev-${REGION_SUFFIX}
aws codepipeline get-pipeline-state --name "GlueInfraPipeline" --profile pipeline-${REGION_SUFFIX}
aws codepipeline get-pipeline-state --name "GlueAppPipeline" --profile pipeline-${REGION_SUFFIX}
```

**If all commands succeed**: 🎉 **Your setup is complete and working!**

Happy data processing! 🚀