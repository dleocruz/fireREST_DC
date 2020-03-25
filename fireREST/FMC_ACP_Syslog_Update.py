# import required dependencies
from __future__ import print_function
import fireREST
from fireREST import Client

# set variables for execution. Make sure your credentials are correct, ACP exists and syslog alert definition exists
device = '10.34.4.73'
username = 'Cisco_d3'
password = 'Prueba1234'
domain = 'Global'
policy = 'IPS-MEXICO'
syslog_alert_id = 'Splunk'

# Initialize a new api object
api = Client(hostname=device, username=username, password=password)

# Get IDs for specified acp and syslog alert. API PK = UUID, so we have to find the matching api object for the name
# specified.

acp_id = api.get_acp_id_by_name(policy)
acp_rules = api.get_acp_rules(acp_id, expanded=True)
for response in acp_rules:
        for acp_rule in response.json()['items']:
                print('rule {0} in policy {1}...'.format(acp_rule['name'], acp_id))
                payload = acp_rule
                print(payload)
                del payload['metadata']
                del payload['links']
                print(payload)

                # set syslog
                payload['syslogConfig'] = {
                        'id': syslog_alert_id
                }
                print(payload)
                result = api.update_acp_rule(policy_id=acp_id, rule_id=acp_rule['id'], data=payload)
                # if this update was successful a return code of 200 would be sent
                if result.status_code == 200:
                        print('[SUCCESS]')