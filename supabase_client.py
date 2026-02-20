import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print("URL ->", repr(url))
print("KEY exists ->", key is not None)

supabase = create_client(url, key)