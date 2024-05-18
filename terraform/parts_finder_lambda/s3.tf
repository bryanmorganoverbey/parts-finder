

# Create an S3 bucket
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = var.s3_bucket_name # Replace with your desired bucket name
}
resource "aws_s3_bucket_versioning" "lambda_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}
# Create a bucket policy
resource "aws_s3_bucket_policy" "my_bucket_policy" {
  bucket = aws_s3_bucket.lambda_bucket.id
  depends_on = [ aws_s3_bucket_public_access_block.lambda_zip_files ]
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "PublicReadGetObject",
        Effect    = "Allow",
        Principal = "*",
        Action    = [
          "s3:*Object"
        ],
        Resource  = "${aws_s3_bucket.lambda_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_s3_bucket_public_access_block" "lambda_zip_files" {
  bucket = aws_s3_bucket.lambda_bucket.id
  block_public_acls       = true
  block_public_policy     = false
  ignore_public_acls      = true
  restrict_public_buckets = true
}
locals {
  lambda-files = [ # explicit list of files to archive
    "lambda_function.py",
    "sns_email_alerts.py",
    "LKQ.py"
  ]
}

# Zip the Lamda function on the fly
data "archive_file" "source" {
  type        = "zip"
  source_dir  = var.path_to_lambda_sourcecode
  excludes    = [for file in fileset(var.path_to_lambda_sourcecode, "**") : file if !contains(local.lambda-files, file)]
  output_path = var.path_to_zip
}
resource "aws_s3_object" "provison_source_files" {
  bucket      = aws_s3_bucket.lambda_bucket.id
  key         = var.lambda_zip_key
  source      = var.path_to_zip
  source_hash = filemd5(data.archive_file.source.output_path)
}

