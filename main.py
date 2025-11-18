from supabase import create_client, Client
import os
from dotenv import load_dotenv
import sys
from PyQt6 import QtWidgets
from controllers.first_window_controller import First_window_controller

load_dotenv(".env")
print("SUPABASE_URL:", os.getenv("DATABASE_URL")) 
print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))
      
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = First_window_controller()
    w.show()
    sys.exit(app.exec())
    app.exec()

if __name__ == "__main__":
    main()
