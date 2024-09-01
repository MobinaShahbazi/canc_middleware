import logging
import requests


def is_token_expired(token):
    response = requests.get(
        url=f'{config.app_config.base_url}/process-models',
        headers={'Authorization': token}
    )
    result = response.json()
    if 'status_code' in result and result['status_code'] == 401:
        return True
    else:
        return False
