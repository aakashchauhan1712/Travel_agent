from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()


from loader import load_travel_guidelines


def create_vector_store():

    # Load chunks
    chunks = load_travel_guidelines(
        r"C:\Users\Akash\Videos\Travel Agent\data\travel_guideline.txt"
    )

    # Embedding Model
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Create FAISS Index
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    # Save locally
    vector_store.save_local(
        "faiss_index"
    )

    print("Vector Store Created Successfully!")

if __name__ == "__main__":
    create_vector_store()