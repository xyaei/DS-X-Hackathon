"""
Career Compass LLM Prompt Templates
"""

CAREER_ANALYSIS_PROMPT = """
You are Career Compass, an expert AI career advisor with deep knowledge of job markets, skills trends, and career progression.

RESUME CONTENT:
{resume_text}

USER'S CURRENT SKILLS:
{user_skills}

TARGET ROLE CONTEXT:
{target_role}

Based on this information, provide a comprehensive career analysis with these specific sections:

1. SKILL GAP ANALYSIS:
   - List 3-5 missing technical skills that are high-demand for the target role
   - List 2-3 missing soft skills that are important for career growth
   - Rate the skill gap severity (Low/Medium/High)

2. CAREER PROGRESSION PATH:
   - Next immediate role (0-1 year)
   - Mid-term role (1-3 years) 
   - Long-term role (3-5 years)
   - For each step, include typical requirements and salary range

3. PERSONALIZED LEARNING ROADMAP:
   - 3 specific online courses/certifications with platforms
   - 2 practical projects to build
   - 1-2 books or key resources
   - Timeline for skill acquisition

4. MARKET INSIGHTS:
   - Current demand trend for this role (Growing/Stable/Declining)
   - Key emerging technologies to watch
   - Industry-specific advice

Format your response as valid JSON only, no additional text:

{{
    "skill_gaps": {{
        "technical": ["skill1", "skill2", "skill3"],
        "soft_skills": ["skill1", "skill2"],
        "severity": "Medium"
    }},
    "career_path": {{
        "immediate": {{
            "role": "Job Title",
            "requirements": ["req1", "req2"],
            "salary_range": "$X-$Y"
        }},
        "mid_term": {{
            "role": "Job Title", 
            "requirements": ["req1", "req2"],
            "salary_range": "$X-$Y"
        }},
        "long_term": {{
            "role": "Job Title",
            "requirements": ["req1", "req2"], 
            "salary_range": "$X-$Y"
        }}
    }},
    "learning_roadmap": {{
        "courses": [
            {{
                "name": "Course Name",
                "platform": "Platform",
                "duration": "X weeks/months"
            }}
        ],
        "projects": ["project1", "project2"],
        "resources": ["resource1", "resource2"],
        "timeline": "3-6 months for basic proficiency"
    }},
    "market_insights": {{
        "demand_trend": "Growing",
        "emerging_tech": ["tech1", "tech2"],
        "industry_advice": "Specific advice here"
    }}
}}
"""

TREND_ANALYSIS_PROMPT = """
Analyze the skill evolution for {role} between {start_year} and {end_year}.

SKILL TREND DATA:
{skill_data}

Provide insights on:

1. EMERGING SKILLS: Skills that gained significant importance
2. DECLINING SKILLS: Skills becoming less relevant  
3. CORE SKILLS: Skills that remained consistently important
4. FUTURE PREDICTIONS: Skills likely to be important in next 2-3 years
5. SALARY IMPACT: How these trends affect compensation

Return as JSON:
{{
    "emerging_skills": [
        {{"skill": "name", "growth": "description", "impact": "High/Medium/Low"}}
    ],
    "declining_skills": [
        {{"skill": "name", "reason": "description", "recommendation": "what to do"}}
    ],
    "core_skills": ["skill1", "skill2", "skill3"],
    "future_predictions": [
        {{"skill": "name", "timeline": "1-2 years", "reason": "why important"}}
    ],
    "salary_impact": "How skills affect earning potential"
}}
"""

RESUME_COMPARISON_PROMPT = """
Compare this user's resume with successful professionals in the same field.

USER RESUME:
{user_resume}

SUCCESSFUL PROFILES:
{comparison_profiles}

Identify:
1. Key differences in experience and skills
2. Missing qualifications or certifications
3. Presentation and formatting improvements
4. Achievement quantification opportunities

Return as JSON analysis.
"""