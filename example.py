# import required dependencies
from __future__ import print_function
from fireREST import FireREST

# set variables for execution. Make sure your credentials are correct, ACP exists and syslog alert definition exists
loglevel = 'DEBUG'
device = 'fmc.example.com'
username = 'admin'
password = 'Cisco123'
domain = 'Global'
policy = 'lab-policy'
syslog_alert = 'syslog-server'

# Initialize a new api object
api = FireREST(device=device, username=username, password=password, loglevel=loglevel)

# Get IDs for specified acp and syslog alert. API PK = UUID, so we have to find the matching api object for the name
# specified.

acp_id = api.get_acp_id_by_name(policy)
syslog_alert_id = api.get_syslogalert_id_by_name(syslog_alert)

# Get all access control rules for the access control policy specified
acp_rules = api.get_acp_rules(acp_id, expanded=True, domain=domain)

# Loop through HTTP response objects
for response in acp_rules:
    # Loop through access control rules in http response object
    for acp_rule in response.json()['items']:
        # Only change syslog settings if no syslog alert configuration exists
        if 'syslogConfig' not in acp_rule:
            # Get the existing rule configuration
            payload = acp_rule
            # Set syslog configuration
            payload['syslogConfig'] = {
                    'id': syslog_alert_id
            }
            # Remove metadata fields from existing rule. This is required since the API does not support
            # PATCH operations as of version 6.2.1 of FMC. Thats why we have to delete metadata before we use a PUT operation to change our ACP rule
            del payload['metadata']
            del payload['links']
            print('Trying set syslog server for rule {0} in policy {1}...'.format(acp_rule['name'], policy))
            # Send json payload to FMC REST API
            result = api.update_acp_rule(policy_id=acp_id, rule_id=acp_rule['id'], data=payload, domain=domain)
            # Verify that the PUT operation has been successful
            if result.status_code == 200:
                print('[SUCCESS]')
            else:
                print('[ERROR] Could not update syslog settings.')
        else:
            print('Syslog configuration for rule {0} in policy {1} already exists. Skipping.'.format(acp_rule['name'], policy))