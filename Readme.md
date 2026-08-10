# ⚖️ LexAI - Legal Research Assistant (RAG Based)

LexAI is an AI-powered legal research assistant built using **Retrieval Augmented Generation (RAG)**.  
It allows users to ask questions related to Indian laws, legal acts, and uploaded legal documents.

The system uses a custom legal knowledge base with FAISS vector search and an LLM-based reasoning layer to generate accurate answers from retrieved legal context.

---

## 🚀 Features

- 📚 Legal Knowledge Base containing Indian Acts and Documents
- 🔎 Semantic search using FAISS Vector Database
- 🤖 LLM-based answer generation
- 📄 User PDF upload and temporary indexing
- 🌐 Web search support for recent legal updates/judgements
- 💬 Interactive Streamlit Chat Interface
- ⚡ Fast document retrieval using embeddings

---

## 🏗️ Project Architecture


User
|
| Question
↓
Streamlit UI
|
↓
RAG Pipeline
|
├── Retriever
| |
| ↓
| FAISS Vector Database
|
├── Web Search Agent
|
↓
Reasoning Model
|
↓
Final Answer


---

## 📂 Project Structure


LexAI/

│── app.py # Streamlit UI
│── requirements.txt # Dependencies
│── .env # API Keys

│
├── data/
│ ├── legal_docs # Permanent legal knowledge base PDFs
│ └── User_upload_pdfs # User uploaded PDFs
│
├── models/
│ ├── embedding.py # Embedding generation
│ ├── extraction.py # PDF extraction utilities
│ └── reasoning.py # LLM reasoning model
│
├── rag/
│ ├── pipeline.py # Main RAG pipeline
│ ├── retriever.py # FAISS retrieval logic
│ └── vector_store.py # Vector database creation
│
├── utils/
│ ├── pdf_loader.py # PDF text extraction
│ ├── chunking.py # Text chunk creation
│ └── web_search.py # Web search integration
│
└── vector_db/
├── index.faiss # FAISS index
└── chunks.pkl # Stored text chunks
🔄 Working Flow
Legal PDFs are loaded from the knowledge base.
Documents are extracted and divided into chunks.
Text chunks are converted into embeddings.
Embeddings are stored in FAISS vector database.
User query is converted into embedding.
Relevant legal context is retrieved.
LLM generates the final response using retrieved context.
🧠 Technologies Used
Python
Streamlit
LangChain Concepts
FAISS
HuggingFace Embeddings
Large Language Models
PyMuPDF
Tavily Search API
📌 Future Improvements
Multi-user document sessions
Conversation memory
Citation generation
Better legal document ranking
Cloud deployment
👨‍💻 Author

Mohd Ishan Khan


