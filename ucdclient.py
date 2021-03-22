import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ucd_api_base_url = config['default']['ucd_api_base_url']
ucd_username = config['default']['ucd_username']
ucd_password = config['default']['ucd_password']
ucd_max_wait_seconds = config['default']['ucd_max_wait_seconds']

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
        
    exit(1)

# data = {
#     "application": "JenkinsTest",
#     "description": "Requesting deployment to OpenShift Test Env",
#     "applicationProcess": "ApplicationProcess1",
#     "environment": "TEST-ENVIRONMENT",
#     "onlyChanged": "false"
# }

# json_data = json.dumps(data)

# r = requests.put('https://192.168.0.220/cli/applicationProcessRequest/request', verify=False, auth=('user1', 'P@ssw0rd'), data = json_data)
# print(r.text)


# r = requests.get('https://192.168.0.220/cli/applicationProcessRequest/178591e5-29f3-5538-2848-35ff91ca618b', verify=False, auth=('user1', 'P@ssw0rd'))
# json_data = json.loads(r.text)
# print(json_data)
# print(json_data['result'])


# r = requests.get('https://192.168.0.220/cli/applicationProcessRequest/requestStatus?request=17859401-10b0-da1f-b61d-db33e93d88c4', verify=False, auth=('user1', 'P@ssw0rd'))
# json_data = json.loads(r.text)
# print(json_data)
# print(json_data['result'])

# {'status': 'CLOSED', 'result': 'SUCCEEDED', 'duration': 4388}
# {'status': 'CLOSED', 'result': 'FAULTED', 'duration': 10363}