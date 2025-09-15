from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku, Kind

import os

# --- CONFIG ---
subscription_id = os.getenv("subscription_id")
resource_group_name = os.getenv("resource_group_name")
storage_account_name = os.getenv("storage_account_name")  # must be globally unique, lowercase only
location = "eastus"

# Authenticate using DefaultAzureCredential (needs `az login` or managed identity)
credential = DefaultAzureCredential()

# Clients
resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)

# 1. Create Resource Group
print(f"Creating resource group '{resource_group_name}'...")
resource_group = resource_client.resource_groups.create_or_update(
    resource_group_name,
    {"location": location}
)
print(f"✅ Resource group '{resource_group_name}' created.")

# 2. Create Storage Account
print(f"Creating storage account '{storage_account_name}'...")
storage_async_operation = storage_client.storage_accounts.begin_create(
    resource_group_name,
    storage_account_name,
    StorageAccountCreateParameters(
        sku=Sku(name="Standard_LRS"),
        kind=Kind.storage_v2,
        location=location
    )
)
storage_account = storage_async_operation.result()
print(f"✅ Storage account '{storage_account_name}' created in '{resource_group_name}'.")
