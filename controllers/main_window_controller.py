from widgets.main_window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow

class main_window_controller(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)