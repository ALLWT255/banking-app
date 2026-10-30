variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnets" {
  description = "Map of Availability Zones to public subnet CIDRs"
  type        = map(string)
}

variable "private_subnets" {
  description = "Map of Availability Zones to private subnet CIDRs"
  type        = map(string)
}
variable "db_name" {
  description = "Name of the PostgreSQL database"
  type        = string
}

variable "enable_dev_http_listener" {
  description = "Enable the temporary HTTP listener for development only; keep disabled in staging and production"
  type        = bool
  default     = false
}
variable "enable_database" {
  description = "Whether to deploy the RDS PostgreSQL database"
  type        = bool
  default     = false
}