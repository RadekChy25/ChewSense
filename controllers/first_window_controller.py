
from PyQt6.QtWidgets import QWidget
from widgets.first_window import Ui_Form
from controllers.start_session_controller import Start_session_controller
from controllers.create_user_form_controller import Create_user_form_controller

class First_window_controller(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.add_user_btn.clicked.connect(self.add_user)
        self.ui.add_session_btn.clicked.connect(self.add_session)

    def add_user(self): 
        self.create_user_widget = Create_user_form_controller()
        self.create_user_widget.show()

    def add_session(self):
        self.create_session_widget = Start_session_controller()
        self.create_session_widget.show()