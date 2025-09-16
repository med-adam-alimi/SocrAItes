from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Production-optimized settings
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=debug_mode,
        threaded=True  # Better performance for multiple requests
    )
