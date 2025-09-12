from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

def create_app():
    """Create and configure the Flask application."""
    
    # Load environment variables
    load_dotenv()
    
    # Get the absolute path to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(project_root, 'templates')
    static_dir = os.path.join(project_root, 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir, 
                static_folder=static_dir)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app
