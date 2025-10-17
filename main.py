from modules.data import import_items, save_data, import_data, import_agents
from modules.worker import ValWorker
from modules.config import remove_temp, ENABLE_PROXY
from DrissionPage.common import Settings
import multiprocessing as mp
from modules import proxy
import time
import os
import sys
import random

Settings.set_language('en')

intro = """
===============================================================
__     __    _ _     _       _               ____        _   
\\ \\   / /_ _| (_) __| | __ _| |_ ___  _ __  | __ )  ___ | |_
 \\ \\ / / _` | | |/ _` |/ _` | __/ _ \\| '__| |  _ \\ / _ \\| __|
  \\ V / (_| | | | (_| | (_| | || (_) | |    | |_) | (_) | |_
   \\_/ \\__,_|_|_|\\__,_|\\__,_|\\__\\___/|_|    |____/ \\___/ \\__|
   
===============================================================
"""



    
    
def init_worker(input, return_dict):
    current_worker = 0
    idx, data, agent= input
    if len(data) < 1:
        return
    worker = ValWorker(data[0], data[1], data[2], agent)
    worker.start()
    return_dict[f"{current_worker}-{idx}"] = data
    del worker
    current_worker += 1

def get_parallel_count():
    count = input("Please insert how many parallel process you want to run (Maximum 100) : ")
    try:
        data = int(count)
        
        if data > 100:
            print("Please refrain from having more than 100 parallel process for safety reasons!")
            return get_parallel_count()
        return data
    
    except Exception as e:
        print("Please only insert number", e)
        return get_parallel_count()

def show_exception_and_exit(exc_type, exc_value, tb):
    allowed_messages = {
        "Tidak ada file input.xlsx dalam folder data. Mohon cek kembali",
        "Data dari file input kosong, mohon cek kembali",
        "Terjadi error saat import data"
    }

    # Check if the exception message is in the allowed list
    if str(exc_value) in allowed_messages:
        print(exc_value)
    else:
        print("Terjadi error yang tidak diketahui:", exc_value)

    input("Press any key to exit.")
    sys.exit(-1)

if __name__ == "__main__":
    sys.excepthook = show_exception_and_exit
    mp.freeze_support()
    remove_temp()
    
    print(intro)
    
    print("Welcome to validator bot!\n\n")
    
    manager = mp.Manager()
    return_dict = manager.dict()
    
    procs = []
    
    # count = get_parallel_count()
    
    # global_data = import_items(count)
    global_data = import_data()
    user_agents = import_agents()
    print(global_data)
    
    if ENABLE_PROXY:
        print("Retrieving proxy data")
        proxy_data = proxy.get_list()    
        if not proxy_data or len(proxy_data) < 1:
            proxy_data = proxy.new_list(5)
        
    
    for i in range(len(global_data)):
        process = mp.Process(target=init_worker,args=((i, global_data[i], random.choice(user_agents)),return_dict))
        procs.append(process)
        process.start()
        
    for i in procs:
        i.join()
    
    # results = return_dict.values()
    # save_data()
    # remove_temp()
    print("Done, Please check results.xlsx in your data folder!")
    time.sleep(10)