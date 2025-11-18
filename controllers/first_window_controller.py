
from PyQt6.QtWidgets import QWidget
from widgets.first_window import Ui_Form
from controllers.start_session_controller import Start_session_controller
from controllers.create_user_form_controller import Create_user_form_controller
from controllers.main_window_controller import Main_window_controller

class First_window_controller(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.create_user_controller = Create_user_form_controller()
        self.start_session_controller = Start_session_controller()
        self.main_window_controller = Main_window_controller()

        self.ui.add_user_btn.clicked.connect(self.add_user)
        self.ui.add_session_btn.clicked.connect(self.add_session)

        self.start_session_controller.ui.start_session_btn.clicked.connect(self.open_main_window)

    def add_user(self): 
        self.create_user_controller.show()

    def add_session(self):
        self.start_session_controller.show()

    def open_main_window(self):
        self.main_window_controller.show()
        
        if self.start_session_controller.isVisible() or self.isVisible():
            self.start_session_controller.close()
            self.close()
