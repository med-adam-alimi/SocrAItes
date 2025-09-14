#!/usr/bin/env python3
"""
Local Ollama Philosophy Chatbot with Internet RAG
Completely local AI generation - no API keys needed!
"""

import requests
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from app.utils.internet_rag_engine import InternetRAGEngine

class OllamaPhilosopherChat:
    """
    Philosophy Chatbot using local Ollama models
    Completely private and free!
    """
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.search_engine = InternetRAGEngine()
        self.base_url = base_url
        self.setup_models()
        self.setup_personas()
        
    def setup_models(self):
        """Setup available Ollama models"""
        self.preferred_models = [
            "llama2:7b",           # Meta's Llama 2 7B
            "mistral:7b",          # Mistral 7B
            "codellama:7b",        # Code Llama (also good for reasoning)
            "neural-chat:7b",      # Intel's Neural Chat
            "phi:2.7b",            # Microsoft Phi (smaller, faster)
        ]
        
        # Check which models are available
        self.available_models = self.check_available_models()
        
    def check_available_models(self) -> List[str]:
        """Check which Ollama models are installed locally"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                available = [model['name'] for model in models_data.get('models', [])]
                print(f"📋 Available Ollama models: {available}")
                return available
            else:
                print("⚠️ Ollama not running or no models installed")
                return []
        except Exception as e:
            print(f"❌ Cannot connect to Ollama: {e}")
            print("💡 To install Ollama:")
            print("   1. Download from: https://ollama.ai/")
            print("   2. Install a model: ollama pull llama2:7b")
            return []
    
    def setup_personas(self):
        """Define philosopher personalities for Ollama"""
        self.personas = {
            'camus': {
                'name': 'Albert Camus',
                'context': 'You are Albert Camus, the French existentialist philosopher and Nobel Prize winner. You believe life is absurd but must be lived with rebellion, freedom, and passion. You speak directly and use vivid metaphors.',
                'style_prompt': 'Answer in the style of Camus - direct, passionate, using metaphors about rocks, mountains, and the human condition.'
            },
            'nietzsche': {
                'name': 'Friedrich Nietzsche',
                'context': 'You are Friedrich Nietzsche, the German philosopher who proclaimed "God is dead" and developed concepts of will to power and eternal recurrence. You are bold, provocative, and challenge conventional thinking.',
                'style_prompt': 'Answer in Nietzsche\'s style - bold, dramatic, with exclamations and challenging questions.'
            },
            'dostoevsky': {
                'name': 'Fyodor Dostoevsky',
                'context': 'You are Fyodor Dostoevsky, the Russian author-philosopher who explored the depths of human psychology, suffering, and redemption. You see profound moral complexity in everything.',
                'style_prompt': 'Answer in Dostoevsky\'s style - psychologically deep, exploring moral dilemmas and human suffering.'
            }
        }
    
    def create_ollama_prompt(self, question: str, persona_name: str, context: List[Dict]) -> str:
        """Create optimized prompt for Ollama models"""
        persona = self.personas.get(persona_name, self.personas['camus'])
        
        # Format internet context
        context_text = self._format_context(context)
        
        prompt = f"""{persona['context']}

Current internet discussions on this topic:
{context_text}

Human question: "{question}"

{persona['style_prompt']} Incorporate insights from the current discussions while staying true to your philosophical perspective. Keep your response engaging and conversational (200-400 words).

Response:"""

        return prompt
    
    def _format_context(self, sources: List[Dict]) -> str:
        """Format internet sources for Ollama"""
        if not sources:
            return "No current internet discussions available."
            
        context_parts = []
        for i, source in enumerate(sources[:3], 1):
            title = source.get('title', 'Unknown')[:50]
            content = source.get('content', '')[:120]
            
            context_parts.append(f"{i}. {title}: {content}...")
            
        return "\n".join(context_parts)
    
    def query_ollama(self, model: str, prompt: str) -> Optional[str]:
        """Query local Ollama model"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            }
            
            print(f"🧠 Thinking with {model}...")
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60  # Ollama can be slower
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()
                
                if len(generated_text) > 30:  # Valid response
                    print(f"✅ Generated response with {model}")
                    return generated_text
                    
            print(f"❌ {model} failed: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Error with {model}: {e}")
            
        return None
    
    def chat(self, question: str, persona: str = 'camus') -> str:
        """Generate philosophical response using local Ollama"""
        # Check if Ollama is available
        if not self.available_models:
            return self._no_ollama_fallback(question, persona)
        
        try:
            # Step 1: Get internet context
            print(f"🔍 Searching internet for: {question}")
            internet_sources = self.search_engine.search_philosophy_content(question)
            print(f"✅ Found {len(internet_sources)} sources")
            
            # Step 2: Create Ollama prompt
            prompt = self.create_ollama_prompt(question, persona, internet_sources)
            
            # Step 3: Try available models
            for model in self.preferred_models:
                if model in self.available_models:
                    response = self.query_ollama(model, prompt)
                    if response:
                        return response
            
            # Try any available model
            for model in self.available_models:
                response = self.query_ollama(model, prompt)
                if response:
                    return response
            
            print("⚠️ All Ollama models failed")
            return self._create_internet_fallback(question, persona, internet_sources)
            
        except Exception as e:
            print(f"❌ Ollama system error: {e}")
            return self._create_basic_fallback(question, persona)
    
    def _no_ollama_fallback(self, question: str, persona: str) -> str:
        """Fallback when Ollama is not available"""
        return f"""🤖 Ollama Local AI Setup Required

To use this completely local and private philosophy chatbot:

1. **Install Ollama**: Download from https://ollama.ai/
2. **Install a model**: Run `ollama pull llama2:7b`
3. **Start Ollama**: It runs as a local server

Then you'll have a completely private AI philosopher that:
✅ Runs locally on your computer
✅ No internet required for AI generation
✅ No API keys needed
✅ Complete privacy

Your question: "{question}"
Persona: {persona}

Once Ollama is set up, I'll give you a proper philosophical response!"""
    
    def _create_internet_fallback(self, question: str, persona: str, sources: List[Dict]) -> str:
        """Use internet content to create philosophical response"""
        persona_info = self.personas.get(persona, self.personas['camus'])
        
        if sources:
            content = sources[0].get('content', '')[:200]
            
            return f"""As {persona_info['name']}, I draw upon current discussions to address your question: "{question}"

From contemporary sources, I see: {content}...

Through my philosophical lens: This connects to the fundamental questions I've always explored. {persona_info['style_prompt']}

The tension between modern concerns and eternal human questions reveals the timeless nature of philosophical inquiry. We must engage with both the immediate and the eternal."""
        
        return self._create_basic_fallback(question, persona)
    
    def _create_basic_fallback(self, question: str, persona: str) -> str:
        """Basic philosophical response"""
        persona_info = self.personas.get(persona, self.personas['camus'])
        
        return f"""As {persona_info['name']}, I approach your question "{question}" through the lens of my philosophical framework.

{persona_info['context']}

This question invites us to examine the foundations of human existence and meaning."""

    def install_recommended_model(self):
        """Helper to install a recommended model"""
        print("🔧 Ollama Setup Instructions:")
        print("1. Download Ollama: https://ollama.ai/")
        print("2. Install it and restart your terminal")
        print("3. Run: ollama pull llama2:7b")
        print("4. Wait for download (few GB)")
        print("5. Run this chatbot again!")

# Testing function
def test_ollama_chat():
    """Test the Ollama chatbot system"""
    print("🚀 Testing Local Ollama Philosophy Chatbot")
    print("=" * 60)
    
    chat = OllamaPhilosopherChat()
    
    if not chat.available_models:
        chat.install_recommended_model()
        return
    
    test_question = "What is the meaning of life in the digital age?"
    print(f"\n📝 Question: {test_question}")
    print("-" * 40)
    
    response = chat.chat(test_question, 'camus')
    print(f"🤖 Camus (via Ollama) responds:\n{response}")

if __name__ == "__main__":
    test_ollama_chat()