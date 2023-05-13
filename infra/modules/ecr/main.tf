resource "aws_ecr_repository" "ml_pipeline" {
  name = "mlops-handson/ml-pipeline"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository" "predict_api" {
  name = "mlops-handson/predict-api"
  image_tag_mutability = "MUTABLE"
}