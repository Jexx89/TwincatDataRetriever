'''
TODO : depending on the PLC, différent kind of data could be measured
make a list fot each PLC of the variable we need
note : we could creat a datastrucure to importe all in one go !
'''

import json
import os
os.add_dll_directory("C:\\TwinCAT\\AdsApi\\TcAdsDll\\x64")
# from tkinter import Tk, filedialog
from pyads import PORT_TC2PLC1

CONFIG_FILE = "config.json"
TIMEOUT_PLC = 3 #in secondes
FAST_SAMPLING_TIME = 1 #in secondes
SLOW_SAMPLING_TIME = 60 #in secondes

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_routes_config()->dict:
    config = get_config()
    return config.get("routes")

def get_config()->dict:
    config = load_config()
    if config:
        return config
    config = initialize_config_file()
    return config

def initialize_config_file()->dict:
    config={}
    routes = {
        "ACV-2111-1":       {"ACTIVE":True,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV-2111-1",           "AMS_NET_ID":"10.171.108.11.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.11", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 1 FSB"},
        "ACV-2111-2":       {"ACTIVE":True,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV-2111-2",           "AMS_NET_ID":"10.171.108.12.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.12", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 2 WSB"},
        "ACV-2111-3":       {"ACTIVE":True,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV-2111-3",           "AMS_NET_ID":"10.171.108.13.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.13", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 3 WSB"},
        "ACV_QUALITY":      {"ACTIVE":True,"CONNECTION_TYPE":"RECORD","ROUTE_NAME":"ACV_QUALITY",           "AMS_NET_ID":"10.171.108.14.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.14", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test Quality"},
        "ACV_LIGNE":        {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_LIGNE",           "AMS_NET_ID":"10.171.108.15.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.15", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test ligne"},
        "ACV_2014":         {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_2014",            "AMS_NET_ID":"10.171.108.16.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.16", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 1 electrique"},
        "ACV_FUITE":        {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_FUITE",           "AMS_NET_ID":"10.171.108.17.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.17", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc test de fuite WSB"},
        "ACV_BALLON":       {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_BALLON",          "AMS_NET_ID":"10.171.108.18.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.18", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test ballon"},
        "ACV_PLATINE_ELECT":{"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_PLATINE_ELECT",   "AMS_NET_ID":"10.171.108.19.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.19", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Band de test pour les platines electriques"},
        "ACV_3701":         {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_3701",            "AMS_NET_ID":"10.171.108.20.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.20", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 2 electrique"},
        }
    config['routes'] = routes
    config['recording'] = {"Excel" : {"FOLDER_PATH" : "C:\\ACV\\Coding Library\\Python\\TwincatDataRetriever\\Recording\\Excel", "RECORD_TIME" : FAST_SAMPLING_TIME},
                            "CSV" : {"FOLDER_PATH" : "C:\\ACV\\Coding Library\\Python\\TwincatDataRetriever\\Recording\\CSV", "RECORD_TIME" : FAST_SAMPLING_TIME},
                            "SQL" : {"parameter" : "not defined yet"}}
    save_config(config)
    return config

#%% main
def main():
    test = get_config()
    print(test)

if __name__=="__main__":
    main()