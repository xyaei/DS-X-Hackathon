# test_best_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def test_best_models():
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    
    # Best models from your discovery
    best_models = [
        'models/gemini-2.5-flash',  # Stable Flash - should work!
        'models/gemini-2.5-flash-lite',  # Stable Lite
        'models/gemini-2.5-pro',  # Stable Pro
        'models/gemini-2.0-flash-001',  # Stable Flash 2.0
    ]
    
    for model_name in best_models:
        try:
            print(f"🤖 Testing: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello World' in JSON format: {'message': 'Hello World'}")
            print(f"✅ SUCCESS with: {model_name}")
            print(f"   Response: {response.text}")
            return model_name
        except Exception as e:
            print(f"❌ Failed: {model_name}")
            print(f"   Error: {str(e)[:100]}...")
    
    return None

working_model = test_best_models()
if working_model:
    print(f"🎉 Use this model in your enhanced analyzer: '{working_model}'")
else:
    print("❌ No working models found")