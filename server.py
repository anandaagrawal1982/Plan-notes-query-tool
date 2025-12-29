from fastmcp import FastMCP
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

mcp = FastMCP("PlanSponsorAssistant")
os.environ["GOOGLE_API_KEY"] = "xxxx"

@mcp.tool()
def query_benefits(plan_id: str, question: str) -> str:
    """Queries the benefit document for a specific plan sponsor."""
    print("MCP Tool called: ", plan_id)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Load the local FAISS index
    vector_store = FAISS.load_local(
        "faiss_index", 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    # Retrieve top 5 results to ensure we have enough after filtering
    docs = vector_store.similarity_search(question, k=5)
    
    # Filter for the specific plan_id provided
    relevant_context = [
        d.page_content for d in docs if d.metadata.get("plan_id") == plan_id
    ]
    
    if not relevant_context:
        return f"No specific information found for {plan_id}."

    return "\n---\n".join(relevant_context)

if __name__ == "__main__":
    mcp.run()