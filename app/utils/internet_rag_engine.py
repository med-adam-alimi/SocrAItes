#!/usr/bin/env python3
"""
Internet-powered RAG Engine for Real-time Philosophy Discussions
Searches web, Reddit, academic papers, and philosophy forums in real-time
"""

import os
import requests
import json
import time
from typing import List, Dict, Any
import urllib.parse
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InternetRAGEngine:
    """Real-time internet search RAG for deep philosophical conversations"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # API Keys (some free, some premium)
        self.serper_api_key = os.getenv('SERPER_API_KEY')  # Free tier: 2500 searches/month
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        
        logger.info("🌐 Internet RAG Engine initialized")
    
    def search_philosophy_content(self, query: str, philosopher: str = None) -> List[Dict]:
        """Search internet for philosophy content related to query"""
        logger.info(f"🔍 Searching internet for: {query}")
        
        search_results = []
        
        # 1. Search general web + philosophy sites
        web_results = self._search_web(query, philosopher)
        search_results.extend(web_results)
        
        # 2. Search Reddit for discussions
        reddit_results = self._search_reddit(query, philosopher)
        search_results.extend(reddit_results)
        
        # 3. Search academic sources
        academic_results = self._search_academic(query, philosopher)
        search_results.extend(academic_results)
        
        # 4. Search philosophy forums
        forum_results = self._search_philosophy_forums(query, philosopher)
        search_results.extend(forum_results)
        
        # 5. Search current events if query relates to modern topics
        if self._is_modern_topic(query):
            news_results = self._search_news(query, philosopher)
            search_results.extend(news_results)
        
        # Rank and filter results
        ranked_results = self._rank_results(search_results, query)
        
        logger.info(f"✅ Found {len(ranked_results)} relevant sources")
        return ranked_results[:10]  # Top 10 most relevant
    
    def _search_web(self, query: str, philosopher: str = None) -> List[Dict]:
        """Search web using multiple search engines"""
        results = []
        
        # Build search query
        search_query = query
        if philosopher:
            search_query += f" {philosopher} philosophy"
        search_query += " philosophy meaning ethics existence"
        
        # Try Serper API (Google results) - FREE TIER
        if self.serper_api_key:
            try:
                serper_results = self._search_serper(search_query)
                results.extend(serper_results)
            except Exception as e:
                logger.warning(f"Serper search failed: {e}")
        
        # Fallback: DuckDuckGo (no API key needed)
        try:
            ddg_results = self._search_duckduckgo(search_query)
            results.extend(ddg_results)
        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {e}")
        
        return results
    
    def _search_serper(self, query: str) -> List[Dict]:
        """Search using Serper API (Google results)"""
        url = "https://google.serper.dev/search"
        
        payload = {
            "q": query,
            "num": 8,
            "hl": "en",
            "gl": "us"
        }
        
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for item in data.get('organic', []):
                results.append({
                    'title': item.get('title', ''),
                    'content': item.get('snippet', ''),
                    'url': item.get('link', ''),
                    'source': 'web',
                    'relevance_score': 0.8
                })
            
            return results
        
        return []
    
    def _search_duckduckgo(self, query: str) -> List[Dict]:
        """Search using DuckDuckGo (updated method)"""
        try:
            # Use the updated ddgs package
            import ddgs
            
            results = []
            with ddgs.DDGS() as ddgs_client:
                search_results = ddgs_client.text(query, max_results=8)
                for result in search_results:
                    results.append({
                        'title': result.get('title', ''),
                        'content': result.get('body', ''),
                        'url': result.get('href', ''),
                        'source': 'web',
                        'relevance_score': 0.7
                    })
            
            return results
        except ImportError:
            # Fallback: Try to install ddgs
            try:
                import subprocess
                import sys
                subprocess.check_call([sys.executable, "-m", "pip", "install", "ddgs"])
                import ddgs
                
                results = []
                with ddgs.DDGS() as ddgs_client:
                    search_results = ddgs_client.text(query, max_results=8)
                    for result in search_results:
                        results.append({
                            'title': result.get('title', ''),
                            'content': result.get('body', ''),
                            'url': result.get('href', ''),
                            'source': 'web',
                            'relevance_score': 0.7
                        })
                
                return results
            except Exception as e:
                logger.warning(f"DuckDuckGo search error: {e}")
                return []
        except Exception as e:
            logger.warning(f"DuckDuckGo search error: {e}")
            return []
    
    def _search_reddit(self, query: str, philosopher: str = None) -> List[Dict]:
        """Search Reddit for philosophy discussions - rate limit friendly"""
        results = []
        
        # Build Reddit search query
        reddit_query = query
        if philosopher:
            reddit_query += f" {philosopher}"
        
        # Search specific philosophy subreddits with delays
        subreddits = ['philosophy', 'askphilosophy', 'stoicism']  # Reduced to avoid rate limits
        
        for i, subreddit in enumerate(subreddits):
            try:
                # Add delay between requests to avoid rate limiting
                if i > 0:
                    time.sleep(2)
                
                subreddit_results = self._search_reddit_subreddit(reddit_query, subreddit)
                results.extend(subreddit_results)
                
                # Limit total results to avoid excessive requests
                if len(results) >= 15:
                    break
                    
            except Exception as e:
                logger.warning(f"Reddit search in r/{subreddit} failed: {e}")
        
        return results
    
    def _search_reddit_subreddit(self, query: str, subreddit: str) -> List[Dict]:
        """Search specific Reddit subreddit"""
        # Reddit JSON API (no auth needed for public posts)
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.reddit.com/r/{subreddit}/search.json"
        
        params = {
            'q': query,
            'restrict_sr': 'on',
            'sort': 'relevance',
            'limit': 5
        }
        
        response = self.session.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                
                # Get post content
                title = post_data.get('title', '')
                selftext = post_data.get('selftext', '')
                url = f"https://reddit.com{post_data.get('permalink', '')}"
                score = post_data.get('score', 0)
                
                if title or selftext:
                    results.append({
                        'title': title,
                        'content': selftext[:500] + '...' if len(selftext) > 500 else selftext,
                        'url': url,
                        'source': f'reddit_r_{subreddit}',
                        'relevance_score': min(0.9, 0.5 + (score / 100))  # Score-based relevance
                    })
            
            return results
        
        return []
    
    def _search_academic(self, query: str, philosopher: str = None) -> List[Dict]:
        """Search academic philosophy sources"""
        results = []
        
        # Search specific academic sources that are working
        academic_sources = [
            'Stanford Encyclopedia of Philosophy',
            'Internet Encyclopedia of Philosophy'
            # Removed PhilPapers and Academia.edu due to access restrictions
        ]
        
        for source in academic_sources:
            search_query = f"site:{self._get_site_domain(source)} {query}"
            if philosopher:
                search_query += f" {philosopher}"
            
            # Use DuckDuckGo for academic search
            try:
                academic_results = self._search_duckduckgo(search_query)
                for result in academic_results:
                    result['source'] = f'academic_{source.lower().replace(" ", "_")}'
                    result['relevance_score'] += 0.3  # Boost academic sources
                results.extend(academic_results)
            except Exception as e:
                logger.warning(f"Academic search for {source} failed: {e}")
        
        return results
    
    def _search_philosophy_forums(self, query: str, philosopher: str = None) -> List[Dict]:
        """Search philosophy forums and discussion sites"""
        results = []
        
        forum_sites = [
            'philosophyforums.com',
            'thephilosophyforum.com',
            'philosophy-forums.org'
        ]
        
        for site in forum_sites:
            search_query = f"site:{site} {query}"
            if philosopher:
                search_query += f" {philosopher}"
            
            try:
                forum_results = self._search_duckduckgo(search_query)
                for result in forum_results:
                    result['source'] = f'forum_{site.replace(".", "_")}'
                results.extend(forum_results)
            except Exception as e:
                logger.warning(f"Forum search for {site} failed: {e}")
        
        return results
    
    def _search_news(self, query: str, philosopher: str = None) -> List[Dict]:
        """Search current news and articles about philosophy"""
        results = []
        
        # Add current date context
        current_year = datetime.now().year
        news_query = f"{query} philosophy {current_year}"
        if philosopher:
            news_query += f" {philosopher}"
        
        # Search news sites
        news_sites = [
            'aeon.co',  # Philosophy magazine
            'philosophynow.org',
            'thenewatlantis.com',
            'theguardian.com/world/philosophy',
            'nytimes.com philosophy'
        ]
        
        for site in news_sites:
            search_query = f"site:{site} {news_query}"
            
            try:
                news_results = self._search_duckduckgo(search_query)
                for result in news_results:
                    result['source'] = f'news_{site.replace(".", "_")}'
                results.extend(news_results)
            except Exception as e:
                logger.warning(f"News search for {site} failed: {e}")
        
        return results
    
    def _is_modern_topic(self, query: str) -> bool:
        """Check if query relates to modern/current topics"""
        modern_keywords = [
            'ai', 'artificial intelligence', 'technology', 'internet', 'social media',
            'climate change', 'pandemic', 'covid', 'bitcoin', 'cryptocurrency',
            'metaverse', 'virtual reality', 'automation', 'future', 'modern',
            'contemporary', '2020', '2021', '2022', '2023', '2024', '2025',
            'today', 'current', 'now', 'recent'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in modern_keywords)
    
    def _get_site_domain(self, source_name: str) -> str:
        """Get domain for academic source"""
        domain_map = {
            'Stanford Encyclopedia of Philosophy': 'plato.stanford.edu',
            'Internet Encyclopedia of Philosophy': 'iep.utm.edu',
            'PhilPapers': 'philpapers.org',
            'Academia.edu philosophy': 'academia.edu'
        }
        return domain_map.get(source_name, '')
    
    def _rank_results(self, results: List[Dict], query: str) -> List[Dict]:
        """Rank search results by relevance"""
        query_words = set(query.lower().split())
        
        for result in results:
            score = result.get('relevance_score', 0.5)
            
            # Boost score based on title/content relevance
            title = result.get('title', '').lower()
            content = result.get('content', '').lower()
            
            title_matches = len(query_words.intersection(set(title.split())))
            content_matches = len(query_words.intersection(set(content.split())))
            
            score += (title_matches * 0.1) + (content_matches * 0.05)
            
            # Boost academic and high-quality sources
            source = result.get('source', '')
            if 'academic' in source or 'stanford' in source or 'iep' in source:
                score += 0.3
            elif 'reddit' in source:
                score += 0.1
            
            result['final_score'] = min(1.0, score)
        
        # Sort by final score
        results.sort(key=lambda x: x.get('final_score', 0), reverse=True)
        
        return results
    
    def format_context_for_ai(self, search_results: List[Dict], query: str) -> str:
        """Format search results into context for AI model"""
        if not search_results:
            return "No relevant internet sources found for this query."
        
        context = f"REAL-TIME INTERNET CONTEXT for query: '{query}'\n"
        context += f"Search performed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for i, result in enumerate(search_results[:8], 1):
            source = result.get('source', 'unknown')
            title = result.get('title', 'No title')
            content = result.get('content', 'No content')
            url = result.get('url', '')
            score = result.get('final_score', 0)
            
            context += f"SOURCE {i} [{source.upper()}] (relevance: {score:.2f})\n"
            context += f"Title: {title}\n"
            context += f"Content: {content}\n"
            context += f"URL: {url}\n"
            context += "-" * 80 + "\n"
        
        context += "\nUse this real-time internet context to provide current, comprehensive philosophical insights."
        
        return context

class ModernPhilosopherChat:
    """AI Philosopher Chat with Internet-powered RAG"""
    
    def __init__(self):
        self.internet_rag = InternetRAGEngine()
        self.huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')
        
        # Use working models that are available for free
        self.model_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        # Fallback to available models if primary is not accessible
        self.fallback_models = [
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
            "https://api-inference.huggingface.co/models/google/flan-t5-base"
        ]
        
        logger.info("🤖 Modern Philosopher Chat with Internet RAG initialized")
    
    def chat(self, user_input: str, philosopher: str = "guide") -> str:
        """Generate AI response using real-time internet context"""
        logger.info(f"💭 Processing query: {user_input}")
        
        # Get real-time internet context
        search_results = self.internet_rag.search_philosophy_content(user_input, philosopher)
        internet_context = self.internet_rag.format_context_for_ai(search_results, user_input)
        
        # Generate AI response with internet context
        ai_response = self._generate_ai_response(user_input, philosopher, internet_context)
        
        return ai_response
    
    def _generate_ai_response(self, user_input: str, philosopher: str, internet_context: str) -> str:
        """Generate AI response using powerful model + internet context"""
        persona_prompt = self._get_philosopher_persona(philosopher)
        
        prompt = f"""{persona_prompt}

{internet_context}

Human Question: {user_input}

Based on the real-time internet context above and your philosophical expertise, provide a deep, thoughtful response that:
1. Addresses the human's question directly
2. Incorporates relevant insights from the internet sources
3. Connects to broader philosophical themes
4. Considers modern/contemporary perspectives when relevant
5. Maintains your authentic philosophical voice

Response:"""
        
        # Try to generate with powerful model
        try:
            response = self._call_huggingface_api(prompt, self.model_url)
            if response and len(response.strip()) > 50:
                return response
        except Exception as e:
            logger.warning(f"Primary model failed: {e}")
        
        # Try fallback models
        for fallback_url in self.fallback_models:
            try:
                response = self._call_huggingface_api(prompt, fallback_url)
                if response and len(response.strip()) > 50:
                    return response
            except Exception as e:
                logger.warning(f"Fallback model failed: {e}")
        
        # Ultimate fallback
        return self._generate_fallback_response(user_input, philosopher, internet_context)
    
    def _call_huggingface_api(self, prompt: str, model_url: str) -> str:
        """Call Hugging Face API with improved error handling"""
        try:
            headers = {
                "Authorization": f"Bearer {self.huggingface_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(model_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated = result[0].get('generated_text', '')
                    # Clean up the response
                    if prompt in generated:
                        generated = generated.replace(prompt, '').strip()
                    return generated
                elif isinstance(result, dict) and 'generated_text' in result:
                    generated = result['generated_text']
                    if prompt in generated:
                        generated = generated.replace(prompt, '').strip()
                    return generated
            
            # If API fails, log the specific error
            logger.warning(f"HF API error {response.status_code}: {response.text[:200]}")
            raise Exception(f"API call failed: {response.status_code} - {response.text[:100]}")
            
        except requests.exceptions.Timeout:
            raise Exception("API call timed out")
        except requests.exceptions.ConnectionError:
            raise Exception("API connection failed")
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")
    
    def _get_philosopher_persona(self, philosopher: str) -> str:
        """Get philosopher persona prompt"""
        personas = {
            "camus": "You are Albert Camus, exploring absurdism and the human condition in a world without inherent meaning.",
            "nietzsche": "You are Friedrich Nietzsche, challenging conventional morality and exploring the will to power.",
            "dostoevsky": "You are Fyodor Dostoevsky, examining human psychology, suffering, and redemption.",
            "sartre": "You are Jean-Paul Sartre, analyzing existence, freedom, and responsibility.",
            "beauvoir": "You are Simone de Beauvoir, exploring existential feminism and ethics of ambiguity.",
            "kant": "You are Immanuel Kant, examining moral duty, categorical imperatives, and reason.",
            "aristotle": "You are Aristotle, exploring virtue ethics, practical wisdom, and human flourishing.",
            "marcus": "You are Marcus Aurelius, embodying Stoic philosophy and practical wisdom.",
            "guide": "You are a wise philosophical guide, drawing from multiple traditions to explore deep questions."
        }
        
        return personas.get(philosopher.lower(), personas["guide"])
    
    def _generate_fallback_response(self, user_input: str, philosopher: str, internet_context: str) -> str:
        """Generate intelligent response using internet context when AI models fail"""
        if not internet_context or "No relevant internet sources" in internet_context:
            return self._get_basic_philosophical_response(user_input, philosopher)
        
        # Parse internet context to extract meaningful content
        sources_data = self._parse_internet_context(internet_context)
        
        if not sources_data:
            return self._get_basic_philosophical_response(user_input, philosopher)
        
        # Create a comprehensive response using internet findings
        persona_intro = self._get_persona_intro(philosopher)
        
        response = f"{persona_intro}\n\n"
        
        # Analyze the question type
        question_type = self._analyze_question_type(user_input)
        
        if question_type == "meaning_life":
            response += self._create_meaning_response(sources_data, philosopher)
        elif question_type == "ethics_morality":
            response += self._create_ethics_response(sources_data, philosopher)
        elif question_type == "existence_reality":
            response += self._create_existence_response(sources_data, philosopher)
        elif question_type == "consciousness_mind":
            response += self._create_consciousness_response(sources_data, philosopher)
        elif question_type == "modern_technology":
            response += self._create_technology_response(sources_data, philosopher)
        else:
            response += self._create_general_response(sources_data, philosopher, user_input)
        
        response += f"\n\n{self._get_persona_conclusion(philosopher, user_input)}"
        
        return response
    
    def _parse_internet_context(self, context: str) -> List[Dict]:
        """Parse internet context to extract source data"""
        sources_data = []
        lines = context.split('\n')
        
        current_source = {}
        for line in lines:
            line = line.strip()
            if line.startswith('SOURCE'):
                if current_source:
                    sources_data.append(current_source)
                current_source = {'source_info': line}
            elif line.startswith('Title:'):
                current_source['title'] = line.replace('Title:', '').strip()
            elif line.startswith('Content:'):
                current_source['content'] = line.replace('Content:', '').strip()
            elif line.startswith('URL:'):
                current_source['url'] = line.replace('URL:', '').strip()
        
        if current_source:
            sources_data.append(current_source)
        
        return [s for s in sources_data if s.get('content') and len(s.get('content', '')) > 50]
    
    def _analyze_question_type(self, question: str) -> str:
        """Analyze what type of philosophical question this is"""
        question_lower = question.lower()
        
        meaning_keywords = ['meaning', 'purpose', 'point', 'why live', 'worthwhile', 'significance']
        ethics_keywords = ['right', 'wrong', 'moral', 'ethical', 'should', 'ought', 'good', 'evil']
        existence_keywords = ['exist', 'reality', 'being', 'existence', 'real', 'universe', 'truth']
        consciousness_keywords = ['consciousness', 'mind', 'aware', 'thinking', 'cognition', 'brain']
        technology_keywords = ['ai', 'artificial intelligence', 'technology', 'digital', 'internet', 'computer']
        
        if any(keyword in question_lower for keyword in meaning_keywords):
            return "meaning_life"
        elif any(keyword in question_lower for keyword in ethics_keywords):
            return "ethics_morality"
        elif any(keyword in question_lower for keyword in existence_keywords):
            return "existence_reality"
        elif any(keyword in question_lower for keyword in consciousness_keywords):
            return "consciousness_mind"
        elif any(keyword in question_lower for keyword in technology_keywords):
            return "modern_technology"
        else:
            return "general"
    
    def _create_meaning_response(self, sources_data: List[Dict], philosopher: str) -> str:
        """Create response about meaning of life"""
        response = "The question of life's meaning has occupied philosophers for millennia, and contemporary discussions reveal fascinating perspectives:\n\n"
        
        for i, source in enumerate(sources_data[:3], 1):
            if 'meaning' in source.get('content', '').lower() or 'purpose' in source.get('content', '').lower():
                response += f"• Current philosophical thought suggests: {source['content'][:150]}...\n\n"
        
        if philosopher == "camus":
            response += "From my absurdist perspective, these discussions confirm what I've always maintained: meaning is not given to us by the universe, but created through our revolt against meaninglessness. We must imagine Sisyphus happy."
        elif philosopher == "nietzsche":
            response += "These modern perspectives echo my conviction: we must become the creators of our own values. Where God is dead, we must become gods ourselves."
        else:
            response += "These contemporary insights remind us that the search for meaning itself gives life its richness and depth."
        
        return response
    
    def _create_technology_response(self, sources_data: List[Dict], philosopher: str) -> str:
        """Create response about technology and AI"""
        response = "The intersection of technology and human existence raises profound questions that philosophers are actively exploring:\n\n"
        
        for i, source in enumerate(sources_data[:3], 1):
            if any(tech_word in source.get('content', '').lower() for tech_word in ['ai', 'technology', 'digital', 'artificial']):
                response += f"• Modern analysis reveals: {source['content'][:150]}...\n\n"
        
        if philosopher == "camus":
            response += "In this age of artificial intelligence, the absurd becomes even more apparent. Machines may compute, but only humans can choose to create meaning in spite of cosmic indifference."
        elif philosopher == "sartre":
            response += "Technology confronts us with radical freedom. We are responsible not just for our own choices, but for how we allow technology to shape human consciousness."
        else:
            response += "These technological developments force us to reconsider fundamental questions about consciousness, free will, and what makes us uniquely human."
        
        return response
    
    def _create_general_response(self, sources_data: List[Dict], philosopher: str, user_input: str) -> str:
        """Create general philosophical response"""
        response = f"Your inquiry touches on fundamental philosophical questions. Contemporary discussions reveal:\n\n"
        
        for i, source in enumerate(sources_data[:3], 1):
            response += f"• Perspective {i}: {source['content'][:120]}...\n\n"
        
        response += f"These modern perspectives enrich our understanding of your question about '{user_input}'. "
        
        return response
    
    def _create_ethics_response(self, sources_data: List[Dict], philosopher: str) -> str:
        """Create response about ethics and morality"""
        response = "Ethical questions remain at the heart of philosophical inquiry, with contemporary sources offering:\n\n"
        
        for i, source in enumerate(sources_data[:3], 1):
            if any(eth_word in source.get('content', '').lower() for eth_word in ['moral', 'ethical', 'right', 'wrong', 'should']):
                response += f"• Ethical insight: {source['content'][:150]}...\n\n"
        
        if philosopher == "kant":
            response += "These discussions reflect the enduring relevance of the categorical imperative: act only according to that maxim whereby you can will that it should become a universal law."
        elif philosopher == "aristotle":
            response += "Contemporary ethics confirms what I taught: virtue lies in finding the mean between extremes, requiring practical wisdom in each situation."
        else:
            response += "These ethical perspectives remind us that moral reasoning requires both philosophical rigor and practical wisdom."
        
        return response
    
    def _create_existence_response(self, sources_data: List[Dict], philosopher: str) -> str:
        """Create response about existence and reality"""
        response = "Questions of existence and reality continue to challenge philosophers, with modern insights revealing:\n\n"
        
        for i, source in enumerate(sources_data[:3], 1):
            if any(exist_word in source.get('content', '').lower() for exist_word in ['exist', 'reality', 'being', 'truth']):
                response += f"• Ontological perspective: {source['content'][:150]}...\n\n"
        
        if philosopher == "sartre":
            response += "These explorations confirm that existence precedes essence - we exist first, then create our essence through our choices and actions."
        elif philosopher == "dostoevsky":
            response += "The mystery of existence continues to reveal the profound tensions between reason and faith, logic and the human heart."
        else:
            response += "These investigations into reality's nature remind us that existence itself remains philosophy's most fundamental puzzle."
        
        return response
    
    def _create_consciousness_response(self, sources_data: List[Dict], philosopher: str) -> str:
        """Create response about consciousness and mind"""
        response = "The nature of consciousness remains one of philosophy's greatest puzzles, with current research exploring:\n\n"
        
        for i, source in enumerate(sources_data[:3], 1):
            if any(mind_word in source.get('content', '').lower() for mind_word in ['consciousness', 'mind', 'awareness', 'thinking']):
                response += f"• Consciousness research: {source['content'][:150]}...\n\n"
        
        if philosopher == "sartre":
            response += "Consciousness, as I've argued, is always consciousness of something - it is intentional, directed outward, the foundation of our being-for-itself."
        elif philosopher == "kant":
            response += "These studies of consciousness return us to the transcendental ego - the unity of consciousness that makes experience possible."
        else:
            response += "Understanding consciousness requires bridging the gap between subjective experience and objective scientific investigation."
        
        return response
    
    def _get_persona_intro(self, philosopher: str) -> str:
        """Get philosopher-specific introduction"""
        intros = {
            "camus": "Ah, mon ami, this touches the very heart of the absurd condition...",
            "nietzsche": "Ha! You ask a question that pierces through conventional morality...",
            "dostoevsky": "My friend, you probe the depths of human psychology...",
            "sartre": "This question confronts us with our radical freedom...",
            "beauvoir": "We must examine this through the lens of situated experience...",
            "kant": "Let us approach this with rigorous rational analysis...",
            "aristotle": "In considering this matter, we must examine the virtuous path...",
            "marcus": "The Stoic way teaches us to consider this calmly...",
            "guide": "This is a profound philosophical question that deserves careful consideration..."
        }
        return intros.get(philosopher.lower(), intros["guide"])
    
    def _get_persona_conclusion(self, philosopher: str, user_input: str) -> str:
        """Get philosopher-specific conclusion"""
        conclusions = {
            "camus": "Thus, we must revolt against meaninglessness not through escape, but through passionate engagement with life itself.",
            "nietzsche": "Will to power demands that we create our own values rather than accepting inherited ones.",
            "dostoevsky": "The human heart remains a battlefield between faith and doubt, love and suffering.",
            "sartre": "We are condemned to be free, and must choose our authentic response to this situation.",
            "beauvoir": "We must recognize both our freedom and our situated constraints in ethical action.",
            "kant": "The categorical imperative guides us toward universal moral principles.",
            "aristotle": "Virtue lies in the mean between extremes, requiring practical wisdom.",
            "marcus": "Accept what cannot be changed, change what can be, and develop wisdom to know the difference.",
            "guide": "Philosophy offers not final answers, but better ways of questioning."
        }
        return conclusions.get(philosopher.lower(), conclusions["guide"])
    
    def _get_basic_philosophical_response(self, user_input: str, philosopher: str) -> str:
        """Basic philosophical response when no internet context available"""
        persona_intro = self._get_persona_intro(philosopher)
        persona_conclusion = self._get_persona_conclusion(philosopher, user_input)
        
        return f"""{persona_intro}

Your question about "{user_input}" opens up rich philosophical territory. While I'm currently experiencing some technical limitations that prevent me from accessing my usual resources, I can share that this type of inquiry has occupied philosophers for centuries.

{persona_conclusion}

I encourage you to explore this question further - perhaps rephrasing it or asking about specific aspects that intrigue you most."""


# Initialize the modern system
def create_modern_philosopher_chat():
    """Factory function to create modern philosopher chat"""
    return ModernPhilosopherChat()

if __name__ == "__main__":
    # Test the system
    chat = ModernPhilosopherChat()
    
    test_questions = [
        "What does Camus think about artificial intelligence?",
        "How would Nietzsche view social media?",
        "What is the philosophical significance of climate change?",
        "How do modern philosophers discuss the meaning of life?"
    ]
    
    for question in test_questions:
        print(f"\n🔮 Question: {question}")
        response = chat.chat(question, "camus")
        print(f"🤖 Response: {response[:200]}...")