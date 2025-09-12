#!/usr/bin/env python3
"""
Test script for AI Philosophy Chatbot functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.rag_engine import RAGEngine
from app.models import PhilosopherChat

def test_rag_engine():
    """Test the RAG engine functionality."""
    print("Testing RAG Engine...")
    
    rag = RAGEngine()
    
    # Test retrieval
    context = rag.retrieve_context("What is existentialism?", "neutral", top_k=2)
    
    print(f"Retrieved {len(context)} context chunks:")
    for i, chunk in enumerate(context, 1):
        print(f"  {i}. {chunk[:100]}...")
    
    return len(context) > 0

def test_philosopher_chat():
    """Test philosopher chat without OpenAI API."""
    print("\nTesting Philosopher Chat (without API)...")
    
    chat = PhilosopherChat()
    
    # Test philosopher prompts
    prompts = chat._load_philosopher_prompts()
    print(f"Loaded {len(prompts)} philosopher prompts:")
    for name in prompts.keys():
        print(f"  - {name}")
    
    return len(prompts) > 0

def test_data_files():
    """Test that data files exist."""
    print("\nTesting Data Files...")
    
    required_files = [
        "data/processed/embeddings.faiss",
        "data/processed/chunks.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"  ✓ {file_path}")
    
    if missing_files:
        print(f"  ✗ Missing files: {missing_files}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🧪 Running AI Philosophy Chatbot Tests\n")
    
    tests = [
        ("RAG Engine", test_rag_engine),
        ("Philosopher Chat", test_philosopher_chat),
        ("Data Files", test_data_files)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
    
    print("\n" + "="*50)
    print("📊 Test Results:")
    print("="*50)
    
    all_passed = True
    for test_name, passed, error in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if error:
            print(f"     Error: {error}")
        all_passed = all_passed and passed
    
    print("="*50)
    if all_passed:
        print("🎉 All tests passed! The chatbot is ready to use.")
        print("\n📋 Next steps:")
        print("1. Add your OpenAI API key to the .env file")
        print("2. Run: python run.py")
        print("3. Open http://localhost:5000 in your browser")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    main()
