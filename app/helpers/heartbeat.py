import requests
import datetime
from flask import current_app as app


def send_heartbeat():
    heartbeat_data = {
        'uid': app.config['uid'],
        'agent_version': app.config['AGENT_VERSION'],
        'ipmi_ip': app.config['ipmi_ip'],
        'model': app.config['model'],
        'creds_name': app.config.get('creds_name'),
        'heartbeat_timestamp': datetime.datetime.now().isoformat()
    }
    headers = {
        'Accept': 'application/json'
    }
    url = f"{app.config['vaxiin_server_url']}/api/v1/heartbeat/"

    try:
        res = requests.put(url=url, headers=headers, json=heartbeat_data)
    except Exception as err:
        app.logger.error(f"Failed to send heartbeat. error: '{err}'")
        return True, f"{err}"

    message = res.json().get('message', '')

    failed = False
    if res.status_code == 200:
        app.logger.info("Heartbeat sent succesfully!")
    elif res.status_code < 300:
        app.logger.warn(f"Heartbeat sent but recieved a warning from server: '{message}'")
    else:
        app.logger.error(f"Failed to send heartbeat, message from server: '{message}'")
        failed = True

    return failed, message


def send_interval_heartbeat(a_app):
    with a_app.app_context():
        app.logger.info("Sending Heartbeat by interval..")
        send_heartbeat()
