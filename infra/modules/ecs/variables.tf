variable "private_subnets" {
  description = "List of private subnet ids to place to predict api"
}

variable "predict_api_security_group" {
  description = "security group id for predict api"
}

variable "target_group_arn" {
  description = "target group for predict api load balancer"
}

variable "ml_pipeline_ecr_uri" {
  description = "ECR URI for ml pipeline ecs task"
}

variable "predict_api_ecr_uri" {
  description = "ECR URI for predict api ecs task"
}

variable "ecs_task_role_arn" {
  description = "IAM Role for ecs task application"
}

variable "ecs_task_execution_role_arn" {
  description = "IAM Role for ecs task execution"
}

variable "bucket" {
  description = "S3 Bucket for ML data"
}