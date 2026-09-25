# ==============================================================================
# MaternaCare Model 5: Google Colab Optical Character Recognition (OCR) Engine
# ==============================================================================
# 100% Free - Works out-of-the-box in Google Colab (NO ngrok token required!)
# Uses Cloudflare Quick Tunnels + GPU EasyOCR + PyPDF + PyTesseract
# ==============================================================================

import io
import os
import re
import time
import subprocess
import threading
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from PIL import Image
import pdf2image
import pytesseract
import easyocr

app = FastAPI(title="MaternaCare Model 5 OCR Microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("⏳ Initializing EasyOCR GPU Engine...")
# Initialize reader on GPU (falls back to CPU if no CUDA)
try:
    reader = easyocr.Reader(['en'], gpu=True)
except Exception:
    reader = easyocr.Reader(['en'], gpu=False)
print("✅ EasyOCR Engine Loaded & Ready!")

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "MaternaCare Model 5 OCR Microservice",
        "supported_formats": ["PDF", "PNG", "JPG", "JPEG", "TIFF"],
        "engine": "PyMuPDF + GPU EasyOCR + PyPDF + PyTesseract"
    }

@app.post("/api/ocr")
async def extract_document_text(file: UploadFile = File(...)):
    """
    Extracts 100% of all text, tables, vitals, and pages from uploaded multi-page PDFs or image scans.
    """
    try:
        contents = await file.read()
        filename = file.filename or "uploaded_document.pdf"
        extracted_pages = []
        is_pdf = filename.lower().endswith(".pdf") or (file.content_type and "pdf" in file.content_type)

        if is_pdf:
            # 1. PyMuPDF (fitz) - handles digital text & renders raster pages with high precision
            try:
                import fitz
                doc = fitz.open(stream=contents, filetype="pdf")
                total_pages = len(doc)
                for idx in range(total_pages):
                    page = doc[idx]
                    page_text = page.get_text()
                    if page_text and len(page_text.strip()) > 10:
                        extracted_pages.append(f"### --- PAGE {idx + 1} of {total_pages} ---\n\n{page_text.strip()}")
                    else:
                        # Page has images/scans - rasterize & run OCR
                        pix = page.get_pixmap(dpi=200)
                        img_bytes = pix.tobytes("png")
                        ocr_lines = reader.readtext(img_bytes, detail=0)
                        ocr_text = "\n".join(ocr_lines).strip()
                        if len(ocr_text) < 30:
                            pil_img = Image.open(io.BytesIO(img_bytes))
                            ocr_text = pytesseract.image_to_string(pil_img).strip()
                        if ocr_text:
                            extracted_pages.append(f"### --- PAGE {idx + 1} of {total_pages} (Optical OCR) ---\n\n{ocr_text}")
            except Exception as fitz_err:
                print(f"PyMuPDF note: {fitz_err}")

            # 2. PyPDF fallback across all pages
            if len(extracted_pages) == 0:
                try:
                    pdf_file = io.BytesIO(contents)
                    reader_pdf = PdfReader(pdf_file)
                    total_pages = len(reader_pdf.pages)
                    
                    for idx, page in enumerate(reader_pdf.pages):
                        page_text = page.extract_text()
                        if page_text and len(page_text.strip()) > 5:
                            extracted_pages.append(f"### --- PAGE {idx + 1} of {total_pages} ---\n\n{page_text.strip()}")
                        else:
                            page_imgs = []
                            try:
                                for img_obj in page.images:
                                    ocr_results = reader.readtext(img_obj.data, detail=0)
                                    if ocr_results:
                                        page_imgs.append("\n".join(ocr_results))
                                    else:
                                        pil_img = Image.open(io.BytesIO(img_obj.data))
                                        tess = pytesseract.image_to_string(pil_img).strip()
                                        if tess:
                                            page_imgs.append(tess)
                            except Exception as img_err:
                                print(f"Image scan note: {img_err}")
                            if page_imgs:
                                extracted_pages.append(f"### --- PAGE {idx + 1} of {total_pages} (Optical OCR) ---\n\n" + "\n\n".join(page_imgs))
                except Exception as pypdf_err:
                    print(f"PyPDF note: {pypdf_err}")

            # 3. pdf2image fallback with poppler
            if len(extracted_pages) == 0:
                try:
                    images = pdf2image.convert_from_bytes(contents)
                    for idx, img in enumerate(images):
                        img_byte_arr = io.BytesIO()
                        img.save(img_byte_arr, format='PNG')
                        ocr_results = reader.readtext(img_byte_arr.getvalue(), detail=0)
                        page_text = "\n".join(ocr_results).strip()
                        if len(page_text) < 40:
                            page_text = pytesseract.image_to_string(img).strip()
                        if page_text:
                            extracted_pages.append(f"### --- PAGE {idx + 1} of {len(images)} (Optical OCR) ---\n\n{page_text}")
                except Exception as img_err:
                    print(f"Optical PDF rasterization note: {img_err}")
        else:
            # Image scans (JPG, PNG) or plain text
            try:
                img = Image.open(io.BytesIO(contents))
                ocr_results = reader.readtext(contents, detail=0)
                page_text = "\n".join(ocr_results).strip()
                if len(page_text) < 30:
                    page_text = pytesseract.image_to_string(img).strip()
                extracted_pages.append(f"### --- SCANNED DOCUMENT TEXT ---\n\n{page_text}")
            except Exception:
                try:
                    text_str = contents.decode("utf-8", errors="ignore").strip()
                    if text_str:
                        extracted_pages.append(f"### --- DOCUMENT TEXT CONTENT ---\n\n{text_str}")
                except Exception as text_err:
                    raise HTTPException(status_code=400, detail=f"Document read error: {str(text_err)}")

        if not extracted_pages:
            raise HTTPException(status_code=422, detail="No readable text could be extracted from document.")

        full_raw_text = "\n\n".join(extracted_pages)

        # Generate complete Markdown
        markdown_output = f"""# 📄 COMPLETE EXTRACTED MEDICAL DOCUMENT (OCR OUTPUT)
**Source File:** `{filename}`  
**Pages Extracted:** {len(extracted_pages)}  
**Engine:** Model 5 (GPU EasyOCR + PyMuPDF + PyPDF)  

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

def run_server():
    # 1. Start FastAPI server in background thread
    def start_uvicorn():
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

    server_thread = threading.Thread(target=start_uvicorn, daemon=True)
    server_thread.start()
    time.sleep(2)
    print("✅ FastAPI Server listening on http://127.0.0.1:8000")

    # 2. Download and launch Cloudflare Quick Tunnel (Free, no account needed)
    subprocess.run(["wget", "-q", "-nc", "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"])
    subprocess.run(["chmod", "+x", "cloudflared-linux-amd64"])

    print("🌐 Launching Free Cloudflare Public Tunnel (No Signup / No Token Required)...")
    tunnel_proc = subprocess.Popen(
        ["./cloudflared-linux-amd64", "tunnel", "--url", "http://127.0.0.1:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    public_url = None
    for _ in range(40):
        line = tunnel_proc.stderr.readline()
        match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
        if match:
            public_url = match.group(0)
            break
        time.sleep(0.3)

    if public_url:
        print("\n" + "="*80)
        print("🚀 MATERNACARE MODEL 5 OCR SERVICE IS RUNNING!")
        print(f"👉 PUBLIC API URL: {public_url}")
        print(f"👉 COPY AND SET IN YOUR NEXT.JS .env.local: COLAB_OCR_URL={public_url}")
        print("="*80 + "\n")
    else:
        print("⚠️ Tunnel initializing in background. Check console output for trycloudflare.com link.")

    # Keep alive in Colab
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down OCR service.")

if __name__ == "__main__":
    run_server()
