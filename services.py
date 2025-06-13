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
        # In a real app, you might want to raise an exception here
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


def summarize_with_gemini(text_to_summarize):
    """Generates a summary using the Gemini API."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"""
        Please summarize the following list of tasks in Hebrew.
        Provide a short, easy-to-read summary that captures the main activities for the day.

        Task list:
        {text_to_summarize}

        Summary:
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "מצטער, הייתה בעיה ביצירת הסיכום באמצעות Gemini."
