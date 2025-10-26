import sys
import os
import pandas as pd
import json

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.analyzer import CareerAnalyzer

def run_demo():
    """Run a complete demo of the LLM capabilities"""
    print("🚀 Starting CareerLens LLM Demo...")
    
    # Initialize analyzer
    try:
        analyzer = CareerAnalyzer()
        print("✅ CareerAnalyzer initialized")
    except Exception as e:
        print(f"❌ Failed to initialize analyzer: {e}")
        return
    
    # Load sample data
    try:
        df = pd.read_csv("data/cleaned_resumes.csv")
        print(f"✅ Loaded {len(df)} resumes for analysis")
    except Exception as e:
        print(f"❌ No cleaned data found: {e}")
        return
    
    # Demo 1: Simple Analysis
    print("\n" + "="*50)
    print("📄 DEMO 1: SIMPLE RESUME ANALYSIS")
    print("="*50)
    
    test_skills = ["python", "sql"]
    test_resume = "Experienced professional with data analysis skills."
    
    print("Testing with simple resume...")
    analysis = analyzer.analyze_resume(test_resume, test_skills, "Data Analyst")
    
    print("✅ Resume Analysis Complete!")
    print(json.dumps(analysis, indent=2))

def test_real_resume():
    """Test with a real resume from the dataset"""
    print("\n" + "="*50)
    print("🔍 DEMO 2: REAL RESUME ANALYSIS")
    print("="*50)
    
    try:
        analyzer = CareerAnalyzer()
        df = pd.read_csv("data/cleaned_resumes.csv")
        
        # Get first resume
        sample = df.iloc[0]
        resume_text = sample['resume_text'][:1000]  # First 1000 chars
        skills = sample['extracted_skills']
        
        print(f"Analyzing real resume with {len(skills)} skills...")
        analysis = analyzer.analyze_resume(resume_text, skills, "Data Analyst")
        
        print(f"✅ Analysis complete!")
        print(f"Recommended role: {analysis['career_path']['immediate']['role']}")
        print(f"Skill gaps: {analysis['skill_gaps']['technical']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_demo()
    test_real_resume()