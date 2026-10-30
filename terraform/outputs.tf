output "vpc_id" {
  description = "ID of the banking application VPC"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = module.vpc.private_subnet_ids
}
output "database_endpoint" {
  description = "PostgreSQL database endpoint, or null when disabled"
  value       = try(module.database[0].database_endpoint, null)
}

output "database_port" {
  description = "PostgreSQL database port, or null when disabled"
  value       = try(module.database[0].database_port, null)
}

output "database_id" {
  description = "RDS instance ID, or null when disabled"
  value       = try(module.database[0].database_id, null)
}
