import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Configure your API Key
os.environ["GOOGLE_API_KEY"] = "xxxxx"

def ingest_plans(plan_files):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    all_chunks = []

    for file_path, plan_id in plan_files.items():
        print(f"Processing {file_path} for {plan_id}...")
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        # Split text into chunks and tag them with the plan_id
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(pages)
        for chunk in chunks:
            chunk.metadata["plan_id"] = plan_id
        
        all_chunks.extend(chunks)

    # Create and save the FAISS index locally
    vector_store = FAISS.from_documents(all_chunks, embeddings)
    vector_store.save_local("faiss_index")
    print("FAISS index created and saved to 'faiss_index' folder.")

if __name__ == "__main__":
    plans = {
        "PlanSponsor_A.pdf": "Sponsor_A",
        "PlanSponsor_B.pdf": "Sponsor_B"
    }
    ingest_plans(plans)