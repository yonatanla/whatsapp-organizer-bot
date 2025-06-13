# bot_logic.py
from services import summarize_with_gemini  # Import the Gemini function

# We will store tasks in memory here.
# For a real app, this should be a database.
tasks = []

def process_command(command):
    """Processes the user's command and returns a reply."""
    cmd_lower = command.lower()

    if cmd_lower.startswith("הוסף משימה ") or cmd_lower.startswith("add task "):
        task_description = command.split(" ", 2)[2]
        tasks.append(task_description)
        return f"✅ משימה נוספה: '{task_description}'"

    elif cmd_lower == "רשימת משימות" or cmd_lower == "list tasks":
        if not tasks:
            return "אין לך משימות! 🎉"
        task_list = "\n".join(f"- {task}" for task in tasks)
        return f"📝 *המשימות שלך:*\n{task_list}"

    elif cmd_lower == "סכם יום" or cmd_lower == "summarize day":
        if not tasks:
            return "אין משימות לסכם."
        tasks_as_string = "\n".join(tasks)
        summary = summarize_with_gemini(tasks_as_string) # Call the imported function
        return f"🤖 *סיכום יומי (באדיבות Gemini):*\n{summary}"

    elif cmd_lower == "עזרה" or cmd_lower == "help":
        return (
            "שלום! אני בוט הארגון האישי שלך. הנה הפקודות:\n\n"
            "*`הוסף משימה [תיאור]`* - מוסיף משימה חדשה.\n"
            "*`רשימת משימות`* - מציג את כל המשימות.\n"
            "*`סכם יום`* - יוצר סיכום של כל המשימות."
        )

    else:
        # If the command isn't recognized, we don't reply.
        # This prevents the bot from saying "I don't understand" to every message in a group chat.
        return None
