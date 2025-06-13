# services.py
import os
import requests
import google.generativeai as genai

# Load API keys from the environment
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)


def send_whatsapp_message(to_number, phone_number_id, text):
    """Sends a message to a user via the WhatsApp Cloud API."""
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
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""
    Please summarize the following list of tasks in Hebrew.
    Provide a short, easy-to-read summary that captures the main activities for the day.

    Task list:
    {text_to_summarize}

    Summary:
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "מצטער, הייתה בעיה ביצירת הסיכום באמצעות Gemini."
