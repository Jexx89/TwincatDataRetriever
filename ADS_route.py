'''
TODO : 
make the monitoring come in this class
make different class one for monitoring, 
one for recording, 
one for taking data and delete the RECORD tables in the PLC 

'''

import queue
from threading import Thread, Event
from Shared_Parameter import SharedInterval, run_task
from datetime import datetime
import logging

import os
os.add_dll_directory("C:\\TwinCAT\\AdsApi\\TcAdsDll\\x64")
import pyads
logging.basicConfig(filename='log\\trace.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



#%%
class ADS_route:
    def __init__(self,route_cfg):
        self.route_cfg=route_cfg
        self.msg_route = f"{self.route_cfg["ROUTE_NAME"]}:{self.route_cfg["IP_ADDRESS"]}"
        self.plc = pyads.Connection(self.route_cfg["AMS_NET_ID"],self.route_cfg["PORT"],self.route_cfg["IP_ADDRESS"])
        self.connected = False
        self.interval_holder = SharedInterval(self.route_cfg["SLOW_SAMPLING_TIME"])
        self.data_queue = queue.Queue()
        self.stop_event = Event()
        self.plc_read_thread = Thread(target=run_task, args = (self.interval_holder,self.stop_event,self.plc_read))
        self.plc_read_thread.start()

    def creat_route(self):
        '''
        how to use? on other system without twnicat'''
        self.route = pyads.add_route_to_plc(
            sending_net_id =self.route_cfg["AMS_NET_ID"],
            adding_host_name =self.route_cfg["IP_ADDRESS"],
            ip_address = self.route_cfg["IP_ADDRESS"],
            username = self.route_cfg["USERNAME"],
            password = self.route_cfg["PASSWORD"],
            route_name =self.route_cfg["ROUTE_NAME"])

    def connect(self):
        try:
            self.plc.open()
            self.connected = True
            logging.info(f"Connected to PLC {self.msg_route}")
        except pyads.pyads_ex.ADSError as e:
            logging.error(f"ADS error occurred while connecting to {self.msg_route}: {e}")
            self.connected = False
        except Exception as e:
            logging.error(f"Error while connecting to {self.msg_route}: {e}")
            self.connected = False

    def disconnect(self):
        if self.connected:
            try:
                self.plc.close()
                self.connected = False
                logging.info(f"Disconnected from PLC at {self.msg_route}")
            except Exception as e:
                logging.error(f"Error while disconnecting from {self.msg_route}: {e}")

    def plc_read(self):
        logging.info(f"Starting recording for {self.msg_route}")
        while not self.stop_event.is_set():
            if self.connected:
                # Check connection status periodically
                try:
                    data = self.plc.read_by_name(".TIME_NOW", pyads.PLCTYPE_STRING)  # 
                    #add functionnalities to check data
                    self.data_queue.put(data)
                except Exception as e:
                    logging.error(f"Connection to {self.msg_route} lost: {e}")
                    self.connected = False

    def get_actual_global_test_sequence(self):
        return self.plc.read_by_name(".SEQ", pyads.PLCTYPE_INT)

    def get_actual_f14_test_sequence(self):
        return self.plc.read_by_name("F14_TEST_PRINCIPALE.SEQ_FCT", pyads.PLCTYPE_INT)

    def test_ongoing(self):
        MIN_SEQ_VAL = 0
        MAX_SEQ_VAL = 30
        seq_test = self.get_actual_global_test_sequence()
        return MIN_SEQ_VAL < seq_test and seq_test < MAX_SEQ_VAL

    def test_f14_ongoing(self):
        f14_seq_fct = self.get_actual_f14_test_sequence()
        return 0 < f14_seq_fct

    def night_standby(self):
        end_shift_time = datetime(hour=22,minute=30, second=0)
        start_shit_time = datetime(hour=5,minute=0, second=0)
        actual_time = datetime.now().time()
        return actual_time < start_shit_time and end_shift_time < actual_time

    def update_sampling_time(self):
        if self.night_standby():
            return self.route_cfg["SLOW_SAMPLING_TIME"]*60 # considering slow = 60sec ==> take data every hour 
        if self.test_ongoing():
            return self.route_cfg["SLOW_SAMPLING_TIME"]/2
        if self.test_f14_ongoing():
            return self.route_cfg["FAST_SAMPLING_TIME"]
        return self.route_cfg["SLOW_SAMPLING_TIME"]
