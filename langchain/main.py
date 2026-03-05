from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
load_dotenv()
import os
print("KEY:", os.getenv("GOOGLE_API_KEY"))


pdf_path = Path(__file__).parent / "CYBERSECURITY.pdf"


#Load file

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()


#Split file into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)

chuncks = text_splitter.split_documents(documents=docs)


##Vector embedding 
embedding_model = HuggingFaceEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2"
)
vector_store = QdrantVectorStore.from_documents(
    documents=chuncks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="cybersecurity_rag"
)

print("Indexing of documents is done...")