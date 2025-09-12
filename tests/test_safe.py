#!/usr/bin/env python3
"""
SAFE test script - no heavy AI models that could crash your system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_safe_imports():
    """Test that we can import safely without crashes."""
    print("Testing safe imports...")
    
    try:
        from app.utils.rag_engine_safe import RAGEngine
        from app.models_safe import PhilosopherChat
        print("✅ Safe imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_safe_rag_engine():
    """Test the safe RAG engine."""
    print("Testing safe RAG engine...")
    
    try:
        from app.utils.rag_engine_safe import RAGEngine
        
        rag = RAGEngine()
        
        # Test retrieval (should work without crashing)
        context = rag.retrieve_context("What is the meaning of life?", "camus")
        print(f"✅ Retrieved {len(context)} context chunks safely")
        
        # Test simple response generation
        response = rag.generate_simple_response(
            "What is existentialism?", 
            "camus", 
            context
        )
        print(f"✅ Generated response: {response[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG engine error: {e}")
        return False

def test_safe_philosopher_chat():
    """Test the safe philosopher chat."""
    print("Testing safe philosopher chat...")
    
    try:
        from app.models_safe import PhilosopherChat
        
        chat = PhilosopherChat()
        
        # Test response generation
        response = chat.generate_response(
            user_message="What is the purpose of life?",
            philosopher="camus",
            context=["Life has no inherent meaning"],
            conversation_id="test_123"
        )
        
        print(f"✅ Generated philosopher response: {response['message'][:50]}...")
        print(f"✅ Sources: {len(response['sources'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Philosopher chat error: {e}")
        return False

def test_flask_app():
    """Test that Flask app can start safely."""
    print("Testing Flask app startup...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            print(f"✅ Home page status: {response.status_code}")
            
            # Test philosophers endpoint
            response = client.get('/api/philosophers')
            print(f"✅ Philosophers API status: {response.status_code}")
            
        return True
        
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def main():
    """Run all safe tests."""
    print("🛡️ Running SAFE Philosophy Chatbot Tests")
    print("="*50)
    
    tests = [
        ("Safe Imports", test_safe_imports),
        ("Safe RAG Engine", test_safe_rag_engine),
        ("Safe Philosopher Chat", test_safe_philosopher_chat),
        ("Flask App", test_flask_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
            print(f"❌ Test failed: {e}")
    
    # Results summary
    print("\n" + "="*50)
    print("📊 SAFE Test Results:")
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
        print("🎉 All safe tests passed! Your system is protected.")
        print("\n🚀 Next steps:")
        print("1. Run: python run.py")
        print("2. Open: http://localhost:5000")
        print("3. Chat safely with philosophers!")
    else:
        print("⚠️ Some tests failed. Check errors above.")
    
    return all_passed

if __name__ == "__main__":
    main()