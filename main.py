from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from src.pipeline import process_document, generate_mcq
import shutil

app = FastAPI()

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    book_name: str = Form(...),
    author: str = Form(...)
):
    try:
        file_path = f"data/{file.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        process_document(file_path, book_name, author)
        return {"message": "Document processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate")
async def generate(topic: str = Form(...), n_questions: int = Form(10)):
    try:
        questions = generate_mcq(topic, n_questions)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/extract-mcqs")
async def extract_mcqs_endpoint(
    file: UploadFile = File(...),
):
    try:
        file_path = f"data/{file.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        from src.mcq_extractor import extract_mcqs
        from src.pipeline import client
        
        mcqs = extract_mcqs(file_path, client)
        return {"mcqs": mcqs, "total": len(mcqs)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))