# bot_logic.py
from services import get_summary_and_actions_with_gemini, send_whatsapp_message, analyze_for_task
from database import add_message, get_recent_messages, clear_history, add_task, get_tasks, complete_task
import json

def process_message(sender_name, message_text, from_number, phone_number_id):
    """
    Saves every message and intelligently responds to commands or natural language.
    """
    add_message(sender_name, message_text)
    
    cmd_lower = message_text.lower()
    reply = None

    # --- Command Handling ---
    if cmd_lower.startswith('/'):
        command_part = cmd_lower.split()[0]
        
        if command_part == "/summary":
            conversation_history = get_recent_messages()
            json_string = get_summary_and_actions_with_gemini(conversation_history)
            try:
                data = json.loads(json_string)
                summary = data.get("summary", "No summary available.")
                action_items = data.get("action_items", [])
                reply = f"🤖 *סיכום שיחה:*\n{summary}\n\n"
                if action_items:
                    reply += "📋 *משימות לביצוע:*\n"
                    for item in action_items:
                        reply += f"- {item}\n"
                else:
                    reply += "✅ *אין משימות חדשות עבורך.*"
                clear_history()
            except (json.JSONDecodeError, TypeError):
                reply = "מצטער, לא הצלחתי לעבד את הסיכום."

        elif command_part == "/help":
            reply = (
                "שלום! אני העוזר האישי שלך.\n\n"
                "📝 *ניהול משימות:*\n"
                "- פשוט כתוב לי מה לעשות (לדוגמה: 'אני צריך לזכור להתקשר לרואה החשבון')\n"
                "- `/tasks` - הצגת המשימות הפתוחות.\n"
                "- `/done [מספר]` - סגירת משימה.\n\n"
                "🧠 *ניתוח שיחה:*\n"
                "- `/summary` - סיכום השיחה האחרונה.\n"
                "- `/clear` - מחיקת היסטוריית השיחה."
            )
        
        elif command_part == "/clear":
            clear_history()
            reply = "🧹 היסטוריית השיחה נמחקה."

        elif command_part == "/tasks":
            tasks = get_tasks()
            if not tasks:
                reply = "🎉 אין לך משימות פתוחות!"
            else:
                reply = "📋 *משימות פתוחות:*\n"
                for task_id, description in tasks:
                    reply += f"{task_id}. {description}\n"
        
        elif command_part == "/done":
            try:
                task_id = int(cmd_lower.split()[1])
                reply = complete_task(task_id)
            except (IndexError, ValueError):
                reply = "אנא ציין מספר משימה. לדוגמה: `/done 2`"

    # --- NEW: Natural Language Task Detection ---
    else:
        # If the message is not a command, ask Gemini if it's a task
        task_json = analyze_for_task(message_text)
        try:
            task_data = json.loads(task_json)
            if task_data.get("is_task"):
                task_description = task_data.get("task_description")
                if task_description:
                    reply = add_task(task_description)
        except (json.JSONDecodeError, TypeError):
            pass # Not a task, so we remain silent

    # Send the reply if one was generated
    if reply:
        send_whatsapp_message(from_number, phone_number_id, reply)
