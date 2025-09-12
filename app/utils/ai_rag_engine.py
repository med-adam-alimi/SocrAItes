import requests
import json
import os
import time
from typing import List, Dict, Any

class AIEnhancedRAGEngine:
    """Enhanced RAG engine with REAL AI generation using FREE Hugging Face API"""
    
    def __init__(self):
        """Initialize with free AI generation capabilities."""
        print("🤖 Initializing AI-Enhanced RAG Engine...")
        
        # Get API configuration
        self.api_type = os.environ.get('API_TYPE', 'huggingface')
        self.hf_token = os.environ.get('HUGGINGFACE_API_KEY', '')
        
        # Hugging Face Free API endpoints
        self.hf_endpoints = {
            'conversational': 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-large',
            'text_generation': 'https://api-inference.huggingface.co/models/gpt2',
            'philosophy_model': 'https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-1.3B'
        }
        
        # Headers for API calls
        self.headers = {
            'Authorization': f'Bearer {self.hf_token}',
            'Content-Type': 'application/json'
        }
        
        # Load philosophy knowledge base
        self._load_philosophy_database()
        
        # Load text chunks for RAG
        self._load_text_chunks()
        
        print("✅ AI-Enhanced RAG Engine ready!")
    
    def _load_philosophy_database(self):
        """Load comprehensive philosophy knowledge base"""
        self.philosophy_db = {
            "existentialism": {
                "definition": "Philosophy emphasizing individual existence, freedom, and choice",
                "key_figures": ["Sartre", "Camus", "Heidegger", "Kierkegaard"],
                "core_concepts": [
                    "Existence precedes essence",
                    "Radical freedom and responsibility",
                    "Authenticity vs bad faith",
                    "Anxiety as fundamental condition"
                ],
                "famous_quotes": [
                    "Existence precedes essence - Jean-Paul Sartre",
                    "Hell is other people - Jean-Paul Sartre",
                    "Life can only be understood backwards - Kierkegaard"
                ]
            },
            "absurdism": {
                "definition": "The conflict between human desire for meaning and the meaningless universe",
                "key_figures": ["Camus"],
                "core_concepts": [
                    "The absurd condition",
                    "Revolt against meaninglessness", 
                    "Living without hope or despair",
                    "Creating meaning through action"
                ],
                "famous_quotes": [
                    "The struggle itself toward the heights is enough to fill a man's heart - Camus",
                    "One must imagine Sisyphus happy - Camus",
                    "In the midst of winter, I found an invincible summer - Camus"
                ]
            },
            "nihilism": {
                "definition": "The view that life lacks objective meaning, purpose, or intrinsic value",
                "key_figures": ["Nietzsche", "Dostoevsky"],
                "core_concepts": [
                    "Rejection of moral principles",
                    "Meaninglessness of existence",
                    "Death of God",
                    "Will to power as response"
                ],
                "famous_quotes": [
                    "God is dead and we have killed him - Nietzsche",
                    "What does not kill me makes me stronger - Nietzsche",
                    "Become who you are - Nietzsche"
                ]
            },
            "ethics": {
                "definition": "Study of moral principles governing behavior",
                "key_figures": ["Kant", "Mill", "Aristotle", "Dostoevsky"],
                "core_concepts": [
                    "Categorical imperative",
                    "Utilitarianism",
                    "Virtue ethics",
                    "Moral responsibility"
                ],
                "famous_quotes": [
                    "Act only according to maxims you could will to be universal laws - Kant",
                    "The greatest happiness for the greatest number - Mill"
                ]
            }
        }
    
    def _load_text_chunks(self):
        """Load processed text chunks for retrieval"""
        chunks_path = os.environ.get('CHUNKS_PATH', 'data/processed/chunks.json')
        try:
            if os.path.exists(chunks_path):
                with open(chunks_path, 'r', encoding='utf-8') as f:
                    self.chunks = json.load(f)
                print(f"✅ Loaded {len(self.chunks)} philosophy text chunks")
            else:
                self._create_enhanced_sample_chunks()
        except Exception as e:
            print(f"⚠️ Error loading chunks: {e}")
            self._create_enhanced_sample_chunks()
    
    def _create_enhanced_sample_chunks(self):
        """Create enhanced philosophical content chunks"""
        self.chunks = [
            {
                'text': '''The absurd is born of this confrontation between the human need and the unreasonable silence of the world. 
                The absurd depends as much on man as on the world. It is all that links them together. The absurd is not in man nor in the world, 
                but in their presence together. The feeling of the absurd is not, for all that, the notion of the absurd.''',
                'philosopher': 'camus',
                'source': 'The Myth of Sisyphus',
                'topic': 'absurdism',
                'id': 0
            },
            {
                'text': '''I am a sick man... I am a spiteful man. I am an unattractive man. I believe my liver is diseased. 
                However, I know nothing at all about my disease, and do not know for certain what ails me. The most direct and 
                straightforward thing is simply to destroy everything. Pain and suffering are always inevitable for a large intelligence and a deep heart.''',
                'philosopher': 'dostoevsky',
                'source': 'Notes from Underground',
                'topic': 'psychology',
                'id': 1
            },
            {
                'text': '''What does not kill me, makes me stronger. God is dead. God remains dead. And we have killed him. 
                There is master morality and slave morality. The individual has always had to struggle not to be overwhelmed by the tribe. 
                Become who you are. One must have chaos within oneself to give birth to a dancing star.''',
                'philosopher': 'nietzsche',
                'source': 'Beyond Good and Evil',
                'topic': 'nihilism',
                'id': 2
            },
            {
                'text': '''Existence precedes essence. Man is condemned to be free; because once thrown into the world, 
                he is responsible for everything he does. Hell is other people. Bad faith is the act of deceiving oneself 
                by pretending that one lacks the freedom to make fundamental choices about one's life.''',
                'philosopher': 'sartre',
                'source': 'Being and Nothingness',
                'topic': 'existentialism',
                'id': 3
            },
            {
                'text': '''The most painful state of being is remembering the future, particularly the one you'll never have. 
                Life can only be understood backwards; but it must be lived forwards. The function of prayer is not to 
                influence God, but rather to change the nature of the one who prays.''',
                'philosopher': 'kierkegaard',
                'source': 'Fear and Trembling',
                'topic': 'existentialism',
                'id': 4
            },
            {
                'text': '''The soul is healed by being with other souls. We are all responsible for one another. 
                If you want to be happy, be. The mystery of human existence lies not in just staying alive, 
                but in finding something to live for.''',
                'philosopher': 'dostoevsky',
                'source': 'The Brothers Karamazov',
                'topic': 'ethics',
                'id': 5
            }
        ]
        print("✅ Created enhanced sample philosophy chunks")
    
    def retrieve_context(self, query: str, philosopher: str = None, top_k: int = 3) -> List[str]:
        """Enhanced context retrieval with topic matching"""
        query_lower = query.lower()
        relevant_contexts = []
        
        # 1. Search philosophy database by topic
        for topic, content in self.philosophy_db.items():
            if any(concept.lower() in query_lower for concept in content['core_concepts']):
                relevant_contexts.append(f"PHILOSOPHICAL CONCEPT - {topic.upper()}: {content['definition']}")
                relevant_contexts.extend(content['famous_quotes'][:2])
        
        # 2. Search text chunks with advanced matching
        chunk_scores = []
        for chunk in self.chunks:
            score = 0
            chunk_text = chunk['text'].lower()
            
            # Keyword matching
            query_words = query_lower.split()
            for word in query_words:
                if word in chunk_text:
                    score += 1
            
            # Philosopher preference
            if philosopher and philosopher != 'neutral':
                if chunk.get('philosopher', '').lower() == philosopher.lower():
                    score += 5
            
            # Topic matching
            chunk_topic = chunk.get('topic', '')
            if any(topic in query_lower for topic in [chunk_topic, 'meaning', 'existence', 'death', 'freedom']):
                score += 3
            
            if score > 0:
                chunk_scores.append((score, chunk['text'], chunk.get('source', 'Unknown')))
        
        # Sort by relevance and add to context
        chunk_scores.sort(key=lambda x: x[0], reverse=True)
        for score, text, source in chunk_scores[:top_k]:
            relevant_contexts.append(f"FROM {source}: {text}")
        
        return relevant_contexts[:top_k + 2]  # Return top contexts
    
    def generate_ai_response(self, user_input: str, philosopher: str, context: List[str]) -> Dict[str, Any]:
        """Generate response using Hugging Face API with enhanced prompting"""
        
        # Check if API is configured
        if not self.hf_token or self.hf_token == 'your_free_hf_token_here':
            return self._generate_fallback_response(user_input, philosopher, context)
        
        try:
            # Prepare context
            context_text = "\n\n".join(context) if context else "No specific context available."
            
            # Enhanced philosopher personas
            personas = {
                'camus': {
                    'name': 'Albert Camus',
                    'description': 'French-Algerian philosopher, Nobel Prize winner, advocate of absurdism',
                    'style': 'passionate, clear, uses concrete metaphors, focuses on human dignity',
                    'approach': 'Emphasize the absurd condition, revolt against meaninglessness, and creating meaning through action'
                },
                'dostoevsky': {
                    'name': 'Fyodor Dostoevsky',
                    'description': 'Russian novelist and philosopher, explorer of human psychology',
                    'style': 'intense, psychologically deep, morally complex, empathetic',
                    'approach': 'Explore psychological depths, moral dilemmas, suffering as path to consciousness'
                },
                'nietzsche': {
                    'name': 'Friedrich Nietzsche',
                    'description': 'German philosopher, critic of traditional morality, advocate of will to power',
                    'style': 'bold, provocative, aphoristic, challenging conventional thinking',
                    'approach': 'Challenge traditional values, promote individual strength and self-creation'
                },
                'neutral': {
                    'name': 'Philosophy Guide',
                    'description': 'Knowledgeable guide through philosophical traditions',
                    'style': 'clear, balanced, educational, connecting different perspectives',
                    'approach': 'Present multiple viewpoints while encouraging critical thinking'
                }
            }
            
            persona_info = personas.get(philosopher, personas['neutral'])
            
            # Create comprehensive prompt
            prompt = f"""You are {persona_info['name']}, {persona_info['description']}.

PHILOSOPHICAL CONTEXT:
{context_text}

QUESTION FROM HUMAN: "{user_input}"

YOUR TASK: Respond as {persona_info['name']} would, with the following approach: {persona_info['approach']}

Your response style should be: {persona_info['style']}

Draw from the philosophical context provided above, but don't simply quote it. Instead, engage with the human's question thoughtfully and provide insights that reflect your philosophical perspective.

RESPONSE:"""

            # Call Hugging Face API
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.8,
                    "do_sample": True,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                }
            }
            
            print("🤖 Calling Hugging Face API...")
            response = requests.post(
                self.hf_endpoints['philosophy_model'],
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ AI response generated successfully!")
                
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    
                    # Extract only the new response
                    if 'RESPONSE:' in generated_text:
                        ai_response = generated_text.split('RESPONSE:')[-1].strip()
                    else:
                        ai_response = generated_text.replace(prompt, '').strip()
                    
                    # Clean up response
                    ai_response = ai_response.replace('\n\n', '\n').strip()
                    
                    if ai_response and len(ai_response) > 10:
                        return {
                            'message': ai_response,
                            'sources': [{'text': ctx[:100] + '...' if len(ctx) > 100 else ctx, 'relevance': 'high'} for ctx in context[:3]],
                            'generated_by': 'huggingface_api'
                        }
            
            print(f"⚠️ API response issue: {response.status_code}")
            return self._generate_fallback_response(user_input, philosopher, context)
            
        except Exception as e:
            print(f"❌ Error calling AI API: {e}")
            return self._generate_fallback_response(user_input, philosopher, context)
    
    def _generate_fallback_response(self, user_input: str, philosopher: str, context: List[str]) -> Dict[str, Any]:
        """Enhanced fallback responses when API fails"""
        input_lower = user_input.lower()
        
        # Enhanced responses based on philosopher and topic
        responses = {
            'camus': {
                'meaning': '''The absurd is born of the confrontation between human need for meaning and the meaningless silence of the world. But we must not despair! We revolt against this meaninglessness not by escaping it, but by fully acknowledging it and choosing to live anyway. The struggle itself toward the heights is enough to fill a person's heart. One must imagine Sisyphus happy.''',
                'death': '''There is but one truly serious philosophical problem, and that is suicide. Judging whether life is or is not worth living amounts to answering the fundamental question of philosophy. I believe life is worth living precisely because it is absurd - we are free to create our own significance in defiance of meaninglessness.''',
                'freedom': '''In the face of an absurd world, we have three options: suicide, philosophical escape, or revolt. I choose revolt - not violent revolution, but the passionate affirmation of life despite its ultimate meaninglessness. This revolt is our freedom, our dignity, our way of saying 'yes' to existence.''',
                'suffering': '''There is scarcely any passion without struggle. The absurd man knows that in that consciousness and in that day-to-day revolt he gives proof of his only truth, which is defiance. Suffering is part of the human condition, but we must neither seek it nor flee from it - we must accept it as part of our absurd existence.'''
            },
            'dostoevsky': {
                'evil': '''The problem of evil cuts to the very heart of human existence. Why does innocent suffering exist if there is a loving God? This question tormented Ivan Karamazov, and it torments us all. Perhaps suffering is the price of consciousness, the cost of our free will, or perhaps through it we learn compassion and find our deepest humanity.''',
                'freedom': '''Man is tormented by no greater anxiety than to find someone quickly to whom he can hand over that great gift of freedom with which the ill-fated creature is born. We desperately want to be free, yet freedom terrifies us because it means taking full responsibility for our choices and their consequences.''',
                'love': '''The soul is healed by being with other souls. Love is the bridge between isolation and connection, between despair and hope. We are all responsible for one another, and through love and understanding, we find redemption and meaning in our shared humanity.''',
                'suffering': '''Pain and suffering are always inevitable for a large intelligence and a deep heart. But suffering is not meaningless - it is the sole origin of consciousness. Through suffering, we come to understand ourselves and develop compassion for others.'''
            },
            'nietzsche': {
                'power': '''The will to power is the fundamental driving force of all life. It is not mere domination over others, but the power to overcome oneself, to create values, to become who you truly are. What does not kill you makes you stronger - embrace your struggles as opportunities for growth.''',
                'morality': '''There are no moral phenomena, only moral interpretations of phenomena. Master morality creates values based on strength and nobility, while slave morality is reactive, based on resentment. We must move beyond good and evil to create new values for a new age.''',
                'god': '''God is dead, and we have killed him. This is not a cause for despair but for celebration - now we are free to become gods ourselves, to create our own values and meaning. The übermensch is one who creates values rather than merely following them.''',
                'existence': '''Become who you are! The individual has always had to struggle not to be overwhelmed by the tribe. You must have chaos within yourself to give birth to a dancing star. Embrace your uniqueness and create your own path.'''
            }
        }
        
        philosopher_responses = responses.get(philosopher, {})
        
        # Find best matching response
        best_response = None
        for topic, response in philosopher_responses.items():
            if topic in input_lower or any(word in input_lower for word in topic.split()):
                best_response = response
                break
        
        if not best_response:
            # General philosophical response
            general_responses = {
                'camus': "In this absurd world, we must create our own meaning through passionate engagement with life, even knowing it will end.",
                'dostoevsky': "The human soul is complex and mysterious. Through understanding our contradictions, we find our humanity.",
                'nietzsche': "Question everything, especially your assumptions about what you 'should' do. Create your own values and become who you are meant to be.",
                'neutral': "This is a profound question that philosophers have grappled with for centuries. Let us explore it together through reason and reflection."
            }
            best_response = general_responses.get(philosopher, general_responses['neutral'])
        
        # Add context if available
        if context:
            best_response += f"\n\nAs the philosophical tradition reminds us: {context[0][:150]}..."
        
        return {
            'message': best_response,
            'sources': [{'text': ctx[:100] + '...' if len(ctx) > 100 else ctx, 'relevance': 'medium'} for ctx in context[:2]],
            'generated_by': 'enhanced_fallback'
        }