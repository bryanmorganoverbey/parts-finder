terraform {
  backend "s3" {
    bucket         = "parts-finder-remote-state-bryan"
    key            = "daily-cron-lambda"
    region         = "us-east-2"                             # Your AWS region
    dynamodb_table = "parts-finder-remote-state-locks-bryan" # Optional, if you want to use DynamoDB for locking
    profile        = "bryanmorganoverbey"
  }
}
