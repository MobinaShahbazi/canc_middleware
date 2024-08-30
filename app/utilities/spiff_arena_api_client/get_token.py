import base64
import re
import requests

class GetToken:
    username = "admin"
    password = "admin"
    realm_name = "spiffworkflow"
    OPEN_ID_CODE = ":this_is_not_secure_do_not_use_in_production"
    backend_base_url = "http://host.docker.internal:8000"
    backend_client_id = "spiffworkflow-backend"
    backend_client_secret = "JXeQExm0JhQPLumgHtIIqf52bDalHz0q"
    openid_token_url = None
    keycloak_base_url = None
    token = ''

    def prepare(func):
        def wrapper(self, *args, **kwargs):
            if self.openid_token_url is None:
                if self.keycloak_base_url is not None:
                    if "spiffworkflow.org" in self.backend_base_url:
                        pattern = r".*api\.(\w+\.spiffworkflow.org).*"
                        match = re.search(pattern, self.backend_base_url)
                        if match is None:
                            raise Exception("Could not determine openid url based on backend url")
                        env_domain = match.group(1)
                        self.keycloak_base_url = "https://keycloak.${env_domain}"
                    else:
                        self.keycloak_base_url = self.backend_base_url
                    self.openid_token_url = f"{self.keycloak_base_url}/realms/{self.realm_name}/protocol/openid-connect/token"
                else:
                    self.openid_token_url = f"{self.backend_base_url}/openid/token"
            self.token = func(self, *args, **kwargs)
        return wrapper


    def get_auth_token(self):
        backend_basic_auth_string = f"{self.backend_client_id}:{self.backend_client_secret}"
        backend_basic_auth_bytes = bytes(backend_basic_auth_string, encoding="ascii")
        backend_basic_auth = base64.b64encode(backend_basic_auth_bytes)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {backend_basic_auth.decode('utf-8')}",
        }
        data = {
            "grant_type": "password",
            "code": self.username + self.OPEN_ID_CODE,
            "username": self.username,
            "password": self.password,
            "client_id": self.backend_client_id,
        }
        self.openid_token_url = f"{self.backend_base_url}/openid/token"
        # if self.openid_token_url is None:
        #     raise Exception("Please specify the OPENID_TOKEN_URL")

        response = requests.post(self.openid_token_url, data=data, headers=headers, timeout=15)
        return response.json()


get_token_instance = GetToken()