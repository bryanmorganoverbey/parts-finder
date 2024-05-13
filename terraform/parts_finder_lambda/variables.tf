variable "s3_bucket_name" {
  description = "The name of the s3 bucket holding the lambda zip"
  type        = string
  sensitive   = false
  default =  "parts-finder-lambda-zip-file"
}

variable "lambda_zip_key" {
  description = "Key of the ZIP file containing Lambda function code in the S3 bucket"
  type        = string
  default = "key-to-file"
}

variable "path_to_zip" {
  description = "Path the the daily_cron.zip lambda function code"
  type = string
  default = "../../lambdas/daily_cron.zip"
}
