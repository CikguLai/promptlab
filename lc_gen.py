# lc_gen.py
# Generation Logic Module
# Handles: PASEC Engine, PDF/CSV, Social Badges, QR

import urllib.parse, os, io, base64  # ✅ [FIX 1] 补全了 base64
from fpdf import FPDF
import qrcode
from PIL import Image
import dm_core as dc
import dm_data as dd

def generate_pasec_prompt(role, mode, option, user_input, tier, lang, tone):
    # [PASEC ENGINE V10.0]
    p_block = f"You are an expert **{role}**. Your knowledge base covers all aspects of this domain."
    a_block = f"Your specific aim is to execute a **{mode}** strategy."
    s_block = f"Structure your response strictly according to the framework of: **{option}**. Ensure all standard elements of this framework are included."
    e_block = f"Maintain a **{tone}** tone of voice throughout the content. Ensure the delivery is effective for the intended audience."
    c_block = f"The specific topic/context provided by the user is: \"{user_input}\""

    header = f"### [PASEC PROTOCOL V3.0 - LAI'S LAB INTERNAL]\n"
    header += f"**1. PERSONA**: {p_block}\n**2. AIM**: {a_block}\n**3. STRUCTURE**: {s_block}\n"
    header += f"**4. EFFECTIVE**: {e_block}\n**5. CONTEXT**: {c_block}\n"
    header += "-" * 30 + "\n"
    header += f"[SYSTEM INSTRUCTION]:\n"
    header += f"1. Analyze the Context above.\n2. Generate the output based on the Structure and Persona.\n"
    header += f"3. Output strictly in **{lang}** language.\n"
    
    if tier != "Pro":
        header += "\n(Generated via Free Version)"
        
    return header

def clean_pro_output(text, tier):
    if tier == "Pro":
        text = text.replace("(Generated via Free Version)", "")
        text = text.replace("### [PASEC PROTOCOL V3.0 - LAI'S LAB INTERNAL]", "### ✨ PROMPT READY")
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
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # ✅ [FIX 2] 优先读取 NotoSansCJKtc-Regular.ttf (防乱码)
        font_path = "NotoSansCJKtc-Regular.ttf"
        if not os.path.exists(font_path):
            font_path = "font.ttf" # 如果没找到新字体，才找旧的
            
        if os.path.exists(font_path):
            try:
                pdf.add_font('CustomFont', '', font_path, uni=True)
                pdf.set_font("CustomFont", size=12)
            except: 
                pdf.set_font("Arial", size=12)
        else:
            pdf.set_font("Arial", size=12)
            
        pdf.cell(0, 10, txt=f"Lai's Lab Report: {role} - {mode}", ln=True, align='C')
        pdf.ln(10)
        clean_text = text.replace("**", "").replace("###", "")
        pdf.multi_cell(0, 10, txt=clean_text)
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        print(f"PDF Error: {e}")
        return None

def generate_qr_code(text):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text[:500])
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
