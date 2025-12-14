from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

def askGemini(command):
  # The client gets the API key from the environment variable `GEMINI_API_KEY`.
  client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

  prompt = (
    f"User query: {command}\n"
    "Instructions: You are Friday, an intelligent personal assistant. "
    "Respond in a confident, futuristic, and conversational tone suitable for spoken output. "
    "Keep responses concise and natural. Avoid '*' or any characters that sound odd when spoken aloud. "
    "If the user speaks in Hindi, reply in smooth Hinglish. "
    "Always provide helpful, clear, and actionable answers like a real-time assistant."
  )

  response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt,
  )
  return response.text