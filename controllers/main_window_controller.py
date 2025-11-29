from views.main_window import Ui_MainWindow
from model.seeduino import Seeeduino
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import QtCore

class Main_window_controller(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.seeduino = Seeeduino()

        self.data_x = []
        self.data_y = []
        self.data_z = []

        self.line = self.ui.left_cheek_high_graph.plot(
            self.data_x,
            self.data_y,
            symbol="+",
            symbolSize=15,
            symbolBrush="b",
        )


        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.plot)
        self.timer.start()

        
        self.seeduino.serial_thread.new_sample.connect(self.update_plot)

        #self.ui.left_cheek_high_graph.plot(self.data_x, self.data_y)
        self.ui.left_cheek_low_graph.plot([1,2,3,4,5,6,7,8,9], [5,10,15,20,25,30,35,40,45])

        self.ui.right_cheek_high_graph.plot([1,2,3,4,5,6,7,8,9], [5,10,15,20,25,30,35,40,45])
        self.ui.right_cheek_low_graph.plot([1,2,3,4,5,6,7,8,9], [5,10,15,20,25,30,35,40,45])

        self.ui.home_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.home_btn))
        self.ui.diagram_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.diagram_btn))
        self.ui.data_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.data_btn))
        self.ui.download_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.download_btn))

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
            self.ui.right_cheek_high_graph.show()
            self.ui.right_cheek_low_graph.show()
            self.seeduino.serial_thread.start()

    #def graph(self, sample_index, adc_value, millis):
        #self.data_x.append(millis)
        #self.data_y.append(adc_value)

    def connect_device(self):
        self.seeduino.serial_thread.start()
    
    def update_plot(self, sample_index, adc_value, millis):
        """Receive samples emitted by pyqtSignal and update the graph."""
        self.data_x.append(millis)
        self.data_y.append(adc_value)
        self.data_z.append(sample_index)  

        self.ui.left_cheek_high_graph.setData(self.data_x, self.data_y)

    def plot(self):
        self.line.setData(self.data_x, self.data_y)
