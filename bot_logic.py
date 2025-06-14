# bot_logic.py
from services import get_summary_and_actions_with_gemini
from collections import deque

# We will now store the last 20 messages of the conversation.
# `deque` is a special list that automatically removes old items.
conversation_history = deque(maxlen=20)

def process_command(message_text):
    """
    Processes user commands and conversation text.
    Now, it only responds to specific commands.
    """
    # Always add the latest message to our history
    conversation_history.append(message_text)
    
    # Make the command check case-insensitive
    cmd_lower = message_text.lower()

    # --- Command Handling ---

    if cmd_lower == "/summary":
        # When this command is received, analyze the stored history
        print(f"Analyzing history: {list(conversation_history)}")
        analysis = get_summary_and_actions_with_gemini(list(conversation_history))
        # Clear the history after summarizing so we start fresh
        conversation_history.clear()
        return f"🤖 *ניתוח שיחה:*\n{analysis}"

    elif cmd_lower == "/help":
        return (
            "שלום! אני בוט העוזר האישי שלך.\n\n"
            "כדי שאנתח את השיחה שלנו, פשוט שוחח איתי כרגיל.\n"
            "בכל עת, כתוב `/summary` ואני אסכם את 20 ההודעות האחרונות ואוציא עבורך משימות."
        )

    # By default, the bot will no longer reply to every single message.
    # It will only reply to the specific commands above.
    return None

