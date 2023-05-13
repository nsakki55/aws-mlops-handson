variable "stepfunctions_role_arn" {
  description = "IAM Role for StepFunctions"
}

variable "event_bridge_role_arn" {
  description = "IAM Role for EventBridge"
}

variable "task_definition_arn" {
  description = "task definition executed by StepFunctions"
}

variable "cluster_arn" {
  description = "cluster arn to execute ecs task"
}

variable "security_group" {
  description = "The security group to associated with the executed task"
}

variable "subnet" {
  description = "The subnet in which the task can execute"
}
