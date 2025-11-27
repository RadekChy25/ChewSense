from views.main_window import Ui_MainWindow
from model.arduino import SerialReaderThread
from PyQt6.QtWidgets import QMainWindow

class Main_window_controller(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.main_stackedWidget.setCurrentIndex(0)

        self.arduino = SerialReaderThread()
        self.arduino.stop()

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

    def graph(self):
        pass
