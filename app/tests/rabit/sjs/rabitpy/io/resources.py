import json
import warnings
import re

from collections import defaultdict

import pandas as pd

from rabitpy.utils import timing, find
from .adapters import RabitReaderBaseAdapter, RabitReaderAPIAdapter, RabitReaderJSONFileAdapter, RabitDatabaseAdapter, \
    RabitReaderJSONObjAdapter
from .parser_utils import _get_idx, _flatten_json
from .parsers import _rename_dict, _replace_set, _check_coding_validity, _set_properties, _set_order, _extract_choices


def json_handler(content):
    if isinstance(content, str):
        try:
            return json.loads(content)
        except:
            return None
    elif isinstance(content, dict) or isinstance(content, list):
        return content


@timing
def _rename_duplicates(md):
    # propagate renamed codes in metadata
    # get all list elements marked as duplicates

    dupcols = ['frmCode', 'fldCode']

    # Drop duplicates of [frmCode, fldCode] first and the see which field codes have duplicates
    dup = md.drop_duplicates(subset=dupcols)
    dup = dup.loc[dup.duplicated(subset='fldCode'), 'fldCode']

    # get boolean array for duplicated values
    ix = md['fldCode'].isin(dup)

    # Assign new names for duplicated values
    md.loc[ix, 'fldCodeR'] = 'frm' + \
                             md.loc[ix, 'frmCode'].astype(str) \
                             + '_' + \
                             md.loc[ix, 'fldCode'].astype(str)

    # Create renaming dictionary in {frmCode: {field1: field1_new_name}} format
    rd = dict.fromkeys(md.loc[ix, 'frmCode'].unique())

    for frm in rd.keys():
        ixx = md['frmCode'] == frm
        rd[frm] = dict(zip(md.loc[ix & ixx, 'fldCode'], md.loc[ix & ixx, 'fldCodeR']))
        rdvc = dict(
            zip(md.loc[ix & ixx, 'fldCode'].apply(lambda x: f"{ {x} }".replace("'", "").replace(' ', '')),
                md.loc[ix & ixx, 'fldCodeR'].apply(lambda x: f"{ {x} }".replace("'", "").replace(' ', ''))
                ))
        md.loc[ix & ixx, 'fldCode'] = md.loc[ix & ixx, 'fldCodeR']

        for k, v in rdvc.items():
            if 'visibleCondition' in list(md.columns):
                md.loc[ixx, 'visibleCondition'] = md.loc[ixx, 'visibleCondition'] \
                    .fillna('').str.replace(k, v, regex=True)
            if 'expression' in list(md.columns):
                md.loc[ixx, 'expression'] = md.loc[ixx, 'expression'].fillna('').str.replace(k, v, regex=True)

    md = md.drop(columns='fldCodeR')

    return md, rd


class RabitBaseResource:

    def __init__(self, source, reader=None, content_path=None, json_path=None, **kwargs):

        """

        Base class for all RABIT resources
        source: Source type corresponding to one of the resource readers in rabit.io.adapters
        **kwargs: Arguments to be passed to RabitReader adapter as specified by 'source'

        """

        self.source = source

        if reader and isinstance(reader.__class__.__bases__[0], RabitReaderBaseAdapter.__class__):
            self.reader = reader
        else:
            self.reader = self.__get_resource_reader(**kwargs)

        self.content_path = content_path

        # TODO: change intermediary json column name in data and metadata to '_json'

        if json_path == '_json':
            ValueError("'json_path' can not be '_json'")

        self.json_path = json_path
        self.raw = None

    @property
    def filters(self):
        return self.reader.filters

    def add_filters(self, filters=None, field=None, condition=None, value=None):

        if isinstance(filters, list) or isinstance(filters, tuple):
            for f in filters:
                if isinstance(f, tuple) or isinstance(f, list):
                    self.__update_filters(*f)
                if isinstance(f, dict):
                    self.__update_filters(**f)
            return None
        elif field and condition and value:
            self.__update_filters(field=field, condition=condition, value=value)
        else:
            warnings.warn('Could not update filter. Check inputs...')

    def reset_filters(self):
        self.reader.reset_filters()

    def __update_filters(self, field, condition, value):
        self.reader.add_filter(field, condition, value)

    def __get_resource_reader(self, **kwargs):

        if self.source == 'api':
            baseurl = kwargs.get('baseurl')
            uri = kwargs.get('uri')
            route = kwargs.get('route')
            verify = kwargs.get('verify', False)
            parameters = kwargs.get('parameters', dict())
            return RabitReaderAPIAdapter(baseurl=baseurl, uri=uri, route=route, verify=verify, parameters=parameters)
        elif self.source == 'json-file':
            fp = kwargs.get('fp')
            encoding = kwargs.get('encoding', 'utf-8')
            return RabitReaderJSONFileAdapter(fp=fp, encoding=encoding)
        elif self.source == 'db':
            url = kwargs.get('url')
            query = kwargs.get('query')
            return RabitDatabaseAdapter(url=url, query=query)
        elif self.source == 'json':
            obj = kwargs.get('obj')
            return RabitReaderJSONObjAdapter(obj=obj)
        else:
            raise ValueError(f'Unrecognized source type: {self.source}...')

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, value):
        self._raw = value

    def fetch(self, cache=False):

        # Fetch data from target resource
        try:
            fetched = self.reader.fetch()
        except ValueError as e:
            warnings.warn(f'Reader fetch method returned malformed or empty response with error:\n{e.__str__()}')
            return None

        # We need to extract the path where targeted resource content is
        if isinstance(fetched, dict):
            content = find(self.content_path, fetched)
        elif isinstance(fetched, list):
            content = []
            for item in fetched:
                content.append(find(self.content_path, item))

        if not content:
            raise ValueError('No content was fetched from source {}.')

        del fetched

        if self.json_path:
            if isinstance(content, dict):
                content[self.json_path] = json_handler(content.get(self.json_path))
            elif isinstance(content, list):
                for item in content:
                    item[self.json_path] = json_handler(item.get(self.json_path))

        if cache:
            self.raw = content
            return self.raw
        else:
            return content

    def dump(self, fp, indent=4):
        with open(fp, 'w') as f:
            json.dump(self.fetch() if not self.raw else self.raw, f, indent=indent)


class RabitData(RabitBaseResource):

    def __init__(self, source, index_fields, use_fields=None, content_path='content', json_path=None, **kwargs):

        """

        RABIT Data Resource Class
        source: Source type corresponding to one of the resource readers in rabit.io.adapters
        index_fields: A list of dictionary specifying the index fields to be used in data
        use_fields: A list of fields other than parsed json to be included in the parsed output
        json_path: A string specifying the path that contains the response json object
        **kwargs: Arguments to be passed to RabitReader adapter as specified by 'source'

        """

        super().__init__(source=source, json_path=json_path, **kwargs)

        # set all necessary data for this parser
        self.index_fields = index_fields
        self.use_fields = use_fields
        self.content_path = content_path

        self.parser_args = ['index_fields', 'json_path', 'use_fields']
        self.idx = None
        self.raw = None
        self.df = None
        self.dff = None

    @timing
    def parse(self, cache=False):

        d = self.fetch(cache) if not self.raw else self.raw

        # This function returns a dataframe with index columns, user selected fields, and dynamic data counts
        if isinstance(d, dict):
            # find and retrieve the data contained in content_path
            d = find(self.content_path, d)
        elif not isinstance(d, dict) and not isinstance(d, list):
            # TODO: Check if this should throw a ValueError exception
            warnings.warn('Specified data path not found or is empty, check path and try again...')
            return None

        # create list of fields to be extracted and indicate index tags
        self.idx = _get_idx(index_fields=self.index_fields,
                            use_fields=self.use_fields,
                            available_fields=list(d[0].keys()))

        # set all fields to extract form observations
        cols = (list(self.idx.keys()) + [self.json_path]) if self.json_path else list(self.idx.keys())
        dtypes = {item['name']: item.get('dtype', 'str') for item in self.index_fields}

        # construct raw response pandas dataframe
        df = pd.DataFrame().from_records(d, columns=cols, coerce_float=False)

        # construct default value dictionary for indices
        fndct = {k: v.get('default') for k, v in self.idx.items() if v.get('index') and v.get('default') is not None}

        df = df.fillna(fndct)

        # User can set data type for index and use_fields fields
        df = df.astype(dtypes)

        # rename fields according to aliases given in idx
        df = df.rename(columns={k: v['alias'] for k, v in self.idx.items() if v.get('alias')})

        ufs = list(filter(lambda x: not self.idx[x].get('index'), self.idx))
        if ufs:
            df['_json'] = df[ufs].to_dict(orient='records')
            df.drop(columns=ufs, inplace=True)
        else:
            df['_json'] = [{} for x in range(len(df))]

        # Flatten json column, otherwise create a json column with empty dictionaries
        if self.json_path:

            try:
                flattened = pd.DataFrame() \
                    .from_records(df[self.json_path]
                                  .apply(lambda x: _flatten_json('', json.loads(x, strict=False), counter={})),
                                  columns=['json_tmp', 'dc'])
            except TypeError:
                flattened = pd.DataFrame() \
                    .from_records(df[self.json_path]
                                  .apply(lambda x: _flatten_json('', x, counter={})),
                                  columns=['json_tmp', 'dc'])

            df.drop(columns=[self.json_path], inplace=True)
            df = pd.concat([df, flattened], axis=1)
            df.apply(lambda x: x['_json'].update(x['json_tmp']), axis=1)
            df.drop(columns='json_tmp', inplace=True)

        else:

            df['dc'] = [dict() for x in range(len(df))]

        # extract all available field codes from json column
        df['fldCode'] = df['_json'].apply(lambda x: list(x.keys()))

        dff = df.groupby(by=['frmCode']).agg({'fldCode': 'sum',
                                              'dc': lambda x: pd.DataFrame().from_records(list(x))
                                             .max().to_dict()})

        dff['fldCode'] = dff['fldCode'].apply(lambda x: set(x))
        dff.reset_index(inplace=True)

        df.drop(columns=['fldCode', 'dc'], inplace=True)
        df.rename(columns={'_json': 'json'}, inplace=True)

        self.df = df
        self.dff = dff

    def rename_duplicates(self):

        # get rename dictionary for responses regardless of metadata
        _, rndct = _rename_duplicates(self.dff.explode('fldCode'))

        dfgbo = self.df.groupby(by=['frmCode'])
        for name, group in dfgbo:
            group['json'].apply(lambda x: _rename_dict(x, rndct.get(name, {})))
            self.dff.loc[self.dff['frmCode'] == name, 'fldCode'] = self.dff.loc[self.dff['frmCode'] == name, 'fldCode'] \
                .apply(lambda x: _replace_set(x, rndct.get(name, {})))
            self.dff.loc[self.dff['frmCode'] == name, 'dc'] = self.dff.loc[self.dff['frmCode'] == name, 'dc'] \
                .apply(lambda x: _rename_dict(x, rndct.get(name, {})))

    @timing
    def reshape(self, shape, index, order=[], filter_array=None, reset_index=False):

        """
        :param order: set the order of forms in the resulting shape
        :param shape:
            - merged: drops duplicated forms and returns all data in a flat arrangement
            - duplicated merge:
        :return:
        """

        if self.df.empty:
            warnings.warn('No data passed. Is data parsed? Skipping...')
            pass

        if filter_array is None:
            filter_array = self.df.index.notna()

        if shape == 'merged':
            out = self.df.loc[filter_array].groupby(by=index) \
                .apply(lambda x: self.__concat_response_merged(x))
        elif shape == 'duplicate merged':
            out = self.df.loc[filter_array].groupby(by=index) \
                .apply(lambda x: self.__concat_response_duplicated_merge(x, order))
        else:
            raise ValueError(f'Shape option {shape} not recognized.')

        return out

    def __concat_response_merged(self, df):

        out = {}
        for item in df['json'].to_list():
            out.update(item)

        return out

    def __concat_response_duplicated_merge(self, order):

        # Maybe add 'frmCode' to sort values
        self.df.sort_values(order, inplace=True)
        self.df['order'] = 1
        self.df.groupby('frmCode')['order'].transform('cumsum')
        self.df['prefix'] = 'frm' + self.df['frmCode'].astype(str) + '_' + self.df['order'].astype(str) + '_'
        self.df['json'] = self.df.apply(lambda x: {x['prefix'] + k: v for k, v in x['json'].items()}, axis=1)

        return self.__concat_response_merged()


class RabitMetadata(RabitBaseResource):

    def __init__(self, source, reader=None, fid_path='id', json_path='json', include_html=False,
                 frm_name_path='surveyName', frm_desc_path='surveyDescription', baseurl=None, **kwargs):

        """

        RABIT Data Resource Class
        source: Source type corresponding to one of the resource readers in rabit.io.adapters
        fid_path: Path to form ID
        json_path: Path to json object containing form data
        include_html: Include html objects in metadata output
        rename_duplicates: Rename all non-unique fields
        frm_name_path: Path to form name
        frm_desc_path: Path to form description
        **kwargs: Arguments to be passed to RabitReader adapter as specified by 'source'

        """

        super().__init__(source=source, reader=reader, json_path=json_path, **kwargs)

        # set all necessary data for this parser
        self.parser_args = ['fid_path', 'json_path', 'include_html', 'rename_duplicates',
                            'frm_name_path', 'frm_desc_path']
        self._fid_path = fid_path
        self.include_html = include_html
        self._frm_name_path = frm_name_path
        self._frm_desc_path = frm_desc_path
        self.baseurl = baseurl
        self.phases = kwargs.get('phases', None)
        self.base_info_data = kwargs.get('base_info_data', None)
        self.md = None
        self.mdn = None
        self._forms = None

    @property
    def fid_path(self):
        return self.get_path_property('_fid_path')

    @property
    def frm_name_path(self):
        return self.get_path_property('_frm_name_path')

    @property
    def frm_desc_path(self):
        return self.get_path_property('_frm_desc_path')

    @property
    def forms(self):
        return self._forms

    def fields(self, fid=None, orient='title'):

        if fid is None:
            fid = list(self._forms.keys())

        if isinstance(fid, list):
            fid = list(map(lambda x: str(x), fid))
        else:
            fid = [str(fid)]

        if isinstance(self.mdn, pd.DataFrame):
            if orient == 'title':
                return self.mdn.loc[self.mdn['frmCode'].astype(str).isin(fid), 'fldName'].to_list()
            elif orient == 'code':
                return self.mdn.loc[self.mdn['frmCode'].astype(str).isin(fid), 'fldCode'].to_list()
            elif orient == 'grouped':
                return self.mdn.loc[self.mdn['frmCode'].astype(str).isin(fid), ['frmCode', 'fldCode', 'fldTitle']]\
                    .groupby(by='frmCode')\
                    .apply(lambda x: x.set_index('fldCode')['fldTitle'].to_dict()).to_dict()
            elif orient == 'dict':
                return self.mdn.loc[self.mdn['frmCode'].astype(str).isin(fid), ['frmCode', 'fldCode', 'fldTitle']] \
                    .set_index('fldCode')['fldTitle'].to_dict()
        else:
            return []

    def get_path_property(self, prop):
        x = getattr(self, prop)
        if isinstance(x, dict):
            x['default'] = x.get('default')
            return x
        elif isinstance(x, str):
            return {'name': x, 'default': None}

    def parse(self, cache=False, rename_duplicates=True):

        # This is the main function for parsing metadata
        if not self.json_path:
            return None

        # Fetch data from reader if not previously cached and parse
        # TODO: Should include some form of forced update where raw data is available but underlying data has changed
        d = self.fetch(cache) if not self.raw else self.raw

        metadata = self.__parse(d)

        if metadata is None:
            return None, None

        md = pd.DataFrame().from_records(metadata)
        md = md.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        md = _check_coding_validity(md=md, nested=False)
        md = _set_order(md, {'frmCode': 'frmOrder', 'fldCode': 'fldOrder', 'fldParentCode': 'fldParentOrder'})
        # md['fld_code_full'] = md.apply(lambda x: f'p{x["phase_id"]}_f{x["frmCode"]}_x["fldCode"]')

        self.md = md
        self.mdn = self.nest()
        self._forms = md.drop_duplicates('frmCode').set_index('frmCode')['frmName'].to_dict()

        if rename_duplicates:
            self.rename_duplicates()

    def __parse(self, d):

        metadata = []

        if not isinstance(d, list):
            d = [d]

        for qnr in d:

            fid = qnr.get(self.fid_path['name'], self.fid_path['default'])
            frm_name = qnr.get(self.frm_name_path['name'], self.frm_name_path['default']) if self.frm_name_path else ''
            frm_desc = qnr.get(self.frm_desc_path['name'], self.frm_desc_path['default']) if self.frm_desc_path else ''

            # check and return exception if metadata json does not contain 'json' key
            qnrjson = qnr.get(self.json_path)

            if not qnrjson:
                warnings.warn(f'Form ID: {fid}: NULL JSON detected. Skipping')
                continue

            try:
                if isinstance(qnrjson, str):
                    qnrjson = json.loads(qnrjson, strict=False)
            except KeyError as e:
                raise KeyError(f'Form ID: {fid}: Invalid JSON...')

            # check if there are 'pages' key, if not, raise error
            pages = qnrjson.get('pages', None)
            if not pages:
                raise KeyError(f'Form ID: {fid}: pages element missing from JSON.')

            # for each page in pages go through each element and parse metadata
            for page in pages:
                # If page does not contain elements key, create empty list which means we continue on this loop
                for element in page.get('elements', []):
                    try:
                        metadata += _set_properties(_qnr=qnr,
                                                    _element=element,
                                                    _choices=_extract_choices(_el=element,
                                                                              baseurl=self.baseurl),
                                                    _fid=fid,
                                                    _frm_name=frm_name,
                                                    _frm_desc=frm_desc,
                                                    baseurl=self.baseurl,
                                                    _include_html=self.include_html)

                    # Add errors to output dict where there are exceptions
                    except Exception as e:

                        print(f'error in processing {fid} {element.get("name")}')

                        metadata.append({'fldCode': element.get('name'),
                                         'fldTitle': element.get('title'),
                                         'frmCode': fid,
                                         'frmName': frm_name,
                                         'frmDesc': frm_desc,
                                         'frmOrder': qnr.get('sortOrder'),
                                         'error': e})
                        raise
        return metadata

    def nest(self):

        if self.md is None:
            warnings.warn('Metadata is empty. Has it been parsed?')
            return None

        cols = ['frmCode', 'fldCode']
        opts = self.md.loc[self.md['optVal'].notna(), cols + ['optVal', 'optText']].copy()
        opts['opt'] = pd.Series(self.md[['optVal', 'optText']]
                                .rename(columns={'optVal': 'value', 'optText': 'text'})
                                .to_dict(orient='records'))
        nested_opts = opts.groupby(cols)['opt'].apply(lambda x: x.to_list()).reset_index()
        mdn = self.md.drop_duplicates(cols).drop(columns=['opt']).merge(nested_opts, on=cols, how='left')
        mdn.loc[mdn['optVal'].isna(), 'opt'] = None
        mdn.drop(columns=['optVal', 'optText'], inplace=True)

        mdn = _check_coding_validity(md=mdn, nested=True)
        return _set_order(mdn, {'frmCode': 'frmOrder', 'fldCode': 'fldOrder', 'fldParentCode': 'fldParentOrder'})

    def rename_duplicates(self):
        self.md, _ = _rename_duplicates(self.md)
        self.nest()


class RabitProject(RabitBaseResource):

    def __init__(self, source, reader=None, project_id=None, content_path=None, json_path=None):
        super().__init__(source=source, reader=reader, content_path=content_path, json_path=json_path)
        print('initiated')

        self.project_id = project_id
        self.project_type = None
        self.project_name = None
        self.project_structure = None
        self.has_phases = None
        self.phases = None

    def parse(self, cache=False):

        d = self.fetch(cache) if not self.raw else self.raw

        if not d:
            return None

        self.project_name = d.get('projectName')

        cols = ['id', 'name', 'level', 'parentId', 'surveyIds']
        rndct = {'id': 'phaseId', 'name': 'phaseTitle', 'surveyIds': 'frmCode', 'level': 'phaseLevel'}
        phases = pd.DataFrame().from_records(d.get('phases'), columns=cols, coerce_float=False) \
            .explode('surveyIds')
        phases = phases.loc[phases['parentId'].isna()]
        phases = _set_order(phases, {'id': 'phaseOrder'}).reset_index(drop=True)
        phases.rename(columns=rndct, inplace=True)

        # TODO: Add subphases
        # set phase aliases
        # level_counts = phases['level'].max()
        # for level in range(level_counts):
        phases = list(filter(lambda x: not x.get('deleted', True), d.get('phases', [])))

        if phases:
            self.has_phases = True
            self.phases = phases

        self.project_structure = d.get('structureAlias')
        self.project_type = d.get('projectTypeAlias')


class RabitDataset:

    def __init__(self, data=None, metadata=None, project=None):

        self.data = data
        self.metadata = metadata
        self.project = project
        self._df = None
        self._idx = None
        self._md = None
        self._mdn = None
        self._dff = None

    def __add__(self):
        pass

    @property
    def df(self):
        return self.data.df

    @property
    def dff(self):

        if self.df is not None and self.mdn is not None:
            self._dff = self.mdn.groupby(by=['frmCode']) \
                .agg({'fldCode': lambda x: dict.fromkeys(list(x))}) \
                .reset_index().merge(self.data.dff[['frmCode', 'dc']], on='frmCode')
        elif self.df is not None:
            self._dff = self.data.dff
            self._dff['fldCode'] = self._dff['fldCode'].apply(lambda x: dict.fromkeys(list(x)))
        else:
            self._dff = None

        return self._dff

    @property
    def idx(self):
        return self.data.idx

    @property
    def md(self):
        return self.metadata.md

    @property
    def mdn(self):
        return self.metadata.mdn

    def load(self, cache=False):

        if self.project:
            self.project.parse(cache)

        if self.metadata:
            self.metadata.parse(cache, rename_duplicates=False)

        if self.data:
            self.data.parse(cache)

        # if ~self.md.empty:
        #     self.update_dynamic_fields_in_metadata()
        #
        # if self.df is not None:
        #     self.sync()

        return None

    def update_dynamic_fields_in_metadata(self):

        target_fields = self.dff.set_index('frmCode')['dc'].to_dict()

        # get all dynamic fields in the metadata
        ix = (self.md['elementType'].str.startswith('matrixdynamic')) | \
             (self.md['elementType'].str.startswith('paneldynamic'))
        dynamic_fields = self.md.loc[ix].to_dict(orient='records')

        # for each record in dynamic fields add them to the nested metadata
        for fld in dynamic_fields:
            fc = target_fields.get(fld['frmCode'])

            try:
                k = list(filter(lambda x: fld['fldCode'].startswith(f'{x}_r'), fc))
            except:
                continue

            try:
                n = int(fc[k[0]])
                new_metadata_rows = []
                for i in range(2, n + 1):
                    this_fld = fld.copy()
                    this_fld['fldCode'] = re.sub(f'^{k[0]}_r\d+_', f'{k[0]}_r{i}_', fld['fldCode'])
                    this_fld['fldParentCode'] = re.sub(f'^{k[0]}_r\d+_', f'{k[0]}_r{i}_', fld['fldParentCode'])

                    # TODO: Need to preserve field orders here
                    new_metadata_rows.append(this_fld)
                    # self.metadata.md = pd.concat([self.md, pd.Series(this_fld).to_frame().T])
                self.metadata.md = pd.concat([self.md, pd.DataFrame(new_metadata_rows)])
                self.metadata.nest()
            except IndexError:
                pass
            except ValueError:
                pass

        return None

    @timing
    def sync(self):
        d = self.df.merge(self.dff[['frmCode', 'fldCode']], on='frmCode', how='right')
        d['json'] = d.apply(lambda x: {k: x['json'].get(k, None) for k in x['fldCode'].keys()}, axis=1)
        self.data.df = d.drop(columns=['fldCode'])
        del d

    def to_pandas(self, reshape=False, **kwargs):

        if self.df is None:
            return
        elif reshape:
            d = self.reshape(**kwargs)
        else:
            d = self.df

        return pd.DataFrame(d.to_list(), index=d.index)

    def reshape(self, shape='merged', index='pid', order=[], filter_array=None):
        return self.data.reshape(shape, index, order, filter_array)

# changes to push.