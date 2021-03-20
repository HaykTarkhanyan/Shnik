from datetime import date, datetime
from time import time
from helpers import *

def get_dates(df):
    """
    Function extracts birth date from columns tari or and amis_num
    Takes as input dataframe
    Returns list of dates
    """
    dates = []
    for i in range(len(df)):

        try:
            _date = str(df.iloc[i].tari) + '-' + str(int(df.iloc[i].amis_num)) + '-' + df.iloc[i]['or']
        except:
            _date = '1509-10-10'
        dates.append(_date)
    return dates


def calculate_age(born):
    born = datetime.strptime(born, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def until_birthday(born):
    if born.endswith('2-29'):
        born = born[:5] + '2-28'
    born = datetime.strptime(born, "%Y-%m-%d").date()
    born_new = datetime.strptime(f'{date.today().year}-{born.month}-{born.day}', "%Y-%m-%d").date()
    if born_new < date.today():
        born_new = datetime.strptime(f'{date.today().year+1}-{born.month}-{born.day}', "%Y-%m-%d").date()
    
    return born_new - date.today()