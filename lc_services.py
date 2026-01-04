# lc_services.py
# Backend Services: Airtable, SMTP, LemonSqueezy

import requests, smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

CONFIG = {
    "EMAIL_APP_PASSWORD": "", "EMAIL_SENDER_ADDRESS": "", 
    "TELEGRAM_BOT_TOKEN": "", "TELEGRAM_CHAT_ID": "", 
    "LEMONSQUEEZY_API_KEY": "", "MASTER_KEY": "LAI-ADMIN-8888", 
    "AIRTABLE_API_KEY": "", "AIRTABLE_BASE_ID": "",
    "AIRTABLE_TABLE_TICKETS": "SupportTickets", 
    "AIRTABLE_TABLE_LEADS": "FreeLeads",
    "AIRTABLE_TABLE_USERS": "ActiveUsers"
}

def send_telegram_alert(msg):
    if not CONFIG["TELEGRAM_BOT_TOKEN"]: return
    try: requests.post(f"https://api.telegram.org/bot{CONFIG['TELEGRAM_BOT_TOKEN']}/sendMessage", data={"chat_id": CONFIG["TELEGRAM_CHAT_ID"], "text": f"🧬 {msg}"}, timeout=3)
    except: pass

def send_email_smtp(to_email, subject, body):
    if not CONFIG["EMAIL_APP_PASSWORD"] or not CONFIG["EMAIL_SENDER_ADDRESS"]: return False
    try:
        msg = MIMEMultipart()
        # [FIX] Sender Name
        msg['From'] = formataddr(("Lai's Lab Team", CONFIG["EMAIL_SENDER_ADDRESS"]))
        msg['To'] = to_email
        msg['Subject'] = subject
        # [FIX] Reply-To
        msg.add_header('Reply-To', 'laislabteam@gmail.com')
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(CONFIG["EMAIL_SENDER_ADDRESS"], CONFIG["EMAIL_APP_PASSWORD"])
        server.sendmail(CONFIG["EMAIL_SENDER_ADDRESS"], to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

def log_lead_to_airtable(email):
    if not CONFIG["AIRTABLE_API_KEY"]: return
    try:
        url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_LEADS']}"
        headers = {"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"}
        data = {"fields": {"Email": email, "Source": "Guest_Login", "CapturedAt": datetime.datetime.now().isoformat()}}
        requests.post(url, json={"records": [data]}, headers=headers, timeout=2)
    except: pass

def log_ticket_to_airtable(email, issue_type, msg, tier, ticket_id):
    send_telegram_alert(f"Ticket {ticket_id} [{tier}]: {msg} ({email})")
    
    if CONFIG["AIRTABLE_API_KEY"]:
        try:
            url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_TICKETS']}"
            headers = {"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"}
            data = {"fields": {"TicketID": ticket_id, "Email": email, "Type": issue_type, "Message": msg, "Tier": tier, "Status": "Open", "CreatedAt": datetime.datetime.now().isoformat()}}
            requests.post(url, json={"records": [data]}, headers=headers, timeout=3)
        except: pass
        
    # [FIX] Final SLA Text
    sla_text = """
Dear User,

Thank you for contacting Lai's Lab AI Support. We have received your request.

All tickets are processed in a queue to ensure quality support.
Due to time zone differences, please allow:

💎 Pro Users: 1-3 Business Days (Priority Queue)
👤 Free Users: 3-5 Business Days (Standard Queue)

Your Ticket ID is: {tid}

Best regards,
The Lai's Lab Team
    """.format(tid=ticket_id)
    
    send_email_smtp(email, f"[Ticket Received] We are looking into your issue #{ticket_id}", sla_text)

def check_user_tier(email, key):
    if key == CONFIG["MASTER_KEY"]: return "Pro", "Master Key Activated"
    if not CONFIG["LEMONSQUEEZY_API_KEY"]: return "Guest", "Server Config Missing"
    try:
        url = "https://api.lemonsqueezy.com/v1/licenses/activate"
        resp = requests.post(url, data={"license_key": key, "instance_name": "LaisLab_App"}, timeout=8)
        data = resp.json()
        if data.get("activated"):
            if CONFIG["AIRTABLE_API_KEY"]:
                u2 = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_USERS']}"
                headers = {"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"}
                d2 = {"fields": {"Email": email, "LicenseKey": key, "ActivatedAt": datetime.datetime.now().isoformat()}}
                requests.post(u2, json={"records": [d2]}, headers=headers)
            return "Pro", "Success"
        else:
            return "Guest", data.get("error", {}).get("detail", "Invalid Key")
    except:
        return "Guest", "Connection Error"
