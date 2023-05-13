output "ml_pipeline_task_definition_arn" {
  value = "${aws_ecs_task_definition.ml_pipeline.arn}"
}

output "cluster_arn" {
  value = "${aws_ecs_cluster.mlops_handson.arn}"
}