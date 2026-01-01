# logic_core.py (V9.32 - FINAL GOLD)
# Features: Real Ticket ID, Smart Email, Prompt Language Injection, Real Activation

import requests, datetime, smtplib, io, urllib.parse, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF
import data_matrix as dm

CONFIG = {
    "EMAIL_APP_PASSWORD": "", "EMAIL_SENDER_ADDRESS": "", "EMAIL_ADMIN_ADDRESS": "",
    "TELEGRAM_BOT_TOKEN": "", "TELEGRAM_CHAT_ID": "", "LEMONSQUEEZY_API_KEY": "", 
    "MASTER_KEY": "LAI-ADMIN-8888", "AIRTABLE_API_KEY": "", "AIRTABLE_BASE_ID": "",
    "AIRTABLE_TABLE_TICKETS": "SupportTickets", "AIRTABLE_TABLE_USERS": "ActiveUsers"
}

def send_telegram_alert(msg):
    if not CONFIG["TELEGRAM_BOT_TOKEN"]: return
    try: requests.post(f"https://api.telegram.org/bot{CONFIG['TELEGRAM_BOT_TOKEN']}/sendMessage", data={"chat_id": CONFIG["TELEGRAM_CHAT_ID"], "text": f"🧬 {msg}"}, timeout=5)
    except: pass

def log_activation(email, key, method):
    if not CONFIG["AIRTABLE_API_KEY"]: return
    url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_USERS']}"
    now = datetime.datetime.now().isoformat()
    data = {"fields": {"Email": email, "LicenseKey": key, "ActivationMethod": method, "ActivatedAt": now}}
    try: 
        requests.post(url, json={"records": [{"fields": data['fields']}]}, headers={"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"})
        send_telegram_alert(f"💎 New Activation: {email} via {method}")
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
    except: return False

# 🔥 核心：真实工单逻辑 (ID + 智能回复)
def log_ticket_to_airtable(email, ticket_type, issue, tier):
    ticket_id = f"#{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
    send_telegram_alert(f"🆘 Ticket {ticket_id}: {ticket_type}\nUser: {email}\nIssue: {issue}")
    
    if CONFIG["AIRTABLE_API_KEY"]:
        url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_TICKETS']}"
        now = datetime.datetime.now().isoformat()
        data = {"fields": {"TicketID": ticket_id, "Email": email, "Type": ticket_type, "Issue": issue, "Tier": tier, "Status": "Pending", "CreatedAt": now}}
        try: requests.post(url, json={"records": [{"fields": data['fields']}]}, headers={"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"})
        except: pass
    
    # Smart Intercept for Email
    is_auto_solvable = False
    issue_lower = issue.lower()
    auto_reply_msg = ""
    for keywords, idx in dm.INTERCEPT_LOGIC:
        if any(k in issue_lower for k in keywords):
            is_auto_solvable = True
            auto_reply_msg = dm.FAQ_DATABASE["English"][idx]["a"]
            break
            
    if is_auto_solvable:
        subject = f"✅ [Case Closed] Ticket {ticket_id}: Solution found"
        body = f"Dear User,\n\nWe received your ticket '{ticket_type}'.\n\n💡 Official Solution:\n{auto_reply_msg}\n\nThis ticket is marked as auto-resolved. If this didn't help, please REPLY to this email.\n\nBest,\nLai's Lab Support"
    else:
        subject = f"🎫 [Ticket Received] Ticket {ticket_id}: We are reviewing"
        wait_time = "1-2 business days" if tier == "Pro" else "3-4 business days"
        priority = "💎 VIP Priority" if tier == "Pro" else "Standard Queue"
        body = f"Dear User,\n\nWe successfully received your ticket.\nTicket ID: {ticket_id}\nIssue: {issue}\n\n⏳ Status: {priority}\nEstimated Reply: {wait_time}.\n\nBest,\nLai's Lab Support"
        
    send_email_smtp(email, subject, body)

# 🔥 核心：真实激活验证
def check_user_tier(email, key):
    if key == CONFIG["MASTER_KEY"]: return "Pro", "Master Key"
    if not CONFIG["LEMONSQUEEZY_API_KEY"]: return "Guest", "No API Key"
    
    url = "https://api.lemonsqueezy.com/v1/licenses/activate"
    payload = {"license_key": key, "instance_name": "LaisLab_App"}
    try:
        response = requests.post(url, data=payload, timeout=8)
        data = response.json()
        if response.status_code == 200 and data.get("activated"):
            log_activation(email, key, "LemonSqueezy")
            return "Pro", "Success"
        elif data.get("error"):
            return "Guest", f"Activation Failed: {data.get('error')}"
    except Exception as e:
        return "Guest", f"Connection Error: {str(e)}"
    return "Guest", "Invalid Key"

# 🔥 核心：Prompt 强指令生成
def generate_pasec_prompt(role, mode, option, user_input, tier, lang, tone):
    templates = dm.ROLES_CONFIG.get(role, {}).get(mode, [])
    template_str = next((t['template'] for t in templates if t['label'] == option), "{input}")
    
    res = f"### [PASEC PROTOCOL V2.8]\n**ROLE**: {role}\n**TONE**: {tone}\n**TARGET LANGUAGE**: {lang}\n"
    res += f"**INSTRUCTION**: {template_str.format(input=user_input)}\n"
    res += f"\n[SYSTEM]: You MUST write the final output content in **{lang}**. Do not use English unless the user asked for it."
    
    if tier == "Pro": res += "\n[MODE]: Clean Output. Human-like tone. No markdown headers."
    else: res += "\n\n(Generated via Lai's Lab Free Version)"
    return res

def create_csv(text): return ("\ufeff" + text).encode("utf-8")

def get_social_links(text):
    e = urllib.parse.quote(text)
    return {
        "WhatsApp": f"https://wa.me/?text={e}",
        "Telegram": f"https://t.me/share/url?url=laislab&text={e}",
        "Email": f"mailto:?body={e}",
        "X": f"https://twitter.com/intent/tweet?text={e}"
    }

def get_whatsapp_link(text): return f"https://wa.me/?text={urllib.parse.quote(text)}"

def create_pdf(text, role, mode):
    try:
        pdf = FPDF(); pdf.add_page(); 
        font_path = "font.ttf"
        font_loaded = False
        if os.path.exists(font_path):
            try:
                pdf.add_font('CustomFont', '', font_path, uni=True)
                pdf.set_font("CustomFont", size=12)
                font_loaded = True
            except: pass
        if not font_loaded:
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt="[Font Error: Upload font.ttf]", ln=True)
        pdf.cell(200, 10, txt=f"Report: {role}", ln=True, align='C')
        pdf.multi_cell(0, 10, txt=text)
        return pdf.output(dest='S').encode('latin-1')
    except: return None

def smart_intercept(text, lang="English"):
    text_lower = text.lower()
    for keywords, faq_index in dm.INTERCEPT_LOGIC:
        if any(k in text_lower for k in keywords):
            return True, "Check FAQ for solution."
    return False, ""

def check_daily_limit_by_email(email, tier, current_usage):
    limit = 1000 if tier == "Pro" else 5
    return (current_usage < limit), limit - current_usage, limit

def check_mode_lock(tier, mode_name): return False if tier == "Pro" else "(Pro)" in mode_name
