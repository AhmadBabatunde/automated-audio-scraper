import openai
import requests
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def download_mp3(mp3_url, save_path):
    response = requests.get(mp3_url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return response.text
