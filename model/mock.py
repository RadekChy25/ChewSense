from PyQt6.QtCore import QThread, pyqtSignal
import time

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
            adc_value += 5
            millis += 100
            self.new_sample.emit(sample_index, adc_value, millis)
            time.sleep(0.1)  # simulate delay between samples
            if time.time() - start_time >= 10:
                break

    def stop(self):
        self._stop_flag = True

class Mock_seeduino():
    def __init__(self):
        super().__init__()
        self.data = []
        self.buffer_size = 200
        self.serial_thread = MockSeeduinoThread()

    def closeEvent(self):
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread.wait()

    def flush_data(self):
        if not self.data:
            return

        chunk = self.data
        self.data = []  # free RAM

        payload = {
            "session_id": 1,
            "sample_rate": 1000,
            "samples": chunk  # stored as 2D array
        }