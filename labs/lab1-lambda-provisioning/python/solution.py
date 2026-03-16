import boto3
import json
import zipfile

iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")
lambda_client = boto3.client('lambda', endpoint_url="http://localhost:4566", region_name="us-east-1")

trust_policy = {
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}

with open('trust-policy.json', 'w') as f:
    json.dump(trust_policy, f)

role_response = iam.create_role(
    RoleName='LambdaExecRole',
    AssumeRolePolicyDocument=json.dumps(trust_policy)
)
role_arn = role_response['Role']['Arn']

lambda_code = '''import json
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    return {
        "statusCode": 200,
        "body": json.dumps("Hello from LocalStack Lambda!")
    }
'''

with open('lambda_function.py', 'w') as f:
    f.write(lambda_code)

with zipfile.ZipFile('function.zip', 'w') as z:
    z.write('lambda_function.py')

with open('function.zip', 'rb') as f:
    zip_bytes = f.read()

lambda_client.create_function(
    FunctionName='ServerlessProcessor',
    Runtime='python3.9',
    Role=role_arn,
    Handler='lambda_function.lambda_handler',
    Code={'ZipFile': zip_bytes}
)

response = lambda_client.invoke(
    FunctionName='ServerlessProcessor'
)

with open('response.json', 'w') as f:
    f.write(response['Payload'].read().decode('utf-8'))
