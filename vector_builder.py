import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


def load_pdf(pdf):
    file = pdf
    loader = PyPDFLoader(file)
    docs = loader.load()
    return docs


def split_pdf(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, add_start_index=True
    )
    chunks = text_splitter.split_documents(docs)
    return chunks


def embed_and_store(chunks, name):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(f"faiss_index/{name}")


def create_vector_store(pdf, name):
    loaded_pdf = load_pdf(pdf)
    chunks = split_pdf(loaded_pdf)
    embed_and_store(chunks, name)
    print("successfully created vector store")
