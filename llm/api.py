from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd
import json
import sys
import os
import uvicorn
import pdfplumber
import spacy
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file in parent directory
from dotenv import load_dotenv
load_dotenv()

# Try to import enhanced analyzer
try:
    from enhanced_analyzer import EnhancedCareerAnalyzer
    analyzer = EnhancedCareerAnalyzer()
    print("✅ Enhanced analyzer loaded successfully!")
except ImportError as e:
    print(f"❌ Enhanced analyzer import failed: {e}")
    analyzer = None
except Exception as e:
    print(f"❌ Enhanced analyzer initialization failed: {e}")
    analyzer = None

# Load spaCy model for NER
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy NER model loaded")
except:
    print("⚠️ spaCy NER model not available")
    nlp = None

app = FastAPI(title="CareerCompass API", version="2.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data once at startup
try:
    # Try different possible paths for the data file
    possible_paths = [
        "data/cleaned_resumes.csv",
        "../data/cleaned_resumes.csv",
        "./data/cleaned_resumes.csv"
    ]
    
    df = None
    for path in possible_paths:
        try:
            df = pd.read_csv(path)
            print(f"✅ API loaded {len(df)} resumes from {path}")
            break
        except:
            continue
            
    if df is None:
        print("⚠️ No resume data loaded: Could not find cleaned_resumes.csv")
        df = None
        
except Exception as e:
    df = None
    print(f"⚠️ No resume data loaded: {e}")

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    skills: List[str]
    target_role: str = "Data Analyst"
    experience_level: str = "Intermediate"
    industry: str = "Technology"

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF extraction failed: {str(e)}")

def anonymize_resume(text):
    """Anonymize resume text using NER"""
    if not nlp or not text:
        return text
    
    doc = nlp(text)
    anonymized_text = text
    
    # Replace sensitive entities
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            anonymized_text = anonymized_text.replace(ent.text, f"[{ent.label_}_REDACTED]")
    
    return anonymized_text

def extract_skills_from_text(text):
    """Extract skills from resume text"""
    tech_skills = [
        'python', 'java', 'javascript', 'sql', 'r', 'c++', 'c#', 'php', 'swift',
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask',
        'spring', 'mysql', 'postgresql', 'mongodb', 'redis', 'aws', 'azure',
        'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'linux', 'machine learning',
        'deep learning', 'data analysis', 'tableau', 'power bi', 'excel', 'tensorflow',
        'pytorch', 'pandas', 'numpy', 'scikit-learn', 'nlp', 'computer vision'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in tech_skills:
        if skill in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))

@app.get("/")
async def root():
    return {
        "message": "CareerCompass API", 
        "version": "2.0",
        "status": "active",
        "analyzer_available": analyzer is not None,
        "data_loaded": df is not None,
        "features": ["resume_analysis", "skill_gap_analysis", "career_path", "market_insights"]
    }

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and process resume file"""
    try:
        # Read file content
        contents = await file.read()
        
        if file.filename.endswith('.pdf'):
            # Save temporarily and extract text
            temp_path = f"temp_resume_{datetime.now().timestamp()}.pdf"
            with open(temp_path, "wb") as f:
                f.write(contents)
            resume_text = extract_text_from_pdf(temp_path)
            os.remove(temp_path)
        else:
            # Assume text file
            resume_text = contents.decode('utf-8')
        
        # Anonymize resume
        anonymized_text = anonymize_resume(resume_text)
        
        # Extract skills
        extracted_skills = extract_skills_from_text(resume_text)
        
        return {
            "status": "success",
            "filename": file.filename,
            "text_length": len(anonymized_text),
            "anonymized_preview": anonymized_text[:500] + "..." if len(anonymized_text) > 500 else anonymized_text,
            "extracted_skills": extracted_skills,
            "skill_count": len(extracted_skills)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume processing failed: {str(e)}")

@app.post("/analyze-resume")
async def analyze_resume(request: ResumeAnalysisRequest):
    """Analyze resume and provide career insights"""
    if analyzer is None:
        raise HTTPException(status_code=500, detail="Career analyzer not available")
    
    try:
        analysis = analyzer.analyze_resume(
            request.resume_text,
            request.skills,
            request.target_role,
            request.experience_level,
            request.industry
        )
        return {
            "status": "success",
            "analysis": analysis,
            "role": request.target_role,
            "industry": request.industry,
            "analysis_source": analysis.get("analysis_source", "unknown")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/analyze-trends/{role}")
async def analyze_trends(role: str, years_back: int = 5):
    """Analyze skill trends for a role"""
    if analyzer is None:
        raise HTTPException(status_code=500, detail="Career analyzer not available")
    
    try:
        trends = analyzer.analyze_skill_evolution(role, years_back)
        return {
            "status": "success",
            "role": role,
            "trends": trends
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "analyzer_available": analyzer is not None,
        "data_loaded": df is not None,
        "ner_available": nlp is not None,
        "openai_available": hasattr(analyzer, 'client') and analyzer.client is not None if analyzer else False
    }

@app.get("/sample-resumes")
async def get_sample_resumes(count: int = 3):
    """Get sample resumes for testing"""
    if df is None:
        # Return mock data if no dataset
        mock_samples = [
            {
                "resume_text": "Experienced data analyst with 3 years in Python, SQL, and data visualization. Strong analytical skills and business acumen.",
                "extracted_skills": ["python", "sql", "data analysis"],
                "positions": "Data Analyst"
            },
            {
                "resume_text": "Software engineer specializing in web development with JavaScript, React, and Node.js. Experience with cloud platforms.",
                "extracted_skills": ["javascript", "react", "node.js", "cloud"],
                "positions": "Software Engineer"
            }
        ]
        return {
            "status": "success",
            "count": len(mock_samples),
            "samples": mock_samples[:count]
        }
    
    samples = df.head(count)[['resume_text', 'extracted_skills', 'positions']].fillna('').to_dict('records')
    return {
        "status": "success",
        "count": len(samples),
        "samples": samples
    }

@app.get("/roles")
async def get_available_roles():
    """Get list of available roles for analysis"""
    roles = [
        "Data Analyst",
        "Data Scientist", 
        "Software Engineer",
        "Machine Learning Engineer",
        "Business Analyst"
    ]
    return {
        "status": "success",
        "roles": roles
    }

if __name__ == "__main__":
    # Fix the reload warning by using the app directly
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)