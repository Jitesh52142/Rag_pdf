import os
from google import genai
from supabase_client import supabase
from dotenv import load_dotenv


load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# -----------------------------
# EMBEDDING
# -----------------------------
def generate_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={
            "output_dimensionality": 768
        }
    )
    return response.embeddings[0].values
# -----------------------------
# STORE CHUNKS
# -----------------------------
def store_chunks(chunks):
    for chunk in chunks:
        embedding = generate_embedding(chunk)

        supabase.table("documents").insert({
            "content": chunk,
            "embedding": embedding
        }).execute()


# -----------------------------
# RETRIEVE
# -----------------------------
def retrieve_similar_chunks(query, top_k=5):
    query_embedding = generate_embedding(query)

    response = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "match_count": top_k
    }).execute()

    return response.data


# -----------------------------
# GENERATE ANSWER
# -----------------------------
def generate_answer(query):
    similar_docs = retrieve_similar_chunks(query)

    if not similar_docs:
        return "No relevant content found."

    context = "\n\n".join([doc["content"] for doc in similar_docs])

    prompt = f"""
Answer the question using ONLY the context below.
If answer is not in the context, say "Not in document".

Context:
{context}

Question:
{query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",  # Use what your list supports
        contents=prompt
    )

    return response.text