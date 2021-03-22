import requests
import json
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')

ucd_api_base_url = config['default']['ucd_api_base_url']
ucd_username = config['default']['ucd_username']
ucd_password = config['default']['ucd_password']
ucd_max_wait_seconds = config['default']['ucd_max_wait_seconds']
ucd_polling_interval_seconds = config['default']['ucd_polling_interval_seconds']

def application_process_request(application, application_process, environment):
    data = {
        "application": application,
        "applicationProcess": application_process,
        "environment": environment,
        "onlyChanged": "false"
    }
    json_data = json.dumps(data)
    request = requests.put(ucd_api_base_url + '/cli/applicationProcessRequest/request', verify=False, auth=(ucd_username, ucd_password), data = json_data)
    response = json.loads(request.text)
    return response['requestId']

def check_application_process_request_status(requestID):
    request = requests.get(ucd_api_base_url + '/cli/applicationProcessRequest/requestStatus?request=' + requestID, verify=False, auth=(ucd_username, ucd_password))
    response = json.loads(request.text)
    return response['result']

def wait_until_status_succeeded(application, application_process, environment):
    requestID = application_process_request(application, application_process, environment)
    time_slept = 0
    while time_slept < ucd_max_wait_seconds:
        status = check_application_process_request_status(requestID)
        if status == 'SUCCEEDED':
            exit(0)
        time.sleep(ucd_polling_interval_seconds)
        time_slept = time_slept + ucd_polling_interval_seconds
    exit(1)

wait_until_status_succeeded(application='JenkinsTest', application_process='ApplicationProcess1', environment='TEST-ENVIRONMENT')