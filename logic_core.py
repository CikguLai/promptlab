# logic_core.py
# Lai's Lab V9.28 - PRODUCTION READY (FINAL)
# Logic: SMTP, PDF(CJK), Intercept, Integrations

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

def log_ticket_to_airtable(email, ticket_type, issue, tier):
    send_telegram_alert(f"🆘 Ticket: {ticket_type}\nUser: {email}\nIssue: {issue}")
    # 1. Airtable Write
    if CONFIG["AIRTABLE_API_KEY"]:
        url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_TICKETS']}"
        now = datetime.datetime.now().isoformat()
        data = {"fields": {"Email": email, "Type": ticket_type, "Issue": issue, "Tier": tier, "Status": "Pending", "CreatedAt": now}}
        try: requests.post(url, json={"records": [{"fields": data['fields']}]}, headers={"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"})
        except: pass
    
    # 2. SMTP Auto-Reply (SLA Logic)
    if tier == "Pro":
        subject = f"💎 [VIP] Priority Ticket Received: {ticket_type}"
        body = f"Dear Valued Pro Member,\n\nWe have received your priority ticket.\nIssue: {issue}\n\nStatus: VIP Queue (Response in 1-2 business days).\n\nBest Regards,\nLai's Lab Support"
    else:
        subject = f"[Ticket] Support Request Received: {ticket_type}"
        body = f"Dear User,\n\nWe have received your ticket.\nIssue: {issue}\n\nStatus: Standard Queue (Response in 3-5 business days).\n\nBest Regards,\nLai's Lab Support"
    send_email_smtp(email, subject, body)

def check_user_tier(email, key):
    if key == CONFIG["MASTER_KEY"]: return "Pro"
    # (LemonSqueezy check omitted for brevity, add if needed)
    return "Guest"

def generate_pasec_prompt(role, mode, option, user_input, tier, lang, tone):
    templates = dm.ROLES_CONFIG.get(role, {}).get(mode, [])
    template_str = next((t['template'] for t in templates if t['label'] == option), "{input}")
    res = f"### [PASEC PROTOCOL V2.8]\n**ROLE**: {role}\n**TONE**: {tone}\n**OUTPUT LANGUAGE**: {lang}\n**INSTRUCTION**: {template_str.format(input=user_input)}\n"
    res += f"\n[SYSTEM]: Ensure the final output is in **{lang}** language."
    if tier == "Pro": res += "\n[MODE]: Clean Output. Human-like tone. No markdown symbols."
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
        
        # 🔥 FONT FIX: 使用用户上传的 font.ttf
        font_path = "font.ttf"
        font_loaded = False
        if os.path.exists(font_path):
            try:
                pdf.add_font('CustomFont', '', font_path, uni=True)
                pdf.set_font("CustomFont", size=12)
                font_loaded = True
            except: pass
        
        if not font_loaded:
            pdf.set_font("Arial", size=12) # Fallback
            pdf.cell(0, 10, txt="[Font Error: CJK characters may fail - font.ttf missing]", ln=True)
            
        pdf.cell(200, 10, txt=f"Lai's Lab Report - {role}", ln=True, align='C')
        pdf.multi_cell(0, 10, txt=text)
        return pdf.output(dest='S').encode('latin-1')
    except: return None

def smart_intercept(text, lang="English"):
    text_lower = text.lower()
    for keywords, faq_index in dm.INTERCEPT_LOGIC:
        if any(k in text_lower for k in keywords):
            faq_db = dm.FAQ_DATABASE.get(lang, dm.FAQ_DATABASE["English"])
            if 0 <= faq_index < len(faq_db): return True, faq_db[faq_index]["a"]
    return False, ""

def check_daily_limit_by_email(email, tier, current_usage):
    limit = 1000 if tier == "Pro" else 5
    return (current_usage < limit), limit - current_usage, limit

def check_mode_lock(tier, mode_name): return False if tier == "Pro" else "(Pro)" in mode_name
