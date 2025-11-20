from google import genai
from dotenv import load_dotenv

load_dotenv()

def askGemini(command):
  # The client gets the API key from the environment variable `GEMINI_API_KEY`.
  client = genai.Client()

  response = client.models.generate_content(
      model="gemini-2.0-flash", contents=command + "Your response should be short and it should not contain '*' or any special symbol that don't sound good if machine speaks. If the question is asked in the hindi, response in hinglish only.", 
  )
  return response.text