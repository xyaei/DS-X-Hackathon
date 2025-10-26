# demo/presentation_demo.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from llm.unified_career_analyzer import UnifiedCareerAnalyzer
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("🔄 Trying alternative import paths...")
    
    # Try adding the llm directory directly
    llm_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'llm')
    sys.path.append(llm_path)
    
    try:
        from unified_career_analyzer import UnifiedCareerAnalyzer
        print("✅ Successfully imported using alternative path")
    except ImportError:
        print("❌ Failed to import UnifiedCareerAnalyzer")
        print("💡 Make sure you have:")
        print("   - llm/__init__.py file")
        print("   - enhanced_analyzer.py in llm directory")
        sys.exit(1)

def presentation_demo():
    print("🎤 HACKATHON PRESENTATION DEMO - CAREERCOMPASS")
    print("=" * 60)
    
    try:
        analyzer = UnifiedCareerAnalyzer()
        
        print("\n1. 📊 MASSIVE HISTORICAL DATASET:")
        print(f"   • {len(analyzer.merged_data):,} real positions analyzed")
        print(f"   • Data spanning decades of market trends")
        print(f"   • Not just AI guesses - real historical patterns")
        
        print("\n2. 🎯 LIVE CAREER ANALYSIS DEMO:")
        print("   Scenario: Business Analyst → Data Scientist")
        
        result = analyzer.enhanced_career_analysis(
            "Business analyst with 3 years experience in financial services. Strong SQL, Excel, and data visualization skills. Completed machine learning courses and built predictive models.",
            ["Excel", "SQL", "Tableau", "Statistics", "Python", "Business Analysis"],
            "Data Scientist",
            "Entry",
            "Technology"
        )
        
        print(f"   • Found {result['historical_context']['total_historical_positions']:,} real Data Scientist positions")
        top_skills = list(result['historical_context']['most_common_skills'].keys())[:3]
        print(f"   • Top skills needed: {', '.join(top_skills)}")
        print(f"   • AI recommends: {result['career_path']['immediate']['role']}")
        print(f"   • Expected salary: {result['career_path']['immediate']['salary_range']}")
        
        print(f"\n3. 💡 UNIQUE VALUE PROPOSITION:")
        print("   • AI + Historical Data = Better Career Advice")
        print("   • Real market validation, not theoretical paths")  
        print("   • Data-driven skill gap analysis")
        print("   • Personalized learning roadmaps")
        
        print(f"\n4. 🚀 IMMEDIATE NEXT STEPS:")
        if 'skill_gaps' in result:
            gaps = result['skill_gaps']['technical'][:2]
            print(f"   • Learn: {', '.join(gaps)}")
        if 'learning_roadmap' in result:
            print(f"   • Start with: {result['learning_roadmap']['courses'][0]['name']}")
            
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("💡 This might be due to API limits or data loading issues")
        print("   The concept demonstrates our unique approach to career guidance")

if __name__ == "__main__":
    presentation_demo()