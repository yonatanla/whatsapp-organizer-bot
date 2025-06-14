# app/bot/logic.py
from .services import get_summary_and_actions_with_gemini, send_text_message, send_interactive_message, analyze_for_task
from .database import add_message, get_recent_messages, clear_history, add_task, get_tasks, complete_task
from flask import current_app
import json

def verify_webhook_token(args):
    """Verifies the webhook token from Meta."""
    token = args.get("hub.verify_token")
    mode = args.get("hub.mode")
    if mode == "subscribe" and token == current_app.config['VERIFY_TOKEN']:
        return True
    return False

def process_message(data):
    """Processes incoming webhook data from WhatsApp."""
    try:
        message_info = data['entry'][0]['changes'][0]['value']
        if 'messages' in message_info:
            message_details = message_info['messages'][0]
            
            # Handling different message types
            if message_details['type'] == 'text':
                process_text_message(message_info, message_details)
            elif message_details['type'] == 'interactive':
                process_interactive_message(message_info, message_details)
                
    except (IndexError, KeyError) as e:
        print(f"Error parsing webhook: {e}")

def process_text_message(message_info, message_details):
    """Handles regular text messages."""
    sender_name = message_info['contacts'][0]['profile']['name']
    message_text = message_details['text']['body']
    from_number = message_details['from']
    
    add_message(sender_name, message_text)
    
    cmd_lower = message_text.lower()
    reply = None

    if cmd_lower.startswith('/'):
        command_part = cmd_lower.split()[0]
        
        if command_part == "/tasks":
            tasks = get_tasks()
            if not tasks:
                send_text_message(from_number, "🎉 אין לך משימות פתוחות!")
            else:
                buttons = [{"type": "reply", "reply": {"id": f"done_{task_id}", "title": f"סמן כבוצע: {description[:20]}"}} for task_id, description in tasks]
                send_interactive_message(from_number, "📋 *משימות פתוחות:*", buttons)
        
        elif command_part == "/help":
            reply = (
                "שלום! אני העוזר האישי שלך.\n\n"
                "📝 *ניהול משימות:*\n"
                "- פשוט כתוב לי מה לעשות (לדוגמה: 'אני צריך לזכור להתקשר לרואה החשבון')\n"
                "- `/tasks` - הצגת המשימות הפתוחות עם כפתורים.\n\n"
                "🧠 *ניתוח שיחה:*\n"
                "- `/summary` - סיכום השיחה האחרונה.\n"
                "- `/clear` - מחיקת היסטוריית השיחה."
            )
            send_text_message(from_number, reply)
        
        elif command_part == "/clear":
            clear_history()
            send_text_message(from_number, "🧹 היסטוריית השיחה נמחקה.")
        
        # ... other commands like /summary can be added here ...

    else:
        task_json = analyze_for_task(message_text)
        try:
            task_data = json.loads(task_json)
            if task_data.get("is_task") and task_data.get("task_description"):
                reply = add_task(task_data["task_description"])
                send_text_message(from_number, reply)
        except (json.JSONDecodeError, TypeError):
            pass

def process_interactive_message(message_info, message_details):
    """Handles replies from interactive buttons."""
    from_number = message_details['from']
    button_reply = message_details['interactive']['button_reply']
    button_id = button_reply['id']
    
    if button_id.startswith("done_"):
        task_id = int(button_id.split('_')[1])
        reply = complete_task(task_id)
        send_text_message(from_number, reply)
