import os
from supabase import create_client
from dotenv import load_dotenv
from PyQt6.QtCore import QRunnable, pyqtSlot

load_dotenv(".env")
SUPABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if SUPABASE_URL is None or SUPABASE_KEY is None:
    raise ValueError("Missing Supabase environment variables") 

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class SaveSamplesWorker(QRunnable):
    def __init__(self, payload):
        super().__init__()
        self.payload = payload

    @pyqtSlot()
    def run(self):
        try:
            print("Saving to supabase...")
            supabase.table("emg_data").insert(self.payload).execute()
            print("Saved successfully.")
        except Exception as e:
            print("Supabase save error:", e)