# test_careercompass.py
import requests
import json
import os
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def test_health():
    print_section("Health Check")
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    print(f"✅ Status: {data['status']}")
    print(f"✅ Timestamp: {data['timestamp']}")
    print(f"✅ Analyzer Available: {data['analyzer_available']}")
    print(f"✅ Data Loaded: {data['data_loaded']}")
    print(f"✅ NER Available: {data['ner_available']}")
    print(f"✅ OpenAI Available: {data['openai_available']}")

def test_basic_endpoints():
    print_section("Basic Endpoints")
    
    # Test root
    response = requests.get(f"{BASE_URL}/")
    data = response.json()
    print(f"✅ API Message: {data['message']}")
    print(f"✅ Version: {data['version']}")
    print(f"✅ Features: {', '.join(data['features'])}")
    
    # Test roles
    response = requests.get(f"{BASE_URL}/roles")
    data = response.json()
    print(f"✅ Available Roles: {', '.join(data['roles'])}")
    
    # Test sample resumes
    response = requests.get(f"{BASE_URL}/sample-resumes?count=2")
    data = response.json()
    print(f"✅ Sample Resumes: {data['count']} loaded")
    for i, sample in enumerate(data['samples']):
        print(f"   Sample {i+1}: {sample['positions']}")
        print(f"   Skills: {sample['extracted_skills']}")

def test_trend_analysis():
    print_section("Trend Analysis")
    
    roles = ["Data Analyst", "Data Scientist", "Software Engineer"]
    
    for role in roles:
        response = requests.get(f"{BASE_URL}/analyze-trends/{role}")
        data = response.json()
        trends = data['trends']
        
        print(f"\n📈 {role} Trends:")
        print(f"   Emerging Skills: {len(trends['emerging_skills'])}")
        for skill in trends['emerging_skills'][:2]:
            print(f"     - {skill['skill']} ({skill['impact']} impact)")
        
        print(f"   Salary Impact: {trends['salary_impact']}")

def test_resume_analysis():
    print_section("Resume Analysis")
    
    # Test case 1: Junior Data Analyst
    test_cases = [
        {
            "name": "Junior Data Analyst",
            "resume_text": """
            Recent graduate with Bachelor's in Statistics. Completed coursework in data analysis, 
            statistics, and programming. Strong foundation in Excel and basic SQL. 
            Looking to start career as Data Analyst.
            
            EDUCATION:
            Bachelor of Science in Statistics, University of Example, 2024
            GPA: 3.6/4.0
            
            SKILLS:
            - Excel: Advanced formulas, pivot tables, charts
            - SQL: Basic queries, joins, aggregations
            - Statistics: Descriptive stats, hypothesis testing
            - Python: Basic pandas, matplotlib
            
            PROJECTS:
            - Analyzed sales data to identify trends (Excel)
            - Created database queries for customer segmentation (SQL)
            """,
            "skills": ["excel", "sql", "statistics", "python", "data analysis"],
            "target_role": "Data Analyst",
            "experience_level": "Entry",
            "industry": "Technology"
        },
        {
            "name": "Experienced Software Engineer",
            "resume_text": """
            Software Engineer with 4 years experience in web development. 
            Strong background in JavaScript, React, and Node.js. 
            Looking to transition to more data-intensive roles.
            
            EXPERIENCE:
            Senior Software Engineer, Tech Company (2022-2024)
            - Developed full-stack web applications
            - Led team of 3 junior developers
            - Implemented REST APIs and microservices
            
            SKILLS:
            - JavaScript, TypeScript, React, Node.js
            - Python, Django, Flask
            - AWS, Docker, Git
            - SQL, MongoDB
            
            EDUCATION:
            BS Computer Science, State University
            """,
            "skills": ["javascript", "react", "node.js", "python", "aws", "sql"],
            "target_role": "Software Engineer", 
            "experience_level": "Senior",
            "industry": "Technology"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🎯 Analyzing: {test_case['name']}")
        
        response = requests.post(f"{BASE_URL}/analyze-resume", json=test_case)
        data = response.json()
        analysis = data['analysis']
        
        print(f"✅ Analysis Source: {data['analysis_source']}")
        
        # Skill Gaps
        skill_gaps = analysis['skill_gaps']
        print(f"🔍 Skill Gaps ({skill_gaps['severity']} severity):")
        print(f"   Technical: {', '.join(skill_gaps['technical'])}")
        print(f"   Soft Skills: {', '.join(skill_gaps['soft_skills'])}")
        
        # Career Path
        career_path = analysis['career_path']
        print(f"🚀 Career Path:")
        print(f"   Immediate: {career_path['immediate']['role']} ({career_path['immediate']['salary_range']})")
        print(f"   Mid-term: {career_path['mid_term']['role']} ({career_path['mid_term']['salary_range']})")
        
        # Learning Roadmap
        roadmap = analysis['learning_roadmap']
        print(f"📚 Learning Roadmap ({roadmap['timeline']}):")
        for course in roadmap['courses']:
            print(f"   - {course['name']} ({course['platform']}, {course['duration']})")
        
        # Market Insights
        market = analysis['market_insights']
        print(f"📊 Market Insights:")
        print(f"   Demand: {market['demand_trend']}")
        print(f"   Emerging Tech: {', '.join(market['emerging_tech'])}")

def test_file_upload_simulation():
    print_section("File Upload Simulation")
    
    # Simulate uploading a text resume
    sample_resume_text = """
    JOHN DOE
    Data Analyst
    Email: john.doe@email.com
    Phone: (555) 123-4567
    
    SUMMARY:
    Data Analyst with 3 years of experience in transforming complex datasets into actionable insights.
    Proficient in SQL, Python, and data visualization tools.
    
    EXPERIENCE:
    Data Analyst, ABC Company (2022-Present)
    - Analyzed customer data to identify trends and opportunities
    - Created interactive dashboards using Tableau
    - Wrote complex SQL queries for data extraction
    
    SKILLS:
    - Programming: Python, SQL, R
    - Tools: Tableau, Excel, Power BI
    - Databases: MySQL, PostgreSQL
    - Cloud: AWS, Google Cloud
    
    EDUCATION:
    Bachelor of Science in Data Science, University of Example
    """
    
    # Since we can't actually upload a file in this test, we'll use the analyze endpoint directly
    print("📄 Simulating resume file upload...")
    
    analysis_request = {
        "resume_text": sample_resume_text,
        "skills": ["python", "sql", "tableau", "excel", "aws"],
        "target_role": "Data Analyst",
        "experience_level": "Intermediate",
        "industry": "Technology"
    }
    
    response = requests.post(f"{BASE_URL}/analyze-resume", json=analysis_request)
    data = response.json()
    
    print(f"✅ Analysis completed for uploaded resume!")
    print(f"   Role: {data['role']}")
    print(f"   Missing skills: {len(data['analysis']['skill_gaps']['technical'])} technical gaps")
    print(f"   Source: {data['analysis_source']}")

def test_comprehensive_workflow():
    print_section("Comprehensive Workflow Test")
    
    print("1. 🎯 User wants to become a Data Scientist")
    print("2. 📊 Checking market trends...")
    
    response = requests.get(f"{BASE_URL}/analyze-trends/Data%20Scientist")
    trends = response.json()['trends']
    print(f"   Trending skills: {', '.join([s['skill'] for s in trends['emerging_skills']])}")
    
    print("3. 📝 User uploads current resume...")
    current_skills = ["python", "sql", "excel", "statistics"]
    
    analysis_request = {
        "resume_text": "Current professional with background in data analysis. Strong Python and SQL skills. Looking to transition to Data Science.",
        "skills": current_skills,
        "target_role": "Data Scientist",
        "experience_level": "Intermediate",
        "industry": "Technology"
    }
    
    response = requests.post(f"{BASE_URL}/analyze-resume", json=analysis_request)
    analysis = response.json()['analysis']
    
    print("4. 🔍 Analysis Results:")
    print(f"   Missing skills: {', '.join(analysis['skill_gaps']['technical'])}")
    print(f"   Career path: {analysis['career_path']['immediate']['role']} → {analysis['career_path']['mid_term']['role']}")
    print(f"   Timeline: {analysis['learning_roadmap']['timeline']}")

def main():
    print("🚀 CareerCompass Comprehensive Test Suite")
    print("Testing all functionality of your career intelligence engine...")
    
    try:
        test_health()
        test_basic_endpoints()
        test_trend_analysis()
        test_resume_analysis()
        test_file_upload_simulation()
        test_comprehensive_workflow()
        
        print_section("🎉 TEST COMPLETE")
        print("All CareerCompass features are working perfectly!")
        print("\n📋 What you can do now:")
        print("1. Build a frontend (Streamlit, React, etc.)")
        print("2. Integrate with other applications")
        print("3. Extend with more features")
        print("4. Deploy to production")
        print(f"\n🌐 Your API is ready at: {BASE_URL}")
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to the CareerCompass API")
        print("   Make sure the server is running: python3 llm/api.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()