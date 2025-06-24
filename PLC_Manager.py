'''
TODO : 

put the monitor action in ADS_route
the thread should be over there and add the sampling time event



'''


from ADS_route import ADS_read as ADS
from Record_method import excel, sql, data_csv
import logging
from ConfigFile import get_routes_config

# Configuration logger
logging.basicConfig(filename='log\\trace.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


#%% PLCConnectionManager
class PLC_Manager:
    def __init__(self):
        self.__configurations = get_routes_config()
        self.routes = [ADS(configuration) for key, configuration in self.__configurations.items()]


    def start(self):
        self.connect()
        self.record()

    def connect(self):
        for route in self.routes:
            if route["ACTIVE"] and not route.connected:
                route.connect()

    def disconnect(self):
        for route in self.routes:
            if route["ACTIVE"] and route.connected:
                route.disconnect()


    def record(self):
        for route in self.routes:
            if route["ACTIVE"] and route.connected:
                route.start()

    def stop_record(self):
        for route in self.routes:
            if route["ACTIVE"] and route.connected:
                route.stop_record()

    def close_all(self):
        self.disconnect()

        # logging.info(f"Waiting threads : {self.ads_route.msg_route}")
        # logging.info(f"End : {self.ads_route.msg_route}")

