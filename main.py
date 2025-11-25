import sys
import os
from supabase import create_client
from dotenv import load_dotenv
from PyQt6 import QtWidgets
from controllers.first_window_controller import First_window_controller


load_dotenv(".env")
SUPABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL is None or SUPABASE_KEY is None:
    raise ValueError("Missing Supabase environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = First_window_controller()
    w.show()
    sys.exit(app.exec())
    app.exec()

if __name__ == "__main__":
    main()