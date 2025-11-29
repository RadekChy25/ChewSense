import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(".env")
SUPABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if SUPABASE_URL is None or SUPABASE_KEY is None:
    raise ValueError("Missing Supabase environment variables") 

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)