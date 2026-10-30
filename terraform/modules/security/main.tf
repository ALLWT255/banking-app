resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  description = "Security group for the Application Load Balancer"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${var.project_name}-alb-sg"
  }
}
resource "aws_vpc_security_group_ingress_rule" "alb_https" {
  security_group_id = aws_security_group.alb.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}
resource "aws_security_group" "backend" {
  name        = "${var.project_name}-backend-sg"
  description = "Security group for the banking application backend"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${var.project_name}-backend-sg"
  }
}
resource "aws_vpc_security_group_ingress_rule" "backend_from_alb" {
  security_group_id = aws_security_group.backend.id

  referenced_security_group_id = aws_security_group.alb.id

  from_port   = var.backend_port
  to_port     = var.backend_port
  ip_protocol = "tcp"
}
resource "aws_security_group" "database" {
  name        = "${var.project_name}-database-sg"
  description = "Security group for the banking application database"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${var.project_name}-database-sg"
  }
}
resource "aws_vpc_security_group_ingress_rule" "database_from_backend" {
  security_group_id = aws_security_group.database.id

  referenced_security_group_id = aws_security_group.backend.id

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"
}
resource "aws_vpc_security_group_egress_rule" "alb_to_backend" {
  security_group_id = aws_security_group.alb.id

  referenced_security_group_id = aws_security_group.backend.id

  from_port   = var.backend_port
  to_port     = var.backend_port
  ip_protocol = "tcp"
}
resource "aws_vpc_security_group_egress_rule" "backend_to_database" {
  security_group_id = aws_security_group.backend.id

  referenced_security_group_id = aws_security_group.database.id

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"
}
resource "aws_vpc_security_group_egress_rule" "backend_https" {
  security_group_id = aws_security_group.backend.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}
resource "aws_vpc_security_group_ingress_rule" "alb_http_dev" {
  count = var.enable_dev_http_listener ? 1 : 0

  security_group_id = aws_security_group.alb.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 80
  to_port     = 80
  ip_protocol = "tcp"
}
