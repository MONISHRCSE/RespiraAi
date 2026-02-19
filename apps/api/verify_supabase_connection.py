
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import sys

# Try loading from current directory
load_dotenv(override=True)

print("--- Environment Check ---")
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

print(f"Supabase URL found: {'Yes' if url else 'No'}")
print(f"Supabase KEY found: {'Yes' if key else 'No'}")

if not url or not key:
    # Try loading from services/.env
    print("Trying services/.env...")
    load_dotenv("services/.env", override=True)
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    print(f"Supabase URL found (services/.env): {'Yes' if url else 'No'}")
    print(f"Supabase KEY found (services/.env): {'Yes' if key else 'No'}")

if not url or not key:
    print("CRITICAL: Supabase credentials missing!")
    sys.exit(1)

print("\n--- Connection Check ---")
try:
    supabase: Client = create_client(url, key)
    print("Supabase client created.")
    
    # Try a simple select to check table existence and permissions
    print("Attempting to select from 'predictions' table...")
    response = supabase.table("predictions").select("*").limit(1).execute()
    print("Select successful!")
    print(f"Data found: {len(response.data)} records")
    
except Exception as e:
    print(f"ERROR: {e}")
