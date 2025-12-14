import torch
import torchaudio
from transformers import pipeline
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)

model_id = '11mlabs/indri-0.1-124m-tts'
task = 'indri-tts'

# Initialize pipeline once (reuse for multiple generations)
pipe = pipeline(
    task,
    model=model_id,
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
    trust_remote_code=True,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32  # Use float16 for faster inference on GPU
)

# Set pad_token_id to avoid warnings
if hasattr(pipe.model.config, 'pad_token_id') and pipe.model.config.pad_token_id is None:
    pipe.model.config.pad_token_id = pipe.model.config.eos_token_id

# Generate with optimizations
with torch.inference_mode():  # Faster inference mode
    output = pipe(['Hello, how are you my friend'], speaker='[spkr_63]')

torchaudio.save('output.wav', output[0]['audio'][0], sample_rate=24000)













# import torch
# from TTS.api import TTS

# # Get device
# device = "cuda" if torch.cuda.is_available() else "cpu"

# # List available 🐸TTS models
# print(TTS().list_models())

# # Init TTS
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# # Run TTS
# # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# # Text to speech list of amplitude values as output
# wav = tts.tts(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en")
# # Text to speech to a file
# tts.tts_to_file(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")