

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
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "PublicReadGetObject",
        Effect    = "Allow",
        Principal = "*",
        Action    = [
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource  = "${aws_s3_bucket.lambda_bucket.arn}/*"
      }
    ]
  })
}


resource "aws_s3_object" "provison_source_files" {
  bucket      = aws_s3_bucket.lambda_bucket.id
  key         = var.lambda_zip_key
  source      = var.path_to_zip
  source_hash = filemd5(var.path_to_zip)
}

