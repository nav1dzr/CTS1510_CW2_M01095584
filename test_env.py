from dotenv import load_dotenv
import os

load_dotenv()

print("API KEY:", os.getenv("GEMINI_API_KEY"))
