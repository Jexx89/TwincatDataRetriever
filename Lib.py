from threading import Lock
from time import sleep, monotonic
import queue

# %% # Shared data structure with lock
class SharedVariable:
    def __init__(self, interval):
        self._interval = interval
        self._lock = Lock()

    def get(self):
        with self._lock:
            return self._interval

    def set(self, new_value):
        with self._lock:
            self._interval = new_value


# class Shared_data:
#     def __init__(self):
#         self._record_interval:float
#         self._monitor_interval:float
#         self._data:queue.Queue
#         self._lock = Lock()

#     def get_record_interval(self):
#         with self._lock:
#             return self._interval

#     def set_record_interval(self, new_value):
#         with self._lock:
#             self._interval = new_value

#     def get_monitor_interval(self):
#         with self._lock:
#             return self._monitor_interval

#     def set_monitor_interval(self, new_value):
#         with self._lock:
#             self._monitor_interval = new_value

#     def get_data(self):
#         with self._lock:
#             return self._data
    
#     def set_data(self,new_value):
#         with self._lock:
#             self._data.put(new_value)

def run_task(stop_event, shared_interval, task_fn):
    next_run = monotonic()
    while not stop_event.is_set():
        now = monotonic()
        interval = shared_interval.get()
        if now >= next_run:
            task_fn()
            next_run += interval
        sleep(0.1)  # Small yield to avoid 100% CPU usage
