provider "aws" {
  region  = "us-east-2"
  profile = "bryanmorganoverbey"
}

# Create a Lambda function
resource "aws_lambda_function" "my_lambda_function" {
  function_name    = "daily_parts_finder"
  handler          = "lambda_function.main"
  runtime          = "python3.11" # Change to your desired runtime
  layers           = ["arn:aws:lambda:us-east-2:336392948345:layer:AWSSDKPandas-Python311:12"]
  role             = aws_iam_role.lambda_exec_role.arn
  s3_bucket        = var.s3_bucket_name
  s3_key           = aws_s3_object.provison_source_files.key
  source_code_hash = filemd5(data.archive_file.source.output_path)
  timeout          = 180
  memory_size      = 1024

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.lambda_bucket.bucket
    }
  }
}




