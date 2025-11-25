
from PyQt6.QtWidgets import QWidget
from widgets.create_user_form import Ui_create_user_form

class Create_user_form_controller(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_create_user_form()
        self.ui.setupUi(self)

        self.ui.close_btn.clicked.connect(self.close_window)

    def close_window(self):
        self.close()