# llm/dataset_integration.py
import json
import pandas as pd
from enhanced_analyzer import EnhancedCareerAnalyzer

class DatasetCareerAnalyzer:
    def __init__(self):
        self.analyzer = EnhancedCareerAnalyzer()
        self.historical_data = self.load_historical_data()
    
    def load_historical_data(self):
        """Load your merged.json dataset"""
        try:
            with open('data/merged.json', 'r') as f:
                data = json.load(f)
            print(f"✅ Loaded {len(data)} historical resume entries")
            return data
        except Exception as e:
            print(f"❌ Failed to load historical data: {e}")
            return []
    
    def analyze_with_historical_context(self, resume_text, user_skills, target_role):
        """Analyze with historical career evolution context"""
        # Get recent trends from your dataset
        recent_trends = self.extract_recent_trends(target_role)
        
        # Enhance the prompt with historical context
        enhanced_prompt = f"""
        {resume_text[:2000]}
        
        USER SKILLS: {user_skills}
        TARGET ROLE: {target_role}
        
        HISTORICAL CAREER TRENDS (from 54k resume dataset):
        {json.dumps(recent_trends, indent=2)}
        
        Provide career analysis considering these historical patterns.
        """
        
        return self.analyzer.analyze_resume(enhanced_prompt, user_skills, target_role)
    
    def extract_recent_trends(self, target_role, years_back=5):
        """Extract trends from your historical dataset"""
        current_year = 2025  # Adjust as needed
        relevant_data = []
        
        for entry in self.historical_data:
            if entry.get('year', 0) >= (current_year - years_back):
                for position in entry.get('positions', []):
                    if target_role.lower() in position.get('position', '').lower():
                        relevant_data.append({
                            'year': entry['year'],
                            'position': position['position'],
                            'skills': self.parse_skills(position.get('skills', ''))
                        })
        
        return relevant_data[:10]  # Return top 10 most recent
    
    def parse_skills(self, skills_str):
        """Parse skills from your dataset format"""
        try:
            if isinstance(skills_str, str) and skills_str.startswith('['):
                return eval(skills_str)
            return []
        except:
            return []

# Test it
if __name__ == "__main__":
    dataset_analyzer = DatasetCareerAnalyzer()
    
    result = dataset_analyzer.analyze_with_historical_context(
        "Data professional with SQL and Python experience",
        ["SQL", "Python", "Excel"],
        "Data Scientist"
    )
    print(json.dumps(result, indent=2))