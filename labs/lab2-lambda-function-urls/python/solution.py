import boto3

lambda_client = boto3.client('lambda', endpoint_url="http://localhost:4566", region_name="us-east-1")

url_response = lambda_client.create_function_url_config(
    FunctionName='ServerlessProcessor',
    AuthType='NONE'
)
func_url = url_response['FunctionUrl']

lambda_client.add_permission(
    FunctionName='ServerlessProcessor',
    Action='lambda:InvokeFunctionUrl',
    StatementId='FunctionURLAllowPublicAccess',
    Principal='*',
    FunctionUrlAuthType='NONE'
)

print(f"Your LocalStack Lambda URL is: {func_url}")
