import os
from groq import Groq
from src.question_generator import generate_questions
from src.embedder import embed_chunks
from src.document_text_extractor import extract_text
from src.chunker import hierarchical_chunk
from src.vector_store import init_collection, store_embeddings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

groq_api_key = os.getenv("GROQ_API_KEY")
pdf_path = r"data/merged_science_chapters.pdf"

full_pdf_text = extract_text(pdf_path)

chunks = hierarchical_chunk(full_pdf_text)

embeddings = embed_chunks(chunks,model)

collection = init_collection()

store_embeddings(collection, chunks, embeddings)

client = Groq(api_key=groq_api_key)

topic = "photosynthesis"
questions = generate_questions(collection, model, client, topic, n_questions=10)
print(questions)



