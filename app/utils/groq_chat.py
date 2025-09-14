#!/usr/bin/env python3
"""
GROQ API Philosophy Chatbot with Internet RAG
FREE, FAST, and ACTUALLY WORKS!

Get your free API key at: https://console.groq.com/
Models: llama3-8b-8192, llama3-70b-8192, mixtral-8x7b-32768
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import requests
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from app.utils.internet_rag_engine import InternetRAGEngine

class GroqPhilosopherChat:
    """
    Philosophy Chatbot using GROQ API - FREE and FAST!
    """
    
    def __init__(self):
        self.search_engine = InternetRAGEngine()
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            print("⚠️ GROQ_API_KEY not found. Get free key at: https://console.groq.com/")
            
        self.setup_models()
        self.setup_personas()
        
    def setup_models(self):
        """Setup GROQ models - these actually work!"""
        self.models = [
            {
                'name': 'llama3-8b-8192',
                'display': 'Llama 3 8B (Fast)',
                'max_tokens': 8192,
                'best_for': 'Speed and general chat'
            },
            {
                'name': 'llama3-70b-8192', 
                'display': 'Llama 3 70B (Smart)',
                'max_tokens': 8192,
                'best_for': 'Complex reasoning'
            },
            {
                'name': 'mixtral-8x7b-32768',
                'display': 'Mixtral 8x7B (Long context)',
                'max_tokens': 32768,
                'best_for': 'Long conversations'
            }
        ]
        
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def setup_personas(self):
        """Define philosopher personalities for GROQ"""
        self.personas = {
            'camus': {
                'name': 'Albert Camus',
                'system_prompt': """You are Albert Camus, the French existentialist philosopher and Nobel Prize winner. 

Your philosophical framework:
- Life is fundamentally absurd (no inherent meaning)
- We must rebel against the absurd through authentic living
- Create your own meaning through freedom and passion
- Embrace both despair and hope simultaneously

Your speaking style:
- Direct and passionate
- Use vivid metaphors (rocks, mountains, Mediterranean sun)
- Reference your own works (The Stranger, The Myth of Sisyphus)
- Balance philosophical depth with accessible language
- Show both intellectual rigor and emotional authenticity

Key concepts to weave in: absurd, rebellion, authenticity, freedom, solidarity, lucidity"""
            },
            'nietzsche': {
                'name': 'Friedrich Nietzsche',
                'system_prompt': """You are Friedrich Nietzsche, the German philosopher who proclaimed "God is dead" and developed the concepts of will to power and eternal recurrence.

Your philosophical framework:
- Will to power as the fundamental drive
- Eternal recurrence as a test of life affirmation
- Übermensch as human potential
- Critique of traditional morality and religion

Your speaking style:
- Bold and provocative
- Use dramatic language and exclamations
- Challenge conventional thinking
- Aphoristic and poetic
- Sometimes harsh but always passionate

Key concepts: will to power, eternal recurrence, übermensch, master/slave morality, life affirmation"""
            },
            'dostoevsky': {
                'name': 'Fyodor Dostoevsky', 
                'system_prompt': """You are Fyodor Dostoevsky, the Russian author-philosopher who explored the depths of human psychology, suffering, and redemption.

Your philosophical framework:
- Human suffering as meaningful and transformative
- Free will as both blessing and burden
- Faith and doubt in constant tension
- Moral complexity in every human action

Your speaking style:
- Psychologically penetrating
- Explore moral paradoxes and dilemmas
- Reference human suffering and redemption
- Show deep empathy for human struggle
- Balance darkness with hope

Key concepts: suffering, redemption, free will, faith, moral responsibility, human dignity"""
            }
        }
    
    def create_groq_messages(self, question: str, persona_name: str, context: List[Dict]) -> List[Dict]:
        """Create messages for GROQ API"""
        persona = self.personas.get(persona_name, self.personas['camus'])
        
        # Format internet context
        context_text = self._format_context(context)
        
        system_message = f"""{persona['system_prompt']}

You have access to current internet discussions about philosophy. Use this context to inform your response, but speak authentically as {persona['name']} would.

Current internet context:
{context_text}

Instructions:
1. Respond as {persona['name']} would, using your philosophical framework
2. Incorporate insights from the internet context naturally
3. Be conversational and engaging, not academic
4. Show the relevance of your philosophy to modern issues
5. Keep responses thoughtful but accessible (200-400 words)"""

        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
    
    def _format_context(self, sources: List[Dict]) -> str:
        """Format internet sources for GROQ"""
        if not sources:
            return "No current internet context available."
            
        context_parts = []
        for i, source in enumerate(sources[:3], 1):
            title = source.get('title', 'Unknown')[:60]
            content = source.get('content', '')[:150]
            source_name = source.get('source', 'Unknown source')
            
            context_parts.append(f"{i}. From {source_name}: '{title}'\n   Content: {content}...")
            
        return "\n\n".join(context_parts)
    
    def query_groq(self, model_name: str, messages: List[Dict]) -> Optional[str]:
        """Query GROQ API with the specified model"""
        try:
            payload = {
                "model": model_name,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 800,
                "top_p": 0.9,
                "stream": False
            }
            
            print(f"🧠 Thinking with {model_name}...")
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"✅ Success with {model_name}")
                return content.strip()
            else:
                print(f"❌ {model_name} failed: {response.status_code}")
                if response.status_code == 401:
                    print("   Check your GROQ_API_KEY")
                
        except Exception as e:
            print(f"❌ Error with {model_name}: {e}")
            
        return None
    
    def chat(self, question: str, persona: str = 'camus', model_preference: str = 'fast') -> str:
        """Generate philosophical response using GROQ models"""
        if not self.api_key:
            return self._no_api_fallback(question, persona)
        
        try:
            # Step 1: Get internet context
            print(f"🔍 Searching internet for: {question}")
            internet_sources = self.search_engine.search_philosophy_content(question)
            print(f"✅ Found {len(internet_sources)} sources")
            
            # Step 2: Create GROQ messages
            messages = self.create_groq_messages(question, persona, internet_sources)
            
            # Step 3: Select model based on preference
            if model_preference == 'smart':
                models_to_try = ['llama3-70b-8192', 'mixtral-8x7b-32768', 'llama3-8b-8192']
            elif model_preference == 'long':
                models_to_try = ['mixtral-8x7b-32768', 'llama3-70b-8192', 'llama3-8b-8192']
            else:  # fast
                models_to_try = ['llama3-8b-8192', 'mixtral-8x7b-32768', 'llama3-70b-8192']
            
            # Step 4: Try models in order
            for model_name in models_to_try:
                response = self.query_groq(model_name, messages)
                if response:
                    return response
            
            print("⚠️ All GROQ models failed, using enhanced fallback")
            return self._create_enhanced_fallback(question, persona, internet_sources)
            
        except Exception as e:
            print(f"❌ Complete system error: {e}")
            return self._create_basic_fallback(question, persona)
    
    def _no_api_fallback(self, question: str, persona: str) -> str:
        """Fallback when no API key is available"""
        return f"""🔑 GROQ API Setup Required

To use this FREE and FAST AI chatbot:

1. **Get free GROQ API key**: https://console.groq.com/
2. **Add to .env file**: GROQ_API_KEY=your_key_here
3. **Enjoy fast AI responses!**

GROQ offers:
✅ FREE tier with generous limits
✅ Llama 3 8B/70B models
✅ Mixtral 8x7B model
✅ MUCH faster than Hugging Face
✅ Actually works in 2025!

Your question: "{question}"
Persona: {persona}

Once GROQ is set up, you'll get real AI-generated philosophical responses!"""
    
    def _create_enhanced_fallback(self, question: str, persona: str, sources: List[Dict]) -> str:
        """Enhanced fallback using internet content"""
        persona_info = self.personas.get(persona, self.personas['camus'])
        
        if sources:
            content = sources[0].get('content', '')[:300]
            
            return f"""As {persona_info['name']}, I approach your question "{question}" with both philosophical rigor and contemporary awareness.

From current discussions I observe: {content}...

Through my philosophical framework: This question touches the very essence of human existence and our struggle to find meaning in an ever-changing world.

The intersection of classical philosophy with modern concerns reveals the timeless nature of our fundamental questions. Whether we face traditional existential dilemmas or contemporary technological challenges, the human condition remains both beautifully complex and profoundly absurd.

(Note: This is a fallback response. For full AI generation, set up GROQ API key for much better responses!)"""
        
        return self._create_basic_fallback(question, persona)
    
    def _create_basic_fallback(self, question: str, persona: str) -> str:
        """Basic fallback response"""
        persona_info = self.personas.get(persona, self.personas['camus'])
        
        return f"""As {persona_info['name']}, your question "{question}" invites deep philosophical reflection.

This inquiry embodies the essential human struggle to understand our place in existence. The search for meaning, authenticity, and purpose remains as relevant today as it was in my time.

(For full AI-generated responses, please set up the free GROQ API key!)"""

# Testing function
def test_groq_chat():
    """Test the GROQ chatbot system"""
    print("🚀 Testing GROQ Philosophy Chatbot")
    print("=" * 60)
    
    chat = GroqPhilosopherChat()
    
    test_question = "What is the meaning of life in the digital age?"
    print(f"\n📝 Question: {test_question}")
    print("-" * 40)
    
    # Test with different model preferences
    for preference in ['fast', 'smart']:
        print(f"\n🎯 Testing with '{preference}' model preference:")
        response = chat.chat(test_question, 'camus', preference)
        print(f"Response: {response[:200]}...")
        print()

if __name__ == "__main__":
    test_groq_chat()