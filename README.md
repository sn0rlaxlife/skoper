## ReadME

## How to use this repository
<code> git clone https://github.com/sn0rlaxlife/skoper.git </code>
<code> cd skoper </code>

## Build the container if you'd like to not run dependencies 
<code> Work with the use by docker build skoper . </code>


## Configuration
### Accessing via credentials 
<br> As you're well aware the credentials needed for this in Microsoft Azure require the following Security Reader, Global Reader</br>

Set the following environment variables in .env file (this is on the gitignore) with the following variables listed below
  <div>AZURE_SUBSCRIPTION_ID=SubscriptionID</div>
  <div>AZURE_CLIENT_ID=ClientID</div>
  <div>AZURE_TENANT_ID=TenantID</div>
  <div>AZURE_CLIENT_SECRET=GeneratedSecret</div>

## Usage
After cloning the repository and setting credentials you can run setup.py.
<code>python3 setup.py --policies all</code>
This initiates the program with a prompt on defining policies with a yes/no response on the cli (this defines the current subscriptions existing policies), its a good idea to know where you're at prior to enforcement before moving forward. If you don't wish to use this option select "n" this moves to the next prompt on monitoring risky events, this queries the Activity Log API and looks for any activity that is deemed administrative in nature along with the operation listing to pinpoint the access and who was the API caller.