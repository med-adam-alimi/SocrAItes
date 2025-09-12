#!/usr/bin/env python3
"""
Data preparation script for AI Philosophy Chatbot.
This script downloads, processes, and embeds philosophical texts for RAG.
"""

import os
import json
import requests
import re
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Any

class PhilosophyDataPreparer:
    """Prepares philosophical texts for RAG system."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.chunk_size = int(os.environ.get('CHUNK_SIZE', 512))
        self.chunk_overlap = int(os.environ.get('CHUNK_OVERLAP', 50))
        
        # Create directories
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize embedding model
        model_name = os.environ.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
    
    def download_sample_texts(self):
        """Download sample philosophical texts from Project Gutenberg."""
        
        # Sample texts from Project Gutenberg (public domain)
        texts_to_download = {
            'nietzsche_beyond_good_evil': {
                'url': 'https://www.gutenberg.org/files/4363/4363-0.txt',
                'philosopher': 'nietzsche',
                'title': 'Beyond Good and Evil',
                'author': 'Friedrich Nietzsche'
            },
            'camus_stranger_excerpt': {
                'content': '''Today, mother died. Or maybe yesterday, I don't know. I received a telegram from the old people's home: "Mother died. Funeral tomorrow. Deep sympathy." That doesn't mean anything. Maybe it was yesterday.

The old people's home is at Marengo, about eighty kilometers from Algiers. I'll take the two o'clock bus and arrive in the afternoon. That way I can watch over her and I'll be back tomorrow night. I asked my boss for two days off and he couldn't refuse me under the circumstances. But he didn't seem pleased. I even said to him, "It's not my fault." He didn't answer. Then I thought I shouldn't have said that. After all, I had no reason to excuse myself. It was more like he had to offer me his condolences. But he'll probably do that the day after tomorrow when he sees me in mourning. For now, it's a bit like mother isn't really dead. After the funeral, though, the case will be closed and everything will have a more official feeling.''',
                'philosopher': 'camus',
                'title': 'The Stranger (Excerpt)',
                'author': 'Albert Camus'
            },
            'dostoevsky_notes_excerpt': {
                'content': '''I am a sick man... I am a spiteful man. I am an unattractive man. I believe my liver is diseased. However, I know nothing at all about my disease, and do not know for certain what ails me. I don't consult a doctor for it, and never have, though I have a respect for medicine and doctors. Besides, I am extremely superstitious, sufficiently so to respect medicine, anyway (I am well-educated enough not to be superstitious, but I am superstitious). No, I refuse to consult a doctor from spite. That you probably will not understand. Well, I understand it, though. Of course, I can't explain who it is precisely that I am mortifying in this case by my spite: I am perfectly well aware that I cannot "pay out" the doctors by not consulting them; I know better than anyone that by all this I am only injuring myself and no one else. But still, if I don't consult a doctor it is from spite. My liver is bad, well—let it get worse!''',
                'philosopher': 'dostoevsky',
                'title': 'Notes from Underground (Excerpt)',
                'author': 'Fyodor Dostoevsky'
            }
        }
        
        print("Downloading sample philosophical texts...")
        
        for text_id, info in texts_to_download.items():
            file_path = self.raw_dir / f"{text_id}.txt"
            
            if file_path.exists():
                print(f"  {text_id} already exists, skipping...")
                continue
            
            if 'url' in info:
                try:
                    response = requests.get(info['url'], timeout=30)
                    response.raise_for_status()
                    content = response.text
                    
                    # Clean up Project Gutenberg headers/footers
                    content = self._clean_gutenberg_text(content)
                    
                except Exception as e:
                    print(f"  Failed to download {text_id}: {e}")
                    continue
            else:
                content = info['content']
            
            # Save the text file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Save metadata
            metadata = {k: v for k, v in info.items() if k != 'url' and k != 'content'}
            metadata_path = self.raw_dir / f"{text_id}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"  Downloaded: {text_id}")
    
    def _clean_gutenberg_text(self, text: str) -> str:
        """Clean Project Gutenberg text formatting."""
        # Remove Project Gutenberg header and footer
        lines = text.split('\n')
        start_idx = 0
        end_idx = len(lines)
        
        # Find start of actual content
        for i, line in enumerate(lines):
            if 'START OF THIS PROJECT GUTENBERG' in line.upper():
                start_idx = i + 1
                break
        
        # Find end of actual content
        for i in range(len(lines) - 1, -1, -1):
            if 'END OF THIS PROJECT GUTENBERG' in lines[i].upper():
                end_idx = i
                break
        
        # Join the content
        content = '\n'.join(lines[start_idx:end_idx])
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = re.sub(r'[ \t]+', ' ', content)
        
        return content.strip()
    
    def create_sample_philosophy_content(self):
        """Create sample philosophical content if downloads fail."""
        print("Creating sample philosophical content...")
        
        sample_contents = {
            'ethics_basics': {
                'content': '''Ethics is the branch of philosophy that examines what is morally right and wrong, good and bad. It seeks to understand the nature of moral judgments and the principles that should guide human conduct.

There are three main approaches to ethics:

1. Consequentialism: The rightness or wrongness of actions is determined solely by their consequences. Utilitarianism, which aims to maximize overall happiness or well-being, is the most well-known consequentialist theory.

2. Deontological Ethics: Certain actions are inherently right or wrong, regardless of their consequences. Immanuel Kant's categorical imperative is a famous deontological principle that states we should act only according to maxims we could will to be universal laws.

3. Virtue Ethics: Rather than focusing on actions or consequences, virtue ethics emphasizes character. It asks not "What should I do?" but "What kind of person should I be?" Aristotle's conception of virtues as the mean between extremes is central to this approach.

These different ethical frameworks often lead to different conclusions about what we ought to do in specific situations, highlighting the complexity of moral reasoning.''',
                'philosopher': 'neutral',
                'title': 'Introduction to Ethics',
                'author': 'Philosophy Guide'
            },
            'existentialism_overview': {
                'content': '''Existentialism is a philosophical movement that emphasizes individual existence, freedom, and choice. It argues that humans exist first and then create their essence through their actions and choices.

Key themes in existentialism include:

Existence precedes essence: Unlike objects which are created for a purpose, humans exist first and then define what they are through their choices and actions.

Freedom and responsibility: We are "condemned to be free" and fully responsible for our choices. This freedom can be both liberating and terrifying.

Authenticity: Living authentically means acknowledging our freedom and taking responsibility for our choices, rather than conforming to external expectations or denying our freedom.

Angst and absurdity: The recognition of our freedom and the absence of predetermined meaning can lead to anxiety (angst) and a sense of the absurd.

Bad faith: The tendency to deny our freedom and responsibility by pretending we have no choice or by defining ourselves solely through external roles.

Major existentialist philosophers include Søren Kierkegaard, Friedrich Nietzsche, Jean-Paul Sartre, Simone de Beauvoir, and Albert Camus (though Camus rejected the existentialist label).''',
                'philosopher': 'neutral',
                'title': 'Existentialism Overview',
                'author': 'Philosophy Guide'
            }
        }
        
        for text_id, info in sample_contents.items():
            file_path = self.raw_dir / f"{text_id}.txt"
            
            # Save content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(info['content'])
            
            # Save metadata
            metadata = {k: v for k, v in info.items() if k != 'content'}
            metadata_path = self.raw_dir / f"{text_id}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"  Created: {text_id}")
    
    def chunk_texts(self) -> List[Dict[str, Any]]:
        """Split texts into chunks for embedding."""
        print("Chunking texts...")
        
        chunks = []
        
        for txt_file in self.raw_dir.glob("*.txt"):
            # Load text
            with open(txt_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Load metadata
            metadata_file = txt_file.with_name(f"{txt_file.stem}_metadata.json")
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            else:
                metadata = {
                    'philosopher': 'unknown',
                    'title': txt_file.stem,
                    'author': 'Unknown'
                }
            
            # Split into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            # Create chunks
            current_chunk = ""
            current_length = 0
            
            for sentence in sentences:
                sentence_length = len(sentence.split())
                
                if current_length + sentence_length <= self.chunk_size:
                    current_chunk += sentence + ". "
                    current_length += sentence_length
                else:
                    if current_chunk.strip():
                        chunks.append({
                            'text': current_chunk.strip(),
                            'philosopher': metadata['philosopher'],
                            'source': f"{metadata['title']} by {metadata['author']}",
                            'file': str(txt_file.name)
                        })
                    
                    # Start new chunk with overlap
                    if self.chunk_overlap > 0 and current_length > self.chunk_overlap:
                        overlap_words = current_chunk.split()[-self.chunk_overlap:]
                        current_chunk = ' '.join(overlap_words) + " " + sentence + ". "
                        current_length = len(overlap_words) + sentence_length
                    else:
                        current_chunk = sentence + ". "
                        current_length = sentence_length
            
            # Add final chunk
            if current_chunk.strip():
                chunks.append({
                    'text': current_chunk.strip(),
                    'philosopher': metadata['philosopher'],
                    'source': f"{metadata['title']} by {metadata['author']}",
                    'file': str(txt_file.name)
                })
        
        print(f"  Created {len(chunks)} chunks")
        return chunks
    
    def create_embeddings(self, chunks: List[Dict[str, Any]]):
        """Create embeddings for text chunks."""
        print("Creating embeddings...")
        
        # Extract texts
        texts = [chunk['text'] for chunk in chunks]
        
        # Create embeddings
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)  # Inner product for similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        index.add(embeddings.astype('float32'))
        
        # Save index
        embeddings_path = self.processed_dir / "embeddings.faiss"
        faiss.write_index(index, str(embeddings_path))
        
        # Save chunks with IDs
        for i, chunk in enumerate(chunks):
            chunk['id'] = i
        
        chunks_path = self.processed_dir / "chunks.json"
        with open(chunks_path, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        
        print(f"  Saved {len(chunks)} embeddings to {embeddings_path}")
        print(f"  Saved chunks metadata to {chunks_path}")
    
    def test_retrieval(self):
        """Test the retrieval system."""
        print("\nTesting retrieval system...")
        
        # Load the index and chunks
        embeddings_path = self.processed_dir / "embeddings.faiss"
        chunks_path = self.processed_dir / "chunks.json"
        
        if not embeddings_path.exists() or not chunks_path.exists():
            print("  Error: Embeddings or chunks not found!")
            return
        
        index = faiss.read_index(str(embeddings_path))
        with open(chunks_path, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        # Test queries
        test_queries = [
            "What is the meaning of life?",
            "What is absurdism?",
            "What is free will?",
            "What is ethics?"
        ]
        
        for query in test_queries:
            print(f"\n  Query: {query}")
            
            # Encode query
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search
            distances, indices = index.search(query_embedding.astype('float32'), 3)
            
            for i, (idx, score) in enumerate(zip(indices[0], distances[0])):
                if idx < len(chunks):
                    chunk = chunks[idx]
                    print(f"    {i+1}. Score: {score:.3f}")
                    print(f"       Source: {chunk['source']}")
                    print(f"       Text: {chunk['text'][:100]}...")
    
    def run(self):
        """Run the complete data preparation pipeline."""
        print("Starting AI Philosophy Chatbot data preparation...")
        
        # Step 1: Download or create sample texts
        try:
            self.download_sample_texts()
        except Exception as e:
            print(f"Download failed: {e}")
            print("Creating sample content instead...")
        
        self.create_sample_philosophy_content()
        
        # Step 2: Chunk texts
        chunks = self.chunk_texts()
        
        if not chunks:
            print("No chunks created! Check your text files.")
            return
        
        # Step 3: Create embeddings
        self.create_embeddings(chunks)
        
        # Step 4: Test the system
        self.test_retrieval()
        
        print(f"\n✅ Data preparation complete!")
        print(f"📁 Raw texts: {self.raw_dir}")
        print(f"📁 Processed data: {self.processed_dir}")
        print(f"📊 Total chunks: {len(chunks)}")
        print("\nYou can now run the Flask app with: python run.py")

if __name__ == "__main__":
    preparer = PhilosophyDataPreparer()
    preparer.run()
