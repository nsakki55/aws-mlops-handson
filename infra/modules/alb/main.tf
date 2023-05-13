resource "aws_lb" "mlops_handson" {
  load_balancer_type = "application"
  name               = "mlops-handson-alb"

  security_groups = ["${var.alb_security_group}"]
  subnets         = var.alb_subnets
}


# ELB Target Group
resource "aws_lb_target_group" "mlops_handson" {
  name = "mlops-handson-tg"

  port        = 8080
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id = "${var.vpc_id}"
  health_check {
    port     = 8080
    path = "/healthcheck"
  }
}

# Listener
resource "aws_lb_listener" "mlops_handson" {
   load_balancer_arn = "${aws_lb.mlops_handson.arn}"
  port              = "8080"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = "${aws_lb_target_group.mlops_handson.arn}"
  }
}
