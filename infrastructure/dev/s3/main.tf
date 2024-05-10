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
    key            = "dev.s3.terraform.tfstate"
    profile        = "bonfire"
  }
}

module "dev_media" {
  source = "../../modules/aws/s3"

  environment = "dev"
  project = "bonfire"
}
