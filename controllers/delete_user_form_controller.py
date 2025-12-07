from PyQt6.QtWidgets import QWidget
from views.delete_user_form import Ui_delete_user_form
from model.user import User

class Delete_user_form_controller(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_delete_user_form()
        self.ui.setupUi(self)

        self.user = User()
        self.user_id = None
        self.on_delete = None
        self.ui.delete_user_button.clicked.connect(self.delete_user)
        self.ui.close_btn.clicked.connect(self.close_window)

    def delete_user(self):
        if self.user_id is not None:
            self.user.delete_user(self.user_id)
            if self.on_delete:
                self.on_delete()
            self.close()

    def close_window(self):
        self.close()
