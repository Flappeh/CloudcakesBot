import pandas as pd
import os
import sys
from pandas.errors import EmptyDataError

root_path = os.getcwd()


def import_data():
    try:
        input_name = 'input.xlsx'
        file_path = root_path + f"\\data\\{input_name}"
        df = pd.read_excel(file_path, header=0)
    except EmptyDataError:
        raise Exception("Data dari file input kosong, mohon cek kembali\n")
    except FileNotFoundError as e:
        raise Exception("Tidak ada file input.xlsx dalam folder data. Mohon cek kembali\n")
    
    df['phone'] = df['phone'].astype('str').str.replace(' ','')
    data = df.values.tolist()
    return data

def import_items(parallel):
    try:
        items = import_data()
        data = list(split(items,parallel))
        return data
    except Exception as e:
        raise
        

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def save_data():
    data = pd.read_csv('data/temp_result.txt',header=None)
    df = pd.DataFrame(data)
    df.columns = ['Card Number', 'Code', 'Result', 'Proxy']
    
    result = df[df['Result'].isin(["NOT", "VALID"])]
    err_list = df[~df['Result'].isin(["NOT", "VALID"])]
    
    result_path = root_path + f"\\data\\results.xlsx"
    err_path = root_path + f"\\data\\errors.xlsx"
    result.to_excel(result_path, index=False)
    err_list.to_excel(err_path, index=False)