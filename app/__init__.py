# app/__init__.py
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import threading
from .bot.database import initialize_database
from .bot.services import configure_services, schedule_daily_digest

# Load environment variables from .env file
load_dotenv()

socketio = SocketIO()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    socketio.init_app(app)

    # Initialize services and database
    with app.app_context():
        initialize_database()
        configure_services(app.config)
        
        # Start the scheduler in a background thread
        scheduler_thread = threading.Thread(target=schedule_daily_digest, daemon=True)
        scheduler_thread.start()

    # Register Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
