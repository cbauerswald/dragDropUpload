from google_utils import pickle_save, pickle_load
import dominate
from dominate.tags import *
from dominate.util import raw
import pandas as pd
import re

AVAILABLE_CONVERSIONS = ['SHSAT 00 Diagnostic', 'SAT - 04 - CB']

def convert(context):
    '''
    Should ALWAYS return a list of tuples, e.g.:
    [(section, converted_score)...]
    '''
    test_name = context['test_name']
    print(f'Test Name is : {test_name}')

    #In the event that a valid scaler has not been provided:
    if context.get('test_name') not in AVAILABLE_CONVERSIONS \
    or type(context.get('scaler')) != pd.DataFrame:
        return [('', 'UNAVAILABLE')]

    else:
        if test_name == 'SHSAT 00 Diagnostic':
            print('Using SHSAT converter')
            return shsat_converter(context)
        elif test_name == 'SAT - 04 - CB':
            print('Using SAT Diagnostic Converter')
            return sat_diag_converter(context)

def shsat_converter(context):
    converted_scores = []
    scale = context['scaler']
    for section in context['sections']:
        converted_scores.append((section, scale.T[context[section]['n_correct']]['New']))

    total = str(int(sum([float(j) for i,j in converted_scores])))
    converted_scores.append(('Total', total))

    return converted_scores

def handle_sat_extraction(context, key):
    section = context.get(key)
    n_correct = 0
    if section:
        n_correct = section['n_correct']
    return n_correct


def sat_diag_converter(context):
    scaler = context['scaler']
    scaler.columns = [re.sub(r'[^A-z]+', ' ', c).strip().replace(' ', '_').lower() for c in scaler.columns]

    math_raw = handle_sat_extraction(context, 'NO CALCULATOR') + \
               handle_sat_extraction(context, 'CALCULATOR')

    math_score = int(scaler.math_section_score.get(math_raw,0))

    wl_raw = handle_sat_extraction(context, 'WRITING & LANGUAGE')
    wl_score = int(scaler.writing_and_language_test_score.get(wl_raw,0))

    reading_raw = handle_sat_extraction(context, 'READING COMP')
    reading_score = int(scaler.reading_test_score.get(reading_raw, 0))

    total_score = math_score + wl_score + reading_score

    return [('Math', math_score), ('Writing', wl_score), ('Reading', reading_score), ('TOTAL', total_score)]





