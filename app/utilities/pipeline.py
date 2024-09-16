import requests
import pandas as pd
import sqlalchemy as sa

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

r = requests.get(url='http://localhost:42420/screenings/breast-cancer/v1/get-data')
df = pd.DataFrame.from_records(r.json())

result_df = pd.DataFrame({
    'height': pd.Series(dtype='int'),
    'weight': pd.Series(dtype='int'),
    'province_iso_code': pd.Series(dtype='str'),
    'child_birth_history': pd.Series(dtype='bool'),
    'smoking_history': pd.Series(dtype='bool'),
    'contraceptive_history': pd.Series(dtype='bool'),
    'clinical_examination_history': pd.Series(dtype='bool'),
    'mammography_history': pd.Series(dtype='bool'),
    'ultrasound_history': pd.Series(dtype='bool'),
    'biopsy_history': pd.Series(dtype='bool'),
    'radiotherapy_history': pd.Series(dtype='bool'),
    'familial_cancer_history': pd.Series(dtype='bool'),
    'risk_level': pd.Series(dtype='str'),
})
print((df.loc[9]['result'][0]['screeningRespond']))
for i in range(len(df)):
    for j in range(len(df.loc[i]['result'])):
        result_df = result_df._append({
                            'height': df.loc[i]['result'][j]['screeningRespond']['height'],
                            'weight': df.loc[i]['result'][j]['screeningRespond']['weight'],
                            'province_iso_code': province_code[df.loc[i]['result'][j]['screeningRespond']['province']],
                            'child_birth_history': df.loc[i]['result'][j]['screeningRespond']['child_birth_history'],
                            'smoking_history': df.loc[i]['result'][j]['screeningRespond']['smoking_history'],
                            'contraceptive_history': df.loc[i]['result'][j]['screeningRespond']['contraceptive_history'],
                            'clinical_examination_history': df.loc[i]['result'][j]['screeningRespond']['clinical_examination_history'],
                            'mammography_history': df.loc[i]['result'][j]['screeningRespond']['mammography_history'],
                            'ultrasound_history': df.loc[i]['result'][j]['screeningRespond']['ultrasound_history'],
                            'biopsy_history': df.loc[i]['result'][j]['screeningRespond']['biopsy_history'],
                            'radiotherapy_history': df.loc[i]['result'][j]['screeningRespond']['radiotherapy_history'],
                            'familial_cancer_history': df.loc[i]['result'][j]['screeningRespond']['familial_cancer_history'],
                            'risk_level': int(df.loc[i]['result'][j]['data']['risk_level']),
                        },
                        ignore_index=True)


engine = sa.create_engine("postgresql://postgres:postgres@10.1.1.5:5432/spiffworkflow_result")
result_df.to_sql('canc_breast_cancer_screening_all', con=engine, if_exists='replace')