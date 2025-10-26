# test_api_working.py
import requests
import json
import time

def test_api_with_gemini():
    print("🚀 Testing CareerCompass API with Gemini AI...")
    
    # First check if API is running
    try:
        health = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ API Health: {health.json()['status']}")
    except:
        print("❌ API is not running! Start it with: python3 llm/api.py")
        return
    
    test_data = {
        "resume_text": "Data analyst with 2 years experience in Excel and SQL. Strong analytical skills and business communication. Completed several data analysis projects.",
        "skills": ["excel", "sql", "data analysis", "communication"],
        "target_role": "Data Analyst",
        "experience_level": "Intermediate",
        "industry": "Technology"
    }
    
    try:
        print("📤 Sending analysis request to API...")
        start_time = time.time()
        
        response = requests.post("http://localhost:8000/analyze-resume", json=test_data, timeout=60)
        result = response.json()
        
        end_time = time.time()
        print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
        
        print(f"✅ Analysis Source: {result['analysis_source']}")
        print(f"🔍 Skill Gaps: {', '.join(result['analysis']['skill_gaps']['technical'][:3])}")
        print(f"🚀 Career Path: {result['analysis']['career_path']['immediate']['role']}")
        
        if result['analysis_source'] == 'gemini':
            print("🎉 SUCCESS: Your CareerCompass is now AI-powered with Gemini!")
        else:
            print("ℹ️ Using fallback analysis")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api_with_gemini()