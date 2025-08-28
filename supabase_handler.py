from supabase import create_client
from dotenv import load_dotenv
import os
import requests
import mimetypes

load_dotenv()

# Load credentials
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE")
bucket = os.getenv("SUPABASE_STORAGE_BUCKET", "call-recordings")

print(f"Connecting to Supabase URL: {url}")
supabase = create_client(url, key)

def get_pending_calls():
    response = (
        supabase
        .table("calls")
        .select("*")
        .or_("status.eq.pending,status.is.null")
        .execute()
    )
    return response.data

def update_call_status(call_id, data: dict):
    response = (
        supabase
        .table("calls")
        .update(data)
        .eq("call_id", call_id)
        .execute()
    )
    return response

def upload_to_storage(local_path: str, bucket_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(local_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    with open(local_path, "rb") as f:
        file_bytes = f.read()

    upload_url = f"{url}/storage/v1/object/{bucket}/{bucket_path}"

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": mime_type,
        "x-upsert": "true"
    }

    response = requests.put(upload_url, headers=headers, data=file_bytes)

    if response.status_code in [200, 201]:
        public_url = f"{url}/storage/v1/object/public/{bucket}/{bucket_path}"
        return public_url
    else:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")


