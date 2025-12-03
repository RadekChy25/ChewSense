from .database import supabase

class Session:
    TABLE = "sessions"

    def get_sessions(self, user_id: int):
        try:
            response = supabase.table(Session.TABLE).select("*").eq("user_id", user_id).execute()
            return response.data 
        except Exception as e:
            print("Error fetching sessions:", e)
            return []
    
    def add_session(self, user_id: int, session_name: str):
        try:
            supabase.table(Session.TABLE).insert({
                "user_id": user_id,
                "name": session_name
            }).execute()
        except Exception as e:
            print("Error adding session:", e)
            return None
        
    def get_session_id(self, user_id: int, session_name: str):
        try:
            response = supabase.table(Session.TABLE).select("*").eq("user_id", user_id).execute()
            print("Fetched session ID:", response)
            if response.data:
                return response.data
            return None
        except Exception as e:
            print("Error fetching session ID:", e)
            return None