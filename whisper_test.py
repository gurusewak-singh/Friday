import whisper

model = whisper.load_model("small")
result = model.transcribe("audio.m4a")
print(result["text"])