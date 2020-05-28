from dateparser import parse
from difflib import SequenceMatcher
import json
import numpy as np
import os
import pandas as pd
import re
import requests
import shutil as sh
import shutil

def strp_nonanum(s):
    return re.sub(r'[^A-Za-z0-9]', '', s)

def write_json(dict_, outfile=None):
    out_data = json.dumps(dict_)
    if outfile:
        with open(outfile, 'w+') as f:
            f.write(out_data)
    return out_data

def load_json(path):
    with open(path) as json_file:
        jdata = json.load(json_file)
    return jdata

def rm_hidden(root_path):
    # Grab hidden files:
    hidden_files = [os.path.join(root_path, f) for f in os.listdir(root_path) if f.startswith('.')]

    # Remove them:
    for f in hidden_files:
        try:
            sh.rmtree(f)
        except:
            try:
                os.remove(f)
            except:
                print('error removing {}'.format(f))

    # Grab again:
    hidden_files = [os.path.join(root_path, f) for f in os.listdir(root_path) if f.startswith('.')]

    if len(hidden_files) > 0:
        error_string = '''
        Operation did not remove all hidden files as expected.
        Remaining files (you may need to remove manually):
        {}
        '''.format(hidden_files)
        raise AssertionError(error_string)

def longestSubstring(str1, str2):
    # initialize SequenceMatcher object with
    # input string
    seqMatch = SequenceMatcher(None, str1, str2)

    # find match of longest sub-string
    # output will be like Match(a=0, b=0, size=5)
    match = seqMatch.find_longest_match(0, len(str1), 0, len(str2))

    # return longest substring
    return str1[match.a: match.a + match.size]

def get_shared_string(a, b):
    '''
    Returns the bkdn sheet title that most closely matches the input filenames.
    '''
    matches = []
    for i in a:
        for j in b:
            match = longestSubstring(i.lower(), j.lower())
            if match:
                matches.append((len(match), match, i))
    return sorted(matches)[-1][-1].strip()

def concat_w_str(x, s):

    null_values = [str(s).lower() for s in ['N/A', np.nan, 'None', 'NaT', 'NAN']]

    to_concat = [str(v) for v in x if str(v).lower() not in null_values]

    res = f'{s}'.join(to_concat)

    return res

def mkdir_force(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def parse_datetime(s):
    if s:
        return parse(s)
    else:
        return False

def df_styler(val):
    """
    applies css styles to each val in a df.
    """
    text_dec = ''
    font_weight = ''
    if '*' in val:
        color = 'red'
        text_dec = 'underline overline'
        font_weight = 'bold'
    else:
        color = 'black'

    return f'color: {color}; text-decoration: {text_dec}; font-weight: {font_weight}'

def markup_answers(r):
    r.A = str(r.A)
    if not r.correct:
        r.A = str(r.A) + '*'
    return r[['Q', 'A']]

def make_report_table(df, n_cols=3, fillna=True, fillval=''):
    '''
    Styles an input df, and returns the style tag and raw html
    :param df: student section_df
    :param n_cols: number of cols for a table - default three
    :param fillna: whether to fill NANs or not
    :param fillval: if fillna, what to fill with.
    :return: raw html style tag and table tag
    '''

    v = df.iloc[:, 1:4]
    v.columns = ['A', 'correct', 'Q']

    v = v.apply(markup_answers, axis=1)

    n_vals = len(v)
    n_cols = 3
    col_height = n_vals // n_cols
    if n_vals % n_cols != 0:
        col_height += 1
    subcols = []
    for i in range(n_cols):
        subcol = v.iloc[(i * col_height):(i * col_height) + col_height].reset_index(drop=True)
        subcols.append(subcol)
    reshaped = pd.concat(subcols, axis=1)
    reshaped.columns = np.array([[f'Q_{i}', f'A_{i}'] for i in range(int(reshaped.shape[1] / 2))]).ravel()

    if fillna:
        reshaped = reshaped.fillna(fillval)

    styled = reshaped.style.applymap(df_styler).hide_index()

    html_unique_cols = styled.render()

    soup = BeautifulSoup(html_unique_cols, features='lxml')

    for th in soup.find_all('th'):
        if '_' in th.text:
            th.string = th.text[0]
        else:
            th.string = ''

    table_styles = soup.find('style')
    table_html = list(soup.find('body').children)[0]
    table_classes = ["table-bordered", "table-striped", "table-hover"]
    table_html['class'] = table_html.get('class', '') + ' '.join(table_classes)

    return str(table_styles), str(table_html)

def write_html(html, fname='out.html'):
    with open(fname, 'w+') as f:
        f.write(str(html))


'''
Free conversion using WKTOHTML
'''
import subprocess
def html_to_pdf(path, watermark_path, out_fname=None, convert_fname=False):
    out_dir = '/'.join(path.split('/')[:-1])
    in_fname = path.split('/')[-1]
    if (not out_fname) or (convert_fname):
        split = path.split('.')
        pdf_outpath = '.'.join(split[:-1]) + '.pdf'
        out_fname = pdf_outpath

    subprocess.run(["cd", out_dir])
    subprocess.run(["wkhtmltopdf", '-B', '10mm', path, pdf_outpath])

    print('Watermarking PDF!')
    watermark_fname = ('WM_'+in_fname).replace('.html', '.pdf')
    watermarked_outpath = os.path.join(out_dir,watermark_fname)
    watermark(pdf_outpath, watermark_path, watermarked_outpath)

    return watermarked_outpath


def watermark(input_file, watermark_file, output_file):
    # create a pdf writer object for the output file
    pdf_writer = PyPDF2.PdfFileWriter()

    with open(input_file, "rb") as filehandle_input:
        # read content of the original file
        pdf = PyPDF2.PdfFileReader(filehandle_input)

        with open(watermark_file, "rb") as filehandle_watermark:
            # read content of the watermark
            watermark = PyPDF2.PdfFileReader(filehandle_watermark)

            for page in pdf.pages:
                # merge the two pages
                page.mergePage(watermark.getPage(0))

                # add page
                pdf_writer.addPage(page)

            with open(output_file, "wb") as filehandle_output:
                # write the watermarked file to the new file
                pdf_writer.write(filehandle_output)

def merge_pdfs(pdfs, out_fname):
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf, import_bookmarks=False)

    merger.write(out_fname)
    merger.close()

def ensure_path(path):
    filtered_path = path
    final = path.split('/')[-1]
    file_in_path = ('.' in final)
    if file_in_path:
        filtered_path = '/'.join(path.split('/')[:-1])
    if not os.path.exists(filtered_path):
        os.makedirs(filtered_path)
    return path

def chunk_list(l,n):
    return [l[i:i+n] for i in range(0,len(l),n)]