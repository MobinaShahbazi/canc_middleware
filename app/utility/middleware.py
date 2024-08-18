import requests

from app import config


class Middleware:

    access_token = config.app_config.access_token
    base_url = 'http://localhost:8000/v1.0'
    project_location = 'demo:breast-cancer'


    def request_create(self, method, url, body=None):

        request = requests.Request(method, url, json=body)


        return None

    def create_process_instance(self):
        url = f'{self.base_url}/process-instances/{self.project_location}'
        session = requests.Session()
        request = requests.Request('POST', url, json={}, headers={'Authorization': self.access_token})
        prepped = session.prepare_request(request)
        r = session.send(prepped, verify=False)

        # response = requests.post(
        #     url=f'{self.base_url}/process-instances/{self.project_location}',
        #     headers={'Authorization': self.access_token}
        # )
        # result = response.json()
        return r.json()

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


# access_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6InNwaWZmd29ya2Zsb3dfYmFja2VuZF9vcGVuX2lkIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvb3BlbmlkIiwiYXVkIjpbInNwaWZmd29ya2Zsb3ctYmFja2VuZCIsIkpYZVFFeG0wSmhRUEx1bWdIdElJcWY1MmJEYWxIejBxIl0sImlhdCI6MTcyMzk2NjcyNywiZXhwIjoxNzI0MTM5NTI3LCJzdWIiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5Ac3BpZmZ3b3JrZmxvdy5vcmciLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJBZG1pbiJ9.EYalpE1Cx1O9fHmZRmRkW5cS_iPv-7o3nNz7eKXTTei8bnMkfW45h7itKVdqk13dnly3QrX6H4nsJHPNt-BgE8qX4lCv2HXl7rC1M8wCcdzP0T7-qMPNV7hSuvb9WBbgB8RaziAz2ua27nl6K8Eyv1-zOljF5xPx0TX3j8KjeIHjT026O_ZODWCAlXkShso2Iczuzefeyf14JVHpvLn_xYCcAiBCz-WplxHPYioX-WUjRhrQ0C0mfU6IpfCA4gqdhPDowBhERg26o9F_4AtS7fewsy3yCnAL_Qybg6qKPaYevHK4wnKbSbTCAHsF2iC77qqmmKeFkuBJaMoa3gxyqQ'
#
# base_url = 'http://localhost:8000/v1.0'
# project_location = 'demo:breast-cancer'
# mw = Middleware(access_token, base_url, project_location)
# form = {
#     "clinical_assessment": True,
#     "biopsy_hist": 0,
#     "chest_radiotherapy_hist": False,
#     "personal_breast_cancer_hist": False,
#     "personal_ovarian_cancer_hist": False,
#     "personal_pancreatic_cancer_hist": False,
#     "family_hist": False,
#     "risk": "low",
#     "age_of_diagnose": 40,
#     "biopsy_date": 1390,
#     "birth_date": 1340,
#     "radiotherapy_date": 1390
# }
# print(mw.get_result(form))
