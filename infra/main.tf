terraform {
  required_version = "~> 1.4"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.60"
    }
  }
}
provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}


module "network" {
  source = "./modules/network"
  aws_region = var.aws_region
}

module "alb" {
  source = "./modules/alb"
  alb_security_group = module.network.alb_security_group
  alb_subnets = module.network.public_subnets
  vpc_id = module.network.vpc_id
}

module "ecr" {
 source = "./modules/ecr"
}

module "iam" {
 source = "./modules/iam"
}

module "s3" {
  source = "./modules/s3"
  account_id = var.aws_account_id
}

module "ecs" {
  source = "./modules/ecs"
  private_subnets = module.network.private_subnets
  predict_api_security_group = module.network.predict_api_security_group
  target_group_arn = module.alb.target_group_arn
  ml_pipeline_ecr_uri = module.ecr.ml_pipeline_ecr_uri
  predict_api_ecr_uri = module.ecr.predict_api_ecr_uri
  ecs_task_role_arn = module.iam.ecs_task_role_arn
  ecs_task_execution_role_arn = module.iam.ecs_task_execution_role_arn
  bucket = module.s3.bucket
}


module "stepfunctions" {
  source = "./modules/stepfunctions"
  stepfunctions_role_arn = module.iam.step_functions_role_arn
  event_bridge_role_arn = module.iam.event_bridge_role_arn
  task_definition_arn = module.ecs.ml_pipeline_task_definition_arn
  cluster_arn = module.ecs.cluster_arn
  security_group = module.network.ml_pipeline_security_group
  subnet = module.network.ml_pipeline_subnet
}

variable "aws_region" {
  description = "The AWS region to create resources in."
}

variable "aws_profile" {
  description = "The AWS-CLI profile for the account to create resources in."
}

variable "aws_account_id" {
  description = "The AWS Account ID to create resources in."
}
