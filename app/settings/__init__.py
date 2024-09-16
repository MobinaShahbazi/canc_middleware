import logging
import os
from dotenv import load_dotenv

from .base_setting_mixin import BaseSettingMixin
from .common_settings import CommonSettings
from .database_settings import DatabaseSettings
from .spiff_arena_settings import SpiffArenaConnectorSettings
from .canc_settings import CancConnectorSettings

from app.utilities import SpiffArenaAPIClient, CancClient

__env_file_path = BaseSettingMixin.get_env_file_path(BaseSettingMixin.get_selected_env(os.environ.get("APP_ENV_NAME")))
load_dotenv(__env_file_path)


class ServiceSettings(
    BaseSettingMixin,
    CommonSettings,
    DatabaseSettings,
    SpiffArenaConnectorSettings,
    CancConnectorSettings
):
    pass


app_config = ServiceSettings()
app_config.setup(__env_file_path)

try:
    spiff_client = SpiffArenaAPIClient(settings=app_config)
except Exception as e:
    raise Exception('Error connecting to BPMN services')

try:
    canc_client = CancClient(settings=app_config)
except Exception as e:
    print(e.__str__())
    raise Exception('Error connecting to CANC services')


logging.log(level=logging.INFO, msg='Application settings successfully initialized')
