import sys
import os
from supabase import create_client
from dotenv import load_dotenv
from PyQt6 import QtWidgets
from controllers.first_window_controller import First_window_controller

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = First_window_controller()
    w.show()
    sys.exit(app.exec())
    app.exec()

if __name__ == "__main__":
    main()