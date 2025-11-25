
from PyQt6.QtWidgets import QWidget
from widgets.start_session_widget import Ui_session_create
from controllers.main_window_controller import Main_window_controller


class Start_session_controller(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_session_create()
        self.ui.setupUi(self)

        self.ui.close_btn.clicked.connect(self.close_window)

    def close_window(self):
        self.close()