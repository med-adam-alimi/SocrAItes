# 🧠 AI Philosophy Chatbot

A Flask web application that allows users to engage in philosophical discussions with AI-powered philosopher personas using Retrieval Augmented Generation (RAG).

## ✨ Features

- 🎭 **Philosopher Personas**: Chat with Camus, Dostoevsky, Nietzsche, and more
- 🔍 **RAG-Powered**: Responses based on actual philosophical texts
- 💬 **Interactive Chat**: Real-time conversation interface
- 📚 **Source Citations**: See which texts influenced each response
- 🎯 **Topic Suggestions**: Get philosophical discussion starters
- 🎨 **Beautiful UI**: Modern, responsive web interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd SocrAItes
   ```

2. **Set up virtual environment** (already configured)
   ```bash
   # Virtual environment is already created at .venv/
   ```

3. **Install dependencies** (already done)
   ```bash
   # Dependencies are already installed
   ```

4. **Configure environment**
   ```bash
   # Edit .env file and add your OpenAI API key:
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Initialize data** (already done)
   ```bash
   # Data has been prepared and embeddings created
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Open in browser**
   Visit `http://localhost:5000` to start chatting with philosophers!

## 🧪 Testing

Run the test suite to verify everything is working:
```bash
python tests/test_setup.py
```

## 📊 Current Status

✅ **Completed:**
- Project structure and Flask app setup
- RAG engine with FAISS vector database
- Sample philosophical texts and embeddings
- Responsive web interface
- Philosopher persona system
- Chat functionality (backend ready)

⚠️ **Needs:**
- OpenAI API key for full functionality
- Additional philosophical texts for richer conversations

## 💭 Available Philosophers

- **Albert Camus** - Existentialism and Absurdism
- **Fyodor Dostoevsky** - Psychology and Human Nature  
- **Friedrich Nietzsche** - Will to Power and Critique of Morality
- **Philosophy Guide** - Neutral philosophical discussion

## 🛣️ Development Roadmap

### Week 1: ✅ COMPLETED
- [x] Project setup and structure
- [x] Flask application framework
- [x] RAG pipeline with FAISS
- [x] Basic web interface
- [x] Sample philosophical texts
- [x] Embedding creation and testing

### Week 2: 📋 TODO
- [ ] Add OpenAI API integration
- [ ] Enhance philosopher personas
- [ ] Improve conversation memory
- [ ] Add more philosophical texts
- [ ] Implement conversation export

### Week 3: 📋 TODO  
- [ ] UI/UX improvements
- [ ] Add conversation history
- [ ] Multi-philosopher debates
- [ ] Topic recommendation engine
- [ ] Mobile responsiveness

### Week 4: 📋 TODO
- [ ] Deployment configuration
- [ ] Performance optimization
- [ ] Documentation and demos
- [ ] User testing and feedback
- [ ] Production deployment

## 🔧 Technical Architecture

```
AI Philosophy Chatbot
├── Frontend (HTML/CSS/JS)
│   ├── Chat interface
│   ├── Philosopher selection
│   └── Topic suggestions
├── Backend (Flask/Python)
│   ├── API endpoints
│   ├── Session management
│   └── Error handling
├── RAG Engine
│   ├── FAISS vector database
│   ├── Sentence transformers
│   └── Context retrieval
├── AI Integration
│   ├── OpenAI GPT models
│   ├── Persona prompts
│   └── Response generation
└── Data Pipeline
    ├── Text preprocessing
    ├── Chunking strategy
    └── Embedding creation
```

## 🎯 Next Steps

1. **Add your OpenAI API key** to `.env` file:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

2. **Test the full functionality**:
   ```bash
   python run.py
   # Open http://localhost:5000 and try chatting
   ```

3. **Add more philosophical texts** to `data/raw/` and re-run:
   ```bash
   python scripts/prepare_data.py
   ```

## 🤝 Contributing

Ideas for expansion:
- Add more philosophers (Aristotle, Kant, Wittgenstein)
- Implement argument mapping visualization
- Add conversation analytics
- Create mobile app version
- Add voice interaction

## 📜 License

MIT License - see LICENSE file for details.

---

**Ready to explore the depths of human thought with AI? Start your philosophical journey today! 🌟**
