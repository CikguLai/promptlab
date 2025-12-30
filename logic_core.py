# logic_core.py
# Lai's Lab V9.28 - Professional Audit Edition (Full Features)

import requests
import datetime
import smtplib
import io
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF
import data_matrix as dm

# ==========================================
# 1. 全局配置核心
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
# 2. 黑科技：Telegram 实时报警系统
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

# ==========================================
# 3. 鉴权与激活逻辑
# ==========================================
def check_user_tier(email, key):
    # 管理员后门
    if key == CONFIG["MASTER_KEY"]:
        log_activation(email, key, "Master-Admin")
        return "Pro"
    
    # LemonSqueezy 真实 API 校验
    try:
        url = "https://api.lemonsqueezy.com/v1/licenses/activate"
        response = requests.post(url, data={
            "license_key": key, 
            "instance_name": "LaisLab_User_App"
        }, timeout=10)
        if response.status_code == 200 and response.json().get("activated"):
            log_activation(email, key, "LemonSqueezy")
            return "Pro"
    except Exception: pass
    return "Guest"

def log_activation(email, key, method):
    if not CONFIG["AIRTABLE_API_KEY"]: return
    url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_USERS']}"
    # 强制 ISO 时间格式解决 Airtable 报错
    now = datetime.datetime.now().isoformat()
    data = {
        "fields": {
            "Email": email, 
            "LicenseKey": key, 
            "ActivationMethod": method, 
            "ActivatedAt": now
        }
    }
    try: 
        requests.post(url, json={"records": [{"fields": data['fields']}]}, 
                      headers={"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"})
        send_telegram_alert(f"💎 New Activation: {email} via {method}")
    except Exception: pass

# ==========================================
# 4. PASEC 核心引擎 (含去 AI 符号黑科技)
# ==========================================
def generate_pasec_prompt(role, mode, option, user_input, tier, lang, tone):
    # 从矩阵索引模板
    templates = dm.ROLES_CONFIG.get(role, {}).get(mode, [])
    template_str = next((t['template'] for t in templates if t['label'] == option), "{input}")
    
    # 基础 Payload 构建
    res = f"### [PASEC PROTOCOL V2.8]\n"
    res += f"**ROLE**: {role}\n**TONE**: {tone}\n**LANG**: {lang}\n"
    res += f"**INSTRUCTION**: {template_str.format(input=user_input)}\n"
    
    # ✅ 黑科技：Pro 用户去 AI 痕迹处理 (移除 # 和 **)
    if tier == "Pro":
        res += "\n[SYSTEM RULE]: Provide a CLEAN output WITHOUT markdown symbols like '##' or '**'. "
        res += "The output must look like a natural human-written text. Avoid 'AI-style' transitions like 'In conclusion'."
    else:
        # 免费版保留符号并强制加水印
        res += "\n\n(Generated via Lai's Lab Free Trial - Upgrade for Clean & Unlimited output)"
    
    return res

# ✅ 黑科技：WhatsApp 分享链接生成 (含带水印/不带水印自动判断)
def get_whatsapp_link(text):
    encoded_text = urllib.parse.quote(text)
    return f"https://wa.me/?text={encoded_text}"

# ✅ 黑科技：专业 PDF 导出
def create_pdf(text, role, mode):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Lai's Lab Analysis - {role} / {mode}", ln=True, align='C')
        pdf.ln(10)
        # 编码处理防止特殊字符崩溃
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_text)
        return pdf.output(dest='S').encode('latin-1')
    except Exception: return None

# ==========================================
# 5. 工单系统与智能拦截
# ==========================================
def smart_intercept(text):
    # 扫描主题词自动从 FAQ 调取答案
    for k, v in dm.INTERCEPTORS.items():
        if k.lower() in text.lower(): return True, v
    return False, ""

def log_ticket_to_airtable(tid, email, tier, type, subject, msg):
    if not CONFIG["AIRTABLE_API_KEY"]: return
    url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{CONFIG['AIRTABLE_TABLE_TICKETS']}"
    fields = {
        "TicketID": str(tid), 
        "Email": email, 
        "Tier": tier, 
        "Issue": f"[{type}] {subject}: {msg}", 
        "Status": "Open"
    }
    try: 
        requests.post(url, json={"records": [{"fields": fields}]}, 
                      headers={"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"})
        send_telegram_alert(f"📩 New Ticket #{tid} from {email}\nSubject: {subject}")
    except Exception: pass

def send_auto_reply_email(user_email, user_tier, ticket_id, subject):
    if not CONFIG["EMAIL_APP_PASSWORD"]: return
    try:
        msg = MIMEMultipart()
        msg['From'] = CONFIG["EMAIL_SENDER_ADDRESS"]
        msg['To'] = user_email
        msg['Subject'] = f"[{'VIP' if user_tier=='Pro' else 'Ticket'}] Case #{ticket_id} Received"
        if CONFIG["EMAIL_REPLY_TO"]: msg.add_header('Reply-To', CONFIG["EMAIL_REPLY_TO"])
        
        body = f"Hello,\n\nWe have received your request: {subject}.\n\nLai's Lab Support Team"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(CONFIG["EMAIL_SENDER_ADDRESS"], CONFIG["EMAIL_APP_PASSWORD"])
        server.sendmail(CONFIG["EMAIL_SENDER_ADDRESS"], user_email, msg.as_string())
        server.quit()
    except Exception: pass

# ==========================================
# 6. 额度控制
# ==========================================
def check_daily_limit_by_email(email, tier, current_usage):
    # Pro 用户宣称为 Unlimited，但后台设置 1000 作为 Fair Use 防御
    limit = 1000 if tier == "Pro" else 5
    return (current_usage < limit), limit - current_usage, limit

def check_mode_lock(tier, mode_name):
    if tier == "Pro": return False
    # 强制锁定带有 Pro 标识或关键付费模块的模式
    pro_keywords = ["(Pro)", "Visuals", "Marketing", "Strategy", "Premium", "Admin", "Pro"]
    return any(k in mode_name for k in pro_keywords)
