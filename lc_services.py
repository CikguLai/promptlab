# lc_services.py
# Backend Services: Airtable (Leads/Tickets), SMTP, LemonSqueezy

import requests, smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# [配置] 请在 .streamlit/secrets.toml 填入真实 Key
CONFIG = {
    "EMAIL_APP_PASSWORD": "", "EMAIL_SENDER_ADDRESS": "", 
    "TELEGRAM_BOT_TOKEN": "", "TELEGRAM_CHAT_ID": "", 
    "LEMONSQUEEZY_API_KEY": "", "MASTER_KEY": "LAI-ADMIN-8888", 
    "AIRTABLE_API_KEY": "", "AIRTABLE_BASE_ID": "",
    "AIRTABLE_TABLE_TICKETS": "SupportTickets", 
    "AIRTABLE_TABLE_LEADS": "FreeLeads",  # 新增：免费用户表
    "AIRTABLE_TABLE_USERS": "ActiveUsers" # Pro用户表
}

def send_telegram_alert(msg):
    if not CONFIG["TELEGRAM_BOT_TOKEN"]: return
    try: requests.post(f"https://api.telegram.org/bot{CONFIG['TELEGRAM_BOT_TOKEN']}/sendMessage", data={"chat_id": CONFIG["TELEGRAM_CHAT_ID"], "text": f"🧬 {msg}"}, timeout=3)
    except: pass

def send_email_smtp(to_email, subject, body):
    if not CONFIG["EMAIL_APP_PASSWORD"] or not CONFIG["EMAIL_SENDER_ADDRESS"]: return False
    try:
        msg = MIMEMultipart()
        msg['From'] = CONFIG["EMAIL_SENDER_ADDRESS"]
        msg['To'] = to_email
        msg['Subject'] = subject
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

# [新增] 收集免费用户 Leads
def log_lead_to_airtable(email):
    if not CONFIG["AIRTABLE_API_KEY"]: return
    try:
        url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_LEADS']}"
        headers = {"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"}
        # 记录邮箱、来源、时间
        data = {"fields": {"Email": email, "Source": "Guest_Login", "CapturedAt": datetime.datetime.now().isoformat()}}
        requests.post(url, json={"records": [data]}, headers=headers, timeout=2)
    except: pass

# [升级] 记录工单 (接受前端生成的 ticket_id)
def log_ticket_to_airtable(email, issue_type, msg, tier, ticket_id):
    # 1. Telegram 通知
    send_telegram_alert(f"Ticket {ticket_id} [{tier}]: {msg} ({email})")
    
    # 2. Airtable 存储
    if CONFIG["AIRTABLE_API_KEY"]:
        try:
            url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_TICKETS']}"
            headers = {"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"}
            data = {"fields": {"TicketID": ticket_id, "Email": email, "Type": issue_type, "Message": msg, "Tier": tier, "Status": "Open", "CreatedAt": datetime.datetime.now().isoformat()}}
            requests.post(url, json={"records": [data]}, headers=headers, timeout=3)
        except: pass
        
    # 3. 自动回复邮件 (确保 ID 一致)
    send_email_smtp(email, f"🎫 [Received] Ticket {ticket_id}", f"Ticket ID: {ticket_id}\n\nWe received your request: '{msg}'.\nOur support team will check it shortly.")

def check_user_tier(email, key):
    if key == CONFIG["MASTER_KEY"]: return "Pro", "Master Key Activated"
    if not CONFIG["LEMONSQUEEZY_API_KEY"]: return "Guest", "Server Config Missing"
    try:
        url = "https://api.lemonsqueezy.com/v1/licenses/activate"
        resp = requests.post(url, data={"license_key": key, "instance_name": "LaisLab_App"}, timeout=8)
        data = resp.json()
        if data.get("activated"):
            # 记录 Pro 用户
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
