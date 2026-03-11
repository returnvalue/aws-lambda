# Lab 3: Asynchronous Polling (SQS Event Source Mapping)

**Goal:** Decouple your system. Send messages to an SQS queue and have the Lambda function automatically poll and process them in batches.

```bash
# 1. Create the SQS Queue
QUEUE_URL=$(awslocal sqs create-queue --queue-name LambdaTriggerQueue --query 'QueueUrl' --output text)
QUEUE_ARN=$(awslocal sqs get-queue-attributes --queue-url $QUEUE_URL --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

# 2. Map the SQS queue as an Event Source for the Lambda
awslocal lambda create-event-source-mapping \
  --function-name ServerlessProcessor \
  --batch-size 5 \
  --event-source-arn $QUEUE_ARN

# 3. Send a message to the queue to asynchronously trigger the Lambda
awslocal sqs send-message \
  --queue-url $QUEUE_URL \
  --message-body "Process this asynchronous payload!"
```

## 🧠 Key Concepts & Importance

- **Event Source Mapping:** A Lambda resource that reads from an event source and invokes a Lambda function. In the case of SQS, Lambda polls the queue and invokes the function synchronously with an event that contains queue messages.
- **Asynchronous Processing:** By using a queue, the sender doesn't wait for the Lambda to finish. This decouples the components and allows for better handling of traffic spikes.
- **Batching:** Lambda can read a batch of messages from the queue and pass them to your function in a single invocation. This improves efficiency and reduces the number of function invocations.
- **Polling:** Lambda automatically manages the polling of the SQS queue, so you don't need to write custom polling logic in your application.
- **Scaling:** If the queue length increases, Lambda automatically scales up the number of concurrent executions to process the messages more quickly.

## 🛠️ Command Reference

- `sqs create-queue`: Creates a new SQS queue.
- `sqs get-queue-attributes`: Retrieves attributes for the specified queue (e.g., `QueueArn`).
- `lambda create-event-source-mapping`: Connects an event source (like SQS) to a Lambda function.
    - `--function-name`: The name of the Lambda function.
    - `--batch-size`: The maximum number of records to retrieve from the event source at the time of invocation.
    - `--event-source-arn`: The Amazon Resource Name (ARN) of the event source.
- `sqs send-message`: Delivers a message to the specified queue.
    - `--queue-url`: The URL of the SQS queue.
    - `--message-body`: The content of the message.
