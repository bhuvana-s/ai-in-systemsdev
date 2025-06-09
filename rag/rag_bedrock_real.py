#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) implementation using Amazon Bedrock and Claude 3 Sonnet.
This script demonstrates a simple RAG system that:
1. Downloads a PDF document about EU data protection and privacy
2. Extracts and chunks the text
3. Creates a vector store using TF-IDF
4. Retrieves relevant chunks based on user queries
5. Generates answers using Amazon Bedrock's Claude 3 Sonnet model

Usage:
  - Run without arguments for interactive mode: python rag_bedrock_real.py
  - Run with a question: python rag_bedrock_real.py "What are the main privacy concerns in the EU?"
"""

import os
import sys
import json
import requests
import tempfile
import boto3
from PyPDF2 import PdfReader
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Constants
# URL of the PDF document to be used as the knowledge base
PDF_URL = "https://fra.europa.eu/sites/default/files/fra_uploads/fra-2020-fundamental-rights-survey-data-protection-privacy_en.pdf"
# Amazon Bedrock model identifier for Claude 3 Sonnet
BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"  # Claude 3 Sonnet
# AWS region for Bedrock API calls
REGION = "us-east-1"  # Change to your preferred region

def download_pdf(url, output_path):
    """
    Download a PDF document from a specified URL and save it to the given path.
    
    Args:
        url (str): The URL of the PDF document to download
        output_path (str): The local file path where the PDF will be saved
        
    Returns:
        str: The path where the PDF was saved
    """
    print(f"Downloading PDF from {url}...")
    response = requests.get(url)
    with open(output_path, 'wb') as f:
        f.write(response.content)
    return output_path

def extract_text_from_pdf(pdf_path):
    """
    Extract all text content from a PDF document.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content from all pages of the PDF
    """
    print("Extracting text from PDF...")
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def split_into_chunks(text, chunk_size=1000):
    """
    Split the extracted text into smaller chunks for processing.
    Uses a simple word-based approach to maintain context within chunks.
    
    Args:
        text (str): The full text to be split
        chunk_size (int, optional): Maximum character count per chunk. Defaults to 1000.
        
    Returns:
        list: List of text chunks, each approximately chunk_size characters
    """
    print("Splitting text into chunks...")
    
    # Simple splitting by character count
    words = text.split()
    chunks = []
    current_chunk = ""
    
    for word in words:
        if len(current_chunk) + len(word) + 1 <= chunk_size:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "
    
    # Add the last chunk if it contains any text
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def create_vector_store(chunks):
    """
    Create a simple vector store using TF-IDF vectorization.
    
    This function converts text chunks into numerical vectors using Term Frequency-Inverse 
    Document Frequency (TF-IDF) vectorization, which helps measure the importance of words
    in each chunk relative to the entire corpus.
    
    Args:
        chunks (list): List of text chunks to vectorize
        
    Returns:
        tuple: (vectorizer, vectors, chunks)
            - vectorizer: The fitted TF-IDF vectorizer
            - vectors: The sparse matrix of TF-IDF vectors
            - chunks: The original text chunks
    """
    print("Creating vector store...")
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(chunks)
    return vectorizer, vectors, chunks

def retrieve_relevant_chunks(query, vectorizer, vectors, chunks, k=3):
    """
    Retrieve the most relevant chunks for a given query using cosine similarity.
    
    Args:
        query (str): The user's question or query
        vectorizer: The fitted TF-IDF vectorizer
        vectors: The sparse matrix of TF-IDF vectors for all chunks
        chunks (list): The original text chunks
        k (int, optional): Number of top chunks to retrieve. Defaults to 3.
        
    Returns:
        list: The k most relevant text chunks for the query
    """
    # Transform the query into the same vector space as the chunks
    query_vector = vectorizer.transform([query])
    # Calculate cosine similarity between query and all chunks
    similarities = cosine_similarity(query_vector, vectors)[0]
    # Get indices of top k most similar chunks
    top_k_indices = similarities.argsort()[-k:][::-1]
    return [chunks[i] for i in top_k_indices]

def get_bedrock_response(query, context):
    """
    Generate a response to the user's query using Amazon Bedrock's Claude model.
    
    This function:
    1. Creates a prompt that includes relevant context chunks and the user's question
    2. Sends the prompt to Amazon Bedrock's Claude 3 Sonnet model
    3. Processes and returns the model's response
    
    Args:
        query (str): The user's question
        context (list): List of relevant text chunks to provide as context
        
    Returns:
        str: The generated answer from Claude
    """
    print("Generating answer using Amazon Bedrock...")
    
    # Initialize Bedrock client
    bedrock_client = boto3.client('bedrock-runtime', region_name=REGION)
    
    # Prepare prompt with context by joining all context chunks
    context_text = "\n\n".join(context)
    prompt = f"""You are an AI assistant helping with questions about EU data protection and privacy.
Based on the following document excerpts, please answer the question.

Document excerpts:
{context_text}

Question: {query}

Answer:"""
    
    # Prepare request for Claude with appropriate parameters
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7  # Controls randomness: lower is more deterministic
    }
    
    # Invoke Bedrock model and handle the response
    try:
        response = bedrock_client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body)
        )
        response_body = json.loads(response['body'].read().decode('utf-8'))
        return response_body['content'][0]['text']
    except Exception as e:
        print(f"Error calling Bedrock: {str(e)}")
        return f"Error generating response: {str(e)}"

def main():
    """
    Main function that orchestrates the RAG workflow:
    1. Determines if running in interactive or single-question mode
    2. Downloads and processes the PDF document
    3. Creates the vector store
    4. Handles user questions and generates answers
    """
    # Check if a question was provided as a command-line argument
    if len(sys.argv) > 1:
        question = ' '.join(sys.argv[1:])
        interactive = False
    else:
        interactive = True
    
    # Download PDF to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        pdf_path = temp_file.name
    
    download_pdf(PDF_URL, pdf_path)
    
    # Process document: extract text, split into chunks, and create vector store
    text = extract_text_from_pdf(pdf_path)
    chunks = split_into_chunks(text)
    vectorizer, vectors, chunks = create_vector_store(chunks)
    
    if interactive:
        # Interactive Q&A mode - continuously prompt for questions
        print("\nRAG system ready! Ask questions about the EU data protection and privacy document.")
        print("Type 'exit' to quit.\n")
        
        while True:
            question = input("Your question: ")
            if question.lower() == 'exit':
                break
            
            # Retrieve relevant chunks based on the question
            relevant_chunks = retrieve_relevant_chunks(question, vectorizer, vectors, chunks)
            
            # Generate answer using Bedrock with the retrieved context
            answer = get_bedrock_response(question, relevant_chunks)
            print(f"\nAnswer: {answer}\n")
    else:
        # Single question mode - process the question provided as command-line argument
        # Retrieve relevant chunks
        relevant_chunks = retrieve_relevant_chunks(question, vectorizer, vectors, chunks)
        
        # Generate answer using Bedrock
        answer = get_bedrock_response(question, relevant_chunks)
        print(f"\nQuestion: {question}")
        print(f"Answer: {answer}\n")
    
    # Clean up by removing the temporary PDF file
    os.unlink(pdf_path)

if __name__ == "__main__":
    main()
