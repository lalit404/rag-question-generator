from src.vector_store import query_collection
    
def generate_questions(collection, model, client, topic, n_questions=10):
    relevant_chunks = query_collection(collection, model, topic, n_results=5)
    context = "\n".join(relevant_chunks)
    
    prompt = f"""You are an exam question generator.
        Generate {n_questions} MCQ questions based on the context below.
        Each question should have 4 options and indicate the correct answer.

        Context:
        {context}

        Topic: {topic}
        """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
#  In interviews if asked about LLM API response structure, say:
# The API returns a response object with a choices array. Each choice contains a message object with role and content fields. The generated text is in choices[0].message.content.


# all_questions = [] — collecting all responses
# append(response.choices[0].message.content) — extracting text and storing
# return all_questions — returning all questions not just last one