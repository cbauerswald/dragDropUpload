import sys, json
from pathlib import Path
import pandas as pd
import sqlite3
from datetime import datetime
import os

#NOTE! This runs on the system's base environment - can't use conda here.
# Will need a requirements.txt file eventually (deployment)

if __name__ == "__main__":

    con = sqlite3.connect('tests.db')
    files = json.loads(sys.argv[1])['files[]']

    with open('jinput.json', 'w+') as f:
        f.write(json.dumps(files))

    for file in files:
        path = file['path']
        name = file['name']
        name_clean = name.split('.')[0].replace(' ', '_').lower()
        now = str(datetime.now().date()).replace('-', '_')
        name_parsed = name_clean + f'_DATE_{now}'

        '''with open(f'{name_parsed}.txt', 'w+') as f:
            f.write(path)
            f.write('\n')
            f.write(name_parsed)
        '''

        df = pd.read_csv(path)
        df.columns = [column.replace(' ', '_').lower() for column in df.columns]
        df.to_sql(name_parsed, con, if_exists='replace')

        os.remove(path)
