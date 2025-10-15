from modules.config import PROXY_URL
import requests as req
from functools import lru_cache
import random

def new_list(count):
    try:
        print("Requesting new proxy list from server")
        res = req.get(f"{PROXY_URL}/proxy?t=2&num={count}")
        json_data = res.json()
        return json_data['data']
    except:
        raise Exception("Error occured on retrieving proxy data from server")

def get_list():
    data = []
    try:
        res = req.get(f"{PROXY_URL}/today_list?t=2&limit=100")
        json_data = res.json()
        for i in json_data["data"]:
            if i['binding']:
                data.append(f"http://127.0.0.1{i['binding']}")
        return data
    except:
        raise Exception("Error retrieving today list from server")


def get_single():
    data = get_list()
    choice = random.choice(data)
    if len(data) < 1:
        raise Exception("Tidak ada port yang di forward dari proxy")
    return choice