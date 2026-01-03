# lc_gen.py
# 核心生成逻辑 + 下载徽章黑科技 + Noto字体支持

import urllib.parse, os, io, base64
from fpdf import FPDF
import qrcode
import dm_core as dc
import dm_data as dd

def generate_pasec_prompt(role, mode, option, user_input, tier, lang, tone):
    # PASEC 5段式结构
    p_block = f"You are an expert **{role}**."
    a_block = f"Aim: **{mode}** strategy."
    s_block = f"Structure: **{option}**."
    e_block = f"Tone: **{tone}**."
    c_block = f"Context: \"{user_input}\""

    # 内部指令头
    header = f"### [PASEC PROTOCOL V3.0]\n"
    header += f"**1.PERSONA**: {p_block}\n**2.AIM**: {a_block}\n**3.STRUCTURE**: {s_block}\n"
    header += f"**4.EFFECTIVE**: {e_block}\n**5.CONTEXT**: {c_block}\n"
    header += "-"*20 + "\n[SYSTEM]: Output strictly in **" + lang + "**.\n"

    # 生成内容
    if tier != "Pro":
        header += "(Generated via Free Version)\n"
    
    return header

def clean_pro_output(text, tier):
    if tier == "Pro":
        text = text.replace("(Generated via Free Version)", "")
        text = text.replace("### [PASEC PROTOCOL V3.0]", "### ✨ PROMPT READY") 
    return text

def get_download_badge(file_data, file_name, mime_type, badge_url):
    b64 = base64.b64encode(file_data).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{file_name}"><img src="{badge_url}" width="100%"></a>'
    return href

def create_pdf(text, role, mode):
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # [UPDATE] 优先检测 NotoSansCJKtc-Regular.ttf
        # 请确保您在 GitHub 根目录上传的文件名完全一致
        font_path = "NotoSansCJKtc-Regular.ttf" 
        
        # 如果找不到 Noto，尝试找 font.ttf
        if not os.path.exists(font_path):
            font_path = "font.ttf"
            
        if os.path.exists(font_path):
            try: 
                # uni=True 开启 Unicode 支持
                pdf.add_font('CustomFont', '', font_path, uni=True)
                pdf.set_font("CustomFont", size=12)
            except: 
                pdf.set_font("Arial", size=12)
        else:
            pdf.set_font("Arial", size=12)
        
        pdf.cell(0, 10, txt=f"Lai's Lab: {role}", ln=True, align='C')
        pdf.ln(10)
        # 清理 markdown 符号以优化 PDF 排版
        clean_text = text.replace("**", "").replace("###", "")
        pdf.multi_cell(0, 10, txt=clean_text)
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        print(f"PDF Gen Error: {e}") 
        return None

def create_csv(text):
    return ("\ufeff" + text).encode("utf-8")

def generate_qr_code(text):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text[:500])
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def get_social_links(text):
    e = urllib.parse.quote(text[:300] + "...")
    return {
        "WhatsApp": f"https://wa.me/?text={e}",
        "Telegram": f"https://t.me/share/url?url=laislab&text={e}",
        "Email": f"mailto:?body={e}",
        "LINE": f"https://line.me/R/msg/text/?{e}"
    }

def check_daily_limit_by_email(email, tier, current_usage):
    limit = 1000 if tier == "Pro" else 5
    return (current_usage < limit), limit - current_usage, limit

def check_mode_lock(tier, mode_name):
    return False if tier == "Pro" else "(Pro)" in mode_name

def smart_intercept(text, lang):
    import dm_core
    import dm_data # 确保引用最新的数据总管
    text_lower = text.lower()
    for keywords, faq_index in dm_core.INTERCEPT_LOGIC:
        if any(k in text_lower for k in keywords):
            # 动态获取当前语言的 FAQ 数据库
            faq_db = dd.FAQ_DATABASE.get(lang, dd.FAQ_DATABASE["English"])
            if faq_index < len(faq_db):
                return True, faq_db[faq_index]["a"]
    return False, ""
