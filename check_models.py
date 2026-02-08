import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("🔍 Searching for your 'Text' models...")
found = False
for m in genai.list_models():
    # We are looking for the standard text generation method
    if 'generateContent' in m.supported_generation_methods:
        print(f"✅ FOUND: {m.name}")
        found = True

if not found:
    print("❌ No standard text models found. Your API key might be restricted to 'Audio-Only' experiments.")