# scheduler.py
import schedule
import time
# When you add reminders back, you will need to import send_whatsapp_message
# from services import send_whatsapp_message

def run_scheduler():
    # Example: schedule.every().day.at("08:00").do(send_daily_summary)
    # This is where you would put schedule.every(1).minutes.do(check_reminders)
    print("Scheduler thread started.")
    while True:
        schedule.run_pending()
        time.sleep(1)