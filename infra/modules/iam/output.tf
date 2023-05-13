output "ecs_task_role_arn" {
  value = "${aws_iam_role.ecs_task_role.arn}"
}

output "ecs_task_execution_role_arn" {
  value = "${aws_iam_role.ecs_task_execution_role.arn}"
}

output "step_functions_role_arn" {
  value = "${aws_iam_role.step_functions_role.arn}"
}

output "event_bridge_role_arn" {
  value = "${aws_iam_role.event_bridge_role.arn}"
}
