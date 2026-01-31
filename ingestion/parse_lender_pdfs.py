import pdfplumber
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "pdfs"

OUT_DIR = BASE_DIR / Path("parsed_pdfs")
OUT_DIR.mkdir(exist_ok=True)

def extract_text(pdf_path: Path):
    text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

    out_file = OUT_DIR / f"{pdf_path.stem}.txt"
    out_file.write_text("\n\n".join(text), encoding="utf-8")

if __name__ == "__main__":
    for pdf in PDF_DIR.glob("*.pdf"):
        extract_text(pdf)
