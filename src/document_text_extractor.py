from docling.document_converter import DocumentConverter
import fitz

def extract_text(file_path):
    doc = fitz.open(file_path)
    total_pages = len(doc)
    converter = DocumentConverter()
    text=""
    for i in range(1,total_pages,5):
        result = converter.convert(file_path,page_range=(i,i+5))
        text += result.document.export_to_markdown()
        print(f"Processing pages {i} to {i+5} of {total_pages}")
    
    return text

