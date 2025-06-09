# RAG with Amazon Bedrock and Claude 3 Sonnet

This project demonstrates a simple Retrieval-Augmented Generation (RAG) system using Amazon Bedrock's Claude 3 Sonnet model. The system downloads a PDF document about EU data protection and privacy, processes it, and allows users to ask questions about the content.

## Features

- Downloads and processes a PDF document about EU data protection
- Extracts and chunks text from the PDF
- Creates a vector store using TF-IDF for semantic search
- Retrieves relevant document chunks based on user queries
- Generates answers using Amazon Bedrock's Claude 3 Sonnet model

## Prerequisites

- Python 3.8+
- AWS account with access to Amazon Bedrock
- AWS CLI configured with appropriate credentials
- Access to Claude 3 Sonnet model in Amazon Bedrock

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd rag
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure your AWS credentials are properly configured:
   ```
   aws configure
   ```

## Usage

### Interactive Mode

Run the script without arguments to enter interactive mode:

```
python rag_bedrock_real.py
```

In interactive mode, you can ask multiple questions about the EU data protection and privacy document. Type 'exit' to quit.

### Single Question Mode

Run the script with your question as an argument:

```
python rag_bedrock_real.py "What are the main privacy concerns in the EU?"
```

## How It Works

1. **Document Processing**:
   - Downloads a PDF document from a specified URL
   - Extracts text content from the PDF
   - Splits the text into manageable chunks

2. **Vector Store Creation**:
   - Creates a TF-IDF vector representation of each text chunk
   - Enables semantic search over the document content

3. **Query Processing**:
   - Converts user questions into the same vector space
   - Retrieves the most relevant chunks using cosine similarity

4. **Answer Generation**:
   - Sends the user question and relevant context to Claude 3 Sonnet
   - Returns the generated answer

## Configuration

You can modify the following constants in the script:

- `PDF_URL`: URL of the PDF document to use as knowledge base
- `BEDROCK_MODEL_ID`: Amazon Bedrock model identifier
- `REGION`: AWS region for Bedrock API calls

## Notes

- The script uses a simple TF-IDF vectorization approach for demonstration purposes
- For production use, consider using more advanced embedding models
- The temporary PDF file is automatically cleaned up after execution
