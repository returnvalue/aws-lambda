# AWS Lambda Serverless Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-Lambda_Compute-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating core Amazon Lambda concepts, from foundational function provisioning to advanced event-driven architectures and triggers. Using [LocalStack Pro](https://localstack.cloud/), we simulate a complete AWS serverless environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS best practices (SAA-C03), these labs cover:
* **Function Provisioning:** Deploying serverless compute with specific runtimes and execution roles.
* **Synchronous Web Access:** Exposing functions via built-in Lambda Function URLs.
* **Asynchronous Polling:** Decoupling systems with SQS Event Source Mappings.
* **Safe Deployments:** Implementing function Versions and Aliases for lifecycle management.
* **Code Reusability:** Leveraging Lambda Layers for shared libraries and logic.
* **Scalability & Resiliency:** Using Reserved Concurrency to guarantee compute availability.
* **IAM Execution Roles:** Implementing the principle of least privilege for Lambda functions.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Configure your LocalStack Auth Token in `.env`:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   
```

2. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   
```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative scenario. You are building an evolving serverless infrastructure.
>
> **Session Persistence:** These labs rely on bash variables (like `$ROLE_ARN`, `$QUEUE_URL`, `$LAYER_ARN`, `$VERSION`). Run all commands in the same terminal session to maintain context.

## 📚 Labs Index
1. [Lab 1: Foundational Lambda Provisioning](./labs/lab1-lambda-provisioning/README.md)
2. [Lab 2: Synchronous Web Access (Function URLs)](./labs/lab2-lambda-function-urls/README.md)
3. [Lab 3: Asynchronous Polling (SQS Event Source Mapping)](./labs/lab3-lambda-sqs-trigger/README.md)
4. [Lab 4: Code Reusability (Lambda Layers)](./labs/lab4-lambda-layers/README.md)
5. [Lab 5: Safe Deployments (Versions, Aliases & Concurrency)](./labs/lab5-lambda-deployments/README.md)

---

💡 **Pro Tip: Using `aws` instead of `awslocal`**

If you prefer using the standard `aws` CLI without the `awslocal` wrapper or repeating the `--endpoint-url` flag, you can configure a dedicated profile in your AWS config files.

### 1. Configure your Profile
Add the following to your `~/.aws/config` file:
```ini
[profile localstack]
region = us-east-1
output = json
# This line redirects all commands for this profile to LocalStack
endpoint_url = http://localhost:4566
```

Add matching dummy credentials to your `~/.aws/credentials` file:
```ini
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

### 2. Use it in your Terminal
You can now run commands in two ways:

**Option A: Pass the profile flag**
```bash
aws iam create-user --user-name DevUser --profile localstack
```

**Option B: Set an environment variable (Recommended)**
Set your profile once in your session, and all subsequent `aws` commands will automatically target LocalStack:
```bash
export AWS_PROFILE=localstack
aws iam create-user --user-name DevUser
```

### Why this works
- **Precedence**: The AWS CLI (v2) supports a global `endpoint_url` setting within a profile. When this is set, the CLI automatically redirects all API calls for that profile to your local container instead of the real AWS cloud.
- **Convenience**: This allows you to use the standard documentation commands exactly as written, which is helpful if you are copy-pasting examples from AWS labs or tutorials.
