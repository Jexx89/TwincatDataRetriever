'''
TODO : 

put the monitor action in ADS_route
the thread should be over there and add the sampling time event



'''


import ADS_route
import Excel_recording
from threading import Thread, Event, Lock
import logging


# Configuration logger
logging.basicConfig(filename='log\\trace.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


#%% PLCConnectionManager
class PLCConnectionManager:
    def __init__(self, ads_route:ADS_route ,excel_recording:Excel_recording, route_cfg):
        self.route_cfg=route_cfg
        self.excel_recording=excel_recording
        self.ads_route=ads_route
        self.ads_route.connect()
        # self.stop_event = Event()
        # self.threads = [Thread(target=self.monitor_connection),Thread(target=self.recording)]
        # for thread in self.threads:
        #     thread.start()

    # def recording(self):
    #     sampling_time = self.slow_sampling_time
    #     logging.info(f"Starting recording for {self.ads_route.msg_route}")
    #     while not self.stop_event.is_set() or not self.data_queue.empty():
    #         if self.ads_route.connected:
    #             # Check connection status periodically
    #             try:
    #                 sequence = self.ads_route.plc.read_by_name(".TIME_NOW", pyads.PLCTYPE_STRING)  # Replace with correct status path
    #                 data = self.ads_route.plc.read_by_name(".TIME_NOW", pyads.PLCTYPE_STRING)  # Replace with correct status path
    #                 #add functionnalities to check data
    #                 self.data_queue.put(data)
    #                 self.excel_recording.excel_record(data)
                    
    #             except Exception as e:
    #                 logging.error(f"Connection to {self.ads_route.msg_route} lost: {e}")
    #                 self.ads_route.connected = False
    #         # print(f"stop_recording_event : {self.stop_event.is_set()}//connected : {self.ads_route.connected}// {self.route_cfg["SAMPLING_TIME"]}")
    
    def monitor_connection(self):
        
        def ads_state_to_name(code: int) -> str:
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
        def plc_state_to_name(code: int) -> str:
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

        logging.info(f"Starting monitoring for {self.ads_route.msg_route}")
        while not self.stop_event.is_set():
            if not self.ads_route.connected:
                self.ads_route.connect()
            else:
                # Check connection status periodically
                try:
                    plc_state, ads_state = self.ads_route.plc.read_state()  # tuple[int;int]  ==> adsState, deviceState
                    # logging.info(f"PLC State: {plc_state_to_name(plc_state)}, ADS State: {ads_state_to_name(ads_state)}")
                except Exception as e:
                    logging.error(f"Connection to {self.ads_route.msg_route} lost: {e}")
                    self.ads_route.connected = False
            # print(f"stop_monitoring_event : {self.stop_event.is_set()}//connected : {self.ads_route.connected}// {self.route_cfg["TIMEOUT"]}")

    def close_all(self):
        logging.info(f"Stopping all functionalities : {self.ads_route.msg_route}")
        # self.stop_event.set()
        self.ads_route.disconnect()
        self.excel_recording.save_workbook()
        logging.info(f"Waiting threads : {self.ads_route.msg_route}")
        # for thread in self.threads:
        #     thread.join()
        logging.info(f"End : {self.ads_route.msg_route}")

