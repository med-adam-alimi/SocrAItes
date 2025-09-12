from flask import Blueprint, render_template, request, jsonify, session
from app.ai_models import AIPhilosopherChat
import uuid
import os

main = Blueprint('main', __name__)

# Initialize AI-Enhanced components
print("🤖 Initializing AI-Enhanced Philosophy Chat...")
philosopher_chat = AIPhilosopherChat()
print("✅ AI components ready!")

@main.route('/')
def index():
    """Main chat interface."""
    return render_template('index.html')

@main.route('/api/philosophers')
def get_philosophers():
    """Get list of available philosophers."""
    philosophers = {
        'camus': {
            'name': 'Albert Camus',
            'description': 'French philosopher known for absurdism and existentialism',
            'period': '1913-1960',
            'key_concepts': ['Absurdism', 'Revolt', 'The Stranger']
        },
        'dostoevsky': {
            'name': 'Fyodor Dostoevsky',
            'description': 'Russian novelist and philosopher exploring human psychology',
            'period': '1821-1881',
            'key_concepts': ['Free will', 'Suffering', 'Faith vs. Reason']
        },
        'nietzsche': {
            'name': 'Friedrich Nietzsche',
            'description': 'German philosopher who declared "God is dead"',
            'period': '1844-1900',
            'key_concepts': ['Will to Power', 'Übermensch', 'Eternal Recurrence']
        },
        'neutral': {
            'name': 'Philosophy Guide',
            'description': 'Neutral philosophical discussion without specific persona',
            'period': 'Modern',
            'key_concepts': ['General Philosophy', 'Critical Thinking', 'Ethics']
        }
    }
    return jsonify(philosophers)

@main.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        philosopher = data.get('philosopher', 'neutral')
        
        if not user_message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Ensure session has a conversation ID
        if 'conversation_id' not in session:
            session['conversation_id'] = str(uuid.uuid4())
        
        # Generate AI-enhanced response
        response = philosopher_chat.generate_response(
            user_message=user_message,
            philosopher=philosopher,
            context=[],  # RAG engine will handle context retrieval
            conversation_id=session['conversation_id']
        )
        
        return jsonify({
            'response': response['message'],
            'sources': response.get('sources', []),
            'philosopher': philosopher,
            'generated_by': response.get('generated_by', 'ai')
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@main.route('/api/topics')
def get_topics():
    """Get suggested philosophical topics."""
    topics = [
        "What is the meaning of life?",
        "Do we have free will?",
        "Is existence absurd?",
        "What is the nature of consciousness?",
        "How should we live ethically?",
        "What is truth?",
        "Does God exist?",
        "What is justice?",
        "Is suffering necessary for growth?",
        "What makes life worth living?"
    ]
    return jsonify(topics)

@main.route('/api/clear_conversation', methods=['POST'])
def clear_conversation():
    """Clear the current conversation."""
    if 'conversation_id' in session:
        session.pop('conversation_id')
    return jsonify({'status': 'cleared'})
