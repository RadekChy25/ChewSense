import pandas as pd
from views.main_window import Ui_MainWindow
from model.seeduino import Seeeduino
from model.mock import Mock_seeduino
from model.sessions import Session
from model.emg import EMG
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6 import QtCore, QtWidgets

class Main_window_controller(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.restricted_mode = False

        self.seeduino = Mock_seeduino()
        self.session = Session()
        self.emg = EMG()

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
        self.seeduino.data.append((sample_index, adc_value, millis))
        self.data = self.seeduino.data

        if len(self.data) == self.seeduino.buffer_size:
            print(f"Id {self.session.get_session_id(self.user_id, self.ui.session_label.text())}")
            self.seeduino.flush_data(self.session.get_session_id(self.user_id, self.ui.session_label.text()))

    def set_restricted_mode(self, restricted: bool):
        self.restricted_mode = restricted

        if restricted:
            self.ui.home_btn.hide()
            self.ui.download_btn.setChecked(False)
            self.ui.data_btn.setChecked(True)

            self.ui.main_stackedWidget.setCurrentIndex(1)
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
            button.clicked.connect(lambda _, sid=i["id"], sname=i["name"]: self.download_session(sid, sname))
            self.ui.gridLayout_4.addWidget(label, session_index, 0, 1, 1)
            self.ui.gridLayout_4.addWidget(button, session_index, 2, 1, 1)

        self.ui.download_all_button.clicked.connect(self.download_all_sessions)

    def save_emg_to_csv(self, emg_data, session_name):
        rows = []

        rows.append({
            "session_name": session_name,
            "mili_seconds": "",
            "adc_value": ""
        })

        for d in emg_data:
            for t, val in zip(d["mili_seconds"], d["adc_values"]):
                rows.append({
                    "session_name": "",
                    "mili_seconds": t,
                    "adc_value": val
                })

        return rows

    def download_session(self, session_id: int, session_name: str):
        emg_data = self.emg.get_emg_data(session_id)

        file_path, _ = QFileDialog.getSaveFileName(
            self.ui.main_stackedWidget,
            "Save CSV",
            f"{session_name}.csv",  # default filename
            "CSV Files (*.csv);;All Files (*)"
        )

        data = pd.DataFrame(self.save_emg_to_csv(emg_data, session_name))

        if not file_path:
            data.to_csv(file_path, mode='w', index=False, header=True)
        else:
            data.to_csv(file_path, mode='a', index=False, header=False)


    def download_all_sessions(self):
        sessions = self.session.get_sessions(self.user_id)
        if not sessions:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self.ui.main_stackedWidget,
            "Save all sessions CSV",
            "all_sessions.csv",
            "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        combined_data = {} 

        for s in sessions:
            emg_data = self.emg.get_emg_data(s["id"])
            for d in emg_data:
                max_len = max(max_len, len(d["mili_seconds"]))

        # Initialize combined_data with mili_seconds (0..max_len-1)
        combined_data["mili_seconds"] = list(range(max_len))

        # Add each session as side-by-side columns
        for s in sessions:
            emg_data = self.emg.get_emg_data(s["id"])
            col_name = f"{s['name']}_adc_values"
            adc_values = []


            combined_data[col_name] = adc_values

        # Create DataFrame and save CSV
        df = pd.DataFrame(combined_data)
        df.to_csv(file_path, index=False)
        print(f"All sessions saved side by side in {file_path}")

