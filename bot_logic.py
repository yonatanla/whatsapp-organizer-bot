# bot_logic.py
from services import get_summary_and_actions_with_gemini, send_whatsapp_message
from database import add_message, get_recent_messages, clear_history
import json

def process_message(sender_name, message_text, from_number, phone_number_id):
    """
    Saves every message to the database and responds only to specific commands.
    """
    # Always save the message to our persistent database
    add_message(sender_name, message_text)
    
    cmd_lower = message_text.lower()

    # --- Command Handling ---

    if cmd_lower == "/summary":
        # Get the recent history from the database
        conversation_history = get_recent_messages()
        
        # Get the structured JSON response from Gemini
        json_string = get_summary_and_actions_with_gemini(conversation_history)
        
        try:
            # Parse the JSON string into a Python dictionary
            data = json.loads(json_string)
            
            # Format the reply beautifully
            summary = data.get("summary", "No summary available.")
            action_items = data.get("action_items", [])
            
            reply = f"🤖 *סיכום שיחה:*\n{summary}\n\n"
            
            if action_items:
                reply += "📋 *משימות לביצוע:*\n"
                for item in action_items:
                    reply += f"- {item}\n"
            else:
                reply += "✅ *אין משימות חדשות עבורך.*"
                
            # Clear the history from the database for the next summary
            clear_history()

        except json.JSONDecodeError:
            # If Gemini doesn't return valid JSON, send the raw text
            reply = "מצטער, לא הצלחתי לעבד את הסיכום. הנה התשובה הגולמית:\n" + json_string
            
        send_whatsapp_message(from_number, phone_number_id, reply)

    elif cmd_lower == "/help":
        reply = (
            "שלום! אני בוט העוזר האישי שלך.\n\n"
            "אני שומר את היסטוריית השיחה באופן אוטומטי.\n"
            "כדי לקבל סיכום ומשימות, כתוב `/summary`.\n"
            "כדי למחוק את ההיסטוריה, כתוב `/clear`."
        )
        send_whatsapp_message(from_number, phone_number_id, reply)

    elif cmd_lower == "/clear":
        clear_history()
        reply = "🧹 היסטוריית השיחה נמחקה. מתחילים דף חדש!"
        send_whatsapp_message(from_number, phone_number_id, reply)

    # Note: No 'else' block. The bot stays silent unless a command is issued.
# bot_logic.py
from services import get_summary_and_actions_with_gemini, send_whatsapp_message
from database import add_message, get_recent_messages, clear_history
import json

def process_message(sender_name, message_text, from_number, phone_number_id):
    """
    Saves every message to the database and responds only to specific commands.
    """
    # Always save the message to our persistent database
    add_message(sender_name, message_text)
    
    cmd_lower = message_text.lower()

    # --- Command Handling ---

    if cmd_lower == "/summary":
        # Get the recent history from the database
        conversation_history = get_recent_messages()
        
        # Get the structured JSON response from Gemini
        json_string = get_summary_and_actions_with_gemini(conversation_history)
        
        try:
            # Parse the JSON string into a Python dictionary
            data = json.loads(json_string)
            
            # Format the reply beautifully
            summary = data.get("summary", "No summary available.")
            action_items = data.get("action_items", [])
            
            reply = f"🤖 *סיכום שיחה:*\n{summary}\n\n"
            
            if action_items:
                reply += "📋 *משימות לביצוע:*\n"
                for item in action_items:
                    reply += f"- {item}\n"
            else:
                reply += "✅ *אין משימות חדשות עבורך.*"
                
            # Clear the history from the database for the next summary
            clear_history()

        except json.JSONDecodeError:
            # If Gemini doesn't return valid JSON, send the raw text
            reply = "מצטער, לא הצלחתי לעבד את הסיכום. הנה התשובה הגולמית:\n" + json_string
            
        send_whatsapp_message(from_number, phone_number_id, reply)

    elif cmd_lower == "/help":
        reply = (
            "שלום! אני בוט העוזר האישי שלך.\n\n"
            "אני שומר את היסטוריית השיחה באופן אוטומטי.\n"
            "כדי לקבל סיכום ומשימות, כתוב `/summary`.\n"
            "כדי למחוק את ההיסטוריה, כתוב `/clear`."
        )
        send_whatsapp_message(from_number, phone_number_id, reply)

    elif cmd_lower == "/clear":
        clear_history()
        reply = "🧹 היסטוריית השיחה נמחקה. מתחילים דף חדש!"
        send_whatsapp_message(from_number, phone_number_id, reply)

    # Note: No 'else' block. The bot stays silent unless a command is issued.
