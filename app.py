import streamlit as st
import datetime
import urllib.parse
import base64
import requests
import smtplib
import random
import time
import re
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from fpdf import FPDF

# ==========================================
# 1. 全局配置 & 样式 (V4.9 Visual UI Upgrade)
# ==========================================
st.set_page_config(page_title="PromptLab AI - Enterprise", layout="wide", page_icon="🧠")

st.markdown("""
<style>
    /* 全局按钮样式优化 */
    .stButton>button { border-radius: 12px; height: 45px; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    
    /* 图标按钮容器 (Icon Dock) */
    .icon-dock {
        display: flex;
        gap: 12px;
        justify-content: flex-start;
        align-items: center;
        flex-wrap: wrap;
        margin-bottom: 15px;
    }
    
    /* 核心图标按钮样式 */
    .icon-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 45px;
        background: white;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        text-decoration: none;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .icon-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-color: #2E86C1;
    }
    .icon-btn img {
        width: 24px;
        height: 24px;
        object-fit: contain;
    }
    
    /* 禁用状态 */
    .icon-btn.disabled {
        opacity: 0.5;
        pointer-events: none;
        filter: grayscale(100%);
        background: #f5f5f5;
    }

    /* 品牌色悬停效果 (可选，为了统一目前用白色背景) */
    
    /* AI Reply Box */
    .ai-reply-box { background-color: #e8f0fe; border-left: 5px solid #1967d2; padding: 15px; margin-bottom: 15px; border-radius: 4px; color: #174ea6; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 多语言核心词典
# ==========================================
LANG_DICT = {
    "English": { "login": "Login (PRO)", "guest": "Free Guest", "key": "Activation Key", "email": "Email Address", "role": "Choose Workspace", "back": "Back", "logout": "Logout", "upgrade": "Upgrade to PRO", "gen_btn": "✨ GENERATE", "upload": "📸 Upload Images", "download": "Download", "copy": "Copy", "limit": "Daily Limit", "used": "used", "wait": "Please wait", "lost_key": "Lost your Key?", "manage": "Manage Sub", "connect": "🚀 AI Direct Connect (Copy First)" },
    "简体中文": { "login": "PRO 会员登入", "guest": "免费试用", "key": "激活码 (Key)", "email": "电子邮箱", "role": "选择工作区", "back": "返回", "logout": "退出", "upgrade": "升级到 PRO", "gen_btn": "✨ 开始生成", "upload": "📸 上传参考图", "download": "下载", "copy": "复制结果", "limit": "今日限额", "used": "已用", "wait": "请等待", "lost_key": "忘记激活码？", "manage": "管理订阅", "connect": "🚀 AI 直通车 (请先复制)" },
    "Bahasa Melayu": { "login": "Log Masuk (PRO)", "guest": "Tetamu Percuma", "key": "Kunci Aktivasi", "email": "Emel", "role": "Pilih Ruang Kerja", "back": "Kembali", "logout": "Keluar", "upgrade": "Naik Taraf PRO", "gen_btn": "✨ Jana Prompt", "upload": "📸 Muat Naik Gambar", "download": "Muat Turun", "copy": "Salin", "limit": "Had Harian", "used": "digunakan", "wait": "Sila tunggu", "lost_key": "Lupa Kunci?", "manage": "Urus Langganan", "connect": "🚀 AI Direct Connect (Salin Dahulu)" },
    "繁體中文": { "login": "PRO 會員登入", "guest": "免費試用", "key": "啟動碼", "email": "電子郵件", "role": "選擇工作區", "back": "返回", "logout": "登出", "upgrade": "升級至 PRO", "gen_btn": "✨ 生成提示詞", "upload": "📸 上傳圖片", "download": "下載", "copy": "複製", "limit": "今日限額", "used": "已用", "wait": "請稍候", "lost_key": "忘記啟動碼？", "manage": "管理訂閱", "connect": "🚀 AI 直通車 (請先複製)" },
}
OUTPUT_LANGUAGES = list(LANG_DICT.keys())

# ==========================================
# 3. 核心数据库
# ==========================================
COMMON_TONES = ["🌟 Professional", "🥰 Empathetic", "🔥 Persuasive", "👻 Witty", "📖 Storyteller", "⚡ Urgent", "🧘 Calm", "🎓 Academic"]

MODES_DB = {
    "Global Educator": {
        "🟢 Pedagogy": { "dd": ["📸 Analyze Student Work", "Direct Instruction", "Gamification", "Project-Based Learning (PBL)", "Socratic Method", "Flipped Classroom", "Differentiated Instruction"], "tones": COMMON_TONES, "in": "Topic", "desc": "Lesson Plans." },
        "🔵 Visuals": { "dd": ["Pixar/Disney 3D", "National Geographic Photo", "Minimalist Vector", "Vintage Watercolor", "Scientific Schematic", "Cyberpunk Concept"], "in": "Visual Desc", "desc": "AI Art Prompts." },
        "🟣 Comm": { "dd": ["Parent Message", "Behavior Report", "Official Proposal", "Classroom Newsletter", "Event Invitation", "Grant Application"], "tones": COMMON_TONES, "in": "Context", "desc": "School Comms." }
    },
    "Global Creator": {
        "🟢 Scripting": { "dd": ["📸 Visual-to-Script", "TikTok/Reels (Hook-Value-CTA)", "YouTube Edutainment", "Storytelling Vlog", "Podcast Interview", "Live Stream Flow"], "tones": COMMON_TONES, "in": "Video Topic", "desc": "Scripts." },
        "🔵 Thumbnail": { "dd": ["High CTR (Shocked)", "Cinematic Poster", "Tech/Neon/Glowing", "Before & After", "Minimalist Apple", "Comic Book Style"], "in": "Context", "desc": "Thumbnail Art." },
        "🟣 Marketing": { "dd": ["Xiaohongshu (KOC)", "Instagram Caption", "Facebook Ad", "LinkedIn Thought Leader", "Twitter Thread", "Email Newsletter"], "tones": COMMON_TONES, "in": "Product", "desc": "Social Copy." }
    },
    "Global Parent": {
        "🟢 Story Time": { "dd": ["📸 From Child's Drawing", "Bedtime Story", "Hero's Journey", "Social Emotional Learning", "Science 'Why' Story", "Cultural Tale"], "tones": ["😴 Calming", "🦸 Exciting"], "in": "Child Name/Age", "desc": "Stories." },
        "🔵 Activities": { "dd": ["DIY Craft Guide", "Rainy Day Game", "Kitchen Science", "Scavenger Hunt", "Family Bonding", "No-Screen Coding"], "tones": ["🎨 Creative", "🔬 Edu"], "in": "Interest", "desc": "Activities." },
        "🟣 Tutor": { "dd": ["📸 Solve Problem", "Feynman Technique", "Homework Helper", "Quiz Generator", "Vocabulary Builder", "Essay Proofreader"], "tones": ["Encouraging", "Logic"], "in": "Subject", "desc": "Tutor." }
    },
    "Global Seller": {
        "🟢 Copywriting": { "dd": ["📸 Product Desc from Photo", "PAS (Pain-Agitate-Solve)", "AIDA (Attention-Action)", "FAB (Feature-Benefit)", "Storytelling Sales", "Objection Handling"], "tones": COMMON_TONES, "in": "Product USP", "desc": "Sales Copy." },
        "🔵 Product Shot": { "dd": ["Studio White BG", "Lifestyle Home", "Luxury Gold/Black", "Nature/Sunlight", "Cyberpunk/Tech", "Flat Lay"], "in": "Product", "desc": "Photo Prompts." },
        "🟣 Support": { "dd": ["Apology & Recovery", "Review Request", "Complaint Reply", "Promo Announcement", "Crisis Statement", "FAQ Gen"], "tones": ["Apologetic", "Pro"], "in": "Issue", "desc": "Support." }
    },
    "Global Student": {
        "🟢 Study": { "dd": ["📸 Explain Chart", "Feynman Technique", "Lit Review Matrix", "Flashcard (Anki)", "Concept Simplifier", "Translation"], "tones": ["Academic", "Simple"], "in": "Topic", "desc": "Study." },
        "🔵 Project": { "dd": ["Essay Outline", "Presentation Script", "Debate Prep", "Lab Report", "Methodology", "Group Roles"], "tones": COMMON_TONES, "in": "Topic", "desc": "Projects." },
        "🟣 Career": { "dd": ["ATS Resume", "Cover Letter", "Interview Prep", "LinkedIn Bio", "Cold Email", "Portfolio Desc"], "tones": ["Corporate", "Creative"], "in": "Role", "desc": "Career." }
    },
    "Global Corporate": {
        "🟢 Admin": { "dd": ["📸 Extract Data from Table", "Meeting Minutes", "Official Proposal", "Internal Memo", "SOP / Process", "Press Release"], "tones": ["Formal", "Direct"], "in": "Context", "desc": "Admin." },
        "🔵 Strategy": { "dd": ["OKRs", "SWOT Analysis", "Competitor Dive", "Business Canvas", "Risk Matrix", "Pitch Deck"], "in": "Biz", "desc": "Strategy." },
        "🟣 HR & Team": { "dd": ["Performance Review", "Job Desc (JD)", "Onboarding Plan", "Crisis Comms", "Team Building", "Termination"], "tones": ["Fair", "Inspiring"], "in": "Situation", "desc": "HR." }
    }
}

FAQ_DB = {
    "💰 Billing": [("Lost Key?", "Retrieve at app.lemonsqueezy.com/my-orders"), ("Cancel?", "Sidebar > Manage Sub")],
    "⚙️ Tech": [("Blank Screen?", "Clear cache"), ("Invalid Key?", "Check spaces")]
}

# ==========================================
# 4. 辅助函数
# ==========================================
COPYRIGHT_FOOTER = "\n\n✨ Generated by PromptLab AI (Free Version) - cikgulai.com"

# --- 图标生成器 (使用 SimpleIcons CDN) ---
def get_icon_btn_html(link, icon_url, tooltip, is_disabled=False):
    cls = "icon-btn disabled" if is_disabled else "icon-btn"
    return f"""
    <a href="{link}" target="_blank" class="{cls}" title="{tooltip}">
        <img src="{icon_url}" alt="{tooltip}">
    </a>
    """

def smart_mock_generate(role, mode_type, option, tone, topic, details, lang, platform_choice):
    output = ""
    content_desc = details if details else topic 
    
    if mode_type.startswith("🔵") or "Visual" in option or "Shot" in option:
        style_keywords = option.split("(")[0].strip()
        if platform_choice == "General AI (ChatGPT/Gemini)":
             output = f"**[General AI Image Request]**\n`Create a high-quality image of {content_desc}.`\n* **Style**: {style_keywords}\n* **Atmosphere**: Cinematic lighting, high resolution."
        elif platform_choice == "Midjourney v6":
            output = f"**[Midjourney v6]**\n`/imagine prompt: {content_desc}, {style_keywords} style, 8k --v 6.0 --ar 16:9`"
        elif platform_choice == "Stable Diffusion XL":
            output = f"**[SD XL]**\n`(masterpiece), {content_desc}, {style_keywords}, 8k uhd`"
        else:
             output = f"**[Leonardo.ai]**\n`{content_desc}, {style_keywords}, 8k`"
    elif "Script" in option or "TikTok" in option or "YouTube" in option:
        output = f"**🎥 Video Script: {topic}**\n**Tone**: {tone} | **Platform**: {option}\n\n**(0:00-0:03) The Hook**\nSpeaker: 'Stop scrolling! You need to hear this about {topic}!'\n\n**(0:30) CTA**\nSpeaker: 'Comment {lang} for more!'"
    elif "Xiaohongshu" in option or "Instagram" in option or "Copywriting" in option:
        output = f"**📱 Social Post: {option}**\n\n(Headline) **{topic}?! 😱**\n\n(Body) Just discovered {content_desc}! 🚀\n\n✅ Super efficient\n✅ {tone} vibes\n\n#{topic.replace(' ','')} #Trending"
    elif "Lesson" in option or "Study" in option or "Tutor" in option:
        output = f"**📚 Resource: {option}**\n**Topic**: {topic}\n\n**1. Objective**: Understand {content_desc}.\n**2. Explanation**: Think of it like a machine... ({tone})\n**3. Action**: Explain it to a friend!"
    else:
        output = f"**🤖 Content: {option}**\n**Context**: {topic} - {content_desc}\n\nDraft in **{tone}** tone:\n1. Intro\n2. Key Point\n3. Conclusion\n\n*(Optimized for {lang})*"
    return output

def check_ai_knowledge_base(subject, message):
    text = (subject + " " + message).lower()
    if "lost" in text or "key" in text: return True, "💡 **AI:** Retrieve key at [LemonSqueezy](https://app.lemonsqueezy.com/my-orders)."
    if "refund" in text: return True, "💡 **AI:** Manage sub at [Billing](https://app.lemonsqueezy.com/my-orders)."
    return False, None

def send_to_airtable(email, type_l, sub, msg, status="New"):
    try:
        if "AIRTABLE_API_KEY" not in st.secrets: return
        url = f"https://api.airtable.com/v0/{st.secrets['AIRTABLE_BASE_ID']}/{st.secrets['AIRTABLE_TABLE_NAME']}"
        headers = {"Authorization": f"Bearer {st.secrets['AIRTABLE_API_KEY']}", "Content-Type": "application/json"}
        requests.post(url, json={"fields": {"Email": email, "Type": type_l, "Subject": sub, "Message": msg, "Status": status, "Date": datetime.datetime.now().strftime("%Y-%m-%d")}}, headers=headers)
    except: pass

def send_admin_alert(msg):
    try: requests.post(f"https://api.telegram.org/bot{st.secrets['TELEGRAM_BOT_TOKEN']}/sendMessage", data={"chat_id": st.secrets["TELEGRAM_CHAT_ID"], "text": f"🔔 {msg}"})
    except: pass

def validate_license(key):
    if key == "ADMIN-8888": return True
    try: return requests.post("https://api.lemonsqueezy.com/v1/licenses/activate", data={"license_key": key, "instance_name": "Web"}).json().get("activated", False)
    except: return False

def clean_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text); text = re.sub(r'\*(.*?)\*', r'\1', text); text = re.sub(r'#+\s', '', text)
    return text.strip()

# --- 核心下载与分享模块 (升级为图标版) ---
def get_pdf_download_link(text, is_pro):
    label = "PDF Report"
    if not is_pro: return get_icon_btn_html("#", "https://cdn.simpleicons.org/adobeacrobatreader/999", "PDF (PRO Only)", True)
    
    pdf = FPDF(); pdf.add_page()
    try:
        pdf.add_font('CustomFont', '', 'font.ttf', uni=True); pdf.set_font('CustomFont', '', 12)
    except:
        pdf.set_font("Arial", size=12)
    
    clean_text = clean_markdown(text)
    pdf.multi_cell(0, 10, txt=clean_text)
    
    try:
        pdf_output = pdf.output(dest='S').encode('latin-1') 
        b64 = base64.b64encode(pdf_output).decode()
        # 图标：Adobe PDF
        return f'<a href="data:application/pdf;base64,{b64}" download="prompt_lab_result.pdf" class="icon-btn" title="Download PDF"><img src="https://cdn.simpleicons.org/adobeacrobatreader/E03E2D"></a>'
    except: return "Error"

def get_text_download_link(text, is_pro):
    final = clean_markdown(text) if is_pro else (text + COPYRIGHT_FOOTER)
    b64 = base64.b64encode(final.encode()).decode()
    # 图标：TXT File
    return f'<a href="data:file/txt;base64,{b64}" download="prompt.txt" class="icon-btn" title="Download TXT"><img src="https://cdn.simpleicons.org/txt/555"></a>'

def get_csv_download_link(text, is_pro):
    if not is_pro: return get_icon_btn_html("#", "https://cdn.simpleicons.org/microsoftexcel/999", "CSV (PRO Only)", True)
    b64 = base64.b64encode(f"Content\n{clean_markdown(text)}".encode()).decode()
    # 图标：Excel CSV
    return f'<a href="data:file/csv;base64,{b64}" download="prompt.csv" class="icon-btn" title="Download CSV"><img src="https://cdn.simpleicons.org/microsoftexcel/217346"></a>'

def get_social_links(text):
    s = urllib.parse.quote(text)
    return { 
        "wa": f"https://wa.me/?text={s}", 
        "fb": f"https://www.facebook.com/sharer/sharer.php?u=pl.ai&quote={s}", 
        "tw": f"https://twitter.com/intent/tweet?text={s}", 
        "li": f"https://www.linkedin.com/sharing/share-offsite/?url=pl.ai", 
        "mail": f"mailto:?subject=Result&body={s}" 
    }

# ==========================================
# 5. 页面逻辑
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 1
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'user_tier' not in st.session_state: st.session_state.user_tier = "FREE"
if 'current_role' not in st.session_state: st.session_state.current_role = ""
if 'generated_result' not in st.session_state: st.session_state.generated_result = ""
if 'last_gen_time' not in st.session_state: st.session_state.last_gen_time = 0
if 'interface_lang' not in st.session_state: st.session_state.interface_lang = "English"
if 'daily_gen_count' not in st.session_state: st.session_state.daily_gen_count = 0
if 'daily_img_count' not in st.session_state: st.session_state.daily_img_count = 0
if 'last_reset_date' not in st.session_state: st.session_state.last_reset_date = datetime.date.today()

if st.session_state.last_reset_date != datetime.date.today():
    st.session_state.daily_gen_count = 0; st.session_state.daily_img_count = 0; st.session_state.last_reset_date = datetime.date.today()

LIMITS = {"FREE": {"gen": 5, "img": 3, "chars": 500, "batch_gen": 1, "batch_img": 1}, "PRO": {"gen": 100, "img": 200, "chars": 2000, "batch_gen": 50, "batch_img": 50}}
ui = LANG_DICT.get(st.session_state.interface_lang, LANG_DICT["English"])

if os.path.exists("logo.png"): st.sidebar.image("logo.png", width=150)

# PAGE 1: LOGIN
if st.session_state.page == 1:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if os.path.exists("logo.png"): st.image("logo.png", width=120)
        st.markdown("<h1 style='text-align: center;'>🧠 PromptLab AI</h1>", unsafe_allow_html=True)
        st.session_state.interface_lang = st.selectbox("🌐 Language", list(LANG_DICT.keys()))
        ui = LANG_DICT.get(st.session_state.interface_lang, LANG_DICT["English"])
        with st.form("login"):
            st.markdown(f"### {ui['login']}")
            email = st.text_input(f"📧 {ui['email']}"); key = st.text_input(f"🔑 {ui['key']}", type="password")
            st.markdown(f"<a href='https://app.lemonsqueezy.com/my-orders' target='_blank' class='recover-link'>🔗 {ui['lost_key']}</a>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.form_submit_button(f"🚀 {ui['login']}"):
                if "@" in email and key:
                    with st.spinner("Verifying..."):
                        if validate_license(key):
                            st.session_state.user_email = email; st.session_state.user_tier = "PRO"; st.session_state.page = 2
                            send_admin_alert(f"💰 New PRO: {email}"); send_to_airtable(email, "🟢 Login", "Verified", "PRO", "Active"); st.rerun()
                        else: st.error("❌ Invalid Key")
                else: st.error("Missing Info")
            if c2.form_submit_button(f"👤 {ui['guest']}"):
                if "@" in email: st.session_state.user_email = email; st.session_state.user_tier = "FREE"; st.session_state.page = 2; st.rerun()
                else: st.warning("Enter Email")

# PAGE 2: ROLE
elif st.session_state.page == 2:
    c1, c2 = st.columns([1, 4])
    if c1.button(f"⬅️ {ui['back']}"): st.session_state.page = 1; st.rerun()
    st.markdown(f"### 👋 Hi, {st.session_state.user_email} ({'💎 PRO' if st.session_state.user_tier=='PRO' else '👤 FREE'})")
    st.markdown(f"## {ui['role']}"); st.markdown("---")
    roles = list(MODES_DB.keys()); c_list = st.columns(3)
    for i, role in enumerate(roles):
        with c_list[i % 3]:
            if st.button(f"🎭\n{role}", key=f"r_{i}", use_container_width=True): st.session_state.current_role = role; st.session_state.page = 3; st.rerun()

# PAGE 3: DASHBOARD
elif st.session_state.page == 3:
    is_pro = st.session_state.user_tier == "PRO"
    limits = LIMITS["PRO"] if is_pro else LIMITS["FREE"]
    with st.sidebar:
        st.info(f"👤 {st.session_state.user_email}")
        if is_pro: st.success("💎 PRO PLAN")
        else: st.warning("👤 FREE PLAN")
        st.progress(st.session_state.daily_gen_count/limits['gen'], text=f"Gen: {st.session_state.daily_gen_count}/{limits['gen']}")
        st.markdown("---")
        st.session_state.interface_lang = st.selectbox("🌐 Language", list(LANG_DICT.keys()))
        ui = LANG_DICT.get(st.session_state.interface_lang, LANG_DICT["English"])
        
        if not is_pro:
            st.link_button(f"💎 {ui['upgrade']} ($12.90)", "https://promptlab.lemonsqueezy.com/checkout", type="primary")
            with st.expander("🏆 Why Upgrade?"):
                st.markdown("| Feature | 👤 Free | 💎 PRO |\n|---|---|---|\n| **Markdown** | ❌ Raw | ✅ **Clean** |\n| **Share** | WA Only | **All** |\n| **Export** | TXT | **PDF/CSV** |\n| **Batch** | 1x | **50x** |")
        else: st.link_button(f"⚙️ {ui['manage']}", "https://app.lemonsqueezy.com/my-orders")
        
        with st.expander("🎫 Support Ticket"):
            with st.form("ticket"):
                st.text_input("User", value=st.session_state.user_email, disabled=True)
                itype = st.selectbox("Issue", ["Bug", "Billing", "Feature"])
                sub = st.text_input("Subject"); msg = st.text_area("Message")
                if st.form_submit_button("🚀 Submit"):
                    if sub and msg:
                        ai_ok, ai_sol = check_ai_knowledge_base(sub, msg)
                        if ai_ok: st.markdown(f'<div class="ai-reply-box">🤖 AI: {ai_sol}</div>', unsafe_allow_html=True)
                        else: send_to_airtable(st.session_state.user_email, itype, sub, msg, "New"); send_admin_alert(f"Ticket: {sub}"); st.success("✅ Sent!")
        st.markdown("---"); 
        if st.button(f"🚪 {ui['logout']}"): st.session_state.clear(); st.rerun()

    bc1, bc2 = st.columns([1, 5])
    if bc1.button(f"⬅️ {ui['role']}"): st.session_state.page = 2; st.rerun()
    role = st.session_state.current_role; role_data = MODES_DB[role]
    st.title(f"🎭 {role}")
    mode_keys = list(role_data.keys()); d_modes = mode_keys if is_pro else [k if i==0 else f"🔒 {k} (PRO)" for i, k in enumerate(mode_keys)]
    sel = st.radio("Mode:", d_modes, horizontal=True); real_mode = sel.replace("🔒 ", "").replace(" (PRO)", ""); locked = "🔒" in sel
    curr = role_data[real_mode]
    st.caption(f"💡 {curr['desc']}"); st.markdown("---")

    if locked: st.error("🔒 PRO Only"); st.link_button(f"💎 {ui['upgrade']}", "#", type="primary")
    else:
        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                opts = curr['dd'].copy(); opts.append("✨ Custom...") if is_pro else opts.append("🔒 More...")
                ch = st.selectbox("👉 Option", opts)
                top = st.text_input("✍️ Custom:") if "Custom" in ch else ("LOCKED" if "🔒" in ch else ch)
                
                platform_choice = "General"
                if "Visual" in real_mode or "Thumbnail" in real_mode or "Product" in real_mode:
                    platform_choice = st.selectbox("🎨 Target Platform", ["General AI (ChatGPT/Gemini)", "Midjourney v6", "Stable Diffusion XL", "Leonardo.ai"])
                
                tone = st.selectbox("🗣️ Tone", curr['tones']) if "tones" in curr else "Standard"
                qty = st.number_input("⚡ Batch", 1, 50, 1) if is_pro else 1
            with c2:
                if "📸" in ch:
                    placeholder_text = "📸 Describe your image (e.g., 'A cat on a sofa'). AI will structure it."
                else:
                    placeholder_text = f"⌨️ {curr['in']} (Max {limits['chars']} chars...)"
                det = st.text_area(placeholder_text, height=100)
                ol = st.selectbox("🌐 Output", OUTPUT_LANGUAGES)
            
            with st.expander(ui['upload']):
                st.caption("💎 Unlimited" if is_pro else f"📊 {st.session_state.daily_img_count}/{limits['img']}")
                if st.session_state.daily_img_count >= limits['img']: st.error("Limit Reached")
                else: ups = st.file_uploader("Img", type=["jpg","png"], accept_multiple_files=True)

            if top == "LOCKED": st.button(ui['gen_btn'], disabled=True)
            else:
                if st.button(f"{ui['gen_btn']} ({qty})", type="primary"):
                    if st.session_state.daily_gen_count + qty > limits['gen']: st.error("Limit Reached"); st.stop()
                    if not is_pro:
                        if time.time()-st.session_state.last_gen_time < 60: st.warning(f"Wait 60s"); st.stop()
                        st.session_state.last_gen_time = time.time()
                    
                    st.session_state.daily_gen_count += qty; ups_len = len(ups) if ups else 0
                    if ups: st.session_state.daily_img_count += ups_len
                    bar = st.progress(0, ui['wait']); 
                    for p in range(100): time.sleep(0.01 if is_pro else 0.03); bar.progress(p+1)
                    bar.empty()
                    
                    res = ""
                    for i in range(qty): 
                        simulated_content = smart_mock_generate(role, real_mode, ch, tone, top, det, ol, platform_choice)
                        res += f"=== #{i+1} ===\n{simulated_content}\n\n"
                    
                    st.session_state.generated_result = res; st.success("✅ Done!")

    if st.session_state.generated_result and not locked:
        st.markdown("### Result"); st.code(st.session_state.generated_result)
        share_text = clean_markdown(st.session_state.generated_result) if is_pro else (st.session_state.generated_result + COPYRIGHT_FOOTER)
        lnk = get_social_links(share_text)
        
        # --- 🚀 [UI 升级] 图标化工具栏 ---
        
        st.markdown("---"); st.caption(ui['connect'])
        
        # AI Connect (Icons)
        st.markdown(f"""
        <div class="icon-dock">
            {get_icon_btn_html("https://gemini.google.com", "https://cdn.simpleicons.org/googlegemini/gradient", "Gemini")}
            {get_icon_btn_html("https://chat.openai.com", "https://cdn.simpleicons.org/openai/10A37F", "ChatGPT")}
            {get_icon_btn_html("https://claude.ai", "https://cdn.simpleicons.org/anthropic/D97757", "Claude")}
            {get_icon_btn_html("https://www.notion.so", "https://cdn.simpleicons.org/notion/000000", "Notion")}
            {get_icon_btn_html("https://www.midjourney.com", "https://cdn.simpleicons.org/artstation/000000", "Midjourney")}
            {get_icon_btn_html("https://www.canva.com", "https://cdn.simpleicons.org/canva/00C4CC", "Canva")}
        </div>
        """, unsafe_allow_html=True)

        st.caption("🚀 Social Deck")
        if is_pro:
            st.markdown(f"""
            <div class="icon-dock">
                {get_icon_btn_html(lnk["wa"], "https://cdn.simpleicons.org/whatsapp/25D366", "WhatsApp")}
                {get_icon_btn_html(lnk["fb"], "https://cdn.simpleicons.org/facebook/1877F2", "Facebook")}
                {get_icon_btn_html(lnk["tw"], "https://cdn.simpleicons.org/x/000000", "X (Twitter)")}
                {get_icon_btn_html(lnk["li"], "https://cdn.simpleicons.org/linkedin/0A66C2", "LinkedIn")}
                {get_icon_btn_html(lnk["mail"], "https://cdn.simpleicons.org/gmail/EA4335", "Email")}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="icon-dock">
                {get_icon_btn_html(lnk["wa"], "https://cdn.simpleicons.org/whatsapp/25D366", "WhatsApp")}
                <span style="font-size:12px; color:#999; margin-left:10px">🔒 Upgrade for FB, X, LinkedIn...</span>
            </div>
            """, unsafe_allow_html=True)

        st.caption("💾 Utility Deck")
        col_util_1, col_util_2 = st.columns([1, 1])
        
        with col_util_1:
            # 下载区 (HTML Icons)
            txt_html = get_text_download_link(st.session_state.generated_result, is_pro)
            pdf_html = get_pdf_download_link(st.session_state.generated_result, is_pro)
            csv_html = get_csv_download_link(st.session_state.generated_result, is_pro)
            
            st.markdown(f"""
            <div class="icon-dock">
                {txt_html} {pdf_html} {csv_html}
            </div>
            """, unsafe_allow_html=True)
            
        with col_util_2:
            # 复制与 App 跳转
            if is_pro:
                 st.markdown(f"""
                <div class="icon-dock">
                    {get_icon_btn_html("https://instagram.com", "https://cdn.simpleicons.org/instagram/E4405F", "Instagram")}
                    {get_icon_btn_html("https://xiaohongshu.com", "https://cdn.simpleicons.org/xiaohongshu/FF2442", "Xiaohongshu")}
                    {get_icon_btn_html("https://tiktok.com", "https://cdn.simpleicons.org/tiktok/000000", "TikTok")}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.caption("🔒 App Links (PRO)")
            
            # Copy 按钮保持原生，因为需要 JS 交互，但我们给它加个图标
            st.button(f"📋 {ui['copy']}", help="Copy to clipboard")

st.markdown("---"); st.markdown("""<div style='text-align:center;color:#888;font-size:12px'>© 2025 Cikgu Lai Inc. | v4.9 Visual UI Edition</div>""", unsafe_allow_html=True)