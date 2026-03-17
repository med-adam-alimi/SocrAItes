# 🧠 SocrAItes - AI Philosophy Chatbot

**Experience philosophical wisdom through AI-powered conversations with history's greatest thinkers.**

SocrAItes is a sophisticated Flask web application that combines **Retrieval Augmented Generation (RAG)** with **modern AI models** to create authentic philosophical discussions. Engage with AI-powered philosopher personas that draw from real philosophical texts and contemporary internet sources to provide thoughtful, contextually rich responses. 

## Demo Video

Watch the full demo video on Google Drive:  
[Watch Demo](https://drive.google.com/file/d/1SvIzlAV-baU0OraCNcemWy41XT9axtV4/view?usp=drive_link)


## 🏗️ Backend Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SocrAItes AI Philosophy Chatbot              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │  Flask Routes   │    │  AI Orchestrator│
│                 │    │                 │    │                 │
│ • Chat Interface│◄──►│ • /api/chat     │◄──►│ • Groq Models   │
│ • Philosopher   │    │ • /api/stream   │    │ • HuggingFace   │
│   Selection     │    │ • Static Assets │    │ • OpenAI (opt)  │
│ • Streaming UI  │    │ • Error Handler │    │ • Model Router  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │ Internet RAG    │    │ Local Knowledge │
                    │ Engine          │    │ Base            │
                    │                 │    │                 │
                    │ • Web Search    │    │ • FAISS Vector  │
                    │ • Reddit API    │    │   Database      │
                    │ • Philosophy    │    │ • Philosophy    │
                    │   Sources       │    │   Texts         │
                    │ • Stanford SEP  │    │ • Embeddings    │
                    │ • Fast Mode     │    │ • Semantic      │
                    └─────────────────┘    │   Search        │
                              │            └─────────────────┘
                              ▼                        │
                    ┌─────────────────┐                │
                    │ External APIs   │                │
                    │                 │                │
                    │ • Serper/Google │◄───────────────┘
                    │ • DuckDuckGo    │
                    │ • Reddit        │
                    │ • Phil Sources  │
                    └─────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        Data Flow                                │
│                                                                 │
│ User Query → RAG Search → Context Retrieval → AI Generation    │
│           ↓              ↓                   ↓               ↓  │
│     • Internet Sources • Local Texts     • Philosopher    • Stream │
│     • Fast Mode (3s)   • FAISS DB        • Persona       • Response │
│     • 5-8 Sources      • Embeddings      • Optimized     • Browser │
└─────────────────────────────────────────────────────────────────┘
```

## ✨ Key Features

### 🎭 **6 Authentic Philosopher Personas**
- **Albert Camus** - Existentialism, Absurdism, and the Human Condition  
- **Fyodor Dostoevsky** - Psychology, Morality, and Human Nature
- **Friedrich Nietzsche** - Will to Power, Ethics, and Cultural Critique
- **Socrates** - Classical Philosophy and the Socratic Method
- **Franz Kafka** - Existential Anxiety, Bureaucracy, and Alienation
- **Emil Cioran** - Pessimism, Nihilism, and the Human Condition

### 🔍 **Advanced RAG System**
- **Dual Knowledge Sources**: Philosophy texts + real-time internet search
- **FAISS Vector Database**: Fast semantic similarity search  
- **Intelligent Context Retrieval**: Finds relevant sources per query
- **Philosophy-Specific Sources**: Stanford Encyclopedia, IEP, Philosophy Basics
- **Fast Mode**: 2-3 second responses with optimized searches
- **Source Citations**: Transparent references for all responses

### ⚡ **Modern AI Integration**
- **Groq API**: Lightning-fast inference with Llama 3.1 8B (FREE)
- **Internet RAG**: Real-time web search for contemporary discussions
- **Multiple AI Backends**: OpenAI, Hugging Face, Ollama support
- **Streaming Responses**: ChatGPT-style real-time text generation
- **Fallback Systems**: Robust error handling and model switching

### 🎨 **ChatGPT-Style Interface**
- **Dark Modern Theme**: GitHub-inspired sophisticated design
- **Welcome Screen**: Engaging philosopher selection with animations
- **Streaming Chat**: Real-time message bubbles with progressive text
- **Responsive Design**: Perfect on desktop, tablet, and mobile
- **Session Management**: Optimized conversation history

## 🆕 Latest Improvements (September 2025)

### 🎯 **Enhanced Conversation Quality**
- **Fixed Repetitive Responses**: Eliminated annoying  repetition 
- **Improved Prompts**: More engaging and contextual responses that flow naturally

### 🧠 **Advanced RAG Engine** 
- **Academic Sources**: Stanford Encyclopedia, Internet Encyclopedia of Philosophy, PhilPapers
- **Semantic Ranking**: Context-aware source prioritization with relevance scoring
- **Contemporary Discussions**: Reddit philosophy communities and academic forums  
- **Enhanced Search**: 8 quality sources vs previous 5, with better content filtering

### 🚀 **Production-Ready Codebase**
- **Clean Architecture**: Removed all disabled/broken files and redundant code
- **Enhanced Mode**: Prioritizes response quality over speed for deeper insights
- **Better Error Handling**: Robust fallback systems and graceful degradation
- **Optimized Performance**: Streamlined search algorithms with semantic understanding

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** - Modern Python with asyncio support
- **Git** - For cloning and version control
- **4GB+ RAM** - For optimal performance with embeddings
- **Internet Connection** - For real-time RAG searches

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/med-adam-alimi/SocrAItes.git
   cd SocrAItes
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # For full internet-enabled version (recommended)
   pip install -r requirements_internet.txt
   
   # OR for safe offline version  
   pip install -r requirements_safe.txt
   ```

4. **Configure API Keys** (Optional - works without)
   ```bash
   # Create .env file
   touch .env  # Linux/Mac
   echo. > .env  # Windows
   
   # Add your API keys (all optional):
   GROQ_API_KEY=your_groq_api_key_here    # Get free at console.groq.com
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here # For web search
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🎯 Usage Examples

### Basic Chat
```
User: "What is the meaning of life?"
Camus: "Life has no inherent meaning, but we must create our own. The absurd condition of existence - the disconnect between our need for meaning and the universe's silence - is not something to escape but to embrace..."
```

### Philosophical Debate
```
User: "Is suffering necessary for growth?"
Dostoevsky: "Suffering is the sole origin of consciousness. Through pain, we discover the depths of our humanity and the complexity of moral choice..."
```

### Modern Context
```
User: "How should we deal with social media anxiety?"
Kierkegaard: "The present age suffers from the anxiety of too many possibilities. Social media amplifies this dread by presenting infinite choices and comparisons..."
```

## 🔧 Technical Architecture

### Core Components

#### 1. **Flask Application** (`app/`)
- **routes.py**: API endpoints, streaming responses, session management
- **models.py**: Data models and philosopher configurations
- **ai_models.py**: AI model abstractions and routing

#### 2. **AI Engine** (`app/utils/`)
- **groq_philosophy_chat.py**: Main AI orchestrator with Groq integration
- **internet_rag_engine.py**: Real-time web search and content retrieval
- **rag_engine.py**: Local knowledge base with FAISS vector search

#### 3. **Data Pipeline** (`data/`)
- **raw/**: Original philosophy texts and metadata
- **processed/**: Preprocessed chunks and FAISS embeddings

#### 4. **Frontend** (`static/`, `templates/`)
- **JavaScript**: Streaming chat interface, philosopher selection
- **CSS**: Modern dark theme, responsive design
- **HTML**: Single-page application structure

### Performance Optimizations

#### 🚀 **Speed Improvements**
- **Fast Mode**: 2-3 second responses (down from 10+ seconds)
- **Limited Sources**: 3-5 sources instead of 40-80
- **Optimized Prompts**: Reduced token usage by 60%
- **Session Caching**: Conversation history optimization

#### 🔄 **Reliability Features**
- **Multiple AI Backends**: Automatic fallback between Groq, OpenAI, HuggingFace
- **Error Handling**: Graceful degradation with informative messages
- **Rate Limiting**: Built-in protections for API limits
- **Timeout Management**: Prevents hanging requests

## 🧪 Testing

### Quick Test
```bash
python test_quick.py
```

### Performance Test
```bash
python test_performance.py
```

### Manual Testing
```bash
python test_manual.py
```

### Comprehensive Test
```bash
python test_comprehensive.py
```

## 🔧 Dependencies & Tech Stack

### **Core Framework**
```python
Flask==3.0.3              # Web framework
Flask-CORS==4.0.1          # Cross-origin requests
```

### **AI & Machine Learning**
```python
# Vector Search & Embeddings
faiss-cpu==1.8.0           # Facebook AI similarity search
sentence-transformers==3.0.1  # Sentence embeddings
transformers==4.44.2       # Hugging Face transformers

# AI API Integrations  
groq==0.9.0               # Groq AI API (FREE & FAST)
openai==1.40.6            # OpenAI GPT models
```

### **Internet RAG System**
```python
# Web Scraping & Search
requests==2.32.3          # HTTP requests
beautifulsoup4==4.12.3    # HTML parsing
duckduckgo-search==6.2.4  # Privacy-focused search
```

### **Data Processing**
```python
numpy==2.1.0              # Numerical computing
python-dotenv==1.0.1      # Environment variables
tqdm==4.66.5              # Progress bars
```

## 📁 Project Structure

```
SocrAItes/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── routes.py             # API endpoints & streaming
│   ├── models.py             # Data models
│   ├── ai_models.py          # AI model management
│   └── utils/
│       ├── groq_philosophy_chat.py    # Main AI engine
│       ├── internet_rag_engine.py     # Web search RAG
│       ├── rag_engine.py              # Local knowledge base
│       └── advanced_hf_chat.py        # HuggingFace integration
├── data/
│   ├── raw/                  # Original philosophy texts
│   └── processed/            # FAISS embeddings & chunks
├── static/
│   ├── css/style.css         # Modern dark theme
│   └── js/app.js             # Streaming chat interface
├── templates/
│   └── index.html            # Single-page application
├── tests/
│   ├── test_quick.py         # Fast functionality test
│   ├── test_performance.py   # Speed benchmarks
│   └── test_comprehensive.py # Full system test
├── scripts/
│   └── prepare_data.py       # Data preprocessing
├── requirements_internet.txt  # Full dependencies
├── requirements_safe.txt     # Offline version
├── run.py                    # Application entry point
└── README.md                 # This file
```

## What Is New

The project now supports two clear usage phases:

- Phase 1: Text chat with philosopher personas and RAG-grounded responses
- Phase 2: Voice mode with generated audio playback and replay controls

## Core Features

- Multi-persona philosophical chat (Camus, Dostoevsky, Nietzsche, Socrates, Kafka, Cioran)
- RAG pipeline combining local philosophy context and optional internet retrieval
- Groq-backed response generation for low-latency inference
- Streaming text chat endpoint for interactive UI updates
- Voice mode using server-side TTS plus replay controls
- Safe fallback paths when APIs are unavailable

## Architecture Overview

- Frontend: HTML, CSS, JavaScript single-page chat interface
- Backend: Flask routes for chat, streaming, metadata, status, and TTS
- Retrieval: Vector/semantic retrieval from philosophy-focused data
- Generation: Groq model orchestration with persona prompting
- Voice: TTS endpoint returning audio/mpeg for client playback and replay

  
## API Endpoints

- GET / : Main chat UI
- POST /api/chat : Standard chat response
- POST /api/chat/stream : Streaming text response
- GET /api/philosophers : Available personas
- GET /api/topics : Suggested topics
- GET /api/status : System capability status
- POST /api/tts : Text-to-speech audio generation
- POST /api/clear_conversation : Clear session conversation

## 🔮 Future Roadmap

### 🎭 **Multi-Philosopher Debates**
- **Philosopher vs Philosopher**: Watch Nietzsche debate Camus on existentialism
- **Panel Discussions**: 3-4 philosophers discussing contemporary issues
- **Historical Recreations**: Recreate famous philosophical debates with AI
### 🧠 **Advanced AI Features**
- **Personality Evolution**: Philosophers learn and adapt from conversations
- **Contextual Memory**: Remember previous discussions across sessions
- **Emotion Recognition**: Respond to user's emotional state and tone

### 🌍 **Extended Philosophy**
- **Eastern Philosophers**: Add Confucius, Buddha, Lao Tzu, Rumi
- **Contemporary Thinkers**: Include modern philosophers like Chomsky, Butler
- **Specialized Domains**: Ethics AI, Political Philosophy AI, Metaphysics AI

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: [GitHub](https://github.com/med-adam-alimi/SocrAItes)


## 🙏 Acknowledgments

- **Philosophy Texts**: Various public domain philosophical works
- **AI Models**: Groq, OpenAI, Hugging Face communities
- **Vector Search**: Facebook AI's FAISS library
- **Web Framework**: Flask development team

---

**Made with ❤️ by the SocrAItes team**

*"The unexamined life is not worth living." - Socrates*
