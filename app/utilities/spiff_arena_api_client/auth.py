import logging
import requests

def is_token_expired(token, base_url):
    response = requests.get(
        url=f'{base_url}/process-models',
        headers={'Authorization': token}
    )
    result = response.json()
    if 'status_code' in result and result['status_code'] == 401:
        return True
    else:
        return False
