provider "aws" {
  region = "us-east-2"
}

# Create a Lambda function
resource "aws_lambda_function" "my_lambda_function" {
  function_name    = "daily_parts_finder"
  handler          = "lambda_function.main"
  runtime          = "python3.11" # Change to your desired runtime
  role             = aws_iam_role.lambda_exec_role.arn
  s3_bucket        = var.s3_bucket_name
  s3_key           = var.lambda_zip_key
  source_code_hash = filemd5(var.path_to_zip)
  timeout = 180
  memory_size = 1024

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.lambda_bucket.bucket
    }
  }
}


