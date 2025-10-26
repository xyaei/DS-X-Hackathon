# llm/advanced_trend_analyzer.py
from enhanced_analyzer import EnhancedCareerAnalyzer
import json

class AdvancedTrendAnalyzer:
    def __init__(self):
        self.analyzer = EnhancedCareerAnalyzer()
    
    def analyze_career_evolution(self, target_role, years_back=10):
        """Advanced career evolution analysis using Gemini"""
        prompt = f"""
        Analyze the evolution of {target_role} roles over the past {years_back} years.
        
        Consider:
        1. Technical skill shifts (what emerged, what declined)
        2. Tool and technology changes  
        3. Industry demand patterns
        4. Salary evolution
        5. Future predictions for next 3-5 years
        
        Provide specific, data-driven insights for someone considering this career path.
        
        Return as comprehensive JSON analysis.
        """
        
        if self.analyzer.ai_client.client:
            analysis = self.analyzer.ai_client.analyze_with_ai(prompt)
            try:
                return json.loads(analysis)
            except:
                # Fallback to structured analysis
                return self.get_structured_trends(target_role)
        return self.get_structured_trends(target_role)
    
    def get_structured_trends(self, target_role):
        """Structured trend analysis"""
        trends = {
            "Data Scientist": {
                "past_skills": ["R", "Hadoop", "Basic Statistics"],
                "current_skills": ["Python", "Machine Learning", "Cloud Platforms"],
                "future_skills": ["Generative AI", "MLOps", "Ethical AI"],
                "salary_growth": "45% increase over 5 years",
                "emerging_roles": ["AI Ethics Specialist", "MLOps Engineer"]
            },
            "Software Engineer": {
                "past_skills": ["Java", "Monolithic Architecture", "Waterfall"],
                "current_skills": ["Microservices", "Cloud Native", "DevOps"],
                "future_skills": ["AI-Assisted Coding", "Quantum Computing", "Edge Computing"],
                "salary_growth": "30% increase over 5 years", 
                "emerging_roles": ["AI Engineer", "Platform Engineer"]
            }
        }
        return trends.get(target_role, trends["Data Scientist"])

# Test it
trend_analyzer = AdvancedTrendAnalyzer()
print(json.dumps(trend_analyzer.analyze_career_evolution("Data Scientist"), indent=2))