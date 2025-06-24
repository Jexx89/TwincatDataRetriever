'''
TODO : 
put the monitor action in ADS_route
the thread should be over there and add the sampling time event
'''
from ADS_route import ADS_monitoring, ADS_read
from Record_method import excel, sql, data_csv
from queue import Queue
import logging
from ConfigFile import get_config

# Configuration logger
logging.basicConfig(filename='log\\trace.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


#%% PLCConnectionManager
class PLC_Manager:
    def __init__(self):
        self.__configurations = get_config()
        self.__routes = self.__configurations["routes"]
        self.data_queue = Queue()
        self.routes = []
        for key, configuration in self.__routes.items():
            if configuration["CONNECTION_TYPE"] == "MONITOR":
                self.routes.append(ADS_monitoring(configuration))
            if configuration["CONNECTION_TYPE"] == "RECORD":
                self.routes.append(ADS_read(configuration,self.data_queue))
                self.excel = excel.Excel_recorder(self.__configurations["recording"]["Excel"], self.data_queue)

    def start(self):
        self.connect()
        self.record()
        self.excel.start()

    def stop(self):
        self.stop_record()
        self.disconnect()
        self.excel.stop()

    def connect(self):
        for route in self.routes:
            if route.route_cfg["ACTIVE"]:
                route.connect()

    def disconnect(self):
        for route in self.routes:
            if route.route_cfg["ACTIVE"]:
                route.disconnect()

    def record(self):
        for route in self.routes:
            if route.route_cfg["ACTIVE"]:
                route.start()

    def stop_record(self):
        for route in self.routes:
            if route.route_cfg["ACTIVE"]:
                route.stop()