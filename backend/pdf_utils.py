import re
from dataclasses import dataclass
from typing import List
from unidecode import unidecode
import pdfplumber

@dataclass
class PageText:
    page_number: int
    text: str

HYPHEN_JOIN = re.compile(r"(\w)-\n(\w)")

def clean_text(s: str) -> str:
    s = unidecode(s or "")
    s = HYPHEN_JOIN.sub(r"\1\2", s)
    s = s.replace("\r", "\n")
    s = re.sub(r"\n{2,}", "\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()

def extract_pdf_text(path: str) -> List[PageText]:
    pages: List[PageText] = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            t = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            pages.append(PageText(page_number=i, text=clean_text(t)))
    return pages
