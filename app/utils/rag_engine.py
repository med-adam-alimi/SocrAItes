import faiss
import numpy as np
import json
import os
import requests
import time
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import pickle

class RAGEngine:
    """Retrieval Augmented Generation engine for philosophy texts using FREE APIs."""
    
    def __init__(self):
        """Initialize the RAG engine with free API support."""
        self.embedding_model_name = os.environ.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        self.embedding_model = None
        self.index = None
        self.chunks = []
        self.philosopher_mapping = {}
        
        # Free API configuration
        self.use_api = True  # Set to True for API mode
        self.api_type = os.environ.get('API_TYPE', 'huggingface')  # 'huggingface', 'cohere', or 'together'
        
        # Hugging Face Free API (no key needed for some models)
        self.hf_api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        self.hf_headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_KEY', '')}"}
        
        # Together AI Free Tier (good alternative)
        self.together_api_url = "https://api.together.xyz/inference"
        self.together_headers = {"Authorization": f"Bearer {os.environ.get('TOGETHER_API_KEY', '')}"}
        
        self._load_models_and_data()
    
    def _load_models_and_data(self):
        """Load embedding model and pre-processed data."""
        try:
            # Load embedding model (lightweight)
            print("Loading lightweight embedding model...")
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            
            # Load FAISS index
            embeddings_path = os.environ.get('EMBEDDINGS_PATH', 'data/processed/embeddings.faiss')
            if os.path.exists(embeddings_path):
                self.index = faiss.read_index(embeddings_path)
            
            # Load text chunks
            chunks_path = os.environ.get('CHUNKS_PATH', 'data/processed/chunks.json')
            if os.path.exists(chunks_path):
                with open(chunks_path, 'r', encoding='utf-8') as f:
                    self.chunks = json.load(f)
            
            # Load philosopher mapping
            mapping_path = 'data/processed/philosopher_mapping.json'
            if os.path.exists(mapping_path):
                with open(mapping_path, 'r', encoding='utf-8') as f:
                    self.philosopher_mapping = json.load(f)
                    
            print(f"✅ RAG engine loaded successfully!")
            print(f"📚 Loaded {len(self.chunks)} text chunks")
                    
        except Exception as e:
            print(f"Warning: Could not load RAG data: {e}")
            print("Run 'python scripts/prepare_data.py' to initialize the data.")
    
    def generate_with_free_api(self, prompt: str, persona: str) -> str:
        """Generate response using free APIs."""
        
        # Persona-specific prompts
        persona_prompts = {
            'camus': f"You are Albert Camus, the existentialist philosopher. Respond with wisdom about absurdism and the human condition.\n\nHuman: {prompt}\n\nCamus:",
            'dostoevsky': f"You are Fyodor Dostoevsky, exploring psychological depths and moral dilemmas.\n\nHuman: {prompt}\n\nDostoevsky:",
            'nietzsche': f"You are Friedrich Nietzsche, bold and provocative, discussing will to power and beyond good and evil.\n\nHuman: {prompt}\n\nNietzsche:",
            'neutral': f"You are a wise philosophy guide. Explain this clearly and thoughtfully.\n\nHuman: {prompt}\n\nPhilosophy Guide:"
        }
        
        full_prompt = persona_prompts.get(persona, persona_prompts['neutral'])
        
        try:
            if self.api_type == 'huggingface':
                return self._call_huggingface_api(full_prompt)
            elif self.api_type == 'together':
                return self._call_together_api(full_prompt)
            else:
                return self._generate_fallback_response(prompt, persona)
                
        except Exception as e:
            print(f"API error: {e}")
            return self._generate_fallback_response(prompt, persona)
    
    def _call_huggingface_api(self, prompt: str) -> str:
        """Call Hugging Face Inference API (free tier)."""
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(
                self.hf_api_url, 
                headers=self.hf_headers, 
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').strip()
                return str(result).strip()
            else:
                print(f"Hugging Face API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Hugging Face API call failed: {e}")
            return None
    
    def _call_together_api(self, prompt: str) -> str:
        """Call Together AI API (free tier available)."""
        payload = {
            "model": "togethercomputer/RedPajama-INCITE-Chat-3B-v1",
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1.1
        }
        
        try:
            response = requests.post(
                self.together_api_url,
                headers=self.together_headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('output', {}).get('choices', [{}])[0].get('text', '').strip()
            else:
                print(f"Together AI API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Together AI API call failed: {e}")
            return None
    
    def _generate_fallback_response(self, prompt: str, persona: str) -> str:
        """Generate fallback response when APIs fail."""
        
        fallback_responses = {
            'camus': {
                'meaning': "The absurd is the confrontation between human need for meaning and the meaningless silence of the world. We must revolt against this absurdity not by escaping it, but by fully acknowledging it and choosing to live anyway.",
                'death': "There is but one truly serious philosophical problem, and that is suicide. Judging whether life is or is not worth living amounts to answering the fundamental question of philosophy.",
                'existence': "In the face of an absurd world, we must create our own meaning. The struggle itself toward the heights is enough to fill a person's heart.",
                'default': "We must imagine Sisyphus happy. In acknowledging life's absurdity, we find our freedom to create meaning."
            },
            'dostoevsky': {
                'suffering': "The mystery of human existence lies not in just staying alive, but in finding something to live for. Suffering is the sole origin of consciousness.",
                'freedom': "Man is tormented by no greater anxiety than to find someone quickly to whom he can hand over that great gift of freedom with which the ill-fated creature is born.",
                'soul': "The soul is healed by being with other souls. We are all responsible for one another, and I more than others.",
                'default': "The human heart is a mystery, and understanding it requires diving into the deepest psychological depths."
            },
            'nietzsche': {
                'power': "What does not kill me makes me stronger. The will to power is the driving force of all life - embrace it and become who you truly are.",
                'morality': "God is dead, and we have killed him. Now we must become gods ourselves and create new values beyond good and evil.",
                'individual': "Become who you are! The individual has always had to struggle not to be overwhelmed by the tribe.",
                'default': "You must have chaos within you to give birth to a dancing star. Embrace your will to power!"
            },
            'neutral': {
                'default': "This is a profound philosophical question that has been explored by many great thinkers throughout history. Let me share some perspectives that might illuminate this topic for you."
            }
        }
        
        prompt_lower = prompt.lower()
        persona_responses = fallback_responses.get(persona, fallback_responses['neutral'])
        
        # Simple keyword matching
        for keyword, response in persona_responses.items():
            if keyword in prompt_lower:
                return response
        
        return persona_responses['default']
    
    def retrieve_context(self, query: str, philosopher: str = None, top_k: int = 3) -> List[str]:
        """Retrieve relevant context for a query."""
        if not self.embedding_model or not self.index or not self.chunks:
            return [
                "Welcome to philosophical discussion! The knowledge base is being prepared.",
                "Feel free to ask any philosophical questions and I'll do my best to engage with the ideas."
            ]
        
        try:
            # Encode the query
            query_embedding = self.embedding_model.encode([query])
            
            # Search for similar chunks
            distances, indices = self.index.search(query_embedding.astype('float32'), top_k * 2)
            
            # Filter by philosopher if specified
            relevant_chunks = []
            for idx in indices[0]:
                if idx < len(self.chunks):
                    chunk = self.chunks[idx]
                    
                    # If philosopher is specified, prefer chunks from that philosopher
                    if philosopher and philosopher != 'neutral':
                        chunk_philosopher = chunk.get('philosopher', '').lower()
                        if philosopher.lower() in chunk_philosopher:
                            relevant_chunks.append(chunk['text'])
                        elif len(relevant_chunks) < top_k:
                            relevant_chunks.append(chunk['text'])
                    else:
                        relevant_chunks.append(chunk['text'])
                    
                    if len(relevant_chunks) >= top_k:
                        break
            
            return relevant_chunks[:top_k]
            
        except Exception as e:
            print(f"Error in retrieval: {e}")
            return ["I can discuss philosophical topics, though my knowledge base is limited right now."]
    
    def add_text_chunk(self, text: str, philosopher: str, source: str):
        """Add a new text chunk to the index (for future expansion)."""
        if not self.embedding_model:
            return
        
        try:
            # Create embedding
            embedding = self.embedding_model.encode([text])
            
            # Add to index
            if self.index is None:
                dimension = embedding.shape[1]
                self.index = faiss.IndexFlatIP(dimension)
            
            self.index.add(embedding.astype('float32'))
            
            # Add to chunks
            chunk_data = {
                'text': text,
                'philosopher': philosopher,
                'source': source,
                'id': len(self.chunks)
            }
            self.chunks.append(chunk_data)
            
        except Exception as e:
            print(f"Error adding text chunk: {e}")
    
    def save_index(self, embeddings_path: str = None, chunks_path: str = None):
        """Save the current index and chunks."""
        try:
            if embeddings_path is None:
                embeddings_path = os.environ.get('EMBEDDINGS_PATH', 'data/processed/embeddings.faiss')
            if chunks_path is None:
                chunks_path = os.environ.get('CHUNKS_PATH', 'data/processed/chunks.json')
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(embeddings_path), exist_ok=True)
            os.makedirs(os.path.dirname(chunks_path), exist_ok=True)
            
            # Save FAISS index
            if self.index:
                faiss.write_index(self.index, embeddings_path)
            
            # Save chunks
            with open(chunks_path, 'w', encoding='utf-8') as f:
                json.dump(self.chunks, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error saving index: {e}")
