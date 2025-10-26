#!/usr/bin/env python3
"""
CareerLens LLM System - Complete Runner
"""

import subprocess
import sys
import time
import webbrowser
import requests
import json

def setup_environment():
    """Setup and test the complete LLM system"""
    print("🔧 Setting up CareerLens LLM System...")
    
    # Check dependencies
    try:
        import openai, pandas, fastapi
        print("✅ All dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    
    # Check API key
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in .env file")
        return False
    
    print("✅ Environment setup complete")
    return True

def test_llm_analysis():
    """Test the LLM analysis functionality"""
    print("\n🧪 Testing LLM Analysis...")
    
    from llm.analyzer import CareerAnalyzer
    from extra.demo import run_demo
    
    try:
        analyzer = CareerAnalyzer()
        
        # Quick test
        test_result = analyzer.analyze_resume(
            "Experienced professional with Python and SQL skills seeking data roles.",
            ["python", "sql", "excel"],
            "Data Analyst"
        )
        
        print("✅ LLM Analysis Test Passed")
        print(f"   - Skill Gaps: {len(test_result['skill_gaps']['technical'])} technical skills")
        print(f"   - Career Path: {test_result['career_path']['immediate']['role']}")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM Analysis Test Failed: {e}")
        return False

def run_complete_system():
    """Run the complete LLM system with API"""
    print("\n🚀 Starting Complete LLM System...")
    
    # Start API server
    print("🌐 Starting LLM API Server...")
    api_process = subprocess.Popen([
        sys.executable, "llm/api.py"
    ])
    
    # Wait for server to start
    time.sleep(5)
    
    # Test API endpoints
    print("\n📡 Testing API Endpoints...")
    
    try:
        # Test sample endpoint
        response = requests.get("http://localhost:8000/sample-resumes?count=2")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Sample Endpoint: {data['count']} samples")
        else:
            print("❌ API Sample Endpoint Failed")
        
        # Test analysis endpoint
        test_payload = {
            "resume_text": "Software engineer with 3 years experience in web development.",
            "skills": ["javascript", "react", "node.js"],
            "target_role": "Software Engineer"
        }
        
        response = requests.post("http://localhost:8000/analyze-resume", json=test_payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Analysis Endpoint: {data['analysis']['skill_gaps']['severity']} severity")
        else:
            print("❌ API Analysis Endpoint Failed")
            
    except Exception as e:
        print(f"❌ API Testing Failed: {e}")
    
    print("\n🎉 CareerLens LLM System is Running!")
    print("   API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the system...")
    
    try:
        api_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down LLM System...")
        api_process.terminate()
        print("✅ System stopped")

if __name__ == "__main__":
    if setup_environment():
        if test_llm_analysis():
            run_complete_system()
        else:
            print("❌ LLM testing failed. Please check your API key and dependencies.")
    else:
        print("❌ Setup failed. Please check the errors above.")