import re
from io import BytesIO
from typing import Tuple, List
import os
import warnings

# Disable ChromaDB telemetry to prevent errors
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Suppress PDF warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pypdf")

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pypdf import PdfReader


def parse_pdf(file: BytesIO, filename: str) -> Tuple[List[str], str]:
    # Use strict=False to handle corrupted/malformed PDFs
    pdf = PdfReader(file, strict=False)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
            text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
            text = re.sub(r"\n\s*\n", "\n\n", text)
            output.append(text)
    return output, filename


def text_to_docs(text: List[str], filename: str) -> List[Document]:
    if isinstance(text, str):
        text = [text]
    page_docs = [Document(page_content=page) for page in text if page]
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1

    doc_chunks = []
    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=0,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
            )
            doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc.metadata["filename"] = filename
            doc_chunks.append(doc)
    return doc_chunks


def docs_to_index(docs, gemini_api_key=None):
    """Create Chroma vector store from documents using HuggingFace embeddings."""
    # Use HuggingFace embeddings with explicit CPU device
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Create Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    return vectorstore


def get_index_for_pdf(pdf_files, pdf_names, gemini_api_key):
    documents = []
    failed_pdfs = []
    
    for pdf_file, pdf_name in zip(pdf_files, pdf_names):
        try:
            text, filename = parse_pdf(BytesIO(pdf_file), pdf_name)
            if text:  # Only add if we got some text
                documents = documents + text_to_docs(text, filename)
            else:
                failed_pdfs.append(pdf_name)
        except Exception as e:
            print(f"  ⚠️ Skipping {pdf_name}: {str(e)}")
            failed_pdfs.append(pdf_name)
    
    if not documents:
        raise Exception(f"No valid documents could be parsed from {len(pdf_files)} PDFs")
    
    if failed_pdfs:
        print(f"  ℹ️ Successfully parsed {len(pdf_files) - len(failed_pdfs)}/{len(pdf_files)} PDFs")
    
    index = docs_to_index(documents, gemini_api_key)
    return index
