import json
import os
import requests
import time
from typing import List, Dict, Any

class RAGEngine:
    """SAFE RAG engine using only FREE APIs - NO heavy model loading!"""
    
    def __init__(self):
        """Initialize with API-only approach - no models loaded locally."""
        print("🆓 Starting SAFE API-only mode...")
        
        # Load text chunks only (lightweight)
        self.chunks = []
        self._load_text_data_only()
        
        # Free API endpoints (no GPU/CPU intensive operations)
        self.api_endpoints = {
            'huggingface_free': {
                'url': 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium',
                'requires_key': False,  # Some HF models are free without key
                'headers': {}
            },
            'ollama_public': {
                'url': 'https://ollama.ai/api/generate',  # If available
                'requires_key': False,
                'headers': {}
            }
        }
        
        print("✅ Safe API-only RAG engine initialized!")
    
    def _load_text_data_only(self):
        """Load only text data - NO model loading to avoid crashes."""
        try:
            chunks_path = os.environ.get('CHUNKS_PATH', 'data/processed/chunks.json')
            if os.path.exists(chunks_path):
                with open(chunks_path, 'r', encoding='utf-8') as f:
                    self.chunks = json.load(f)
                print(f"✅ Loaded {len(self.chunks)} text chunks safely")
            else:
                print("⚠️ No chunks found - creating sample data")
                self._create_sample_chunks()
        except Exception as e:
            print(f"⚠️ Error loading chunks: {e}")
            self._create_sample_chunks()
    
    def _create_sample_chunks(self):
        """Create sample philosophy chunks if data is missing."""
        self.chunks = [
            {
                'text': 'The absurd is born of this confrontation between the human need and the unreasonable silence of the world. - Albert Camus',
                'philosopher': 'camus',
                'source': 'The Myth of Sisyphus',
                'id': 0
            },
            {
                'text': 'I am a sick man... I am a spiteful man. I am an unattractive man. I believe my liver is diseased. - Fyodor Dostoevsky',
                'philosopher': 'dostoevsky', 
                'source': 'Notes from Underground',
                'id': 1
            },
            {
                'text': 'What does not kill me makes me stronger. - Friedrich Nietzsche',
                'philosopher': 'nietzsche',
                'source': 'Twilight of the Idols',
                'id': 2
            },
            {
                'text': 'The unexamined life is not worth living. - Socrates',
                'philosopher': 'neutral',
                'source': 'Plato Apology',
                'id': 3
            }
        ]
        print("✅ Created sample philosophy chunks")
    
    def retrieve_context(self, query: str, philosopher: str = None, top_k: int = 2) -> List[str]:
        """Simple text search - no AI embedding needed."""
        if not self.chunks:
            return ["Philosophy is the art of thinking about thinking itself."]
        
        # Simple keyword matching (no heavy AI needed)
        query_words = query.lower().split()
        relevant_chunks = []
        
        for chunk in self.chunks:
            # Score based on keyword overlap
            chunk_text = chunk['text'].lower()
            score = sum(1 for word in query_words if word in chunk_text)
            
            # Prefer philosopher-specific chunks
            if philosopher and philosopher != 'neutral':
                chunk_philosopher = chunk.get('philosopher', '').lower()
                if philosopher.lower() == chunk_philosopher:
                    score += 3  # Boost philosopher-specific content
            
            if score > 0:
                relevant_chunks.append((score, chunk['text']))
        
        # Sort by score and return top chunks
        relevant_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk[1] for chunk in relevant_chunks[:top_k]]
    
    def generate_simple_response(self, user_input: str, philosopher: str, context: List[str]) -> str:
        """Generate response using templates - no AI API needed for testing."""
        
        # Get context
        context_text = ' '.join(context) if context else ""
        
        # Simple template responses based on philosopher
        responses = {
            'camus': {
                'default': "In the face of the absurd, we must imagine Sisyphus happy. Your question touches on the fundamental confrontation between human need for meaning and the silence of the universe.",
                'meaning': "There is no inherent meaning in life - this is the absurd condition. But we can create meaning through our revolt, our freedom, and our passion.",
                'death': "There is but one truly serious philosophical problem, and that is suicide. Judging whether life is worth living is the fundamental question of philosophy."
            },
            'dostoevsky': {
                'default': "The human soul is a mysterious abyss. What you ask strikes at the heart of our moral and psychological struggles.",
                'freedom': "Man is tormented by no greater anxiety than to find someone to whom he can hand over that gift of freedom with which he was born.",
                'suffering': "Pain and suffering are always inevitable for a large intelligence and a deep heart."
            },
            'nietzsche': {
                'default': "What does not destroy me, makes me stronger. Your question calls for a revaluation of values!",
                'power': "The will to power is the driving force of all life. Embrace your strength and become who you truly are.",
                'morality': "There are no moral phenomena at all, but only a moral interpretation of phenomena."
            },
            'neutral': {
                'default': "This is a profound philosophical question that has engaged thinkers for centuries. Let me help you explore different perspectives.",
                'general': "Philosophy begins in wonder and seeks to understand the fundamental nature of reality, knowledge, and existence."
            }
        }
        
        # Choose response based on keywords in user input
        user_lower = user_input.lower()
        philosopher_responses = responses.get(philosopher, responses['neutral'])
        
        # Simple keyword matching for response selection
        if any(word in user_lower for word in ['meaning', 'purpose', 'why']):
            response = philosopher_responses.get('meaning', philosopher_responses['default'])
        elif any(word in user_lower for word in ['death', 'die', 'suicide']):
            response = philosopher_responses.get('death', philosopher_responses['default'])
        elif any(word in user_lower for word in ['freedom', 'free', 'choice']):
            response = philosopher_responses.get('freedom', philosopher_responses['default'])
        elif any(word in user_lower for word in ['power', 'strong', 'strength']):
            response = philosopher_responses.get('power', philosopher_responses['default'])
        elif any(word in user_lower for word in ['moral', 'ethics', 'good', 'evil']):
            response = philosopher_responses.get('morality', philosopher_responses['default'])
        elif any(word in user_lower for word in ['suffering', 'pain', 'hurt']):
            response = philosopher_responses.get('suffering', philosopher_responses['default'])
        else:
            response = philosopher_responses['default']
        
        # Add context if available
        if context_text:
            response += f"\n\nAs the texts remind us: {context_text[:100]}..."
        
        return response