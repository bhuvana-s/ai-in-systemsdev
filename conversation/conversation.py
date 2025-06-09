"""
conversation.py - AWS Bedrock Conversation System

This script demonstrates how to interact with AWS Bedrock's Claude LLM model
to have simple conversations. It provides a basic menu-driven interface for
asking predefined questions to the LLM.

Requirements:
- AWS account with Bedrock access
- Appropriate IAM permissions for Bedrock
- boto3 library installed
- Access granted to the Claude model in AWS Bedrock console
"""

import boto3
import json

# Initialize AWS Bedrock client
# This creates a connection to the AWS Bedrock service in the us-east-1 region
# Make sure your AWS credentials are properly configured with Bedrock access
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def conversation_with_llm(query):
    """
    Send a query to AWS Bedrock's Claude LLM and get a response.
    
    Args:
        query (str): The user's question or prompt to send to the LLM
        
    Returns:
        None: Prints the LLM's response to the console
    """
    # Display the query being sent to the LLM
    print(f"Asking: {query}")
    user_input = query
    
    # Call AWS Bedrock for LLM response using Claude model
    try:
        # Prepare the payload for the Bedrock API call
        # This follows the Claude API format required by Bedrock
        bedrock_payload = {
            "anthropic_version": "bedrock-2023-05-31",  # API version for Claude
            "max_tokens": 1000,                         # Maximum response length
            "messages": [
                {
                    "role": "user",                     # Message is from the user
                    "content": user_input               # The actual query text
                }
            ]
        }
        
        # Make the API call to the Bedrock service
        bedrock_response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',  # Claude 3 Sonnet model
            body=json.dumps(bedrock_payload)                    # Convert payload to JSON string
        )
        
        # Parse the response from Bedrock
        response_body = json.loads(bedrock_response['body'].read().decode('utf-8'))
        llm_reply = response_body['content'][0]['text']  # Extract the text response
        
    except Exception as e:
        # Handle any errors that occur during the API call
        print(f"Error calling Bedrock: {e}")
        llm_reply = "Sorry, I couldn't retrieve the information at this time."

    # Display the LLM's response
    print(f"LLM Response: {llm_reply}")

# Main program execution block
if __name__ == "__main__":
    # Display welcome message and menu options
    print("Welcome to the conversation system")
    print("1. Ask about S3 bucket")
    print("2. Ask who is the founder of Amazon")
    print("3. Exit")
    
    # Get user's menu choice
    choice = input("Enter your choice (1-3): ")
    
    # Process the user's choice
    if choice == "1":
        conversation_with_llm("What is S3 bucket?")  # Query about AWS S3
    elif choice == "2":
        conversation_with_llm("Who is the founder of Amazon?")  # Query about Amazon's founder
    elif choice == "3":
        print("Exiting the program. Goodbye!")  # Exit the program
    else:
        print("Invalid choice. Please try again.")  # Handle invalid input
