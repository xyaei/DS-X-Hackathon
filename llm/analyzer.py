import os
import json
from datetime import datetime

class CareerAnalyzer:
    def __init__(self, model="gpt-3.5-turbo"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ OPENAI_API_KEY not found, using fallback mode")
            self.client = None
        else:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
                print("✅ OpenAI client initialized")
            except ImportError:
                print("⚠️ OpenAI library not available, using fallback mode")
                self.client = None
        
        self.model = model
        
    def analyze_resume(self, resume_text, user_skills, target_role="Data Analyst"):
        """Analyze a resume and provide career insights"""
        
        if self.client is None:
            print("⚠️ Using fallback analysis")
            return self._get_fallback_analysis(user_skills, target_role)
        
        try:
            prompt = self._build_prompt(resume_text, user_skills, target_role)
            
            print("🤖 Calling OpenAI API...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a expert career advisor. Return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            analysis_text = response.choices[0].message.content
            print("✅ OpenAI response received")
            analysis_data = json.loads(analysis_text)
            analysis_data["analysis_timestamp"] = datetime.now().isoformat()
            analysis_data["analysis_source"] = "openai"
            return analysis_data
            
        except Exception as e:
            print(f"❌ OpenAI analysis failed: {e}")
            return self._get_fallback_analysis(user_skills, target_role)
    
    def _build_prompt(self, resume_text, user_skills, target_role):
        return f"""
        Analyze this resume for a {target_role} position:

        RESUME:
        {resume_text[:2000]}

        USER SKILLS: {', '.join(user_skills)}

        Provide JSON with:
        - skill_gaps: {{technical: [], soft_skills: [], severity: "Low/Medium/High"}}
        - career_path: {{immediate: {{role, requirements, salary}}, mid_term: {{role, requirements, salary}}}}
        - learning_roadmap: {{courses: [], projects: [], timeline: ""}}
        - market_insights: {{demand_trend: "", emerging_tech: [], industry_advice: ""}}

        Return only valid JSON.
        """
    
    def _get_fallback_analysis(self, user_skills, target_role):
        """Fallback analysis without OpenAI"""
        role_gaps = {
            "Data Analyst": {
                "technical": ["SQL", "Python", "Tableau", "Statistics", "Data Visualization"],
                "soft_skills": ["Communication", "Problem Solving"],
                "severity": "Medium"
            },
            "Data Scientist": {
                "technical": ["Machine Learning", "Python", "SQL", "Statistics", "Big Data"],
                "soft_skills": ["Business Acumen", "Storytelling"],
                "severity": "High"
            },
            "Software Engineer": {
                "technical": ["Data Structures", "System Design", "Cloud Computing", "Testing"],
                "soft_skills": ["Team Collaboration", "Code Review"],
                "severity": "Medium"
            }
        }
        
        gaps = role_gaps.get(target_role, role_gaps["Data Analyst"])
        
        return {
            "skill_gaps": gaps,
            "career_path": {
                "immediate": {
                    "role": f"Junior {target_role}",
                    "requirements": ["Build portfolio", "Learn core skills"],
                    "salary_range": "$60k-$80k"
                },
                "mid_term": {
                    "role": f"Senior {target_role}",
                    "requirements": ["Advanced skills", "Project leadership"],
                    "salary_range": "$90k-$120k"
                }
            },
            "learning_roadmap": {
                "courses": [
                    {
                        "name": f"{target_role} Fundamentals",
                        "platform": "Coursera",
                        "duration": "3 months"
                    }
                ],
                "projects": ["Build portfolio project", "Practice skills"],
                "timeline": "6-12 months"
            },
            "market_insights": {
                "demand_trend": "Growing",
                "emerging_tech": ["AI", "Cloud Computing"],
                "industry_advice": "Focus on practical projects"
            },
            "analysis_timestamp": datetime.now().isoformat(),
            "analysis_source": "fallback"
        }