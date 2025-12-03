
from PyQt6.QtWidgets import QWidget
from views.create_user_form import Ui_create_user_form
from model.user import User

class Create_user_form_controller(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_create_user_form()
        self.ui.setupUi(self)

        self.ui.close_btn.clicked.connect(self.close_window)

    def close_window(self):
        self.close()

    def load_users():
        users = User.get_user()
        return users