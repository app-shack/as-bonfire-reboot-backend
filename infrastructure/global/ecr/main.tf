provider "aws" {
  region  = "eu-north-1"
  profile = "bonfire"
}

terraform {
  backend "s3" {
    bucket         = "bonfire-terraform-state"
    dynamodb_table = "terraform-state-lock-dynamo"
    encrypt        = true
    region         = "eu-north-1"
    key            = "global.ecr.terraform.tfstate"
    profile        = "bonfire"
  }
}

module "ecr" {
  source = "../../modules/aws/ecr"

  project = "bonfire"
}
