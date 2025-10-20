#!/bin/bash
set -e

# Configuration
STAGE=${1:-dev}
REGION=${2:-us-west-2}
ACCOUNT_ID=${3}
PROFILE=${4}

if [ -z "$ACCOUNT_ID" ] || [ -z "$PROFILE" ]; then
    echo "Usage: ./deploy_and_validate.sh <stage> <region> <account_id> <profile>"
    echo "Example: ./deploy_and_validate.sh dev us-west-2 123456789012 pipeline-profile"
    exit 1
fi

echo "🚀 Deploying Infrastructure for Stage: $STAGE"
echo "Region: $REGION, Account: $ACCOUNT_ID, Profile: $PROFILE"

# Deploy infrastructure
echo "📦 Deploying CDK stack..."
cdk deploy --profile $PROFILE --require-approval never

# Wait for deployment to settle
echo "⏳ Waiting for deployment to settle (30 seconds)..."
sleep 30

# Run validation
echo "🔍 Running infrastructure validation..."
python3 scripts/validate_infrastructure.py $STAGE $REGION $ACCOUNT_ID

echo "✅ Infrastructure deployment and validation complete!"