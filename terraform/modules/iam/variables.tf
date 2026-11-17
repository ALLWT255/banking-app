variable "project_name" {
  description = "Name of the project used for IAM resource naming"
  type        = string
}
variable "database_secret_arn" {
  description = "ARN of the RDS-managed database secret"
  type        = string
  default     = null
}
variable "jwt_secret_arn" {
  description = "ARN of the JWT signing secret in AWS Secrets Manager"
  type        = string
  default     = null
}
variable "enable_database" {
  description = "Whether RDS database access is enabled"
  type        = bool
  default     = false
}