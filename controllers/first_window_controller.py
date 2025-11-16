
from PyQt6.QtWidgets import QWidget
from widgets.first_window import Ui_Form
from controllers.create_user_form_controller import create_user_form_controller


class first_window_controller(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.add_user_btn.clicked.connect(self.add_user)

    def add_user(self): 
        self.create_user_widget = create_user_form_controller()
        self.create_user_widget.show()