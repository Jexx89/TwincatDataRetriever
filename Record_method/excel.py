'''
TODO : 
- add a thread to record the data every second and limit the recording if the dataqueue in empty
- compelete the header to have all the data needed
- copy past to make a SQL base function
- add a function to copy past the actual more efficiently
'''

import openpyxl
import logging
from os import makedirs
from datetime import datetime
from threading import Thread, Event
from time import sleep

logging.basicConfig(filename='log\\trace.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Excel_recorder:
    def __init__(self,config,data):
        self.path = config["FOLDER_PATH"]
        self.record_time = config["RECORD_TIME"] 
        self.full_path = f"{self.path}\\Recording_{datetime.now().date()}.xlsx"
        self.header = ["RECORD_TIME", "ROUTE_NAME",  "ADS_TIME", "PLC_TIME"]
        self.data = data
        makedirs(self.path, exist_ok=True)
        self.initialize_excel()
        self.stop_event = Event()
        self.excel_recorder = Thread(target=self.record, args = (self.stop_event))

    def start(self):
        if self.excel_recorder.is_alive():
            self.excel_recorder.start()

    def stop(self):
        self.stop_event.set()
        self.excel_recorder.join()
        logging.info(f"Closing workbook {self.full_path}")
        self.save_workbook()
        self.workbook.close()
        self.sheet = None
        self.workbook= None

    def initialize_excel(self):
        try:
            workbook = openpyxl.load_workbook(self.full_path)
            logging.info("Opening existing workbook")
        except FileNotFoundError:
            workbook = openpyxl.Workbook()
            logging.info("Creating new workbook")
        sheet = workbook.active

        for col, value in enumerate(self.header, start=1):
            sheet.cell(row=1, column=col, value=value)

        logging.info("Initialized workbook")
        self.workbook =  workbook
        self.sheet = sheet
        self.save_workbook()

    def save_workbook(self):
        logging.info(f"Saving workbook {self.full_path}")
        self.workbook.save(self.full_path)

    def excel_record(self, data):
        self.sheet.append([datetime.now(), data])

    def record(self, stop_event):
        logging.info(f"Starting recording")
        while not stop_event.is_set():
            try:
                if not self.data.empty():
                    self.excel_record(self.data.get())
            except Exception as e:
                logging.error(f"Error while writting into the excel file : {e}")
            sleep(self.record_time)
    