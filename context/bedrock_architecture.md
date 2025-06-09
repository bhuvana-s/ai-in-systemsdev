# AWS Architecture for Bedrock Product Assistant

## Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  User / CLI     │────▶│  Product        │────▶│  AWS Bedrock    │
│  Interface      │     │  Assistant      │     │  Runtime        │
│                 │     │  Python Script  │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │                       │
                                 │                       │
                                 │                       ▼
                                 │              ┌─────────────────┐
                                 │              │                 │
                                 │              │  Foundation     │
                                 │              │  Models         │
                                 │              │  (Claude)       │
                                 │              │                 │
                                 ▼              └─────────────────┘
                        ┌─────────────────┐
                        │                 │
                        │  Product        │
                        │  Database       │
                        │  (In-Memory)    │
                        │                 │
                        └─────────────────┘
```

## Component Description

### User / CLI Interface
- Accepts command-line arguments: product ID, question, model ID, and region
- Displays formatted responses to the user
- Handles error messages and exit codes

### Product Assistant Python Script
- Core application logic
- Manages product data retrieval
- Formats prompts for the AI model
- Processes responses from Bedrock
- Handles exceptions and error conditions

### Product Database (In-Memory)
- Stores product specifications (model, name, ports, processor, etc.)
- In a production environment, this would be replaced with a real database service like DynamoDB or RDS

### AWS Bedrock Runtime
- AWS service that provides API access to foundation models
- Handles authentication and authorization
- Processes requests and manages model invocation

### Foundation Models
- AI models like Claude 3 Sonnet that generate responses
- Process natural language prompts and generate contextually relevant answers

## Data Flow

1. User provides product ID and question via command-line arguments
2. Script retrieves product specifications from the in-memory database
3. Script constructs a prompt combining product specifications and user question
4. Script calls AWS Bedrock Runtime service to invoke the specified AI model
5. AWS Bedrock authenticates the request using AWS credentials
6. The foundation model processes the prompt and generates a response
7. Response is returned to the script via AWS Bedrock Runtime
8. Script formats and displays the response to the user

## AWS Services Used

- **Amazon Bedrock**: Managed service that provides access to foundation models
- **AWS Identity and Access Management (IAM)**: Manages authentication and authorization
- **AWS SDK for Python (boto3)**: Provides programmatic access to AWS services

## Security Considerations

- AWS credentials are stored in `~/.aws/credentials`
- IAM permissions control access to specific models and regions
- Error handling prevents exposure of sensitive information

## Potential Enhancements

- Replace in-memory database with Amazon DynamoDB
- Add Amazon CloudWatch for logging and monitoring
- Implement Amazon API Gateway for RESTful API access
- Add caching with Amazon ElastiCache to improve performance
- Implement AWS Lambda for serverless deployment
