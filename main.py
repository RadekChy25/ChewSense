from supabase import create_client, Client
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt
import sys
from PyQt6 import QtWidgets
from widgets.main_window import Ui_MainWindow

load_dotenv(".env")
print("SUPABASE_URL:", os.getenv("DATABASE_URL")) 
print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))
      
def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

    app.exec()

if __name__ == "__main__":
    main()
