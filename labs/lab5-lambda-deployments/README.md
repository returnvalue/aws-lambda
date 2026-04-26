# Lab 5: Safe Deployments (Versions, Aliases & Concurrency)

**Goal:** Publish an immutable version of the function, point a PROD alias to it, and apply Reserved Concurrency to guarantee the function can always scale up to handle critical requests.
```bash
# 1. Publish an immutable Version of the current function state
VERSION=$(awslocal lambda publish-version \
  --function-name ServerlessProcessor \
  --query 'Version' --output text)
VERSION=$(aws lambda publish-version \
  --function-name ServerlessProcessor \
  --query 'Version' --output text)

# 2. Create a PROD Alias pointing to that specific Version
awslocal lambda create-alias \
  --function-name ServerlessProcessor \
  --name PROD \
  --function-version $VERSION
aws lambda create-alias \
  --function-name ServerlessProcessor \
  --name PROD \
  --function-version $VERSION

# 3. Set Reserved Concurrency to 10 (Guarantees exactly 10 execution environments are reserved for this function)
awslocal lambda put-function-concurrency \
  --function-name ServerlessProcessor \
  --reserved-concurrent-executions 10
aws lambda put-function-concurrency \
  --function-name ServerlessProcessor \
  --reserved-concurrent-executions 10

# 4. Invoke the PROD alias specifically
awslocal lambda invoke \
  --function-name ServerlessProcessor \
  --qualifier PROD \
  alias_response.json
aws lambda invoke \
  --function-name ServerlessProcessor \
  --qualifier PROD \
  alias_response.json

cat alias_response.json
```

## 🧠 Key Concepts & Importance

- **Lambda Versions:** A version is an immutable snapshot of your function's code and configuration. This allows you to lock in a known-good state for production.
- **Lambda Aliases:** A pointer to a specific function version. Aliases (like `PROD` or `DEV`) allow you to update the underlying version without changing the resource name or ARN used by clients.
- **Reserved Concurrency:** Guarantees that a specific number of concurrent executions are always available for your function. It also acts as a ceiling, preventing the function from consuming all available account-level concurrency.
- **Safe Deployments:** Using versions and aliases enables advanced deployment strategies like blue-green or canary deployments (using weighted aliases).
- **Scalability Management:** Reserved concurrency is critical for protecting mission-critical functions from "noisy neighbor" issues where other functions exhaust the account's concurrency pool.

## 🛠️ Command Reference

- `lambda publish-version`: Creates an immutable version of the function's code and configuration.
    - `--function-name`: The name of the function.
- `lambda create-alias`: Creates an alias for a specific function version.
    - `--function-name`: The name of the function.
    - `--name`: The name of the alias (e.g., `PROD`).
    - `--function-version`: The specific version the alias should point to.
- `lambda put-function-concurrency`: Sets the reserved concurrency for a function.
    - `--function-name`: The name of the function.
    - `--reserved-concurrent-executions`: The number of concurrent executions to reserve.
- `lambda invoke`: Triggers the function.
    - `--qualifier`: Specifies the version or alias to invoke (e.g., `PROD`).

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
