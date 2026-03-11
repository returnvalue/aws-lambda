resource "aws_sqs_queue" "trigger_queue" {
  name = "LambdaTriggerQueue"
}

resource "aws_lambda_event_source_mapping" "sqs_mapping" {
  event_source_arn = aws_sqs_queue.trigger_queue.arn
  function_name    = var.function_name
  batch_size       = 5
}
