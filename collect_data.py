from time import sleep
import os
import pandas as pd
from conf import *
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine('mysql+mysqldb://' + user_mysql + ':' + pass_mysql + '@' + host_mysql + '/' + db_name)

def load_csv(path):
    file_df = pd.read_csv(path)
    file_df['timestamp'] = file_df['acq_date'] + ' ' + file_df['acq_time']
    return file_df


def insert_into_mysql(df, table):
    df.to_sql(name=table, con=engine, if_exists='append', index=False)


def monitor(ftp, dir, interval=50):
    old_files = os.listdir(dir)
    now = datetime.now()
    year = now.year
    try:
        while True:
            print 'looping'
            new_files = ftp.nlst()
            if new_files != old_files:
                files = [i for i in new_files if i not in old_files]
                old_files = old_files + files
                for file in files:
                    file_list = file.split('_')[-1]
                    file_date = file_list.split('.')[0]
                    file_year = datetime.strptime(file_date[0:4], '%Y')
                    if file_year.year >= year and int(file_date[4::]) > 200:
                        path = dir + '/' + file
                        command = 'RETR ' + file
                        print command
                        ftp.retrbinary(command, open(path, 'wb').write)
                        result = load_csv(path)
                        insert_into_mysql(result, table='fire')

            sleep(interval)
    except KeyboardInterrupt:
        ftp.quit()

