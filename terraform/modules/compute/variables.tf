variable "project_name" {
  description = "Name of the project used for resource naming"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs where ECS tasks will run"
  type        = map(string)
}

variable "backend_security_group_id" {
  description = "Security group ID assigned to the backend ECS tasks"
  type        = string
}

variable "backend_port" {
  description = "Port exposed by the backend container"
  type        = number
  default     = 8000
}
variable "ecs_execution_role_arn" {
  description = "IAM role ARN used by ECS to pull images and send logs"
  type        = string
}

variable "ecs_task_role_arn" {
  description = "IAM role ARN used by the banking application"
  type        = string
}
variable "vpc_id" {
  description = "VPC ID used by the ALB target group"
  type        = string
}

variable "public_subnet_ids" {
  description = "Public subnet IDs for the internet-facing ALB"
  type        = map(string)
}

variable "alb_security_group_id" {
  description = "Security group ID assigned to the ALB"
  type        = string
}
variable "acm_certificate_arn" {
  description = "Optional ACM certificate ARN for HTTPS"
  type        = string
  default     = null
}

variable "enable_dev_http_listener" {
  description = "Enable the temporary HTTP listener for development only; keep disabled in staging and production"
  type        = bool
  default     = false
}
