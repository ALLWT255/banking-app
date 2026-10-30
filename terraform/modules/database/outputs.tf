output "database_endpoint" {
  description = "Connection endpoint for the PostgreSQL database"
  value       = aws_db_instance.main.address
}

output "database_port" {
  description = "Port used by the PostgreSQL database"
  value       = aws_db_instance.main.port
}

output "database_id" {
  description = "ID of the RDS database instance"
  value       = aws_db_instance.main.id
}
