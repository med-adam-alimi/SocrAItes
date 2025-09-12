# AI Philosophy Chatbot Project Instructions

This is a Python Flask web application for an AI Philosophy Chatbot using RAG (Retrieval Augmented Generation).

## Project Overview
- **Framework**: Flask + Python
- **AI/ML**: OpenAI API, Hugging Face Transformers, sentence-transformers
- **Vector Database**: FAISS
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **Deployment**: Local development, can be deployed to Hugging Face Spaces

## Key Features
- Philosopher persona selection (Camus, Dostoevsky, Nietzsche, etc.)
- RAG-based responses using philosophy texts
- Real-time chat interface
- Conversation history
- Source citations

## Development Guidelines
- Use virtual environment for Python dependencies
- Follow Flask best practices for project structure
- Implement proper error handling
- Add comprehensive logging
- Include unit tests for core functionality

## Architecture
- `/app` - Flask application code
- `/data` - Philosophy texts and processed embeddings
- `/static` - CSS, JS, images
- `/templates` - HTML templates
- `/tests` - Unit tests
- `/docs` - Documentation

## Current Status
✅ Project structure created
✅ Virtual environment configured
✅ Dependencies installed
✅ RAG engine implemented
✅ Sample data prepared
✅ Web interface created
✅ Basic testing completed

## Next Steps
1. Add OpenAI API key to .env file
2. Test full chat functionality
3. Add more philosophical texts
4. Enhance UI/UX
5. Prepare for deployment
