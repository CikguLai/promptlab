import streamlit as st
import google.generativeai as genai
from PIL import Image
import zipfile
import io
import time
import requests
from fpdf import FPDF
import base64
import random
import urllib.parse

# ==========================================
# 1. 全球多语言字典 (Enterprise Edition - 15 Languages)
# ==========================================
TRANSLATIONS = {
    "English": {
        "nav_home": "🚀 Generator", "nav_history": "📂 History & Export", "nav_vip": "💎 VIP Plan", "nav_help": "💁 Help Center",
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 VIP Login",
        "activation_code": "Enter License Key",
        "vip_active": "✅ VIP Active",
        "vip_benefits": "⚡ Benefit: Instant Speed, Batch 50, PDF",
        "free_limit_info": "🔓 Free Daily Limit: {remaining}",
        "upgrade_title": "🚀 Upgrade to Professional",
        "upgrade_desc": "Unlock the full potential of AI with VisionPrompter VIP.",
        "price_old": "$39.90", "price_new": "$12.90", "price_lifetime": "/ Lifetime",
        "feature_1": "⚡ **Instant Speed** (No Queues)",
        "feature_2": "📦 **Batch 50 Items** (vs 3)",
        "feature_3": "📄 **PDF & Excel Export**",
        "feature_4": "🎨 **Unlock All 12 Pro Styles**",
        "upgrade_btn": "👉 Get Lifetime Access Now",
        "limited_offer": "⚡ Limited time early-bird offer.",
        "get_started": "📧 Free Guest Access",
        "email_hint": "Email address",
        "config": "⚙️ Configuration",
        "mode_label": "Mode:",
        "input_method_label": "Input:",
        "input_upload": "📷 Image Analysis",
        "input_text": "✍️ Text to Prompt",
        "text_area_label": "Describe your idea...",
        "lang_label": "Output Language:",
        "style_vip_label": "🎨 Pro Styles (VIP):",
        "style_free_label": "🎨 Basic Styles:",
        "style_lock_warning": "💎 VIP Only.",
        "upload_label": "Drag & Drop Images (Max {limit})",
        "email_warning": "🔒 Please login with Email (Sidebar) to start.",
        "generate_btn": "✨ Generate Prompts",
        "daily_limit_error": "⛔ Daily Limit Reached. See VIP tab.",
        "credit_warning": "⚠️ Credits left: {count}.",
        "batch_warning": "⚠️ Batch limit: {limit}.",
        "processing_vip": "⚡ **VIP Speed:** Processing {current}/{total}...",
        "processing_free": "⏳ **Queue:** {msg}...",
        "complete": "✅ Done!",
        "clear_btn": "🗑️ Clear History",
        "copy_text": "📋 Copy",
        "share_title": "🚀 Share:",
        "download_pdf": "📄 PDF Report",
        "upsell_msg": "⚡ Too slow? <a href='#' style='color:#FF4B4B'>Go VIP</a>",
        "export_title": "📦 Export Data",
        "download_zip": "💎 Download Batch (.zip)",
        "zip_desc": "Includes Excel (CSV) + Txt",
        "download_txt": "📄 Download .txt",
        "txt_desc": "Excel is for VIPs.",
        "footer_rights": "© 2025 Cikgu Lai. Enterprise Edition.",
        "footer_disclaimer": "Secure AI Processing.",
        "faq_title": "📚 Frequently Asked Questions",
        "faq_content": "**Q: Does it create images?**\nA: No. It generates professional **Prompts**. You copy these into Midjourney/Bing.\n\n**Q: Is there a monthly fee?**\nA: No! **One-Time Payment** for lifetime access.\n\n**Q: I didn't get the code?**\nA: Check your **Spam/Junk** folder. Email comes from LemonSqueezy.",
        "support_title": "🎫 Submit a Support Ticket",
        "support_ticket_label": "We usually reply within 24 hours.",
        "ticket_email": "Your Email",
        "ticket_type": "Issue Type",
        "ticket_desc": "Describe the issue...",
        "ticket_btn": "🚀 Submit Ticket",
        "ticket_success": "✅ Ticket {id} Received!"
    },
    "Chinese (Simplified)": {
        "nav_home": "🚀 开始生成", "nav_history": "📂 历史与导出", "nav_vip": "💎 会员中心", "nav_help": "💁 帮助与客服",
        "app_title": "VisionPrompter 视觉大师",
        "vip_access": "💎 VIP 登录",
        "activation_code": "输入激活码",
        "vip_active": "✅ VIP 已激活",
        "vip_benefits": "⚡ 权益：极速模式、批量50张、PDF导出",
        "free_limit_info": "🔓 今日免费额度: {remaining}",
        "upgrade_title": "🚀 升级到专业版",
        "upgrade_desc": "解锁 VisionPrompter 的全部 AI 潜力。",
        "price_old": "$39.90", "price_new": "$12.90", "price_lifetime": "/ 终身买断",
        "feature_1": "⚡ **极速生成** (无需排队)",
        "feature_2": "📦 **批量处理 50 项** (免费仅3项)",
        "feature_3": "📄 **导出 PDF 报告与 Excel**",
        "feature_4": "🎨 **解锁所有 12 种专业风格**",
        "upgrade_btn": "👉 立即获取终身使用权",
        "limited_offer": "⚡ 限时早鸟优惠",
        "get_started": "📧 访客通道",
        "email_hint": "输入邮箱开始",
        "config": "⚙️ 生成参数",
        "mode_label": "模式:",
        "input_method_label": "输入:",
        "input_upload": "📷 图片分析",
        "input_text": "✍️ 创意文本",
        "text_area_label": "描述你的想法...",
        "lang_label": "输出语言:",
        "style_vip_label": "🎨 专业风格 (VIP):",
        "style_free_label": "🎨 基础风格:",
        "style_lock_warning": "💎 VIP 专属",
        "upload_label": "拖拽上传图片 (最多 {limit} 张)",
        "email_warning": "🔒 请先在左侧输入邮箱。",
        "generate_btn": "✨ 立即生成",
        "daily_limit_error": "⛔ 今日额度已尽。请查看会员中心。",
        "credit_warning": "⚠️ 剩余额度: {count}",
        "batch_warning": "⚠️ 批量限制: {limit}",
        "processing_vip": "⚡ **VIP 极速:** 正在处理 {current}/{total}...",
        "processing_free": "⏳ **排队中:** {msg}...",
        "complete": "✅ 完成!",
        "clear_btn": "🗑️ 清空记录",
        "copy_text": "📋 复制",
        "share_title": "🚀 分享:",
        "download_pdf": "📄 PDF 报告",
        "upsell_msg": "⚡ 太慢了？ <a href='#' style='color:#FF4B4B'>升级 VIP</a>",
        "export_title": "📦 数据导出",
        "download_zip": "💎 下载数据包 (.zip)",
        "zip_desc": "包含 Excel (CSV) + 文本",
        "download_txt": "📄 下载 .txt",
        "txt_desc": "Excel 仅限 VIP",
        "footer_rights": "© 2025 Cikgu Lai. 企业版。",
        "footer_disclaimer": "AI 数据安全处理。",
        "faq_title": "📚 常见问题 (FAQ)",
        "faq_content": "**Q: 能直接生成图片吗？**\nA: 不能。它是生成**专业提示词**的。您复制提示词去 Midjourney/Bing 生成图片。\n\n**Q: 是按月付费吗？**\nA: 不是！**一次性付费**，终身使用。\n\n**Q: 没收到激活码？**\nA: 请检查**垃圾邮件 (Spam)**。邮件来自 LemonSqueezy。",
        "support_title": "🎫 提交工单",
        "support_ticket_label": "我们通常在 24 小时内回复。",
        "ticket_email": "联系邮箱",
        "ticket_type": "问题类型",
        "ticket_desc": "问题描述...",
        "ticket_btn": "🚀 提交工单",
        "ticket_success": "✅ 工单 {id} 已收到！"
    },
    "Malay": {
        "nav_home": "🚀 Generator", "nav_history": "📂 Sejarah & Eksport", "nav_vip": "💎 Pelan VIP", "nav_help": "💁 Bantuan",
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 Log Masuk VIP",
        "activation_code": "Masukkan Kod",
        "vip_active": "✅ VIP Aktif",
        "vip_benefits": "⚡ Faedah: Laju, 50/Batch, PDF",
        "free_limit_info": "🔓 Had Harian: {remaining}",
        "upgrade_title": "🚀 Naik Taraf Profesional",
        "upgrade_desc": "Buka potensi penuh AI dengan VisionPrompter VIP.",
        "price_old": "$39.90", "price_new": "$12.90", "price_lifetime": "/ Seumur Hidup",
        "feature_1": "⚡ **Kelajuan Pantas** (Tiada Giliran)",
        "feature_2": "📦 **Batch 50 Item** (vs 3)",
        "feature_3": "📄 **Eksport PDF & Excel**",
        "feature_4": "🎨 **Buka Semua 12 Gaya Pro**",
        "upgrade_btn": "👉 Dapatkan Akses Seumur Hidup",
        "limited_offer": "⚡ Tawaran terhad.",
        "get_started": "📧 Akses Tetamu",
        "email_hint": "Alamat Emel",
        "config": "⚙️ Tetapan",
        "mode_label": "Mod:",
        "input_method_label": "Input:",
        "input_upload": "📷 Analisis Gambar",
        "input_text": "✍️ Teks ke Prompt",
        "text_area_label": "Tulis idea anda...",
        "lang_label": "Bahasa Output:",
        "style_vip_label": "🎨 Gaya Pro (VIP):",
        "style_free_label": "🎨 Gaya Asas:",
        "style_lock_warning": "💎 Khas VIP",
        "upload_label": "Muat Naik Gambar (Max {limit})",
        "email_warning": "🔒 Sila masukkan emel di kiri dahulu.",
        "generate_btn": "✨ Mula Jana",
        "daily_limit_error": "⛔ Had Harian Tamat. Lihat tab VIP.",
        "credit_warning": "⚠️ Baki kredit: {count}",
        "batch_warning": "⚠️ Had batch: {limit}",
        "processing_vip": "⚡ **VIP Laju:** Memproses {current}/{total}...",
        "processing_free": "⏳ **Giliran:** {msg}...",
        "complete": "✅ Siap!",
        "clear_btn": "🗑️ Padam Sejarah",
        "copy_text": "📋 Salin",
        "share_title": "🚀 Kongsi:",
        "download_pdf": "📄 Laporan PDF",
        "upsell_msg": "⚡ Lambat? <a href='#' style='color:#FF4B4B'>Naik Taraf VIP</a>",
        "export_title": "📦 Eksport Data",
        "download_zip": "💎 Muat Turun (.zip)",
        "zip_desc": "Termasuk Excel (CSV) + Txt",
        "download_txt": "📄 Muat Turun .txt",
        "txt_desc": "Excel untuk VIP.",
        "footer_rights": "© 2025 Cikgu Lai. Enterprise Edition.",
        "footer_disclaimer": "Pemprosesan AI Selamat.",
        "faq_title": "📚 Soalan Lazim (FAQ)",
        "faq_content": "**Q: Adakah ia buat gambar?**\nA: Tidak. Ia menjana **Prompt Profesional**. Anda copy ke Midjourney/Bing.\n\n**Q: Adakah bayaran bulanan?**\nA: Tidak! **Bayar Sekali Sahaja** seumur hidup.\n\n**Q: Tak dapat kod?**\nA: Semak folder **Spam/Junk**. Emel dari LemonSqueezy.",
        "support_title": "🎫 Hantar Tiket Sokongan",
        "support_ticket_label": "Kami balas dalam 24 jam.",
        "ticket_email": "Emel Anda",
        "ticket_type": "Jenis Masalah",
        "ticket_desc": "Huraian masalah...",
        "ticket_btn": "🚀 Hantar Tiket",
        "ticket_success": "✅ Tiket {id} Diterima!"
    }
}

# 简单的回退机制
def get_text(t, key):
    return t.get(key, TRANSLATIONS["English"].get(key, key))

# ==========================================
# 2. 系统配置
# ==========================================
st.set_page_config(
    page_title="VisionPrompter AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 Session State
if 'results' not in st.session_state: st.session_state['results'] = []
if 'usage_count' not in st.session_state: st.session_state['usage_count'] = 0 
if 'user_email' not in st.session_state: st.session_state['user_email'] = ""
if 'last_used_time' not in st.session_state: st.session_state['last_used_time'] = 0

# 检查 API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Critical: GOOGLE_API_KEY missing in Secrets.")
    st.stop()
api_key = st.secrets["GOOGLE_API_KEY"]

# === ✨ CSS 高级美化 (Enterprise Look) ===
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .result-card { 
        background: white; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #e0e0e0; 
        margin-bottom: 20px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.04); 
    }
    .vip-card {
        background: linear-gradient(135deg, #ffffff 0%, #fff8f8 100%);
        border: 2px solid #FF4B4B;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(255, 75, 75, 0.15);
    }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: white; border-radius: 8px 8px 0 0; border: 1px solid #eee; border-bottom: none; }
    .stTabs [aria-selected="true"] { background-color: #fff; border-top: 3px solid #FF4B4B; color: #FF4B4B; }
</style>
""", unsafe_allow_html=True)

# === 核心功能函数 ===
def send_telegram_msg(name, email, msg):
    if "telegram" in st.secrets:
        token = st.secrets["telegram"]["token"]
        chat_id = st.secrets["telegram"]["chat_id"]
        text = f"🔔 **Notification**\n\n👤 **User:** {name}\n📧 **Email:** {email}\n💬 **Content:**\n{msg}"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
        except:
            pass

# === 📄 PDF 生成函数 (含 VIP 签名与时间) ===
def create_pdf(image, text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 标题
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(190, 10, txt=f"VisionPrompter Report", ln=1, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(190, 10, txt=f"File Reference: {filename}", ln=1, align='C')
    pdf.ln(5)
    
    # 图片
    if image:
        try:
            with io.BytesIO() as output:
                image.save(output, format="JPEG")
                pdf.image(output, x=15, y=35, w=180)
                pdf.ln(105)
        except:
            pdf.cell(190, 10, txt="[Image Processing Error]", ln=1)
            
    # 内容
    pdf.set_font("Arial", size=11)
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, safe_text)
    
    # === 底部签名 (防伪) ===
    pdf.ln(15)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    current_user = st.session_state.get('user_email', '')
    if not current_user: current_user = "Verified VIP Member"

    pdf.set_font("Arial", size=8, style='I')
    pdf.set_text_color(128, 128, 128)
    # 自动插入当前日期
    date_str = time.strftime('%Y-%m-%d')
    footer_text = f"Generated by VisionPrompter AI | Licensed to: {current_user} | Date: {date_str}"
    
    pdf.cell(0, 10, txt=footer_text, ln=1, align='R')
    return pdf.output(dest='S').encode('latin-1')

def generate_share_links(text, url="https://app.cikgulai.com"):
    safe_text = urllib.parse.quote(text[:200] + "...") 
    safe_url = urllib.parse.quote(url)
    return {
        "wa": f"https://wa.me/?text={safe_text} {safe_url}",
        "fb": f"https://www.facebook.com/sharer/sharer.php?u={safe_url}",
        "tw": f"https://twitter.com/intent/tweet?text={safe_text}&url={safe_url}",
        "li": f"https://www.linkedin.com/sharing/share-offsite/?url={safe_url}",
    }

def build_prompt(mode, language, style_modifier, is_vip, input_type="image"):
    vip_quality_boost = "masterpiece, best quality, 8k"
    if mode == "Prompt Gacha":
        if input_type == "text":
            return f"Role: Expert Prompter. Task: Convert '{language}' idea to English Stable Diffusion prompt. Idea: {{INPUT}}. Style: {style_modifier}. Add: {vip_quality_boost if is_vip else ''}"
        else:
            return f"Role: Expert Prompter. Task: Analyze image and create English Stable Diffusion prompt. Structure: Subject, Style, Lighting. Style: {style_modifier}. Add: {vip_quality_boost if is_vip else ''}"
    elif mode == "Storyteller":
        return f"Write a children's story in {language}. Input: {{INPUT}}. Include a drawing prompt."
    elif mode == "Social Kit":
        return f"Write a viral social post in {language}. Input: {{INPUT}}."
    return "Describe input."

def process_and_save(inputs, mode, output_lang, style, is_vip, ui_text, input_type):
    # === 🛡️ 防滥用冷却系统 ===
    current_time = time.time()
    last_used = st.session_state.get('last_used_time', 0)
    cooldown = 2 if is_vip else 5
    if current_time - last_used < cooldown:
        st.warning(f"⏳ Please wait {cooldown} seconds between generations.")
        st.stop()
    st.session_state['last_used_time'] = current_time
    # === 结束 ===

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash') # ✅ 锁定 2.5 Flash
    
    loading_messages = ["AI is thinking...", "Connecting neural networks...", "Drafting magic..."]
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_items = len(inputs)

    for i, item in enumerate(inputs):
        if is_vip:
            msg = get_text(ui_text, "processing_vip").format(current=i+1, total=total_items)
            status_text.markdown(msg)
            time.sleep(0.5) 
        else:
            rand_msg = random.choice(loading_messages)
            msg = get_text(ui_text, "processing_free").format(msg=rand_msg)
            status_text.markdown(msg)
            time.sleep(1.5)
        try:
            base_prompt = build_prompt(mode, output_lang, style, is_vip, input_type)
            if input_type == "text":
                final_prompt = base_prompt.replace("{{INPUT}}", item)
                response = model.generate_content(final_prompt)
                filename = f"Idea_{str(int(time.time()))}_{i}" 
                img_obj = None 
            else:
                img_obj = Image.open(item)
                response = model.generate_content([base_prompt, img_obj])
                filename = item.name
            content = response.text
            st.session_state['results'].append({"filename": filename, "content": content, "image": img_obj, "mode": mode})
            if not is_vip: st.session_state['usage_count'] += 1
        except Exception as e:
            st.error(f"Error: {e}")
        progress_bar.progress((i + 1) / total_items)
    
    time.sleep(0.5)
    progress_bar.progress(100)
    status_text.success(get_text(ui_text, "complete"))
    time.sleep(1)
    status_text.empty()

# ==========================================
# 3. 侧边栏：核心设置
# ==========================================
with st.sidebar:
    lang_list = list(TRANSLATIONS.keys())
    ui_lang = st.selectbox("🌐 Language / 语言", lang_list, index=0)
    t = TRANSLATIONS.get(ui_lang, TRANSLATIONS["English"])
    st.divider()
    vip_code = st.text_input(get_text(t, 'activation_code'), type="password", placeholder="License Key")
    if vip_code: vip_code = vip_code.strip()
    is_vip = vip_code in st.secrets.get("MANUAL_CODES", ["demo"])
    
    if is_vip:
        st.success(get_text(t, 'vip_active'))
        st.caption("✨ Lifetime Enterprise License")
        daily_limit = 200
    else:
        st.info("👤 Guest Mode")
        email = st.text_input("Email", value=st.session_state['user_email'], placeholder="user@example.com")
        if email: st.session_state['user_email'] = email
        daily_limit = 3
        remaining = daily_limit - st.session_state['usage_count']
        if remaining < 0: remaining = 0
        st.progress(st.session_state['usage_count'] / daily_limit)
        st.caption(get_text(t, 'free_limit_info').format(remaining=remaining))
    st.divider()
    st.subheader(get_text(t, 'config'))
    input_method = st.radio(get_text(t, "input_method_label"), ["upload", "text"], 
                            format_func=lambda x: get_text(t, "input_upload") if x == "upload" else get_text(t, "input_text"))
    mode = st.radio(get_text(t, 'mode_label'), ["Prompt Gacha", "Storyteller", "Social Kit"])
    output_lang = st.selectbox(get_text(t, 'lang_label'), lang_list, index=0)
    if is_vip:
        style_options = ["None (Default)", "🖍️ Coloring Book", "🧱 Claymation 3D", "🎬 Pixar/Disney", "✨ Anime Ghibli", "📸 Hyper-Realistic", "🔳 Vector Flat Art", "🌃 Cyberpunk", "📜 Watercolor"]
        style_modifier = st.selectbox(get_text(t, 'style_vip_label'), style_options)
    else:
        style_options_free = ["None (Default)", "📝 Detailed", "⚡ Concise", "🔒 Unlock 12+ Pro Styles (VIP)"]
        style_modifier = st.selectbox(get_text(t, 'style_free_label'), style_options_free)

# ==========================================
# 4. 主界面：多标签导航
# ==========================================
st.title(f"{get_text(t, 'app_title')}")
tab_home, tab_history, tab_vip, tab_help = st.tabs([get_text(t, "nav_home"), get_text(t, "nav_history"), get_text(t, "nav_vip"), get_text(t, "nav_help")])

# --- Tab 1: 生成器 ---
with tab_home:
    batch_limit = 50 if is_vip else 3
    passed_gate = is_vip or (st.session_state['user_email'] != "")
    inputs = []
    st.markdown(f"#### 🪄 {mode}")
    if st.session_state['usage_count'] >= daily_limit:
        st.error(get_text(t, 'daily_limit_error'))
    else:
        if input_method == "upload":
            label = get_text(t, 'upload_label').format(limit=batch_limit)
            uploaded_files = st.file_uploader(label, type=["jpg","png","webp"], accept_multiple_files=True)
            if uploaded_files: inputs = uploaded_files
            current_input_type = "image"
        else:
            user_text = st.text_area(get_text(t, "text_area_label"), height=150)
            if user_text: inputs = [user_text] 
            current_input_type = "text"

        if inputs:
            if not passed_gate:
                st.warning(get_text(t, 'email_warning'))
            else:
                if st.button(get_text(t, 'generate_btn'), type="primary", use_container_width=True):
                    process_and_save(inputs, mode, output_lang, style_modifier, is_vip, t, current_input_type)
                    st.rerun()

    if st.session_state['results']:
        st.divider()
        latest = st.session_state['results'][-1]
        st.markdown(f"### 🎉 Latest Result")
        st.markdown(latest['content'])

# --- Tab 2: 历史 ---
with tab_history:
    st.header(get_text(t, "nav_history"))
    if not st.session_state['results']:
        st.info("📭 No history yet.")
    else:
        if st.button(get_text(t, 'clear_btn')):
            st.session_state['results'] = []
            st.rerun()
        st.markdown("### " + get_text(t, 'export_title'))
        ex_c1, ex_c2 = st.columns(2)
        txt_buffer = ""
        csv_buffer = "Filename,Mode,Content\n"
        for item in st.session_state['results']:
            txt_buffer += f"=== {item['filename']} ===\n{item['content']}\n\n"
            safe_content = item['content'].replace('"', '""')
            csv_buffer += f'"{item["filename"]}","{item["mode"]}","{safe_content}"\n'
        with ex_c1:
            st.download_button(get_text(t, 'download_txt'), txt_buffer, "prompts.txt", "text/plain", use_container_width=True)
        with ex_c2:
            if is_vip:
                st.download_button("📥 Download Excel (CSV)", csv_buffer, "prompts.csv", "text/csv", use_container_width=True)
            else:
                st.button("🔒 Download Excel (VIP)", disabled=True)
        st.divider()
        for item in reversed(st.session_state['results']):
            with st.container():
                st.markdown(f"<div class='result-card'><h5>📄 {item['filename']}</h5>", unsafe_allow_html=True)
                cols = st.columns([1, 3])
                with cols[0]:
                    if item['image']: st.image(item['image'], use_container_width=True)
                    else: st.info("Text")
                with cols[1]:
                    st.code(item['content'], language="markdown")
                    if is_vip:
                        pdf_bytes = create_pdf(item['image'], item['content'], item['filename'])
                        st.download_button("📄 PDF Report", pdf_bytes, f"{item['filename']}.pdf", "application/pdf")
                st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 3: VIP ---
with tab_vip:
    if is_vip:
        st.balloons()
        st.success(f"🎉 {get_text(t, 'vip_active')}")
        st.markdown(f"<div class='vip-card'><h2>👑 Enterprise License Active</h2><p>Unlimited Speed & Styles Unlocked.</p></div>", unsafe_allow_html=True)
    else:
        st.header(get_text(t, "upgrade_title"))
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown(f"### {get_text(t, 'price_new')} <span style='font-size:0.6em;color:#666'>{get_text(t, 'price_lifetime')}</span>\n\n{get_text(t, 'feature_1')}\n{get_text(t, 'feature_2')}\n{get_text(t, 'feature_3')}\n{get_text(t, 'feature_4')}", unsafe_allow_html=True)
            st.link_button(get_text(t, "upgrade_btn"), "https://your-shop.lemonsqueezy.com/buy/xxxx", type="primary")

# --- Tab 4: Help ---
with tab_help:
    col_help1, col_help2 = st.columns([3, 2])
    with col_help1:
        st.header(get_text(t, "faq_title"))
        faq_text = get_text(t, "faq_content")
        parts = faq_text.split("**Q:")
        for part in parts:
            if part.strip():
                try:
                    q, a = part.split("**\nA:")
                    with st.expander(f"❓ {q.strip()}"):
                        st.markdown(a.strip())
                except: continue
    with col_help2:
        st.markdown(f"<div class='result-card'>", unsafe_allow_html=True)
        st.subheader(get_text(t, "support_title"))
        with st.form("ticket_form"):
            t_email = st.text_input(get_text(t, "ticket_email"), value=st.session_state['user_email'])
            t_desc = st.text_area(get_text(t, "ticket_desc"))
            if st.form_submit_button(get_text(t, "ticket_btn"), type="primary", use_container_width=True):
                if t_email and t_desc:
                    st.success(get_text(t, "ticket_success").format(id=random.randint(1000,9999)))
                    send_telegram_msg("Support", t_email, f"Ticket: {t_desc}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<div style='text-align:center;color:#aaa;font-size:0.8em'>{get_text(t, 'footer_rights')}</div>", unsafe_allow_html=True)