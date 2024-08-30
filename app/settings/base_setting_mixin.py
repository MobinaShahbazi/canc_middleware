import os
import sys
from pathlib import Path
from pydantic_settings import BaseSettings


class BaseSettingMixin(BaseSettings):

    class Config:
        case_sensitive = False
        validate_assignment = True

    @classmethod
    def get_selected_env(cls, SELECTED_ENV_NAME) -> str:
        if SELECTED_ENV_NAME in ("dev", "stg", "prod", "local", "redirect"):
            env_name = f".env.{SELECTED_ENV_NAME}"
        else:
            env_name = ".env"
        return env_name

    @classmethod
    def get_env_file_path(cls, env_name: str) -> str:
        env_file_path = os.path.join(os.getcwd(), "envs", env_name)
        if not os.path.isfile(env_file_path):
            with open(env_file_path, "w") as f:  # noqa
                pass
        return env_file_path

    def setup(self, from_env: str, **kwargs):
        self.notify_environment(from_env)

    def notify_environment(self, from_env: str):
        print(2 * "\n" + 50 * "-" + "\n")
        print("Your selected environment: ", from_env)
        print("\n\n")
