provider "aws" {
    region = "eu-west-2"
}


data "aws_vpc" "vpc" {
    id = "vpc-04423dbb18410aece"
}


data "aws_ecs_cluster" "cluster" {
    cluster_name = "ecs-cluster"
}


data "aws_ecr_repository" "t3-pipeline" {
    name = "foodtruck-repo"
}


data "aws_ecr_repository" "t3-dashboard" {
    name = "foodtruck-dashboard"
}


data "aws_iam_role" "execution-role" {
    name = "ecsTaskExecutionRole"
}

