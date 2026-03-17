# SocrAItes - AI Philosophy Chatbot

Experience philosophical dialogue through persona-based AI conversations powered by Retrieval Augmented Generation (RAG), Groq inference, and optional voice playback.

## What Is New

The project now supports two clear usage phases:

- Phase 1: Text chat with philosopher personas and RAG-grounded responses
- Phase 2: Voice mode with generated audio playback and replay controls

## Core Features

- Multi-persona philosophical chat (Camus, Dostoevsky, Nietzsche, Socrates, Kafka, Cioran)
- RAG pipeline combining local philosophy context and optional internet retrieval
- Groq-backed response generation for low-latency inference
- Streaming text chat endpoint for interactive UI updates
- Voice mode using server-side TTS plus replay controls
- Safe fallback paths when APIs are unavailable

## Architecture Overview

- Frontend: HTML, CSS, JavaScript single-page chat interface
- Backend: Flask routes for chat, streaming, metadata, status, and TTS
- Retrieval: Vector/semantic retrieval from philosophy-focused data
- Generation: Groq model orchestration with persona prompting
- Voice: TTS endpoint returning audio/mpeg for client playback and replay

## Why RAG

RAG is used to improve response grounding and reduce hallucinations.

- Injects relevant context before generation
- Improves domain relevance for philosophical discussions
- Keeps generated answers closer to trusted source material
- Enables context updates without retraining the model

## Why Groq

Groq is used primarily for speed and integration simplicity.

- Fast inference suitable for interactive chat UX
- Reliable API integration for Flask pipelines
- Good practical quality-latency balance for this application type

## Tech Stack

- Python, Flask, Flask-CORS
- requests, python-dotenv
- sentence-transformers, faiss-cpu, scikit-learn, numpy, pandas, nltk
- edge-tts for voice synthesis
- HTML/CSS/JavaScript for frontend

## Project Structure

SocrAItes/
- app/
  - __init__.py
  - routes.py
  - models.py
  - models_safe.py
  - ai_models.py
  - utils/
    - groq_philosophy_chat.py
    - internet_rag_engine.py
    - rag_engine.py
    - rag_engine_safe.py
    - advanced_hf_chat.py
    - groq_chat.py
- data/
  - raw/
- static/
  - css/style.css
  - js/app.js
- templates/
  - index.html
- scripts/
  - prepare_data.py
- tests/
  - test_safe.py
  - test_setup.py
- run.py
- requirements.txt
- docs/
  - latex_report_roadmap.md

## Quick Start

1. Clone repository

   git clone https://github.com/med-adam-alimi/SocrAItes.git
   cd SocrAItes

2. Create and activate virtual environment

   Windows:
   python -m venv .venv
   .venv\Scripts\activate

   Linux or macOS:
   python3 -m venv .venv
   source .venv/bin/activate

3. Install dependencies

   pip install -r requirements.txt

4. Configure environment variables in .env

   Required for Groq mode:
   GROQ_API_KEY=your_key_here

   Recommended:
   API_TYPE=groq
   USE_INTERNET_SEARCH=true
   FLASK_DEBUG=false

5. Run application

   python run.py

6. Open browser

   http://127.0.0.1:5000

## API Endpoints

- GET / : Main chat UI
- POST /api/chat : Standard chat response
- POST /api/chat/stream : Streaming text response
- GET /api/philosophers : Available personas
- GET /api/topics : Suggested topics
- GET /api/status : System capability status
- POST /api/tts : Text-to-speech audio generation
- POST /api/clear_conversation : Clear session conversation

## Text Mode (Phase 1)

- User sends philosophical prompt
- Backend retrieves context using RAG
- Persona-conditioned prompt is sent to model
- Text response is returned and rendered

## Voice Mode (Phase 2)

- Voice mode can generate audio from response text
- Playback controls support replay of generated voice
- If autoplay is blocked by browser policy, user can trigger playback via replay control

## Testing

Run available scripts from project root:

- python test_quick.py
- python test_comprehensive.py
- python test_api.py
- python tests/test_setup.py
- python tests/test_safe.py

## Documentation

For report planning and chapter roadmap:

- docs/latex_report_roadmap.md

## License

MIT License (if LICENSE file is present in repository).

## Acknowledgments

- Public philosophy resources and excerpts used for retrieval context
- Open-source Python ecosystem
- Groq and TTS tooling communities
