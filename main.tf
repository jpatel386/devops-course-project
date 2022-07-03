terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 2.49"
    } 
  }
}
provider "azurerm" {
  features {

  }
}
data "azurerm_resource_group" "main" {
  name     = "devops-todo-app"
}

resource "azurerm_app_service_plan" "main" {
  name                = "todoapp-jaigeneric-plan"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Basic"
    size = "B1"
  } 
}

resource "azurerm_app_service" "main" {
  name                = "todoapp-jaigeneric"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|jaisalpatel836/todo_app:latest"
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "mongo_db_connection" = resource.azurerm_cosmosdb_account.main.connection_strings[0]
    "mongo_db_name" = "todo_app"
    "SECRET_KEY" = "secret-key"
    "git_client_id" = var.git_client_id
    "git_client_secret" = var.git_client_secret
  } 
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "todoapp-jai-cosmosdb-account"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = true

  capabilities {
    name = "EnableAggregationPipeline"
  }

  capabilities {
    name = "mongoEnableDocLevelTTL"
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "todoapp-jai-cosmosdb-mongo-db"
  resource_group_name = resource.azurerm_cosmosdb_account.main.resource_group_name
  account_name        = resource.azurerm_cosmosdb_account.main.name

  lifecycle { 
    prevent_destroy = true 
  }
}