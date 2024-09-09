import requests
import logging
import json
from .auth import is_token_expired, get_token_instance
from app.utilities.input_management import reform_info

class SpiffArenaAPIClient:

    def __init__(self, settings):
        self.base_api_url = settings.spiff_arena_base_api_url
        self.base_url = settings.spiff_arena_base_url
        self.project_location = 'canc:test'                   # change
        self.token = self.get_token()

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
        self.access_token = self.token['access_token']

    @staticmethod
    def check_token(func):
        def wrapped(self, *args, **kwargs):
            if is_token_expired(self.access_token, self.base_api_url):
                logging.log(level=logging.WARNING, msg="BPMN Service token expired, obtaining a new one.")
                self.get_token()
            return func(self, *args, **kwargs)

        return wrapped

    @check_token
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

    def get_process_instances(self, modified_process_model_identifier):
        url = f'process-instances'
        body = {
            "report_metadata":
                {
                    "columns": [],
                    "filter_by": [
                        {
                            "field_name": "modified_process_model_identifier",
                            "field_value": modified_process_model_identifier
                        }
                    ],
                    "order_by": []
                }

        }
        results = self.http_request(method='POST', url=url, body=body)
        return results

    def trigger_process(self, instance_id):
        response_trigger = requests.get(
            url=f'{self.base_api_url}/tasks?process_instance_id={instance_id}',
            headers={'Authorization': self.access_token}
        )
        result_trigger = response_trigger.json()
        return result_trigger

    def put_data(self, form, instance_id, task_id):
        response_put = requests.put(
            url=f'{self.base_api_url}/tasks/{instance_id}/{task_id}',
            headers={'Authorization': self.access_token},
            json=form
        )
        response_put.raise_for_status()
        result_put = response_put.json()
        return result_put

    def get_task_data(self, instance_id, task_id):
        response_task_data = requests.get(
            url=f'{self.base_api_url}/task-data/{self.project_location}/{instance_id}/{task_id}',
            headers={'Authorization': self.access_token}
        )
        result_task_data = response_task_data.json()
        return result_task_data["data"]

    def start_bpmn(self, input_obj):
        result_direct = self.direct_call('start', {})
        instance_id = result_direct['process_instance']['id']

        # the process instance id should be saved

        result_ready = self.trigger_process(instance_id)
        task_id = result_ready["results"][0]["id"]

        self_assessment_data = reform_info(input_obj)

        self.put_data(self_assessment_data, instance_id, task_id)
        data = self.get_task_data(instance_id, self.get_end_event_id(instance_id))
        return json.dumps(data)

    def get_process_instance_status(self, instance_id):
        response = requests.get(
            url=f'{self.base_api_url}/process-instances/{self.project_location}/{instance_id}',
            headers={'Authorization': self.access_token}
        )
        result = response.json()
        return result["status"]

    def get_end_event_id(self, instance_id):
        response = requests.get(
            url=f'{self.base_api_url}/process-instances/{self.project_location}/{instance_id}/task-info',
            headers={'Authorization': self.access_token}
        )
        tasks = response.json()
        for task in tasks:
            if task["typename"] == "EndEvent":
                end_event_id = task['guid']
        return end_event_id
