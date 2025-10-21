# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
# Test change to verify automatic pipeline triggering
from typing import Dict
from os import path
from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    Duration,
    aws_glue_alpha as glue,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_lambda as lambda_,
)
from constructs import Construct

class InfrastructureStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, config:Dict, stage:str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Cross-account role for pipeline access
        self.cross_account_role = self.create_cross_account_role(
            f"GlueCrossAccountRole-{stage}",
            str(config['pipelineAccount']['awsAccountId'])
        )

        # Create INPUT bucket
        self.input_bucket = s3.Bucket(self, f"InputBucket-{stage}",
            bucket_name=f"glue-input-{stage}-{config[f'{stage}Account']['awsAccountId']}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True,
            event_bridge_enabled=True
        )

        # Create OUTPUT bucket  
        self.output_bucket = s3.Bucket(self, f"OutputBucket-{stage}",
            bucket_name=f"glue-output-{stage}-{config[f'{stage}Account']['awsAccountId']}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True
        )

        # Create ASSETS bucket (for Glue scripts)
        self.assets_bucket = s3.Bucket(self, f"AssetsBucket-{stage}",
            bucket_name=f"glue-assets-v2-{stage}-{config[f'{stage}Account']['awsAccountId']}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Create Glue database
        self.glue_database = glue.Database(self, f"GlueDatabase-{stage}",
            database_name=f"glue_database_v2_{stage}"
        )

        # Role for Glue service operations with S3 access
        self.glue_service_role = iam.Role(self, "GlueServiceRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
            ],
            inline_policies={
                "S3Access": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "s3:GetObject",
                                "s3:PutObject",
                                "s3:DeleteObject", 
                                "s3:ListBucket"
                            ],
                            resources=[
                                # Input bucket permissions
                                self.input_bucket.bucket_arn,
                                f"{self.input_bucket.bucket_arn}/*",
                                # Output bucket permissions
                                self.output_bucket.bucket_arn,
                                f"{self.output_bucket.bucket_arn}/*",
                                # Assets bucket permissions
                                self.assets_bucket.bucket_arn,
                                f"{self.assets_bucket.bucket_arn}/*"
                            ]
                        )
                    ]
                )
            }
        )

        # Create Lambda function to trigger Glue job for CSV files
        self.trigger_lambda = lambda_.Function(self, f"GlueTriggerLambda-{stage}",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            timeout=Duration.seconds(30),  # Increase timeout for Glue job triggering
            code=lambda_.Code.from_inline(f"""
import json
import boto3
import urllib.parse

def handler(event, context):
    print(f"Received event: {{json.dumps(event)}}")
    
    glue = boto3.client('glue')
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        print(f"File uploaded: s3://{{bucket}}/{{key}}")
        
        # Only process CSV files
        if not key.lower().endswith('.csv'):
            print(f"Skipping non-CSV file: {{key}}")
            continue
        
        # Start Glue job to process the CSV file
        try:
            response = glue.start_job_run(
                JobName=f'FileProcessorV2-{stage}',
                Arguments={{
                    '--input_path': f's3://{{bucket}}/{{key}}',
                    '--output_path': f's3://glue-output-{stage}-{config[f'{stage}Account']['awsAccountId']}/',
                    '--database_name': f'glue_database_v2_{stage}'
                }}
            )
            print(f"Started CSV to Iceberg job: {{response['JobRunId']}} for file: {{key}}")
        except Exception as e:
            print(f"Failed to start Glue job for {{key}}: {{e}}")
    
    return {{'statusCode': 200, 'body': 'CSV processing triggered'}}
            """),
            environment={
                'STAGE': stage,
                'OUTPUT_BUCKET': f"glue-output-{stage}-{config[f'{stage}Account']['awsAccountId']}"
            }
        )

        # Add Glue permissions to Lambda role
        self.trigger_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "glue:StartJobRun",
                    "glue:GetJobRun",
                    "glue:GetJob"
                ],
                resources=[
                    f"arn:aws:glue:{self.region}:{self.account}:job/FileProcessorV2-{stage}"
                ]
            )
        )

        # INPUT bucket triggers Lambda on any file upload
        self.input_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(self.trigger_lambda)
        )

        # For integration test
        self.iam_role = iam.Role(self, "GlueTestRole",
            assumed_by=iam.ArnPrincipal(f"arn:aws:iam::{str(config['pipelineAccount']['awsAccountId'])}:root"),
            inline_policies={
                "GluePolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "glue:GetJobs",
                                "glue:GetJobRun",
                                "glue:GetTags",
                                "glue:StartJobRun"
                            ],
                            resources=[
                                "*"
                            ]
                        )
                    ]
                )
            }
        )

        # Export all bucket names and role ARN
        CfnOutput(self, f"InputBucketName-{stage}",
            value=self.input_bucket.bucket_name,
            export_name=f"InputBucket-{stage}"
        )

        CfnOutput(self, f"OutputBucketName-{stage}",
            value=self.output_bucket.bucket_name,
            export_name=f"OutputBucket-{stage}"
        )

        CfnOutput(self, f"AssetsBucketName-{stage}",
            value=self.assets_bucket.bucket_name,
            export_name=f"AssetsBucket-{stage}"
        )

        CfnOutput(self, f"GlueDatabaseName-{stage}",
            value=self.glue_database.database_name,
            export_name=f"GlueDatabase-{stage}"
        )

        CfnOutput(self, f"GlueJobRoleArn-{stage}",
            value=self.glue_service_role.role_arn,
            export_name=f"GlueJobRole-{stage}"
        )

        CfnOutput(self, f"TriggerLambdaName-{stage}",
            value=self.trigger_lambda.function_name,
            export_name=f"TriggerLambda-{stage}"
        )
    def create_cross_account_role(self, role_name: str, trusted_account_id: str):
        return iam.Role(self, f"{role_name}CrossAccountRole",
            assumed_by=iam.AccountPrincipal(trusted_account_id),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")]
        )
    @property
    def glue_service_role_arn(self):
        return self.glue_service_role.role_arn
    @property
    def cross_account_role_arn(self):
        return self.glue_app_stack.cross_account_role_arn