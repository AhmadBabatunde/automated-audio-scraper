# Audio Call Processing System

This Python-based system automates the processing of audio calls by downloading, transcribing, and storing them in a structured manner. It integrates with a dashboard to fetch call information, processes the audio files, and stores both the recordings and transcriptions in a Supabase backend.

## Features

- 🎵 Automatic MP3 download from call URLs
- 📝 Audio transcription using OpenAI's services
- 🗄️ Secure storage of audio files in Supabase storage
- 📊 Call status tracking and management
- 🔄 Automated workflow from download to transcription

## Prerequisites

- Python 3.x
- Supabase account
- OpenAI API access
- Playwright for web scraping

## Installation

1. Change directory:
```bash
cd audio-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install
```

4. Set up your environment variables in a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Project Structure

- `main.py` - Main execution script that orchestrates the entire process
- `dashboard_scraper.py` - Handles web scraping to retrieve MP3 URLs
- `transcriber.py` - Manages audio file downloading and transcription
- `supabase_handler.py` - Handles all Supabase interactions
- `recordings/` - Temporary storage for downloaded MP3 files

## Usage

Run the main script to process pending calls:

```bash
python main.py
```

The script will:
1. Fetch pending calls from the database
2. Download MP3 files for each call
3. Upload the files to Supabase storage
4. Generate transcriptions
5. Update call status and store transcriptions
6. Clean up temporary files

link to video sample --> https://www.awesomescreenshot.com/video/40561925?key=e7b2448da8c651a19e8498c1da95cc9e

## Error Handling

The system includes comprehensive error handling and logging for each step of the process. Failed operations are logged and won't prevent the processing of subsequent calls.


## License

Ahmadtijani1639@gmail.com
