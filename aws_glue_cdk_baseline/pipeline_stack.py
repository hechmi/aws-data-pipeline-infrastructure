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
 
# TODO: Replace these placeholders with your actual values
GITHUB_REPO = "YOUR_GITHUB_USERNAME/YOUR_INFRASTRUCTURE_REPO_NAME"
GITHUB_BRANCH = "main"
GITHUB_CONNECTION_ARN = "arn:aws:codeconnections:YOUR_REGION:YOUR_PIPELINE_ACCOUNT:connection/YOUR_CONNECTION_ID"

# Test automatic triggering
 
class PipelineStack(Stack):
 
    def __init__(self, scope: Construct, construct_id: str, config: Dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
 
        source = CodePipelineSource.connection(
            GITHUB_REPO,
            GITHUB_BRANCH,
            connection_arn=GITHUB_CONNECTION_ARN,
            trigger_on_push=True  # Enable automatic triggering on commits
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
        
        pipeline.add_stage(dev_stage)

        # Add production stage with manual approval
        prod_stage = DeploymentStage(self, "ProdStage", config=config, stage="prod", 
            env=cdk.Environment(
                account=str(config['prodAccount']['awsAccountId']),
                region=config['prodAccount']['awsRegion']
            ))
        
        pipeline.add_stage(prod_stage, 
            pre=[ManualApprovalStep("ApproveProduction")])