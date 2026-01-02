# lc_gen.py
# Generation Logic Module
# Handles: PASEC Protocol, PDF/CSV creation, Social Links, QR Code

import urllib.parse, os, io
from fpdf import FPDF
import qrcode # [NEW]
import dm_core as dc
import dm_data as dd

def generate_pasec_prompt(role, mode, option, user_input, tier, lang, tone):
    templates = dc.ROLES_CONFIG.get(role, {}).get(mode, [])
    template_str = next((t['template'] for t in templates if t['label'] == option), "{input}")
    
    res = f"### [PASEC PROTOCOL V3.0 - LAI'S LAB]\n"
    res += f"**ROLE**: {role} | **MODE**: {mode}\n"
    res += f"**TONE**: {tone} | **LANGUAGE**: {lang}\n"
    res += f"**TASK**: {option}\n"
    res += "-" * 20 + "\n"
    res += f"**INSTRUCTION**: {template_str.format(input=user_input)}\n"
    res += "-" * 20 + "\n"
    res += f"[SYSTEM]: Output strictly in **{lang}**."
    
    if tier == "Pro":
        res += " Use advanced formatting, bullet points, and professional terminology."
    else:
        res += " (Generated via Free Version)"
        
    return res

def check_daily_limit_by_email(email, tier, current_usage):
    limit = 1000 if tier == "Pro" else 5
    return (current_usage < limit), limit - current_usage, limit

def check_mode_lock(tier, mode_name):
    return False if tier == "Pro" else "(Pro)" in mode_name

def smart_intercept(text, lang):
    text_lower = text.lower()
    for keywords, faq_index in dc.INTERCEPT_LOGIC:
        if any(k in text_lower for k in keywords):
            return True, dd.FAQ_DATABASE.get(lang, dd.FAQ_DATABASE["English"])[faq_index]["a"]
    return False, ""

# [UPDATED] 加入 LINE
def get_social_links(text):
    e = urllib.parse.quote(text[:300] + "...") # Truncate for URL safety
    return {
        "WhatsApp": f"https://wa.me/?text={e}",
        "Telegram": f"https://t.me/share/url?url=laislab&text={e}",
        "Email": f"mailto:?body={e}",
        "X": f"https://twitter.com/intent/tweet?text={e}",
        "LINE": f"https://line.me/R/msg/text/?{e}" # [NEW]
    }

def create_csv(text):
    return ("\ufeff" + text).encode("utf-8")

def create_pdf(text, role, mode):
    try:
        pdf = FPDF()
        pdf.add_page()
        font_path = "font.ttf"
        if os.path.exists(font_path):
            try:
                pdf.add_font('CustomFont', '', font_path, uni=True)
                pdf.set_font("CustomFont", size=12)
            except: pdf.set_font("Arial", size=12)
        else:
            pdf.set_font("Arial", size=12)
            
        pdf.cell(0, 10, txt=f"Lai's Lab Report: {role} - {mode}", ln=True, align='C')
        pdf.ln(10)
        pdf.multi_cell(0, 10, txt=text)
        return pdf.output(dest='S').encode('latin-1')
    except: return None

# [NEW] 生成二维码函数
def generate_qr_code(text):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    # 限制二维码内容长度，防止太密扫不出来
    qr.add_data(text[:800]) 
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    # 转换为字节流供 Streamlit 显示
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()