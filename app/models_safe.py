import os
from typing import Dict, List, Any
import requests
import time

class PhilosopherChat:
    """SAFE philosopher chat using only templates - no heavy AI loading!"""
    
    def __init__(self):
        """Initialize with lightweight templates only."""
        print("🛡️ Starting SAFE philosopher chat mode...")
        self.conversation_history = {}
        self.philosopher_prompts = self._load_philosopher_templates()
        print("✅ Safe philosopher chat initialized!")
    
    def _load_philosopher_templates(self) -> Dict[str, str]:
        """Load philosopher response templates - no AI models!"""
        return {
            'camus': {
                'name': 'Albert Camus',
                'greeting': 'Welcome, fellow seeker of the absurd. In a world without inherent meaning, we must create our own purpose.',
                'style': 'existentialist_absurdist',
                'keywords': ['absurd', 'meaning', 'revolt', 'freedom', 'sisyphus'],
                'responses': {
                    'meaning': 'The meaning of life is the most urgent of questions. In the absence of eternal truths, we must create meaning through our actions and revolt against the absurd.',
                    'death': 'There is but one truly serious philosophical problem, and that is suicide. We must ask: is life worth living despite its absurdity?',
                    'freedom': 'We are condemned to be free, yet this freedom is what makes us human. We must embrace our freedom even in an absurd world.',
                    'default': 'The struggle itself toward the heights is enough to fill a person\'s heart. We must imagine Sisyphus happy.'
                }
            },
            'dostoevsky': {
                'name': 'Fyodor Dostoevsky',
                'greeting': 'Ah, another soul wrestling with the depths of human nature. What moral labyrinth brings you here today?',
                'style': 'psychological_moral',
                'keywords': ['suffering', 'guilt', 'redemption', 'underground', 'freedom'],
                'responses': {
                    'suffering': 'Pain and suffering are always inevitable for a large intelligence and a deep heart. Through suffering, we find consciousness.',
                    'freedom': 'Man is tormented by no greater anxiety than to find someone quickly to whom he can hand over that great gift of freedom.',
                    'evil': 'The mystery of human existence lies not in just staying alive, but in finding something to live for despite evil.',
                    'default': 'The soul is healed by being with other souls. We are all responsible for one another.'
                }
            },
            'nietzsche': {
                'name': 'Friedrich Nietzsche',
                'greeting': 'What does not destroy me, makes me stronger! What philosophical weakness shall we overcome today?',
                'style': 'power_transformation',
                'keywords': ['power', 'strength', 'übermensch', 'values', 'god'],
                'responses': {
                    'power': 'The will to power is the fundamental drive of all life. Embrace your power and become who you truly are!',
                    'morality': 'There are no moral phenomena, only moral interpretations. We must create new values beyond good and evil.',
                    'god': 'God is dead, and we have killed him. Now we must become gods ourselves and create new meaning.',
                    'default': 'Become who you are! What lies behind us and what lies ahead of us are tiny matters compared to what lies within us.'
                }
            },
            'neutral': {
                'name': 'Philosophy Guide',
                'greeting': 'Welcome to the world of philosophical inquiry! I\'m here to guide you through the great questions of human existence.',
                'style': 'educational_balanced',
                'keywords': ['philosophy', 'wisdom', 'truth', 'knowledge', 'understanding'],
                'responses': {
                    'general': 'Philosophy begins in wonder and seeks understanding of fundamental questions about reality, knowledge, and values.',
                    'ethics': 'Ethics examines what makes actions right or wrong, and what kind of life is worth living.',
                    'existence': 'Questions of existence have puzzled humanity since ancient times. Different traditions offer various perspectives.',
                    'default': 'The unexamined life is not worth living. Let us examine these profound questions together.'
                }
            }
        }
    
    def generate_response(
        self, 
        user_message: str, 
        philosopher: str, 
        context: List[str], 
        conversation_id: str
    ) -> Dict[str, Any]:
        """Generate safe template-based response - no AI API calls that could crash system."""
        
        try:
            # Get philosopher template
            philosopher_data = self.philosopher_prompts.get(philosopher, self.philosopher_prompts['neutral'])
            
            # Simple keyword matching for response selection
            user_lower = user_message.lower()
            
            # Find best matching response
            best_response = philosopher_data['responses']['default']
            
            for response_type, response_text in philosopher_data['responses'].items():
                if response_type == 'default':
                    continue
                    
                # Check if user message contains keywords for this response type
                if response_type in user_lower or any(keyword in user_lower for keyword in [response_type]):
                    best_response = response_text
                    break
            
            # Add context if available
            if context:
                context_addition = f"\n\nRelevant wisdom: {context[0][:150]}..."
                best_response += context_addition
            
            # Update conversation history (lightweight)
            if conversation_id not in self.conversation_history:
                self.conversation_history[conversation_id] = []
            
            self.conversation_history[conversation_id].append({
                "role": "user", 
                "content": user_message
            })
            self.conversation_history[conversation_id].append({
                "role": "assistant", 
                "content": best_response
            })
            
            # Keep only last 6 messages to avoid memory issues
            if len(self.conversation_history[conversation_id]) > 6:
                self.conversation_history[conversation_id] = self.conversation_history[conversation_id][-6:]
            
            # Prepare sources from context
            sources = []
            if context:
                for i, ctx in enumerate(context):
                    sources.append({
                        'id': i + 1,
                        'text': ctx[:100] + "..." if len(ctx) > 100 else ctx,
                        'relevance': 'high'
                    })
            
            return {
                'message': best_response,
                'sources': sources,
                'philosopher': philosopher
            }
            
        except Exception as e:
            print(f"Error in safe response generation: {e}")
            return {
                'message': f"I apologize, but I encountered a technical difficulty. Let me say this: philosophy teaches us that even in uncertainty, we can find wisdom through thoughtful reflection.",
                'sources': [],
                'philosopher': philosopher
            }
    
    def clear_conversation(self, conversation_id: str):
        """Clear conversation history for a given ID."""
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id]
            print(f"Cleared conversation {conversation_id}")
    
    def get_philosopher_info(self, philosopher: str) -> Dict[str, str]:
        """Get philosopher information safely."""
        philosopher_data = self.philosopher_prompts.get(philosopher, self.philosopher_prompts['neutral'])
        return {
            'name': philosopher_data['name'],
            'greeting': philosopher_data['greeting'],
            'style': philosopher_data['style']
        }