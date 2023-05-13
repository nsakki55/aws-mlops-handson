resource "aws_sfn_state_machine" "mlops_handson" {
  name     = "mlops-handson-ml-pipeline"
  role_arn = "${var.stepfunctions_role_arn}"

  definition = templatefile("./modules/stepfunctions/definition/execute_ml_pipeline.json", {
    cluster_arn = "${var.cluster_arn}",
    task_definition_arn = "${var.task_definition_arn}",
    security_group = "${var.security_group}",
    subnet = "${var.subnet}"
  })
}

resource "aws_scheduler_schedule" "mlops_hanson" {
  name                = "mlops-handson-stepfunctions-schedule"
  schedule_expression =  "cron(0 */1 * * ? *)"
  group_name = "default"
  flexible_time_window {
    mode = "OFF"
  }
  target {
    arn = aws_sfn_state_machine.mlops_handson.arn
    role_arn = "${var.event_bridge_role_arn}"
  }
  state="DISABLED"
}