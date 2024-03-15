import os
from azure.common.credentials import ServicePrincipalCredentials
from flask import Flask, request , render_template
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters, SkuName, Sku, Kind

app = Flask(__name__)
# Variable configuration
# Resource Group Configuration
@app.route('/createstrg')
def CreateStorage():
    resource_group = str(request.args.get('rgname'))
    location = str(request.args.get('regions'))
    storage_account_name = str(request.args.get('storageaccountname'))


    subscription_id = os.environ["subscription_id"]
    client_id = os.environ["client_id"]
    secret = os.environ["secret"]
    tenant = os.environ["tenant"]

    # Create Azure Credential object
    #credentials = ServicePrincipalCredentials(
    #    client_id= client_id,
    #    secret=secret,
    #    tenant=tenant
    #)

    credentials = ClientSecretCredential(
        tenant_id=tenant,
        client_id=client_id,
        client_secret=secret
    )

    client = ResourceManagementClient(credentials, subscription_id)

    # Create Resource Group
    resource_group_param = {"location" : location}
    client.resource_groups.create_or_update(resource_group, resource_group_param)

    params = {
            "sku": {
                "name": "Standard_GRS"
            },
            "kind": "StorageV2",
            "location": location,
            "isHnsEnabled": True,
            "encryption": {
                "services": {
                "file": {
                    "key_type": "Account",
                    "enabled": True
                },
                "blob": {
                    "key_type": "Account",
                    "enabled": True
                }
                },
                "key_source": "Microsoft.Storage"
            },
            "minimum_tls_version": "TLS1_2",
            "tags": {
                "key1": "value1",
                "key2": "value2"
            }
            }
    # Create Azure Storage Account
    storage_account_param =  StorageAccountCreateParameters(sku=Sku(name=SkuName.standard_ragrs), kind="StorageV2", location = location)
    storage_client = StorageManagementClient(credentials, subscription_id)
    storage_async_operation = storage_client.storage_accounts.begin_create(resource_group, storage_account_name, params)
    storage_account = storage_async_operation.result()

if __name__ == "__main__":
    app.run(debug=True)