from rabitpy.io.resources import RabitData, RabitMetadata, RabitDataset, RabitProject
from rabitpy.io.adapters import RabitReaderAPIAdapter, RabitDatabaseAdapter
import requests
import json
from datetime import datetime
from rabitpy.errors import JsonError
import pandas as pd
import numpy as np
import warnings
from datetime import date, timedelta
from utils.process_func import *

if __name__ == '__main__':
    connection_string = 'postgresql+psycopg2://postgres:postgres@10.1.1.5:5432/sjs'
    get_equipment_data(connection_string)
    get_equipment_checklist_data(connection_string)

