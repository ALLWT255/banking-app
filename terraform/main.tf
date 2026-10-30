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

  vpc_id = module.vpc.vpc_id
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
  source = "./modules/iam"

  project_name = var.project_name
}
module "compute" {
  source = "./modules/compute"

  enable_dev_http_listener = var.enable_dev_http_listener

  project_name = var.project_name

  vpc_id                = module.vpc.vpc_id
  public_subnet_ids     = module.vpc.public_subnet_ids
  alb_security_group_id = module.security.alb_security_group_id

  private_subnet_ids        = module.vpc.private_subnet_ids
  backend_security_group_id = module.security.backend_security_group_id

  ecs_execution_role_arn = module.iam.ecs_execution_role_arn
  ecs_task_role_arn      = module.iam.ecs_task_role_arn
}
