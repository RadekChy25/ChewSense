from PyQt6.QtWidgets import QWidget
from views.first_window import Ui_Form
from controllers.start_session_controller import Start_session_controller
from controllers.create_user_form_controller import Create_user_form_controller
from controllers.main_window_controller import Main_window_controller
from model.user import User
from model.sessions import Session

class First_window_controller(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.user = User()
        self.session = Session()

        self.users = self.user.get_user()  # Save full user info
        self.ui.user_list.addItems([f"{u['first_name']} {u['last_name']}" for u in self.users])
        self.ui.user_list.currentIndexChanged.connect(self.update_session_list)
        
        self.create_user_controller = Create_user_form_controller()
        self.start_session_controller = Start_session_controller()
        self.main_window_controller = Main_window_controller()

        self.ui.add_user_btn.clicked.connect(self.add_user)
        self.ui.add_session_btn.clicked.connect(self.add_session)

        self.main_window_controller.ui.exit_btn.clicked.connect(self.close_main_window)

        self.create_user_controller.ui.add_user_btn.clicked.connect(self.create_user)
        self.start_session_controller.ui.start_session_btn.clicked.connect(self.create_session)

        if self.users:
            self.update_session_list(0)
                
    def add_user(self): 
        self.create_user_controller.show()

    def update_session_list(self, row):
        """Update the session_list based on selected user."""
        self.ui.session_list.clear()
        if row < 0 or row >= len(self.users):
            return
        user_id = self.users[row]["id"]
        sessions = self.session.get_sessions(user_id)
        session_names = [s["name"] for s in sessions]
        self.ui.session_list.addItems(session_names)
    
    #def get_session_list(self, user_ids):
        #sessions = self.session.get_sessions(user_ids)
        #return [session['name'] for session in sessions]

    def add_session(self):
        self.start_session_controller.show()

    def open_main_window(self):
        self.main_window_controller.show()
        
        if self.start_session_controller.isVisible() or self.isVisible():
            self.start_session_controller.close()
            self.close()

    def close_main_window(self):
        self.main_window_controller.close()
        self.show()

    def create_user(self):
        first_name = self.create_user_controller.ui.first_name_input.text()
        last_name = self.create_user_controller.ui.last_name_input.text()
        self.user.add_user(first_name, last_name)
        self.create_user_controller.close()
        self.users = self.user.get_user()  # Refresh user list
        self.ui.user_list.addItems([f"{u['first_name']} {u['last_name']}" for u in self.users])
        self.ui.user_list.setCurrentIndex(len(self.users) - 1)  # Select the newly added user

    def create_session(self):
        session_name = self.start_session_controller.ui.session_nr_input.text()
        selected_user_index = self.ui.user_list.currentIndex()
        if selected_user_index < 0 or selected_user_index >= len(self.users):
            print("No user selected.")
            return
        self.session.add_session(selected_user_index, session_name)
        self.main_window_controller.ui.session_label.setText(session_name)
        self.open_main_window()