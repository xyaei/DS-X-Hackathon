from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware  # kept for reference, not used here
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import sys
import os
import pdfplumber
import spacy
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file in parent directory
from dotenv import load_dotenv
load_dotenv()

# Try to import enhanced analyzer (optional)
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

# Load spaCy model for NER (optional)
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy NER model loaded")
except Exception:
    print("⚠️ spaCy NER model not available")
    nlp = None

router = APIRouter(prefix="/career", tags=["career"])

# Optional dataset
try:
    possible_paths = [
        "data/cleaned_resumes.csv",
        "../data/cleaned_resumes.csv",
        "./data/cleaned_resumes.csv",
    ]
    df = None
    for path in possible_paths:
        try:
            df = pd.read_csv(path)
            print(f"✅ API loaded {len(df)} resumes from {path}")
            break
        except Exception:
            continue
    if df is None:
        print("⚠️ No resume data loaded: Could not find cleaned_resumes.csv")
except Exception as e:
    df = None
    print(f"⚠️ No resume data loaded: {e}")

# ---- Simple built-in fallback analyzer (no external deps) ----

ROLE_BASELINES: Dict[str, List[str]] = {
    "Data Analyst": [
        "python","sql","excel","tableau","power bi","pandas","numpy","data analysis","statistics","visualization"
    ],
    "Data Scientist": [
        "python","sql","pandas","numpy","scikit-learn","pytorch","tensorflow","ml","statistics","nlp"
    ],
    "Software Engineer": [
        "python","java","javascript","react","node.js","git","linux","docker","sql","rest"
    ],
    "Machine Learning Engineer": [
        "python","pytorch","tensorflow","ml","docker","kubernetes","aws","gcp","feature engineering","deployment"
    ],
    "Business Analyst": [
        "sql","excel","power bi","tableau","requirements","stakeholder management","process","analysis","dashboard"
    ],
}

def fallback_analyze(resume_text: str, skills: List[str], target_role: str,
                     experience_level: str = "Intermediate", industry: str = "Technology") -> Dict[str, Any]:
    """A lightweight, deterministic analysis when EnhancedCareerAnalyzer is unavailable."""
    role = target_role if target_role in ROLE_BASELINES else "Data Analyst"
    baseline = [s.lower() for s in ROLE_BASELINES[role]]
    user_skills = sorted(set([s.lower() for s in skills]))
    matched = sorted([s for s in user_skills if s in baseline])
    missing = sorted([s for s in baseline if s not in user_skills])

    # Tiny heuristic scoring
    coverage = len(matched) / max(len(baseline), 1)
    level_bonus = {"Entry": 0.0, "Intermediate": 0.05, "Senior": 0.1}.get(experience_level, 0.0)
    score = round(min(1.0, coverage + level_bonus), 2)

    suggestions = []
    if missing:
        suggestions.append(
            f"Focus on {', '.join(missing[:5])}" + ("…" if len(missing) > 5 else "")
        )
    if "projects" not in resume_text.lower():
        suggestions.append("Add 1-2 impact-focused project bullets with metrics.")
    if "sql" in missing and "python" in matched:
        suggestions.append("Pair Python with SQL queries on real datasets to close the analytics loop.")
    if "tableau" in missing and "power bi" in missing:
        suggestions.append("Learn one BI tool (Tableau or Power BI) and build a portfolio dashboard.")

    return {
        "analysis_source": "fallback_analyzer",
        "target_role": role,
        "experience_level": experience_level,
        "industry": industry,
        "score": score,  # 0..1
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": suggestions,
        "notes": "Using local baseline because EnhancedCareerAnalyzer is unavailable.",
    }

# ---- Models ----

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    skills: List[str]
    target_role: str = "Data Analyst"
    experience_level: str = "Intermediate"
    industry: str = "Technology"

# ---- Helpers ----

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
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            anonymized_text = anonymized_text.replace(ent.text, f"[{ent.label_}_REDACTED]")
    return anonymized_text

def extract_skills_from_text(text):
    """Extract skills from resume text"""
    tech_skills = [
        'python','java','javascript','sql','r','c++','c#','php','swift',
        'html','css','react','angular','vue','node.js','django','flask',
        'spring','mysql','postgresql','mongodb','redis','aws','azure',
        'gcp','docker','kubernetes','jenkins','git','linux','machine learning',
        'deep learning','data analysis','tableau','power bi','excel','tensorflow',
        'pytorch','pandas','numpy','scikit-learn','nlp','computer vision','rest',
        'feature engineering','deployment','statistics','visualization','requirements',
        'stakeholder management','process','dashboard','ml'
    ]
    found = []
    text_lower = text.lower()
    for skill in tech_skills:
        if skill in text_lower:
            found.append(skill)
    return sorted(list(set(found)))

# ---- Routes ----

@router.get("/")
async def root():
    return {
        "message": "CareerCompass API",
        "version": "2.0",
        "status": "active",
        "analyzer_available": analyzer is not None,
        "data_loaded": df is not None,
        "features": ["resume_analysis", "skill_gap_analysis", "career_path", "market_insights"]
    }

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and process resume file. Returns full_text for analysis."""
    try:
        contents = await file.read()
        if file.filename.lower().endswith(".pdf") or file.content_type == "application/pdf":
            temp_path = f"temp_resume_{datetime.now().timestamp()}.pdf"
            with open(temp_path, "wb") as f:
                f.write(contents)
            resume_text = extract_text_from_pdf(temp_path)
            os.remove(temp_path)
        else:
            # Assume text or image with no OCR in this demo
            resume_text = contents.decode("utf-8", errors="ignore")

        anonymized_text = anonymize_resume(resume_text)
        extracted_skills = extract_skills_from_text(resume_text)

        return {
            "status": "success",
            "filename": file.filename,
            "text_length": len(anonymized_text),
            # NEW: return full text for the frontend to pass into /analyze-resume
            "full_text": resume_text,
            "anonymized_preview": anonymized_text[:500] + "..." if len(anonymized_text) > 500 else anonymized_text,
            "extracted_skills": extracted_skills,
            "skill_count": len(extracted_skills),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume processing failed: {str(e)}")

@router.post("/analyze-resume")
async def analyze_resume(request: ResumeAnalysisRequest):
    """
    Analyze resume and provide career insights.
    Uses EnhancedCareerAnalyzer if available; otherwise falls back to local baseline analysis.
    """
    try:
        if analyzer is not None:
            analysis = analyzer.analyze_resume(
                request.resume_text,
                request.skills,
                request.target_role,
                request.experience_level,
                request.industry,
            )
            source = analysis.get("analysis_source", "enhanced_analyzer")
        else:
            analysis = fallback_analyze(
                resume_text=request.resume_text,
                skills=request.skills,
                target_role=request.target_role,
                experience_level=request.experience_level,
                industry=request.industry,
            )
            source = analysis.get("analysis_source", "fallback_analyzer")

        return {
            "status": "success",
            "analysis": analysis,
            "role": request.target_role,
            "industry": request.industry,
            "analysis_source": source,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/analyze-trends/{role}")
async def analyze_trends(role: str, years_back: int = 5):
    """Analyze skill trends for a role (only available if enhanced analyzer is present)."""
    if analyzer is None:
        # graceful, not 500
        return {
            "status": "success",
            "role": role,
            "trends": [],
            "analysis_source": "fallback_analyzer",
            "notes": "Trend analysis requires EnhancedCareerAnalyzer; returning empty trends.",
        }
    try:
        trends = analyzer.analyze_skill_evolution(role, years_back)
        return {"status": "success", "role": role, "trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "analyzer_available": analyzer is not None,
        "data_loaded": df is not None,
        "ner_available": nlp is not None,
        "openai_available": hasattr(analyzer, "client") and analyzer.client is not None if analyzer else False,
    }

@router.get("/sample-resumes")
async def get_sample_resumes(count: int = 3):
    """Get sample resumes for testing"""
    if df is None:
        mock_samples = [
            {
                "resume_text": "Experienced data analyst with 3 years in Python, SQL, and data visualization. Strong analytical skills and business acumen.",
                "extracted_skills": ["python", "sql", "data analysis"],
                "positions": "Data Analyst",
            },
            {
                "resume_text": "Software engineer specializing in web development with JavaScript, React, and Node.js. Experience with cloud platforms.",
                "extracted_skills": ["javascript", "react", "node.js", "cloud"],
                "positions": "Software Engineer",
            },
        ]
        return {"status": "success", "count": len(mock_samples), "samples": mock_samples[:count]}
    samples = df.head(count)[["resume_text", "extracted_skills", "positions"]].fillna("").to_dict("records")
    return {"status": "success", "count": len(samples), "samples": samples}

@router.get("/roles")
async def get_available_roles():
    """Get list of available roles for analysis"""
    roles = [
        "Data Analyst",
        "Data Scientist",
        "Software Engineer",
        "Machine Learning Engineer",
        "Business Analyst",
    ]
    return {"status": "success", "roles": roles}
