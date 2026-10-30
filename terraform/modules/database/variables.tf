variable "project_name" {
  description = "Name of the project used for resource naming"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs where the database can be deployed"
  type        = map(string)
}

variable "database_security_group_id" {
  description = "Security group ID assigned to the database"
  type        = string
}
variable "db_name" {
  description = "Name of the PostgreSQL database"
  type        = string
}

variable "db_username" {
  description = "Master username for the PostgreSQL database"
  type        = string
  default     = "bankadmin"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Allocated database storage in GB"
  type        = number
  default     = 20
}