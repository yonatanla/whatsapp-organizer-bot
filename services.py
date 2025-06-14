# services.py
import os
import requests
import google.generativeai as genai

WHATSAPP_TOKEN = None

def configure_services():
    """Configures the API clients after environment variables are loaded."""
    global WHATSAPP_TOKEN
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not WHATSAPP_TOKEN or not gemini_api_key:
        print("ERROR: API keys not found. Please set WHATSAPP_TOKEN and GEMINI_API_KEY environment variables.")
    else:
        genai.configure(api_key=gemini_api_key)
        print("Services configured successfully.")


def send_whatsapp_message(to_number, phone_number_id, text):
    """Sends a message to a user via the WhatsApp Cloud API."""
    if not WHATSAPP_TOKEN:
        print("ERROR: WhatsApp token not configured.")
        return

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {"messaging_product": "whatsapp", "to": to_number, "text": {"body": text}}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")


def get_summary_and_actions_with_gemini(conversation_history):
    """
    Uses Gemini to analyze a conversation, summarize it, 
    and extract action items.
    """
    if not conversation_history:
        return "No conversation history to analyze."

    # Format the conversation for the AI
    formatted_conversation = "\n".join(conversation_history)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # This is a more advanced prompt for the AI
        prompt = f"""
        You are a personal assistant. Your user, Yonatan, is busy and needs you to analyze the following WhatsApp conversation.
        Please perform two tasks:
        1. Provide a brief, one-sentence summary of the main topic of the conversation.
        2. Identify and list any action items or tasks that were assigned to Yonatan, or that Yonatan needs to do. Look for mentions of his name or phrases like "you need to," "can you," etc. If there are no action items for him, state "No action items for Yonatan."

        Here is the conversation:
        ---
        {formatted_conversation}
        ---

        Analysis:
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "מצטער, הייתה בעיה בניתוח השיחה באמצעות Gemini."
