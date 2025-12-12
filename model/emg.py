from .database import supabase
from PyQt6.QtCore import QRunnable, pyqtSlot

class EMG(QRunnable):
    TABLE = "emg_data"

    def get_emg_data(self, session_id: int):
        try:
            response = supabase.table(EMG.TABLE).select("*").eq("session_id", session_id).execute()
            return response.data 
        except Exception as e:
            print("Error fetching EMG data:", e)
            return []
    
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