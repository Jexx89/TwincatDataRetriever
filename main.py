import pyads.pyads_ex
import datetime
import logging
from threading import Thread, Event
from time import sleep
import openpyxl

from openpyxl import Workbook
import os

# Configuration logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PLCConnectionManager:
    def __init__(self, ip, port, username, password, retry_interval=5, path_to_wb:str="C:\\ACV\\Coding Library\\Python\\TwincatDataRetriever\\recording\\template.xlsx"):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.retry_interval = retry_interval
        self.initialize_excel(path_to_wb)
        self.plc = pyads.Connection(self.ip, self.port, self.username, self.password)
        self.connected = False
        self.stop_recording_event = Event()
        self.stop_monitoring_event = Event()
        

    def connect(self):
        try:
            self.plc.open()
            self.connected = True
            logging.info(f"Connected to PLC at {self.ip}")
        except pyads.pyads_ex.ADSError as e:
            logging.error(f"ADS error occurred while connecting to {self.ip}: {e}")
            self.connected = False
        except Exception as e:
            logging.error(f"Error while connecting to {self.ip}: {e}")
            self.connected = False

    def disconnect(self):
        if self.connected:
            try:
                self.plc.close()
                self.connected = False
                logging.info(f"Disconnected from PLC at {self.ip}")
            except Exception as e:
                logging.error(f"Error while disconnecting from {self.ip}: {e}")

    def read_data(self):
        if self.connected:
            try:
                data = self.plc.read_by_name("ANA_IN.COEF_RHEOSTAT", pyads.PLCTYPE_REAL)  # Replace with correct path and datatype
                logging.info(f"Data from {self.ip}: {data}")
            except pyads.pyads_ex.ADSError as e:
                logging.error(f"Error while reading data from {self.ip}: {e}")
                self.connected = False
            except Exception as e:
                logging.error(f"Error while reading data from {self.ip}: {e}")
                self.connected = False

    def monitor_connection(self):
        while not self.stop_monitoring_event.is_set():
            if not self.connected:
                self.connect()

            if self.connected:
                # Check connection status periodically
                try:
                    self.plc.read_by_name("ANA_IN.COEF_RHEOSTAT", pyads.PLCTYPE_REAL)  # Replace with correct status path
                except Exception as e:
                    logging.error(f"Connection to {self.ip} lost: {e}")
                    self.connected = False

            sleep(self.retry_interval)

    def stop_monitoring(self):
        self.stop_monitoring_event.set()
        self.disconnect()

    def recording(self, sample_time):
        while not self.stop_monitoring_event.is_set():
            if not self.connected:
                self.connect()

            if self.connected:
                # Check connection status periodically
                try:
                    data = self.plc.read_by_name("ANA_IN.COEF_RHEOSTAT", pyads.PLCTYPE_REAL)  # Replace with correct status path
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.sheet.append([current_time, data])
                except Exception as e:
                    logging.error(f"Connection to {self.ip} lost: {e}")
                    self.connected = False

            sleep(sample_time)

    def stop_recording(self):
        self.stop_recording_event.set()



    def initialize_excel(self, file_path):
        try:
            workbook = openpyxl.load_workbook(file_path)
            logging.info("Opened existing workbook")
        except FileNotFoundError:
            workbook = Workbook()
            logging.info("Created new workbook")

        sheet = workbook.active
        sheet.append(["Timestamp", "Temperature"])

        workbook.save(file_path)
        logging.info("Initialized workbook")
        self.workbook =  workbook
        self.sheet = sheet


if __name__ == '__main__':
    # List of PLCs to monitor and maintain connections for
    os.environ['Path'] += ';C:\\TwinCAT\\AdsApi\\TcAdsDll\\'
    
    
    ipaddress = "10.171.108.13"
    path_to_wb= f"C:\\ACV\\Coding Library\\Python\\TwincatDataRetriever\\recording\\PLC_{ipaddress}.xlsx"
    
    
    plcs = [
        PLCConnectionManager(ipaddress, pyads.PORT_TC2PLC1, "Administrator", "",5,path_to_wb),
        #PLCConnectionManager("192.168.0.2", 80, "user2", "password2"),
        # Add more as necessary
    ]

    # Start monitoring threads
    for plc in plcs:
        monitor_thread = Thread(target=plc.monitor_connection)
        monitor_thread.start()

    # Start monitoring threads
    for plc in plcs:
        recording_thread = Thread(target=plc.recording(1))
        recording_thread.start()
    # for i in range (60):
    #     for plc in plcs:
    #         plc.read_data()
    #     sleep(1)


    sleep(120)
    # To stop monitoring, call stop_monitoring() on each PLC manager
    for plc in plcs:
        plc.stop_recording()
        plc.stop_monitoring()
        plc.workbook.save(path_to_wb)
        