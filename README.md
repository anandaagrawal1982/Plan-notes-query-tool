# 🏥 Healthcare Care Manager RAG Assistant

A specialized Retrieval-Augmented Generation (RAG) system built to help care managers navigate complex health plan sponsor documents. This tool uses **Gemini 2.0 Flash**, **FastMCP**, and **FAISS** to provide accurate, plan-specific benefit information.

---

## 🛠️ Tech Stack

* **LLM:** Gemini 2.0 Flash (via Google GenAI SDK)
* **Protocol:** [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) via FastMCP
* **Vector Store:** FAISS (Facebook AI Similarity Search)
* **Frameworks:** LangChain, Streamlit
* **Embeddings:** Google `text-embedding-004` (or `models/embedding-001`)

---

## 📐 Architecture

The system follows a modular RAG architecture to ensure data isolation between different plan sponsors:



1.  **Ingest Stage:** PDFs are parsed and stored in a local FAISS index with metadata tags for each `plan_id`.
2.  **Server Stage:** A FastMCP server exposes a `query_benefits` tool.
3.  **UI Stage:** A Streamlit app gathers the patient's plan ID and query, passing them to Gemini.
4.  **Retrieval Stage:** Gemini uses the MCP tool to fetch only the text chunks matching that specific `plan_id`.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/anandaagrawal/plan-notes-query-tool.git](https://github.com/anandaagrawal/plan-notes-query-tool.git)
cd plan-notes-query-tool
