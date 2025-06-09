#!/usr/bin/env python3
"""
Product Support Assistant using Amazon Bedrock

This script simulates a product support assistant that answers user questions
about products by fetching product specifications and using them as context
for Amazon Bedrock's AI models.
"""

import boto3
import json
import argparse
import sys
import logging
from typing import Dict, Any, Tuple, Optional
from botocore.exceptions import ClientError, NoCredentialsError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Mock product database - in a real scenario, this would be fetched from a database
PRODUCT_DATABASE = {
    "X123": {
        "Model": "X123",
        "Name": "ProBook Ultra",
        "Ports": "2x USB-C, 1x Thunderbolt 4, HDMI",
        "Processor": "Intel Core i7-12700H",
        "RAM": "16GB DDR5",
        "Storage": "512GB NVMe SSD",
        "Display": "15.6-inch 4K OLED",
        "Graphics": "NVIDIA RTX 3060 6GB"
    },
    "Y456": {
        "Model": "Y456",
        "Name": "ThinBook Air",
        "Ports": "2x USB-C, 1x USB-A, HDMI",
        "Processor": "AMD Ryzen 7 5800U",
        "RAM": "8GB DDR4",
        "Storage": "256GB NVMe SSD",
        "Display": "13.3-inch FHD IPS",
        "Graphics": "AMD Radeon Graphics"
    },
    "Z789": {
        "Model": "Z789",
        "Name": "GameMaster Pro",
        "Ports": "3x USB-A, 1x USB-C, 1x Thunderbolt 4, HDMI, Ethernet",
        "Processor": "Intel Core i9-12900K",
        "RAM": "32GB DDR5",
        "Storage": "1TB NVMe SSD + 2TB HDD",
        "Display": "17.3-inch QHD 165Hz",
        "Graphics": "NVIDIA RTX 3080 12GB"
    }
}

class BedrockProductAssistant:
    def __init__(self, model_id="anthropic.claude-3-sonnet-20240229-v1:0", region="us-east-1"):
        """
        Initialize the Bedrock Product Assistant
        
        Args:
            model_id: The Bedrock model ID to use
            region: AWS region where Bedrock is available
        """
        self.model_id = model_id
        self.region = region
        
        # Initialize Bedrock client
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=region
        )
        logger.info(f"Successfully initialized Bedrock client in {region}")
    
    def get_product_specs(self, product_id: str) -> Dict[str, str]:
        """
        Get product specifications from the database
        
        Args:
            product_id: The product ID to look up
            
        Returns:
            Dictionary of product specifications or empty dict if not found
        """
        return PRODUCT_DATABASE.get(product_id, {})
    
    def format_specs_as_string(self, specs: Dict[str, str]) -> str:
        """
        Format product specifications as a readable string
        
        Args:
            specs: Dictionary of product specifications
            
        Returns:
            Formatted string of product specifications
        """
        if not specs:
            return "Product not found"
        
        result = []
        for key, value in specs.items():
            result.append(f"{key}: {value}")
        
        return "\n".join(result)
    
    def generate_prompt(self, product_specs: str, user_question: str) -> str:
        """
        Generate a prompt for the Bedrock model
        
        Args:
            product_specs: Formatted product specifications
            user_question: The user's question about the product
            
        Returns:
            Complete prompt for the Bedrock model
        """
        return f"""You are a helpful product support assistant. 
The user is asking about a product with the following specifications:
{product_specs}

User's question: '{user_question}'

Please answer the question accurately based on the product specifications provided.
If the information needed to answer the question is not in the specifications, 
politely state that you don't have that specific information.
"""

    def invoke_bedrock(self, prompt: str) -> str:
        """
        Invoke the Bedrock model with the given prompt
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            Response from the Bedrock model
        
        Raises:
            ClientError: If there's an AWS-specific error
            NoCredentialsError: If AWS credentials are not found
            Exception: For any other unexpected errors
        """
        # Prepare the request based on the model
        if "claude" in self.model_id.lower():
            # Claude models use a different request format
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        else:
            # Generic format for other models
            request_body = {
                "prompt": prompt,
                "max_tokens_to_sample": 1000,
                "temperature": 0.7,
                "top_p": 0.9,
            }
        
        logger.info(f"Invoking Bedrock model: {self.model_id}")
        response = self.bedrock_runtime.invoke_model(
            modelId=self.model_id,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response.get("body").read())
        
        # Extract the response based on the model
        if "claude" in self.model_id.lower():
            return response_body.get("content", [{}])[0].get("text", "No response")
        else:
            return response_body.get("completion", "No response")
    
    def answer_question(self, product_id: str, user_question: str) -> str:
        """
        Answer a user's question about a product
        
        Args:
            product_id: The product ID the user is inquiring about
            user_question: The user's question
            
        Returns:
            Response from the model
        """
        # Get product specifications
        product_specs = self.get_product_specs(product_id)
        
        if not product_specs:
            return f"I couldn't find any information about product {product_id}."
        
        # Format specifications as string
        specs_string = self.format_specs_as_string(product_specs)
        
        # Generate prompt
        prompt = self.generate_prompt(specs_string, user_question)
        
        # Get response from Bedrock
        return self.invoke_bedrock(prompt)

def main():
    """Main function to run the product assistant"""
    parser = argparse.ArgumentParser(description="Product Support Assistant using Amazon Bedrock")
    parser.add_argument("--product-id", type=str, required=True, help="Product ID to query")
    parser.add_argument("--question", type=str, required=True, help="User's question about the product")
    parser.add_argument("--model", type=str, default="anthropic.claude-3-sonnet-20240229-v1:0", 
                        help="Bedrock model ID to use")
    parser.add_argument("--region", type=str, default="us-east-1", 
                        help="AWS region where Bedrock is available")
    parser.add_argument("--verbose", action="store_true", 
                        help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Set logging level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        # Also set boto3 and botocore loggers to INFO
        logging.getLogger('boto3').setLevel(logging.INFO)
        logging.getLogger('botocore').setLevel(logging.INFO)
    
    try:
        assistant = BedrockProductAssistant(
            model_id=args.model, 
            region=args.region
        )
        
        response = assistant.answer_question(args.product_id, args.question)
        
        print("\n=== Product Assistant Response ===")
        print(response)
        print("=================================")
        print(f"Response generated by Amazon Bedrock ({assistant.model_id})")
        print()
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', str(e))
        logger.error(f"AWS error ({error_code}): {error_message}")
        print(f"Error: {error_message}")
        sys.exit(1)
        
    except NoCredentialsError:
        logger.error("No AWS credentials found")
        print("Error: No AWS credentials found.")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
