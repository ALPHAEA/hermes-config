---
name: ocr-and-documents
description: Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker-pdf for OCR/scanned docs. For DOCX use python-docx, for PPTX see the powerpoint skill. Also covers image OCR (JPEG/PNG) when the current model lacks vision support.
version: 2.4.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR, Image-OCR]
    related_skills: [powerpoint]
---

# PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR).
For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs and scanned documents**.

## Step 0: Image OCR (JPEG/PNG — when model lacks vision)

When the user sends an image (JPEG/PNG screenshot of text) but the current model's `vision_analyze` tool fails with errors like `unknown variant image_url` (model doesn't support vision), use this fallback chain:

### Option 0 (NEW): Tesseract OCR (lightest, pre-installed, no rate limits)

**Tesseract is often pre-installed** on many Linux systems. Check first:
```bash
which tesseract
tesseract --version
tesseract --list-langs
```

If installed, this is the **best option** for English/scanned PDFs — no pip install, no RAM issues, no API rate limits:

```python
# Full pipeline: PDF page → PNG → Tesseract → text
import fitz, subprocess
from PIL import Image

doc = fitz.open("/path/to/scanned.pdf")
all_text = []
for i in range(doc.page_count):
    page = doc[i]
    mat = fitz.Matrix(2, 2)  # 144 DPI — good balance
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img_path = f"/tmp/ocr_page_{i+1}.png"
    img.save(img_path, format="PNG")
    subprocess.run(["tesseract", img_path, f"/tmp/ocr_page_{i+1}", "-l", "eng", "--psm", "6"],
                   capture_output=True, timeout=30)
    with open(f"/tmp/ocr_page_{i+1}.txt") as f:
        text = f.read()
    all_text.append(f"=== Page {i+1} ===\n{text.strip()}")
full_text = "\n\n".join(all_text)
```

**Key settings:**
- **144 DPI** (`Matrix(2,2)` from 72 DPI base): enough for English text, keeps image ~2MB
- **`-l eng`**: English language pack
- **`--psm 6`**: Assume uniform block of text (best for exam papers)
- **No rate limits**: fully local, process 50+ pages in one go
- **~2GB RAM enough**: tested on system with 1.9GB total RAM

**If `tesseract` not found**: install via `apt` (needs root) or use EasyOCR fallback.

**Chinese text**: Need Chinese language pack:
```bash
# Check if Chinese is available
tesseract --list-langs  # should show 'chi_sim' or 'chi_tra'
# If not, may need: sudo apt install tesseract-ocr-chi-sim
```

**Install if missing** (root required):
```bash
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng  # English
sudo apt-get install -y tesseract-ocr-chi-sim             # Chinese simplified
```

When the user sends an image (JPEG/PNG screenshot of text) but the current model's `vision_analyze` tool fails with errors like `unknown variant image_url` (model doesn't support vision), use this fallback chain:

**Note**: DeepSeek V4 Flash produces `unknown variant 'image_url', expected 'text'` — this is a model-level limitation, not a tool bug. Models using `chat_completions` api_mode may lack multimodal support entirely.

### Option A: EasyOCR (lightweight, no root needed)

```bash
# Install in the hermes venv
/home/agentuser/.hermes/hermes-agent/venv/bin/pip3 install easyocr

# Direct extraction (note: first load takes ~30s for PyTorch init)
/home/agentuser/.hermes/hermes-agent/venv/bin/python3 << 'EOF'
import easyocr
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)
results = reader.readtext('/path/to/image.jpg', detail=0, paragraph=True)
for line in results:
    print(line)
EOF
```

**Important pitfalls for EasyOCR:**
- **First import is VERY slow** (~30-60s). PyTorch loads CUDA/cpu libraries. Use a timeout of 120s+ or delegate to a subagent.
- **Already installed**: If it was previously installed in the venv, check with `ls /home/agentuser/.hermes/hermes-agent/venv/lib/python3.11/site-packages/easyocr/`
- **No root needed**: EasyOCR installs its own models to `~/.cache/huggingface/` — no system packages required.
- **Common OCR errors**: Numbers adjacent to characters may get merged (e.g. `3080500.94` → `3 08 0500,94`), Chinese punctuation gets confused with digits.
- **Sorting**: Use `paragraph=True` for grouped text, or add custom Y-axis sorting for multi-column layouts.
- **Memory**: EasyOCR + PyTorch requires ~2GB+ free RAM. On systems with 2GB total RAM, may get OOM-killed (exit code 137). Use Tesseract instead on low-RAM systems.

### Option B: Subagent delegation (preferred for long-running OCR)

If EasyOCR direct import times out, delegate to a subagent:

```
delegate_task(
    goal="Extract text from this image using OCR",
    context=f"Image path: /path/to/image.jpg\nEasyOCR installed at /home/agentuser/.hermes/hermes-agent/venv/bin/pip3",
    toolsets=["terminal", "file"]
)
```

This works because the subagent gets a fresh terminal session with its own timeout budget.

### Option C: Upload to tmpfiles + browser screenshot

If all else fails:
1. Upload the image: `curl -s -F "file=@image.jpg" https://tmpfiles.org/api/v1/upload`
2. Navigate to the download URL in the browser
3. Try `browser_vision()` on the rendered page

### Markdown → PDF workflow

After extracting text via OCR, generate a PDF:

```bash
/home/agentuser/.hermes/hermes-agent/venv/bin/pip3 install fpdf2
```

Then create a Python script using `FPDF` with a Chinese-capable font (fonts available on system: check `/usr/share/fonts/truetype/wqy/` for `wqy-zenhei.ttc`).

```python
from fpdf import FPDF
pdf = FPDF()
pdf.add_font('freesans', '', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
pdf.add_page()
pdf.set_font('freesans', '', 12)
pdf.cell(0, 10, '中文标题', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.output('/tmp/output.pdf')
```

**Note**: fpdf2 v2.5+ deprecates `uni=True` in `add_font()` and `ln=1` in `cell()` — use `new_x=XPos.LMARGIN, new_y=YPos.NEXT` instead.

### Decision flow for image OCR

```
User sends image with text → Try vision_analyze() first
  ├── Works → Done
  └── Fails (model lacks vision) →
       ├── Tesseract installed? → Run it (fastest, no rate limits)
       ├── EasyOCR installed? → Run it (delegate if timeout concern)
       ├── Not installed → pip3 install easyocr → Run it
       ├── OCR.space API (if rate limit not hit) → Use API
       └── All local options fail → Upload to tmpfiles → browser_vision()
```

**Tesseract priority**: Check first before EasyOCR — it's lighter, faster, and may be pre-installed.
**OCR.space**: Free tier limited to 20 requests/hour — use for small docs only.

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- **Always classify scanned PDFs first**: Before choosing an extraction method, open the PDF with `fitz.open(path)`, check each page with `page.get_text()` and `page.get_images()`. If text length is 0 and images exist, the PDF is scanned/image-based and needs OCR (EasyOCR or marker-pdf). If text exists, use pymupdf directly.
- **For EasyOCR on scanned PDFs**: Convert each PDF page to an image with `page.get_pixmap()` first, then run EasyOCR on the resulting PIL image. Do NOT feed PDF files directly to EasyOCR.
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)
