import os  
import tomllib

config_data = {}


with open("data/config.toml",'rb') as f:
    config_data = tomllib.load(f)

LOGIN_URL = config_data["target"]["LOGIN_URL"]
ENABLE_PROXY = config_data["proxy"]["ENABLE_PROXY"]
PROXY_HOST = config_data["proxy"]["PROXY_HOST"]
PROXY_PORT = config_data["proxy"]["PROXY_PORT"]

LICENSE_HOST = config_data["license"]["LICENSE_HOST"]
LICENSE_KEY = config_data["license"]["LICENSE_KEY"]

PROXY_URL = f"{PROXY_HOST}:{PROXY_PORT}/api"
LICENSE_URL = f"{LICENSE_HOST}/{LICENSE_KEY}"


def remove_temp():
    try:
        os.remove("data/temp_result.txt")
    except:
        pass