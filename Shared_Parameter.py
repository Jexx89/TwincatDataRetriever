from threading import Lock
from time import sleep, monotonic

# %% # Shared data structure with lock
class SharedInterval:
    def __init__(self, initial_value):
        self._interval = initial_value
        self._lock = Lock()

    def get(self):
        with self._lock:
            return self._interval

    def set(self, new_value):
        with self._lock:
            self._interval = new_value

def run_task(shared_interval, stop_event, task_fn):
    next_run = monotonic()
    while not stop_event.is_set():
        now = monotonic()
        interval = shared_interval.get()
        if now >= next_run:
            task_fn()
            next_run += interval
        sleep(0.1)  # Small yield to avoid 100% CPU usage
