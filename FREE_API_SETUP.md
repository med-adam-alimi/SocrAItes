# 🆓 Free API Setup Guide

## Option 1: Hugging Face (Recommended - Completely Free!)

### Step 1: Get Free API Token
1. Go to [huggingface.co](https://huggingface.co)
2. Create a free account
3. Go to Settings → Access Tokens
4. Create a new token (read permission is enough)
5. Copy the token

### Step 2: Add to .env file
```bash
API_TYPE=huggingface
HUGGINGFACE_API_KEY=hf_your_token_here
```

### Step 3: Test it!
```bash
python run.py
```

## Option 2: Together AI (Free Tier)

### Step 1: Get Free API Key
1. Go to [together.ai](https://api.together.xyz)
2. Sign up for free account
3. Get $5 free credits (good for thousands of requests)
4. Copy your API key

### Step 2: Add to .env file
```bash
API_TYPE=together
TOGETHER_API_KEY=your_together_key_here
```

## Option 3: No API Keys (Fallback Mode)

If you don't want to sign up for anything:

### Step 1: Set fallback mode
```bash
API_TYPE=fallback
```

This will use pre-written philosophical responses - not AI generated, but still educational!

## 🚀 Quick Start Commands

```bash
# 1. Install dependencies (if not done)
pip install -r requirements.txt

# 2. Update your .env file with a free API key

# 3. Test the setup
python tests/test_setup.py

# 4. Run the app
python run.py

# 5. Open browser: http://localhost:5000
```

## ✨ What You Get for FREE:

- ✅ Unlimited local RAG (text retrieval)
- ✅ Philosophy text database
- ✅ Web interface
- ✅ Philosopher personas
- ✅ AI responses (with free API)
- ✅ No heavy CPU usage
- ✅ Works on any computer

## 📊 Free Tier Limits:

**Hugging Face**: Unlimited (with rate limits)
**Together AI**: $5 credit = ~10,000 messages
**Fallback Mode**: Unlimited (pre-written responses)

Choose the option that works best for you! 🎯
