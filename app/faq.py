import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

faqs_path = Path(__file__).parent / 'resources/faq_data.csv'
client = chromadb.Client()
collection_name = 'faqs'
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
groq_client = Groq()

def ingest_faq_data(file_path: str):
    """
    Load FAQ data from a CSV file into a pandas DataFrame.
    
    Args:
        file_path (str): The path to the CSV file containing FAQ data.
        
    Returns:
    """
    if collection_name not in client.list_collections():
        print("Ingesting FAQ data...")
        collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=ef
        )

        df = pd.read_csv(faqs_path)
        docs = df['question'].tolist()
        metadata = [{'answer': ans} for ans in df['answer'].tolist()]
        ids = [f"id_{i}" for i in range(len(docs))]

        collection.add(
            documents=docs,
            metadatas=metadata,
            ids=ids
        )

        print(f"Added {len(docs)} FAQs to the collection '{collection_name}'")
    
    else:
        print(f"Collection '{collection_name}' already exists!")

def get_relevant_qa(query: str) -> dict:
    """
    Retrieve relevant FAQs based on a query.
    
    Args:
        query (str): The query string to search for relevant FAQs.
    
    Returns:
        dict: A dictionary containing the results of the query.
    """
    collection = client.get_collection(name=collection_name)
    return collection.query(
        query_texts=[query],
        n_results=2
    )

def faq_chain(query: str) -> str:
    """
    Process the query and return the answer from the FAQ collection.
    
    Args:
        query (str): The query string to search for an answer.
    
    Returns:
        str: The answer to the query.
    """
    result = get_relevant_qa(query)
    context = ''.join(r.get('answer') for r in result['metadatas'][0])
    answer = generate_answer(query, context)
    return answer

def generate_answer(query: str, context: str) -> str:

    prompt = f"""
    Given the question and context below, answer the question based on context only.
    Don't reply as We don't know, just start the answer
    If you don't know the answer, say "I don't know".
    Give response in we, not you.
    Do not make up an answer.
    
    Question: {query}

    Context: {context}
    """

    #call LLM to generate the answer
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ],
        model = os.environ['GROQ_MODEL'],
    )

    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    ingest_faq_data(faqs_path)
    query = input("Enter your query: ")
    # results = get_relevant_qa(query)
    answer = faq_chain(query)
    print(answer)
