import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
MACHINE_ID = int(os.getenv("MACHINE_ID", 1))

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_url(snowflake_id: int, short_code: str, long_url: str):
    data = {
        "id": snowflake_id,
        "short_code": short_code,
        "long_url": long_url
    }
    return supabase.table("urls").insert(data).execute()

def get_long_url(short_code: str):
    # Fetch from DB (In Phase 3, we will add Redis here)
    response = supabase.table("urls").select("long_url").eq("short_code", short_code).single().execute()
    return response.data["long_url"] if response.data else None