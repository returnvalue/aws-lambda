import boto3
import zipfile
import os

lambda_client = boto3.client('lambda', endpoint_url="http://localhost:4566", region_name="us-east-1")

os.makedirs('python', exist_ok=True)
with open('python/custom_logger.py', 'w') as f:
    f.write('def log_message(msg):\n    return f"[CUSTOM LAYER LOG] {msg}"\n')

with zipfile.ZipFile('layer.zip', 'w') as z:
    z.write('python/custom_logger.py')

with open('layer.zip', 'rb') as f:
    zip_bytes = f.read()

layer_response = lambda_client.publish_layer_version(
    LayerName='CustomLoggerLayer',
    Description='Shared logging utility',
    Content={'ZipFile': zip_bytes},
    CompatibleRuntimes=['python3.9']
)
layer_arn = layer_response['LayerVersionArn']

lambda_client.update_function_configuration(
    FunctionName='ServerlessProcessor',
    Layers=[layer_arn]
)
