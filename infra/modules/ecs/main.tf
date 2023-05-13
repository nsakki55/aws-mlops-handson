resource "aws_ecs_cluster" "mlops_handson" {
  name = "mlops-handson-ecs"
}

resource "aws_ecs_task_definition" "ml_pipeline" {
  family                   = "ml-pipeline"
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  requires_compatibilities = ["FARGATE"]
  container_definitions    = templatefile("./modules/ecs/container_definitions/ml_pipeline.json", {
    ml_pipeline_ecr_uri = "${var.ml_pipeline_ecr_uri}",
    bucket              = "${var.bucket}"
  })
  task_role_arn            = "${var.ecs_task_role_arn}"
  execution_role_arn       = "${var.ecs_task_execution_role_arn}"
}

resource "aws_ecs_task_definition" "predict_api" {
  family                   = "predict-api"
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  requires_compatibilities = ["FARGATE"]
  container_definitions    = templatefile("./modules/ecs/container_definitions/predict_api.json", {
    predict_api_ecr_uri = "${var.predict_api_ecr_uri}",
    bucket              = "${var.bucket}"
  })
  task_role_arn            = "${var.ecs_task_role_arn}"
  execution_role_arn       = "${var.ecs_task_execution_role_arn}"
}

resource "aws_ecs_service" "predict_api" {
  name                               = "predict-api"
  cluster                            = "${aws_ecs_cluster.mlops_handson.name}"
  task_definition                    = "${aws_ecs_task_definition.predict_api.arn}"
  desired_count                      = 2
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 200
  launch_type                        = "FARGATE"
  network_configuration {
    security_groups = [
      "${var.predict_api_security_group}"
    ]
    subnets = "${var.private_subnets}"
  }

  load_balancer {
    target_group_arn = "${var.target_group_arn}"
    container_name = "predict-api"
    container_port = 8080
  }
}

resource "aws_appautoscaling_target" "predict_api" {
  max_capacity       = 10
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.mlops_handson.name}/${aws_ecs_service.predict_api.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "predict_api" {
  name               = "predicto-api-app-autos-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.predict_api.resource_id
  scalable_dimension = aws_appautoscaling_target.predict_api.scalable_dimension
  service_namespace  = aws_appautoscaling_target.predict_api.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    scale_in_cooldown  = 60
    scale_out_cooldown = 60
    target_value       = 70.0
  }
}