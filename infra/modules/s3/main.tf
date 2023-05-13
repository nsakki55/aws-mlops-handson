resource "aws_s3_bucket" "mlops_handson" {
  bucket = "mlops-handson-${var.account_id}"
}