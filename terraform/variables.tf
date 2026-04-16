variable "location" {
  type    = string
  default = "Canada Central"
}

variable "resource_group_name" {
  type    = string
  default = "rg-mlops-dev-ca"
}

variable "acr_name" {
  type    = string
  default = "acrmlopsmtl001"
}


variable "aks_name" {
  type    = string
  default = "aks-mlops-dev-ca"
}

variable "storage_account_name" {
  type    = string
  default = "stmlopsartifacts001"
}

variable "key_vault_name" {
  type    = string
  default = "kv-mlops-dev-ca-001"
}

variable "databricks_name" {
  type    = string
  default = "dbw-mlops-dev-ca"
}