# Lab 2: Synchronous Web Access (Function URLs)

**Goal:** Instead of setting up a complex API Gateway, use Lambda Function URLs to quickly expose a synchronous HTTP endpoint for web clients. Because LocalStack generates custom subdomains that your local DNS might not recognize, we will use an HTTP Host header trick to route the request successfully.

```bash
# 1. Create a Function URL configuration (No auth for testing)
FUNC_URL=$(awslocal lambda create-function-url-config \
  --function-name ServerlessProcessor \
  --auth-type NONE \
  --query 'FunctionUrl' --output text)

# 2. Grant public access to invoke the URL
awslocal lambda add-permission \
  --function-name ServerlessProcessor \
  --action lambda:InvokeFunctionUrl \
  --statement-id FunctionURLAllowPublicAccess \
  --principal "*" \
  --function-url-auth-type NONE

echo "Your LocalStack Lambda URL is: $FUNC_URL"

# 3. Extract the hostname to bypass local DNS routing issues
# This strips out the 'http://' and trailing '/' to isolate the raw hostname
HOST_NAME=$(echo $FUNC_URL | awk -F/ '{print $3}' | awk -F: '{print $1}')

# 4. Test the synchronous invocation via cURL using the Host header workaround
# We send the request to localhost directly, but tell LocalStack which function to trigger via the Host header
curl -H "Host: $HOST_NAME" http://localhost:4566/
```

## 🧠 Key Concepts & Importance

- **Lambda Function URLs:** A built-in HTTP(S) endpoint for your Lambda function. It's the simplest way to configure an HTTPS endpoint for your function without the overhead of API Gateway or ALB.
- **Synchronous Invocation:** When you invoke a function using a Function URL, the client waits for the function to process the request and return a response.
- **Resource-Based Policies:** Using `add-permission` allows you to grant specific entities (like the public `*`) the right to invoke your function's URL.
- **LocalStack DNS Workaround:** LocalStack uses subdomains (e.g., `http://<id>.lambda-url.us-east-1.localhost.localstack.cloud:4566`) which may not resolve on all local machines. Using the `Host` header allows you to route the request to the correct function while sending the traffic to `localhost:4566`.
- **Use Cases:** 
    - Webhooks.
    - Simple APIs.
    - Single-function web applications.

## 🛠️ Command Reference

- `lambda create-function-url-config`: Creates a Function URL for a specific Lambda function.
    - `--function-name`: The name of the function.
    - `--auth-type`: The type of authentication (e.g., `NONE` or `AWS_IAM`).
- `lambda add-permission`: Adds a statement to the function's resource-based policy.
    - `--action`: The action to allow (e.g., `lambda:InvokeFunctionUrl`).
    - `--statement-id`: A unique identifier for the policy statement.
    - `--principal`: The entity granted permission (e.g., `*` for public).
    - `--function-url-auth-type`: Must match the auth type of the URL config.
