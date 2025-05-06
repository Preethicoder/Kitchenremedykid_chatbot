from pathlib import Path
import os
from typing import List

from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
load_dotenv()
FAISS_INDEX_PATH = "faiss_index"
SEEN_URLS_PATH = Path("seen_urls.txt")
embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
text_splitter = RecursiveCharacterTextSplitter()

def load_documents_from_urls(urls: List[str]):
    """Load and split documents from a list of URLs."""
    print("🌐 Loading documents from URLs...")
    all_docs = []
    for url in urls:
        loader = WebBaseLoader(url)
        docs = loader.load()
        all_docs.extend(docs)
    return text_splitter.split_documents(all_docs)

def get_or_create_vectorstore(urls: List[str]):
    """Create or update FAISS vectorstore from provided URLs."""
    seen_urls_path = Path("seen_urls.txt")
    if seen_urls_path.exists():
        seen_urls = set(seen_urls_path.read_text().splitlines())
    else:
        seen_urls = set()

    new_urls = [url for url in urls if url not in seen_urls]
    if Path(FAISS_INDEX_PATH).exists():
        print("🔁 Loading existing FAISS index...")
        vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embedding, allow_dangerous_deserialization=True)

        # Load and add new documents
        print("new_uerl:::", new_urls)
        if new_urls:
            new_documents = load_documents_from_urls(new_urls)
            print(f"➕ Adding {len(new_documents)} new documents...")
            vectorstore.add_documents(new_documents)
            vectorstore.save_local(FAISS_INDEX_PATH)
            print("✅ FAISS index updated and saved.")
        else:
            print("No new URLs to process. FAISS index remains unchanged.")
    else:
        print("🆕 Creating new FAISS index...")
        documents = load_documents_from_urls(new_urls)
        vectorstore = FAISS.from_documents(documents, embedding)
        vectorstore.save_local(FAISS_INDEX_PATH)
        print("✅ FAISS index created and saved.")

    with open(seen_urls_path, 'a') as f:
        f.write("\n".join(new_urls) + "\n")

    return vectorstore.as_retriever()
