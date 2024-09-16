import requests
import logging


class CancClient:

    def __init__(self, settings):
        self.base_api_url = settings.canc_base_api_url
        self.base_url = settings.canc_base_url
        self.user = settings.canc_user
        self.password = settings.canc_password
        self.access_token = None
        self.get_token()


    def get_token(self):
        url = f'{self.base_api_url}/auth/authenticate'
        result = requests.post(url=url, json={'mobile': self.user, 'otpPassword': self.password}).json()
        self.access_token = result['body'].get('apiToken')
        return None

    @staticmethod
    def check_token(func):
        def wrapped(self, *args, **kwargs):
            result = self.http_request(method='POST', url='auth/verify-token')
            if result['status'] != 'SUCCESS':
                logging.log(level=logging.WARNING, msg="Canc authentication failed...")
                self.get_token()
            return func(self, *args, **kwargs)

        return wrapped

    def http_request(self, method, url, body=None):
        full_url = f'{self.base_api_url}/{url}'
        request = requests.Request(method, full_url, json=body, headers={'Authorization': f'Bearer {self.access_token}'})
        prepared = request.prepare()
        with requests.Session() as session:
            response = session.send(prepared)
        return response.json()

    @check_token
    def get_screening_data(self):
        results = self.http_request(url='screening/list', method='GET')
        return results
