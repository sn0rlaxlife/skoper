import click
from azure_sdk import authenticate, get_virtual_machines, get_networks



@click.group()
def cli():
    """Cloud Security Posture Management Tool"""
    pass

@click.command()
@click.option('--scan', default=1, help='Provide a scan of resources')
def retrieve_data():
    """Retrieve virtual machines and networks"""
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

@click.option('--scan', default=1, help='Provide a scan of resources')
def scancom(scan, summary):
    """Command for logic 1."""
    pass


@click.command()
@click.option('--scan', default=1, help='Provide a scan of resources')
@click.option('--summary', prompt='Summary??', help='Provide a summary of the scan output')
def summarycom(scan, summary):
    """Command for logic 2."""
    pass



if __name__ == '__main__':
    cli()