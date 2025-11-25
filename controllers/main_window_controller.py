from views.main_window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow

class Main_window_controller(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.home_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.home_btn))
        self.ui.diagram_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.diagram_btn))
        self.ui.data_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.data_btn))
        self.ui.download_btn.clicked.connect(lambda: self.nav_button_switching(self.ui.download_btn))

    def nav_button_switching(self, button_name):
        buttons = [
            self.ui.home_btn,
            self.ui.diagram_btn,
            self.ui.data_btn,
            self.ui.download_btn
        ]
        
        for btn in buttons:
            btn.setChecked(btn is button_name)
