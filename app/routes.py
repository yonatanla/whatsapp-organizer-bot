# app/routes.py
from flask import Blueprint, request, current_app
from .bot.logic import process_message, verify_webhook_token

main = Blueprint('main', __name__)

@main.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verifies the webhook subscription with Meta."""
    if verify_webhook_token(request.args):
        return request.args.get("hub.challenge"), 200
    return "Verification token mismatch", 403

@main.route('/webhook', methods=['POST'])
def handle_message():
    """Handles incoming messages from WhatsApp."""
    data = request.get_json()
    process_message(data)
    return "OK", 200