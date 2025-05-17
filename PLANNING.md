# Agentic RAG Support Agent for Asset Management Platform

## Overview

This project aims to develop an agentic Retrieval Augmented Generation (RAG) model that serves as a support agent for a company's asset management platform. The agent will be integrated within the platform via a chat window interface, allowing users to interact with it directly.

The system will be architected with an orchestration agent that has access to specialized product-level expert tools, with each tool possessing comprehensive knowledge about specific products (both the main platform and integrated third-party solutions like Starlink).

## Goals

1. Create an AI assistant that can accurately answer user queries about the asset management platform and its integrated products
2. Implement a modular architecture with specialized expert tools for different product domains
3. Enable the system to intelligently route queries to the appropriate expert tool
4. Provide contextually relevant and accurate responses based on the knowledge base
5. Allow flexibility in embedding and LLM model selection to optimize for performance and cost

## Technology Stack

### Core Components

- **Python 3**: Primary programming language for developing the solution
- **Crawl4AI**: Open-source web crawler for gathering and processing structured data from product documentation, knowledge bases, and relevant websites
- **Pydantic**: For data validation, schema definition, and structured output formatting
- **Supabase**: Backend database for storing vector embeddings and other related data
- **LLM Models**: Flexible architecture to support different LLM providers (specific models to be determined)
- **Embedding Models**: Multiple options for generating embeddings (specific models to be determined)

### Architecture

The system will follow an orchestrator pattern with specialized tools:

1. **Orchestration Agent**:

   - Central controller for routing queries
   - Responsible for query understanding and determining which expert tool to engage
   - Manages conversation flow and follows up as needed

2. **Expert Tools**:

   - Product-specific knowledge experts (e.g., platform expert, Starlink expert)
   - Each tool has access to relevant knowledge bases through vector search
   - Can perform specialized reasoning and answer domain-specific questions

3. **RAG Implementation**:

   - Document crawling and preprocessing with Crawl4AI
   - Vector database storage in Supabase
   - Contextual retrieval preprocessing
   - Embedding generation and similarity search
   - Retrieval-enhanced responses
   - Re-ranking of retrieved documents

4. **Knowledge Base Management**:
   - Regular updates to keep information current
   - Quality assurance for accuracy
   - Version control for knowledge base content

## Development Phases

### Phase 1: Foundation

- Set up development environment
- Implement basic RAG functionality with a single knowledge source
- Create initial schema and database structure
- Establish crawler integration for document processing

### Phase 2: Modular Architecture

- Develop the orchestration agent
- Create specialized expert tools for different product domains
- Implement routing logic for query delegation

### Phase 3: Testing and Optimization

- Performance testing with different embedding and LLM models
- Optimize for accuracy, latency, and cost
- User acceptance testing

### Phase 4: Integration and Deployment

- Integrate with the asset management platform
- Implement user interface (chat window)
- Deploy to production environment

## Metrics for Success

- Response accuracy: >90% correct answers
- Response time: <3 seconds for typical queries
- User satisfaction: >85% positive feedback
- Coverage: Ability to address >95% of common support queries

## Considerations

- **Security**: Ensure data privacy and security measures are implemented
- **Scalability**: Design to handle increasing knowledge base size and user load
- **Maintainability**: Create a system that can be easily updated as products evolve
- **Cost Optimization**: Balance between performance and operational costs
