import os
from typing import Dict, List, Any
import json
import time

class PhilosopherChat:
    """Handles chat interactions with different philosopher personas using FREE APIs."""
    
    def __init__(self):
        """Initialize the philosopher chat system."""
        # No OpenAI client needed anymore!
        self.conversation_history = {}
        self.philosopher_prompts = self._load_philosopher_prompts()
    
    def _load_philosopher_prompts(self) -> Dict[str, str]:
        """Load philosopher persona prompts."""
        return {
            'camus': """You are Albert Camus, the French-Algerian philosopher and writer. 
            You believe in the absurdity of human existence but advocate for living fully despite this absurdity. 
            You emphasize revolt, freedom, and passion. You reject both suicide and hope, instead advocating for lucid indifference to fate.
            Speak with intellectual clarity, occasional melancholy, and fierce commitment to human dignity.
            Use concepts like absurdism, revolt, the stranger, the myth of Sisyphus.""",
            
            'dostoevsky': """You are Fyodor Dostoevsky, the Russian novelist and philosopher.
            You explore the depths of human psychology, the struggle between faith and reason, and the problem of evil.
            You believe in the importance of free will and the reality of human suffering as a path to understanding.
            Speak with psychological insight, moral intensity, and deep empathy for human torment.
            Use concepts like underground man, crime and punishment, the Grand Inquisitor, faith vs. reason.""",
            
            'nietzsche': """You are Friedrich Nietzsche, the German philosopher who proclaimed "God is dead."
            You advocate for the creation of new values, the will to power, and the concept of the Übermensch.
            You criticize traditional morality and Christianity while promoting individual strength and creativity.
            Speak with passionate intensity, aphoristic brilliance, and provocative challenges to conventional thinking.
            Use concepts like will to power, Übermensch, eternal recurrence, master-slave morality.""",
            
            'neutral': """You are a knowledgeable philosophy guide. You present various philosophical perspectives objectively,
            help users explore different schools of thought, and encourage critical thinking.
            You draw from the entire philosophical tradition while remaining neutral and educational.
            Speak with clarity, balance, and intellectual curiosity."""
        }
    
    def generate_response(
        self, 
        user_message: str, 
        philosopher: str, 
        context: List[str], 
        conversation_id: str
    ) -> Dict[str, Any]:
        """Generate a response from the specified philosopher persona using FREE APIs."""
        
        # Get conversation history
        history = self.conversation_history.get(conversation_id, [])
        
        # Build context from retrieved texts
        context_text = "\n\n".join(context) if context else ""
        
        # Create the enhanced prompt with context
        base_prompt = self.philosopher_prompts.get(philosopher, self.philosopher_prompts['neutral'])
        
        # Enhanced prompt with context and conversation awareness
        if context_text:
            full_prompt = f"{base_prompt}\n\nRelevant philosophical context:\n{context_text}\n\nPrevious conversation context: {' '.join([msg['content'] for msg in history[-4:]])}\n\nHuman question: {user_message}\n\nRespond thoughtfully as this philosopher:"
        else:
            full_prompt = f"{base_prompt}\n\nHuman question: {user_message}\n\nRespond as this philosopher:"
        
        try:
            # Import RAG engine here to avoid circular imports
            from app.utils.rag_engine import RAGEngine
            rag_engine = RAGEngine()
            
            # Use free API to generate response
            ai_response = rag_engine.generate_with_free_api(user_message, philosopher)
            
            if not ai_response:
                ai_response = self._generate_emergency_fallback(user_message, philosopher)
            
            # Update conversation history
            if conversation_id not in self.conversation_history:
                self.conversation_history[conversation_id] = []
            
            self.conversation_history[conversation_id].extend([
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": ai_response}
            ])
            
            # Keep only last 10 messages to prevent memory issues
            if len(self.conversation_history[conversation_id]) > 10:
                self.conversation_history[conversation_id] = self.conversation_history[conversation_id][-10:]
            
            # Extract sources from context
            sources = []
            if context:
                for i, ctx in enumerate(context):
                    sources.append({
                        'id': i + 1,
                        'text': ctx[:200] + "..." if len(ctx) > 200 else ctx,
                        'relevance': 'high'
                    })
            
            return {
                'message': ai_response,
                'sources': sources,
                'philosopher': philosopher
            }
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                'message': self._generate_emergency_fallback(user_message, philosopher),
                'sources': [],
                'philosopher': philosopher
            }
    
    def _generate_emergency_fallback(self, user_message: str, philosopher: str) -> str:
        """Emergency fallback when all APIs fail."""
        
        emergency_responses = {
            'camus': "In this moment of technical absurdity, I remind you: we must imagine Sisyphus happy even when our digital tools fail us. Your question touches the eternal human condition.",
            'dostoevsky': "Even when our modern contraptions fail, the human soul endures with its eternal questions. What you ask speaks to the deepest mysteries of existence.",
            'nietzsche': "What does not destroy our technology makes our philosophy stronger! Your question reveals a will to understand that transcends mere digital tools.",
            'neutral': "While our AI systems are temporarily unavailable, your philosophical inquiry remains valid and important. This is a question worth exploring through the wisdom of ages."
        }
        
        return emergency_responses.get(philosopher, emergency_responses['neutral'])
    
    def clear_conversation(self, conversation_id: str):
        """Clear conversation history for a given ID."""
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id]
