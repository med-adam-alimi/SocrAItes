#!/usr/bin/env python3
"""
Quick test to verify your Groq API key works
Run this after adding GROQ_API_KEY to your .env file
"""

import os
import sys
import requests
from dotenv import load_dotenv

def test_groq_connection():
    print("🔥 TESTING GROQ API CONNECTION")
    print("=" * 40)
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key or api_key == 'your_free_groq_key_here':
        print("❌ No Groq API key found!")
        print()
        print("💡 Setup steps:")
        print("1. Go to: https://console.groq.com/")
        print("2. Sign up (FREE - no credit card)")
        print("3. Generate API key")
        print("4. Add to .env: GROQ_API_KEY=gsk_your_key_here")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test connection
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "messages": [{"role": "user", "content": "Hello, test message"}],
            "model": "llama-3.1-8b-instant",
            "max_tokens": 50,
            "temperature": 0.7
        }
        
        print("🧪 Testing connection...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            test_response = result['choices'][0]['message']['content']
            print("✅ SUCCESS! Groq API is working!")
            print(f"📝 Test response: {test_response[:100]}...")
            print()
            print("🎯 Your chatbot is ready to use!")
            print("Run: python app/utils/groq_philosophy_chat.py")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    test_groq_connection()