import boto3

lambda_client = boto3.client('lambda', endpoint_url="http://localhost:4566", region_name="us-east-1")

version_response = lambda_client.publish_version(
    FunctionName='ServerlessProcessor'
)
version = version_response['Version']

lambda_client.create_alias(
    FunctionName='ServerlessProcessor',
    Name='PROD',
    FunctionVersion=version
)

lambda_client.put_function_concurrency(
    FunctionName='ServerlessProcessor',
    ReservedConcurrentExecutions=10
)

response = lambda_client.invoke(
    FunctionName='ServerlessProcessor',
    Qualifier='PROD'
)

with open('alias_response.json', 'w') as f:
    f.write(response['Payload'].read().decode('utf-8'))
