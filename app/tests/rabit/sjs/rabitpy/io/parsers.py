import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import warnings
from collections import OrderedDict
from .validity import _check_coding_validity
from .parser_utils import _get_idx, _flatten_json
import pandas as pd
from rabitpy.utils import timing
from requests.exceptions import ConnectionError


@timing
def _parse_project(p):
    rndct = {'id': 'phaseId', 'name': 'phaseTitle', 'surveyIds': 'frmCode', 'level': 'phaseLevel'}
    cols = ['id', 'name', 'level', 'parentId', 'surveyIds']
    phases = pd.DataFrame().from_records(p.get('phases'), columns=cols, coerce_float=False) \
        .explode('surveyIds')
    phases = phases.loc[phases['parentId'].isna()]
    phases = _set_order(phases, {'id': 'phaseOrder'}).reset_index(drop=True)
    phases.rename(columns=rndct, inplace=True)

    # TODO: Add subphases
    # set phase aliases
    # level_counts = phases['level'].max()
    # for level in range(level_counts):

    output_cols = ['projectId', 'projectName', 'phaseId', 'phaseTitle', 'phaseLevel', 'phaseOrder', 'frmCode']
    dfp = pd.DataFrame().from_records([p], columns=['id', 'projectName'], coerce_float=False) \
        .rename(columns={'id': 'projectId'})
    dfp = dfp.loc[dfp.index.repeat(max([len(phases), 1]))].reset_index(drop=True)
    dfp = dfp.merge(phases, how='outer', left_index=True, right_index=True)

    return dfp[output_cols]


def _set_properties(_qnr=None, _element=None, _choices=None, _fid=None, _frm_name=None, _frm_desc=None, baseurl=None,
                    _include_html=False):
    if _element['type'] == 'html' and not _include_html:
        return []

    # This function parses single elements in a questionnaire
    properties = []

    this = OrderedDict()
    updater = lambda x: properties.append(x) if isinstance(this, OrderedDict) else properties + this

    # Multiple text
    if _element.get('type') == 'multipletext':

        for item in _element.get('items'):
            # copy item into a recursive element
            rec_element = item

            # flatten parent and child element codes
            rec_element.update({'name': '{}_{}'.format(_element.get('name', ''), item.get('name')),
                                'type': 'text',
                                'visibleIf': _element.get('visibleIf'),
                                'fldParentCode': _element.get('name', ''),
                                'fldParentTitle': _translation_handler(s=_element, target='title', alt='')})

            # send the element back to the function and update properties
            this = _set_properties(_qnr=_qnr, _element=rec_element, baseurl=baseurl,
                                   _fid=_fid, _frm_name=_frm_name, _frm_desc=_frm_desc)

            if isinstance(this, dict):
                this['elementType'] = f'multipletext - {this["elementType"]}'
            elif isinstance(this, list):
                for item in this:
                    item['elementType'] = f'multipletext - {item["elementType"]}'

            properties = updater(this.copy())

        return properties

    # Matrix
    if _element.get('type') == 'matrix':

        fldAx = _element.get('rows')
        optAx = _element.get('columns')

        for fld in fldAx:

            fldtmp = {}

            if isinstance(fld, dict):
                fldtmp['name'] = '{}_{}'.format(_element.get('name'), fld.get('value'))
                fldtmp['title'] = '{} - {}'.format(
                    _translation_handler(s=_element, target='title', alt=_element.get('name')),
                    _translation_handler(s=fld, target='text', alt=fld.get('name')))

            elif isinstance(fld, str):
                fldtmp['name'] = '{}_{}'.format(_element.get('name'), fld)
                fldtmp['title'] = fld

            else:
                raise TypeError(f'Matrix row type is {type(fld)} and not dict or string...')

            fldtmp.update({'choices': optAx,
                           'type': 'radiogroup',
                           'visibleIf': _element.get('visibleIf'),
                           'fldParentCode': _element.get('name'),
                           'fldParentTitle': _translation_handler(s=_element, target='title', alt=_element.get('name'))
                           })

            # send the element back to the function and update properties
            this = _set_properties(_qnr=_qnr,
                                   _element=fldtmp,
                                   _choices=_choices,
                                   _fid=_fid,
                                   _frm_name=_frm_name,
                                   _frm_desc=_frm_desc,
                                   baseurl=baseurl)

            if isinstance(this, dict):
                this['elementType'] = f'matrix - {this["elementType"]}'
            elif isinstance(this, list):
                for item in this:
                    item['elementType'] = f'matrix - {item["elementType"]}'

            properties = updater(this.copy())
        return properties

    # Dropdown Matrix
    if _element.get('type') == 'matrixdropdown':

        fldAx = _element.get('rows')
        optAx = _element.get('columns')

        for row in fldAx:

            ttl = _translation_handler(s=_element, target='title', alt=_element.get('name'))
            if isinstance(row, dict):
                parentFldTitle = f"{ttl} - {row.get('text', row.get('value'))}"
                parentFldCode = f"{_element.get('name')}_{row.get('value')}"
            elif isinstance(row, str):
                parentFldTitle = f"{ttl} - {row}"
                parentFldCode = f"{_element.get('name')}_{row}"
            else:
                raise TypeError(f'Matrix row type is {type(row)} and not dict or string...')

            fld = {}

            for col in optAx:
                fld['type'] = col.get('cellType', 'dropdown')
                # TODO: Check visibleIf condition for column and rows and implenet in necessary
                # fld['visibleIf'] = _element.get('visibleIf', None)

                ttl = _translation_handler(s=col, target='title', alt=col.get('name'))
                fld['title'] = f"{parentFldTitle} - {ttl}"
                fld['name'] = f"{parentFldCode}_{col.get('name')}"
                fld['fldParentCode'] = parentFldCode
                fld['fldParentTitle'] = parentFldTitle

                # send the element back to the function and update properties
                this = _set_properties(_qnr=_qnr,
                                       _element=fld,
                                       _choices=_choices,
                                       _fid=_fid,
                                       _frm_name=_frm_name,
                                       _frm_desc=_frm_desc,
                                       baseurl=baseurl)

                if isinstance(this, dict):
                    this['elementType'] = f'matrixdropdown - {this["elementType"]}'
                elif isinstance(this, list):
                    for item in this:
                        item['elementType'] = f'matrixdropdown - {item["elementType"]}'

                properties = updater(this.copy())

        return properties

    # Panel
    if _element.get('type') == 'panel':
        for el in _element.get('elements', []):

            el['name'] = '{}'.format(el.get('name'))
            el['fldParentCode'] = el.get('name')
            el['fldParentTitle'] = _translation_handler(s=el, target='title', alt=el.get('name'))

            this = _set_properties(_qnr=_qnr,
                                   _element=el,
                                   _fid=_fid,
                                   _choices=_extract_choices(_el=el, baseurl=baseurl),
                                   _frm_name=_frm_name,
                                   _frm_desc=_frm_desc,
                                   baseurl=baseurl)

            if isinstance(this, dict):
                this['elementType'] = f'panel - {this["elementType"]}'
            elif isinstance(this, list):
                for item in this:
                    item['elementType'] = f'panel - {item["elementType"]}'

            properties = updater(this.copy())
        return properties

    # Dynamic Matrix
    if _element.get('type') == 'matrixdynamic':
        warnings.warn('Dynamic matrix parsing is currently experimental...')
        optAx = _element.get('columns')

        parentFldTitle = f"{_translation_handler(s=_element, target='title', alt=_element.get('name'))}"
        parentFldCode = f"{_element.get('name')}_r1"
        fld = {}

        for col in optAx:
            fld['type'] = col.get('cellType', 'dropdown')

            # TODO: Check visibleIf condition for column and rows and implement if necessary
            # fld['visibleIf'] = _element.get('visibleIf', None)

            fld['title'] = f"{parentFldTitle} - {_translation_handler(s=col, target='title', alt=col.get('name'))}"
            fld['name'] = f"{parentFldCode}_{col.get('name')}"

            # send the element back to the function and update properties
            this = _set_properties(_qnr=_qnr,
                                   _element=fld,
                                   _choices=_extract_choices(_el=col, baseurl=baseurl),
                                   _fid=_fid,
                                   _frm_name=_frm_name,
                                   _frm_desc=_frm_desc,
                                   baseurl=baseurl)

            if isinstance(this, dict):
                this['elementType'] = f'matrixdynamic - {this["elementType"]}'
            elif isinstance(this, list):
                for item in this:
                    item['elementType'] = f'matrixdynamic - {item["elementType"]}'

            properties = updater(this.copy())

        return properties

    # Dynamic panel
    if _element.get('type') == 'paneldynamic':
        warnings.warn('Dynamic panel parsing is currently experimental...')
        for el in _element.get('templateElements', []):
            el['name'] = '{}_r1_{}'.format(_element.get('name'), el.get('name'))
            this = _set_properties(_qnr=_qnr,
                                   _element=el,
                                   _fid=_fid,
                                   _choices=_extract_choices(_el=el, baseurl=baseurl),
                                   _frm_name=_frm_name,
                                   _frm_desc=_frm_desc,
                                   baseurl=baseurl)

            if isinstance(this, dict):
                this['elementType'] = f'paneldynamic - {this["elementType"]}'
            elif isinstance(this, list):
                for item in this:
                    item['elementType'] = f'paneldynamic - {item["elementType"]}'

            properties = updater(this.copy())
        return properties

    # set common properties, the type property is set here once and if necessary it will be reset in later steps
    this['frmCode'] = _fid
    this['frmName'] = _frm_name
    this['frmDesc'] = _frm_desc
    this['fldCode'] = _element.get('name')
    this['fldTitle'] = _translation_handler(_element, 'title', _element.get('name'))
    this['fldParentCode'] = _element.get('fldParentCode', this['fldCode'])
    this['fldParentTitle'] = _element.get('fldParentTitle', this['fldTitle'])
    this['elementType'] = _element.get('type')
    this['visibleCondition'] = _element.get('visibleIf', '')
    this['expression'] = _element.get('expression', '')
    this['validators'] = _element.get('validators')
    this['optVal'] = None
    this['optText'] = None
    this['opt'] = None

    # set data type for field
    if this.get('elementType') == 'text':
        if _element.get('inputType', '') == 'number':
            this.update({'dType': 'numeric'})
        elif _element.get('inputType', '') == 'date':
            this.update({'dType': 'datetime'})
        elif _element.get('inputType', '') == 'date-jalali':
            this.update({'dType': 'jalalidate'})
        else:
            this.update({'dType': 'str'})

    if this.get('elementType') == 'expression':
        this.update({'dType': 'numeric'})

    elif this.get('elementType') in ['comment', 'html', 'file']:
        this.update({'dType': 'str'})

    elif this.get('elementType') in ['radiogroup', 'dropdown', 'rating', 'boolean']:
        this.update({'dType': 'category'})

    elif this.get('elementType') in ['checkbox', 'tagbox']:
        this.update(({'dType': 'bool'}))

    # deal with input types which have choice element
    if _choices is not None and this.get('elementType') not in ['matrixdropdown', 'matrixdynamic']:
        parentFldTitle = this.get('fldTitle')
        parentFldCode = this.get('fldCode')
        opt = []

        for _choice in _choices:
            # set value and label of choice
            if isinstance(_choice, dict):
                chValue = str(_choice.get('value')).strip()
                chText = _translation_handler(_choice, 'text', _choice.get('value'))
            else:
                chValue = str(_choice).strip()
                chText = str(_choice).strip()

            # update name and field code of checkbox type quesitons, update and continue
            if this.get('elementType') == 'checkbox':
                this.update({'fldTitle': '{} - {}'.format(parentFldTitle, chText),
                             'fldCode': '{}_{}'.format(parentFldCode, chValue)})

                this.update({'optVal': chValue, 'optText': chText})
                updater(this.copy())
                continue

            this.update({'optVal': chValue, 'optText': chText})
            updater(this.copy())

        if opt:
            updater(this.copy())

    else:
        updater(this.copy())

    # Add 'other' option if it is active
    if _element.get('hasOther'):
        this.pop('optVal')
        this.pop('optText')
        this.update({'dType': 'str', 'elementType': 'text', 'fldCode': '{}_{}'.format(_element['name'], 'comment')})
        this.update({'fldTitle': '{} - {}'.format(parentFldTitle, this.get('otherText', 'other'))})
        updater(this.copy())

    return properties


def _extract_choices(_el, baseurl=None, base_info_data=None):
    if _el.get('type') == 'boolean':
        return [{'value': True, 'text': _el.get('labelTrue', 'Yes')},
                {'value': False, 'text': _el.get('labelFalse', 'No')}]

    if _el.get('choices', _el.get('rateValues')):
        return _el.get('choices', _el.get('rateValues'))

    if _el.get('choicesByUrl') or _el.get('choicesByDynamicUrl'):

        c = []

        value_name = _el.get('valueName', 'code')
        title_name = _el.get('titleName', 'title')

        url = _el.get('choicesByUrl', _el.get('choicesByDynamicUrl')).get('url').split('&')[0]
        try:
            # This works for url of format /api/vars&code=varcode
            code = \
            _el.get('choicesByUrl', _el.get('choicesByDynamicUrl')).get('url').split('?')[1].split('&')[0].split('=')[1]
        except IndexError:
            # This works for url of format /api/vars/varcode
            code = _el.get('choicesByUrl', _el.get('choicesByDynamicUrl')).get('url').split('/')[1]

        if isinstance(base_info_data, pd.DataFrame):
            if code in base_info_data['varCode'].to_list():
                r = base_info_data.loc[base_info_data['varCode'] == code, [value_name, title_name]] \
                    .to_dict(orient='records')
        else:
            if url.startswith('/'):
                baseurl = 'http://sjs-api.vista-group.ir'
                url = baseurl + url

            retry_strategy = Retry(connect=1)
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session = requests.Session()
            session.mount(prefix='https://', adapter=adapter)
            session.mount(prefix='http://', adapter=adapter)

            try:
                print(f'Extracting choices from {url}')
                access_token = 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY5MDg4NTA2OCwiaWF0IjoxNjkwMjgwMjY4fQ.IaQKiY05o-uuGZig63d64azMaI1-bukT6YKQJlAGcGNljB62kUamzHLvUZEoTxAIV_DiD7phjoyhNVMjwR6fPA'
                headers = {'Authorization': f'{access_token}'}
                response = session.get(url, headers=headers, verify=False, timeout=2)
                r = response.json()
            except ConnectionError as e:
                warnings.warn(f'Failed to extract choices from {url}. Check if address exists.')
                return []
            except requests.exceptions.JSONDecodeError:
                print(f'Error extracting choice data from {url}')

        try:
            for item in r:
                # item['value'] = item.pop(value_name)
                # item['text'] = item.pop(title_name)
                record = {}
                record['value'] = item['id']
                record['text'] = item['title']
                c.append(record)
        except Exception as e:
            warnings.warn(f'An unexpected exception occured when reading choice data: {e}')

        return c


def _add_dynamics_to_metadata(md, dynamics_counter):
    # get all dynamic fields in the metadata
    ix = (md['elementType'].str.startswith('matrixdynamic')) | (md['elementType'].str.startswith('paneldynamic'))
    dynamic_fields = md.loc[ix].to_dict(orient='records')

    # for each record in dynamic fields add them to the nested metadata
    for fld in dynamic_fields:
        fc = dynamics_counter.get(fld['frmCode'])

        try:
            k = list(filter(lambda x: fld['fldCode'].startswith(f'{x}_r'), fc))
        except:
            continue

        try:
            n = fc[k[0]]
            for i in range(2, n + 1):
                this_fld = fld.copy()
                this_fld['fldCode'] = re.sub(f'^{k[0]}_r\d+_', f'{k[0]}_r{i}_', fld['fldCode'])
                this_fld['fldParentCode'] = re.sub(f'^{k[0]}_r\d+_', f'{k[0]}_r{i}_', fld['fldParentCode'])
                md = pd.concat([md, pd.Series(this_fld).to_frame().T])
        except IndexError:
            pass
        except ValueError:
            pass

    return md


def _set_order(md, fields):
    # fields: a dictionary of the form {old_column: new_column}
    # this function sets numeric order for categories in old_column and saves it in new_column based on order in md

    md[list(fields.values())] = (md[list(fields.keys())].shift(1) != md[list(fields.keys())]).cumsum() + 1

    return md


def _rename_dict(d, rndct):
    for k, v in rndct.items():
        try:
            d[v] = d.pop(k)
        except KeyError:
            pass
    return d


def _replace_set(s, rndct):
    if rndct:
        return s.difference(set(rndct.keys())).union(set(rndct.values()))
    else:
        return s


def _sync_data_metadata(obvs, remap_dict=None, md=None):
    if isinstance(md, list):
        # get fields in forms in the shape of {frmCode1: [fldCode1, fldCode2, ...]}
        mdf = pd.DataFrame().from_records(md)
    elif isinstance(md, pd.DataFrame):
        mdf = md
    else:
        raise TypeError(f'Metadata should either be in Pandas DataFrame or List form, got {type(md)}')

    # obvs is DataFrame with index_fields + json
    # obvsgbo = obvs.groupby(by=['frmCode', 'phaseId'])
    obvsgbo = obvs.groupby(by=['frmCode'])
    obvslst = {}

    # Process responses for each form in each phase separately
    for name, obvg in obvsgbo:
        # extract field codes from metadata
        # this_form_fields = mdf.loc[(mdf['frmCode'] == name[0]) & (mdf['phaseId'] == name[1])] \
        #     .sort_values('fldOrder')['fldCode'].unique()

        this_form_fields = mdf.loc[(mdf['frmCode'] == name)] \
            .sort_values('fldOrder')['fldCode'].unique()

        # Define an empty dataframe with all necessary fields
        this_df = pd.DataFrame(columns=this_form_fields)

        # Create a dataframe from current records and apply remapping dictionary for this form
        tmp = this_df.append(obvg['json'].apply(pd.Series).rename(columns=remap_dict.get(name, {})))

        # Update observations list
        obvslst.update({name: pd.concat([obvg.drop(columns=['json']), tmp], axis=1)})

    return obvslst


def _translation_handler(s, target, alt):
    if target in s:
        if isinstance(s[target], dict):
            return s[target].get('fa', s[target].get('default'))
        else:
            return s[target]
    else:
        return alt


def _sync_data_phase(o, ph):
    p = pd.DataFrame().from_records(ph)
    p['phaseAlias'] = 'p' + p['phaseOrder'].astype(str)
    # p = p.drop('surveyIds').merge(p['surveyIds'].explode(), left_index=True, right_index=True)

    o = o.merge(p[['id', 'phaseAlias']], left_on='phaseId', right_on='id')
    o['json'] = o.apply(lambda x: {k + '_' + x['phaseAlias']: v for k, v in x['json'].items()}, axis=1)
    o.drop(columns=['phaseId', 'phaseAlias', 'id'], inplace=True)

    return o


@timing
def _df_to_dict(df):
    return df.apply(lambda x: {**x[['pid', 'frmCode', 'fillDate']].to_dict(), **x['json']}, axis=1).to_list()
