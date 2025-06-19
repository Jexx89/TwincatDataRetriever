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
TIMEOUT_PLC = 10 #in secondes
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

def get_routes_config():
    config = load_config()
    routes = config.get("routes")

    if routes:
        return routes

    # # Ask the user to select a file if path not set or doesn't exist
    # Tk().withdraw()  # Hide the root window
    # path = filedialog.askopenfilename(
    #     title="Select Excel file",
    #     filetypes=[("Excel files", "*.xlsx *.xls")]
    # )

    #if path:
    
    routes = {
        "ACV-2111-1":{"ACTIVE":False,"ROUTE_NAME":"ACV-2111-1", "AMS_NET_ID":"10.171.108.11.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.11", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC, "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 1 FSB"},
        "ACV-2111-2":{"ACTIVE":False,"ROUTE_NAME":"ACV-2111-2", "AMS_NET_ID":"10.171.108.12.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.12", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC,  "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 2 WSB"},
        "ACV-2111-3":{"ACTIVE":False,"ROUTE_NAME":"ACV-2111-3", "AMS_NET_ID":"10.171.108.13.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.13", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC,  "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 3 WSB"},
        "ACV_QUALITY":{"ACTIVE":True,"ROUTE_NAME":"ACV_QUALITY", "AMS_NET_ID":"10.171.108.14.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.14", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC,  "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test Quality"},
        "ACV_LIGNE":{"ACTIVE":False,"ROUTE_NAME":"ACV_LIGNE", "AMS_NET_ID":"10.171.108.15.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.15", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC,  "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test ligne"},
        "ACV_2014":{"ACTIVE":False,"ROUTE_NAME":"ACV_2014", "AMS_NET_ID":"10.171.108.16.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.16", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC,  "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 1 electrique"},
        "ACV_FUITE":{"ACTIVE":False,"ROUTE_NAME":"ACV_FUITE", "AMS_NET_ID":"10.171.108.17.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.17", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC,  "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc test de fuite WSB"},
        "ACV_BALLON":{"ACTIVE":False,"ROUTE_NAME":"ACV_BALLON", "AMS_NET_ID":"10.171.108.18.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.18", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC,  "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test ballon"},
        "ACV_PLATINE_ELECT":{"ACTIVE":False,"ROUTE_NAME":"ACV_PLATINE_ELECT", "AMS_NET_ID":"10.171.108.19.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.19", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC,  "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Band de test pour les platines electriques"},
        "ACV_3701":{"ACTIVE":False,"ROUTE_NAME":"ACV_3701", "AMS_NET_ID":"10.171.108.20.1.1", "TRANSPORT": "TCP/IP", "IP_ADDRESS":"10.171.108.20", "PORT": PORT_TC2PLC1, "TIMEOUT":TIMEOUT_PLC,  "FAST_SAMPLING_TIME":FAST_SAMPLING_TIME,"SLOW_SAMPLING_TIME":SLOW_SAMPLING_TIME, "USERNAME":"Administrator", "PASSWORD":"", "DESCRIPTION":"Banc de test 2 electrique"},
    }
    config['routes'] = routes

    config["other"] = "not defined yet"
    save_config(config)
    return routes
    # else:
    #     raise FileNotFoundError("No Excel file selected.")

if __name__=="__main__":
    test = get_routes_config()
    print(test)