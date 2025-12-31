# logic_core.py
# Lai's Lab V9.28 - 2026 READY
# Backend Logic: Integrations, PDF, CSV, Security, PASEC Engine

import requests
import datetime
import smtplib
import io
import urllib.parse
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF
import data_matrix as dm

# ==========================================
# 1. 全局配置
# ==========================================
CONFIG = {
    "EMAIL_APP_PASSWORD": "", 
    "EMAIL_SENDER_ADDRESS": "", 
    "EMAIL_ADMIN_ADDRESS": "", 
    "EMAIL_REPLY_TO": "support@cikgulai.com",
    "TELEGRAM_BOT_TOKEN": "", 
    "TELEGRAM_CHAT_ID": "",
    "LEMONSQUEEZY_API_KEY": "", 
    "MASTER_KEY": "LAI-ADMIN-8888",
    "AIRTABLE_API_KEY": "", 
    "AIRTABLE_BASE_ID": "",
    "AIRTABLE_TABLE_TICKETS": "SupportTickets",
    "AIRTABLE_TABLE_USERS": "ActiveUsers"
}

# ==========================================
# 2. 黑科技：Telegram & Airtable & SMTP
# ==========================================
def send_telegram_alert(msg):
    if not CONFIG["TELEGRAM_BOT_TOKEN"]: return
    url = f"https://api.telegram.org/bot{CONFIG['TELEGRAM_BOT_TOKEN']}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": CONFIG["TELEGRAM_CHAT_ID"], 
            "text": f"🧬 [Lai's Lab Alert]\n{msg}"
        }, timeout=5)
    except Exception: pass

def log_activation(email, key, method):
    if not CONFIG["AIRTABLE_API_KEY"]: return
    url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_USERS']}"
    now = datetime.datetime.now().isoformat()
    data = {"fields": {"Email": email, "LicenseKey": key, "ActivationMethod": method, "ActivatedAt": now}}
    try: 
        requests.post(url, json={"records": [{"fields": data['fields']}]}, 
                      headers={"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"})
        send_telegram_alert(f"💎 New Activation: {email} via {method}")
    except Exception: pass

def send_email_smtp(to_email, subject, body):
    if not CONFIG["EMAIL_APP_PASSWORD"] or not CONFIG["EMAIL_SENDER_ADDRESS"]: return False
    try:
        msg = MIMEMultipart()
        msg['From'] = CONFIG["EMAIL_SENDER_ADDRESS"]
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.add_header('Reply-To', CONFIG["EMAIL_REPLY_TO"])
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(CONFIG["EMAIL_SENDER_ADDRESS"], CONFIG["EMAIL_APP_PASSWORD"])
        server.sendmail(CONFIG["EMAIL_SENDER_ADDRESS"], to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

def log_ticket_to_airtable(email, ticket_type, issue, tier):
    send_telegram_alert(f"🆘 New Ticket: {ticket_type}\nUser: {email} ({tier})\nIssue: {issue}")
    if CONFIG["AIRTABLE_API_KEY"]:
        url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_TICKETS']}"
        now = datetime.datetime.now().isoformat()
        data = {"fields": {"Email": email, "Type": ticket_type, "Issue": issue, "Tier": tier, "Status": "Pending", "CreatedAt": now}}
        try:
            requests.post(url, json={"records": [{"fields": data['fields']}]}, 
                          headers={"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"})
        except Exception: pass
    
    if tier == "Pro":
        subject = f"💎 [VIP] Ticket Received: {ticket_type}"
        body = f"Dear Pro Member,\n\nWe received your {ticket_type}.\nIssue: {issue}\n\n💎 Status: VIP Queue (1-2 Days).\n\nBest,\nCikgu Lai"
    else:
        subject = f"[Ticket] Received: {ticket_type}"
        body = f"Dear User,\n\nWe received your {ticket_type}.\nIssue: {issue}\n\nStatus: Standard Queue (3-5 Days).\n\nBest,\nLai's Lab Support"
    send_email_smtp(email, subject, body)

# ==========================================
# 3. 鉴权逻辑
# ==========================================
def check_user_tier(email, key):
    if key == CONFIG["MASTER_KEY"]:
        log_activation(email, key, "Master-Admin")
        return "Pro"
    try:
        url = "https://api.lemonsqueezy.com/v1/licenses/activate"
        response = requests.post(url, data={"license_key": key, "instance_name": "LaisLab_User_App"}, timeout=10)
        if response.status_code == 200 and response.json().get("activated"):
            log_activation(email, key, "LemonSqueezy")
            return "Pro"
    except Exception: pass
    return "Guest"

# ==========================================
# 4. PASEC 核心引擎
# ==========================================
def generate_pasec_prompt(role, mode, option, user_input, tier, lang, tone):
    templates = dm.ROLES_CONFIG.get(role, {}).get(mode, [])
    template_str = next((t['template'] for t in templates if t['label'] == option), "{input}")
    
    res = f"### [PASEC PROTOCOL V2.8]\n"
    res += f"**ROLE**: {role}\n**TONE**: {tone}\n**OUTPUT LANGUAGE**: {lang}\n"
    res += f"**INSTRUCTION**: {template_str.format(input=user_input)}\n"
    
    if tier == "Pro":
        res += "\n[SYSTEM RULE]: Provide a CLEAN output WITHOUT markdown symbols like '##'. Human-like tone."
    else:
        res += "\n\n(Generated via Lai's Lab Free Trial - Upgrade for Clean Output)"
    return res

# 🔥 新增：生成 CSV (带 BOM 头防止乱码)
def create_csv(text):
    return ("\ufeff" + text).encode("utf-8")

# 🔥 新增：生成社交分享链接
def get_social_links(text):
    encoded = urllib.parse.quote(text)
    return {
        "WhatsApp": f"https://wa.me/?text={encoded}",
        "Telegram": f"https://t.me/share/url?url=https://laislab.com&text={encoded}",
        "Email": f"mailto:?subject=Generated%20Content&body={encoded}",
        "X": f"https://twitter.com/intent/tweet?text={encoded}"
    }

def create_pdf(text, role, mode):
    try:
        pdf = FPDF()
        pdf.add_page()
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
            pdf.cell(0, 10, txt="[Font Error: CJK characters may fail - Upload font.ttf]", ln=True)
        
        pdf.cell(200, 10, txt=f"Lai's Lab Report - {role}", ln=True, align='C')
        pdf.ln(10)
        
        if font_loaded:
            pdf.multi_cell(0, 10, txt=text)
        else:
            pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))
        return pdf.output(dest='S').encode('latin-1')
    except: return None

# ==========================================
# 5. 客服拦截与权限
# ==========================================
def smart_intercept(text):
    for k, v in dm.INTERCEPTORS.items():
        if k.lower() in text.lower(): return True, v
    return False, ""

def check_daily_limit_by_email(email, tier, current_usage):
    limit = 1000 if tier == "Pro" else 5
    return (current_usage < limit), limit - current_usage, limit

def check_mode_lock(tier, mode_name):
    if tier == "Pro": return False
    return "(Pro)" in mode_name
