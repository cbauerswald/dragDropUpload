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

    base = './uploads'
    for file in os.listdir(base):
        path = Path(os.path.join(base, file))
        if '.csv' in path:
            name = path.name.split('_')[2].split('.')[0].replace(' ','_').lower()
            now = str(datetime.now().date()).replace('-','_')
            name += f'_DATE_{now}'

            df = pd.read_csv(path)
            df.columns = [column.replace(' ', '_').lower() for column in df.columns]
            df.to_sql(name, con, if_exists='replace')
        os.remove(path)
