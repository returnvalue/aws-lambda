# AWS Lambda Serverless Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-Lambda_Compute-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating core Amazon Lambda concepts, from foundational function provisioning to advanced event-driven architectures and triggers. Using [LocalStack Pro](https://localstack.cloud/), we simulate a complete AWS serverless environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS best practices (SAA-C03), these labs cover:
* **Function Provisioning:** Deploying serverless compute with specific runtimes and execution roles.
* **IAM Execution Roles:** Implementing the principle of least privilege for Lambda functions.
* **Event Triggers:** (Upcoming) Decoupling systems using S3, SQS, and SNS triggers.
* **API Integration:** (Upcoming) Fronting functions with Amazon API Gateway.
* **Serverless Resilience:** (Upcoming) Configuring DLQs and destination policies.
* **Scalability:** (Upcoming) Understanding concurrency and environment variables.

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
> **Session Persistence:** These labs rely on bash variables (like `$ROLE_ARN`). Run all commands in the same terminal session to maintain context.

## 📚 Labs Index
1. [Lab 1: Foundational Lambda Provisioning](./labs/lab1-lambda-provisioning/README.md)
