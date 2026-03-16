import boto3

sqs = boto3.client('sqs', endpoint_url="http://localhost:4566", region_name="us-east-1")
lambda_client = boto3.client('lambda', endpoint_url="http://localhost:4566", region_name="us-east-1")

queue_response = sqs.create_queue(QueueName='LambdaTriggerQueue')
queue_url = queue_response['QueueUrl']

attrs_response = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['QueueArn'])
queue_arn = attrs_response['Attributes']['QueueArn']

lambda_client.create_event_source_mapping(
    FunctionName='ServerlessProcessor',
    BatchSize=5,
    EventSourceArn=queue_arn
)

sqs.send_message(
    QueueUrl=queue_url,
    MessageBody="Process this asynchronous payload!"
)
