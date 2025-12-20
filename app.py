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
# 1. 核心配置与语言包
# ==========================================
TRANSLATIONS = {
    "English": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 VIP Access",
        "activation_code": "Activation Code",
        "vip_active": "✅ VIP Active",
        "vip_benefits": "⚡ Unlock: Instant Speed, Max 50/Batch, PDF Export",
        "free_limit_info": "🔓 Free Daily Limit: {remaining} left",
        "upgrade_btn": "🚀 Get Lifetime Access",
        "limited_offer": "Limited time early-bird price.",
        "get_started": "📧 Get Started",
        "email_hint": "Enter email to activate free generator.",
        "config": "⚙️ Configuration",
        "mode_label": "Mode:",
        "input_method_label": "Input Method:",
        "input_upload": "📷 Upload Image (Analyze)",
        "input_text": "✍️ Type Idea (Create)",
        "text_area_label": "Enter your idea here (e.g., 'A cute dinosaur'):",
        "lang_label": "Output Language:",
        "style_vip_label": "🎨 Style (VIP):",
        "style_free_label": "🎨 Style (Free):",
        "style_lock_warning": "💎 This style is for VIPs only. Please upgrade.",
        "upload_label": "Upload Images (Max {limit}/Batch)",
        "email_warning": "🔒 Please enter your Email in sidebar to proceed.",
        "generate_btn": "🚀 Generate Content",
        "daily_limit_error": "⛔ Daily Limit Reached ({current}/{total}). Please come back tomorrow.",
        "credit_warning": "⚠️ You only have {count} credits left. Processing first {count} items.",
        "batch_warning": "⚠️ Batch limit is {limit}. Processing first {limit} only.",
        "processing_vip": "⚡ **VIP Speed:** Processing item {current}/{total} ...",
        "processing_free": "⏳ **Free Tier Queue:** {msg} ...",
        "complete": "✅ Complete!",
        "clear_btn": "🗑️ Clear All",
        "copy_text": "📋 Copy Text",
        "share_title": "🚀 Share to Social Media:",
        "download_pdf": "📄 Download PDF Report",
        "upsell_msg": "⚡ Want instant speed & PDF reports? <a href='#' style='color:#FF4B4B'>Upgrade to VIP</a>",
        "export_title": "📦 Export Data",
        "download_zip": "💎 Download VIP Batch Pack (.zip)",
        "zip_desc": "✅ Includes: Excel (CSV) + Text files",
        "download_txt": "📄 Download as Text (.txt)",
        "txt_desc": "🔒 Want Excel/CSV export? Upgrade to VIP.",
        "footer_rights": "© 2025 Cikgu Lai. All Rights Reserved.",
        "footer_disclaimer": "Disclaimer: Data is processed securely and deleted instantly.",
        "faq_title": "📚 FAQ",
        "faq_content": "**Q: Does it create images?** A: No, it generates Prompts. Copy to Bing/MJ.\n**Q: Subscription?** A: No! One-time payment.\n**Q: Paid but no code?** A: Check Spam.",
        "support_title": "💁 Help Center",
        "support_ticket_label": "Submit a support ticket.",
        "ticket_email": "Email (Required)",
        "ticket_type": "Issue Type",
        "ticket_desc": "Description",
        "ticket_btn": "🚀 Submit Ticket",
        "ticket_success": "✅ Ticket {id} Created!"
    },
    "Chinese (Simplified)": {
        "app_title": "VisionPrompter 视觉大师",
        "vip_access": "💎 VIP 会员通道",
        "activation_code": "输入激活码",
        "vip_active": "✅ VIP 已激活",
        "vip_benefits": "⚡ 解锁权益：极速生成、批量50次、PDF导出",
        "free_limit_info": "🔓 今日免费额度剩余: {remaining}",
        "upgrade_btn": "🚀 获取终身会员 (限时)",
        "limited_offer": "早鸟价限时优惠",
        "get_started": "📧 免费试用",
        "email_hint": "输入邮箱以开启免费生成器",
        "config": "⚙️ 生成设置",
        "mode_label": "选择模式:",
        "input_method_label": "输入方式:",
        "input_upload": "📷 上传图片 (分析风格)",
        "input_text": "✍️ 输入想法 (从零创作)",
        "text_area_label": "在这里输入你的想法 (例如：'一只吃披萨的猫'):",
        "lang_label": "生成语言:",
        "style_vip_label": "🎨 艺术风格 (VIP):",
        "style_free_label": "🎨 基础风格 (免费):",
        "style_lock_warning": "💎 此风格仅限 VIP。请升级以解锁高级风格。",
        "upload_label": "上传图片 (每批最多 {limit} 张)",
        "email_warning": "🔒 请在侧边栏输入邮箱以继续。",
        "generate_btn": "🚀 开始生成",
        "daily_limit_error": "⛔ 今日额度已用完 ({current}/{total})。请明天再来。",
        "credit_warning": "⚠️ 您只剩 {count} 次额度，将仅处理前 {count} 项。",
        "batch_warning": "⚠️ 单次限制 {limit} 项。仅处理前 {limit} 项。",
        "processing_vip": "⚡ **VIP 极速模式:** 正在处理第 {current}/{total} 项 ...",
        "processing_free": "⏳ **免费排队中:** {msg} ...",
        "complete": "✅ 处理完成!",
        "clear_btn": "🗑️ 清空历史",
        "copy_text": "📋 复制文案",
        "share_title": "🚀 一键分享到社媒:",
        "download_pdf": "📄 下载 PDF 报告",
        "upsell_msg": "⚡ 想要秒速生成和 Excel 报表？ <a href='#' style='color:#FF4B4B'>升级 VIP</a>",
        "export_title": "📦 数据导出",
        "download_zip": "💎 下载 VIP 数据包 (.zip)",
        "zip_desc": "✅ 包含: Excel表格 (CSV) + 文本文件",
        "download_txt": "📄 下载纯文本 (.txt)",
        "txt_desc": "🔒 需要 Excel 表格？请升级 VIP。",
        "footer_rights": "© 2025 Cikgu Lai. 版权所有。",
        "footer_disclaimer": "免责声明：数据仅供 AI 分析，处理后即刻删除，绝不留存。",
        "faq_title": "📚 常见问题",
        "faq_content": "**Q: 能直接生图吗？** A: 不能，生成的是提示词。\n**Q: 是订阅制吗？** A: 不是！一次付费终身使用。\n**Q: 没收到码？** A: 检查垃圾邮件。",
        "support_title": "💁 帮助中心",
        "support_ticket_label": "提交工单，24小时内回复。",
        "ticket_email": "联系邮箱",
        "ticket_type": "问题类型",
        "ticket_desc": "问题描述",
        "ticket_btn": "🚀 提交工单",
        "ticket_success": "✅ 工单 {id} 已创建！"
    },
    "Chinese (Traditional)": {
        "app_title": "VisionPrompter 視覺大師", "vip_access": "💎 VIP 會員通道", "activation_code": "輸入激活碼", "vip_active": "✅ VIP 已激活", "vip_benefits": "⚡ 解鎖權益：極速生成、批量50次、PDF導出", "free_limit_info": "🔓 今日免費額度剩餘: {remaining}", "upgrade_btn": "🚀 獲取終身會員 (限時)", "limited_offer": "早鳥價限時優惠", "get_started": "📧 免費試用", "email_hint": "輸入郵箱以開啟免費生成器", "config": "⚙️ 生成設置", "mode_label": "選擇模式:", "input_method_label": "輸入方式:", "input_upload": "📷 上傳圖片 (分析風格)", "input_text": "✍️ 輸入想法 (從零創作)", "text_area_label": "在這裡輸入你的想法:", "lang_label": "生成語言:", "style_vip_label": "🎨 藝術風格 (VIP):", "style_free_label": "🎨 基礎風格 (免費):", "style_lock_warning": "💎 此風格僅限 VIP。請升級以解鎖高級風格。", "upload_label": "上傳圖片 (每批最多 {limit} 張)", "email_warning": "🔒 請在側邊欄輸入郵箱以繼續。", "generate_btn": "🚀 開始生成", "daily_limit_error": "⛔ 今日額度已用完 ({current}/{total})。請明天再來。", "credit_warning": "⚠️ 您只剩 {count} 次額度。", "batch_warning": "⚠️ 單次限制 {limit} 項。", "processing_vip": "⚡ **VIP 極速模式:** 正在處理第 {current}/{total} 項 ...", "processing_free": "⏳ **免費排隊中:** {msg} ...", "complete": "✅ 處理完成!", "clear_btn": "🗑️ 清空歷史", "copy_text": "📋 複製文案", "share_title": "🚀 一鍵分享到社媒:", "download_pdf": "📄 下載 PDF 報告", "upsell_msg": "⚡ 想要秒速生成和 Excel 報表？ <a href='#' style='color:#FF4B4B'>升級 VIP</a>", "export_title": "📦 數據導出", "download_zip": "💎 下載 VIP 數據包 (.zip)", "zip_desc": "✅ 包含: Excel表格 (CSV) + 文本文件", "download_txt": "📄 下載純文本 (.txt)", "txt_desc": "🔒 需要 Excel 表格？請升級 VIP。", "footer_rights": "© 2025 Cikgu Lai. 版權所有。", "footer_disclaimer": "免責聲明：數據僅供 AI 分析，處理後即刻刪除。", "faq_title": "📚 常見問題", "faq_content": "**Q: 能直接生圖嗎？** A: 不能，生成的是提示詞。\n**Q: 是訂閱制嗎？** A: 不是！一次付費終身使用。", "support_title": "💁 幫助中心", "support_ticket_label": "提交工單。", "ticket_email": "聯繫郵箱", "ticket_type": "問題類型", "ticket_desc": "問題描述", "ticket_btn": "🚀 提交工單", "ticket_success": "✅ 工單 {id} 已創建！"
    },
    "Malay": {
        "app_title": "VisionPrompter AI", "vip_access": "💎 Akses VIP", "activation_code": "Kod Pengaktifan", "vip_active": "✅ VIP Aktif", "vip_benefits": "⚡ Buka: Kelajuan Pantas, 50/Batch, PDF", "free_limit_info": "🔓 Had Harian Percuma: {remaining} tinggal", "upgrade_btn": "🚀 Dapatkan Akses Seumur Hidup", "limited_offer": "Tawaran harga terhad.", "get_started": "📧 Mula Sekarang", "email_hint": "Masukkan emel untuk mula.", "config": "⚙️ Tetapan", "mode_label": "Mod:", "input_method_label": "Kaedah Input:", "input_upload": "📷 Muat Naik Gambar (Analisis)", "input_text": "✍️ Tulis Idea (Cipta)", "text_area_label": "Masukkan idea anda di sini:", "lang_label": "Bahasa Output:", "style_vip_label": "🎨 Gaya Seni (VIP):", "style_free_label": "🎨 Gaya Asas (Percuma):", "style_lock_warning": "💎 Gaya ini untuk VIP sahaja. Sila naik taraf.", "upload_label": "Muat Naik Gambar (Max {limit})", "email_warning": "🔒 Sila masukkan Emel di sidebar.", "generate_btn": "🚀 Mula Jana", "daily_limit_error": "⛔ Had Harian Dicapai ({current}/{total}).", "credit_warning": "⚠️ Baki anda {count}.", "batch_warning": "⚠️ Had batch ialah {limit}.", "processing_vip": "⚡ **Kelajuan VIP:** Memproses item {current}/{total} ...", "processing_free": "⏳ **Barisan Percuma:** {msg} ...", "complete": "✅ Selesai!", "clear_btn": "🗑️ Padam Semua", "copy_text": "📋 Salin Teks", "share_title": "🚀 Kongsi ke Media Sosial:", "download_pdf": "📄 Muat Turun PDF", "upsell_msg": "⚡ Mahu laju & Excel? <a href='#' style='color:#FF4B4B'>Naik Taraf VIP</a>", "export_title": "📦 Eksport Data", "download_zip": "💎 Muat Turun Pek VIP (.zip)", "zip_desc": "✅ Termasuk: Excel (CSV) + Teks", "download_txt": "📄 Muat Turun Teks (.txt)", "txt_desc": "🔒 Mahu Excel? Naik Taraf VIP.", "footer_rights": "© 2025 Cikgu Lai. Hak Cipta Terpelihara.", "footer_disclaimer": "Penafian: Data diproses oleh AI dan dipadam serta-merta.", "faq_title": "📚 Soalan Lazim", "faq_content": "**Q: Jana gambar?** A: Tidak, hanya Prompt.\n**Q: Bayaran bulanan?** A: Tidak! Bayar sekali seumur hidup.", "support_title": "💁 Pusat Bantuan", "support_ticket_label": "Hantar tiket sokongan.", "ticket_email": "Emel", "ticket_type": "Jenis Masalah", "ticket_desc": "Huraian", "ticket_btn": "🚀 Hantar Tiket", "ticket_success": "✅ Tiket {id} Dicipta!"
    }
}

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

if 'results' not in st.session_state: st.session_state['results'] = []
if 'usage_count' not in st.session_state: st.session_state['usage_count'] = 0 
if 'user_email' not in st.session_state: st.session_state['user_email'] = ""

# 检查 API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Critical: GOOGLE_API_KEY missing in Secrets.")
    st.stop()
api_key = st.secrets["GOOGLE_API_KEY"]

# CSS 美化
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom, #ffffff, #f8f9fa); font-family: 'Inter', sans-serif; }
    .result-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .share-btn { display: inline-block; padding: 6px 12px; border-radius: 4px; color: white !important; text-decoration: none !important; margin-right: 6px; margin-bottom: 6px; font-size: 0.8em; font-weight: bold; transition: opacity 0.3s; }
    .share-btn:hover { opacity: 0.8; }
    .btn-wa { background-color: #25D366; } .btn-fb { background-color: #1877F2; } .btn-tw { background-color: #000000; }
    .btn-li { background-color: #0077b5; } .btn-ig { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); }
    .btn-tt { background-color: #000000; border: 1px solid #333; } .btn-xhs { background-color: #FF2442; }
    .delay-msg { color: #f59e0b; font-size: 0.9em; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# === 📨 Telegram 通知函数 ===
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

# === 📄 PDF 生成函数 ===
def create_pdf(image, text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"VisionPrompter: {filename}", ln=1, align='C')
    pdf.ln(10)
    if image:
        try:
            with io.BytesIO() as output:
                image.save(output, format="JPEG")
                pdf.image(output, x=10, y=30, w=190)
                pdf.ln(110)
        except:
            pdf.cell(200, 10, txt="[Image Error]", ln=1)
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, safe_text)
    pdf.ln(20)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Arial", size=9, style='I')
    pdf.set_text_color(100, 100, 100)
    user_identity = "Cikgu Lai AI Class"
    if 'user_email' in st.session_state and st.session_state['user_email']:
        user_identity = st.session_state['user_email']
    footer_text = f"Generated with VisionPrompter | Prepared for: {user_identity}"
    pdf.cell(0, 10, txt=footer_text, ln=1, align='R')
    return pdf.output(dest='S').encode('latin-1')

def generate_share_links(text, url="https://app.cikgulai.com"):
    safe_text = urllib.parse.quote(text[:200] + "...") 
    safe_url = urllib.parse.quote(url)
    links = {
        "wa": f"https://wa.me/?text={safe_text} {safe_url}",
        "fb": f"https://www.facebook.com/sharer/sharer.php?u={safe_url}",
        "tw": f"https://twitter.com/intent/tweet?text={safe_text}&url={safe_url}",
        "li": f"https://www.linkedin.com/sharing/share-offsite/?url={safe_url}",
        "ig": "https://www.instagram.com/",
        "tt": "https://www.tiktok.com/upload",
        "xhs": "https://www.xiaohongshu.com/explore"
    }
    return links

# === 🧠 核心 AI 逻辑 ===
def build_prompt(mode, language, style_modifier, is_vip, input_type="image"):
    style_recipes = {
        "📝 Detailed (More Words)": "highly detailed description, verbose, analyze every element, focus on textures and lighting",
        "⚡ Concise (Short)": "concise description, brief, to the point, short keywords only",
        "🖍️ Coloring Book (Line Art)": "coloring book page, black and white, clean lines, no shading, white background, thick outlines, vector style",
        "🧱 Claymation (Cute 3D)": "claymation style, plasticine texture, stop motion, soft lighting, 3d render, cute, miniature world, tilt-shift",
        "🎬 Pixar/Disney 3D": "Pixar style 3d render, unreal engine 5, cgsociety, disney animation style, expressive characters, cinematic lighting",
        "✨ Anime / Studio Ghibli": "Studio Ghibli style, anime, hayao miyazaki, pastel colors, cel shaded, breathtaking sky, detailed background",
        "📸 Hyper-Realistic Photo": "hyper-realistic photography, 8k resolution, raw photo, highly detailed, dslr, cinematic lighting, sharp focus",
        "🔳 Vector Flat Art": "flat vector art, minimal, clean geometric shapes, adobe illustrator, white background, corporate art style",
        "🌃 Cyberpunk / Neon": "cyberpunk, neon lights, night city, futuristic, synthwave, purple and blue gradient, cinematic",
        "📜 Vintage Watercolor": "vintage watercolor illustration, beatrix potter style, soft strokes, paper texture, dreamy, storybook"
    }
    vip_negative_prompt = "low quality, ugly, deformed, blurry, extra fingers, bad anatomy, watermark, text, signature, cropped"
    vip_quality_boost = "masterpiece, best quality, 8k resolution, highly detailed, sharp focus, cinematic lighting"
    added_prompt = ""
    if style_modifier and "None" not in style_modifier and "Lock" not in style_modifier:
        recipe = style_recipes.get(style_modifier, "")
        if recipe: added_prompt = f", {recipe}"

    if mode == "Prompt Gacha":
        if input_type == "text":
            if is_vip:
                return f"""
                You are an elite AI art director.
                Task: Turn the user's simple idea into a World-Class Stable Diffusion prompt.
                User Idea: {{INPUT}}
                Target Style: {added_prompt if added_prompt else "high quality"}
                Action:
                1. EXPAND the idea creatively.
                2. INTEGRATE the target style perfectly.
                3. APPEND these quality boosters: "{vip_quality_boost}".
                Output Format: Combine into a single raw prompt string.
                At the very end, append: " --no {vip_negative_prompt}"
                """
            else:
                return f"""
                You are a translator. Task: Translate the user's idea into a simple English prompt for AI generation.
                User Idea: {{INPUT}}
                Target Style: {added_prompt if added_prompt else "standard"}
                Output Format: Single raw prompt string.
                """
        else:
            base = """
            You are an expert AI art prompter. Analyze the image and reverse-engineer it into a Stable Diffusion prompt.
            Strictly output the prompt in these 4 distinct sections (comma separated, English Only):
            1. **Subject**: (Character, object, action)
            2. **Style**: (Art style, medium)
            3. **Environment**: (Background, lighting)
            4. **Quality**: (Tags e.g., masterpiece)
            """
            if added_prompt: base += f" INTEGRATE this style: '{added_prompt}'. "
            base += "Format: Combine into a single raw prompt string."
            if is_vip: base += f" Append ' --no {vip_negative_prompt}' at the end."
            return base
    elif mode == "Storyteller":
        style_instruction = f"Visual Style: {style_modifier}" if style_modifier else "Style: Warm"
        return f"""
        Task: Write a creative children's story in {language} based on the input (300 words).
        Structure: 1. Title 2. Story 3. Moral 4. 🎨 **AI Drawing Prompt**: Create a prompt to generate an illustration for this story in {style_modifier} style.
        Tone: {style_instruction}. Input: {{INPUT}}
        """
    elif mode == "Social Kit":
        return f"""
        Write a viral social post in {language} based on the input. 
        Structure: Hook, Content, 15+ Hashtags. 
        Tone/Style: {style_modifier}. Input: {{INPUT}}
        """
    return "Describe input."

def process_and_save(inputs, mode, output_lang, style, is_vip, ui_text, input_type):
    genai.configure(api_key=api_key)
    # 🌟 关键修正：使用您列表中排名第一的 Gemini 2.5 Flash！
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    loading_messages = ["AI is dreaming...", "Analyzing...", "Extracting magic...", "Polishing words..."]
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_items = len(inputs)

    for i, item in enumerate(inputs):
        if is_vip:
            msg = get_text(ui_text, "processing_vip").format(current=i+1, total=total_items)
            status_text.markdown(msg)
            time.sleep(1.0)
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
            if "block" in str(content).lower(): content = "⚠️ Safety Block: Content filtered."
            st.session_state['results'].append({
                "filename": filename, "content": content, "image": img_obj, "mode": mode
            })
            if not is_vip: st.session_state['usage_count'] += 1
        except Exception as e:
            st.error(f"Error: {e}")
        progress_bar.progress((i + 1) / total_items)

    time.sleep(0.5)
    progress_bar.progress(100)
    status_text.success(get_text(ui_text, "complete"))
    time.sleep(1)
    status_text.empty()
    try:
        log_user = st.session_state.get('user_email', 'Anonymous')
        if is_vip: log_user += " (VIP)"
        log_msg = f"🚀 **Usage**\n👤 {log_user}\n⚙️ {mode}\n📄 {len(inputs)} Items"
        if len(inputs) > 1 or is_vip:
            send_telegram_msg("System", log_user, log_msg)
    except:
        pass

# ==========================================
# 4. 侧边栏
# ==========================================
with st.sidebar:
    lang_list = list(TRANSLATIONS.keys())
    ui_lang = st.selectbox("🌐 Interface Language", lang_list, index=0)
    t = TRANSLATIONS.get(ui_lang, TRANSLATIONS["English"])
    st.markdown(f"## 🔮 {get_text(t, 'app_title')}")
    
    with st.expander(get_text(t, 'vip_access'), expanded=True):
        vip_code = st.text_input(get_text(t, 'activation_code'), type="password")
        st.markdown("""
        <div style="font-size: 0.75em; color: #555; background-color: #e2e3e5; padding: 8px; border-radius: 5px; margin-bottom: 10px;">
            🛡️ <b>Secure Session:</b> This workspace is personalized for you.
        </div>
        """, unsafe_allow_html=True)
        if vip_code: vip_code = vip_code.strip()
        is_vip = vip_code in st.secrets.get("MANUAL_CODES", ["demo"])
        daily_limit = 200 if is_vip else 3
        remaining = daily_limit - st.session_state['usage_count']
        if remaining < 0: remaining = 0
        if is_vip:
            st.success(get_text(t, 'vip_active'))
            st.caption(f"📊 {st.session_state['usage_count']} / {daily_limit}")
        else:
            st.info(get_text(t, 'free_limit_info').format(remaining=remaining))
            st.markdown("""
            <div style="text-align: center; margin-bottom: 10px;">
                <span style="text-decoration: line-through; color: #888; font-size: 0.9em;">$39.90</span>
                <span style="color: #FF4B4B; font-weight: bold; font-size: 1.2em; margin-left: 5px;">$12.90</span>
            </div>
            """, unsafe_allow_html=True)
            # ⚠️ 记得换成您的支付链接
            buy_url = "https://your-shop.lemonsqueezy.com/buy/xxxx" 
            st.markdown(f"""
            <a href="{buy_url}" target="_blank">
                <button style="width:100%; background: linear-gradient(90deg, #FF4B4B 0%, #FF6B6B 100%); color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">
                    {get_text(t, 'upgrade_btn')}
                </button>
            </a>
            <p style="text-align:center; font-size:0.7em; color:#666; margin-top:5px;">{get_text(t, 'limited_offer')}</p>
            """, unsafe_allow_html=True)

    st.markdown("---")
    if not is_vip:
        st.markdown(f"### {get_text(t, 'get_started')}")
        st.caption(get_text(t, 'email_hint'))
        email = st.text_input("Email", value=st.session_state['user_email'])
        if email: st.session_state['user_email'] = email
        
    st.markdown(f"### {get_text(t, 'config')}")
    input_method = st.radio(get_text(t, "input_method_label"), ["upload", "text"], 
                            format_func=lambda x: get_text(t, "input_upload") if x == "upload" else get_text(t, "input_text"))
    mode = st.radio(get_text(t, 'mode_label'), ["Prompt Gacha", "Storyteller", "Social Kit"])
    output_lang = st.selectbox(get_text(t, 'lang_label'), lang_list, index=0)
    
    style_modifier = None
    if is_vip:
        style_options = ["None (Default)", "🖍️ Coloring Book (Line Art)", "🧱 Claymation (Cute 3D)", "🎬 Pixar/Disney 3D", "✨ Anime / Studio Ghibli", "📸 Hyper-Realistic Photo", "🔳 Vector Flat Art", "🌃 Cyberpunk / Neon", "📜 Vintage Watercolor"]
        style_modifier = st.selectbox(get_text(t, 'style_vip_label'), style_options)
    else:
        style_options_free = ["None (Default)", "📝 Detailed (More Words)", "⚡ Concise (Short)", "🔒 Unlock 8+ Pro Styles (VIP Only)"]
        style_modifier = st.selectbox(get_text(t, 'style_free_label'), style_options_free)
        if "Lock" in style_modifier:
            st.warning(get_text(t, 'style_lock_warning'))
            style_modifier = "None (Default)"

    with st.expander(get_text(t, 'faq_title')):
        st.markdown(get_text(t, 'faq_content'))
    st.markdown("---")
    with st.expander(get_text(t, "support_title"), expanded=False):
        st.caption(get_text(t, "support_ticket_label"))
        with st.form(key="support_ticket_form"):
            current_email = st.session_state.get('user_email', "")
            user_email_input = st.text_input(get_text(t, "ticket_email"), value=current_email)
            issue_type = st.selectbox(get_text(t, "ticket_type"), ["🐛 Bug Report", "💳 Billing/Payment", "💡 Feature Request", "Other"])
            user_msg = st.text_area(get_text(t, "ticket_desc"), height=100)
            submit_btn = st.form_submit_button(get_text(t, "ticket_btn"))
            if submit_btn:
                if user_email_input and user_msg:
                    ticket_id = f"#{random.randint(10000, 99999)}"
                    st.success(get_text(t, "ticket_success").format(id=ticket_id))
                    full_msg = f"📌 **Type:** {issue_type}\n🎫 **Ticket:** {ticket_id}\n📝 **Content:** {user_msg}"
                    send_telegram_msg("User", user_email_input, full_msg)

# ==========================================
# 5. 主界面
# ==========================================
st.title(f"🔮 {mode}")
batch_limit = 50 if is_vip else 3
passed_gate = is_vip or (st.session_state['user_email'] != "")
inputs = []
input_type = "image"

if st.session_state['usage_count'] >= daily_limit:
    st.error(get_text(t, 'daily_limit_error').format(current=st.session_state['usage_count'], total=daily_limit))
else:
    if input_method == "upload":
        label = get_text(t, 'upload_label').format(limit=batch_limit)
        uploaded_files = st.file_uploader(label, type=["jpg","png","webp"], accept_multiple_files=True)
        if uploaded_files: inputs = uploaded_files
        input_type = "image"
    else:
        user_text = st.text_area(get_text(t, "text_area_label"), height=150)
        if user_text: inputs = [user_text] 
        input_type = "text"

if inputs:
    if not passed_gate:
        st.warning(get_text(t, 'email_warning'))
    else:
        if st.button(get_text(t, 'generate_btn')):
            potential_usage = st.session_state['usage_count'] + len(inputs)
            if potential_usage > daily_limit:
                allowed_count = daily_limit - st.session_state['usage_count']
                st.warning(get_text(t, 'credit_warning').format(count=allowed_count))
                inputs = inputs[:allowed_count]
            elif len(inputs) > batch_limit:
                st.warning(get_text(t, 'batch_warning').format(limit=batch_limit))
                inputs = inputs[:batch_limit]
            st.caption("⚠️ Please do not refresh the page.")
            process_and_save(inputs, mode, output_lang, style_modifier, is_vip, t, input_type)
            st.rerun()

# ==========================================
# 6. 结果展示
# ==========================================
if st.session_state['results']:
    st.markdown("---")
    if st.button(get_text(t, 'clear_btn')):
        st.session_state['results'] = []
        st.rerun()
    for item in reversed(st.session_state['results']):
        c = item['content']
        n = item['filename']
        m = item['mode']
        img = item['image']
        with st.container():
            st.markdown(f"<div class='result-card'>", unsafe_allow_html=True)
            cols = st.columns([1, 3])
            with cols[0]:
                if img: st.image(img, use_container_width=True)
                else:
                    st.markdown("## ✍️ Idea")
                    st.info(n.split('_')[-1] if '_' in n else "Text")
                st.caption(n)
            with cols[1]:
                if m == "Prompt Gacha": st.code(c, language="markdown")
                else: 
                    st.markdown(c)
                    with st.expander(get_text(t, 'copy_text')): st.code(c, language=None)
                if is_vip:
                    st.markdown("---")
                    if m == "Social Kit":
                        links = generate_share_links(c)
                        st.caption(get_text(t, 'share_title'))
                        st.markdown(f"""
                        <a href='{links['wa']}' target='_blank' class='share-btn btn-wa'>WhatsApp</a>
                        <a href='{links['fb']}' target='_blank' class='share-btn btn-fb'>Facebook</a>
                        <a href='{links['tw']}' target='_blank' class='share-btn btn-tw'>X (Twitter)</a>
                        <a href='{links['li']}' target='_blank' class='share-btn btn-li'>LinkedIn</a>
                        """, unsafe_allow_html=True)
                    if m == "Storyteller":
                        pdf = create_pdf(img, c, n)
                        st.download_button(get_text(t, 'download_pdf'), pdf, f"{n}.pdf", "application/pdf")
                else:
                    st.markdown("---")
                    st.markdown(f"<p class='delay-msg'>{get_text(t, 'upsell_msg')}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader(get_text(t, 'export_title'))
    txt_buffer = ""
    csv_buffer = "Filename,Mode,Content\n"
    for item in st.session_state['results']:
        n = item['filename']
        c = item['content'].replace('"', '""')
        m = item['mode']
        txt_buffer += f"=== [{m}] {n} ===\n{item['content']}\n\n"
        csv_buffer += f'"{n}","{m}","{c}"\n'
    col1, col2 = st.columns([1, 1])
    if is_vip:
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w") as zf:
            zf.writestr("all_results.txt", txt_buffer)
            zf.writestr("export_data.csv", csv_buffer)
        col1.download_button(get_text(t, 'download_zip'), zip_buf.getvalue(), "visionprompter_vip.zip", "application/zip", use_container_width=True, type="primary")
        col1.caption(get_text(t, 'zip_desc'))
    else:
        col1.download_button(get_text(t, 'download_txt'), txt_buffer, "results.txt", "text/plain", use_container_width=True)
        col1.caption(get_text(t, 'txt_desc'))

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #aaa; font-size: 0.8em; line-height: 1.5;">
    <b>{get_text(t, 'footer_rights')}</b><br>
    {get_text(t, 'footer_disclaimer')}<br>
    <span style="font-size: 0.8em; opacity: 0.6; font-family: monospace;">System Version: v2.5 (International Edition)</span>
</div>
""", unsafe_allow_html=True)
