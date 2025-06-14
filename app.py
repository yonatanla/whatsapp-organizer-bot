# app.py
import os
from flask import Flask, request
from dotenv import load_dotenv
import threading

# Load environment variables from .env file FIRST
load_dotenv() 

# Import our own modules
from bot_logic import process_message
from services import configure_services
from database import initialize_database

# Configure services and database on startup
configure_services()
initialize_database()

app = Flask(__name__)

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verifies the webhook subscription with Meta."""
    verify_token = "YOUR_OWN_SECRET_TOKEN" 
    
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token and mode == "subscribe" and token.lower() == verify_token.lower():
        print("WEBHOOK_VERIFIED")
        return challenge, 200
    else:
        print(f"Verification failed: Received token '{token}' did not match expected token '{verify_token}'.")
        return "Verification token mismatch", 403

@app.route('/webhook', methods=['POST'])
def handle_message():
    """Handles incoming messages from WhatsApp."""
    body = request.get_json()
    print("Received message:", body)

    try:
        # Extract the message information from the webhook payload
        message_info = body['entry'][0]['changes'][0]['value']
        
        # Check if it's a message notification
        if 'messages' in message_info:
            message_details = message_info['messages'][0]
            
            # Get sender's profile name and message text
            sender_name = message_info['contacts'][0]['profile']['name']
            message_text = message_details['text']['body']
            from_number = message_details['from']
            phone_number_id = message_info['metadata']['phone_number_id']

            # Let the bot logic module handle the message
            process_message(sender_name, message_text, from_number, phone_number_id)
            
    except (IndexError, KeyError) as e:
        print(f"Could not parse message or non-message webhook: {e}")
        pass

    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)), debug=True)
