resource "aws_lambda_alias" "prod" {
  name             = "PROD"
  description      = "Production alias"
  function_name    = aws_lambda_function.serverless_processor.function_name
  function_version = aws_lambda_function.serverless_processor.version
}

resource "aws_lambda_function" "serverless_processor" {
  # ... existing attributes
  publish                        = true
  reserved_concurrent_executions = 10
}
