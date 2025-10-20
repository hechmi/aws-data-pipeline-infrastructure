#!/usr/bin/env python3
"""
Infrastructure validation script
Tests that all infrastructure components are deployed and working correctly
"""

import boto3
import json
import time
import sys
import uuid
from datetime import datetime

class InfrastructureValidator:
    def __init__(self, stage, region, account_id):
        self.stage = stage
        self.region = region
        self.account_id = account_id
        
        # AWS clients
        self.s3 = boto3.client('s3', region_name=region)
        self.cloudformation = boto3.client('cloudformation', region_name=region)
        self.logs = boto3.client('logs', region_name=region)
        self.glue = boto3.client('glue', region_name=region)
        
        # Expected resource names
        self.input_bucket = f"glue-input-{stage}-{account_id}"
        self.output_bucket = f"glue-output-{stage}-{account_id}"
        self.assets_bucket = f"glue-assets-{stage}-{account_id}"
        self.glue_database = f"glue_database_{stage}"
        
    def validate_buckets(self):
        """Test that all S3 buckets exist and are accessible"""
        print("🪣 Validating S3 Buckets...")
        
        buckets_to_check = [
            ("Input", self.input_bucket),
            ("Output", self.output_bucket), 
            ("Assets", self.assets_bucket)
        ]
        
        for bucket_type, bucket_name in buckets_to_check:
            try:
                self.s3.head_bucket(Bucket=bucket_name)
                print(f"  ✅ {bucket_type} bucket exists: {bucket_name}")
            except Exception as e:
                print(f"  ❌ {bucket_type} bucket missing: {bucket_name} - {e}")
                return False
        
        return True
    
    def validate_cloudformation_exports(self):
        """Test that CloudFormation exports are available"""
        print("📤 Validating CloudFormation Exports...")
        
        expected_exports = [
            f"InputBucket-{self.stage}",
            f"OutputBucket-{self.stage}",
            f"AssetsBucket-{self.stage}",
            f"GlueDatabase-{self.stage}",
            f"GlueJobRole-{self.stage}",
            f"TriggerLambda-{self.stage}"
        ]
        
        try:
            exports = self.cloudformation.list_exports()['Exports']
            export_names = [exp['Name'] for exp in exports]
            
            for export_name in expected_exports:
                if export_name in export_names:
                    print(f"  ✅ Export available: {export_name}")
                else:
                    print(f"  ❌ Export missing: {export_name}")
                    return False
            
            return True
        except Exception as e:
            print(f"  ❌ Failed to check exports: {e}")
            return False
    
    def validate_glue_database(self):
        """Test that Glue database exists"""
        print("🗄️  Validating Glue Database...")
        
        try:
            self.glue.get_database(Name=self.glue_database)
            print(f"  ✅ Glue database exists: {self.glue_database}")
            return True
        except Exception as e:
            print(f"  ❌ Glue database missing: {self.glue_database} - {e}")
            return False
    
    def test_s3_lambda_trigger(self):
        """Test that uploading to input bucket triggers Lambda"""
        print("🔄 Testing S3 → Lambda Trigger...")
        
        # Create test file
        test_key = f"test-{uuid.uuid4().hex[:8]}.json"
        test_content = json.dumps({
            "test": True,
            "timestamp": datetime.now().isoformat(),
            "message": "Infrastructure validation test"
        })
        
        try:
            # Upload test file to input bucket
            print(f"  📤 Uploading test file: s3://{self.input_bucket}/{test_key}")
            self.s3.put_object(
                Bucket=self.input_bucket,
                Key=test_key,
                Body=test_content,
                ContentType='application/json'
            )
            
            # Wait for Lambda to process
            print("  ⏳ Waiting for Lambda trigger (15 seconds)...")
            time.sleep(15)
            
            # Find Lambda function name by looking at exports
            try:
                exports = self.cloudformation.list_exports()['Exports']
                lambda_name = None
                for exp in exports:
                    if exp['Name'] == f"TriggerLambda-{self.stage}":
                        lambda_name = exp['Value']
                        break
                
                if not lambda_name:
                    print("  ❌ Could not find Lambda function name in exports")
                    return False
                
                log_group = f"/aws/lambda/{lambda_name}"
                print(f"  🔍 Checking logs in: {log_group}")
                
                # Get recent log streams
                streams = self.logs.describe_log_streams(
                    logGroupName=log_group,
                    orderBy='LastEventTime',
                    descending=True,
                    limit=5
                )
                
                # Check recent logs for our test file
                for stream in streams['logStreams']:
                    events = self.logs.get_log_events(
                        logGroupName=log_group,
                        logStreamName=stream['logStreamName'],
                        startTime=int((time.time() - 300) * 1000)  # Last 5 minutes
                    )
                    
                    for event in events['events']:
                        if test_key in event['message']:
                            print(f"  ✅ Lambda triggered successfully for: {test_key}")
                            
                            # Cleanup test file
                            self.s3.delete_object(Bucket=self.input_bucket, Key=test_key)
                            print(f"  🧹 Cleaned up test file")
                            return True
                
                print(f"  ❌ Lambda trigger not detected for: {test_key}")
                # Still cleanup the test file
                try:
                    self.s3.delete_object(Bucket=self.input_bucket, Key=test_key)
                    print(f"  🧹 Cleaned up test file")
                except:
                    pass
                return False
                
            except Exception as e:
                print(f"  ❌ Error checking Lambda logs: {e}")
                # Cleanup test file
                try:
                    self.s3.delete_object(Bucket=self.input_bucket, Key=test_key)
                except:
                    pass
                return False
            
        except Exception as e:
            print(f"  ❌ S3 trigger test failed: {e}")
            return False
    
    def run_all_validations(self):
        """Run all validation tests"""
        print(f"\n🔍 Validating Infrastructure for Stage: {self.stage}")
        print(f"Region: {self.region}, Account: {self.account_id}")
        print("=" * 60)
        
        tests = [
            ("S3 Buckets", self.validate_buckets),
            ("CloudFormation Exports", self.validate_cloudformation_exports),
            ("Glue Database", self.validate_glue_database),
            ("S3 Lambda Trigger", self.test_s3_lambda_trigger)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n{test_name}:")
            result = test_func()
            results.append((test_name, result))
        
        # Summary
        print("\n" + "=" * 60)
        print("📋 VALIDATION SUMMARY:")
        
        all_passed = True
        for test_name, passed in results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {status}: {test_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print(f"\n🎉 All infrastructure validation tests PASSED for {self.stage}!")
            return 0
        else:
            print(f"\n💥 Some infrastructure validation tests FAILED for {self.stage}!")
            return 1

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python validate_infrastructure.py <stage> <region> <account_id>")
        print("Example: python validate_infrastructure.py dev us-west-2 123456789012")
        sys.exit(1)
    
    stage = sys.argv[1]
    region = sys.argv[2] 
    account_id = sys.argv[3]
    
    validator = InfrastructureValidator(stage, region, account_id)
    exit_code = validator.run_all_validations()
    sys.exit(exit_code)