variable "vpc_id" {
  description = "ID of the VPC where security groups will be created"
  type        = string
}
variable "project_name" {
  description = "Name of the project used for resource naming"
  type        = string
}
variable "backend_port" {
  description = "Port used by the backend application"
  type        = number
  default     = 8000
}

variable "enable_dev_http_listener" {
  description = "Enable public HTTP ingress for development only; keep disabled in staging and production"
  type        = bool
  default     = false
}
