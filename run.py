# run.py
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Use os.environ.get('PORT', 5001) for compatibility with Render
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)