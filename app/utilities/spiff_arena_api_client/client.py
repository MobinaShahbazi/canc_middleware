import os

import requests
from app import config
from app.utility.check_token import is_token_expired
from app.utility.get_token import get_token_instance

# # from check_token import is_token_expired
# from get_token import get_token_instance


class Middleware:
    base_url = config.app_config.base_url
    project_location = config.app_config.project_location

    expired_token: str = 'eyJhbGciOiJSUzI1NiIsImtpZCI6InNwaWZmd29ya2Zsb3dfYmFja2VuZF9vcGVuX2lkIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvb3BlbmlkIiwiYXVkIjpbInNwaWZmd29ya2Zsb3ctYmFja2VuZCIsIkpYZVFFeG0wSmhRUEx1bWdIdElJcWY1MmJEYWxIejBxIl0sImlhdCI6MTcyNDA0ODc2NywiZXhwIjoxNzI0MjIxNTY4LCJzdWIiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5Ac3BpZmZ3b3JrZmxvdy5vcmciLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJBZG1pbiJ9.CukXixVSNq_fZib-YCTn-B-FgAvwX-p1wprZ_MMh5iaOM5nSey83lkV_3vYTbL1ypozqaMnyNAsoDUsv8RLR87jbt3SsMyQUG4sFjYMZPGx2c8n0v2KcePtPRI8toxzjT7KkZ2vJcP1gqi4syBBDqrE0zDjW65ApYML8RaQLOiDF75f5m3Kh-obUn0quRb7aGJlFdKZx8DhUpHz8yvW4EpOyIU-NXCc2hN8qHteVfXoKzlR-2QrFnHV1oPecw9Iuhov6EpWZSTqO-GBB1BwPXLBa6yfD4SosFfscq9yZuzZmhZuqez_D-DJWdP0MRHpnEwoMmpsPli_3XsDWeM5mJg'
    token: str = 'eyJhbGciOiJSUzI1NiIsImtpZCI6InNwaWZmd29ya2Zsb3dfYmFja2VuZF9vcGVuX2lkIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvb3BlbmlkIiwiYXVkIjpbInNwaWZmd29ya2Zsb3ctYmFja2VuZCIsIkpYZVFFeG0wSmhRUEx1bWdIdElJcWY1MmJEYWxIejBxIl0sImlhdCI6MTcyNDQ3OTI1OCwiZXhwIjoxNzI0NjUyMDU5LCJzdWIiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5Ac3BpZmZ3b3JrZmxvdy5vcmciLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJBZG1pbiJ9.YuE4Kf8TjC5Ew3mpsHVOTIYD0lN0IW304sUoDXzwkPFF9s7bNsBzUN2_PCF1OXHUTFDMLwGvC9OLwEfMAhlAP_LYW3veFd9ldH65FsbQPXv_vtHFYZFKj6xyzmDS3T0ieSDVacNDT_YvXzHQzvAdD_wtXP4Eu1vg8MwP6PkbpU7F45IoWtUsgm9wW7sAQQXSC4R7Vlq57ncBo-HVwvoOPfTpgwqNnQoGevnijeR9RNMS083s0N77mKx4SuLTSaqU5-i98bD4SmQ_DiqMcZkgBNqeFdxrLOmahp8odkylsG4fVVwHOdwNr4tU1OjcHgfCDW5JiD5wU7_PrxgrNO0PRg'
    access_token: str = expired_token

    request_result = ''

    def token_handler(func):
        def wrapper(self, *args, **kwargs):
            if is_token_expired(self.access_token):
                print("it is expired")
                get_token_instance.get_auth_token()
                self.access_token = get_token_instance.token
            self.request_result = func(self, *args, **kwargs)
        return wrapper


    def request_create(self, method, url, body=None):
        request = requests.Request(method, url, json=body)


        return None

    def create_process_instance(self):
        # url = f'{self.base_url}/process-instances/{self.project_location}'
        # session = requests.Session()
        # request = requests.Request('POST', url, json={}, headers={'Authorization': self.access_token})
        # prepped = session.prepare_request(request)
        # r = session.send(prepped, verify=False)

        response = requests.post(
            url=f'{self.base_url}/process-instances/{self.project_location}',
            headers={'Authorization': self.access_token}
        )
        result = response.json()
        return result

    def run_process_instance(self, result_create):
        response_run = requests.post(
            url=f'{self.base_url}/process-instances/{self.project_location}/{result_create["id"]}/run',
            headers={'Authorization': self.access_token}
        )

    def trigger_process(self, result_create):
        response_trigger = requests.get(
            url=f'{self.base_url}/tasks?process_instance_id={result_create["id"]}',
            headers={'Authorization': self.access_token}
        )
        result_trigger = response_trigger.json()
        return result_trigger

    def put_data(self, form, result_create, result_trigger):
        response_put = requests.put(
            url=f'{self.base_url}/tasks/{result_create["id"]}/{result_trigger["results"][0]["id"]}',
            headers={'Authorization': self.access_token},
            json=form
        )
        response_put.raise_for_status()
        result_put = response_put.json()
        return result_put

    def get_task_data(self, result_create, result_put):
        response_task_data = requests.get(
            url=f'{self.base_url}/task-data/{self.project_location}/{result_create["id"]}/{result_put["id"]}',
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

    @token_handler
    def direct_call(self, name, body):
        response = requests.post(
            url=f'{self.base_url}/messages/{name}?execution_mode=synchronous',
            headers={'Authorization': self.access_token, 'Content-Type': 'application/json'},
            json=body
        )
        result = response.json()
        return result

# print(os.getenv("BASE_URL"))
# mw = Middleware()
# mw.direct_call('popcorn', {"size": "large"})
# print(mw.request_result)

