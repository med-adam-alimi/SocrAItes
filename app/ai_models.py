import os
from typing import Dict, List, Any
import uuid

class AIPhilosopherChat:
    """Enhanced philosopher chat using AI generation"""
    
    def __init__(self):
        """Initialize with AI-enhanced RAG engine."""
        print("🤖 Starting AI-Enhanced Philosopher Chat...")
        
        from app.utils.ai_rag_engine import AIEnhancedRAGEngine
        self.rag_engine = AIEnhancedRAGEngine()
        
        self.conversation_history = {}
        print("✅ AI Philosopher Chat ready!")
    
    def generate_response(
        self, 
        user_message: str, 
        philosopher: str, 
        context: List[str], 
        conversation_id: str
    ) -> Dict[str, Any]:
        """Generate AI-powered response with RAG context."""
        
        try:
            # Get enhanced context from RAG engine
            enhanced_context = self.rag_engine.retrieve_context(user_message, philosopher)
            
            # Combine with any additional context provided
            full_context = enhanced_context + (context if context else [])
            
            # Generate AI response
            response_data = self.rag_engine.generate_ai_response(
                user_message, 
                philosopher, 
                full_context
            )
            
            # Update conversation history
            if conversation_id not in self.conversation_history:
                self.conversation_history[conversation_id] = []
            
            self.conversation_history[conversation_id].append({
                "role": "user", 
                "content": user_message
            })
            self.conversation_history[conversation_id].append({
                "role": "assistant", 
                "content": response_data['message']
            })
            
            # Keep only last 6 messages to avoid memory issues
            if len(self.conversation_history[conversation_id]) > 6:
                self.conversation_history[conversation_id] = self.conversation_history[conversation_id][-6:]
            
            return response_data
            
        except Exception as e:
            print(f"Error in AI response generation: {e}")
            return {
                'message': "I apologize, but I'm having difficulty responding right now. This question touches on deep philosophical themes that deserve careful consideration. Perhaps we could explore it from a different angle?",
                'sources': [],
                'philosopher': philosopher,
                'generated_by': 'error_fallback'
            }
    
    def clear_conversation(self, conversation_id: str):
        """Clear conversation history for a given ID."""
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id]
            print(f"Cleared conversation {conversation_id}")
    
    def get_philosopher_greeting(self, philosopher: str) -> str:
        """Get personalized greeting for philosopher."""
        greetings = {
            'camus': "Welcome, fellow seeker of the absurd. In a world without inherent meaning, what profound questions weigh on your mind today?",
            'dostoevsky': "Ah, another soul wrestling with the complexities of existence. The human heart is a mysterious labyrinth - what moral or psychological depths shall we explore?",
            'nietzsche': "What does not destroy you makes you stronger! I sense you wish to overcome something, to become who you truly are. What conventional wisdom shall we shatter today?",
            'neutral': "Welcome to the realm of philosophical inquiry! I'm here to guide you through the profound questions that have shaped human thought for millennia. What would you like to explore?"
        }
        return greetings.get(philosopher, greetings['neutral'])
    
    def get_conversation_context(self, conversation_id: str) -> List[Dict[str, str]]:
        """Get recent conversation history for context."""
        return self.conversation_history.get(conversation_id, [])[-4:]  # Last 4 exchanges