import json

from src.chunker import hierarchical_chunk
from src.document_text_extractor import extract_text

def is_valid_mcq(mcq):
    title = mcq.get("main", {}).get("title", "")
    options = mcq.get("main", {}).get("options", [])
    return len(title) > 15 and len(options) == 4

def extract_mcqs(file_path, client):
    full_pdf_text = extract_text(file_path)
    
    chunks,metadatas = hierarchical_chunk(full_pdf_text)
    
    all_mcqs = []
        
    for chunk in chunks:
        prompt = f"""Extract all Multiple Choice Questions from the text below.

        STRICT RULES:
        1. Only extract questions that have complete question text and exactly 4 options
        2. Pick ONLY ONE level: EASY, MEDIUM, or HARD — never combine them
        3. Skip match-the-column questions entirely
        4. Skip assertion-reason questions entirely  
        5. Skip questions where options are codes like 1,2,3,4 or A,B,C,D without actual text
        6. If answer is not clearly mentioned set answer as empty string
        7. Never use placeholder text like opt1, opt2 in options
        8. Return ONLY valid JSON array. No explanation. No markdown.
        9. If no valid MCQs found return empty array []
        10. Skip any question where options are empty or less than 4 options
        11. Skip any question where question text is less than 15 characters

        Format:
        [
        {{
            "level": "EASY or MEDIUM or HARD",
            "subject": "<subject name>",
            "topic": "<topic name>",
            "main_language": "English or Hindi",
            "main": {{
            "title": "<complete question text>",
            "options": ["option1", "option2", "option3", "option4"],
            "answer": "<exact matching option text>",
            "description": "<1-2 line explanation or empty string>"
            }}
        }}
        ]

        Text:
        {chunk}
        """
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = response.choices[0].message.content
        try:
            chunk_mcqs = json.loads(response_text)
            valid_mcqs = [mcq for mcq in chunk_mcqs if is_valid_mcq(mcq)]
            all_mcqs.extend(valid_mcqs)
        except:
            pass
            
    return all_mcqs