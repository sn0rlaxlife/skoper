import os
import sys
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource import PolicyClient
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.monitor import MonitorManagementClient
import click
from click import echo, style
from dotenv import load_dotenv
from datetime import datetime, timedelta
from tabulate import tabulate
import json
import pandas as pd

load_dotenv()

tenant_id = os.environ.get("TENANT_ID")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
subscription_id = os.environ.get("SUBSCRIPTION_ID")

credential = ClientSecretCredential(tenant_id, client_id, client_secret)
subscription_client = SubscriptionClient(credential)
monitor_client = MonitorManagementClient(credential, subscription_id)

# Get the subscription
try: 
    subscription = (subscription_id)
    print("Subscription found in the account. Continuing...")
    subscription_id = (subscription_id)
except StopIteration:
    print("ERROR: No subscription found in the account. Exiting...")
    sys.exit()


@click.command()
@click.option('--policies', prompt=True, help='List all policies assigned to the subscription', required=True)
def get(policies):
    policy_details = []
    if policies:
        policy_client = PolicyClient(credential, subscription_id)
        try: 
            policy_finder = policy_client.policy_assignments.list()
            for policy in policy_finder:
                metadata = policy.metadata
                if metadata and len(metadata) > 1 and metadata.get('assignedBy'):
                    assigned_by = metadata.get('assignedBy')
                    paramaterscopes = str(metadata.get('parameterScopes'))
                    policy_details.append({
                        "Name": policy.display_name,
                        "Description": policy.description,
                        "ID": policy.id,
                        "Assigned by": assigned_by,
                        "Parameter Scopes": paramaterscopes
                    })
        except Exception as e:
            click.echo(f"An error occurred: {e}")
            sys.exit(1)
        requirements = click.prompt('Do you want list the defined policies? (y/n)', type=str)
        if requirements.lower() == 'y':
           define_policy()
        else:
            pass
        monitoring = click.prompt('List the monitored the policies? (y/n)', type=str)
        if monitoring.lower() == 'y':
           risky_signins()
        else:
            pass
        subscription_settings_finder = click.prompt('Do you want to list subscription operations? (y/n)', type=str)
        if subscription_settings_finder.lower() == 'y':
            list_subscription_operations(subscription_id)
        else:
            pass
# List operations related to subscription (if exists)       
def list_subscription_operations(subscription_id):
    findings = subscription_client.operations.list()
    filtered_findings = [finding for finding in findings if any(term in finding.name.lower() for term in ["create", "delete", "write", "update"])]

    # Prepare the data for the table
    table_data_findings = []
    for finding in filtered_findings:
        cleaned_data = {
            "Name": finding.name
        }
        table_data_findings.append(cleaned_data)
    
    if not table_data_findings:
        click.echo("No relevant subscription operations found!")
    else:
        # Create a DataFrame from the table data
        df_filter = pd.DataFrame(table_data_findings)
        click.echo(click.style(df_filter, fg='green'))

# Checks alerts related to subscription (if exists)
# Get the risky sign-ins from the past day.
def risky_signins():
    start_time = datetime.now() - timedelta(days=1)
    end_time = datetime.now()
    filter = "eventTimestamp ge {} and eventTimestamp le {}".format(start_time, end_time)        
    activity_logs = monitor_client.activity_logs.list(filter=filter, select='eventTimestamp,resourceId,operationName,category,caller,properties')

    # Prepare the data for the table
    table_data_activity = []
    for log in activity_logs:
        operation_name = log.operation_name.value
        if any(term in operation_name.lower() for term in ["write", "delete", "create","update"]):
            cleaned_data = {
                "Operation Name": operation_name,
                "Caller": log.caller,
                "Properties": log.properties['eventCategory'] # Convert LocalizableString to string
            }
            table_data_activity.append(cleaned_data)
    if not activity_logs:
        click.echo("No risky sign-ins found in subscription!")
    else:
        # Create a DataFrame from the table data
        df_activity = pd.DataFrame(table_data_activity)
        # Print the table
        click.echo(click.style(df_activity, fg='green'))
##def list_policy_manifests(subscription_id):
##    policy_client = PolicyClient(credential, subscription_id)
##    policy_manifests = policy_client.data_policy_manifests.get_by_policy_mode(policy_mode="Indexed")
##    for policy in policy_manifests:
##        click.echo(click.style(f"Name: {policy.policy_mode}\n{policy.is_built_in_only}\nEnforcement: {policy.effects}", fg='red'))
        
# Checks policies related to subscription in assignments (if exists)
def define_policy(): 
    try:
        policy_client = PolicyClient(credential, subscription_id)
        policy_listing = policy_client.policy_assignments.list(filter="atScope()", top=500) 
        # Prepare the data for the table
        table_data_policy = []
        for policy in policy_listing:
            data = {
                "Name": policy.display_name,
                "Description": policy.description,
                "Enforcement": policy.enforcement_mode
            }
            table_data_policy.append(data)
        
        if not table_data_policy:
            click.echo(click.style("No policy assignments found!", fg='blue'))
        else:
            # Create a DataFrame from the table data
            df_policy = pd.DataFrame(table_data_policy)
            
            # Print the table
            click.echo(click.style(df_policy, fg='green'))
    except Exception as e:
        click.echo(f"An error occurred: {e}")
        sys.exit()


if __name__ == "__main__":
    get()
    define_policy()
