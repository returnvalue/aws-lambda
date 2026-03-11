resource "aws_lambda_layer_version" "logger" {
  filename            = "layer.zip"
  layer_name          = "CustomLoggerLayer"
  compatible_runtimes = ["python3.9"]
}

# (Updating the function configuration)
resource "aws_lambda_function" "serverless_processor" {
  # ... existing attributes
  layers = [aws_lambda_layer_version.logger.arn]
}
