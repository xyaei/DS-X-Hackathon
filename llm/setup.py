# setup_simple.py
import subprocess
import sys

def install_packages():
    # Use latest compatible versions instead of pinned old versions
    packages = [
        "fastapi",
        "uvicorn[standard]", 
        "python-multipart",
        "openai",
        "python-dotenv",
        "pandas",
        "numpy",
        "spacy",
        "pdfplumber", 
        "requests",
        "plotly",
        "kagglehub",
        "scikit-learn"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    # Download spaCy model
    print("Downloading spaCy model...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    
    print("✅ All dependencies installed successfully!")

if __name__ == "__main__":
    install_packages()