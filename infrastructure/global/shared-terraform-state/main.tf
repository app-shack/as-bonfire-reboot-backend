provider "aws" {
  region  = "eu-north-1"
  profile = "bonfire"
}

module "shared-terraform-state" {
  source  = "../../modules/aws/shared-terraform-state"
  project = "bonfire"
}
