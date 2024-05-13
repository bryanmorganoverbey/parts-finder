
resource "aws_cloudwatch_event_rule" "lambda_schedule" {
  name                = "lambda-schedule"
  description           = "Schedule lambda function"
  schedule_expression = "rate(4 hours)" # Change the schedule as needed
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  target_id = "my-lambda-function-target"
  rule      = aws_cloudwatch_event_rule.lambda_schedule.name
  arn       = aws_lambda_function.my_lambda_function.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.my_lambda_function.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.lambda_schedule.arn
}