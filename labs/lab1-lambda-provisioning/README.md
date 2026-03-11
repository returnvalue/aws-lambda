# Lab 1: Foundational Lambda Provisioning

**Goal:** Create an IAM Execution Role (Trust Policy) and deploy a simple Python Lambda function using a zipped deployment package.

```bash
# 1. Create a Trust Policy allowing Lambda to assume the role
cat <<EOF > trust-policy.json
{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}
EOF

ROLE_ARN=$(awslocal iam create-role --role-name LambdaExecRole --assume-role-policy-document file://trust-policy.json --query 'Role.Arn' --output text)

# 2. Write a simple Python Lambda function
cat <<EOF > lambda_function.py
import json
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    return {
        "statusCode": 200,
        "body": json.dumps("Hello from LocalStack Lambda!")
    }
EOF

# 3. Zip the code payload
zip function.zip lambda_function.py

# 4. Create the Lambda function
awslocal lambda create-function \
  --function-name ServerlessProcessor \
  --runtime python3.9 \
  --role $ROLE_ARN \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip

# 5. Invoke the function manually (CLI)
awslocal lambda invoke --function-name ServerlessProcessor response.json
cat response.json
```

## 🧠 Key Concepts & Importance

- **Lambda Execution Role:** An IAM role that provides your Lambda function with permissions to access other AWS services. The role must have a trust policy allowing `lambda.amazonaws.com` to assume it.
- **Serverless Compute:** You provide the code, and Lambda manages the underlying infrastructure, scaling, and high availability.
- **Deployment Packages:** Lambda functions are typically deployed as `.zip` archives containing your code and any necessary dependencies.
- **Runtime:** The environment in which your function code runs (e.g., Python, Node.js, Go).
- **Handler:** The specific function in your code that Lambda calls when the function is invoked.
- **Synchronous vs. Asynchronous:** In this lab, we use a synchronous invocation via the CLI to receive an immediate response.

## 🛠️ Command Reference

- `iam create-role`: Creates an IAM role with a specific trust policy.
- `lambda create-function`: Provisions a new Lambda function.
    - `--function-name`: Unique identifier for the function.
    - `--runtime`: The identifier of the function's runtime.
    - `--role`: The ARN of the function's execution role.
    - `--handler`: The name of the method within your code that Lambda calls.
    - `--zip-file`: The path to the deployment package (using `fileb://` for binary).
- `lambda invoke`: Manually triggers a Lambda function.
    - `--function-name`: The function to invoke.
    - `response.json`: The file where the output payload will be saved.
