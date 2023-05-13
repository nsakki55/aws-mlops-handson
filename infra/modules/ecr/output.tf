output "ml_pipeline_ecr_uri" {
  value = "${aws_ecr_repository.ml_pipeline.repository_url}"
}

output "predict_api_ecr_uri" {
  value = "${aws_ecr_repository.predict_api.repository_url}"
}
