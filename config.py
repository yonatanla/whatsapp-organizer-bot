# config.py
import os

class Config:
    """Configuration settings for the bot."""
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', "YOUR_OWN_SECRET_TOKEN")
    PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

    # Prompts for the AI
    SUMMARY_PROMPT = """
    Analyze the following WhatsApp conversation. Your user is Yonatan.
    Provide your response as a valid JSON object with two keys:
    1. "summary": A brief, one-sentence summary of the conversation's main topic.
    2. "action_items": A list of strings, where each string is a specific task or action item for Yonatan.
    If there are no action items, the list should be empty.

    Conversation:
    ---
    {conversation}
    ---
    """

    TASK_ANALYSIS_PROMPT = """
    Analyze the following message. Your user's name is Yonatan.
    Determine if the message contains an explicit or implicit task, to-do item, or reminder for Yonatan.
    Respond with a JSON object with two keys:
    1. "is_task": boolean (true if it is a task, false otherwise).
    2. "task_description": a string containing the clear, concise task description if is_task is true, otherwise an empty string. Reword the task as a simple command, for example, "Call the accountant tomorrow morning."

    Message: "{message}"
    """
