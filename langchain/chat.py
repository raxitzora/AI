from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# same embedding model used during indexing
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# connect to existing Qdrant collection
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="cybersecurity_rag"
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.3
)

print("\nCybersecurity PDF Chat Ready\n")



while True:
    question = input("You: ")

    if question.lower() in ["exit", "quit"]:
        break

    # retrieve relevant docs
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer clearly:
"""

    response = llm.invoke(prompt)

    print("\nAI:", response.content, "\n")