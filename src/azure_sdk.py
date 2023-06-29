from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.authorization import AuthorizationManagementClient
import os
from os import path

def authenticate():
    """
    Authenticates with Azure using the DefaultAzureCredential.

    Returns:
        object: An authenticated Azure client.
    """
    credential = DefaultAzureCredential()
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    compute_client = ComputeManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)
    authorization = AuthorizationManagementClient(credential, subscription_id)

    return compute_client, network_client

def get_virtual_machines(compute_client):
    """
    Retrieves a list of virtual machines from Azure.

    Args:
        compute_client (object): Azure ComputeManagementClient object.

    Returns:
        list: A list of virtual machine names.
    """

    roles = compute_client.cloud_services.list_all()
    roles_names = [role.name for role in roles]

    vm_list = compute_client.virtual_machines.list_all()
    vm_names = [vm.name for vm in vm_list]

    ## grab compute operations using the operations model in the compute client
    compute_ops = compute_client.operations.list()
    ## iterate over the operations and print out the name and display name
    origins, names, display_names = [op.origin for op in compute_ops], [op.name for op in compute_ops], [op.display_name for op in compute_ops]

    ssh_keys = compute_client.ssh_public_keys.list_by_subscription()
    ssh_key_names = [ssh_key.name for ssh_key in ssh_keys]

    return vm_names
    return roles_names
def get_networks(network_client):
    """
    Retrieves a list of networks from Azure.

    Args:
        network_client (object): Azure NetworkManagementClient object.

    Returns:
        list: A list of network names.
    """
    network_list = network_client.virtual_networks.list_all()
    network_names = [network.name for network in network_list]

    return network_names
def get_access_settings(authorization):
    """
    Retrieves a list of access settings from Azure.

    Args:
        authorization (object): Azure AuthorizationManagementClient object.

    Returns:
        list: A list of access settings.
    """
    credential = DefaultAzureCredential()
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    authorization = AuthorizationManagementClient(credential, subscription_id)

    access_list = authorization.role_definitions.list(scope=f"/subscriptions/{subscription_id}/")
                                                      
    access_settings = [access.name for access in access_list]
    role_definitions_list = [access.type for access in access_list]

    permissions_list = authorization.permissions.list_for_resource_group(resource_group_name='aks-calico-west')
    permissions_lookup = [permissions.name for permissions in permissions_list]

    return access_settings
    return permissions_lookup

# Example usage
compute_client, network_client = authenticate()
access_authorization = authenticate()
vms = get_virtual_machines(compute_client)
networks = get_networks(network_client)
roles = get_virtual_machines(compute_client)
origins = get_virtual_machines(compute_client)
names = get_virtual_machines(compute_client)
display_names = get_virtual_machines(compute_client)
ssh_key_names = get_virtual_machines(compute_client)
access_list = get_access_settings(access_authorization)

# Print the retrieved data
print("Virtual Machines:")
for vm in vms:
    print(vm)

print("\nNetworks:")
for network in networks:
    print(network)

print("\nOperations:-------------------")
print(f'{origins}, {names}, {display_names}')
print(f'{ssh_key_names}')

print("---------Roles being utilized----------")
for role in roles:
    print(role)

print("---------Access Settings----------")
for access_settings in access_list:
    print(access_list)
