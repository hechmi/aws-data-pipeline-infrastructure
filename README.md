# AWS Glue Pipeline Infrastructure

This repository contains the infrastructure code for an AWS Glue data pipeline using AWS CDK v2 and CodePipeline.

## 🏗️ Architecture

This infrastructure template creates a multi-account AWS Glue data pipeline with:

- **Pipeline Account**: Hosts the CI/CD pipelines
- **Dev Account**: Development environment for testing
- **Prod Account**: Production environment for live data processing

## 📦 What Gets Deployed

### Infrastructure Resources
- **S3 Buckets**: Input, output, and assets buckets
- **IAM Roles**: Cross-account roles and service permissions
- **Lambda Functions**: Event-driven triggers for Glue jobs
- **Glue Database**: Data catalog for metadata management
- **EventBridge Rules**: S3 event notifications

### CI/CD Pipeline
- **CodePipeline**: Automated deployment pipeline
- **CodeBuild**: Build and test automation
- **Cross-Account Deployment**: Automatic deployment to dev and prod accounts

## 🚀 Quick Start

**⚠️ IMPORTANT**: Before using this repository, you must customize it with your own AWS account numbers and GitHub connection.

### 1. Follow the Bootstrap Guide

This repository requires initial setup and configuration. Please follow the comprehensive setup guide:

**📖 [Developer Bootstrap Guide](./docs/DEVELOPER_BOOTSTRAP_GUIDE.md)**

The bootstrap guide will walk you through:
- Setting up your local environment
- Configuring AWS accounts and credentials
- Creating GitHub connections
- Updating configuration files
- Deploying the infrastructure

### 2. Required Customizations

Before deploying, you must update these files with your information:

#### `default-config.yaml`
```yaml
pipelineAccount:
  awsAccountId: YOUR_PIPELINE_ACCOUNT_ID  # Replace this
  awsRegion: YOUR_PREFERRED_REGION        # Replace this
```

#### `aws_glue_cdk_baseline/pipeline_stack.py`
```python
GITHUB_REPO = "YOUR_GITHUB_USERNAME/YOUR_INFRASTRUCTURE_REPO_NAME"  # Replace this
GITHUB_CONNECTION_ARN = "arn:aws:codeconnections:YOUR_REGION:YOUR_PIPELINE_ACCOUNT:connection/YOUR_CONNECTION_ID"  # Replace this
```

## 🔧 Local Development

### Prerequisites
- Python 3.9+
- AWS CLI configured
- AWS CDK v2
- Node.js (for CDK)

### Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install CDK
npm install -g aws-cdk
```

### Deploy
```bash
# Bootstrap CDK (first time only)
cdk bootstrap aws://YOUR_PIPELINE_ACCOUNT/YOUR_REGION --profile YOUR_PIPELINE_PROFILE

# Deploy infrastructure
cdk deploy --profile YOUR_PIPELINE_PROFILE
```

## 📁 Repository Structure

```
aws-glue-pipeline-infrastructure/
├── app.py                          # CDK app entry point
├── aws_glue_cdk_baseline/          # Infrastructure stacks
│   ├── deployment_stage.py         # Multi-account deployment stage
│   ├── infrastructure_stack.py     # Core infrastructure resources
│   └── pipeline_stack.py           # CI/CD pipeline definition
├── docs/                           # Documentation
│   ├── DEVELOPER_BOOTSTRAP_GUIDE.md # Complete setup guide
│   ├── AWS_Architecture_Documentation.md # Technical architecture
│   ├── ARCHITECTURE_DIAGRAMS.md    # Visual diagrams
│   └── generated-diagrams/         # PNG exports for presentations
├── default-config.yaml             # Configuration file (customize this)
├── requirements.txt                # Python dependencies
└── tests/                          # Unit and integration tests
```

## 🔄 CI/CD Pipeline

The pipeline automatically:
1. **Source**: Pulls code from your GitHub repository
2. **Build**: Runs CDK synth and tests
3. **Deploy Dev**: Deploys infrastructure to development account
4. **Deploy Prod**: Deploys to production (with manual approval)

## 🔐 Security

- Uses cross-account IAM roles for secure deployment
- Follows AWS security best practices
- Implements least-privilege access principles

## 📊 Monitoring

- CloudWatch logs for all components
- Pipeline execution monitoring
- Infrastructure drift detection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For setup help, see the [Developer Bootstrap Guide](./docs/DEVELOPER_BOOTSTRAP_GUIDE.md).

For issues or questions, please open a GitHub issue.