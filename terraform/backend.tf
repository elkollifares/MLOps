terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate-ca"
    storage_account_name = "tfstatemlopsmtl001"
    container_name       = "tfstate"
    key                  = "mlops-dev.terraform.tfstate"
  }
}
