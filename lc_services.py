# lc_services.py
# Backend Services Module
# Handles: Airtable, SMTP Email, Telegram, LemonSqueezy

import requests, smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dm_data as dm
import dm_core as dc # [FIX] 增加核心逻辑引用

CONFIG = {
    "EMAIL_APP_PASSWORD": "", "EMAIL_SENDER_ADDRESS": "", 
    "TELEGRAM_BOT_TOKEN": "", "TELEGRAM_CHAT_ID": "", 
    "LEMONSQUEEZY_API_KEY": "", "MASTER_KEY": "LAI-ADMIN-8888", 
    "AIRTABLE_API_KEY": "", "AIRTABLE_BASE_ID": "",
    "AIRTABLE_TABLE_TICKETS": "SupportTickets", "AIRTABLE_TABLE_USERS": "ActiveUsers"
}

def send_telegram_alert(msg):
    if not CONFIG["TELEGRAM_BOT_TOKEN"]: return
    try: requests.post(f"https://api.telegram.org/bot{CONFIG['TELEGRAM_BOT_TOKEN']}/sendMessage", data={"chat_id": CONFIG["TELEGRAM_CHAT_ID"], "text": f"🧬 {msg}"}, timeout=3)
    except: pass

def send_email_smtp(to_email, subject, body):
    if not CONFIG["EMAIL_APP_PASSWORD"] or not CONFIG["EMAIL_SENDER_ADDRESS"]: return False
    try:
        msg = MIMEMultipart()
        msg['From'] = f"Lai's Lab Support <{CONFIG['EMAIL_SENDER_ADDRESS']}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(CONFIG["EMAIL_SENDER_ADDRESS"], CONFIG["EMAIL_APP_PASSWORD"])
        server.sendmail(CONFIG["EMAIL_SENDER_ADDRESS"], to_email, msg.as_string())
        server.quit()
        return True
    except: return False

def log_ticket_to_airtable(email, ticket_type, issue, tier):
    ticket_id = f"#{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
    send_telegram_alert(f"🆘 Ticket {ticket_id}\nUser: {email}\nType: {ticket_type}\nIssue: {issue}")
    
    if CONFIG["AIRTABLE_API_KEY"]:
        url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_TICKETS']}"
        data = {"fields": {"TicketID": ticket_id, "Email": email, "Type": ticket_type, "Issue": issue, "Tier": tier, "Status": "Pending", "CreatedAt": datetime.datetime.now().isoformat()}}
        try: requests.post(url, json={"records": [{"fields": data['fields']}]}, headers={"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"})
        except: pass
    
    # Auto-Reply Logic
    is_auto, auto_ans = False, ""
    # [FIX] 这里改为从 dc (dm_core) 调用 INTERCEPT_LOGIC
    for keywords, idx in dc.INTERCEPT_LOGIC:
        if any(k in issue.lower() for k in keywords):
            is_auto, auto_ans = True, dm.FAQ_DATABASE["English"][idx]["a"]
            break
            
    if is_auto:
        send_email_smtp(email, f"✅ [Resolved] Ticket {ticket_id}", f"Auto-Reply Solution:\n{auto_ans}\n\nReply if you still need help.")
    else:
        wait = "1-2 days" if tier == "Pro" else "3-4 days"
        send_email_smtp(email, f"🎫 [Received] Ticket {ticket_id}", f"We received your request.\nEstimated Wait: {wait}")

def check_user_tier(email, key):
    if key == CONFIG["MASTER_KEY"]: return "Pro", "Master Key Activated"
    if not CONFIG["LEMONSQUEEZY_API_KEY"]: return "Guest", "Server Config Missing"
    
    try:
        url = "https://api.lemonsqueezy.com/v1/licenses/activate"
        resp = requests.post(url, data={"license_key": key, "instance_name": "LaisLab_App"}, timeout=8)
        data = resp.json()
        if data.get("activated"):
            # Log Activation
            if CONFIG["AIRTABLE_API_KEY"]:
                u2 = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_USERS']}"
                d2 = {"fields": {"Email": email, "LicenseKey": key, "ActivationMethod": "LemonSqueezy", "ActivatedAt": datetime.datetime.now().isoformat()}}
                requests.post(u2, json={"records": [{"fields": d2['fields']}]}, headers={"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"})
            send_telegram_alert(f"💎 New PRO User: {email}")
            return "Pro", "Success"
        return "Guest", data.get("error", "Invalid Key")
    except Exception as e:
        return "Guest", str(e)