resource "aws_lambda_function_url" "sync_url" {
  function_name      = var.function_name
  authorization_type = "NONE"
}

resource "aws_lambda_permission" "allow_public" {
  statement_id           = "FunctionURLAllowPublicAccess"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = var.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}
