terraform {
  backend "s3" {
    bucket         = "parts-finder-remote-state"
    key = "daily-cron-lambda"
    region         = "us-east-2" # Your AWS region
    dynamodb_table = "parts-finder-remote-state-locks" # Optional, if you want to use DynamoDB for locking
  }
}
