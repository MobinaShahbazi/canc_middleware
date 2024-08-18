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


def get_equipment_data():

    query_bi = '''
        SELECT
            bi.code AS "varCode",
            bid.code,
            bid.title 
        FROM
            base_info bi
            INNER JOIN base_info_detail AS bid ON bi.pid = bid.base_info_id
        ORDER BY
            "varCode"
    '''

    queried = RabitDatabaseAdapter(url='postgresql+psycopg2://postgres:postgres@10.1.1.5:5432/sjs', query=query_bi)

    try:
        fetched = queried.fetch()
        base_info_data = pd.DataFrame(fetched)
    except ValueError as e:
        warnings.warn(f'Reader fetch method returned malformed or empty response with error 400')

    equipment_survey_query = '''select distinct s.gid::varchar as survey_id, s."name"::varchar as survey_name,
                                s.description::varchar as survey_description,
                                s.survey_json::jsonb from equipment e 
                                inner join equipment_form ef on ef."type" = e."type" 
                                left join survey s on ef.survey_id = s.gid 
                                where s.deleted = False '''

    equipment_data_query = '''select distinct e.pid, s.gid::varchar as survey_id, e.survey_respond::jsonb,
                              e.title,
                              e.created_by_user_id::varchar as created_by, e.modified_date::timestamp,
                              e.created_date ::varchar as fillDate from equipment e 
                              inner join equipment_form ef on ef."type" = e."type" 
                              left join survey s on ef.survey_id = s.gid 
                              where s.deleted = False '''

    md_reader = RabitDatabaseAdapter(url="postgresql+psycopg2://postgres:postgres@10.1.1.5:5432/sjs",
                                     query=equipment_survey_query)
    d_reader = RabitDatabaseAdapter(url="postgresql+psycopg2://postgres:postgres@10.1.1.5:5432/sjs",
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
    rd.load()

    rd = remap_opts(rd)
    df_data = rd.data.df

    raw_data = df_data.to_dict(orient='records')
    n_metadata = rd.metadata.mdn.to_dict(orient='records')

    if not n_metadata:
        print('Error 400 - No metadata')

    if not raw_data:
        raw_data = None

    # data = raw_data
    uid = 'cf93a0bb-4d3f-44f9-8459-f1ccad1800a3'

    to_sumit(uid, raw_data, n_metadata)

def get_equipment_checklist_data():

    query_bi = '''
            SELECT
                bi.code AS "varCode",
                bid.code,
                bid.title 
            FROM
                base_info bi
                INNER JOIN base_info_detail AS bid ON bi.pid = bid.base_info_id
            ORDER BY
                "varCode"
        '''

    queried = RabitDatabaseAdapter(url='postgresql+psycopg2://postgres:postgres@10.1.1.5:5432/sjs', query=query_bi)

    try:
        fetched = queried.fetch()
        base_info_data = pd.DataFrame(fetched)
    except ValueError as e:
        warnings.warn(f'Reader fetch method returned malformed or empty response with error 400')

    # equipment_survey_query = '''select distinct s.gid::varchar as survey_id, s."name"::varchar as survey_name,
    #                             s.description::varchar as survey_description,
    #                             s.survey_json::jsonb from survey s
    #                             left join equipment_checklist ec on ec.survey_id = s.gid
    #                             where s.deleted = False'''
    equipment_survey_query = '''select distinct s.gid::varchar as survey_id, s."name"::varchar as survey_name,
                                     s.description::varchar as survey_description,
                                     s.survey_json::jsonb from survey s
                                     left join equipment_checklist ec on ec.survey_id = s.gid
                                     where s.gid in ('44e5c0d9-24bf-447c-a770-98c7d2d2e076',    
                                                     '1b02db7f-122e-4192-acf7-38f0b90747ba',
                                                     '062b4cd6-440c-4a86-8f99-29493221b842',
                                                     '9804d912-dfc3-4fd7-8799-8bcd9e224ffd',
                                                     '5cbfc69b-fd52-4676-a15b-8ce7a265e34c',
                                                     'ae5cf01e-105d-4c65-a8c6-9d7452d009b3',
                                                     '329166a7-a2da-49a9-af17-ac8e6551da5f',
                                                     '6465d559-61c6-4f5b-af53-84e6fd743708',
                                                     '8984de6a-9360-4129-a560-8d0d216c7dfd',
                                                     '7e67ff41-7c61-4b74-a2d2-76e1e0311438',
                                                     'fea627be-57e5-40b5-a431-48392a44027d',
                                                     '9222e3c8-b0a8-4e05-a5d7-efc7e9c721c8')'''
    # and s.gid = '0271422a-fe60-4695-84c5-931d30880229' or s.gid = '78a644da-41eb-4253-a308-0668c852ab2f'

    equipment_data_query = '''select ecr.equipment_id::int,
                                ec.survey_id::varchar as survey_id,
                                ecr.survey_respond::jsonb,
                                ecr.created_by_user_id::varchar as created_by,
                                ecr.modified_date::varchar,
                                ecr.created_date::varchar as fillDate,
                                ecr.plan_id,
								ep.period,
								ep.time_unit
                                from equipment_checklist_respond ecr
                                left join equipment_checklist ec on ec.pid = ecr.check_list_id
                                left join equipment_checklist_plan ep on ep.pid = ecr.plan_id
                                where survey_id in (select distinct s.gid::varchar as survey_id from survey s
                                where s.deleted = False)'''

    md_reader = RabitDatabaseAdapter(url="postgresql+psycopg2://postgres:postgres@10.1.1.5:5432/sjs",
                                     query=equipment_survey_query)

    d_reader = RabitDatabaseAdapter(url="postgresql+psycopg2://postgres:postgres@10.1.1.5:5432/sjs",
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
                      use_fields=['period', 'time_unit'])

    rd = RabitDataset(data=d_obj, metadata=md_obj)
    rd.load()

    rd = remap_opts(rd)
    df_data = rd.data.df
    df_data['json'] = df_data.apply(add_info, axis=1)
    df_data['ins_date'] = df_data['json'].apply(lambda d: d['ins_date'])
    df_data.sort_values(['pid', 'ins_date'], inplace=True)
    gbos = df_data.groupby(['pid'])
    ret_list = list(map(check_last_inspection, [gbo for index, gbo in gbos]))
    df_data = pd.concat(ret_list)
    ix = df_data['last_ins_date'] == df_data['ins_date']
    df_data.loc[ix, 'last_ins'] = True
    df_data['json'] = df_data.apply(add_info_ins, axis=1)


    raw_data = df_data.to_dict(orient='records')
    n_metadata = rd.metadata.mdn.to_dict(orient='records')

    if not n_metadata:
        print('Error 400 - No metadata')

    if not raw_data:
        raw_data = None

    # data = raw_data
    uid = 'cf93a0bb-4d3f-44f9-8459-f1ccad1800a4'
    to_sumit(uid, raw_data, n_metadata)

    return None

def check_last_inspection(gbo):
    last_ins_date = gbo.iloc[-1]['ins_date']
    gbo['last_ins_date'] = last_ins_date
    gbo['pervious_ins_date'] = gbo['ins_date'].shift(1)
    gbo['last_ins'] = False
    return gbo

def add_info_ins(row):
    json_data = row['json']
    pervious_ins_date = row['pervious_ins_date']
    last_ins_date = row['last_ins_date']
    last_ins = row['last_ins']
    json_data['last_ins_date'] = last_ins_date
    json_data['pervious_ins_date'] = pervious_ins_date
    json_data['last_ins'] = last_ins
    return json_data

def add_info(row):
    json_data = row['json']
    ins_date = json_data['ins_date']
    ins_date_split = ins_date.split('-')
    ins_date = date(int(ins_date_split[0]), int(ins_date_split[1]), int(ins_date_split[2]))
    period = json_data['period']
    time_unit = json_data['time_unit']

    if time_unit == 'MONTH':
        time = 30 * period

    elif time_unit == 'YEAR':
        time = 365 * period

    elif time_unit == 'DAY':
        time = 1 * period

    elif time_unit == 'WEEK':
        time = 7 * period

    next_ins_date = ins_date + timedelta(time)
    json_data['next_ins_date'] = next_ins_date.strftime('%Y-%m-%d')
    return json_data


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
                               .replace('NaN', 'null'), strict=False)
    except JsonError as e:
        print('Error 400 - Json')
    print("prepairng to send request!")
    print("request sent!")
    requests.post(f'{DBIO}/add_entry/{uid}', json=resp_dict)


if __name__ == '__main__':

    get_equipment_data()
    get_equipment_checklist_data()

