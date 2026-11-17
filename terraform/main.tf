module "vpc" {
  source = "./modules/vpc"

  project_name = var.project_name
  vpc_cidr     = var.vpc_cidr

  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets
}

module "security" {
  source = "./modules/security"

  enable_dev_http_listener = var.enable_dev_http_listener

  project_name = var.project_name
  vpc_id       = module.vpc.vpc_id
}

module "database" {
  count  = var.enable_database ? 1 : 0
  source = "./modules/database"

  project_name               = var.project_name
  private_subnet_ids         = module.vpc.private_subnet_ids
  database_security_group_id = module.security.database_security_group_id

  db_name = var.db_name
}

module "iam" {
  source       = "./modules/iam"
  project_name = var.project_name

  enable_database = var.enable_database

  database_secret_arn = var.enable_database ? module.database[0].database_master_secret_arn : null

  jwt_secret_arn = var.jwt_secret_arn
}

module "compute" {
  source = "./modules/compute"

  depends_on = [
    module.iam,
    module.vpc,
    module.security
  ]

  enable_dev_http_listener = var.enable_dev_http_listener

  project_name = var.project_name

  vpc_id                = module.vpc.vpc_id
  public_subnet_ids     = module.vpc.public_subnet_ids
  alb_security_group_id = module.security.alb_security_group_id

  private_subnet_ids        = module.vpc.private_subnet_ids
  backend_security_group_id = module.security.backend_security_group_id

  ecs_execution_role_arn = module.iam.ecs_execution_role_arn
  ecs_task_role_arn      = module.iam.ecs_task_role_arn

  db_host             = var.enable_database ? module.database[0].database_endpoint : null
  db_port             = var.enable_database ? module.database[0].database_port : 5432
  db_name             = var.enable_database ? var.db_name : null
  database_secret_arn = var.enable_database ? module.database[0].database_master_secret_arn : null

  jwt_secret_arn = var.jwt_secret_arn
}