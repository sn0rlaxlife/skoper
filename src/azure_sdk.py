from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
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

# Example usage
compute_client, network_client = authenticate()
vms = get_virtual_machines(compute_client)
networks = get_networks(network_client)
roles = get_virtual_machines(compute_client)

# Print the retrieved data
print("Virtual Machines:")
for vm in vms:
    print(vm)

print("\nNetworks:")
for network in networks:
    print(network)
print("Roles being utilized")
for role in roles:
    print(role)