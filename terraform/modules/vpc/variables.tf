variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "project_name" {
  description = "Name of the project used for resource naming"
  type        = string
}
variable "public_subnets" {
  description = "Map of Availability Zones to public subnet CIDR blocks"
  type        = map(string)
}

variable "private_subnets" {
  description = "Map of Availability Zones to private subnet CIDR blocks"
  type        = map(string)
}
