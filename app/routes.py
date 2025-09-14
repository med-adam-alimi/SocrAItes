from flask import Blueprint, render_template, request, jsonify, session
import logging
import os
import uuid

# Import all available chat systems for maximum flexibility
try:
    from app.utils.groq_philosophy_chat import GroqPhilosopherChat
    GROQ_AVAILABLE = True
    logging.info("✅ GROQ Chat Engine loaded successfully")
except ImportError as e:
    GROQ_AVAILABLE = False
    logging.warning(f"⚠️ GROQ Chat not available: {e}")

try:
    from app.utils.internet_rag_engine import ModernPhilosopherChat
    INTERNET_RAG_AVAILABLE = True
    logging.info("✅ Internet RAG Engine loaded successfully")
except ImportError as e:
    INTERNET_RAG_AVAILABLE = False
    logging.warning(f"⚠️ Internet RAG not available: {e}")

# Fallback to AI-enhanced system
try:
    from app.ai_models import AIPhilosopherChat
    AI_ENHANCED_AVAILABLE = True
except ImportError:
    AI_ENHANCED_AVAILABLE = False

# Ultimate fallback to safe system
from app.models_safe import PhilosopherChat as SafePhilosopherChat

main = Blueprint('main', __name__)

# Initialize the best available chat system
def get_chat_system():
    """Get the best available chat system with priority order"""
    api_type = os.getenv('API_TYPE', 'groq').lower()
    use_internet = os.getenv('USE_INTERNET_SEARCH', 'true').lower() == 'true'
    
    # Priority 1: GROQ (free, fast, actually works!)
    if api_type == 'groq' and GROQ_AVAILABLE:
        logging.info("🚀 Using GROQ Chat Engine (FREE & FAST)")
        return GroqPhilosopherChat()
    
    # Priority 2: Internet RAG with fallbacks
    elif INTERNET_RAG_AVAILABLE and use_internet:
        logging.info("🌐 Using Internet RAG Engine")
        return ModernPhilosopherChat()
    
    # Priority 3: AI Enhanced
    elif AI_ENHANCED_AVAILABLE:
        logging.info("🤖 Using AI-Enhanced Chat")
        return AIPhilosopherChat()
    
    # Final fallback: Safe templates
    else:
        logging.info("🛡️ Using Safe Template Chat")
        return SafePhilosopherChat()

# Initialize chat system
print("🤖 Initializing Philosophy Chat System...")
chat_system = get_chat_system()
print(f"✅ Chat system ready: {type(chat_system).__name__}")

@main.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@main.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with Internet RAG"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        philosopher = data.get('philosopher', 'neutral').lower()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Ensure session has a conversation ID
        if 'conversation_id' not in session:
            session['conversation_id'] = str(uuid.uuid4())
        
        # Log the interaction
        logging.info(f"💭 User ({philosopher}): {user_message}")
        
        # Generate response using the best available system
        if hasattr(chat_system, 'chat'):
            # Internet RAG or AI-Enhanced system
            response = chat_system.chat(user_message, philosopher)
            generated_by = 'internet_rag' if INTERNET_RAG_AVAILABLE else 'ai_enhanced'
        elif hasattr(chat_system, 'generate_response'):
            # AI-Enhanced system alternative
            result = chat_system.generate_response(
                user_message=user_message,
                philosopher=philosopher,
                context=[],
                conversation_id=session['conversation_id']
            )
            response = result['message']
            generated_by = 'ai_enhanced'
        else:
            # Safe template system
            response = chat_system.get_response(user_message, philosopher)
            generated_by = 'template'
        
        # Store conversation in session
        if 'conversation' not in session:
            session['conversation'] = []
        
        session['conversation'].append({
            'user': user_message,
            'philosopher': philosopher,
            'response': response
        })
        
        session.modified = True
        
        # Log the response
        logging.info(f"🤖 {philosopher.title()}: {response[:100]}...")
        
        return jsonify({
            'response': response,
            'philosopher': philosopher,
            'generated_by': generated_by,
            'system_type': type(chat_system).__name__,
            'internet_enabled': INTERNET_RAG_AVAILABLE and os.getenv('USE_INTERNET_SEARCH', 'true').lower() == 'true',
            'sources': []  # Will be populated by Internet RAG in future updates
        })
    
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        logging.error(error_msg)
        
        # Fallback response
        fallback_response = f"I apologize, but I'm experiencing some technical difficulties. Your question about '{user_message[:50]}...' is fascinating and deserves a thoughtful response. Please try again in a moment, or rephrase your question."
        
        return jsonify({
            'response': fallback_response,
            'philosopher': philosopher,
            'error': True,
            'generated_by': 'fallback',
            'system_type': 'Fallback'
        })

@main.route('/api/philosophers')
def get_philosophers():
    """Get available philosophers"""
    philosophers = {
        'camus': {
            'name': 'Albert Camus',
            'description': 'French philosopher known for absurdism and existentialism',
            'period': '1913-1960',
            'specialties': ['Absurdism', 'Revolt', 'The Stranger'],
            'key_concepts': ['Absurdism', 'Revolt', 'The Stranger']
        },
        'nietzsche': {
            'name': 'Friedrich Nietzsche', 
            'description': 'German philosopher who declared "God is dead"',
            'period': '1844-1900',
            'specialties': ['Will to Power', 'Übermensch', 'Eternal Recurrence'],
            'key_concepts': ['Will to Power', 'Übermensch', 'Eternal Recurrence']
        },
        'dostoevsky': {
            'name': 'Fyodor Dostoevsky',
            'description': 'Russian novelist and philosopher exploring human psychology',
            'period': '1821-1881',
            'specialties': ['Free will', 'Suffering', 'Faith vs. Reason'],
            'key_concepts': ['Free will', 'Suffering', 'Faith vs. Reason']
        },
        'sartre': {
            'name': 'Jean-Paul Sartre',
            'description': 'Existentialist philosopher of freedom and responsibility', 
            'period': '1905-1980',
            'specialties': ['Existentialism', 'Freedom', 'Bad Faith'],
            'key_concepts': ['Existentialism', 'Freedom', 'Bad Faith']
        },
        'beauvoir': {
            'name': 'Simone de Beauvoir',
            'description': 'Existential feminist exploring ethics and oppression',
            'period': '1908-1986',
            'specialties': ['Existential Feminism', 'Ethics of Ambiguity', 'Gender'],
            'key_concepts': ['Existential Feminism', 'Ethics of Ambiguity', 'Gender']
        },
        'kant': {
            'name': 'Immanuel Kant',
            'description': 'Critical philosopher of reason and moral duty',
            'period': '1724-1804',
            'specialties': ['Categorical Imperative', 'Critical Philosophy', 'Ethics'],
            'key_concepts': ['Categorical Imperative', 'Critical Philosophy', 'Ethics']
        },
        'aristotle': {
            'name': 'Aristotle',
            'description': 'Ancient philosopher of virtue ethics and practical wisdom',
            'period': '384-322 BCE',
            'specialties': ['Virtue Ethics', 'Practical Wisdom', 'Human Flourishing'],
            'key_concepts': ['Virtue Ethics', 'Practical Wisdom', 'Human Flourishing']
        },
        'marcus': {
            'name': 'Marcus Aurelius',
            'description': 'Stoic emperor-philosopher emphasizing virtue and acceptance',
            'period': '121-180 CE',
            'specialties': ['Stoicism', 'Virtue', 'Inner Peace'],
            'key_concepts': ['Stoicism', 'Virtue', 'Inner Peace']
        },
        'neutral': {
            'name': 'Philosophy Guide',
            'description': 'Neutral philosophical discussion without specific persona',
            'period': 'Modern',
            'specialties': ['General Philosophy', 'Critical Thinking', 'Ethics'],
            'key_concepts': ['General Philosophy', 'Critical Thinking', 'Ethics']
        }
    }
    
    return jsonify(philosophers)

@main.route('/api/topics')
def get_topics():
    """Get suggested philosophical topics with modern themes"""
    topics = [
        "What is the meaning of life in the digital age?",
        "Do we have free will in a deterministic universe?",
        "Is existence absurd? How do we find purpose?",
        "What is consciousness? Are we more than our neurons?",
        "How should we live ethically in modern society?",
        "What is truth in an era of information overload?",
        "How do we find meaning after traditional beliefs?",
        "What is justice in an unequal world?",
        "Is suffering necessary for growth and wisdom?",
        "How do we stay human in an AI-dominated future?",
        "What are our obligations to future generations?",
        "How do we balance individual freedom with social responsibility?",
        "What does it mean to live authentically today?",
        "How do we cope with existential anxiety?",
        "What is the role of technology in human flourishing?"
    ]
    return jsonify(topics)

@main.route('/api/conversation')
def get_conversation():
    """Get conversation history"""
    conversation = session.get('conversation', [])
    return jsonify(conversation)

@main.route('/api/clear_conversation', methods=['POST']) 
def clear_conversation():
    """Clear the current conversation"""
    if 'conversation_id' in session:
        session.pop('conversation_id')
    if 'conversation' in session:
        session.pop('conversation')
    session.modified = True
    return jsonify({'status': 'cleared'})

@main.route('/api/status')
def system_status():
    """Get system status and capabilities"""
    return jsonify({
        'internet_rag_available': INTERNET_RAG_AVAILABLE,
        'ai_enhanced_available': AI_ENHANCED_AVAILABLE,
        'current_system': type(chat_system).__name__,
        'internet_search_enabled': os.getenv('USE_INTERNET_SEARCH', 'true').lower() == 'true',
        'features': {
            'real_time_search': INTERNET_RAG_AVAILABLE,
            'reddit_integration': INTERNET_RAG_AVAILABLE,
            'academic_sources': INTERNET_RAG_AVAILABLE,
            'current_events': INTERNET_RAG_AVAILABLE,
            'ai_generation': AI_ENHANCED_AVAILABLE or INTERNET_RAG_AVAILABLE,
            'template_fallback': True
        },
        'model_info': {
            'primary_model': os.getenv('PRIMARY_MODEL', 'meta-llama/Llama-2-70b-chat-hf'),
            'fallback_model': os.getenv('FALLBACK_MODEL', 'microsoft/DialoGPT-large'),
            'search_enabled': os.getenv('USE_INTERNET_SEARCH', 'true').lower() == 'true'
        }
    })
