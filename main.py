from dotenv import load_dotenv
from supabase_handler import *
from dashboard_scraper import get_mp3_url
from transcriber import download_mp3, transcribe_audio
import os
from datetime import datetime

load_dotenv()

def process_calls():
    calls = get_pending_calls()
    print(f"Retrieved {len(calls)} pending calls.")
    
    for call in calls:
        try:
            call_id = call["call_id"]
            date = call["created_at"].split("T")[0]

            mp3_url = get_mp3_url(call["call_url"])
            print(f"[{call_id}] MP3 URL retrieved: {mp3_url}")

            local_path = f"recordings/{call_id}.mp3"
            download_mp3(mp3_url, local_path)
            print(f"[{call_id}] MP3 downloaded to {local_path}")

            bucket_path = f"call-recordings/{date}/{call_id}.mp3"
            public_url = upload_to_storage(local_path, bucket_path)
            print(f"[{call_id}] MP3 uploaded to bucket: {public_url}")

            update_call_status(call_id, {"status": "downloaded", "mp3_url": public_url})
            print(f"[{call_id}] Status updated to 'downloaded'")

            transcript = transcribe_audio(local_path)
            print(f"[{call_id}] Transcription completed:\n{transcript[:100]}...")  # print first 100 chars

            update_call_status(call_id, {"transcription": transcript, "status": "transcribed"})
            print(f"[{call_id}] Status updated to 'transcribed'")

            os.remove(local_path)
            print(f"[{call_id}] Local file removed.\n")

        except Exception as e:
            print(f"[{call['call_id']}] Error: {e}\n")

if __name__ == "__main__":
    process_calls()
