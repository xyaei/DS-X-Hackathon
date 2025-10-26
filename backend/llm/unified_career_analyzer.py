# llm/unified_career_analyzer.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import json
from datetime import datetime
from collections import Counter
import numpy as np
from enhanced_analyzer import EnhancedCareerAnalyzer

try:
    from .enhanced_analyzer import EnhancedCareerAnalyzer
except ImportError:
    from enhanced_analyzer import EnhancedCareerAnalyzer

class UnifiedCareerAnalyzer:
    def __init__(self):
        self.analyzer = EnhancedCareerAnalyzer()
        self.merged_data = self.load_processed_data()
        self.analysis_data = self.load_analysis_data()
        
        print(f"🚀 Unified Career Analyzer Ready!")
        print(f"📊 Loaded {len(self.merged_data):,} position records")
        print(f"📅 Data spans {self.analysis_data['year_range'][0]} to {self.analysis_data['year_range'][1]}")
        print(f"🔧 {len(self.analysis_data['skill_counts'])} meaningful skills identified")
        
        # Show top skills
        top_skills = list(self.analysis_data['skill_counts'].keys())[:10]
        print(f"🏆 Top skills: {', '.join(top_skills)}")
    
    def load_processed_data(self):
        """Load the fixed processed data"""
        try:
            # Try fixed data first, fall back to original
            df = pd.read_csv('data/merged_processed_fixed.csv')
            print("✅ Loaded fixed processed data")
        except:
            df = pd.read_csv('data/merged_processed.csv')
            print("✅ Loaded original processed data")
        return df
    
    def load_analysis_data(self):
        """Load the analysis results"""
        try:
            # Try fixed analysis first, fall back to original
            with open('data/merged_analysis_fixed.json', 'r') as f:
                analysis = json.load(f)
            print("✅ Loaded fixed analysis data")
        except:
            with open('data/merged_analysis.json', 'r') as f:
                analysis = json.load(f)
            print("✅ Loaded original analysis data")
        return analysis
    
    def convert_numpy_types(self, obj):
        """Convert numpy types to native Python types for display"""
        if isinstance(obj, list):
            return [int(item) if hasattr(item, 'item') else item for item in obj]
        elif hasattr(obj, 'item'):
            return obj.item()
        elif isinstance(obj, dict):
            return {str(k): self.convert_numpy_types(v) for k, v in obj.items()}
        return obj
    
    def get_role_insights(self, target_role):
        """Get comprehensive insights for a specific role"""
        print(f"🔍 Analyzing historical data for {target_role}...")
        
        # Filter for the target role
        role_data = self.merged_data[
            self.merged_data['position_title'].str.contains(target_role, case=False, na=False)
        ]
        
        if role_data.empty:
            return {"error": f"No historical data found for {target_role}"}
        
        # Analyze role data
        all_skills = []
        for skills in role_data['extracted_skills']:
            # Handle both list and string formats
            if isinstance(skills, str):
                # Convert string representation to list
                if skills.startswith('[') and skills.endswith(']'):
                    try:
                        skills_list = eval(skills)
                        if isinstance(skills_list, list):
                            all_skills.extend(skills_list)
                    except:
                        pass
                else:
                    all_skills.append(skills)
            elif isinstance(skills, list):
                all_skills.extend(skills)
        
        # Filter out meaningless skills
        meaningful_skills = [skill for skill in all_skills 
                           if isinstance(skill, str) and len(skill) > 2 
                           and skill not in ["'", '"', ',', ' ', '[', ']', 'nan']]
        
        skill_counts = Counter(meaningful_skills)
        
        # Yearly evolution (only recent years for relevance)
        yearly_evolution = {}
        recent_years = sorted([year for year in role_data['year'].unique() if year >= 2010])  # Only years from 2010+
        
        for year in recent_years[-5:]:  # Last 5 years only
            year_skills = []
            year_positions = role_data[role_data['year'] == year]
            
            for skills in year_positions['extracted_skills']:
                if isinstance(skills, str):
                    if skills.startswith('[') and skills.endswith(']'):
                        try:
                            skills_list = eval(skills)
                            if isinstance(skills_list, list):
                                year_skills.extend([s for s in skills_list if isinstance(s, str) and len(s) > 2])
                        except:
                            pass
                    else:
                        if len(skills) > 2:
                            year_skills.append(skills)
                elif isinstance(skills, list):
                    year_skills.extend([s for s in skills if isinstance(s, str) and len(s) > 2])
            
            if year_skills:  # Only add if we have meaningful skills
                yearly_evolution[str(year)] = {
                    'positions_count': len(year_positions),
                    'top_skills': dict(Counter(year_skills).most_common(10))
                }
        
        # Convert numpy types to native Python types
        recent_years_clean = self.convert_numpy_types(recent_years[-5:]) if recent_years else []
        
        return {
            'role': target_role,
            'total_historical_positions': len(role_data),
            'years_covered': self.convert_numpy_types(sorted(role_data['year'].unique())),
            'recent_years_analyzed': recent_years_clean,
            'most_common_skills': dict(skill_counts.most_common(15)),
            'skill_evolution': yearly_evolution,
            'experience_distribution': self.convert_numpy_types(role_data['experience_level'].value_counts().to_dict()),
            'industry_distribution': self.convert_numpy_types(role_data['industry'].value_counts().to_dict())
        }
    
    def enhanced_career_analysis(self, resume_text, user_skills, target_role, experience_level="Intermediate", industry="Technology"):
        """Enhanced analysis using both AI and historical data"""
        # Get historical insights
        historical_insights = self.get_role_insights(target_role)
        
        # Build context-rich prompt
        enhanced_prompt = self._build_enhanced_prompt(
            resume_text, user_skills, target_role, historical_insights, experience_level, industry
        )
        
        # Get AI analysis
        analysis = self.analyzer.analyze_resume(
            enhanced_prompt, user_skills, target_role, experience_level, industry
        )
        
        # Enhance with historical context
        analysis["historical_context"] = historical_insights
        analysis["data_sources"] = {
            "merged_dataset_positions": len(self.merged_data),
            "analysis_timestamp": datetime.now().isoformat(),
            "data_years_covered": f"{self.analysis_data['year_range'][0]}-{self.analysis_data['year_range'][1]}",
            "meaningful_skills_analyzed": len(self.analysis_data['skill_counts'])
        }
        
        return analysis
    
    def _build_enhanced_prompt(self, resume_text, user_skills, target_role, historical_insights, experience_level, industry):
        """Build prompt with historical context"""
        
        # Extract key historical insights
        common_skills = list(historical_insights.get('most_common_skills', {}).keys())[:10]
        years_data = historical_insights.get('years_covered', [])
        recent_years = historical_insights.get('recent_years_analyzed', [])
        total_positions = historical_insights.get('total_historical_positions', 0)
        
        # Get skill evolution insights
        skill_evolution = historical_insights.get('skill_evolution', {})
        recent_skills = []
        if skill_evolution and recent_years:
            recent_year = max(skill_evolution.keys())
            recent_skills = list(skill_evolution[recent_year].get('top_skills', {}).keys())[:5]
        
        return f"""
        CAREER ANALYSIS WITH HISTORICAL MARKET DATA (Based on {len(self.merged_data):,} positions since {self.analysis_data['year_range'][0]})

        RESUME:
        {resume_text[:2000]}

        USER PROFILE:
        - Skills: {user_skills}
        - Target Role: {target_role}
        - Experience Level: {experience_level}
        - Industry: {industry}

        HISTORICAL MARKET INSIGHTS (from {total_positions} real {target_role} positions):
        - Most common skills: {common_skills}
        - Recent trending skills ({recent_years}): {recent_skills}
        - Data spans {len(years_data)} years ({min(years_data)}-{max(years_data)})
        - Based on real position data from {total_positions} historical roles

        Provide SPECIFIC, ACTIONABLE career advice that considers these real-world market patterns.
        Focus on skills that are actually in demand based on historical data.
        Consider how this role has evolved over time and what skills are most valuable today.
        Tailor recommendations for {experience_level} level in the {industry} industry.
        """
    
    def get_available_roles(self):
        """Get list of available roles with data counts"""
        common_roles = [
            "Data Scientist", "Software Engineer", "Machine Learning Engineer",
            "Data Analyst", "Business Analyst", "Product Manager",
            "DevOps Engineer", "Cloud Engineer", "Frontend Developer",
            "Backend Developer", "Full Stack Developer"
        ]
        
        role_counts = {}
        for role in common_roles:
            count = len(self.merged_data[
                self.merged_data['position_title'].str.contains(role, case=False, na=False)
            ])
            if count > 0:
                role_counts[role] = count
        
        return role_counts
    
    def analyze_skill_trends(self, skill_name):
        """Analyze trends for a specific skill across all roles"""
        skill_occurrences = []
        
        for _, row in self.merged_data.iterrows():
            skills = row['extracted_skills']
            if isinstance(skills, str) and skills.startswith('['):
                try:
                    skills_list = eval(skills)
                    if skill_name.lower() in [s.lower() for s in skills_list if isinstance(s, str)]:
                        skill_occurrences.append({
                            'year': row['year'],
                            'position': row['position_title'],
                            'industry': row['industry']
                        })
                except:
                    continue
        
        if not skill_occurrences:
            return {"error": f"No data found for skill: {skill_name}"}
        
        # Analyze by year
        years = [occ['year'] for occ in skill_occurrences]
        year_counts = Counter(years)
        
        # Analyze by industry
        industries = [occ['industry'] for occ in skill_occurrences]
        industry_counts = Counter(industries)
        
        return {
            'skill': skill_name,
            'total_occurrences': len(skill_occurrences),
            'yearly_trend': dict(year_counts.most_common()),
            'industry_distribution': dict(industry_counts.most_common()),
            'first_appearance': min(years) if years else None,
            'recent_activity': max(years) if years else None
        }

# Test the unified analyzer
if __name__ == "__main__":
    print("🚀 Testing Unified Career Analyzer with Meaningful Historical Data...")
    
    unified_analyzer = UnifiedCareerAnalyzer()
    
    # Show available roles
    print(f"\n📋 AVAILABLE ROLES WITH DATA:")
    role_counts = unified_analyzer.get_available_roles()
    for role, count in sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:8]:
        print(f"   • {role}: {count:,} positions")
    
    # Test with different roles
    test_cases = [
        {
            "resume": "Data professional with 2 years of SQL and Python experience. Built dashboards and performed business analysis. Looking to transition to data science.",
            "skills": ["SQL", "Python", "Excel", "Tableau", "Statistics"],
            "role": "Data Scientist",
            "experience": "Intermediate",
            "industry": "Technology"
        },
        {
            "resume": "Software developer with 3 years of Java and Spring experience. Worked on web applications and REST APIs. Interested in cloud technologies and system design.",
            "skills": ["Java", "Spring", "SQL", "Git", "REST API"],
            "role": "Software Engineer", 
            "experience": "Mid-Level",
            "industry": "Technology"
        },
        {
            "resume": "Machine learning enthusiast with Python and statistics background. Completed several ML projects and want to pursue a career as ML engineer.",
            "skills": ["Python", "Machine Learning", "Statistics", "Pandas", "Scikit-learn"],
            "role": "Machine Learning Engineer",
            "experience": "Entry",
            "industry": "Technology"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'#' * 60}")
        print(f"🧪 TEST CASE {i}: {case['role']}")
        print(f"{'#' * 60}")
        
        result = unified_analyzer.enhanced_career_analysis(
            case["resume"],
            case["skills"], 
            case["role"],
            case["experience"],
            case["industry"]
        )
        
        print(f"✅ Analysis complete!")
        print(f"📊 Based on {result['historical_context']['total_historical_positions']} historical positions")
        
        if result['historical_context']['recent_years_analyzed']:
            print(f"📅 Recent years analyzed: {result['historical_context']['recent_years_analyzed']}")
        
        # Show meaningful historical skills
        meaningful_skills = [skill for skill in list(result['historical_context']['most_common_skills'].keys())[:8] 
                           if isinstance(skill, str) and len(str(skill)) > 2]
        print(f"🔧 Top historical skills: {meaningful_skills}")
        
        # Show AI insights
        print(f"\n🤖 AI RECOMMENDATIONS:")
        print(f"   Missing skills: {', '.join(result['skill_gaps']['technical'][:3])}")
        print(f"   Severity: {result['skill_gaps']['severity']}")
        print(f"   Immediate role: {result['career_path']['immediate']['role']}")
        print(f"   Salary range: {result['career_path']['immediate']['salary_range']}")
    
    # Test skill trend analysis
    print(f"\n{'#' * 60}")
    print(f"📈 SKILL TREND ANALYSIS")
    print(f"{'#' * 60}")
    
    trending_skills = ["python", "machine learning", "docker", "react"]
    for skill in trending_skills:
        trend = unified_analyzer.analyze_skill_trends(skill)
        if 'error' not in trend:
            print(f"\n🔍 {skill.upper()} Trends:")
            print(f"   Total occurrences: {trend['total_occurrences']:,}")
            print(f"   First appearance: {trend['first_appearance']}")
            print(f"   Recent activity: {trend['recent_activity']}")
            print(f"   Top industries: {', '.join(list(trend['industry_distribution'].keys())[:3])}")