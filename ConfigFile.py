'''
TODO : 

'''

import pickle
import os
os.add_dll_directory("C:\\TwinCAT\\AdsApi\\TcAdsDll\\x64")
# from tkinter import Tk, filedialog
from pyads import PORT_TC2PLC1,PLCTYPE_REAL,PLCTYPE_LREAL,PLCTYPE_STRING, PLCTYPE_INT

CONFIG_FILE = "config.pkl"
TIMEOUT_PLC = 3 #in secondes
FAST_SAMPLING_TIME = 1 #in secondes
SLOW_SAMPLING_TIME = 60 #in secondes

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'rb') as f:
            try:
                return pickle.load(f)
            except (pickle.UnpicklingError, FileNotFoundError, EOFError) as e:
                return {}
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'wb') as f:
        try:
            pickle.dump(config, f)
        except (pickle.PicklingError, IOError) as e:
            print(f"Error while saving pickle: {e}")

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
        "ACV-2111-1":       {"ACTIVE":True,"CONNECTION_TYPE":"RECORD","ROUTE_NAME":"ACV-2111-1",           "AMS_NET_ID":"10.171.108.11.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.11", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 1 FSB"},
        "ACV-2111-2":       {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV-2111-2",           "AMS_NET_ID":"10.171.108.12.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.12", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 2 WSB"},
        "ACV-2111-3":       {"ACTIVE":True,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV-2111-3",           "AMS_NET_ID":"10.171.108.13.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.13", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 3 WSB"},
        "ACV_QUALITY":      {"ACTIVE":True,"CONNECTION_TYPE":"RECORD","ROUTE_NAME":"ACV_QUALITY",           "AMS_NET_ID":"10.171.108.14.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.14", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test Quality"},
        "ACV_LIGNE":        {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_LIGNE",           "AMS_NET_ID":"10.171.108.15.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.15", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test ligne"},
        "ACV_2014":         {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_2014",            "AMS_NET_ID":"10.171.108.16.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.16", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 1 electrique"},
        "ACV_FUITE":        {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_FUITE",           "AMS_NET_ID":"10.171.108.17.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.17", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc test de fuite WSB"},
        "ACV_BALLON":       {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_BALLON",          "AMS_NET_ID":"10.171.108.18.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.18", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test ballon"},
        "ACV_PLATINE_ELECT":{"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_PLATINE_ELECT",   "AMS_NET_ID":"10.171.108.19.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.19", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Band de test pour les platines electriques"},
        "ACV_3701":         {"ACTIVE":False,"CONNECTION_TYPE":"MONITOR","ROUTE_NAME":"ACV_3701",            "AMS_NET_ID":"10.171.108.20.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.20", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 2 electrique"},
        }
    recording = {"Excel" : {"FOLDER_PATH" : "C:\\ACV\\Coding Library\\Python\\TwincatDataRetriever\\Recording\\Excel", "RECORD_TIME" : SLOW_SAMPLING_TIME},
                            "CSV" : {"FOLDER_PATH" : "C:\\ACV\\Coding Library\\Python\\TwincatDataRetriever\\Recording\\CSV", "RECORD_TIME" : FAST_SAMPLING_TIME*5},
                            "SQL" : {"parameter" : "not defined yet"}}
    structure_data = (
            ("PLC_TIME",PLCTYPE_STRING,1,20),
            ("RIG_WATER_T_IN",PLCTYPE_REAL,1),
            ("RIG_WATER_T_OUT",PLCTYPE_REAL,1),
            ("RIG_WATER_T_REGUL",PLCTYPE_REAL,1),
            ("RIG_WATER_FLOW",PLCTYPE_REAL,1),
            ("RIG_WATER_FLOW_REGUL",PLCTYPE_REAL,1),
            ("RIG_WATER_PRESS",PLCTYPE_REAL,1),
            
            ("RIG_AMB_T",PLCTYPE_REAL,1),
            ("RIG_AMB_PRESS",PLCTYPE_REAL,1),

            ("RIG_GAZ_T",PLCTYPE_REAL,1),
            ("RIG_GAZ_PRESS",PLCTYPE_REAL,1),
            ("RIG_GAZ_PRESS_REGUL",PLCTYPE_REAL,1),
            ("RIG_GAZ_DEBIT",PLCTYPE_REAL,1),
            ("RIG_GAZ_CUMUL",PLCTYPE_LREAL,1),
            ("RIG_GAZ_PRESS_OFF",PLCTYPE_REAL,1),

            ("RIG_FLUE_T",PLCTYPE_REAL,1),
            ("RIG_FLUE_CO",PLCTYPE_REAL,1),
            ("RIG_FLUE_CO2",PLCTYPE_REAL,1),

            ("SEQ", PLCTYPE_INT,1),
            ("SEQ_FCT14", PLCTYPE_INT,1),
            )

    config['routes'] = routes
    config['recording'] = recording
    config["data_structure"] = structure_data
    save_config(config)
    return config

#%% main
def main():
    test = get_config()
    print(test)

if __name__=="__main__":
    main()