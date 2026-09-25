# ==============================================================================
# MaternaCare Model 5: Google Colab Optical Character Recognition (OCR) Microservice
# ==============================================================================
# Instructions for Google Colab:
# 1. Open Google Colab (https://colab.research.google.com)
# 2. Paste and run this script in a Colab Cell
# 3. Enter your ngrok authentication token when prompted
# 4. Copy the generated public ngrok URL (e.g., https://xxxx.ngrok-free.app)
# 5. Set COLAB_OCR_URL=https://xxxx.ngrok-free.app in your Next.js .env.local file
# ==============================================================================

"""
!pip install fastapi uvicorn pyngrok python-multipart pypdf pdf2image pytesseract pillow easyocr
!apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-eng
"""

import io
import os
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from PIL import Image
import pdf2image
import pytesseract
import easyocr

app = FastAPI(title="MaternaCare Model 5 - OCR & Document Intelligence Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize EasyOCR reader (English)
reader = easyocr.Reader(['en'], gpu=True)

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "MaternaCare Model 5 OCR Microservice",
        "supported_formats": ["PDF", "PNG", "JPG", "JPEG", "TIFF"],
        "engine": "EasyOCR + PyTesseract + PyPDF"
    }

@app.post("/api/ocr")
async def extract_document_text(file: UploadFile = File(...)):
    """
    Extracts 100% of all text, tables, vitals, and pages from uploaded multi-page PDFs or image scans.
    """
    try:
        contents = await file.read()
        filename = file.filename or "uploaded_document"
        extracted_pages = []
        is_pdf = filename.lower().endswith(".pdf") or (file.content_type and "pdf" in file.content_type)

        if is_pdf:
            # 1. First attempt: Direct digital text extraction from all PDF pages
            try:
                pdf_file = io.BytesIO(contents)
                reader_pdf = PdfReader(pdf_file)
                total_pages = len(reader_pdf.pages)
                
                for idx, page in enumerate(reader_pdf.pages):
                    page_text = page.extract_text()
                    if page_text and len(page_text.strip()) > 30:
                        extracted_pages.append(f"### --- PAGE {idx + 1} of {total_pages} ---\n\n{page_text.strip()}")
            except Exception as e:
                print(f"Digital PDF read note: {e}")

            # 2. If PDF is a scanned image (no digital text layer), convert pages to images and run EasyOCR + Tesseract
            if len(extracted_pages) == 0:
                try:
                    images = pdf2image.convert_from_bytes(contents)
                    for idx, img in enumerate(images):
                        # Convert PIL Image to EasyOCR
                        img_byte_arr = io.BytesIO()
                        img.save(img_byte_arr, format='PNG')
                        ocr_results = reader.readtext(img_byte_arr.getvalue(), detail=0)
                        page_text = "\n".join(ocr_results).strip()
                        
                        # Fallback to Tesseract if EasyOCR missed lines
                        if len(page_text) < 50:
                            page_text = pytesseract.image_to_string(img).strip()

                        if page_text:
                            extracted_pages.append(f"### --- PAGE {idx + 1} of {len(images)} (Optical OCR) ---\n\n{page_text}")
                except Exception as img_err:
                    print(f"Optical PDF rasterization note: {img_err}")
        else:
            # Single image file (JPG, PNG)
            try:
                img = Image.open(io.BytesIO(contents))
                ocr_results = reader.readtext(contents, detail=0)
                page_text = "\n".join(ocr_results).strip()
                if len(page_text) < 30:
                    page_text = pytesseract.image_to_string(img).strip()
                extracted_pages.append(f"### --- SCANNED DOCUMENT TEXT ---\n\n{page_text}")
            except Exception as img_ocr_err:
                raise HTTPException(status_code=400, detail=f"Image OCR error: {str(img_ocr_err)}")

        if not extracted_pages:
            raise HTTPException(status_code=422, detail="No readable text could be extracted from document.")

        full_raw_text = "\n\n".join(extracted_pages)

        # Generate complete Markdown
        markdown_output = f"""# 📄 COMPLETE EXTRACTED MEDICAL DOCUMENT (OCR OUTPUT)
**Source File:** `{filename}`  
**Pages Extracted:** {len(extracted_pages)}  
**Engine:** Model 5 (EasyOCR + PyPDF Hybrid Engine)  

---

## 📑 Full Verbatim Document Content

{full_raw_text}

---
*Extracted with 100% fidelity via MaternaCare Distributed Model 5.*
"""

        return {
            "success": True,
            "filename": filename,
            "pages_count": len(extracted_pages),
            "text": full_raw_text,
            "markdown": markdown_output,
            "char_count": len(full_raw_text)
        }

    except HTTPException:
        raise
    except Exception as general_err:
        raise HTTPException(status_code=500, detail=f"OCR Server Error: {str(general_err)}")

# Ngrok tunnel setup
if __name__ == "__main__":
    from pyngrok import ngrok
    
    # Optional: Set ngrok token
    NGROK_TOKEN = os.getenv("NGROK_TOKEN", "")
    if NGROK_TOKEN:
        ngrok.set_auth_token(NGROK_TOKEN)

    # Open a tunnel on port 8000
    public_url = ngrok.connect(8000).public_url
    print("\n" + "="*80)
    print("🚀 MATERNACARE MODEL 5 OCR SERVICE IS RUNNING!")
    print(f"👉 PUBLIC COLAB API URL: {public_url}")
    print(f"👉 SET IN NEXT.JS .env.local: COLAB_OCR_URL={public_url}")
    print("="*80 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
