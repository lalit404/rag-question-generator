import chromadb

def init_collection():
    client = chromadb.Client()
    collection=client.get_or_create_collection("ncert_chunks")
    return collection

# Function 1 — init_collection()
# ChromaDB needs two things to start:

# A client — the connection to the database engine. Like mysql.connector.connect() in MySQL.
# A collection — the table where your data lives.
    
def store_embeddings(collection, chunks, embeddings,metadatas):
    ids=[f"chunks_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,                 #model.encode(chunks) returns numpy array
        embeddings=embeddings.tolist(),  #model.encode(chunks).tolist() returns plain Python list
        ids=ids,
        metadatas=metadatas                                    
    )
    
# Function 2 — store_embeddings()
# You are doing INSERT INTO. Three things go in together:

# documents — actual text of each chunk
# embeddings — 384 numbers for each chunk
# ids — unique identifier for each chunk

def query_collection(collection, model, question, n_results=3):
    question_embedding = model.encode([question]).tolist() #ChromaDB's query_embeddings expects a 2D array — a list of embeddings. Even if you are querying with one question, it expects it wrapped in a list.  
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=n_results
    )
    return results['documents'][0]
    
#results is a dictionary. It has multiple keys — documents, ids, distances etc.
    
    