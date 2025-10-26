# llm/trend_analyzer.py - FIXED IMPORTS
import json
import pandas as pd
from datetime import datetime
import sys
import os

# Add parent directory to path to import from the same directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from llm.enhanced_analyzer import EnhancedCareerAnalyzer
except ImportError:
    # Try relative import
    from enhanced_analyzer import EnhancedCareerAnalyzer

class CareerTrendAnalyzer:
    def __init__(self):
        self.analyzer = EnhancedCareerAnalyzer()
        
    # ... rest of your existing code remains the same ...

class CareerTrendAnalyzer:
    def __init__(self):
        self.analyzer = EnhancedCareerAnalyzer()
        
    def analyze_career_evolution(self, target_role, years_back=10):
        """Analyze career evolution using your merged.json dataset"""
        try:
            # Load your merged.json dataset
            with open('data/merged.json', 'r') as f:
                historical_data = json.load(f)
            
            # Filter data for the target role and time period
            current_year = datetime.now().year
            relevant_data = []
            
            for entry in historical_data:
                if entry['year'] >= (current_year - years_back):
                    for position in entry['positions']:
                        if target_role.lower() in position['position'].lower():
                            relevant_data.append({
                                'year': entry['year'],
                                'position': position['position'],
                                'skills': self._parse_skills(position['skills'])
                            })
            
            # Build prompt for Gemini
            prompt = self._build_trend_prompt(target_role, relevant_data, years_back)
            
            if self.analyzer.ai_client.client:
                analysis = self.analyzer.ai_client.analyze_with_ai(prompt)
                return self._parse_trend_analysis(analysis, target_role)
            else:
                return self._get_fallback_trends(target_role)
                
        except Exception as e:
            print(f"❌ Trend analysis failed: {e}")
            return self._get_fallback_trends(target_role)
    
    def _parse_skills(self, skills_str):
        """Parse skills from string format to list"""
        try:
            if isinstance(skills_str, str) and skills_str.startswith('['):
                return eval(skills_str)
            return []
        except:
            return []
    
    def _build_trend_prompt(self, target_role, historical_data, years_back):
        """Build prompt for career trend analysis"""
        return f"""
        Analyze the evolution of {target_role} roles over the past {years_back} years using this historical data:

        HISTORICAL POSITION DATA:
        {json.dumps(historical_data[:10], indent=2)}  # Sample of data

        Provide insights on:

        1. SKILL EVOLUTION:
           - Which technical skills have emerged as most important?
           - Which skills have declined in importance?
           - New skill categories that didn't exist {years_back} years ago

        2. ROLE TRANSFORMATION:
           - How has the {target_role} role evolved?
           - New responsibilities that have been added
           - Obsolete responsibilities

        3. FUTURE PREDICTIONS:
           - Skills that will be crucial in the next 2-3 years
           - Emerging technologies to watch
           - How AI/automation is changing this role

        4. CAREER ADVICE:
           - Most valuable skills to learn now
           - Certifications or education paths
           - Portfolio project ideas

        Return as JSON:
        {{
            "skill_evolution": {{
                "emerging_skills": ["skill1", "skill2"],
                "declining_skills": ["skill1", "skill2"],
                "new_categories": ["category1", "category2"]
            }},
            "role_transformation": {{
                "added_responsibilities": ["resp1", "resp2"],
                "obsolete_tasks": ["task1", "task2"],
                "evolution_summary": "Brief description"
            }},
            "future_predictions": {{
                "crucial_skills": ["skill1", "skill2"],
                "emerging_tech": ["tech1", "tech2"],
                "ai_impact": "How AI is changing this role"
            }},
            "career_advice": {{
                "top_skills": ["skill1", "skill2", "skill3"],
                "learning_path": "Recommended approach",
                "project_ideas": ["idea1", "idea2"]
            }}
        }}
        """
    
    def _parse_trend_analysis(self, analysis_text, target_role):
        """Parse the trend analysis response"""
        try:
            analysis_text = analysis_text.strip()
            if analysis_text.startswith('```json'):
                analysis_text = analysis_text[7:]
            if analysis_text.endswith('```'):
                analysis_text = analysis_text[:-3]
            
            analysis_data = json.loads(analysis_text)
            analysis_data["analysis_timestamp"] = datetime.now().isoformat()
            analysis_data["target_role"] = target_role
            analysis_data["source"] = "Gemini 2.5 Flash + Historical Dataset"
            
            return analysis_data
        except Exception as e:
            print(f"❌ Trend analysis parsing failed: {e}")
            return self._get_fallback_trends(target_role)
    
    def _get_fallback_trends(self, target_role):
        """Fallback trend analysis"""
        return {
            "skill_evolution": {
                "emerging_skills": ["AI/ML", "Cloud Computing", "Data Engineering"],
                "declining_skills": ["Manual Reporting", "Traditional ETL"],
                "new_categories": ["MLOps", "DataOps", "AI Ethics"]
            },
            "role_transformation": {
                "added_responsibilities": ["AI integration", "Cloud infrastructure", "Data governance"],
                "obsolete_tasks": ["Manual data entry", "Basic reporting"],
                "evolution_summary": f"{target_role} roles have shifted from basic analysis to strategic data leadership"
            },
            "future_predictions": {
                "crucial_skills": ["Python", "SQL", "Cloud Platforms", "Machine Learning"],
                "emerging_tech": ["Generative AI", "Edge Computing", "Quantum Computing"],
                "ai_impact": "AI is automating routine tasks, allowing professionals to focus on strategic insights"
            },
            "career_advice": {
                "top_skills": ["Python", "SQL", "Data Visualization", "Business Acumen"],
                "learning_path": "Focus on practical projects and cloud certifications",
                "project_ideas": ["End-to-end data pipeline", "ML model deployment", "Real-time dashboard"]
            },
            "target_role": target_role,
            "analysis_timestamp": datetime.now().isoformat(),
            "source": "Fallback Analysis"
        }