# RAG Question Generator

## What is this project
I built a RAG pipeline to generate MCQ questions from competitive exam books. The problem I solved is that LLMs only know their training data and have a fixed context window — you cannot feed a 300 page book directly into an LLM prompt.
My solution extracts text from any document format using Docling, which handles PDFs, DOCX, scanned pages and two column layouts. The text is broken into overlapping chunks to preserve meaning at boundaries. Each chunk is converted into a 384 dimensional vector using sentence-transformers and stored in ChromaDB.
When a user specifies a topic, the topic is embedded into a vector, ChromaDB performs similarity search and returns the most relevant chunks. Those chunks are sent as context to Groq's Llama LLM which generates MCQ questions from that content.
Key technical decisions I made: batch processing for memory efficiency on large files, overlap chunking to preserve meaning at boundaries, and topic based retrieval instead of processing all chunks to reduce API calls from 500+ to just one.


## Tech Stack
- Docling — document extraction
- sentence-transformers — text embeddings
- ChromaDB — vector database
- Groq LLM — question generation

## How to Run
1. Clone the repository
2. Create virtual environment
3. pip install -r requirements.txt
4. Add GROQ_API_KEY to .env file
5. python main.py

## Known Limitations
- Stylized chapter headings may not be detected
- Mathematical formulas not extracted
- Requires GPU for large scanned documents

## Future Improvements
- Hierarchical chunking by chapter
- Metadata storage per chunk
- Parallel batch processing with concurrent.futures
- Redis caching for repeated documents