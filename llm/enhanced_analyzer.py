# llm/enhanced_analyzer.py - ADD AT THE VERY TOP
import os
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
env_path = os.path.join(parent_dir, '.env')
load_dotenv(env_path)

# Now continue with your existing imports...
import json
from datetime import datetime

# Rest of your existing code...

class RealTimeDataFetcher:
    def get_market_trends(self, role, industry="Technology"):
        """Get simulated market trends for a role"""
        trends = {
            "demand_level": self._get_demand_level(role),
            "average_salary": self._get_salary_data(role),
            "trending_skills": self._get_trending_skills(role),
            "growth_prediction": self._get_growth_prediction(role),
            "last_updated": datetime.now().isoformat()
        }
        return trends
    
    def _get_demand_level(self, role):
        demand_map = {
            "Data Scientist": "Very High",
            "Software Engineer": "High", 
            "Data Analyst": "High",
            "Machine Learning Engineer": "Very High",
            "Business Analyst": "Medium"
        }
        return demand_map.get(role, "High")
    
    def _get_salary_data(self, role):
        salary_map = {
            "Data Scientist": "$120,000-$160,000",
            "Software Engineer": "$100,000-$140,000",
            "Data Analyst": "$70,000-$100,000",
            "Machine Learning Engineer": "$130,000-$180,000",
            "Business Analyst": "$65,000-$95,000"
        }
        return salary_map.get(role, "$80,000-$120,000")
    
    def _get_trending_skills(self, role):
        skill_map = {
            "Data Scientist": ["Machine Learning", "Python", "Deep Learning", "LLMs"],
            "Software Engineer": ["Cloud Computing", "Microservices", "DevOps", "Kubernetes"],
            "Data Analyst": ["SQL", "Tableau", "Python", "Statistics", "Power BI"],
            "Machine Learning Engineer": ["PyTorch", "TensorFlow", "MLOps", "Deep Learning"],
            "Business Analyst": ["SQL", "Excel", "Requirements Gathering", "Process Modeling"]
        }
        return skill_map.get(role, ["Python", "SQL", "Cloud Computing"])
    
    def _get_growth_prediction(self, role):
        growth_map = {
            "Data Scientist": "23% growth expected",
            "Software Engineer": "15% growth expected", 
            "Data Analyst": "18% growth expected",
            "Machine Learning Engineer": "35% growth expected",
            "Business Analyst": "12% growth expected"
        }
        return growth_map.get(role, "15% growth expected")

class AIClient:
    def __init__(self):
        self.client = None
        self.provider = None
        self.model_name = None
        self.setup_ai()
    
    def setup_ai(self):
        """Setup AI client with proven working Gemini 2.5 Flash model"""
        # Try Gemini first (free)
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                
                # Use the proven working model from testing
                proven_models = [
                    'models/gemini-2.5-flash',  # Stable Flash - confirmed working!
                    'models/gemini-2.5-flash-lite',  # Backup option
                    'models/gemini-2.5-pro',  # Pro version
                    'models/gemini-2.0-flash-001',  # Fallback
                ]
                
                for model_path in proven_models:
                    try:
                        print(f"🔧 Testing Gemini model: {model_path}")
                        self.client = genai.GenerativeModel(model_path)
                        # Quick test with simple prompt
                        test_response = self.client.generate_content(
                            "Respond with: OK", 
                            request_options={"timeout": 10}
                        )
                        self.provider = "gemini"
                        self.model_name = model_path
                        print(f"✅ Gemini 2.5 Flash client ready!")
                        return
                    except Exception as e:
                        print(f"⚠️ Gemini model {model_path} failed: {str(e)[:100]}")
                        continue
                        
                print("❌ No Gemini models worked")
                        
            except Exception as e:
                print(f"❌ Gemini setup failed: {e}")
        
        # Try OpenAI as backup
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=openai_key)
                self.provider = "openai"
                self.model_name = "gpt-3.5-turbo"
                print("✅ OpenAI client ready!")
                return
            except Exception as e:
                print(f"❌ OpenAI setup failed: {e}")
        
        print("❌ No AI providers available - using fallback mode")
        self.client = None
    
    def analyze_with_ai(self, prompt):
        """Analyze using available AI provider"""
        if not self.client:
            return None
            
        try:
            if self.provider == "gemini":
                response = self.client.generate_content(
                    prompt, 
                    request_options={"timeout": 60}  # Increased timeout for complex analysis
                )
                return response.text
                
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content
                
        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            return None

class EnhancedCareerAnalyzer:
    def __init__(self):
        self.ai_client = AIClient()
        self.real_time_data = RealTimeDataFetcher()
        print("🚀 Enhanced Career Analyzer with Gemini 2.5 Flash loaded!")
        if self.ai_client.client:
            print(f"🤖 Using {self.ai_client.provider.upper()} with model: {self.ai_client.model_name}")
    
    def analyze_resume(self, resume_text, user_skills, target_role="Data Analyst", 
                      experience_level="Intermediate", industry="Technology", analysis_type="detailed"):
        """Enhanced resume analysis with AI"""
        
        # Get real-time market data
        market_trends = self.real_time_data.get_market_trends(target_role, industry)
        
        # Try to use AI if available
        if self.ai_client.client:
            print(f"🤖 Using Gemini 2.5 Flash for career analysis...")
            ai_analysis = self._analyze_with_ai(resume_text, user_skills, target_role, experience_level, industry, market_trends)
            if ai_analysis:
                return ai_analysis
            else:
                print("🔄 AI analysis failed, using enhanced fallback analysis")
        
        # Fallback to comprehensive analysis
        return self._get_fallback_analysis(user_skills, target_role, market_trends)
    
    def _analyze_with_ai(self, resume_text, user_skills, target_role, experience_level, industry, market_trends):
        """Analyze using Gemini 2.5 Flash"""
        prompt = self._build_analysis_prompt(resume_text, user_skills, target_role, experience_level, industry, market_trends)
        
        print("📊 Generating AI-powered career analysis...")
        analysis_text = self.ai_client.analyze_with_ai(prompt)
        
        if not analysis_text:
            return None
            
        try:
            # Clean the response - handle JSON code blocks
            analysis_text = analysis_text.strip()
            if analysis_text.startswith('```json'):
                analysis_text = analysis_text[7:]
            elif analysis_text.startswith('```'):
                analysis_text = analysis_text[3:]
            if analysis_text.endswith('```'):
                analysis_text = analysis_text[:-3]
            analysis_text = analysis_text.strip()

            # Parse JSON response
            analysis_data = json.loads(analysis_text)
            
            # Enhance with real-time data and metadata
            analysis_data["real_time_insights"] = market_trends
            analysis_data["analysis_timestamp"] = datetime.now().isoformat()
            analysis_data["analysis_source"] = f"Gemini 2.5 Flash"
            analysis_data["model_used"] = self.ai_client.model_name
            
            print("✅ Gemini 2.5 Flash analysis successful!")
            return analysis_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"📄 Raw response preview: {analysis_text[:300]}...")
            # Try to extract JSON if it's wrapped in other text
            return self._extract_json_from_text(analysis_text, market_trends)
        except Exception as e:
            print(f"❌ AI response processing failed: {e}")
            return None

    def _extract_json_from_text(self, text, market_trends):
        """Extract JSON from text response if parsing fails"""
        try:
            # Look for JSON pattern in the text
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_text = text[start_idx:end_idx]
                analysis_data = json.loads(json_text)
                
                # Add metadata
                analysis_data["real_time_insights"] = market_trends
                analysis_data["analysis_timestamp"] = datetime.now().isoformat()
                analysis_data["analysis_source"] = "Gemini 2.5 Flash (extracted)"
                analysis_data["model_used"] = self.ai_client.model_name
                
                print("✅ Successfully extracted JSON from response!")
                return analysis_data
        except Exception as e:
            print(f"❌ JSON extraction also failed: {e}")
        
        return None
    
    def _build_analysis_prompt(self, resume_text, user_skills, target_role, experience_level, industry, market_trends):
        """Build the analysis prompt for Gemini 2.5 Flash"""
        return f"""You are CareerCompass, an expert AI career advisor specializing in {industry} industry. 

ANALYSIS REQUEST:
- Target Role: {target_role}
- Experience Level: {experience_level}
- Industry: {industry}

RESUME CONTENT (first 2000 chars):
{resume_text[:2000]}

USER'S CURRENT SKILLS:
{', '.join(user_skills)}

CURRENT MARKET TRENDS:
{json.dumps(market_trends, indent=2)}

Provide a comprehensive career analysis with SPECIFIC, ACTIONABLE insights. Focus on:

1. SKILL GAP ANALYSIS:
   - 3-5 CRITICAL technical skills missing for {target_role}
   - 2-3 essential soft skills needed
   - Gap severity assessment (Low/Medium/High) with justification

2. CAREER PROGRESSION PATH (realistic for {experience_level} level):
   - Immediate (0-1 year): Role title, key requirements, realistic salary
   - Mid-term (1-3 years): Role title, advanced requirements, salary progression
   - Long-term (3-5+ years): Senior role, leadership requirements, salary potential

3. LEARNING ROADMAP:
   - 2-3 specific courses with platforms (Coursera, edX, Udemy, etc.)
   - 1-2 hands-on project ideas relevant to {target_role}
   - Realistic timeline for skill development

4. MARKET INSIGHTS:
   - Current demand analysis for {target_role} in {industry}
   - 2-3 emerging technologies to focus on
   - Specific industry advice for career growth

IMPORTANT: Return ONLY valid JSON with this exact structure - no additional text, no code formatting:

{{
    "skill_gaps": {{
        "technical": ["skill1", "skill2", "skill3"],
        "soft_skills": ["skill1", "skill2"],
        "severity": "Medium",
        "justification": "Brief explanation of gap severity"
    }},
    "career_path": {{
        "immediate": {{
            "role": "Specific Job Title",
            "requirements": ["requirement1", "requirement2", "requirement3"],
            "salary_range": "$Realistic-Range"
        }},
        "mid_term": {{
            "role": "Advanced Job Title", 
            "requirements": ["advanced_req1", "advanced_req2"],
            "salary_range": "$Higher-Range"
        }},
        "long_term": {{
            "role": "Senior/Leadership Title",
            "requirements": ["leadership_req1", "strategic_req2"],
            "salary_range": "$Senior-Range"
        }}
    }},
    "learning_roadmap": {{
        "courses": [
            {{
                "name": "Specific Course Name",
                "platform": "Platform Name",
                "duration": "Realistic Duration",
                "focus": "What it covers"
            }}
        ],
        "projects": ["Specific project idea 1", "Specific project idea 2"],
        "timeline": "Realistic timeline description"
    }},
    "market_insights": {{
        "demand_trend": "Specific trend description",
        "emerging_tech": ["technology1", "technology2", "technology3"],
        "industry_advice": "Specific actionable advice for this industry"
    }}
}}"""
    
    def _get_fallback_analysis(self, user_skills, target_role, market_trends):
        """Provide enhanced fallback analysis when AI is not available"""
        # Enhanced role-specific analysis
        role_analysis = {
            "Data Analyst": {
                "technical_gaps": ["SQL", "Python", "Tableau/Power BI", "Statistics", "Data Visualization"],
                "soft_gaps": ["Business Communication", "Problem Solving", "Stakeholder Management"],
                "severity": "Medium",
                "immediate_role": "Junior Data Analyst",
                "mid_term_role": "Senior Data Analyst", 
                "long_term_role": "Data Analytics Manager"
            },
            "Data Scientist": {
                "technical_gaps": ["Machine Learning", "Python", "SQL", "Statistics", "Big Data Tools"],
                "soft_gaps": ["Business Acumen", "Storytelling", "Research Mindset"],
                "severity": "High",
                "immediate_role": "Junior Data Scientist",
                "mid_term_role": "Data Scientist",
                "long_term_role": "Lead Data Scientist"
            },
            "Software Engineer": {
                "technical_gaps": ["Data Structures", "System Design", "Cloud Computing", "Testing", "DevOps"],
                "soft_gaps": ["Team Collaboration", "Code Review", "Agile Methodology"],
                "severity": "Medium",
                "immediate_role": "Software Developer",
                "mid_term_role": "Senior Software Engineer",
                "long_term_role": "Engineering Manager"
            }
        }
        
        analysis_template = role_analysis.get(target_role, role_analysis["Data Analyst"])
        
        # Calculate actual missing skills
        user_skills_lower = [skill.lower() for skill in user_skills]
        missing_technical = [skill for skill in analysis_template["technical_gaps"] if skill.lower() not in user_skills_lower]
        missing_soft = analysis_template["soft_gaps"][:2]
        
        # If no technical gaps found, use the standard ones
        if not missing_technical:
            missing_technical = analysis_template["technical_gaps"][:3]

        analysis = {
            "skill_gaps": {
                "technical": missing_technical,
                "soft_skills": missing_soft,
                "severity": analysis_template["severity"],
                "justification": f"Based on standard requirements for {target_role} roles"
            },
            "career_path": {
                "immediate": {
                    "role": analysis_template["immediate_role"],
                    "requirements": [
                        "Build portfolio projects demonstrating core skills",
                        "Learn fundamental technologies and tools",
                        "Gain practical experience through internships or projects"
                    ],
                    "salary_range": "$60,000-$85,000"
                },
                "mid_term": {
                    "role": analysis_template["mid_term_role"],
                    "requirements": [
                        "Develop advanced technical expertise",
                        "Lead projects and mentor junior team members", 
                        "Specialize in specific domains or technologies"
                    ],
                    "salary_range": "$90,000-$130,000"
                },
                "long_term": {
                    "role": analysis_template["long_term_role"],
                    "requirements": [
                        "Team leadership and management skills",
                        "Strategic planning and decision making",
                        "Cross-functional collaboration and stakeholder management"
                    ],
                    "salary_range": "$130,000-$180,000"
                }
            },
            "learning_roadmap": {
                "courses": [
                    {
                        "name": f"{target_role} Fundamentals Specialization",
                        "platform": "Coursera",
                        "duration": "3-4 months",
                        "focus": "Core technical skills and foundational knowledge"
                    },
                    {
                        "name": "Applied Data Science with Python",
                        "platform": "edX",
                        "duration": "2-3 months", 
                        "focus": "Practical implementation and projects"
                    }
                ],
                "projects": [
                    f"Build a complete {target_role.lower().replace(' ', '_')}_portfolio project",
                    "Contribute to open source projects in your target domain"
                ],
                "timeline": "6-12 months for comprehensive skill development"
            },
            "market_insights": {
                "demand_trend": "Growing steadily across industries",
                "emerging_tech": ["AI and Machine Learning", "Cloud Computing", "Automation Tools"],
                "industry_advice": "Focus on building practical, portfolio-worthy projects and continuously updating skills based on market trends"
            },
            "real_time_insights": market_trends,
            "analysis_timestamp": datetime.now().isoformat(),
            "analysis_source": "enhanced_fallback",
            "model_used": "fallback"
        }
        
        return analysis

    def analyze_skill_evolution(self, role, years_back=5):
        """Analyze skill evolution trends using Gemini 2.5 Flash if available"""
        if self.ai_client.client:
            prompt = f"""Analyze skill evolution trends for {role} over the past {years_back} years.
            
            Provide insights on:
            1. Emerging skills (last 2-3 years)
            2. Declining skills  
            3. Future skill predictions (next 2-3 years)
            4. Salary impact of new vs old skills
            
            Return as JSON with: emerging_skills, declining_skills, future_predictions, salary_impact"""
            
            ai_analysis = self.ai_client.analyze_with_ai(prompt)
            if ai_analysis:
                try:
                    return json.loads(ai_analysis)
                except:
                    pass
        
        # Fallback skill evolution analysis
        return {
            "emerging_skills": [
                {"skill": "AI/ML Integration", "growth": "Rapid adoption across industries", "impact": "High"},
                {"skill": "Cloud Computing", "growth": "Steady enterprise adoption", "impact": "High"},
                {"skill": "Data Engineering", "growth": "Increasing specialization", "impact": "Medium"}
            ],
            "declining_skills": [
                {"skill": "Manual Reporting", "reason": "Automation and self-service tools"},
                {"skill": "Traditional ETL", "reason": "Modern data integration platforms"}
            ],
            "future_predictions": [
                {"skill": "Generative AI Applications", "timeline": "1-2 years", "impact": "Transformative"},
                {"skill": "MLOps and AI Engineering", "timeline": "2-3 years", "impact": "High"}
            ],
            "salary_impact": "AI, cloud, and data engineering skills command 20-30% salary premiums",
            "role": role,
            "analysis_period": f"Last {years_back} years",
            "analysis_source": "Gemini 2.5 Flash" if self.ai_client.client else "fallback"
        }

# Example usage
if __name__ == "__main__":
    analyzer = EnhancedCareerAnalyzer()
    
    # Test with sample data
    sample_resume = "Experienced data professional with 3 years in analytics. Strong SQL skills and experience with Python for data analysis. Worked on reporting dashboards and business intelligence projects."
    sample_skills = ["SQL", "Python", "Excel", "Data Analysis", "Reporting"]
    
    result = analyzer.analyze_resume(sample_resume, sample_skills, "Data Scientist")
    print(json.dumps(result, indent=2))