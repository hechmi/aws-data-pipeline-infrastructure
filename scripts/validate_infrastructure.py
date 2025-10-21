#!/usr/bin/env python3
"""
Simplified Infrastructure validation script
Validates that infrastructure resources were created successfully using CloudFormation
"""

import boto3
import sys

class InfrastructureValidator:
    def __init__(self, stage, region, account_id):
        self.stage = stage
        self.region = region
        self.account_id = account_id
        self.stack_name = f"{stage.title()}Stage-Infrastructure"
        
        # AWS clients
        self.cloudformation = boto3.client('cloudformation', region_name=region)
        
    def validate_stack_status(self):
        """Validate that the CloudFormation stack deployed successfully"""
        print("📋 Validating CloudFormation Stack...")
        
        try:
            response = self.cloudformation.describe_stacks(StackName=self.stack_name)
            stack = response['Stacks'][0]
            status = stack['StackStatus']
            
            if status in ['CREATE_COMPLETE', 'UPDATE_COMPLETE']:
                print(f"  ✅ Stack status: {status}")
                return True
            else:
                print(f"  ❌ Stack status: {status}")
                return False
                
        except Exception as e:
            print(f"  ❌ Stack validation failed: {e}")
            return False
    
    def validate_stack_resources(self):
        """Validate that expected resources were created"""
        print("🏗️  Validating Stack Resources...")
        
        expected_resource_types = [
            'AWS::S3::Bucket',
            'AWS::Glue::Database', 
            'AWS::IAM::Role',
            'AWS::Lambda::Function'
        ]
        
        try:
            resources = self.cloudformation.describe_stack_resources(StackName=self.stack_name)
            resource_types = [r['ResourceType'] for r in resources['StackResources']]
            
            all_found = True
            for expected_type in expected_resource_types:
                count = resource_types.count(expected_type)
                if count > 0:
                    print(f"  ✅ {expected_type}: {count} resource(s)")
                else:
                    print(f"  ❌ {expected_type}: Missing")
                    all_found = False
            
            return all_found
            
        except Exception as e:
            print(f"  ❌ Resource validation failed: {e}")
            return False
    
    def validate_stack_outputs(self):
        """Validate that stack outputs/exports are available"""
        print("📤 Validating Stack Outputs...")
        
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
            
            all_found = True
            for export_name in expected_exports:
                if export_name in export_names:
                    print(f"  ✅ Export available: {export_name}")
                else:
                    print(f"  ❌ Export missing: {export_name}")
                    all_found = False
            
            return all_found
            
        except Exception as e:
            print(f"  ❌ Export validation failed: {e}")
            return False
    
    def run_all_validations(self):
        """Run all validation tests"""
        print(f"\n🔍 Validating Infrastructure for Stage: {self.stage}")
        print(f"Region: {self.region}, Account: {self.account_id}")
        print(f"Stack: {self.stack_name}")
        print("=" * 60)
        
        tests = [
            ("CloudFormation Stack Status", self.validate_stack_status),
            ("Stack Resources", self.validate_stack_resources),
            ("Stack Outputs/Exports", self.validate_stack_outputs)
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