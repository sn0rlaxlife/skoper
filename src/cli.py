import click
import azure_sdk
from azure_sdk import authenticate, get_virtual_machines, get_networks, get_access_settings



@click.group()
def cli():
    """Cloud Security Posture Management Tool"""
    pass

@click.command()
@click.option('--scan', default=1, help='Provide a scan of resources')
def retrieve_data():
    """Retrieve virtual machines and networks"""
    with open('azure_sdk.py', 'r') as f:
        compute_client, network_client = authenticate()
        vms = get_virtual_machines(compute_client)
        networks = get_networks(network_client)

    # Use the retrieved data as needed
    click.echo("Virtual Machines:")
    for vm in vms:
        click.echo(vm)

    click.echo("\nNetworks:")
    for network in networks:
        click.echo(network)

    click.echo("\nOperations:-------------------")
    for origin in origins:
        click.echo(origin)
    for name in names:
        click.echo(name)
    for display_name in display_names:
        click.echo(display_name)

@click.option('--scan', default=1, help='Provide a scan of resources')
def scancom(scan, summary):
    """Command for logic 1."""
    pass

##resource scanning
@click.command()
def scan_resources_permissions():
    with open('azure_sdk.py', 'r') as f:
        authorization = authenticate()
        access_settings = get_access_settings(authorization)
    resource_group = click.prompt("Enter the resource group name, you'd like to scan", type=str)
    if resource_group == len(resource_group) > 0:
        click.echo("Resource group name is valid")
    else:
        click.echo("Resource group name is invalid")
    resource_group_scanning = (f"The following permissions are listed {permissions_lookup}")

@click.command()
@click.option('--scan', default=1, help='Provide a scan of resources')
@click.option('--summary', prompt='Summary??', help='Provide a summary of the scan output')
def summarycom(scan, summary):
    """Command for logic 2."""
    pass



if __name__ == '__main__':
    cli()