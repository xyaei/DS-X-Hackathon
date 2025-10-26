import pandas as pd
import json
import sys
import os
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.enhanced_analyzer import EnhancedCareerAnalyzer

def showcase_enhanced_system():
    print("🎯 CareerCompass Enhanced - AI Career Intelligence Platform")
    print("=" * 70)
    
    analyzer = EnhancedCareerAnalyzer()
    
    # Load resume data
    try:
        df = pd.read_csv("data/cleaned_resumes.csv")
        print(f"📊 System loaded: {len(df)} professional resumes")
        print("🤖 Enhanced AI Analysis: Real-time trends • Skill evolution • Market insights")
        print("💼 Powered by live market data and historical trends")
        print()
    except Exception as e:
        print(f"❌ Data loading issue: {e}")
        return
    
    # Enhanced test cases with different industries and experience levels
    test_cases = [
        {
            "skills": ["python", "excel", "sql"], 
            "role": "Data Analyst", 
            "name": "Tech Career Changer",
            "experience": "1-2 years",
            "industry": "Technology",
            "analysis_type": "detailed"
        },
        {
            "skills": ["java", "spring", "sql", "git", "docker"],
            "role": "Software Engineer", 
            "name": "Finance Sector Developer",
            "experience": "3-4 years", 
            "industry": "Finance",
            "analysis_type": "detailed"
        },
        {
            "skills": ["tableau", "sql", "statistics", "excel"],
            "role": "Data Scientist",
            "name": "Healthcare Analyst", 
            "experience": "2-3 years",
            "industry": "Healthcare",
            "analysis_type": "detailed"
        }
    ]
    
    print("🚀 DEMONSTRATING ENHANCED AI CAREER ANALYSIS")
    print("=" * 70)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'#' * 60}")
        print(f"👤 CASE {i}: {case['name']}")
        print(f"   🎯 Target Role: {case['role']}")
        print(f"   🏢 Industry: {case['industry']}")
        print(f"   💼 Experience: {case['experience']}")
        print(f"   🛠️  Current Skills: {', '.join(case['skills'])}")
        print(f"{'#' * 60}")
        
        analysis = analyzer.analyze_resume(
            f"Professional in {case['industry']} with {case['experience']} experience",
            case["skills"],
            case["role"],
            case["experience"],
            case["industry"],
            case["analysis_type"]
        )
        
        # Display enhanced results
        print(f"\n📈 ENHANCED CAREER ANALYSIS:")
        print(f"   🎯 Immediate Role: {analysis['career_path']['immediate']['role']}")
        print(f"   💰 Salary Range: {analysis['career_path']['immediate']['salary_range']}")
        
        print(f"\n🔍 SKILL GAPS ANALYSIS:")
        print(f"   🔧 Technical: {', '.join(analysis['skill_gaps']['technical'])}")
        print(f"   💬 Soft Skills: {', '.join(analysis['skill_gaps']['soft_skills'])}")
        print(f"   ⚠️  Severity: {analysis['skill_gaps']['severity']}")
        
        print(f"\n📚 PERSONALIZED LEARNING ROADMAP:")
        for j, course in enumerate(analysis['learning_roadmap']['courses'][:3], 1):
            print(f"   {j}. {course['name']}")
            print(f"      📍 {course['platform']} | ⏱️  {course['duration']}")
        
        print(f"\n🌐 REAL-TIME MARKET INSIGHTS:")
        if 'real_time_insights' in analysis:
            trends = analysis['real_time_insights']
            print(f"   📊 Demand Level: {trends.get('demand_level', 'High')}")
            print(f"   💵 Average Salary: {trends.get('average_salary', 'N/A')}")
            print(f"   📈 Growth Prediction: {trends.get('growth_prediction', 'N/A')}")
            print(f"   🚀 Trending Skills: {', '.join(trends.get('trending_skills', []))}")
        
        print(f"\n🕒 Analysis Timestamp: {analysis.get('analysis_timestamp', 'N/A')}")

def demonstrate_skill_evolution():
    print(f"\n\n{'='*70}")
    print("📈 SKILL EVOLUTION & TREND ANALYSIS")
    print("=" * 70)
    
    analyzer = EnhancedCareerAnalyzer()
    
    roles_to_analyze = ["Data Scientist", "Software Engineer", "Data Analyst"]
    
    for role in roles_to_analyze:
        print(f"\n🔍 Analyzing skill evolution for: {role}")
        print("-" * 50)
        
        try:
            trends = analyzer.analyze_skill_evolution(role, years_back=5)
            
            print(f"📊 Historical Trends (5 years):")
            if 'visualization_data' in trends:
                viz_data = trends['visualization_data']
                skill_timeline = viz_data.get('skill_timeline', {})
                
                # Show key skills evolution
                current_year = datetime.now().year
                years = list(range(current_year - 5, current_year + 1))
                
                print(f"   Key skills evolution {current_year-5}-{current_year}:")
                for skill in ["Python", "Machine Learning", "Cloud Computing"]:
                    if skill.lower() in str(skill_timeline).lower():
                        values = []
                        for year in years:
                            year_data = skill_timeline.get(year, {})
                            # Find matching skill (case insensitive)
                            matching_skill = next((s for s in year_data.keys() if skill.lower() in s.lower()), None)
                            if matching_skill:
                                values.append(f"{year_data[matching_skill]}%")
                            else:
                                values.append("N/A")
                        print(f"   • {skill}: {' → '.join(values)}")
            
            print(f"\n🚀 Emerging Skills:")
            emerging = trends.get('emerging_skills', [])
            for skill in emerging[:3]:
                print(f"   • {skill.get('skill', 'N/A')}: {skill.get('growth', 'Rapid growth')}")
                
            print(f"\n📉 Declining Skills:")
            declining = trends.get('declining_skills', [])
            for skill in declining[:2]:
                print(f"   • {skill.get('skill', 'N/A')}: {skill.get('reason', 'Being replaced')}")
                
        except Exception as e:
            print(f"   ❌ Trend analysis failed: {e}")

def demonstrate_real_time_comparison():
    print(f"\n\n{'='*70}")
    print("🔄 REAL-TIME RESUME COMPARISON")
    print("=" * 70)
    
    analyzer = EnhancedCareerAnalyzer()
    
    # Compare different career paths
    comparisons = [
        {
            "name": "Data Analyst Path",
            "skills": ["excel", "sql", "tableau"],
            "role": "Data Analyst",
            "industry": "Technology"
        },
        {
            "name": "Data Scientist Path", 
            "skills": ["python", "machine learning", "sql", "statistics"],
            "role": "Data Scientist",
            "industry": "Technology"
        }
    ]
    
    print("🔍 Comparing Career Paths:")
    
    for comp in comparisons:
        print(f"\n📊 {comp['name']}:")
        analysis = analyzer.analyze_resume(
            f"Professional seeking {comp['role']} role",
            comp["skills"],
            comp["role"],
            "Intermediate",
            comp["industry"]
        )
        
        print(f"   🎯 Target: {comp['role']}")
        print(f"   🛠️  Skills: {', '.join(comp['skills'])}")
        print(f"   🔍 Key Gaps: {', '.join(analysis['skill_gaps']['technical'][:2])}")
        
        if 'real_time_insights' in analysis:
            trends = analysis['real_time_insights']
            print(f"   📈 Demand: {trends.get('demand_level', 'N/A')}")
            print(f"   💰 Salary: {trends.get('average_salary', 'N/A')}")

def show_advanced_capabilities():
    print(f"\n\n{'='*70}")
    print("🚀 ADVANCED CAPABILITIES")
    print("=" * 70)
    
    capabilities = [
        "🎯 Dynamic Prompting: Tailors analysis based on industry, experience, role",
        "📊 Real-time Market Data: Live trends from multiple sources", 
        "📈 Skill Evolution: Historical trends and future predictions",
        "🔄 Multi-Resume Comparison: Side-by-side career path analysis",
        "🏢 Industry-Specific Insights: Tailored for tech, finance, healthcare, etc.",
        "⏱️ Timely Analysis: Always current with market conditions",
        "📱 Visualization Ready: Data prepared for charts and graphs",
        "🔮 Predictive Insights: 1-3 year skill demand forecasts"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")

if __name__ == "__main__":
    showcase_enhanced_system()
    demonstrate_skill_evolution()
    demonstrate_real_time_comparison() 
    show_advanced_capabilities()
    
    print(f"\n{'🎉' * 25}")
    print("🚀 CAREERCOMPASS ENHANCED READY!")
    print("💡 Now with real-time data, skill evolution, and industry insights")
    print("🎯 Professional-grade career intelligence platform")
    print(f"{'🎉' * 25}")