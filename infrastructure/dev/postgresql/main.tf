provider "aws" {
  region = "eu-north-1"
  profile = "bonfire"
}

terraform {
  backend "s3" {
    bucket         = "bonfire-terraform-state"
    dynamodb_table = "terraform-state-lock-dynamo"
    encrypt        = true
    region         = "eu-north-1"
    key            = "dev.postgresql.terraform.tfstate"
    profile        = "bonfire"

  }
}

data "terraform_remote_state" "app" {
  backend = "s3"

  config = {
    bucket  = "bonfire-terraform-state"
    key     = "dev.api.terraform.tfstate"
    region  = "eu-north-1"
    profile = "bonfire"
  }
}

variable "db_password" {
  description = "Password for dev database"
}

module "dev_database" {
  source = "../../modules/aws/postgresql"

  instance_class      = "db.t3.micro"
  environment         = "dev"
  db_password         = var.db_password
  app_security_group  = data.terraform_remote_state.app.outputs.app_sg
  project             = "bonfire"
}
