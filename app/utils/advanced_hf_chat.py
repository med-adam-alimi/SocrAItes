#!/usr/bin/env python3
"""
Advanced Hugging Face Philosophy Chatbot with Internet RAG
Uses multiple HF models for reliable conversational AI generation
"""

import os
import requests
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.utils.internet_rag_engine import InternetRAGEngine

@dataclass
class ModelConfig:
    name: str
    url: str
    max_tokens: int
    temperature: float
    style: str

class HuggingFacePhilosopherChat:
    """
    Advanced Philosophy Chatbot using Hugging Face models
    Multiple model fallbacks for reliability
    """
    
    def __init__(self):
        self.search_engine = InternetRAGEngine()
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment")
            
        self.setup_models()
        self.setup_personas()
        
    def setup_models(self):
        """Setup multiple HF models with fallbacks"""
        base_url = "https://api-inference.huggingface.co/models"
        
        self.models = [
            # Primary models - larger and more capable
            ModelConfig(
                name="microsoft/DialoGPT-large",
                url=f"{base_url}/microsoft/DialoGPT-large",
                max_tokens=500,
                temperature=0.7,
                style="conversational"
            ),
            ModelConfig(
                name="mistralai/Mistral-7B-Instruct-v0.1",
                url=f"{base_url}/mistralai/Mistral-7B-Instruct-v0.1",
                max_tokens=800,
                temperature=0.6,
                style="instruction-following"
            ),
            ModelConfig(
                name="google/flan-t5-large",
                url=f"{base_url}/google/flan-t5-large",
                max_tokens=400,
                temperature=0.8,
                style="text-generation"
            ),
            # Backup models
            ModelConfig(
                name="facebook/blenderbot-400M-distill",
                url=f"{base_url}/facebook/blenderbot-400M-distill",
                max_tokens=300,
                temperature=0.7,
                style="conversational"
            )
        ]
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def setup_personas(self):
        """Define philosopher personalities"""
        self.personas = {
            'camus': {
                'name': 'Albert Camus',
                'style': 'existentialist and absurdist',
                'traits': 'direct, passionate, uses metaphors',
                'concepts': 'absurd, rebellion, authenticity, freedom'
            },
            'nietzsche': {
                'name': 'Friedrich Nietzsche',
                'style': 'bold and provocative',
                'traits': 'dramatic, challenging, aphoristic',
                'concepts': 'will to power, eternal recurrence, übermensch'
            },
            'dostoevsky': {
                'name': 'Fyodor Dostoevsky',
                'style': 'psychologically deep',
                'traits': 'moral complexity, spiritual insight',
                'concepts': 'suffering, redemption, free will, faith'
            }
        }
    
    def create_philosophical_prompt(self, question: str, persona_name: str, context: List[Dict]) -> str:
        """Create a sophisticated prompt for the HF model"""
        persona = self.personas.get(persona_name, self.personas['camus'])
        
        # Format internet context
        context_text = self._format_context(context)
        
        prompt = f"""You are {persona['name']}, the renowned philosopher. 

Your philosophical style: {persona['style']}
Your speaking traits: {persona['traits']}
Your key concepts: {persona['concepts']}

Current internet discussions about this topic:
{context_text}

Human asks: "{question}"

Respond as {persona['name']} would, incorporating both your philosophical framework and insights from the current discussions. Be conversational, engaging, and authentic to your philosophical style.

{persona['name']} responds:"""

        return prompt
    
    def _format_context(self, sources: List[Dict]) -> str:
        """Format internet sources for the prompt"""
        if not sources:
            return "No current internet context available."
            
        context_parts = []
        for i, source in enumerate(sources[:3], 1):  # Use top 3 sources
            title = source.get('title', 'Unknown')[:60]
            content = source.get('content', '')[:150]
            
            context_parts.append(f"{i}. {title}: {content}...")
            
        return "\n".join(context_parts)
    
    def query_huggingface_model(self, model: ModelConfig, prompt: str) -> Optional[str]:
        """Query a specific HF model with error handling"""
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": model.max_tokens,
                    "temperature": model.temperature,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            print(f"🤖 Trying {model.name}...")
            response = requests.post(
                model.url, 
                headers=self.headers, 
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        text = result[0]['generated_text']
                    elif 'generated_text' in result:
                        text = result['generated_text']
                    else:
                        text = str(result[0])
                else:
                    text = str(result)
                
                # Clean up the response
                text = self._clean_response(text, prompt)
                if len(text) > 50:  # Valid response
                    print(f"✅ Success with {model.name}")
                    return text
                    
            elif response.status_code == 503:
                print(f"⏳ {model.name} is loading, trying next model...")
            else:
                print(f"❌ {model.name} failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error with {model.name}: {e}")
            
        return None
    
    def _clean_response(self, text: str, original_prompt: str) -> str:
        """Clean and format the model response"""
        # Remove the original prompt if it's repeated
        if original_prompt in text:
            text = text.replace(original_prompt, "").strip()
        
        # Remove common artifacts
        text = text.strip()
        
        # Split by common delimiters and take the first substantial part
        for delimiter in ['\n\nHuman:', '\n\nUser:', '###', 'Question:']:
            if delimiter in text:
                text = text.split(delimiter)[0].strip()
        
        return text
    
    def chat(self, question: str, persona: str = 'camus') -> str:
        """Generate philosophical response using HF models with internet context"""
        try:
            # Step 1: Get internet context
            print(f"🔍 Searching internet for: {question}")
            internet_sources = self.search_engine.search_philosophy_content(question)
            print(f"✅ Found {len(internet_sources)} sources")
            
            # Step 2: Create sophisticated prompt
            prompt = self.create_philosophical_prompt(question, persona, internet_sources)
            
            # Step 3: Try models in order until one works
            for model in self.models:
                response = self.query_huggingface_model(model, prompt)
                if response:
                    return response
                time.sleep(1)  # Brief pause between attempts
            
            # If all models fail, use enhanced fallback
            print("⚠️ All HF models failed, using enhanced fallback")
            return self._create_enhanced_fallback(question, persona, internet_sources)
            
        except Exception as e:
            print(f"❌ Complete system failure: {e}")
            return self._create_basic_fallback(question, persona)
    
    def _create_enhanced_fallback(self, question: str, persona: str, sources: List[Dict]) -> str:
        """Create intelligent fallback using internet content"""
        persona_info = self.personas.get(persona, self.personas['camus'])
        
        # Use internet content to create response
        if sources:
            key_content = sources[0].get('content', '')[:200]
            
            response = f"""As {persona_info['name']}, I find your question about "{question}" deeply relevant to our current times.

From what I observe in contemporary discussions: {key_content}...

Through the lens of my {persona_info['style']} philosophy, particularly my focus on {persona_info['concepts']}, I would say:

This question touches the very core of human existence. {persona_info['traits']} - we must examine not just the surface, but the fundamental implications for how we live authentically.

What strikes me most is how this modern concern echoes the eternal questions I've always explored. The absurd nature of existence remains, whether we face traditional dilemmas or new technological ones."""

            return response
        
        return self._create_basic_fallback(question, persona)
    
    def _create_basic_fallback(self, question: str, persona: str) -> str:
        """Basic fallback when everything fails"""
        persona_info = self.personas.get(persona, self.personas['camus'])
        
        return f"""As {persona_info['name']}, I approach your question "{question}" through my {persona_info['style']} perspective.

This inquiry embodies the essential human struggle to understand {persona_info['concepts']}. 

{persona_info['traits']} - I believe we must confront such questions directly, without illusion or false comfort.

The answer lies not in simple formulas, but in how we choose to live authentically in the face of uncertainty."""

# Testing function
def test_hf_chat():
    """Test the HF chatbot system"""
    print("🚀 Testing Hugging Face Philosophy Chatbot")
    print("=" * 60)
    
    try:
        chat = HuggingFacePhilosopherChat()
        
        test_questions = [
            "What is the meaning of life in the digital age?",
            "How should we think about artificial intelligence?",
            "What would you say about modern anxiety and technology?"
        ]
        
        for question in test_questions:
            print(f"\n📝 Question: {question}")
            print("-" * 40)
            
            response = chat.chat(question, 'camus')
            print(f"🤖 Camus responds: {response}")
            print()
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_hf_chat()