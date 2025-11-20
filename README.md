# Friday: Voice-Activated AI Assistant

Friday is a voice-activated AI assistant built with Python. It can recognize your speech, open popular websites, play music from a predefined library, and answer questions using Google Gemini AI. The assistant responds with speech using Google Text-to-Speech and can be easily extended for more features.

## Features

- **Voice Recognition:** Uses your microphone to listen for commands.
- **Speech Synthesis:** Replies using natural-sounding speech.
- **Open Websites:** Instantly open Google, YouTube, LinkedIn, or GitHub with a voice command.
- **Play Music:** Play songs from a customizable music library (YouTube links).
- **AI Q&A:** Ask questions and get answers from Google Gemini AI.
- **Wake Word:** Only responds to commands prefixed with "friday".
- **Graceful Exit:** Say "turn off" to stop the assistant.

## Project Structure

```
Friday/
│
├── main.py             # Main entry point for the assistant
├── gemini_client.py    # Handles communication with Google Gemini AI
├── musicLib.py         # Music library (YouTube links)
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (API keys)
├── .venv/              # Python virtual environment
├── __pycache__/        # Python cache files
└── .gitignore          # Git ignore file
```

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/gurusewak-singh/Friday.git
cd Friday
```

### 2. Create and Activate a Virtual Environment

```sh
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```sh
pip install -r temp_requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with your Gemini API key:

```
GEMINI_API_KEY="your-gemini-api-key"
```

### 5. Run the Assistant

```sh
python main.py
```

## Usage

- Say "friday" to wake the assistant.
- Say "open google", "open youtube", "open linkedin", or "open github" to open those sites.
- Say "play [song name]" to play a song from the music library.
- Ask any question after "friday" to get an AI-powered answer.
- Say "turn off" to exit the assistant.

## Customizing the Music Library

Edit `musicLib.py` to add or change songs:

```python
music = {
  "song name": "https://youtube-link",
  ...
}
```

## Dependencies

- `SpeechRecognition`
- `PyAudio`
- `gTTS`
- `pygame`
- `python-dotenv`
- `google-genai` (for Gemini API)

## Notes

- Make sure your microphone is set up and accessible.
- The Gemini API key is required for AI responses.
- The assistant only responds to commands prefixed with "friday" for safety.

## License

MIT License

