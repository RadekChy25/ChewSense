from views.main_window import Ui_MainWindow
from model.seeduino import Seeeduino
from model.mock import Mock_seeduino
from model.sessions import Session
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import QtCore

class Main_window_controller(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.main_stackedWidget.setCurrentIndex(4)

        self.seeduino = Mock_seeduino()
        self.session = Session()

        self.ui.connect_device_btn.clicked.connect(self.connect_device)

        self.user_id = 0
        
        self.data = self.seeduino.data
        self.x_data = list(range(self.seeduino.buffer_size))
        self.x_data = [0] * self.seeduino.window_size  # X axis data
        self.y_data = [0] * self.seeduino.window_size  # Y axis data
        self.last_saved_index = 0

        self.line = self.ui.left_cheek_high_graph.plot(self.x_data, self.y_data)
        self.ui.left_cheek_high_graph.setYRange(0, 1023)


        # self.ui.left_cheek_high_graph.plot(self.data_x, self.data_y)
        self.ui.left_cheek_low_graph.plot([1,2,3,4,5,6,7,8,9], [5,10,15,20,25,30,35,40,45])

        self.ui.right_cheek_high_graph.plot([1,2,3,4,5,6,7,8,9], [5,10,15,20,25,30,35,40,45])
        self.ui.right_cheek_low_graph.plot([1,2,3,4,5,6,7,8,9], [5,10,15,20,25,30,35,40,45])

        self.ui.home_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.home_btn))
        self.ui.diagram_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.diagram_btn))
        self.ui.data_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.data_btn))
        self.ui.download_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.download_btn))
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(80) # Update every 80 ms
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def nav_button_switching(self, button_name):
        buttons = {
            self.ui.home_btn: 0,
            self.ui.diagram_btn: 1,
            self.ui.data_btn: 2,
            self.ui.download_btn: 3
        }

        self.ui.main_stackedWidget.setCurrentIndex(buttons[button_name])
        
        for btn in buttons:
            btn.setChecked(btn is button_name)

        if button_name == self.ui.home_btn:
            self.ui.left_cheek_high_graph.show()
            self.ui.left_cheek_low_graph.show()
            # self.ui.right_cheek_high_graph.show()
            self.ui.right_cheek_low_graph.show()

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
            self.seeduino.flush_data(self.session.get_session_id(self.user_id, self.ui.session_label.text()))
