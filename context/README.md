# Bedrock Product Assistant

A Python application that uses Amazon Bedrock to create an AI-powered product support assistant. This assistant answers user questions about products by fetching product specifications and using them as context for Amazon Bedrock's foundation models.

## Architecture

The application follows a simple architecture:
- Command-line interface for user interaction
- In-memory product database (simulated)
- AWS Bedrock integration for AI-powered responses
- Error handling and logging

For more details, see [bedrock_architecture.md](./bedrock_architecture.md).

## Prerequisites

- Python 3.8 or higher
- AWS account with access to Amazon Bedrock
- AWS CLI configured with appropriate credentials
- Permissions to access the Bedrock models (e.g., Claude 3)

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Ensure your AWS credentials are configured:
   ```
   aws configure
   ```

## Usage

Run the product assistant with the following command:

```
python bedrock_product_assistant.py --product-id <PRODUCT_ID> --question "<YOUR_QUESTION>"
```

### Arguments

- `--product-id`: The ID of the product to query (e.g., X123, Y456, Z789)
- `--question`: The question about the product (in quotes)
- `--model`: (Optional) The Bedrock model ID to use (default: anthropic.claude-3-sonnet-20240229-v1:0)
- `--region`: (Optional) AWS region where Bedrock is available (default: us-east-1)
- `--verbose`: (Optional) Enable verbose logging

### Example

```
python bedrock_product_assistant.py --product-id X123 --question "Does this laptop support Thunderbolt 4?"
```

## Available Products

The application includes a mock product database with the following products:

- **X123**: ProBook Ultra
- **Y456**: ThinBook Air
- **Z789**: GameMaster Pro

Each product has specifications like ports, processor, RAM, storage, etc.

## Error Handling

The application handles various error scenarios:
- Product not found
- AWS credential issues
- Bedrock service errors
- General exceptions

## License

[Specify your license here]

## Contributing

[Specify contribution guidelines if applicable]
