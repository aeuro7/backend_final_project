
import fitz

async def extract_text_from_pdf(uploaded_pdf):
    text = ""
    doc = fitz.open(stream=await uploaded_pdf.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text
