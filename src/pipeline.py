from src.chunker import hierarchical_chunk
from src.document_text_extractor import extract_text
from src.embedder import embed_chunks
from src.question_generator import generate_questions
from src.vector_store import init_collection, store_embeddings
from sentence_transformers import SentenceTransformer
from groq import Groq
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)
collection = init_collection()

def process_document(file_path, book_name, author):

    full_pdf_text = extract_text(file_path)
    
    chunks,metadatas = hierarchical_chunk(full_pdf_text)

    for meta in metadatas:
        meta["book_name"]=book_name
        meta["author"]=author

    embeddings = embed_chunks(chunks,model)
    store_embeddings(collection, chunks, embeddings,metadatas)
    
def generate_mcq(topic, n_questions):
    questions = generate_questions(collection, model, client, topic, n_questions)
    return questions
