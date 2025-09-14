#!/usr/bin/env python3
"""
Demo script to show how the Internet RAG system works WITHOUT AI generation
This proves it's NOT static - it gets fresh content every time
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.internet_rag_engine import InternetRAGEngine

def main():
    print("🔍 DEMONSTRATING REAL-TIME INTERNET CONTENT EXTRACTION")
    print("=" * 60)
    
    # Create search engine
    search_engine = InternetRAGEngine()
    
    # Test different queries to show it's dynamic
    queries = [
        "artificial intelligence consciousness philosophy 2025",
        "meaning of life existentialism modern philosophy",
        "ethics AI technology philosophy current debates"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n🔍 QUERY {i}: {query}")
        print("-" * 50)
        
        try:
            # Get real-time internet content
            sources = search_engine.search_philosophy_content(query)
            
            print(f"✅ Found {len(sources)} LIVE internet sources")
            
            # Show first 2 sources to prove it's dynamic
            for j, source in enumerate(sources[:2], 1):
                print(f"\nSOURCE {j}:")
                print(f"  FROM: {source.get('source', 'unknown')}")
                print(f"  TITLE: {source.get('title', 'No title')[:60]}...")
                print(f"  CONTENT: {source.get('content', 'No content')[:150]}...")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 KEY POINT: This content is fetched LIVE from the internet")
    print("   - Different every time you run it")
    print("   - Gets current discussions and debates")
    print("   - NOT from static files!")

if __name__ == "__main__":
    main()