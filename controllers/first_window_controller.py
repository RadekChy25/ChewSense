from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from views.first_window import Ui_Form
from controllers.start_session_controller import Start_session_controller
from controllers.create_user_form_controller import Create_user_form_controller
from controllers.main_window_controller import Main_window_controller
from controllers.delete_user_form_controller import Delete_user_form_controller
from controllers.delete_session_form_controller import Delete_session_form_controller
from model.user import User
from model.sessions import Session

class First_window_controller(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.user = User()
        self.session = Session()
        self.create_user_controller = Create_user_form_controller()
        self.start_session_controller = Start_session_controller()
        self.main_window_controller = Main_window_controller()
        self.delete_user_form_controller = Delete_user_form_controller()
        self.delete_session_form_controller = Delete_session_form_controller()

        self.users = self.user.get_user()  # Save full user info
        self.sessions = []
        self.ui.user_list.clear()
        if self.users:
            self.ui.user_list.addItems([f"{u['first_name']} {u['last_name']}" for u in self.users])
            #self.ui.user_list.setCurrentIndex(-1)
       # self.ui.user_list.currentIndexChanged.connect(self.update_session_list)
        self.ui.session_list.clear()
        self.ui.user_list.setCurrentIndex(-1)
        self.ui.session_list.setCurrentIndex(-1)
        self.ui.user_list.currentIndexChanged.connect(self.update_session_list)
    

        self.ui.add_user_btn.clicked.connect(self.add_user)
        self.ui.add_session_btn.clicked.connect(self.add_session)
        self.ui.delete_user_btn.clicked.connect(self.open_delete_user_form)
        self.ui.delete_session_btn.clicked.connect(self.open_delete_session_form)
        self.ui.go_to_main.clicked.connect(self.open_main_window)


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
        if row < 0:
            self.sessions = []
            return
        if row >= len(self.users):
            self.sessions = []
            return 
        user_id = self.users[row]["id"]
        self.sessions = self.session.get_sessions(user_id)
        session_names = [s["name"] for s in self.sessions]
        if session_names:
            self.ui.session_list.addItems(session_names)
            self.ui.session_list.setCurrentIndex(-1)
        else:
            self.ui.session_list.setCurrentIndex(-1)
    

    def add_session(self):
        self.start_session_controller.show()

    def open_delete_user_form(self):
        index = self.ui.user_list.currentIndex()
        if index < 0 or index >= len(self.users):
            return
        user_id = self.users[index]["id"]
        self.delete_user_form_controller.user_id = user_id
        self.delete_user_form_controller.on_delete =self.refresh_user_list
        self.delete_user_form_controller.show()

    def open_main_window(self):
        user_index = self.ui.user_list.currentIndex()
        if user_index < 0 or user_index >= len(self.users):
            print("No user selected.")
            return
        user_id = self.users[user_index]["id"]
        self.main_window_controller.user_id = user_id
        self.main_window_controller.ui.user_label.setText(self.ui.user_list.currentText())
        session_index = self.ui.session_list.currentIndex()
        if session_index >= 0 and session_index < len(self.sessions):
            session_id = self.sessions[session_index]["id"]
            session_name = self.sessions[session_index]["name"]
            self.main_window_controller.session_id = session_id
            self.main_window_controller.ui.session_label.setText(session_name)
        else:
            self.main_window_controller.ui.session_label.setText("No session selected")
        self.main_window_controller.show()
        if self.start_session_controller.isVisible():
            self.start_session_controller.close()
        if self.isVisible():
            self.close()
         
    

    def close_main_window(self):
        self.main_window_controller.close()
        self.main_window_controller.seeduino.serial_thread.stop()
        self.show()

    def create_user(self):
        first_name = self.create_user_controller.ui.first_name_input.text()
        last_name = self.create_user_controller.ui.last_name_input.text()
        if not first_name or not last_name:
            print("First name and last name cannot be empty.")
            return
        self.user.add_user(first_name, last_name)
        self.create_user_controller.close()
        self.refresh_user_list()
        if self.users:
            new_user_index = len(self.users) - 1
            self.ui.user_list.setCurrentIndex(new_user_index)   
            self.update_session_list(new_user_index)

    def refresh_user_list(self):
        self.users = self.user.get_user()
        self.ui.user_list.clear()
        self.ui.user_list.addItems([f"{u['first_name']} {u['last_name']}" for u in self.users])
        if self.users:
            self.ui.user_list.setCurrentIndex(-1)
            self.update_session_list(-1)

    def create_session(self):
        index = self.ui.user_list.currentIndex()
        if index < 0 or index >= len(self.users):
            print("No user selected.")
            return
        user_id = self.users[index]["id"]
        session_name = self.start_session_controller.ui.session_nr_input.text()
        #selected_user_index = self.ui.user_list.currentIndex() + 1
        #if selected_user_index < 0 or selected_user_index >= len(self.users):
            #print("No user selected.")
            #return
        #self.session.add_session(selected_user_index, session_name)
        #index = self.ui.user_list.currentIndex()
        #if index < 0 or index >= len(self.users):
            #print("No user selected.")
            #return

        #user_id = self.users[index]["id"]
        if not session_name:
            print("Session name cannot be empty.")
            return
        self.session.add_session(user_id, session_name)
        self.sessions = self.session.get_sessions(user_id)
        self.update_session_list(index)

        self.main_window_controller.ui.session_label.setText(session_name)
        self.open_main_window()

    def open_delete_session_form(self):
        user_index = self.ui.user_list.currentIndex()
        session_index = self.ui.session_list.currentIndex()
        if user_index < 0 or user_index >= len(self.users):
            return
        
        session_id = self.sessions[session_index]["id"]
        self.delete_session_form_controller.session_id = session_id
        self.delete_session_form_controller.on_delete = lambda: self.update_session_list(user_index)
        self.delete_session_form_controller.show()
