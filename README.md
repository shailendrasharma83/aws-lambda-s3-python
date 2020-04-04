# aws-lambda-s3-python
Lambda function to perform S3 write

    Create aws profile "sandbox"
    Load aws profile "sandbox"
    export AWS_PROFILE=sandbox

   
   # Validate templates
   
    cd cloudformation
   
    aws --profile sandbox cloudformation validate-template --template-body file://iam.yaml
   
    aws --profile sandbox cloudformation validate-template --template-body file://pre-requisite.yaml
   
  
   # Create IAM Roles
    aws --profile sandbox cloudformation create-stack --stack-name MySkillsDemoIAMRoles --template-body file://iam.yaml --capabilities CAPABILITY_NAMED_IAM
    aws --profile sandbox cloudformation create-stack --stack-name MySkillsDemoIAMRoles --template-body file://pre-requisite.yaml --capabilities CAPABILITY_NAMED_IAM
   
   **Note** :: As these commands are being executed in the context of an IAM user, the IAM user need to he added in the principal for S3 bucket policy and allow usage block in KMS
  
  **Example :: S3 Bucket policy**
  
            "AWS": [
                       "arn:aws:iam::************:role/CloudFormationRole",
                       "arn:aws:iam::************:user/*******.*******.com"
                   ] 
                   
  **Example :: KMS**
  
            {
               "Sid": "Allow use of the key for Cloudformation Role",
               "Effect": "Allow",
               "Principal": {
                   "AWS": [
                       "arn:aws:iam::************:role/CloudFormationRole",
                        "arn:aws:iam::************:user/*******.*******.com"
                   ]
               },
               "Action": [
                   "kms:Encrypt",
                   "kms:Decrypt",
                   "kms:ReEncrypt*",
                   "kms:GenerateDataKey*",
                   "kms:DescribeKey"
               ],
               "Resource": "*"
           }  
                   
  # Run CloudFormation commands for deployment
    
    cd ..
    
    aws cloudformation package --template-file template.yaml --output-template-file template-export.yaml --s3-bucket my-skills-demo-deployment-bucket  --kms-key-id alias/my-skills-demo-key
    
    aws cloudformation deploy --template-file template-export.yaml --stack-name my-skills-demo --s3-bucket my-skills-demo-deployment-bucket --kms-key-id  alias/my-skills-demo-key --capabilities CAPABILITY_NAMED_IAM  --role-arn arn:aws:iam::<account-id>:role/CloudFormationRole --parameter-overrides ExecutionRole=arn:aws:iam::<account-id>:role/LambdaRole
  
