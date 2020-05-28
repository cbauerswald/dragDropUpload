import json
import numpy as np
import os
import pandas as pd

import google.auth
from google.cloud import firestore
from google.oauth2 import service_account

from .data_utils import *
from .google_utils import *
from .report_utils import *

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def df_to_json(df):
    df.to_json('tmp/tmp.json')
    jdata = load_json('tmp/tmp.json')
    os.remove('tmp/tmp.json')
    return jdata


def coerce_to_json(d):
    iterables = [list, np.ndarray]
    if type(d) in iterables:
        return [coerce_to_json(item) for item in d]
    elif type(d) == dict:
        for k, v in d.items():
            v_type = type(v)
            is_list_type = v_type in iterables

            if v_type == pd.DataFrame:
                d[k] = df_to_json(v)

            elif is_list_type:
                d[k] = [coerce_to_json(item) for item in v]
            else:
                d[k] = coerce_to_json(v)
        return d
    else:
        return d


import json


def load_firestore(doc):
    return json.loads(doc.to_dict()['data'])


def upload(report_paths, test_name=None):
    if not test_name:
        test_name = input('Test Name: ')

    bkdn_dfs = pickle_load(mem['db_info']['bkdn']['path'])
    scaler = bkdn_dfs[f'_SCALE - {test_name}']
    bkdn = bkdn_dfs[test_name]
    data = gen_report_data(test_name, report_paths, bkdn, scaler)
    jdata = NpEncoder().encode(coerce_to_json(data))

    doc_ref = db.collection(u'db_test').document(f'{test_name}')

    doc_ref.set({
        'data': jdata
    })