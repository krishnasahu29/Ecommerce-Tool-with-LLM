# 🏠 ECommerce Tool with LLM

This project is an **AI-powered analytics and insights tool** that leverages **Large Language Models (LLMs) via Groq** to analyze, summarize, and generate insights from women's footwear data scraped from **Flipkart**. It helps e-commerce teams, sellers, and analysts understand product trends, pricing, sentiment, and competitive landscape.

---

## 🚀 Features

- 🔍 **Web Scraping**: Collects live product data (title, price, brand, rating, reviews) from Flipkart women's shoes category.
- 🧠 **LLM-Powered Insights**: Uses Groq-hosted LLMs to generate insights like:
  - Popular brands
  - Price range distribution
  - Top-rated products
  - Summary of customer sentiment
- 📊 **Interactive Reports**: Outputs insights in clean markdown, JSON, or optional HTML dashboard.
- 🛠️ **Extensible**: Easily extendable to other categories like men's shoes, clothing, electronics, etc.

---

## 🛠️ Technology Stack

Frontend: Streamlit AI Framework: LangChain Vector Database: Chroma LLM: Groq/Llama Embeddings: Sentence Transformers Data Sources: CSV Files through Web Scraping Backend: Python, FastAPI (optional)

## 📋 Prerequisites

Python 3.8+ Groq API key (or other LLM provider) Real estate URLs Git

## 🔧 Installation

Clone the repository

bashgit clone https://github.com/krishnasahu29/Ecommerce-Tool-with-LLM

Create virtual environment

bashpython -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate

Install dependencies

bashpip install -r requirements.txt

Set up environment variables

bashcp .env.example .env

Edit .env with your API keys and configuration
Initialize vector database

bashpython scripts/setup_vectordb.py

## ⚙️ Configuration

Create a .env file with the following variables: envOPENAI_API_KEY=your_openai_api_key STREAMLIT_SERVER_PORT=8501 VECTOR_DB_PATH=./data/vectordb REAL_ESTATE_API_KEY=your_real_estate_api_key EMBEDDING_MODEL=all-MiniLM-L6-v2 LLM_MODEL=llama-3.3-70b-versatile

## 🚀 Usage

Start the Streamlit application

bashstreamlit run app.py

Access the application Open your browser and navigate to http://localhost:8501 Upload URLs

## 🤖 RAG Implementation Details

Document Processing Pipeline

Document Ingestion: URLs Text Chunking: Semantic chunking with overlap for context preservation Embedding Generation: Convert text chunks to vector embeddings Vector Storage: Store embeddings in vector database with metadata

Retrieval Strategy

Semantic Search: Find most relevant documents using cosine similarity Hybrid Search: Combine semantic and keyword-based search Re-ranking: Post-retrieval re-ranking for improved relevance Context Window Management: Optimize retrieved context for LLM input

Generation Enhancement

Prompt Engineering: Specialized prompts for real estate domain Context Integration: Seamlessly blend retrieved information with user queries Source Attribution: Track and display information sources Hallucination Mitigation: Grounding responses in retrieved documents

## 📁 Project Structure

ecommerce-tool/
│
├── app/                           # Streamlit UI and app logic
│   ├── __pycache__/
│   ├── db.sqlite
│   ├── main.py                    # Streamlit chat interface (LLM-powered)
│   ├── router.py                  # Route logic (if needed for modularity)
│   ├── sql.py                     # DB queries for products
│   ├── faq.py                     # Optional FAQ bot logic
│   ├── resources/                 # Logos, images, icons
│       ├── ecommerce_data_final.csv   # Finalized scraped data
│       ├── faq_data.csv               # Few faq questions fed to the chatbot
│       ├── architecture-diagram.png   # Architecture for the project
│       └── product-ss.png             # Screenshot of the Frontend
│
├── data/                          # Structured product datasets
│   ├── flipkart_product_data.csv
│   ├── flipkart_product_links.csv
│   ├── unavailable_products.csv
│   ├── flipkart_data_extraction.ipynb
│   ├── duplicate_products.csv
│   └── csv_to_sqlite.py          # Convert CSV → SQLite
│
├── requirements.txt               # Python dependencies
└── README.md                      # Project overview

## 📈 Example Output

![image](https://github.com/user-attachments/assets/c935d369-3b53-4411-b347-3efec4bd8280)


## 🤝 Contributing

Fork the repository Create a feature branch (git checkout -b feature/amazing-feature) Commit your changes (git commit -m 'Add amazing feature') Push to the branch (git push origin feature/amazing-feature) Open a Pull Request

## 🙏 Acknowledgments

Groq for providing powerful language models Streamlit team for the excellent web framework LangChain/LlamaIndex communities for RAG tools Real estate data providers and APIs

## 📞 Support 

If you have any questions or need support, please reach out on: GitHub: @krishnasahu29 LinkedIn: www.linkedin.com/in/krishnasahu29 Email: krishna.sahu.work222@gmail.com

