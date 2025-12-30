# logic_core.py
# Lai's Lab V9.14 - 业务逻辑核心 (Final Gold Version)
# 功能：PASEC引擎、真人语气注入、SMTP邮件、智能拦截

import requests
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import data_matrix as dm

CONFIG = {
    "EMAIL_APP_PASSWORD": "", "EMAIL_SENDER_ADDRESS": "", "EMAIL_ADMIN_ADDRESS": "",
    "TELEGRAM_BOT_TOKEN": "", "TELEGRAM_CHAT_ID": "",
    "AIRTABLE_API_KEY": "", "LEMONSQUEEZY_API_KEY": ""
}

# 1. 智能拦截 (数据驱动)
def smart_intercept(subject_text):
    if not subject_text: return False, ""
    subject_lower = subject_text.lower()
    # 遍历 data_matrix 自动生成的拦截字典
    for keyword, reply in dm.INTERCEPTORS.items():
        if keyword in subject_lower: return True, reply
    return False, ""

# 2. SMTP 真实邮件
def send_auto_reply_email(user_email, user_tier, ticket_id, subject):
    if not CONFIG["EMAIL_APP_PASSWORD"] or not CONFIG["EMAIL_SENDER_ADDRESS"]: return "SMTP Not Configured"
    try:
        msg = MIMEMultipart(); msg['From'] = CONFIG["EMAIL_SENDER_ADDRESS"]; msg['To'] = user_email
        
        # 区分 Guest 和 Pro 的回执内容
        if user_tier == "Pro":
            msg['Subject'] = f"💎 [VIP Priority] Case #{ticket_id} - Priority Access Confirmed"
            body = f"""Dear Pro Member,

We have escalated your ticket to the top of our queue.
Subject: {subject}

💎 Priority Status: VIP (Expect reply in 1-2 business days).

Best,
Lai's Lab Enterprise Team"""
        else:
            msg['Subject'] = f"[Ticket Received] Case #{ticket_id} - We are reviewing your issue"
            body = f"""Dear User,

We have received your support request.
Subject: {subject}

💡 Tip: Check the FAQ in the sidebar for instant answers.
Status: Queued (Expect reply in 3-5 business days).

Best,
Lai's Lab Support"""
            
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587); server.starttls()
        server.login(CONFIG["EMAIL_SENDER_ADDRESS"], CONFIG["EMAIL_APP_PASSWORD"])
        server.sendmail(CONFIG["EMAIL_SENDER_ADDRESS"], user_email, msg.as_string()); server.quit()
        return "Email Sent Successfully"
    except Exception as e: return f"SMTP Error: {str(e)}"

# 3. 辅助功能
def check_user_tier(email, key):
    # 简单模拟：实际可对接 LemonSqueezy API
    if key.startswith("LAI-") and len(key) > 8: return "Pro"
    return "Guest"

def check_daily_limit_by_email(email, tier, current_usage):
    limit = 5 if tier == "Guest" else 1000 # Pro 无限
    if current_usage >= limit: return False, 0, limit
    return True, limit - current_usage, limit

def check_mode_lock(tier, mode_name):
    if tier == "Pro": return False
    # 包含 (Pro) 字样的模式对 Guest 锁定
    if "(Pro)" in mode_name: return True
    return False

# 4. PASEC 核心生成引擎
def generate_ai_response_mock(role, mode, option, user_input, tier, lang, tone="Professional"):
    # 获取 Prompt 模板
    template = "Generate content for: {input}"
    if role in dm.ROLES_CONFIG and mode in dm.ROLES_CONFIG[role]:
        for opt in dm.ROLES_CONFIG[role][mode]:
            if opt["label"] == option:
                template = opt["template"]
                break
    
    # 清洗语气字符串 (例如 "Witty (幽默)" -> "Witty")
    tone_clean = tone.split("(")[0].strip()
    
    # 组装 PASEC 结构
    pasec_output = f"""
## 👤 P - Persona
I am acting as a top-tier **{role}** specialized in **{mode}**.
My voice is strictly **{tone}**. I will adopt this persona to best serve your request regarding: "{user_input}".

## 🎯 A - Aim
The goal is to execute **{option}** effectively.
We aim to solve the specific challenge: *{user_input}* while adhering to the cultural context of **{lang}**.

## 📂 S - Structure
1. **Hook/Opening**: Grab attention or define the problem.
2. **Core Content**: The main deliverable ({option}).
3. **Refinement**: Polishing based on the "{tone_clean}" style.
4. **Call to Action/Closing**: Next steps or conclusion.

## 📝 E - Effective (The Output)
*(AI generating content in {lang} with {tone_clean} tone...)*

**[Here is your draft]:**

> "{user_input} is a great starting point. Here is how we make it shine:"
>
> ... (This section would contain the actual AI generated text based on the template: "{template}") ...
> ... (The content strictly follows the **{tone_clean}** guidelines you selected) ...
> ... (e.g., if you chose 'Witty', expect jokes; if 'Academic', expect citations.) ...
> ...

## 💡 C - Context
* **Why this works**: This approach leverages the {mode} methodology to maximize impact.
* **Pro Tip**: To improve this further, try adding more specific data points to your input next time.
"""
    
    # Guest 水印
    watermark = "\n\n(Generated by Lai's Lab Free Version)" if tier == "Guest" else ""
    return pasec_output + watermark

def log_ticket_to_airtable(tid, email, tier, issue):
    print(f"Logged to Airtable: {tid} | {email} | {issue}")

def perform_logout():
    pass
