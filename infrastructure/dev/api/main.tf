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
    key            = "dev.api.terraform.tfstate"
    profile        = "bonfire"
  }
}

variable "public_ssh_key" {
  description = "Public RSA key used for SSH access to server"
  default     = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDH3f0sqt8biZBreyLM+D89vlKD80JVicJMHaqOVV0M7itj2zeiNjyAqCAyLqG/vSmaFQ2viWs7pXkka6OWy9grh3JDSEYEs2V5sKmyAl94dztn6n9irCAfMMe5ax3+5gxhTsWp03dDl3ExAr/fldkWtC32DILx/7ROrx/PSrYeUEka8rWIyz3Pq+CHL/ngtOBdYkFR4EgrNo4qjSDAgS6d51U1w1jL9d6IOCTUrIKOtiPaNsxZiuxzQ8aryeMtHQsEcDBRBmkehz5s/RHh+9jMZUdt6nZDX/s0kba2Ali96HgVr/M0pgNvQsvhbhzohBp3KJrf1JW0/HgPLNp+wQK8dSKvk7Px9UYKWr8qETeIgcxazh0Z7g4Jko1VWyeoPS0pLbkixMcd6pQ9cI1tnzWTPpWLtbeRiRcU7owbrdwvze22CviFlNhE4CRVXajRV11qrl10X020vFDt6VKH6WFPuvAv/YcUeIb+GP/KMSK2U8GWTEViMWauuh/9lZU6c08= antonrundberg@MacBook-Pro"
}

module "dev_application" {
  source = "../../modules/aws/api"

  environment       = "dev"
  ec2_instance_type = "t3.medium"
  ami               = "ami-09f8f28c19052e51f" # Ubuntu Server 22.04 eu-north-1
  public_ssh_key    = var.public_ssh_key
}

output "ip" {
  value = module.dev_application.ip
}

output "app_sg" {
  value = module.dev_application.app_sg
}
