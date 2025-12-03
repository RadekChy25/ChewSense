from .database import supabase

class User:
    TABLE = "users"
    def create_user(self, first_name: str, last_name: str):
        try:
            response = supabase.table(User.TABLE).insert({
                "first_name": first_name,
                "last_name": last_name
            }).execute()
            return response.data
        except Exception as e:
            print("Error creating user:", e)
            return None 
        
    def get_user(self):
        try:
            response = supabase.table(User.TABLE).select("*").execute()
            if response.data is None:
                return []
            return response.data
            #return [response["first_name"] +" "+ response["last_name"] for response in response.data]
        except Exception as e:
            print("Error fetching users:", e)
            return None
        
    def add_user(self, first_name: str, last_name: str):
        try:
            supabase.table(User.TABLE).insert({
                "first_name": first_name,
                "last_name": last_name
            }).execute()
        except Exception as e:
            print("Error adding user:", e)
            return None