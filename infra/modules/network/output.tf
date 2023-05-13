output "public_subnets" {
  value = [ "${aws_subnet.public1a.id}", "${aws_subnet.public1c.id}" ]
}

output "private_subnets" {
  value = [ "${aws_subnet.private1a.id}", "${aws_subnet.private1c.id}" ]
}

output "alb_security_group" {
  value = "${aws_security_group.alb.id}"
}

output "ml_pipeline_security_group" {
  value = "${aws_security_group.ml_pipeline.id}"
}

output "predict_api_security_group" {
  value = "${aws_security_group.predict_api.id}"
}

output "vpc_id" {
  value = "${aws_vpc.mlops_handson.id}"
}

output "ml_pipeline_subnet" {
  value = "${aws_subnet.private1a.id}"
}