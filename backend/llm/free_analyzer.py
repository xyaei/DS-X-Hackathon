import json
import requests

class FreeCareerAnalyzer:
    def __init__(self):
        self.model = "llama2"  # Free local model
    
    def analyze_resume(self, resume_text, user_skills, target_role="Data Analyst"):
        """Analyze resume using free local LLM"""
        try:
            # Try using Ollama (free local LLM)
            return self._analyze_with_ollama(resume_text, user_skills, target_role)
        except:
            # Fallback to our predefined analysis
            return self._get_fallback_analysis(user_skills, target_role)
    
    def _analyze_with_ollama(self, resume_text, user_skills, target_role):
        """Use Ollama local LLM"""
        prompt = f"""
        Analyze this resume for career development:

        Resume: {resume_text[:1000]}
        Skills: {user_skills}
        Target Role: {target_role}

        Provide career advice in JSON format with skill gaps, career path, and learning recommendations.
        """
        
        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llama2',
                    'prompt': prompt,
                    'stream': False
                }
            )
            if response.status_code == 200:
                return json.loads(response.json()['response'])
        except:
            pass
        
        return self._get_fallback_analysis(user_skills, target_role)
    
    def _get_fallback_analysis(self, user_skills, target_role):
        """Enhanced fallback analysis"""
        return {
            "skill_gaps": {
                "technical": self._get_technical_gaps(user_skills, target_role),
                "soft_skills": ["Communication", "Problem Solving", "Teamwork"],
                "severity": "Medium"
            },
            "career_path": self._get_career_path(target_role),
            "learning_roadmap": self._get_learning_roadmap(target_role),
            "market_insights": self._get_market_insights(target_role)
        }
    
    def _get_technical_gaps(self, user_skills, target_role):
        """Get relevant technical skill gaps"""
        role_requirements = {
            "Data Analyst": ["SQL", "Python", "Tableau", "Statistics", "Excel"],
            "Software Engineer": ["Data Structures", "System Design", "Testing", "Cloud"],
            "Data Scientist": ["Machine Learning", "Python", "Statistics", "Big Data"],
            "Product Manager": ["Product Strategy", "User Research", "Roadmapping", "Analytics"]
        }
        
        required = role_requirements.get(target_role, role_requirements["Data Analyst"])
        user_skills_lower = [s.lower() for s in user_skills]
        
        gaps = [skill for skill in required if skill.lower() not in user_skills_lower]
        return gaps[:3] if gaps else ["Advanced SQL", "Data Visualization", "Business Analytics"]
    
    def _get_career_path(self, target_role):
        return {
            "immediate": {
                "role": f"Junior {target_role}",
                "requirements": ["Build portfolio", "Learn core tools", "Get certification"],
                "salary_range": "$60k-$80k"
            },
            "mid_term": {
                "role": f"Senior {target_role}",
                "requirements": ["Lead projects", "Mentor juniors", "Specialize"],
                "salary_range": "$90k-$120k"
            },
            "long_term": {
                "role": f"{target_role} Manager",
                "requirements": ["Team leadership", "Strategy", "Budget management"],
                "salary_range": "$130k-$160k"
            }
        }
    
    def _get_learning_roadmap(self, target_role):
        courses = {
            "Data Analyst": [
                {"name": "Google Data Analytics", "platform": "Coursera", "duration": "6 months"},
                {"name": "SQL for Data Science", "platform": "Udemy", "duration": "2 weeks"},
                {"name": "Tableau Training", "platform": "LinkedIn Learning", "duration": "1 month"}
            ],
            "Software Engineer": [
                {"name": "CS50", "platform": "edX", "duration": "3 months"},
                {"name": "Full Stack Development", "platform": "freeCodeCamp", "duration": "6 months"},
                {"name": "System Design", "platform": "Educative", "duration": "2 months"}
            ],
            "Data Scientist": [
                {"name": "Machine Learning Specialization", "platform": "Coursera", "duration": "4 months"},
                {"name": "Python for Data Science", "platform": "DataCamp", "duration": "3 months"}
            ]
        }
        
        return {
            "courses": courses.get(target_role, courses["Data Analyst"]),
            "projects": ["Build a portfolio project", "Contribute to open source"],
            "resources": ["Industry blogs", "Meetup groups", "Online communities"],
            "timeline": "3-6 months for basic proficiency"
        }
    
    def _get_market_insights(self, target_role):
        insights = {
            "Data Analyst": {
                "demand_trend": "High Growth",
                "emerging_tech": ["AI Analytics", "Cloud BI Tools", "Automated Reporting"],
                "industry_advice": "Focus on business storytelling with data"
            },
            "Software Engineer": {
                "demand_trend": "Very High",
                "emerging_tech": ["AI Programming", "Cloud Native", "DevOps"],
                "industry_advice": "Build full-stack projects and learn system design"
            },
            "Data Scientist": {
                "demand_trend": "Rapid Growth", 
                "emerging_tech": ["Generative AI", "MLOps", "Big Data Platforms"],
                "industry_advice": "Combine technical skills with business domain knowledge"
            }
        }
        
        return insights.get(target_role, insights["Data Analyst"])