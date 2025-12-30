# logic_core.py
# Lai's Lab V9.20 - 业务逻辑核心 (1000 Limit Edition)

import requests
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import data_matrix as dm

# 全局配置
CONFIG = {
    "EMAIL_APP_PASSWORD": "", "EMAIL_SENDER_ADDRESS": "", "EMAIL_ADMIN_ADDRESS": "",
    "TELEGRAM_BOT_TOKEN": "", "TELEGRAM_CHAT_ID": "",
    "LEMONSQUEEZY_API_KEY": "", "MASTER_KEY": "LAI-ADMIN-8888",
    "AIRTABLE_API_KEY": "", "AIRTABLE_BASE_ID": "",
    "AIRTABLE_TABLE_TICKETS": "SupportTickets",
    "AIRTABLE_TABLE_USERS": "ActiveUsers"
}

# ==========================================
# 1. 真实鉴权 (LemonSqueezy API)
# ==========================================
def check_user_tier(email, key):
    # 🕵️‍♂️ 1. 管理员后门 (Master Key)
    if key == CONFIG["MASTER_KEY"]:
        log_activation(email, "Master-Key", "Admin-Backdoor")
        return "Pro"

    # 🌍 2. LemonSqueezy 真实联网验证
    try:
        response = requests.post(
            "https://api.lemonsqueezy.com/v1/licenses/activate",
            data={"license_key": key, "instance_name": "LaisLab_Web_App"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("activated") is True:
                log_activation(email, key, "LemonSqueezy-API")
                return "Pro"
            else:
                return "Guest"
        else:
            return "Guest"
    except Exception:
        return "Guest"

# ==========================================
# 2. 真实产品引擎 (PASEC Prompt Generator)
# ==========================================
def generate_pasec_prompt(role, mode, option, user_input, tier, lang, tone="Professional"):
    """
    生成真实的 PASEC 结构化提示词。
    """
    
    # 1. 获取模板
    template_structure = "Create content based on: {input}"
    if role in dm.ROLES_CONFIG and mode in dm.ROLES_CONFIG[role]:
        for opt in dm.ROLES_CONFIG[role][mode]:
            if opt["label"] == option:
                template_structure = opt["template"]
                break
    
    # 2. 清洗语气
    tone_clean = tone.split("(")[0].strip()
    
    # 3. 组装 Prompt
    pasec_output = f"""
# 🧬 Lai's Lab Optimized Prompt (PASEC Protocol)

## 👤 P - Persona (身份设定)
> **Role**: You are an expert **{role}** specializing in **{mode}**.
> **Tone**: Adopt a **{tone_clean}** voice and style throughout the response.
> **Language**: Please output the final result in **{lang}**.

## 🎯 A - Aim (任务目标)
> **Objective**: Execute the task: **{option}**.
> **Context**: The user has provided the following details: 
> *"{user_input}"*
> **Goal**: Your goal is to solve this specific challenge effectively and professionally.

## 📂 S - Structure (执行框架)
Please follow this structure in your response:
1.  **Hook/Insight**: Start with a compelling opening or key insight.
2.  **Core Delivery**: Execute the main task ({option}) based on the context.
3.  **Refinement**: Ensure the content strictly follows the **{tone_clean}** style.
4.  **Actionable Closing**: Provide next steps or a strong conclusion.

## 📝 E - Execution (指令执行)
**[Instruction to AI]**: 
Based on the template: "{template_structure.format(input=user_input)}", please generate the high-quality content now.

## 💡 C - Context Constraints
* Do not mention you are an AI.
* Ensure cultural relevance to **{lang}**.
* Focus on value and clarity.
"""
    
    # Guest 水印
    if tier == "Guest":
        pasec_output += "\n\n(🔒 Trial Version - Upgrade to Pro to remove this watermark and unlock 15 languages)"
        
    return pasec_output

# ==========================================
# 3. 真实数据写入 (Airtable)
# ==========================================
def send_to_airtable(table_name, fields):
    if not CONFIG["AIRTABLE_API_KEY"] or not CONFIG["AIRTABLE_BASE_ID"]:
        return
    url = f"https://api.airtable.com/v0/{CONFIG['AIRTABLE_BASE_ID']}/{table_name}"
    headers = {"Authorization": f"Bearer {CONFIG['AIRTABLE_API_KEY']}", "Content-Type": "application/json"}
    try: requests.post(url, headers=headers, json={"records": [{"fields": fields}]}, timeout=5)
    except Exception: pass

def log_ticket_to_airtable(tid, email, tier, issue):
    fields = {"TicketID": str(tid), "Email": email, "Tier": tier, "Issue": issue, "Status": "Open", "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    send_to_airtable(CONFIG["AIRTABLE_TABLE_TICKETS"], fields)

def log_activation(email, key, method):
    fields = {"Email": email, "LicenseKey": key, "ActivationMethod": method, "ActivatedAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    send_to_airtable(CONFIG["AIRTABLE_TABLE_USERS"], fields)

# ==========================================
# 4. 其他功能 (含限额逻辑)
# ==========================================
def smart_intercept(subject_text):
    if not subject_text: return False, ""
    subject_lower = subject_text.lower()
    for keyword, reply in dm.INTERCEPTORS.items():
        if keyword in subject_lower: return True, reply
    return False, ""

def send_auto_reply_email(user_email, user_tier, ticket_id, subject):
    if not CONFIG["EMAIL_APP_PASSWORD"] or not CONFIG["EMAIL_SENDER_ADDRESS"]: return "SMTP Not Configured"
    try:
        msg = MIMEMultipart(); msg['From'] = CONFIG["EMAIL_SENDER_ADDRESS"]; msg['To'] = user_email
        if user_tier == "Pro":
            msg['Subject'] = f"💎 [VIP Priority] Case #{ticket_id} Received"
            body = f"Dear Pro Member,\n\nReceived: {subject}\nStatus: VIP Priority.\n\nLai's Lab Team"
        else:
            msg['Subject'] = f"[Ticket] Case #{ticket_id} Received"
            body = f"Dear User,\n\nReceived: {subject}\nStatus: Standard Queue.\n\nLai's Lab Support"
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587); server.starttls()
        server.login(CONFIG["EMAIL_SENDER_ADDRESS"], CONFIG["EMAIL_APP_PASSWORD"])
        server.sendmail(CONFIG["EMAIL_SENDER_ADDRESS"], user_email, msg.as_string()); server.quit()
        return "Email Sent"
    except Exception: return "SMTP Error"

# ✅ 核心修正：明确限制 Pro 为 1000
def check_daily_limit_by_email(email, tier, current_usage):
    # Guest = 5, Pro = 1000
    limit = 5 if tier == "Guest" else 1000
    
    if current_usage >= limit:
        return False, 0, limit # 超过限额
    
    return True, limit - current_usage, limit

def check_mode_lock(tier, mode_name):
    if tier == "Pro": return False
    if "(Pro)" in mode_name: return True
    return False

def perform_logout(): pass
