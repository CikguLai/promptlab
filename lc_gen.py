# lc_gen.py
# Generation Logic Module
# Handles: PASEC Engine (Pro Clean / Guest Watermark), PDF Fix

import urllib.parse, os, io, base64
from fpdf import FPDF
import qrcode
from PIL import Image
import dm_core as dc
import dm_data as dd

def generate_pasec_prompt(role, mode, option, user_input, tier, lang, tone):
    # [PASEC ENGINE V10.3]
    
    # 核心内容块
    p_block = f"You are an expert {role}. Your knowledge base covers all aspects of this domain."
    a_block = f"Your specific aim is to execute a {mode} strategy."
    s_block = f"Structure your response strictly according to the framework of: {option}. Ensure all standard elements of this framework are included."
    e_block = f"Maintain a {tone} tone of voice throughout the content. Ensure the delivery is effective for the intended audience."
    c_block = f"The specific topic/context provided by the user is: \"{user_input}\""

    # [GUEST 模式] - 包含 Markdown 格式和系统指令 (为了好看)
    if tier != "Pro":
        header = f"### [PASEC PROTOCOL V3.0]\n"
        header += f"**1. PERSONA**: {p_block}\n"
        header += f"**2. AIM**: {a_block}\n"
        header += f"**3. STRUCTURE**: {s_block}\n"
        header += f"**4. EFFECTIVE**: {e_block}\n"
        header += f"**5. CONTEXT**: {c_block}\n"
        header += "-" * 30 + "\n"
        header += f"[SYSTEM INSTRUCTION]:\n1. Analyze the Context above.\n2. Output strictly in **{lang}** language.\n"
        header += "\n(Generated via Free Version - Lai's Lab AI)"
        return header

    # [PRO 模式] - 纯净版 (方案 A+)
    # 移除 ** (加粗), 移除 ### (标题), 移除 [SYSTEM] 底部废话
    # 只保留核心 Key (PERSONA, AIM...) 供 AI 识别
    # 增加了 ethical safe instruction (策略A的补充)
    
    clean_prompt = f"1. PERSONA: {p_block}\n"
    clean_prompt += f"2. AIM: {a_block}\n"
    clean_prompt += f"3. STRUCTURE: {s_block}\n"
    clean_prompt += f"4. EFFECTIVE: {e_block}\n"
    clean_prompt += f"5. CONTEXT: {c_block}\n"
    clean_prompt += f"\n[INSTRUCTION]: Output the result strictly in {lang} language. Ensure the generated content is ethical, safe, and suitable for general audiences."
    
    return clean_prompt

def clean_pro_output(text, tier):
    # 保持接口兼容
    return text

def check_daily_limit_by_email(email, tier, current_usage):
    limit = 1000 if tier == "Pro" else 5
    return (current_usage < limit), limit - current_usage, limit

def check_mode_lock(tier, mode_name):
    return False if tier == "Pro" else "(Pro)" in mode_name

def smart_intercept(text, lang):
    text_lower = text.lower()
    for keywords, faq_index in dc.INTERCEPT_LOGIC:
        if any(k in text_lower for k in keywords):
            faq_db = dd.FAQ_DATABASE.get(lang, dd.FAQ_DATABASE["English"])
            if faq_index < len(faq_db):
                return True, faq_db[faq_index]["a"]
    return False, ""

def get_social_links(text):
    e = urllib.parse.quote(text[:300] + "...")
    return {
        "WhatsApp": f"https://wa.me/?text={e}",
        "Telegram": f"https://t.me/share/url?url=laislab&text={e}",
        "Email": f"mailto:?body={e}",
        "LINE": f"https://line.me/R/msg/text/?{e}"
    }

def create_csv(text):
    return ("\ufeff" + text).encode("utf-8")

def create_pdf(text, role, mode):
    # [PDF FIX V9 LEGACY] 
    # 不做任何检测，假定 font.ttf 就在那里。这是最原始有效的方法。
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # 直接加载字体，不做 fallback
        pdf.add_font('CustomFont', '', 'font.ttf', uni=True)
        pdf.set_font("CustomFont", size=12)
            
        pdf.cell(0, 10, txt=f"Lai's Lab Report: {role} - {mode}", ln=True, align='C')
        pdf.ln(10)
        
        # 清理不支持的 Markdown 符号
        clean_text = text.replace("**", "").replace("###", "")
        pdf.multi_cell(0, 10, txt=clean_text)
        
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        # 如果真的报错了（比如忘了上传字体），打印出来，但不要崩整个 App
        print(f"PDF Gen Error: {e}")
        return None

def generate_qr_code(text):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text[:500])
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
