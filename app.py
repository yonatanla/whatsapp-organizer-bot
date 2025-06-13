# app.py
import os
from flask import Flask, request
from dotenv import load_dotenv
import threading

# Import our own modules
from bot_logic import process_command
from services import send_whatsapp_message
from scheduler import run_scheduler

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verifies the webhook subscription with Meta."""
    verify_token = "vcuyvxushakh009!" # Your secret token
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token and mode == "subscribe" and token == verify_token:
        print("WEBHOOK_VERIFIED")
        return challenge, 200
    else:
        return "Verification token mismatch", 403

@app.route('/webhook', methods=['POST'])
def handle_message():
    """Handles incoming messages from WhatsApp."""
    body = request.get_json()
    print("Received message:", body)  # For debugging

    if body.get("object") == "whatsapp_business_account":
        try:
            message_info = body['entry'][0]['changes'][0]['value']
            message = message_info['messages'][0]
            from_number = message['from']
            message_text = message['text']['body']
            phone_number_id = message_info['metadata']['phone_number_id']

            # Let the bot logic module decide what to do
            reply_text = process_command(message_text)

            # If the command generated a reply, send it
            if reply_text:
                send_whatsapp_message(from_number, phone_number_id, reply_text)

        except (IndexError, KeyError) as e:
            print(f"Could not parse message: {e}")
            pass  # Not a message notification we can handle

    return "OK", 200

if __name__ == '__main__':
    # Start the scheduler in a background thread
    # scheduler_thread = threading.Thread(target=run_scheduler)
    # scheduler_thread.daemon = True
    # scheduler_thread.start()

    # Run the Flask web server
    # The host='0.0.0.0' is important for deployment services like Render or Heroku
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)), debug=True)