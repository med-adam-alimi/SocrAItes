#!/usr/bin/env python3
"""
LangChain-powered Philosophy Chatbot with Internet RAG
Uses professional APIs for high-quality conversational AI
"""

import os
from typing import List, Dict, Any
from dataclasses import dataclass

# LangChain imports
try:
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI, ChatAnthropic
    from langchain.schema import SystemMessage, HumanMessage
    from langchain.prompts import ChatPromptTemplate, PromptTemplate
    from langchain.chains import LLMChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

from app.utils.internet_rag_engine import InternetRAGEngine

@dataclass
class PhilosopherPersona:
    name: str
    style: str
    key_concepts: List[str]
    speaking_pattern: str

class LangChainPhilosopherChat:
    """
    Advanced Philosophy Chatbot using LangChain for human-like responses
    Combines internet RAG with professional LLM generation
    """
    
    def __init__(self):
        self.search_engine = InternetRAGEngine()
        self.setup_llm()
        self.setup_personas()
        
    def setup_llm(self):
        """Initialize LangChain LLM with multiple provider options"""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain not installed. Run: pip install langchain openai anthropic")
            
        # Try OpenAI first (most reliable)
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0.7,
                max_tokens=1000,
                openai_api_key=openai_key
            )
            self.provider = "OpenAI"
            return
            
        # Try Anthropic as backup
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            self.llm = ChatAnthropic(
                model="claude-3-sonnet-20240229",
                temperature=0.7,
                max_tokens=1000,
                anthropic_api_key=anthropic_key
            )
            self.provider = "Anthropic"
            return
            
        raise ValueError("No API keys found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    
    def setup_personas(self):
        """Define philosopher personalities for authentic responses"""
        self.personas = {
            'camus': PhilosopherPersona(
                name="Albert Camus",
                style="Existentialist, absurdist, direct and passionate",
                key_concepts=["absurd", "rebellion", "freedom", "authenticity"],
                speaking_pattern="Direct, passionate, uses metaphors of rocks and mountains"
            ),
            'nietzsche': PhilosopherPersona(
                name="Friedrich Nietzsche",
                style="Bold, provocative, aphoristic",
                key_concepts=["will to power", "eternal recurrence", "übermensch"],
                speaking_pattern="Dramatic, uses exclamations, challenges conventional thinking"
            ),
            'dostoevsky': PhilosopherPersona(
                name="Fyodor Dostoevsky",
                style="Psychological depth, moral complexity",
                key_concepts=["suffering", "redemption", "free will", "faith"],
                speaking_pattern="Deep psychological insight, explores moral dilemmas"
            )
        }
    
    def create_philosophical_prompt(self, question: str, persona_name: str, context: List[Dict]) -> List:
        """Create a sophisticated prompt for philosophical conversation"""
        persona = self.personas.get(persona_name, self.personas['camus'])
        
        # Extract key content from internet sources
        context_text = self._format_context(context)
        
        system_prompt = f"""You are {persona.name}, the renowned philosopher. Your response style is: {persona.style}.

Your key philosophical concepts include: {', '.join(persona.key_concepts)}.
Your speaking pattern: {persona.speaking_pattern}.

You have access to current internet discussions about philosophy. Use this context to inform your response, but speak authentically as {persona.name} would.

Current internet context about the topic:
{context_text}

Rules:
1. Respond as {persona.name} would, using his philosophical framework
2. Incorporate insights from the internet context naturally
3. Be conversational and engaging, not academic
4. Show the relevance of your philosophy to modern issues
5. Keep responses focused and thoughtful (200-400 words)
"""

        return [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]
    
    def _format_context(self, sources: List[Dict]) -> str:
        """Format internet sources into readable context"""
        if not sources:
            return "No specific internet context available."
            
        context_parts = []
        for i, source in enumerate(sources[:5], 1):  # Use top 5 sources
            title = source.get('title', 'Unknown')
            content = source.get('content', '')[:200]  # Limit content length
            source_name = source.get('source', 'Unknown source')
            
            context_parts.append(f"{i}. From {source_name}: '{title}'\n   {content}...")
            
        return "\n\n".join(context_parts)
    
    def chat(self, question: str, persona: str = 'camus') -> str:
        """Generate philosophical response using internet context and LangChain"""
        try:
            # Step 1: Get internet context
            print(f"🔍 Searching internet for: {question}")
            internet_sources = self.search_engine.search_philosophy_content(question)
            print(f"✅ Found {len(internet_sources)} sources")
            
            # Step 2: Create sophisticated prompt
            messages = self.create_philosophical_prompt(question, persona, internet_sources)
            
            # Step 3: Generate response with LangChain
            print(f"🤖 Generating response with {self.provider}...")
            response = self.llm(messages)
            
            # Extract content based on response type
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
                
        except Exception as e:
            print(f"❌ LangChain generation failed: {e}")
            return self._fallback_response(question, persona, internet_sources)
    
    def _fallback_response(self, question: str, persona: str, sources: List[Dict]) -> str:
        """Fallback when LangChain fails"""
        persona_obj = self.personas.get(persona, self.personas['camus'])
        
        if sources:
            context = sources[0].get('content', '')[:300]
            return f"""As {persona_obj.name}, I find this question fascinating. 
            
Based on current discussions I've encountered: {context}...

From my philosophical perspective: {question} touches on the core of {', '.join(persona_obj.key_concepts[:2])}. 

{persona_obj.speaking_pattern} Let me explore this further with you."""
        
        return f"As {persona_obj.name}, this question about '{question}' is precisely what philosophy should address..."

# Example usage and testing
if __name__ == "__main__":
    print("🚀 Testing LangChain Philosophy Chatbot")
    print("=" * 50)
    
    try:
        chat = LangChainPhilosopherChat()
        
        test_question = "What does modern philosophy say about artificial intelligence and consciousness?"
        response = chat.chat(test_question, 'camus')
        
        print(f"Question: {test_question}")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Setup failed: {e}")
        print("Please install: pip install langchain openai anthropic")
        print("And set your API keys in .env file")