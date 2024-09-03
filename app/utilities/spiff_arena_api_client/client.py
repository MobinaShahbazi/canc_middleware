import requests
import logging
from .auth import is_token_expired
from .get_token import get_token_instance


class SpiffArenaAPIClient:

    def __init__(self, settings):
        self.base_api_url = settings.spiff_arena_base_api_url
        self.base_url = settings.spiff_arena_base_url

        if not settings.spiff_arena_token:
            self.token = self.get_token()
            self.access_token = self.token['access_token']
        else:
            self.access_token = settings.spiff_arena_token

        # TODO: Project location or modified_process_group_id should be passed to the client on method calls.
        # project_location = app_config.project_location
        request_result = ''

    def get_token(self):
        auth = get_token_instance
        auth.backend_base_url = self.base_url
        try:
            self.token = auth.get_auth_token()
            logging.log(level=logging.INFO, msg='BPMN service token obtained successfully')
        except Exception as e:
            logging.log(level=logging.ERROR, msg='An error occured in obtaining Spiff Arena token')
            raise
        # self.token = auth.token
        self.access_token = self.token['access_token']

    def check_token(func):
        def wrapper(self, *args, **kwargs):
            if is_token_expired(self.access_token, self.base_api_url):
                logging.log(level=logging.WARNING, msg="BPMN Service token expired, obtaining a new one.")
                self.get_token()

        return wrapper

    # TODO this should be decorated with check_token as soon as getting token directly from spiff arena works
    def http_request(self, method, url, body=None):
        full_url = f'{self.base_api_url}/{url}'
        request = requests.Request(method, full_url, json=body, headers={'Authorization': self.access_token})
        prepared = request.prepare()
        with requests.Session() as session:
            response = session.send(prepared)
        return response.json()


    def direct_call(self, name, body):
        response = requests.post(
            url=f'{self.base_api_url}/messages/{name}?execution_mode=synchronous',
            headers={'Authorization': self.access_token, 'Content-Type': 'application/json'},
            json=body
        )
        results = response.json()
        return results

    def create_process_instance(self, modified_process_model_identifier):
        url = f'process-instances/{modified_process_model_identifier}'
        results = self.http_request(method='POST', url=url)
        return results

    def get_process_instances(self, process_model_identifier):
        url = f'process-instances'
        body = {
            "report_metadata":
                {
                    "columns": [],
                    "filter_by": [
                        {
                            "field_name": "process_model_identifier",
                            "field_value": process_model_identifier
                        }
                    ],
                    "order_by": []
                }

        }
        results = self.http_request(method='POST', url=url, body=body)
        return results

    # def create_process_instance(self):
    #     # url = f'{self.base_api_url}/process-instances/{self.project_location}'
    #     # session = requests.Session()
    #     # request = requests.Request('POST', url, json={}, headers={'Authorization': self.access_token})
    #     # prepped = session.prepare_request(request)
    #     # r = session.send(prepped, verify=False)
    #
    #     response = requests.post(
    #         url=f'{self.base_api_url}/process-instances/{self.project_location}',
    #         headers={'Authorization': self.access_token}
    #     )
    #     result = response.json()
    #     return result

    def run_process_instance(self, result_create):
        response_run = requests.post(
            url=f'{self.base_api_url}/process-instances/{self.project_location}/{result_create["id"]}/run',
            headers={'Authorization': self.access_token}
        )

    def trigger_process(self, result_create):
        response_trigger = requests.get(
            url=f'{self.base_api_url}/tasks?process_instance_id={result_create["id"]}',
            headers={'Authorization': self.access_token}
        )
        result_trigger = response_trigger.json()
        return result_trigger

    def put_data(self, form, result_create, result_trigger):
        response_put = requests.put(
            url=f'{self.base_api_url}/tasks/{result_create["id"]}/{result_trigger["results"][0]["id"]}',
            headers={'Authorization': self.access_token},
            json=form
        )
        response_put.raise_for_status()
        result_put = response_put.json()
        return result_put

    def get_task_data(self, result_create, result_put):
        response_task_data = requests.get(
            url=f'{self.base_api_url}/task-data/{self.project_location}/{result_create["id"]}/{result_put["id"]}',
            headers={'Authorization': self.access_token}
        )
        result_task_data = response_task_data.json()
        return result_task_data["data"]

    def get_result(self, form):
        result_create = self.create_process_instance()
        self.run_process_instance(result_create)
        result_trigger = self.trigger_process(result_create)
        result_put = self.put_data(form, result_create, result_trigger)
        answer = self.get_task_data(result_create, result_put)
        return answer
