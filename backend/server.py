from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pdf_utils import extract_pdf_text
import os, tempfile

from pdf_utils import extract_pdf_text  # <-- import the helper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"ok": True, "service": "trajectory-backend"}

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/upload")
async def upload_resume(resume: UploadFile = File(...)):
    # basic type check (adjust as you like)
    if resume.content_type not in {"application/pdf"} and not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF for parsing.")

    # write to a temp file so pdfplumber can open it
    suffix = os.path.splitext(resume.filename)[1] or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file_path = tmp.name
        while True:
            chunk = await resume.read(1024 * 1024)
            if not chunk:
                break
            tmp.write(chunk)

    try:
        pages = extract_pdf_text(file_path)  # List[PageText]
        combined = "\n\n".join(p.text for p in pages)
        # keep response light: return counts + first page text (and all pages if you want)
        return {
            "ok": True,
            "filename": resume.filename,
            "pages": len(pages),
            "first_page_text": pages[0].text if pages else "",
            "all_pages": [{"page": p.page_number, "text": p.text} for p in pages],  # remove if too big
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parse failed: {e}")
    finally:
        try:
            os.remove(file_path)
        except Exception:
            pass
