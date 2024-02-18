# import libraries
import json
import requests

# define endpoint and credentials
api_key = 'gc3m2IlVWsyn6BB1gB14qahVwUvJBr84CpNx4iRs84e31GATGQLvYAT2Rn/4pUFXKn5Nb6+0LXevU09k'
api_secret = 'U30h5XzvIoiXTH8CqQdDdy1FQUvfDVg2uwQtqYP59UIohZ1hBbdsTmyYsVdDPv1vqCBvG8In2NF6YG1K'
url = 'http://192.168.1.1/api/core/firmware/status'

# request data
r = requests.get(url,
                 verify=False,
                 auth=(api_key, api_secret))

if r.status_code == 200:
    response = json.loads(r.text)

    if response['status'] == 'ok':
        print('OPNsense can be upgraded')
        print('download size : %s' % response['download_size'])
        print('number of packages : %s' % response['updates'])
        if response['upgrade_needs_reboot'] == '1':
            print('REBOOT REQUIRED')
    elif 'status_msg' in response:
        print(response['status_msg'])
else:
    print('Connection / Authentication issue, response received:')
    print(r.text)