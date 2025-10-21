from typing import Dict
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_codebuild as codebuild
)
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, CodeBuildStep, ManualApprovalStep
from aws_glue_cdk_baseline.deployment_stage import DeploymentStage
 
GITHUB_REPO = "hechmi/aws-data-pipeline-infrastructure"
GITHUB_BRANCH = "main"
GITHUB_CONNECTION_ARN = "arn:aws:codeconnections:us-west-2:009507777973:connection/e2814821-01cb-4c90-8ba5-3df3093c31c0"

# Test automatic triggering
 
class PipelineStack(Stack):
 
    def __init__(self, scope: Construct, construct_id: str, config: Dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
 
        source = CodePipelineSource.connection(
            GITHUB_REPO,
            GITHUB_BRANCH,
            connection_arn=GITHUB_CONNECTION_ARN
        )
 
        pipeline = CodePipeline(self, "GluePipeline",
            pipeline_name="GlueInfraPipeline",
            cross_account_keys=True,
            docker_enabled_for_synth=True,
            synth=CodeBuildStep("CdkSynth",
                input=source,
                install_commands=[
                    "pip install -r requirements.txt",
                    "pip install -r requirements-dev.txt",
                    "npm install -g aws-cdk",
                ],
                commands=[
                    "cdk synth",
                ],
                build_environment=codebuild.BuildEnvironment(
                    build_image=codebuild.LinuxBuildImage.STANDARD_7_0
                )
            ),
            code_build_defaults={
                "build_environment": codebuild.BuildEnvironment(
                    build_image=codebuild.LinuxBuildImage.STANDARD_7_0
                )
            }
        )
 
        # Add development stage
        dev_stage = DeploymentStage(self, "DevStage", config=config, stage="dev", 
            env=cdk.Environment(
                account=str(config['devAccount']['awsAccountId']),
                region=config['devAccount']['awsRegion']
            ))
        
        # Add validation step after dev deployment
        dev_validation = CodeBuildStep("ValidateDevInfra",
            install_commands=[
                "pip install boto3"
            ],
            commands=[
                "echo 'Validating Dev Infrastructure...'",
                "chmod +x scripts/validate_infrastructure.py",
                # Use cross-account role to access dev account
                f"aws sts assume-role --role-arn arn:aws:iam::{config['devAccount']['awsAccountId']}:role/cdk-hnb659fds-cfn-exec-role-{config['devAccount']['awsAccountId']}-{config['devAccount']['awsRegion']} --role-session-name ValidationSession > /tmp/creds.json",
                "export AWS_ACCESS_KEY_ID=$(cat /tmp/creds.json | python3 -c \"import sys, json; print(json.load(sys.stdin)['Credentials']['AccessKeyId'])\")",
                "export AWS_SECRET_ACCESS_KEY=$(cat /tmp/creds.json | python3 -c \"import sys, json; print(json.load(sys.stdin)['Credentials']['SecretAccessKey'])\")",
                "export AWS_SESSION_TOKEN=$(cat /tmp/creds.json | python3 -c \"import sys, json; print(json.load(sys.stdin)['Credentials']['SessionToken'])\")",
                f"python3 scripts/validate_infrastructure.py dev {config['devAccount']['awsRegion']} {config['devAccount']['awsAccountId']}"
            ],
            build_environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_7_0
            ),
            role_policy_statements=[
                iam.PolicyStatement(
                    actions=[
                        "sts:AssumeRole"
                    ],
                    resources=[
                        f"arn:aws:iam::{config['devAccount']['awsAccountId']}:role/cdk-hnb659fds-cfn-exec-role-{config['devAccount']['awsAccountId']}-{config['devAccount']['awsRegion']}"
                    ]
                )
            ]
        )
        
        pipeline.add_stage(dev_stage, post=[dev_validation])

        # Add production stage with manual approval
        prod_stage = DeploymentStage(self, "ProdStage", config=config, stage="prod", 
            env=cdk.Environment(
                account=str(config['prodAccount']['awsAccountId']),
                region=config['prodAccount']['awsRegion']
            ))
        
        # Add validation step after prod deployment
        prod_validation = CodeBuildStep("ValidateProdInfra",
            install_commands=[
                "pip install boto3"
            ],
            commands=[
                "echo 'Validating Prod Infrastructure...'",
                "chmod +x scripts/validate_infrastructure.py",
                # Use cross-account role to access prod account
                f"aws sts assume-role --role-arn arn:aws:iam::{config['prodAccount']['awsAccountId']}:role/cdk-hnb659fds-cfn-exec-role-{config['prodAccount']['awsAccountId']}-{config['prodAccount']['awsRegion']} --role-session-name ValidationSession > /tmp/creds.json",
                "export AWS_ACCESS_KEY_ID=$(cat /tmp/creds.json | python3 -c \"import sys, json; print(json.load(sys.stdin)['Credentials']['AccessKeyId'])\")",
                "export AWS_SECRET_ACCESS_KEY=$(cat /tmp/creds.json | python3 -c \"import sys, json; print(json.load(sys.stdin)['Credentials']['SecretAccessKey'])\")",
                "export AWS_SESSION_TOKEN=$(cat /tmp/creds.json | python3 -c \"import sys, json; print(json.load(sys.stdin)['Credentials']['SessionToken'])\")",
                f"python3 scripts/validate_infrastructure.py prod {config['prodAccount']['awsRegion']} {config['prodAccount']['awsAccountId']}"
            ],
            build_environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_7_0
            ),
            role_policy_statements=[
                iam.PolicyStatement(
                    actions=[
                        "sts:AssumeRole"
                    ],
                    resources=[
                        f"arn:aws:iam::{config['prodAccount']['awsAccountId']}:role/cdk-hnb659fds-cfn-exec-role-{config['prodAccount']['awsAccountId']}-{config['prodAccount']['awsRegion']}"
                    ]
                )
            ]
        )
        
        pipeline.add_stage(prod_stage, 
            pre=[ManualApprovalStep("ApproveProduction")],
            post=[prod_validation])