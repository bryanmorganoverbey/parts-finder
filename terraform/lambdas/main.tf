provider "aws" {
  region = "us-east-2"
}

resource "aws_lambda_function" "my_lambda_function" {
  function_name    = "daily-parts-finder"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.handler"
  runtime          = "python3.11"
  filename         = "../../lambdas/daily_cron.zip"# Path to your Lambda function code
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda-exec-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_cloudwatch_event_rule" "lambda_schedule" {
  name                = "lambda-schedule"
  schedule_expression = "rate(1 day)" # Change the schedule as needed
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.lambda_schedule.name
  arn       = aws_lambda_function.my_lambda_function.arn
  target_id = "my-lambda-function-target"
}
