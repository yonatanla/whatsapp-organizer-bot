# app/bot/services.py
import os
import requests
import google.generativeai as genai
import schedule
import time
from flask import current_app
from .database import get_tasks

CONFIG = None

def configure_services(app_config):
    """Configures the API clients with settings from the config object."""
    global CONFIG
    CONFIG = app_config
    if not CONFIG['WHATSAPP_TOKEN'] or not CONFIG['GEMINI_API_KEY']:
        print("ERROR: API keys not found in config.")
    else:
        genai.configure(api_key=CONFIG['GEMINI_API_KEY'])
        print("Services configured successfully.")

def send_text_message(to_number, text):
    """Sends a simple text message."""
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "text": {"body": text}
    }
    _send_whatsapp_request(payload)

def send_interactive_message(to_number, body_text, buttons):
    """Sends a message with interactive buttons."""
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body_text},
            "action": {"buttons": buttons}
        }
    }
    _send_whatsapp_request(payload)

def _send_whatsapp_request(data):
    """Helper function to send API requests to WhatsApp."""
    if not CONFIG or not CONFIG['WHATSAPP_TOKEN']:
        print("ERROR: Service not configured.")
        return
    url = f"https://graph.facebook.com/v19.0/{CONFIG['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {CONFIG['WHATSAPP_TOKEN']}", "Content-Type": "application/json"}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e.response.text}")

def get_summary_and_actions_with_gemini(conversation_history):
    """Analyzes a conversation for summary and action items."""
    if not conversation_history:
        return "{}"
    formatted_conversation = "\n".join(conversation_history)
    prompt = CONFIG['SUMMARY_PROMPT'].format(conversation=formatted_conversation)
    return _call_gemini(prompt)

def analyze_for_task(message):
    """Determines if a message contains a task."""
    prompt = CONFIG['TASK_ANALYSIS_PROMPT'].format(message=message)
    return _call_gemini(prompt)

def _call_gemini(prompt):
    """Helper function to call the Gemini API with JSON mode."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return '{}' # Return empty JSON on error

def send_daily_digest():
    """Scheduled job to send a daily summary of open tasks."""
    print("Running daily digest job...")
    tasks = get_tasks()
    if tasks:
        # NOTE: You need to define which user to send the digest to.
        # This should be your personal WhatsApp number from the .env file.
        user_number = os.getenv('MY_PERSONAL_PHONE_NUMBER')
        if user_number:
            message = "☀️ *סיכום משימות יומי:*\n"
            for task_id, description in tasks:
                message += f"- {description}\n"
            send_text_message(user_number, message)
        else:
            print("Could not send daily digest: MY_PERSONAL_PHONE_NUMBER not set.")

def schedule_daily_digest():
    """Sets up the scheduler to run the digest job."""
    schedule.every().day.at("08:00").do(send_daily_digest)
    while True:
        schedule.run_pending()
        time.sleep(60)
