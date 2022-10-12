import datetime
import re
import pandas as pd

def is_work(letter:str):
    return True if re.match(r'(W)([\d])',letter) else False

def is_hang_muc(letter:str):
    return True if re.match(r'(HM)([\d])',letter) else False

def is_norm(letter:str):
    return True if re.match(r'([A-Za-z]{2})(.)([\d]{5})',letter) else False

def is_machine(letter:str):
    return True if re.match(r'(^[Mm])([\d]+)',letter) else False

def is_worker(letter:str):
    return True if re.match(r'(^[Nn])([\d]+)',letter) else False

def is_material(letter):
    return True if re.match(r'([\d]+)',letter) else False

def is_dif_machine(letter):
    return True if letter in ['ZM999','zm999'] else False

def is_dif_material(letter):   
    return True if letter in ['ZV999','zv999'] else False

def read_excel(path) -> list:
    dutoanDF = pd.read_excel(path,sheet_name='Chiết tính',header=4,usecols='c:g')

    # Fill cho hàng Mã CV
    dutoanDF[dutoanDF.columns[0]].fillna(inplace=True,method='ffill')
    #Xóa duplucate
    dutoanDF.drop_duplicates(subset=[dutoanDF.columns[0],dutoanDF.columns[1]],inplace=True)
    # Xóa dòng trống
    dutoanDF.dropna(subset=[dutoanDF.columns[1]],inplace=True)
    # Xóa TT và TĐG
    dutoanDF = dutoanDF[dutoanDF[dutoanDF.columns[0]].apply(len)==8]
    # Fill NA cho cột định mức 
    dutoanDF[dutoanDF.columns[4]].fillna(inplace=True,value=0)
    
    return dutoanDF.values

def display_date_time(date_time:datetime.datetime):
    format = '%d/%m/%y'
    return date_time.strftime(format)