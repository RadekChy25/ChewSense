import serial
import serial.tools.list_ports
from PyQt6.QtCore import QThread, pyqtSignal

class SerialReaderThread(QThread):
    new_sample = pyqtSignal(int, int, int)  # sample_index, adc_value, millis

    def __init__(self, port, baudrate=115200, parent=None):
        super().__init__(parent)
        self.baudrate = baudrate
        self._stop_flag = False
        self.serial = None
        self.ports = port

    def run(self):
        try:
            self.serial = serial.Serial(self.ports, self.baudrate, timeout=1)
            self.serial.flush()

            while not self._stop_flag:
                line = self.serial.readline().decode('utf-8', errors='ignore').strip()
                if not line or line.startswith('#'):
                    continue
                try:
                    parts = line.split(',')
                    if len(parts) == 3:
                        sample_index = int(parts[0])
                        adc_value = int(parts[1])
                        millis = int(parts[2])
                        self.new_sample.emit(sample_index, adc_value, millis)
                except ValueError:
                    continue  # just skip faulty lines
        except Exception as e:
            print("SerialReaderThread error:", e)

        if self.serial and self.serial.is_open:
            self.serial.close()

    def stop(self):
        self._stop_flag = True


class Seeeduino():
    def __init__(self):
        super().__init__()

        self.serial_thread = SerialReaderThread(self.detect_seeeduino_port())
        self.closeEvent()
        self.serial_thread.new_sample.connect(self.handle_emg_sample)
        self.serial_thread.start()

    def handle_emg_sample(self, sample_index, adc_value, millis):
        print(f"EMG: {sample_index}, {adc_value}, {millis} ms")
    

    def closeEvent(self):
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread.wait()

    def detect_seeeduino_port(self):
        seeeduino_ports = []
        for port in serial.tools.list_ports.comports():
            desc = port.description.lower()
            if (
                "seeeduino" in desc
                or "ch340" in desc
                or "wchusb" in desc
                or port.vid == 0x1A86 and port.pid == 0x7523  # CH340G Driver detection
                or port.vid == 0x10C4 and port.pid == 0xEA60  # CP2102 Driver detection
                or port.vid == 0x2341  # from an official Arduino thingy
            ):
                seeeduino_ports.append(port.device)

        if not seeeduino_ports:
            raise IOError("sEMG not detected. Please check the USB connection.")
        elif len(seeeduino_ports) == 1:
            return seeeduino_ports[0]
        else:
            print("Multiple compatible ports found:")
            for i, p in enumerate(seeeduino_ports):
                print(f"{i}: {p}")
            choice = int(input("Select port number: "))
            return seeeduino_ports[choice]
        
