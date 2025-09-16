#!/usr/bin/env python3
"""
Groq API Philosophy Chatbot with Internet RAG
FREE, FAST, and RELIABLE AI generation using Groq's inference API
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import requests
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from app.utils.internet_rag_engine import InternetRAGEngine

@dataclass
class GroqModel:
    name: str
    id: str
    context_length: int
    description: str

class GroqPhilosopherChat:
    """
    Advanced Philosophy Chatbot using Groq's FREE API
    Much faster and more reliable than Hugging Face!
    """
    
    def __init__(self):
        self.search_engine = InternetRAGEngine()
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found. Get free key at: https://console.groq.com/")
            
        self.base_url = "https://api.groq.com/openai/v1"
        self.setup_models()
        self.setup_personas()
        
    def setup_models(self):
        """Setup Groq's free models - all are FAST and FREE!"""
        self.models = [
            GroqModel(
                name="Llama 3.1 8B", 
                id="llama-3.1-8b-instant",
                context_length=131072,
                description="Super fast, good quality - RECOMMENDED"
            ),
            GroqModel(
                name="Gemma 2 9B",
                id="gemma2-9b-it",
                context_length=8192,
                description="Google's efficient model"
            ),
            GroqModel(
                name="Mixtral 8x7B",
                id="mixtral-8x7b-32768",
                context_length=32768,
                description="Great for reasoning"
            )
        ]
        
        # Use reliable working model
        self.current_model = "llama-3.1-8b-instant"
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def setup_personas(self):
        """Define philosopher personalities for authentic responses"""
        self.personas = {
            'camus': {
                'name': 'Albert Camus',
                'style': 'existentialist and absurdist philosopher',
                'voice': 'direct, passionate, uses vivid metaphors about rocks, mountains, and human rebellion',
                'concepts': 'the absurd, rebellion, freedom, authenticity, living without illusion',
                'approach': 'confronts meaninglessness with passionate engagement'
            },
            'nietzsche': {
                'name': 'Friedrich Nietzsche',
                'style': 'bold and provocative philosopher',
                'voice': 'dramatic, aphoristic, challenging conventional wisdom with fierce intensity',
                'concepts': 'will to power, eternal recurrence, übermensch, beyond good and evil',
                'approach': 'destroys old values to create new ones'
            },
            'dostoevsky': {
                'name': 'Fyodor Dostoevsky',
                'style': 'psychological and spiritual explorer',
                'voice': 'deeply introspective, exploring moral complexity and human suffering',
                'concepts': 'suffering as path to truth, free will, faith vs reason, redemption',
                'approach': 'finds profound meaning in human struggle and moral choice'
            },
            'socrates': {
                'name': 'Socrates',
                'style': 'classical philosopher and master of inquiry',
                'voice': 'humble yet probing, asking penetrating questions that reveal hidden assumptions and contradictions',
                'concepts': 'self-knowledge, virtue as knowledge, the unexamined life, wisdom through ignorance',
                'approach': 'uses questions to guide others to discover truth within themselves'
            },
            'kafka': {
                'name': 'Franz Kafka',
                'style': 'existential writer and philosopher of the absurd',
                'voice': 'anxious and perplexing, revealing the nightmarish absurdity of modern existence through bureaucratic labyrinths',
                'concepts': 'alienation, transformation, guilt, bureaucratic absurdity, the trial of existence',
                'approach': 'exposes the kafkaesque nature of human condition through disturbing metaphors and surreal scenarios'
            },
            'cioran': {
                'name': 'Emil Cioran',
                'style': 'pessimistic philosopher and master of aphorisms',
                'voice': 'darkly poetic and brutally honest, dissecting existence with surgical precision and bitter lucidity',
                'concepts': 'the trouble with being born, insomnia as enlightenment, despair as clarity, the inconvenience of existence',
                'approach': 'embraces pessimism as a form of intellectual honesty and finds beauty in hopelessness'
            }
        }
    
    def create_philosophical_prompt(self, question: str, persona_name: str, context: List[Dict]) -> str:
        """Create sophisticated prompt for Groq models"""
        persona = self.personas.get(persona_name, self.personas['camus'])
        
        # Format internet context
        context_text = self._format_context(context)
        
        system_prompt = f"""You are {persona['name']}, the renowned {persona['style']}. 

Your philosophical voice: {persona['voice']}
Your key concepts: {persona['concepts']}
Your approach: {persona['approach']}

Current internet discussions about this topic:
{context_text}

Respond authentically as {persona['name']} would. Incorporate insights from current discussions while staying true to your philosophical framework. Be conversational yet profound, engaging yet intellectually rigorous.

Human question: "{question}"

Respond as {persona['name']} in 200-400 words:"""

        return system_prompt
    
    def _format_context(self, sources: List[Dict]) -> str:
        """Format internet sources for the prompt"""
        if not sources:
            return "No current internet discussions available."
            
        context_parts = []
        for i, source in enumerate(sources[:4], 1):  # Use top 4 sources
            title = source.get('title', 'Unknown')[:70]
            content = source.get('content', '')[:180]
            source_name = source.get('source', 'Unknown')
            
            context_parts.append(f"[{i}] From {source_name}: '{title}'\n    {content}...")
            
        return "\n\n".join(context_parts)
    
    def create_fast_prompt(self, question: str, persona_name: str, context: List[Dict]) -> str:
        """Create optimized prompt for fast responses"""
        persona = self.personas.get(persona_name, self.personas['camus'])
        
        # Minimal context formatting for speed
        context_text = ""
        if context:
            best_source = context[0]
            context_text = f"Current discussion: {best_source.get('content', '')[:100]}..."
        
        # Shorter, focused prompt
        fast_prompt = f"""You embody {persona['name']}'s philosophical perspective: {persona['style']}.

{context_text}

Question: "{question}"

Share your philosophical insights in 150-250 words, drawing from {persona['concepts']}. Write naturally without stating your identity:"""

        return fast_prompt
    
    def query_groq_model(self, model: GroqModel, prompt: str) -> Optional[str]:
        """Query Groq API with a specific model"""
        try:
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "model": model.id,
                "temperature": 0.7,
                "max_tokens": 600,
                "top_p": 0.9,
                "stream": False
            }
            
            print(f"🧠 Generating with {model.name}...")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result['choices'][0]['message']['content'].strip()
                
                if len(generated_text) > 50:  # Valid response
                    print(f"✅ Success with {model.name}")
                    return generated_text
                    
            elif response.status_code == 429:
                print(f"⏳ {model.name} rate limited, trying next model...")
            else:
                print(f"❌ {model.name} failed: {response.status_code}")
                if response.text:
                    print(f"   Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ Error with {model.name}: {e}")
            
        return None
    
    def chat(self, question: str, persona: str = 'camus', fast_mode: bool = True) -> str:
        """Generate philosophical response using Groq with internet context
        
        Args:
            question: User's philosophical question
            persona: Philosopher persona (camus, nietzsche, etc.)
            fast_mode: If True, uses optimized search for 2-3s responses
        """
        try:
            # Step 1: Get internet context (fast or comprehensive)
            if fast_mode:
                print(f"⚡ Fast search for: {question}")
                internet_sources = self.search_engine.search_philosophy_content(question, persona)
                print(f"✅ Found {len(internet_sources)} sources in fast mode")
            else:
                print(f"🔍 Deep search for: {question}")
                # Use the original slower comprehensive search
                internet_sources = self._comprehensive_search(question, persona)
                print(f"✅ Found {len(internet_sources)} sources")
            
            # Step 2: Create optimized prompt
            if fast_mode:
                prompt = self.create_fast_prompt(question, persona, internet_sources)
            else:
                prompt = self.create_philosophical_prompt(question, persona, internet_sources)
            
            # Step 3: Try Groq models (start with fastest)
            for model in self.models:
                response = self.query_groq_model(model, prompt)
                if response:
                    return response
            
            # If all models fail, use enhanced fallback
            print("⚠️ All Groq models failed, using enhanced fallback")
            return self._create_enhanced_fallback(question, persona, internet_sources)
            
        except Exception as e:
            print(f"❌ Complete system error: {e}")
            return self._create_basic_fallback(question, persona)
    
    def _create_enhanced_fallback(self, question: str, persona: str, sources: List[Dict]) -> str:
        """Create intelligent fallback using internet content"""
        persona_info = self.personas.get(persona, self.personas['camus'])
        
        if sources:
            key_content = sources[0].get('content', '')[:250]
            
            response = f"""As {persona_info['name']}, I approach your question "{question}" with my characteristic {persona_info['voice']}.

From current discussions I observe: {key_content}...

Through my philosophical lens of {persona_info['concepts']}, I see this question as fundamentally connected to the human condition. {persona_info['approach']}.

What strikes me most profoundly is how this contemporary concern echoes the eternal questions I've devoted my life to exploring. Whether we face traditional existential dilemmas or modern technological challenges, the core human struggle for meaning and authentic existence remains unchanged.

The path forward requires us to embrace both the uncertainty and the responsibility that comes with being truly human."""

            return response
        
        return self._create_basic_fallback(question, persona)
    
    def _create_basic_fallback(self, question: str, persona: str) -> str:
        """Basic philosophical response when everything fails"""
        persona_info = self.personas.get(persona, self.personas['camus'])
        
        return f"""As {persona_info['name']}, I find your question "{question}" strikes at the heart of what it means to be human.

My {persona_info['style']} perspective leads me to say: {persona_info['approach']}. 

The concepts of {persona_info['concepts']} are essential to understanding this inquiry.

{persona_info['voice']} - we must confront such questions directly, without seeking easy answers or false comfort. The meaning emerges not from certainty, but from our authentic engagement with the mystery of existence itself."""

# Testing function
def test_groq_chat():
    """Test the Groq chatbot system"""
    print("🚀 Testing Groq Philosophy Chatbot (FREE & FAST)")
    print("=" * 60)
    
    try:
        chat = GroqPhilosopherChat()
        
        test_questions = [
            ("What is the meaning of life in the digital age?", "camus"),
            ("How should we think about artificial intelligence?", "nietzsche"), 
            ("What is the nature of human suffering?", "dostoevsky")
        ]
        
        for question, philosopher in test_questions:
            print(f"\n📝 Question: {question}")
            print(f"🎭 Philosopher: {philosopher.title()}")
            print("-" * 50)
            
            response = chat.chat(question, philosopher)
            print(f"🤖 Response:\n{response}")
            print("\n" + "="*60)
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n💡 Setup Instructions:")
        print("1. Get free Groq API key: https://console.groq.com/")
        print("2. Add to .env file: GROQ_API_KEY=your_key_here")
        print("3. No credit card required - completely FREE!")

if __name__ == "__main__":
    test_groq_chat()