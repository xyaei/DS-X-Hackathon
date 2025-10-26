import sys
import os
import pandas as pd
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.analyzer import CareerAnalyzer

def simple_test():
    print("🧪 Simple LLM Test...")
    
    # Initialize analyzer
    analyzer = CareerAnalyzer()
    
    # Test with minimal data
    test_skills = ["python", "sql"]
    test_resume = "Experienced professional looking to transition into tech."
    
    print("Testing LLM analysis...")
    analysis = analyzer.analyze_resume(test_resume, test_skills, "Data Analyst")
    
    print("✅ LLM Test Complete!")
    print(f"Skill Gaps: {analysis['skill_gaps']['technical']}")
    print(f"Next Role: {analysis['career_path']['immediate']['role']}")

if __name__ == "__main__":
    simple_test()