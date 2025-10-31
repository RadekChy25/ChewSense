from supabase import create_client, Client
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt
import sys

load_dotenv(".env")
print("SUPABASE_URL:", os.getenv("DATABASE_URL")) 
print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))
      
def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    label = QLabel("Hello, PyQt6!", parent=window)

    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.setCentralWidget(label)
    window.setWindowTitle("Simple PyQt6 App")
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
