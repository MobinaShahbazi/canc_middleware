from rabitpy.errors import JsonError
import numpy as np
from datetime import datetime
import pandas as pd
import json
from rabitpy.io.resources import RabitData, RabitMetadata, RabitDataset, RabitProject
from rabitpy.io.adapters import RabitReaderAPIAdapter, RabitDatabaseAdapter
import warnings
import requests
from datetime import date, timedelta
from sqlalchemy import create_engine


def read_sql_file(path):
    sql_file = open(path, 'r')
    query = sql_file.read()
    query = query.replace('\n', " ")
    sql_file.close()
    return query

def convert(o):
    """
    function on how to convert other values to json
    """
    if isinstance(o, np.int64):
        return int(o)
    if isinstance(o, datetime):
        return str(o)
    if isinstance(o, np.bool_):
        if o:
            return True
        else:
            return False
    if pd.isna(o):
        return None
    if o is np.ma.masked:
        return None
    try:
        json.dumps(o)
    except ValueError as e:
        raise JsonError(str(e).split(' ')[0], type=True)


def remap_opts(rd):

    rdct = rd.md[['fldCode', 'optVal', 'optText']].groupby(by='fldCode') \
        .apply(lambda x: dict(zip(x['optVal'], x['optText']))).to_dict()
    rd.data.df['json'] = rd.df['json'].apply(lambda x: {k: rdct.get(k, {}).get(v, v) for k, v in x.items()})

    return rd


def to_sumit(uid, raw_data, n_metadata):
    data = raw_data
    current_datetime = datetime.now()
    modified = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    DBIO = "http://127.0.0.1:5500"
    resp_dict = {'data': data, 'raw_data': raw_data, 'n_metadata': n_metadata, 'metadata': n_metadata,
                 'uid': uid, 'last_modified': datetime.strptime(str(modified), "%Y-%m-%d %H:%M:%S.%f"), 'report': [],
                 'project_name': 'sjs_checklist'}
    try:
        resp_dict = json.loads(json.dumps(resp_dict, default=convert, sort_keys=False).replace('"None"', 'null')
                               .replace('NaN', 'null').replace('nan', 'null'), strict=False)
    except JsonError as e:
        print('Error 400 - Json')
    print("prepairng to send request!")
    print("request sent!")
    requests.post(f'{DBIO}/add_entry/{uid}', json=resp_dict)


def get_equipment_data(connection_string):
    query_bi = read_sql_file("./sql/query_bi.sql")
    queried = RabitDatabaseAdapter(url=connection_string, query=query_bi)

    try:
        fetched = queried.fetch()
        base_info_data = pd.DataFrame(fetched)
    except ValueError as e:
        warnings.warn(f'Reader fetch method returned malformed or empty response with error 400')

    query_bi_org = read_sql_file("./sql/query_bi_organization.sql")
    queried = RabitDatabaseAdapter(url=connection_string, query=query_bi_org)

    try:
        fetched = queried.fetch()
        base_info_data_org = pd.DataFrame(fetched)
    except ValueError as e:
        warnings.warn(f'Reader fetch method returned malformed or empty response with error 400')

    base_info_data = pd.concat([base_info_data, base_info_data_org])
    equipment_survey_query = read_sql_file("./sql/equipment_survey.sql")
    equipment_data_query = read_sql_file("./sql/equipment_data.sql")

    md_reader = RabitDatabaseAdapter(url=connection_string,
                                     query=equipment_survey_query)
    d_reader = RabitDatabaseAdapter(url=connection_string,
                                    query=equipment_data_query)

    md_obj = RabitMetadata(source='db', reader=md_reader, fid_path='survey_id', frm_desc_path='survey_description',
                           frm_name_path='survey_name', json_path='survey_json',
                           include_html=False,
                           base_info_data=base_info_data)

    entry_index_fields = [{'name': 'pid', 'alias': 'pid', 'dtype': 'str'},
                          {'name': 'created_by', 'alias': 'qid', 'dtype': 'str'},
                          {'name': 'survey_id', 'alias': 'frmCode', 'dtype': 'str'},
                          {'name': 'modified_date', 'alias': 'last_modified'},
                          {'name': 'filldate', 'alias': 'fillDate', 'dtype': 'str'}]

    d_obj = RabitData(source='db', reader=d_reader, fid_path='survey_id', json_path='survey_respond', content_path=None,
                      frm_name_path='survey_name', frm_desc_path='survey_description', index_fields=entry_index_fields,
                      use_fields=['title'])

    rd = RabitDataset(data=d_obj, metadata=md_obj)
    rd.load(cache=True)

    rd = remap_opts(rd)
    df_data = rd.data.df

    #TODO: add organ_title

    # df_data['organ_id'] = df_data['json'].apply(lambda x: x['organ_id'])

    # get organization data
    # organ_query = read_sql_file('../sql/organization.sql')
    # organization = pd.read_sql(sql=organ_query, engine = create_engine(connection_string))

    # df_data = df_data.merge(organization, left_on='organ_id', right_on="gid")
    # df_data['json'] = df_data.apply(add_info_json, axis=1)

    raw_data = df_data.to_dict(orient='records')
    n_metadata = rd.metadata.mdn.to_dict(orient='records')

    if not n_metadata:
        print('Error 400 - No metadata')

    if not raw_data:
        raw_data = None

    # data = raw_data
    uid = 'cf93a0bb-4d3f-44f9-8459-f1ccad1800a3'

    to_sumit(uid, raw_data, n_metadata)
    return None


def add_info_json(row):
    json_data = row['json']
    org_title = row['org_title']
    org_prov = row['province']
    org_city = row['city']

    json_data['org_title'] = org_title
    json_data['org_prov'] = org_prov
    json_data['org_city'] = org_city

    return json_data

def get_equipment_checklist_data(connection_string):

    query_bi = read_sql_file("./sql/query_bi.sql")
    queried = RabitDatabaseAdapter(url=connection_string, query=query_bi)

    try:
        fetched = queried.fetch()
        base_info_data = pd.DataFrame(fetched)
    except ValueError as e:
        warnings.warn(f'Reader fetch method returned malformed or empty response with error 400')

    query_bi_org = read_sql_file("./sql/query_bi_organization.sql")
    queried = RabitDatabaseAdapter(url=connection_string, query=query_bi_org)

    try:
        fetched = queried.fetch()
        base_info_data_org = pd.DataFrame(fetched)
    except ValueError as e:
        warnings.warn(f'Reader fetch method returned malformed or empty response with error 400')

    base_info_data = pd.concat([base_info_data, base_info_data_org])
    equipment_survey_query = read_sql_file("./sql/equipment_checklist_survey.sql")
    equipment_data_query = read_sql_file('./sql/equipment_checklist_data.sql')

    md_reader = RabitDatabaseAdapter(url=connection_string,
                                     query=equipment_survey_query)

    d_reader = RabitDatabaseAdapter(url=connection_string,
                                    query=equipment_data_query)

    md_obj = RabitMetadata(source='db', reader=md_reader, fid_path='survey_id', frm_desc_path='survey_description',
                           frm_name_path='survey_name', json_path='survey_json',
                           include_html=False, base_info_data=base_info_data)

    entry_index_fields = [{'name': 'equipment_id', 'alias': 'pid', 'dtype': 'str'},
                          {'name': 'created_by', 'alias': 'qid', 'dtype': 'str'},
                          {'name': 'survey_id', 'alias': 'frmCode', 'dtype': 'str'},
                          {'name': 'modified_date', 'alias': 'last_modified'},
                          {'name': 'filldate', 'alias': 'fillDate', 'dtype': 'str'}]

    d_obj = RabitData(source='db', reader=d_reader, fid_path='survey_id', json_path='survey_respond', content_path=None,
                      frm_name_path='survey_name', frm_desc_path='survey_description', index_fields=entry_index_fields,
                      use_fields=['title'])

    rd = RabitDataset(data=d_obj, metadata=md_obj)
    rd.load()

    rd = remap_opts(rd)
    df_data = rd.data.df
    df_data['ins_date'] = df_data.apply(get_ins_date, axis=1)
    df_data.sort_values(['pid', 'ins_date'], inplace=True)
    gbos = df_data.groupby(['pid'])
    ret_list = list(map(check_last_inspection, [gbo for index, gbo in gbos]))
    df_data = pd.concat(ret_list)
    ix = df_data['last_ins_date'] == df_data['ins_date']
    df_data.loc[ix, 'last_ins'] = True
    df_data['json'] = df_data.apply(add_info_ins, axis=1)
    #TODO: delete this
    df_data['last_modified'] = df_data['fillDate']
    raw_data = df_data.to_dict(orient='records')
    n_metadata = rd.metadata.mdn.to_dict(orient='records')

    if not n_metadata:
        print('Error 400 - No metadata')

    if not raw_data:
        raw_data = None

    # data = raw_data
    uid = '8f1e61b1-df86-43de-aa93-5fd8a5e4383a'
    to_sumit(uid, raw_data, n_metadata)

    return None

def get_ins_date(row):
    json_data = row['json']
    try:
        ins_date = json_data['ins_date']
    except:
        ins_date = np.nan
    return ins_date

def check_last_inspection(gbo):
    last_ins_date = gbo.iloc[-1]['ins_date']
    gbo['last_ins_date'] = last_ins_date
    gbo['last_ins'] = False
    return gbo

def add_info_ins(row):
    json_data = row['json']
    last_ins_date = row['last_ins_date']
    last_ins = row['last_ins']
    json_data['last_ins_date'] = last_ins_date
    json_data['last_ins'] = last_ins
    return json_data


