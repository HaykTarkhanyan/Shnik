import pandas as pd
import re
from datetime import date, datetime
from time import time
from helpers import *

def get_info(name=None, surname=None, haeranun=None, marz=None, taracashrjan=None, min_age=None, max_age=None):
    print ('statring to read df')
    st = time()
    # df = pd.read_csv('elections_updated.csv')
    df = pd.read_parquet('electors_2019.parquet')
    df_copy = df
    print (f'loaded data in {time() - st}')

    print (f'extracting info for {name} {surname}')
    if name:
        df = df[df.anun == name]
        print (f'found {len(df)} with {name}')
    if surname:
        df = df[df.azganun == surname]
        print (f'found {len(df)} with {surname}')
    if haeranun:
        df = df[df.haeranun == haeranun]
        print (f'found {len(df)} with {haeranun}')
    if marz and marz != 'Ընտրել մարզը':
        df = df[df.marz == marz]
        print (f'found {len(df)} from {marz}')
    if taracashrjan:
        df = df[df.taracashrjan == taracashrjan]
        print (f'found {len(df)} from {taracashrjan}')
    

    print ('calculting date columns')
    # calculate date related columns
    
    st = time()
    dates = get_dates(df)
    try:
        df['date_new'] = dates
        df['age'] = df['date_new'].apply(calculate_age)
        df['until_birthday'] = df['date_new'].apply(until_birthday)
    except:
        print ('failed on time')
    print (f'took {time() - st}seconds')
    
    print ('filtering by age')
    st = time()
    
    if min_age:
        df = df[df.age >= int(min_age)]
        print (f'found {len(df)} older than {min_age}')
    
    if max_age:
        df = df[df.age <= int(max_age)]
        print (f'found {len(df)} younger than {max_age}')
    
    print (f'took {time() - st}seconds')
    
    print ('converting to html')
    try:
        output = df[['anun', 'azganun', 'haeranun', 'or', 'amis', 'tari', 'marz', \
                     'taracashrjan','hasce', 'age', 'until_birthday']].to_html()
        print ('done')

        print (f'found {len(df)}')     
    except:
        print ('fail') 
        output = df[['anun', 'azganun', 'haeranun', 'or', 'amis', 'tari', 'marz', \
                     'taracashrjan','hasce']].to_html()
        print ('done')

        print (f'found {len(df)}')  
   

    if len(df) == 0:
        message =  "Ոչմեկ չկար, հնարավորա չի քվյարկել, ամեն դեպքում տառասխալ ստուգեք ունեք թե չէ  ավելի քիչ տվյալ ներմուծեք նոր գտնելու դեպքում ավելացրեք լրացուցիչ ֆիլտռեր"
        return ['no results', message]
    if len(df) == 1:
        miasin_grancvac = df_copy[df_copy.hasce == df.hasce.values[0]]
        
        same_surname = df_copy[df_copy.azganun == df.azganun.values[0]]
        qur_axper = same_surname[same_surname.haeranun == df.haeranun.values[0]]

        return ['one person', output, miasin_grancvac.to_html(), qur_axper.to_html()]
    if len(df) > 1:
        return ['multiple results', f'{output} <br> Եթե այնպես անեք որ մենակ մեկ մարդ լինի վերևի աղյուսակում կկարողանամ լրացուցիչ տվյալներեկ արտածել']
