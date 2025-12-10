import csv
from views.main_window import Ui_MainWindow
from model.seeduino import Seeeduino
from model.mock import Mock_seeduino
from model.sessions import Session
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import QtCore, QtWidgets
from datetime import datetime

class Main_window_controller(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.restricted_mode = False

        self.seeduino = Mock_seeduino()
        self.session = Session()

        self.ui.connect_device_btn.clicked.connect(self.connect_device)

        self.user_id = 0
        
        self.data = self.seeduino.data
        self.x_data = list(range(self.seeduino.buffer_size))
        self.x_data = [0] * self.seeduino.window_size  # X axis data
        self.y_data = [0] * self.seeduino.window_size  # Y axis data
        self.last_saved_index = 0

        self.line = self.ui.left_cheek_graph.plot(self.x_data, self.y_data)
        self.ui.left_cheek_graph.setYRange(0, 1023)


        # self.ui.left_cheek_high_graph.plot(self.data_x, self.data_y)
        self.ui.right_cheek_graph.plot([1,2,3,4,5,6,7,8,9], [5,10,15,20,25,30,35,40,45])

        self.ui.home_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.home_btn))
        self.ui.data_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.data_btn))
        self.ui.download_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.download_btn))
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(80) # Update every 80 ms
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        self.session_max_adc = None
        self.session_end_millis = None

    

    def nav_button_switching(self, button_name):
        buttons = {
            self.ui.home_btn: 0,
            self.ui.data_btn: 1,
            self.ui.download_btn: 2
        }

        self.ui.main_stackedWidget.setCurrentIndex(buttons[button_name])
        
        for btn in buttons:
            btn.setChecked(btn is button_name)

        if button_name == self.ui.home_btn:
            self.ui.left_cheek_graph.show()
            self.ui.right_cheek_graph.show()
            self.update_home_summary()
        if button_name == self.ui.data_btn:
            self.update_data_stats()

        if button_name == self.ui.download_btn:
            self.add_session_download()

    def connect_device(self):
        self.seeduino.serial_thread.start()
        self.ui.main_stackedWidget.setCurrentIndex(0)
        self.seeduino.serial_thread.new_sample.connect(self.add_data_graph)
    
    def update_plot(self):
        """Receive samples emitted by pyqtSignal and update the graph."""
        
        self.x_data[:-1] = self.x_data[1:]  # shift left to create scrolling effect
        self.y_data[:-1] = self.y_data[1:]
        self.x_data[-1] = self.data[-1][2] / 1000 if self.data else 0  # new millis value
        self.y_data[-1] = self.data[-1][1] if self.data else 0  # new adc_value
        self.line.setData(self.x_data, self.y_data)

    def add_data_graph(self, sample_index, adc_value, millis):
        print("add data '", sample_index, adc_value, millis)
        self.seeduino.data.append((sample_index, adc_value, millis))
        self.data = self.seeduino.data

        if self.session_max_adc is None or adc_value > self.session_max_adc:
            self.session_max_adc = adc_value
        self.session_end_millis = millis
        self.update_home_summary()

        if self.ui.main_stackedWidget.currentIndex() == 1:
            self.update_data_stats()

        if len(self.data) == self.seeduino.buffer_size:
            self.seeduino.flush_data(self.session.get_session_id(self.user_id, self.ui.session_label.text()))

    def update_home_summary(self):
        if self.session_max_adc is None or self.session_end_millis is None:
            self.ui.highest_value.setText("N/A")
            self.ui.time_value.setText("N/A")
            return

        self.ui.highest_value.setText(str(self.session_max_adc))
        end_time = datetime.fromtimestamp(self.session_end_millis / 1000.0).strftime("%M:%S")
        self.ui.time_value.setText(end_time)


    def set_restricted_mode(self, restricted: bool, session_id: int | None = None):
        self.restricted_mode = restricted

        if restricted:
            self.ui.home_btn.hide()
            self.ui.download_btn.setChecked(False)
            self.ui.data_btn.setChecked(True)

            self.ui.main_stackedWidget.setCurrentIndex(1)
            if session_id is not None:
                data = self.session.get_session_data(session_id)   # list of dicts
                # convert to same format as live mode: (sample_index, adc_value, millis)
                self.data = [
                    (s["sample_index"], s["adc_value"], s["millis"]) for s in data
                ]
                # recompute stats for this stored session
                if self.data:
                    self.session_max_adc = max(s[1] for s in self.data)
                    self.session_end_millis = self.data[-1][2]
                else:
                    self.session_max_adc = None
                    self.session_end_millis = None

                self.update_data_stats()
        else:
            self.ui.home_btn.show()
            self.ui.home_btn.setChecked(True)
            self.ui.data_btn.setChecked(False)
            self.ui.download_btn.setChecked(False)
            self.ui.main_stackedWidget.setCurrentIndex(3)

    def add_session_download(self):
        sessions = self.session.get_sessions(self.user_id)
        session_index = 0
        if self.ui.main_stackedWidget.currentIndex() != 2:
            return
        for i in sessions:
            session_index += 1
            label = QtWidgets.QLabel(parent=self.ui.scrollAreaWidgetContents)
            label.setText(i["name"])
            button = QtWidgets.QPushButton(parent=self.ui.scrollAreaWidgetContents)
            button.setText("Download the session")
            button.clicked.connect(lambda _, sid=i["id"]: self.download_session(sid))
            self.ui.gridLayout_4.addWidget(label, session_index, 0, 1, 1)
            self.ui.gridLayout_4.addWidget(button, session_index, 2, 1, 1)

    def download_session(self, session_id: int):
        data = self.session.get_session_data(session_id)
        if not data:
            print("No data found for session ID:", session_id)
            return
        filename = f"session_{session_id}_data.csv"
        try:
            with open(filename, 'a') as file:
                file.write("sample_index,adc_value,millis\n")
                for sample in data:
                    file.write(f"{sample['sample_index']},{sample['adc_value']},{sample['millis']}\n")
            print(f"Session data saved to {filename}")
        except Exception as e:
            print("Error saving session data:", e)

    def count_peaks(self, data, threshold=100, min_distance = 5):
        if len(data) < min_distance * 2:
            return 0
        peaks = 0
        last_peak_index = -min_distance
        for i in range(1, len(data) - 1):
            curr = data[i][1]
            prev = data[i - 1][1]
            next = data[i + 1][1]
            if curr > threshold and curr > prev and curr > next and i - last_peak_index >= min_distance:
                peaks += 1
                last_peak_index = i
        return peaks
    
    def update_data_stats(self):
        if not self.data:
            self.ui.label_7.setText("N/A")
            self.ui.label_8.setText("N/A")
            self.ui.label_9.setText("N/A")
            return
        max_adc = max(sample[1] for sample in self.data)
        self.ui.label_7.setText(str(max_adc))

        avg_adc = sum(sample[1] for sample in self.data) / len(self.data)
        self.ui.label_8.setText(f"{avg_adc:.1f}")

        peak_count = self.count_peaks(self.data)
        self.ui.label_9.setText(str(peak_count))