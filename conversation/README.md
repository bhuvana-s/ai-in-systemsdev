# Conversation with AWS Bedrock LLM

This script demonstrates how to interact with AWS Bedrock's Claude LLM model to have simple conversations.

## Prerequisites

1. **Python 3.11+** - This project is built with Python 3.11.12
2. **AWS Account** - You need an active AWS account with access to AWS Bedrock
3. **AWS CLI configured** - With appropriate permissions for Bedrock
4. **Required Python packages**:
   - boto3

## Setup Instructions

1. **Set up a virtual environment**:
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

2. **Install required packages**:
   ```bash
   pip install boto3
   ```

3. **Configure AWS credentials**:
   Make sure your AWS credentials are properly configured with access to Bedrock.
   ```bash
   aws configure
   ```
   
   You'll need to provide:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region name (e.g., us-east-1)
   - Default output format (json)

4. **Enable AWS Bedrock model access**:
   - Go to the AWS Bedrock console
   - Navigate to "Model access"
   - Request access to the Anthropic Claude model (anthropic.claude-3-sonnet-20240229-v1:0)

## Running the Script

To run the conversation script:

```bash
python conversation.py
```

The script will present a simple menu with options:
1. Ask about S3 bucket
2. Ask who is the founder of Amazon
3. Exit

Select an option by entering the corresponding number.

## Customizing the Script

You can modify the script to:
- Add more conversation options
- Change the model being used
- Adjust the maximum token output
- Implement a continuous conversation loop

## Troubleshooting

If you encounter errors:

1. **Authentication issues**: Verify your AWS credentials are correctly configured
2. **Access denied**: Ensure you have requested and been granted access to the Claude model in AWS Bedrock
3. **Region issues**: Make sure you're using a region where AWS Bedrock is available
4. **Quota limits**: Check if you've hit your AWS Bedrock quota limits
