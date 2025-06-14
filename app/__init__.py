# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
import threading
import os
from .bot.database import initialize_database
from .bot.services import configure_services, schedule_daily_digest

# Load environment variables from .env file
load_dotenv()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # This check ensures the scheduler runs only once, not on every worker thread
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        with app.app_context():
            initialize_database()
            configure_services(app.config)
            
            # Start the scheduler in a background thread
            scheduler_thread = threading.Thread(target=schedule_daily_digest, args=(app,), daemon=True)
            scheduler_thread.start()

    # Register Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
