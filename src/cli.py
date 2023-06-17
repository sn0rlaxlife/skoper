import click

@click.group()
def cli():
    """Cloud Security Posture Management Tool"""
    pass

@click.command()
@click.option('--scan', default=1, help='Provide a scan of resources')
@click.option('--summary', prompt='Summary??', help='Provide a summary of the scan output')

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