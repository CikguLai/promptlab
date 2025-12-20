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
# 1. 核心配置 (Configuration)
# ==========================================
SYSTEM_VERSION = "v2.5 (International Edition)"
COPYRIGHT_OWNER = "Cikgu Lai"

# 🎨 画风配方字典 (AI 的脑子 - 包含 12 种风格)
STYLE_RECIPES = {
    "None (Default)": "",
    "🖍️ Coloring Book": "coloring book page, black and white, clean lines, no shading, white background, thick outlines, vector style, kids illustration",
    "🧱 Claymation 3D": "claymation style, plasticine texture, stop motion, soft lighting, 3d render, cute, miniature world, tilt-shift photography",
    "🎬 Pixar/Disney": "Pixar style 3d render, unreal engine 5, cgsociety, disney animation style, expressive characters, cinematic lighting, 8k",
    "✨ Anime Ghibli": "Studio Ghibli style, anime, hayao miyazaki, pastel colors, cel shaded, breathtaking sky, detailed background, hand drawn",
    "📸 Hyper-Realistic": "hyper-realistic photography, 8k resolution, raw photo, highly detailed, dslr, cinematic lighting, sharp focus, f/1.8",
    "🔳 Vector Flat Art": "flat vector art, minimal, clean geometric shapes, adobe illustrator, white background, corporate art style, vibrant colors",
    "🌃 Cyberpunk": "cyberpunk, neon lights, night city, futuristic, synthwave, purple and blue gradient, cinematic, blade runner vibe",
    "📜 Watercolor": "vintage watercolor illustration, beatrix potter style, soft strokes, paper texture, dreamy, storybook, wet on wet",
    "🔮 3D Isometric": "3d isometric render, cute, blender 3d, soft lighting, pastel colors, orthographic view, detailed",
    "👾 Pixel Art": "pixel art, 16-bit, retro game style, vibrant colors, clean pixels",
    "✏️ Sketch": "pencil sketch, graphite, rough lines, academic drawing, white background"
}

# 🌍 15国语言字典
TRANSLATIONS = {
    "English": {
        "nav_home": "🚀 Workbench", "nav_history": "📂 Archive", "nav_vip": "💎 Pro Plan", "nav_help": "💁 Support",
        "app_title": "VisionPrompter AI", "hero_subtitle": "Enterprise-grade AI Prompt Engineering.",
        "vip_active": "✅ PRO Active", "free_limit_info": "🔓 Daily Limit: {remaining}",
        "upgrade_btn": "👉 Get Lifetime Access", "config": "⚙️ Control Panel",
        "input_upload": "📷 Image Analysis", "input_text": "✍️ Creative Writing",
        "style_vip_label": "🎨 Art Style (Pro):", "generate_btn": "✨ Generate Magic",
        "share_title": "🚀 Share to Social:", "welcome_msg": "👈 **Start on the left**",
        "processing_vip": "⚡ **VIP Speed:** Processing...", "processing_free": "⏳ **Queue:** Waiting...",
        "copy_hint": "💡 Tip: Click the copy icon 📄 in the top-right of the box above.",
        "download_pdf": "📄 Download PDF Report",
        "footer_disclaimer": "Disclaimer: AI generated content. Not legal advice.",
        "faq_title": "📚 FAQ", "faq_content": "**Q: Images?** No, Prompts.\n**Q: Monthly?** No, Lifetime.\n**Q: No Code?** Check Spam."
    },
    "Chinese (Simplified)": {
        "nav_home": "🚀 工作台", "nav_history": "📂 归档数据", "nav_vip": "💎 会员计划", "nav_help": "💁 服务中心",
        "app_title": "VisionPrompter 视觉大师", "hero_subtitle": "企业级提示词工程引擎。",
        "vip_active": "✅ 专业版已激活", "free_limit_info": "🔓 今日额度: {remaining}",
        "upgrade_btn": "👉 立即获取终身使用权", "config": "⚙️ 控制面板",
        "input_upload": "📷 图片分析", "input_text": "✍️ 创意文本",
        "style_vip_label": "🎨 专业风格 (VIP):", "generate_btn": "✨ 立即生成",
        "share_title": "🚀 一键分享:", "welcome_msg": "👈 **请在左侧面板开始**",
        "processing_vip": "⚡ **VIP 极速通道:** 处理中...", "processing_free": "⏳ **免费排队:** 等待中...",
        "copy_hint": "💡 提示：点击文本框右上角的复制图标 📄。",
        "download_pdf": "📄 下载 PDF 报告",
        "footer_disclaimer": "免责声明：AI 生成内容仅供参考。",
        "faq_title": "📚 常见问题", "faq_content": "**Q: 生成图片？** 不，提示词。\n**Q: 月费？** 不，终身买断。\n**Q: 没码？** 查垃圾邮件。"
    },
    "Chinese (Traditional)": {
        "nav_home": "🚀 工作台", "nav_history": "📂 歸檔數據", "nav_vip": "💎 會員計劃", "nav_help": "💁 服務中心",
        "app_title": "VisionPrompter 視覺大師", "hero_subtitle": "企業級提示詞工程引擎。",
        "vip_active": "✅ 專業版已激活", "free_limit_info": "🔓 今日額度: {remaining}",
        "upgrade_btn": "👉 獲取終身使用權", "config": "⚙️ 控制面板",
        "input_upload": "📷 圖片分析", "input_text": "✍️ 創意文本",
        "style_vip_label": "🎨 專業風格 (VIP):", "generate_btn": "✨ 立即生成",
        "share_title": "🚀 一鍵分享:", "welcome_msg": "👈 **請在左側面板開始**",
        "processing_vip": "⚡ **VIP 極速:** 處理中...", "processing_free": "⏳ **免費排隊:** 等待中...",
        "copy_hint": "💡 提示：點擊文本框右上角的複製圖標 📄。",
        "download_pdf": "📄 下載 PDF 報告",
        "footer_disclaimer": "免責聲明：AI 生成內容僅供參考。",
        "faq_title": "📚 常見問題", "faq_content": "**Q: 生成圖片？** 不，提示詞。\n**Q: 月費？** 不，終身買斷。\n**Q: 沒碼？** 查垃圾郵件。"
    },
    "Malay": {
        "nav_home": "🚀 Meja Kerja", "nav_history": "📂 Arkib", "nav_vip": "💎 Pelan PRO", "nav_help": "💁 Bantuan",
        "app_title": "VisionPrompter AI", "hero_subtitle": "Enjin Prompt AI Gred Enterprise.",
        "vip_active": "✅ PRO Aktif", "free_limit_info": "🔓 Had Harian: {remaining}",
        "upgrade_btn": "👉 Dapatkan Akses Seumur Hidup", "config": "⚙️ Panel Kawalan",
        "input_upload": "📷 Analisis Gambar", "input_text": "✍️ Teks Kreatif",
        "style_vip_label": "🎨 Gaya Pro (VIP):", "generate_btn": "✨ Mula Jana",
        "share_title": "🚀 Kongsi:", "welcome_msg": "👈 **Mula di kiri**",
        "processing_vip": "⚡ **Laju VIP:** Memproses...", "processing_free": "⏳ **Giliran:** Menunggu...",
        "copy_hint": "💡 Tip: Tekan ikon salin 📄 di atas.",
        "download_pdf": "📄 Laporan PDF",
        "footer_disclaimer": "Penafian: Kandungan dijana AI.",
        "faq_title": "📚 Soalan Lazim", "faq_content": "**Q: Gambar?** Tidak, Prompt.\n**Q: Bulanan?** Tidak, Sekali Bayar.\n**Q: Tiada kod?** Semak Spam."
    },
    # === 其他语言占位符 (确保菜单显示所有国家) ===
    "Indonesian": {}, "Vietnamese": {}, "Thai": {}, "Japanese": {}, "Korean": {}, 
    "Arabic": {}, "Russian": {}, "Spanish": {}, "French": {}, "German": {}, "Portuguese": {}
}

def get_text(t, key):
    return t.get(key, TRANSLATIONS["English"].get(key, key))

# ==========================================
# 2. 系统初始化 (System Init)
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
if 'last_used_time' not in st.session_state: st.session_state['last_used_time'] = 0

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Critical: GOOGLE_API_KEY missing.")
    st.stop()
api_key = st.secrets["GOOGLE_API_KEY"]

# === ✨ CSS 美化 (Dashboard V5.3 样式 - 含彩色按钮) ===
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .result-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #eee; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    
    /* 基础分享按钮样式 */
    .share-btn { 
        display: inline-block; 
        padding: 5px 10px; 
        border-radius: 4px; 
        color: white !important; 
        text-decoration: none !important; 
        margin-right: 6px; 
        margin-bottom: 6px;
        font-size: 0.8em; 
        font-weight: bold; 
        transition: opacity 0.3s;
    }
    .share-btn:hover { opacity: 0.8; }
    
    /* 社交平台颜色 */
    .wa { background-color: #25D366; } 
    .fb { background-color: #1877F2; } 
    .tw { background-color: #000000; }
    .xhs { background-color: #FF2442; } /* 小红书红 */
    .ig { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); } /* Instagram 渐变 */
    .tt { background-color: #000000; border: 1px solid #333; } /* TikTok 黑 */

    .footer-box { text-align: center; color: #aaa; font-size: 0.75em; margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee; }
    .copy-hint { font-size: 0.8em; color: #888; font-style: italic; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心功能函数 (Functional Core)
# ==========================================

# 📡 Telegram 监控
def send_telegram_msg(name, email, msg):
    if "telegram" in st.secrets:
        token = st.secrets["telegram"]["token"]
        chat_id = st.secrets["telegram"]["chat_id"]
        text = f"🔔 **{name}**\n📧 {email}\n📝 {msg}"
        try:
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
        except: pass

# 📱 社媒分享按钮 (6大平台全覆盖)
def render_share_buttons(text, ui_text):
    safe_text = urllib.parse.quote(text[:200] + "...")
    url = urllib.parse.quote("https://app.cikgulai.com") # ⚠️ 确保这是您的真实域名
    
    st.markdown(f"""
    <div style="margin-top:15px; margin-bottom:15px;">
        <p style="font-size:0.9em; color:#555; font-weight:bold; margin-bottom:8px;">{get_text(ui_text, 'share_title')}</p>
        
        <a href="https://wa.me/?text={safe_text} {url}" target="_blank" class="share-btn wa">WhatsApp</a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={url}" target="_blank" class="share-btn fb">Facebook</a>
        <a href="https://twitter.com/intent/tweet?text={safe_text}&url={url}" target="_blank" class="share-btn tw">X (Twitter)</a>
        
        <br>
        
        <a href="https://www.xiaohongshu.com/explore" target="_blank" class="share-btn xhs" title="Copy text then open">小红书 (XHS)</a>
        <a href="https://www.instagram.com/" target="_blank" class="share-btn ig" title="Copy text then open">Instagram</a>
        <a href="https://www.tiktok.com/upload" target="_blank" class="share-btn tt" title="Copy text then open">TikTok</a>
        
        <p style="font-size:0.7em; color:#999; margin-top:5px;">
            * For IG/TikTok/XHS: Please copy text first 📋
        </p>
    </div>
    """, unsafe_allow_html=True)

# 📄 PDF 生成 (精确签名 + 版权)
def create_pdf(image, text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(190, 10, txt="VisionPrompter Report", ln=1, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(190, 10, txt=f"Ref: {filename}", ln=1, align='C')
    pdf.ln(5)
    if image:
        try:
            with io.BytesIO() as output:
                image.save(output, format="JPEG")
                pdf.image(output, x=15, y=35, w=180)
                pdf.ln(105)
        except: pdf.cell(190, 10, txt="[Image Error]", ln=1)
    pdf.set_font("Arial", size=11)
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, safe_text)
    pdf.ln(15)
    pdf.set_draw_color(200, 200, 200); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    # 获取用户身份
    user = st.session_state.get('user_email', '')
    if not user: user = "Verified VIP Member"
    
    pdf.set_font("Arial", size=8, style='I'); pdf.set_text_color(128, 128, 128)
    date_str = time.strftime('%Y-%m-%d')
    footer = f"Generated by VisionPrompter ({SYSTEM_VERSION}) | Licensed to: {user} | Date: {date_str} | {COPYRIGHT_OWNER}"
    pdf.cell(0, 10, txt=footer, ln=1, align='R')
    return pdf.output(dest='S').encode('latin-1')

# 🧠 AI 逻辑 (风格注入 + 道德价值观)
def build_prompt(mode, language, style_name, is_vip, input_type="image"):
    style_prompt = STYLE_RECIPES.get(style_name, "")
    vip_boost = "masterpiece, best quality, 8k, highly detailed" if is_vip else ""
    
    if mode == "Prompt Gacha":
        if input_type == "text":
            return f"""
            Role: World-class AI Art Director.
            Task: Convert the user's idea ({language}) into a professional Stable Diffusion prompt (English).
            User Idea: {{INPUT}}
            Target Style: {style_prompt}
            Quality Boosters: {vip_boost}
            Output: A single, raw prompt string.
            """
        else:
            return f"""
            Role: Expert Image Analyst.
            Task: Analyze this image and reverse-engineer a prompt to recreate it.
            Style Focus: {style_prompt}
            Quality Boosters: {vip_boost}
            Output: Subject, Art Style, Lighting, Camera Settings.
            """
    elif mode == "Storyteller":
        return f"""
        Task: Write a creative story for children (Age 5-8) in {language}.
        Input Idea: {{INPUT}}
        
        Strict Structure:
        1. 📖 **Title**
        2. 📝 **Story** (approx 200 words, engaging)
        3. 🌟 **Moral Value** (Explain the lesson learned)
        4. 🎨 **AI Drawing Prompt** (English prompt to generate an illustration for this story, style: {style_name})
        """
    elif mode == "Social Kit":
        return f"Write a viral social media post in {language}. Include Hook, Body, and 10 Hashtags. Input: {{INPUT}}"
    
    return "Process input."

def process_and_save(inputs, mode, output_lang, style, is_vip, ui_text, input_type):
    # 🛡️ 防滥用冷却 (VIP 2s, Free 5s)
    current_time = time.time()
    last_used = st.session_state.get('last_used_time', 0)
    cooldown = 2 if is_vip else 5
    if current_time - last_used < cooldown:
        st.warning(f"⏳ Please wait {cooldown}s."); st.stop()
    st.session_state['last_used_time'] = current_time

    # 🚀 启动 Gemini 2.5 Flash
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_items = len(inputs)

    # 📡 发送监控通知到 Telegram
    user_id = st.session_state.get('user_email', 'VIP_User') if is_vip else st.session_state.get('user_email', 'Guest')
    send_telegram_msg("Usage Alert", user_id, f"Running {mode} ({len(inputs)} items)")

    for i, item in enumerate(inputs):
        msg_key = "processing_vip" if is_vip else "processing_free"
        status_text.markdown(get_text(ui_text, msg_key))
        
        try:
            base_prompt = build_prompt(mode, output_lang, style, is_vip, input_type)
            if input_type == "text":
                final_prompt = base_prompt.replace("{{INPUT}}", item)
                response = model.generate_content(final_prompt)
                filename = f"Idea_{int(time.time())}_{i}" 
                img_obj = None 
            else:
                img_obj = Image.open(item)
                response = model.generate_content([base_prompt, img_obj])
                filename = item.name
            
            st.session_state['results'].append({"filename": filename, "content": response.text, "image": img_obj, "mode": mode})
            if not is_vip: st.session_state['usage_count'] += 1
            
        except Exception as e:
            st.error(f"Error: {e}")
        
        progress_bar.progress((i + 1) / total_items)
    
    progress_bar.progress(100)
    status_text.success("✅ Done!")
    time.sleep(1)
    status_text.empty()

# ==========================================
# 4. 侧边栏 (Sidebar)
# ==========================================
with st.sidebar:
    lang_list = list(TRANSLATIONS.keys())
    ui_lang = st.selectbox("🌐 Language", lang_list, index=0)
    t = TRANSLATIONS.get(ui_lang, TRANSLATIONS["English"])
    
    st.divider()
    vip_code = st.text_input(get_text(t, 'activation_code'), type="password")
    if vip_code: vip_code = vip_code.strip()
    is_vip = vip_code in st.secrets.get("MANUAL_CODES", ["demo"])
    
    if is_vip:
        st.success(f"🎉 {get_text(t, 'vip_active')}")
        daily_limit = 200
    else:
        st.info("👤 Guest")
        email = st.text_input("Email", value=st.session_state['user_email'])
        if email: st.session_state['user_email'] = email
        daily_limit = 3
        remaining = daily_limit - st.session_state['usage_count']
        if remaining < 0: remaining = 0
        st.caption(get_text(t, 'free_limit_info').format(remaining=remaining))
        # ⚠️ 请将此处链接改为您的 LemonSqueezy 真实链接
        st.markdown(f"<a href='https://your-shop.lemonsqueezy.com' target='_blank'><button style='width:100%;padding:10px;background:#FF4B4B;color:white;border:none;border-radius:5px;cursor:pointer;'>{get_text(t, 'upgrade_btn')}</button></a>", unsafe_allow_html=True)

# ==========================================
# 5. 主界面 (Dashboard UI)
# ==========================================
st.markdown(f"<h2>{get_text(t, 'app_title')} <span style='font-size:0.4em;color:#FF4B4B;vertical-align:middle'>PRO</span></h2>", unsafe_allow_html=True)
st.caption(get_text(t, 'hero_subtitle'))

tab_home, tab_history, tab_vip, tab_help = st.tabs([get_text(t, "nav_home"), get_text(t, "nav_history"), get_text(t, "nav_vip"), get_text(t, "nav_help")])

# --- Tab 1: Workbench ---
with tab_home:
    col_input, col_result = st.columns([4, 6], gap="large")
    
    with col_input:
        st.markdown(f"### {get_text(t, 'config')}")
        input_method = st.radio("Input:", ["upload", "text"], format_func=lambda x: get_text(t, "input_upload") if x == "upload" else get_text(t, "input_text"))
        mode = st.selectbox("Mode:", ["Prompt Gacha", "Storyteller", "Social Kit"])
        output_lang = st.selectbox("Output:", lang_list, index=0)
        
        # 风格选择器 (VIP 才有完整配方)
        if is_vip:
            style_options = list(STYLE_RECIPES.keys())
            style_modifier = st.selectbox(get_text(t, 'style_vip_label'), style_options)
        else:
            style_modifier = st.selectbox("Style:", ["None", "Detailed", "Concise", "🔒 Unlock Pro Styles"])
        
        st.divider()
        
        batch_limit = 50 if is_vip else 3
        passed_gate = is_vip or (st.session_state['user_email'] != "")
        inputs = []
        
        if st.session_state['usage_count'] >= daily_limit:
            st.error("⛔ Limit Reached")
        else:
            if input_method == "upload":
                label = f"Upload (Max {batch_limit})"
                uploaded_files = st.file_uploader(label, type=["jpg","png","webp"], accept_multiple_files=True)
                if uploaded_files: inputs = uploaded_files
                current_input_type = "image"
            else:
                user_text = st.text_area("Input Text", height=150)
                if user_text: inputs = [user_text] 
                current_input_type = "text"

            if inputs and passed_gate:
                if st.button(get_text(t, 'generate_btn'), type="primary", use_container_width=True):
                    process_and_save(inputs, mode, output_lang, style_modifier, is_vip, t, current_input_type)
                    st.rerun()
            elif inputs and not passed_gate:
                st.warning("🔒 Login Required")

    with col_result:
        if st.session_state['results']:
            latest = st.session_state['results'][-1]
            st.markdown(f"### 🎉 Result")
            with st.container():
                st.markdown(f"<div class='result-card'>", unsafe_allow_html=True)
                if latest['image']: st.image(latest['image'], use_container_width=True)
                
                # 结果展示区 + 复制提示
                st.code(latest['content'], language="markdown")
                st.markdown(f"<p class='copy-hint'>{get_text(t, 'copy_hint')}</p>", unsafe_allow_html=True)
                
                # ✅ 6大平台分享按钮
                render_share_buttons(latest['content'], t)
                
                # VIP 专属 PDF 下载
                if is_vip:
                    pdf_bytes = create_pdf(latest['image'], latest['content'], latest['filename'])
                    st.download_button(get_text(t, 'download_pdf'), pdf_bytes, f"{latest['filename']}.pdf", "application/pdf", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:center;padding:50px;color:#aaa;border:2px dashed #ddd;border-radius:10px;'><h3>👋</h3><p>{get_text(t, 'welcome_msg')}</p></div>", unsafe_allow_html=True)

# --- Tab 2: History ---
with tab_history:
    if st.button("🗑️ Clear All"):
        st.session_state['results'] = []
        st.rerun()
    
    txt_buffer = ""
    for item in st.session_state['results']:
        txt_buffer += f"=== {item['filename']} ===\n{item['content']}\n\n"
    st.download_button("📄 Download All (.txt)", txt_buffer, "archive.txt")
    
    for item in reversed(st.session_state['results']):
        with st.expander(f"📄 {item['filename']} ({item['mode']})"):
            if item['image']: st.image(item['image'], width=200)
            st.code(item['content'])

# --- Tab 3 & 4 (VIP & Help) ---
with tab_vip:
    st.info(f"Current Plan: {'**Enterprise VIP**' if is_vip else 'Free Guest'}")
    if not is_vip: st.markdown("### Benefits:\n* ⚡ Instant Speed\n* 📦 Batch 50\n* 🎨 12 Pro Styles\n* 📄 PDF Reports")

with tab_help:
    st.markdown(f"### {get_text(t, 'faq_title')}")
    st.markdown(get_text(t, 'faq_content'))
    st.markdown("---")
    st.markdown("### ❓ Need more help?")
    with st.form("ticket"):
        email = st.text_input("Email", value=st.session_state['user_email'])
        desc = st.text_area("Message")
        if st.form_submit_button("Submit Ticket"):
            st.success("Ticket Sent!")
            send_telegram_msg("Support Ticket", email, desc)

# ==========================================
# 6. 页脚 (Footer) - 法律声明 & 版权
# ==========================================
st.markdown(f"""
<div class="footer-box">
    <b>{SYSTEM_VERSION}</b><br>
    {get_text(t, 'footer_disclaimer')}<br>
    &copy; 2025 {COPYRIGHT_OWNER}. All Rights Reserved.
</div>
""", unsafe_allow_html=True)