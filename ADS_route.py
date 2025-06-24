'''
TODO : 
make different class 
    one for taking data and delete the RECORD tables in the PLC


'''
from threading import Thread, Event
from Lib import SharedVariable, run_task 
from datetime import datetime
from queue import Queue
import logging
from time import sleep

import os
os.add_dll_directory("C:\\TwinCAT\\AdsApi\\TcAdsDll\\x64")
import pyads
logging.basicConfig(filename='log\\trace.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

END_SHIFT_TIME= datetime(year = 2000, month = 1, day =1, hour=22,minute=30, second=0)
START_SHIFT_TIME = datetime(year = 2000, month = 1, day =1, hour=5,minute=0, second=0)
MIN_SEQ_VAL = 0
MAX_SEQ_VAL = 30

#%%ads_handler
class ADS:
    def __init__(self,route_cfg):
        self.route_cfg=route_cfg
        self.msg_route = f"{self.route_cfg["ROUTE_NAME"]}:{self.route_cfg["IP_ADDRESS"]}"
        self.plc = pyads.Connection(self.route_cfg["AMS_NET_ID"],self.route_cfg["PORT"],self.route_cfg["IP_ADDRESS"])
        self.connected = False

    def creat_route(self):
        '''
        how to use? on other system without twnicat'''
        self.route = pyads.add_route_to_plc(
            sending_net_id =self.route_cfg["AMS_NET_ID"],
            adding_host_name =self.route_cfg["IP_ADDRESS"],
            ip_address = self.route_cfg["IP_ADDRESS"],
            username = self.route_cfg["USERNAME"],
            password = self.route_cfg["PASSWORD"],
            route_name =self.route_cfg["ROUTE_NAME"],)

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
    
    def ads_state_to_name(self,code: int) -> str:
        ads_states = {
            0: "ADSSTATE_INVALID",
            1: "ADSSTATE_IDLE",
            2: "ADSSTATE_RESET",
            3: "ADSSTATE_INIT",
            4: "ADSSTATE_START",
            5: "ADSSTATE_RUN",# ✅ Normal operation
            6: "ADSSTATE_STOP",
            7: "ADSSTATE_SAVECFG",
            8: "ADSSTATE_LOADCFG",
            9: "ADSSTATE_POWERFAILURE",
            10: "ADSSTATE_POWERGOOD",
            11: "ADSSTATE_ERROR",
            12: "ADSSTATE_SHUTDOWN",
            13: "ADSSTATE_SUSPEND",
            14: "ADSSTATE_RESUME",
            15: "ADSSTATE_CONFIG",
            16: "ADSSTATE_RECONFIG"
        }
        return ads_states.get(code, f"UNKNOWN_STATE ({code})")

    def plc_state_to_name(self, code: int) -> str:
        plc_states = {
            0: "INVALID",
            1: "IDLE",
            2: "RESET",
            3: "INIT",
            4: "START",
            5: "RUN",            # ✅ Normal operation
            6: "STOP",
            7: "SAVECFG",
            8: "LOADCFG",
            9: "POWERFAILURE",
            10: "POWERGOOD",
            11: "ERROR",
            12: "SHUTDOWN",
            13: "SUSPEND",
            14: "RESUME",
            15: "CONFIG",
            16: "RECONFIG"
        }
        return plc_states.get(code, f"UNKNOWN_STATE ({code})")


#%%ads monitoring
class ADS_monitoring(ADS):
    def __init__(self,route_cfg):
        super().__init__(route_cfg)
        self.stop_monitor_event = Event()
        self.plc_monitor_thread = Thread(target=self.monitor, args = [self.stop_monitor_event])
        self.monitor_interval =self.route_cfg["TIMEOUT"]
        
    def start(self):
        if not self.plc_monitor_thread.is_alive():
            self.plc_monitor_thread.start()

    def stop(self):
        self.stop_monitor_event.set()

    def monitor(self,stop_event):
        logging.info(f"Starting monitoring for {self.msg_route}")
        while not stop_event.is_set():
            if not self.connected:
                self.connect()
            else:
                # Check connection status periodically
                try:
                    plc_state, ads_state = self.plc.read_state()  # tuple[int;int]  ==> adsState, deviceState
                    logging.info(f"PLC State: {self.plc_state_to_name(plc_state)}, ADS State: {self.ads_state_to_name(ads_state)}")
                except Exception as e:
                    logging.error(f"Connection to {self.msg_route} lost: {e}")
                    self.connected = False
            sleep(self.monitor_interval)
            # print(f"stop_monitoring_event : {self.stop_event.is_set()}//connected : {self.connected}// {self.route_cfg["TIMEOUT"]}")

#%%ads recording
class ADS_read(ADS):
    def __init__(self,route_cfg, data:Queue):
        super().__init__(route_cfg)
        self.sh_var = SharedVariable(self.route_cfg["SLOW_SAMPLING_TIME"])
        self.data = data
        self.stop_record_event = Event()
        self.stop_monitor_event = Event()
        self.plc_monitor_thread = Thread(target=self.monitor, args = [self.stop_monitor_event])
        self.plc_read_thread = Thread(target=run_task, args = (self.stop_record_event,self.sh_var,self.plc_read))
        self.monitor_interval =self.route_cfg["TIMEOUT"]
        
        

    def start(self):
        if not self.plc_read_thread.is_alive():
            logging.info(f"Starting recording for {self.msg_route}")
            self.plc_read_thread.start()
        if not self.plc_monitor_thread.is_alive():
            self.plc_monitor_thread.start()

    def stop(self):
        self.record_interval = 0.5
        self.sh_var.set(self.record_interval)
        self.stop_record_event.set()
        
        self.plc_read_thread.join()
        self.plc_monitor_thread.join()

    def plc_read(self):
        if self.connected:
            # Check connection status periodically
            try:
                data = self.plc.read_by_name(".TIME_NOW", pyads.PLCTYPE_STRING)
                #add functionnalities to check data
                # // from PLC : ROUTE_NAME // data - time // data
                record_data = [self.route_cfg["ROUTE_NAME"],datetime.now(),data]
                self.data.put(record_data)
            except Exception as e:
                logging.error(f"Connection to {self.msg_route} lost: {e}")
                self.connected = False

    def monitor(self,stop_event):
        logging.info(f"Starting monitoring for {self.msg_route}")
        while not stop_event.is_set():
            if not self.connected:
                self.connect()
            else:
                # Check connection status periodically
                try:
                    plc_state, ads_state = self.plc.read_state()  # tuple[int;int]  ==> adsState, deviceState
                    self.record_interval = self.update_sampling_time()
                    self.sh_var.set(self.record_interval)
                    logging.info(f"{self.route_cfg["ROUTE_NAME"]} PLC State: {self.plc_state_to_name(plc_state)}, ADS State: {self.ads_state_to_name(ads_state)}")
                except Exception as e:
                    logging.error(f"Connection to {self.msg_route} lost: {e}")
                    self.connected = False
            sleep(self.monitor_interval)

    def update_sampling_time(self):
        try:
            if self.night_standby():
                return self.route_cfg["SLOW_SAMPLING_TIME"]*60 # considering slow = 60sec ==> take data every hour 
            if self.test_ongoing():
                return self.route_cfg["SLOW_SAMPLING_TIME"]/2
            if self.test_f14_ongoing():
                return self.route_cfg["FAST_SAMPLING_TIME"]
            return self.route_cfg["SLOW_SAMPLING_TIME"]
        except Exception as e : 
            return self.route_cfg["SLOW_SAMPLING_TIME"]

    def test_ongoing(self):
        seq_test = self.get_actual_global_test_sequence()
        return MIN_SEQ_VAL < seq_test and seq_test < MAX_SEQ_VAL

    def test_f14_ongoing(self):
        f14_seq_fct = self.get_actual_f14_test_sequence()
        return 0 < f14_seq_fct

    def night_standby(self):
        actual_time = datetime.now().time()
        return actual_time < START_SHIFT_TIME.time() and END_SHIFT_TIME.time() < actual_time

    def get_actual_global_test_sequence(self):
        return self.plc.read_by_name(".SEQ", pyads.PLCTYPE_INT)

    def get_actual_f14_test_sequence(self):
        return self.plc.read_by_name("F14_TEST_PRINCIPALE.SEQ_FCT", pyads.PLCTYPE_INT)
