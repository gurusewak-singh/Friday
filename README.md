# Friday - Voice-Activated AI Assistant 🎤

Friday is a powerful voice-activated AI assistant built with Python. It uses OpenAI Whisper for accurate speech recognition, Google Gemini AI for intelligent responses, and supports multi-command chaining for seamless interaction.

---

## ✨ Features

- **Advanced Voice Recognition** – Uses OpenAI Whisper for accurate, multilingual speech-to-text
- **AI-Powered Responses** – Answers questions using Google Gemini AI
- **App Control** – Open, close, switch, minimize, and maximize applications
- **Browser Control** – Open websites, search, manage tabs
- **Music Playback** – Play songs from YouTube via voice commands
- **Multi-Command Support** – Chain commands like "open chrome and search Python tutorials"
- **Wake Word Activation** – Only responds to commands prefixed with "friday"
- **Sleep/Wake Modes** – Say "turn off" to sleep or "turn on" to wake

---

## 📋 Prerequisites

Before starting, make sure you have:

- **Python 3.10+** installed
- **Microphone** connected and working
- **FFmpeg** installed (required for Whisper audio processing)
- **GPU (Optional)** – For faster Whisper transcription (CUDA supported)

### Installing FFmpeg

**Windows:**
```sh
# Using Chocolatey
choco install ffmpeg

# Or using Winget
winget install ffmpeg
```

**macOS:**
```sh
brew install ffmpeg
```

**Linux:**
```sh
sudo apt update && sudo apt install ffmpeg
```

---

## 🧠 Whisper Model Selection

The project uses OpenAI Whisper for speech recognition. Choose a model based on your hardware:

| Size   | Parameters | English-only | Multilingual | Required VRAM | Relative Speed |
|--------|------------|--------------|--------------|---------------|----------------|
| tiny   | 39 M       | `tiny.en`    | `tiny`       | ~1 GB         | ~10x           |
| base   | 74 M       | `base.en`    | `base`       | ~1 GB         | ~7x            |
| small  | 244 M      | `small.en`   | `small`      | ~2 GB         | ~4x            |
| medium | 769 M      | `medium.en`  | `medium`     | ~5 GB         | ~2x            |
| large  | 1550 M     | N/A          | `large`      | ~10 GB        | 1x             |
| turbo  | 809 M      | N/A          | `turbo`      | ~6 GB         | ~8x            |

### How to Change Whisper Model

Open `main.py` and find line 21:

```python
model = whisper.load_model("turbo")  # Change this to your preferred model
```

**GPU Examples:**
```python
model = whisper.load_model("turbo")   # Best balance of speed and accuracy (needs ~6GB VRAM)
model = whisper.load_model("medium")  # Good accuracy (needs ~5GB VRAM)
model = whisper.load_model("small")   # Lighter option (needs ~2GB VRAM)
```

**CPU / No GPU:**
```python
model = whisper.load_model("base")    # Recommended for CPU (needs ~1GB RAM)
model = whisper.load_model("tiny")    # Fastest, least accurate (needs ~1GB RAM)
```

> [!TIP]
> If you have limited hardware, use `base` or `tiny` models. They work on CPU without a dedicated GPU.

---

## 🚫 No GPU? Use Default Speech Recognition

If you don't have a GPU and find Whisper too slow, you can use Google's free speech recognition instead.

### How to Switch to Google Speech Recognition

In `main.py`, make these changes:

1. **Comment out Whisper import and model loading (lines 5 and 21):**
```python
# import whisper
# model = whisper.load_model("turbo")
```

2. **In the `friday()` function, replace Whisper transcription with Google:**

Find these lines (around lines 304-306):
```python
with open("temp_audio_input.wav", "wb") as f:
    f.write(audio.get_wav_data())
command = model.transcribe("temp_audio_input.wav")["text"].lower()
```

Replace with:
```python
command = recognizer.recognize_google(audio).lower()
```

Do the same for the second occurrence (around lines 347-349).

> [!NOTE]
> Google Speech Recognition requires an internet connection but works without a GPU.

---

## 🔧 Installation

### 1. Clone the Repository

```sh
git clone https://github.com/gurusewak-singh/Friday.git
cd Friday
```

### 2. Create and Activate Virtual Environment

```sh
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```sh
pip install SpeechRecognition PyAudio gTTS pygame python-dotenv google-genai openai-whisper google-search-results pyautogui pygetwindow
```

**Or if you have a requirements file:**
```sh
pip install -r requirements.txt
```

> [!IMPORTANT]
> **PyAudio Installation Issues on Windows:**  
> If `pip install PyAudio` fails, download the appropriate `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install with:
> ```sh
> pip install PyAudio‑0.2.11‑cp312‑cp312‑win_amd64.whl
> ```

---

## 🔑 Environment Variables Setup

Create a `.env` file in the project root with your API keys:

```env
GEMINI_API_KEY="your-gemini-api-key-here"
SERP_API_KEY="your-serp-api-key-here"
```

### Getting API Keys

| API Key | Where to Get | Purpose |
|---------|--------------|---------|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) | AI-powered responses |
| `SERP_API_KEY` | [SerpAPI](https://serpapi.com/) | Web search & YouTube link fetching |

> [!CAUTION]
> Never commit your `.env` file to version control. Make sure `.env` is in your `.gitignore` file.

---

## 🚀 Running the Assistant

```sh
python main.py
```

You'll hear an initialization sound. The assistant is now listening!

---

## 🗣️ Voice Commands

### Wake Word
Always prefix commands with **"friday"** or say "friday" first and wait for response.

### Application Control

| Command | Action |
|---------|--------|
| `friday open chrome` | Opens Google Chrome |
| `friday open notepad` | Opens Notepad |
| `friday close spotify` | Closes Spotify |
| `friday switch to vscode` | Switches to VS Code window |
| `friday minimize chrome` | Minimizes Chrome window |
| `friday maximize discord` | Maximizes Discord window |

### Browser Control

| Command | Action |
|---------|--------|
| `friday open youtube` | Opens YouTube in browser |
| `friday open github` | Opens GitHub in browser |
| `friday search python tutorials` | Searches in current browser tab |
| `friday search cats in new tab` | Opens new tab and searches |
| `friday close tab` | Closes current browser tab |
| `friday next tab` | Switches to next tab |
| `friday new tab` | Opens a new tab |

### Music Playback

| Command | Action |
|---------|--------|
| `friday play shape of you` | Plays song on YouTube |
| `friday play tum ho from rockstar` | Plays specific song |

### Typing

| Command | Action |
|---------|--------|
| `friday type hello world` | Types "hello world" in active window |

### Multi-Command Chaining

| Command | Action |
|---------|--------|
| `friday open chrome and search weather` | Opens Chrome, then searches |
| `friday open spotify and then open discord` | Opens both apps sequentially |

### System Commands

| Command | Action |
|---------|--------|
| `friday turn off` or `friday sleep` | Puts assistant to sleep (stops listening) |
| `friday turn on` or `friday wake up` | Wakes assistant from sleep |
| `friday shut down` | Completely exits the assistant |

### Ask Questions

| Command | Action |
|---------|--------|
| `friday what is the weather today` | AI answers using Gemini |
| `friday tell me a joke` | AI responds with a joke |
| `friday explain quantum computing` | AI provides explanation |

---

## 📁 Project Structure

```
Friday/
├── main.py              # Main entry point
├── gemini_client.py     # Google Gemini AI integration
├── get_link.py          # Web/song link fetching via SerpAPI
├── app_control.py       # System app open/close/switch functions
├── browser_control.py   # Browser tab management
├── musicLib.py          # Local music library
├── song_links.py        # Song link caching
├── web_links.py         # Web link caching
├── song_links.json      # Cached song links
├── web_links.json       # Cached web links
├── mfu_mp3/             # Pre-recorded audio responses
├── .env                 # API keys (create this!)
└── .gitignore           # Git ignore rules
```

---

## 🎵 Customizing Music Library

Edit `musicLib.py` to add your favorite songs:

```python
music = {
    "song name": "https://youtube.com/watch?v=...",
    "another song": "https://youtube.com/watch?v=...",
}
```

---

## 🐛 Troubleshooting

### "No module named 'whisper'"
```sh
pip install openai-whisper
```

### PyAudio Installation Error
See the [PyAudio section](#3-install-dependencies) above for Windows-specific instructions.

### Microphone Not Working
- Check microphone permissions in system settings
- Ensure no other application is using the microphone
- Test with: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

### Whisper Too Slow
- Use a smaller model (`base` or `tiny`)
- Or switch to Google Speech Recognition (see [No GPU section](#-no-gpu-use-default-speech-recognition))

### CUDA/GPU Not Detected
- Install PyTorch with CUDA: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`
- Verify: `python -c "import torch; print(torch.cuda.is_available())"`

---

## 📄 License

MIT License

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
