from PyQt6.QtWidgets import QWidget
from views.delete_session_form import Ui_delete_session_form
from model.sessions import Session

class Delete_session_form_controller(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_delete_session_form()
        self.ui.setupUi(self)

        self.session = Session()
        self.session_id = None
        self.on_delete = None
        self.ui.delete_session_button.clicked.connect(self.delete_session)
        self.ui.close_btn.clicked.connect(self.close_window)

    def delete_session(self):
        if self.session_id is not None:
            print("Deleting session_id =", self.session_id)
            self.session.delete_session(self.session_id)
            if self.on_delete:
                self.on_delete()
            self.close()

    def close_window(self):
        self.close()
