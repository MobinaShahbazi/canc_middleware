import requests
import pandas as pd
import sqlalchemy as sa
from datetime import datetime
import json

province_code = {
    "اردبیل": 'IR-24',
    "اصفهان": 'IR-10',
    "البرز": 'IR-30',
    "ایلام": 'IR-16',
    "آذربایجان شرقی": 'IR-03',
    "آذربایجان غربی": 'IR-04',
    "بوشهر": 'IR-18',
    "تهران": 'IR-23',
    "چهارمحال و بختیاری": 'IR-14',
    "خراسان جنوبی": 'IR-29',
    "خراسان رضوی": 'IR-09',
    "خراسان شمالی": 'IR-28',
    "خوزستان": 'IR-06',
    "زنجان": 'IR-19',
    "سمنان": 'IR-20',
    "سیستان و بلوچستان": 'IR-11',
    "فارس": 'IR-07',
    "قزوین": 'IR-26',
    "قم": 'IR-25',
    "کردستان": 'IR-12',
    "کرمان": 'IR-08',
    "کرمانشاه": 'IR-05',
    "کهگیلویه و بویراحمد": 'IR-17',
    "گلستان": 'IR-27',
    "گیلان": 'IR-01',
    "لرستان": 'IR-15',
    "مازندران": 'IR-02',
    "مرکزی": 'IR-00',
    "هرمزگان": 'IR-22',
    "همدان": 'IR-13',
    "یزد": 'IR-21',
    "خارج از ایران": 'out'

}


def get_smoking_frequency(screening_respond):
    if screening_respond['smoking_history'] == 'false':
        freq = "4"
    elif screening_respond['smoking_history'] == 'before':
        freq = screening_respond['smoking_amount_past']
    elif screening_respond['smoking_history'] == 'now':
        freq = screening_respond['smoking_amount_current']

    return freq


def bmi_state(bmi):
    if bmi <= 18.4:
        return 'Underweight'
    elif 18.4 < bmi and bmi <= 24.9:
        return 'Normal'
    elif 24.9 < bmi and bmi <= 29.9:
        return 'Overweight'
    else:
        return 'Obese'


r = requests.get(url='http://localhost:42420/screenings/breast-cancer/v1/get-data')
df = pd.DataFrame.from_records(r.json())

result_df = pd.DataFrame({
    'height': pd.Series(dtype='int'),
    'weight': pd.Series(dtype='int'),
    'province_iso_code': pd.Series(dtype='str'),
    'child_birth_history': pd.Series(dtype='bool'),
    'smoking_history': pd.Series(dtype='bool'),
    'smoking_frequency': pd.Series(dtype='str'),
    'contraceptive_history': pd.Series(dtype='bool'),
    'clinical_examination_history': pd.Series(dtype='bool'),
    'mammography_history': pd.Series(dtype='bool'),
    'ultrasound_history': pd.Series(dtype='bool'),
    'biopsy_history': pd.Series(dtype='bool'),
    'radiotherapy_history': pd.Series(dtype='bool'),
    'familial_cancer_history': pd.Series(dtype='bool'),
    'self_awareness': pd.Series(dtype='bool'),
    'risk_level': pd.Series(dtype='str'),
    'age': pd.Series(dtype='int'),
    'bmi': pd.Series(dtype='str'),
    'participation_count': pd.Series(dtype='int'),
    'self_assessment_time': pd.Series(dtype='datetime64[ns]'),

})

bool_dict = {'true': True, 'false': False}

print((df.loc[22]['result'][5]))

result_df['clinical_examination_history'] = result_df['clinical_examination_history'].replace({'true': True, 'false': False}).astype(bool)
result_df['mammography_history'] = result_df['mammography_history'].replace({'true': True, 'false': False}).astype(bool)
result_df['ultrasound_history'] = result_df['ultrasound_history'].replace({'true': True, 'false': False}).astype(bool)

for i in range(len(df)):
    for j in range(len(df.loc[i]['result'])):
        screening_respond = df.loc[i]['result'][j]['screeningRespond']
        data = df.loc[i]['result'][j]['data']

        date_string = df.loc[i]['result'][j]['createdDate']
        format_string = "%Y/%m/%d %H:%M"
        datetime_object = datetime.strptime(date_string, format_string)

        self_awareness = screening_respond['clinical_examination_history'] or screening_respond[
            'mammography_history'] or screening_respond['ultrasound_history']

        # familial_hist =
        result_df = result_df._append({
            'height': screening_respond['height'],
            'weight': screening_respond['weight'],
            'province_iso_code': province_code[screening_respond['province']],
            'province': screening_respond['province'],
            'child_birth_history': screening_respond['child_birth_history'],
            'smoking_history': screening_respond['smoking_history'],
            'smoking_frequency': get_smoking_frequency(screening_respond),
            'contraceptive_history': screening_respond['contraceptive_history'],
            'clinical_examination_history': screening_respond['clinical_examination_history'],
            'mammography_history': screening_respond['mammography_history'],
            'ultrasound_history': screening_respond['ultrasound_history'],
            'biopsy_history': screening_respond['biopsy_history'],
            'radiotherapy_history': screening_respond['radiotherapy_history'],
            'familial_cancer_history': screening_respond['familial_cancer_history'],
            'self_awareness': self_awareness,
            'risk_level': int(data['risk_level']),
            'age': data['age'],
            'bmi': bmi_state(
                screening_respond['weight'] / screening_respond['height'] / screening_respond['height'] * 10000),
            'participation_count': len(df.loc[i]['result']),
            'self_assessment_time': datetime_object,
        },
            ignore_index=True)


engine = sa.create_engine("postgresql://postgres:postgres@10.1.1.5:5432/spiffworkflow_result")
result_df['familial_cancer_history'] = result_df['familial_cancer_history'].replace({'true': True, 'false': False}).astype(bool)
result_df['self_awareness'] = result_df['self_awareness'].replace({'true': True, 'false': False}).astype(bool)
result_df['clinical_examination_history'] = result_df['clinical_examination_history'].replace({'true': True, 'false': False}).astype(bool)
result_df['mammography_history'] = result_df['mammography_history'].replace({'true': True, 'false': False}).astype(bool)
result_df.to_sql('canc_breast_cancer_screening_all', con=engine, if_exists='replace')
