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
        print("ERROR: API keys not found.")
    else:
        genai.configure(api_key=gemini_api_key)
        print("Services configured successfully.")

def send_whatsapp_message(to_number, phone_number_id, text):
    """Sends a message to a user via the WhatsApp Cloud API."""
    if not WHATSAPP_TOKEN:
        print("ERROR: WhatsApp token not configured.")
        return

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = { "Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json" }
    data = { "messaging_product": "whatsapp", "to": to_number, "text": {"body": text} }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

def get_summary_and_actions_with_gemini(conversation_history):
    """
    Uses Gemini's JSON mode to analyze a conversation and extract a summary
    and action items in a structured format.
    """
    if not conversation_history:
        return "{}"

    formatted_conversation = "\n".join(conversation_history)
    
    prompt = f"""
    Analyze the following WhatsApp conversation. Your user is Yonatan.
    Provide your response as a valid JSON object with two keys:
    1. "summary": A brief, one-sentence summary of the conversation's main topic.
    2. "action_items": A list of strings, where each string is a specific task or action item for Yonatan.
    If there are no action items, the list should be empty.

    Conversation:
    ---
    {formatted_conversation}
    ---
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return '{ "summary": "Error analyzing conversation.", "action_items": [] }'

def analyze_for_task(message):
    """
    NEW: Uses Gemini to determine if a single message contains a task.
    """
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
    
    prompt = f"""
    Analyze the following message. Your user's name is Yonatan.
    Determine if the message contains an explicit or implicit task, to-do item, or reminder for Yonatan.
    Respond with a JSON object with two keys:
    1. "is_task": boolean (true if it is a task, false otherwise).
    2. "task_description": a string containing the clear, concise task description if is_task is true, otherwise an empty string. Reword the task as a simple command, for example, "Call the accountant tomorrow morning."

    Message: "{message}"
    """
    
    try:
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text
    except Exception as e:
        print(f"Gemini Task Analysis Error: {e}")
        return '{ "is_task": false, "task_description": "" }'
