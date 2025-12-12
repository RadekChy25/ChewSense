from PyQt6.QtCore import QThread, pyqtSignal, QThreadPool
from model.emg import SaveSamplesWorker
import time
import random as rd

class MockSeeduinoThread(QThread):
    new_sample = pyqtSignal(int, int, int)  # sample_index, adc_value, millis

    def __init__(self):
        super().__init__()
        self._stop_flag = False

    def run(self):
        start_time = time.time()
        sample_index = 0
        adc_value = 0
        millis = 0
        while not self._stop_flag:
            sample_index += 1
            adc_value = rd.randint(0, 1023)
            millis += 100
            self.new_sample.emit(sample_index, adc_value, millis) 
            time.sleep(0.001)  # simulate delay
            if time.time() - start_time >= 60:
                break

    def stop(self):
        self._stop_flag = True

class Mock_seeduino():
    def __init__(self):
        super().__init__()
        self.data = []
        self.buffer_size = 10000
        self.window_size = 250
        self.serial_thread = MockSeeduinoThread()
        self.thread_pool = QThreadPool()

    def closeEvent(self):
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread.wait()

    def flush_data(self, session_id: str):
        if not self.data:
            return

        chunk = self.data  # free RAM
        self.data = []

        payload = {
            "session_id": session_id,
            "adc_values": [d[1] for d in chunk],
            "mili_seconds": [d[2] for d in chunk],
        }

        worker = SaveSamplesWorker(payload)
        self.thread_pool.start(worker)
        print("Saved ")
