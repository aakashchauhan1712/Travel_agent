import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from rag.retriever import retrieve_context
from config import get_google_api_key

load_dotenv()


def ask_travel_guidelines(question):

    docs = retrieve_context(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=get_google_api_key()
    )

    prompt = f"""
You are a travel guidelines assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say:

"I could not find that information in the travel guidelines."

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content