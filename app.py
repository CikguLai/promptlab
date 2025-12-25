import streamlit as st
import datetime
import urllib.parse
import base64
import requests
import smtplib
import random
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# ==========================================
# 1. 全局配置 & 样式
# ==========================================
st.set_page_config(page_title="PromptLab AI - Enterprise", layout="wide", page_icon="🧠")

st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 8px; }
    .stSelectbox, .stTextInput, .stNumberInput { border-radius: 8px; }
    .reportview-container { background: #f0f2f6; }
    .warning-text { color: #FF4B4B; font-weight: bold; font-size: 14px; margin: 10px 0; padding: 10px; background-color: #ffe8e8; border-radius: 5px; border-left: 5px solid #FF4B4B; }
    .social-link { display: inline-block; text-decoration: none; color: white; background-color: #2E86C1; padding: 8px 12px; border-radius: 5px; text-align: center; width: 100%; margin: 2px; font-size: 14px; }
    .social-link:hover { opacity: 0.8; color: white; }
    .app-link { display: inline-block; text-decoration: none; color: white; background-color: #333; padding: 6px 10px; border-radius: 15px; text-align: center; width: 100%; font-size: 12px; border: 1px solid #555; }
    .xhs { background-color: #FF2442; }
    .insta { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); }
    .tiktok { background-color: #000000; }
    .disabled-link { display: inline-block; text-decoration: none; color: #999; background-color: #eee; padding: 6px 10px; border-radius: 5px; text-align: center; width: 100%; border: 1px solid #ddd; pointer-events: none; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 多语言核心词典 (15 Languages)
# ==========================================
LANG_DICT = {
    "English": {
        "login": "Login (PRO)", "guest": "Free Guest", "key": "Activation Key", "email": "Email Address",
        "role": "Choose Workspace", "back": "Back", "logout": "Logout", "upgrade": "Upgrade to PRO",
        "gen_btn": "✨ GENERATE PROMPT", "upload": "📸 Upload Images", "download": "Download", "copy": "Copy",
        "limit": "Daily Limit", "used": "used", "wait": "Please wait"
    },
    "简体中文": {
        "login": "PRO 会员登入", "guest": "免费试用", "key": "激活码 (Key)", "email": "电子邮箱",
        "role": "选择工作区", "back": "返回", "logout": "退出", "upgrade": "升级到 PRO",
        "gen_btn": "✨ 生成提示词", "upload": "📸 上传参考图", "download": "下载", "copy": "复制",
        "limit": "今日限额", "used": "已用", "wait": "请等待"
    },
    "Bahasa Melayu": {
        "login": "Log Masuk (PRO)", "guest": "Tetamu Percuma", "key": "Kunci Aktivasi", "email": "Emel",
        "role": "Pilih Ruang Kerja", "back": "Kembali", "logout": "Keluar", "upgrade": "Naik Taraf PRO",
        "gen_btn": "✨ Jana Prompt", "upload": "📸 Muat Naik Gambar", "download": "Muat Turun", "copy": "Salin",
        "limit": "Had Harian", "used": "digunakan", "wait": "Sila tunggu"
    },
    "繁體中文": {
        "login": "PRO 會員登入", "guest": "免費試用", "key": "啟動碼", "email": "電子郵件",
        "role": "選擇工作區", "back": "返回", "logout": "登出", "upgrade": "升級至 PRO",
        "gen_btn": "✨ 生成提示詞", "upload": "📸 上傳圖片", "download": "下載", "copy": "複製",
        "limit": "今日限額", "used": "已用", "wait": "請稍候"
    },
    "Tamil (தமிழ்)": {
        "login": "உள்நுழை (PRO)", "guest": "இலவச விருந்தினர்", "key": "செயல்படுத்தும் விசை", "email": "மின்னஞ்சல்",
        "role": "பணியிடத்தைத் தேர்வுசெய்க", "back": "பின்னால்", "logout": "வெளியேறு", "upgrade": "PRO க்கு மேம்படுத்தவும்",
        "gen_btn": "✨ உருவாக்கவும்", "upload": "📸 படங்களை பதிவேற்றவும்", "download": "பதிவிறக்க", "copy": "நகலெடு",
        "limit": "தினசரி வரம்பு", "used": "பயன்படுத்தப்பட்டது", "wait": "காத்திருக்கவும்"
    },
    "Japanese (日本語)": {
        "login": "ログイン (PRO)", "guest": "無料ゲスト", "key": "ライセンスキー", "email": "メールアドレス",
        "role": "ワークスペースを選択", "back": "戻る", "logout": "ログアウト", "upgrade": "PROにアップグレード",
        "gen_btn": "✨ プロンプト生成", "upload": "📸 画像をアップロード", "download": "ダウンロード", "copy": "コピー",
        "limit": "1日の上限", "used": "使用済み", "wait": "お待ちください"
    },
    "Korean (한국어)": {
        "login": "로그인 (PRO)", "guest": "무료 체험", "key": "활성화 키", "email": "이메일",
        "role": "워크스페이스 선택", "back": "뒤로", "logout": "로그아웃", "upgrade": "PRO로 업그레이드",
        "gen_btn": "✨ 프롬프트 생성", "upload": "📸 이미지 업로드", "download": "다운로드", "copy": "복사",
        "limit": "일일 한도", "used": "사용됨", "wait": "기다려주세요"
    },
    "Arabic (العربية)": {
        "login": "تسجيل الدخول (PRO)", "guest": "ضيف مجاني", "key": "مفتاح التفعيل", "email": "البريد الإلكتروني",
        "role": "اختر مساحة العمل", "back": "رجوع", "logout": "خروج", "upgrade": "ترقية إلى PRO",
        "gen_btn": "✨ إنشاء", "upload": "📸 تحميل الصور", "download": "تحميل", "copy": "نسخ",
        "limit": "الحد اليومي", "used": "مستخدم", "wait": "انتظر من فضلك"
    },
    "Indonesian (Bahasa Indonesia)": {
        "login": "Masuk (PRO)", "guest": "Tamu Gratis", "key": "Kunci Aktivasi", "email": "Email",
        "role": "Pilih Peran", "back": "Kembali", "logout": "Keluar", "upgrade": "Tingkatkan ke PRO",
        "gen_btn": "✨ Buat Prompt", "upload": "📸 Unggah Gambar", "download": "Unduh", "copy": "Salin",
        "limit": "Batas Harian", "used": "digunakan", "wait": "Mohon tunggu"
    },
    "Thai (ไทย)": {
        "login": "เข้าสู่ระบบ (PRO)", "guest": "ทดลองฟรี", "key": "รหัสเปิดใช้งาน", "email": "อีเมล",
        "role": "เลือกพื้นที่ทำงาน", "back": "กลับ", "logout": "ออกจากระบบ", "upgrade": "อัปเกรดเป็น PRO",
        "gen_btn": "✨ สร้างพรอมต์", "upload": "📸 อัปโหลดรูปภาพ", "download": "ดาวน์โหลด", "copy": "คัดลอก",
        "limit": "ขีดจำกัดรายวัน", "used": "ใช้แล้ว", "wait": "โปรดรอ"
    },
    "Vietnamese (Tiếng Việt)": {
        "login": "Đăng nhập (PRO)", "guest": "Khách miễn phí", "key": "Mã kích hoạt", "email": "Email",
        "role": "Chọn vai trò", "back": "Quay lại", "logout": "Đăng xuất", "upgrade": "Nâng cấp lên PRO",
        "gen_btn": "✨ Tạo Prompt", "upload": "📸 Tải ảnh lên", "download": "Tải xuống", "copy": "Sao chép",
        "limit": "Giới hạn ngày", "used": "đã dùng", "wait": "Vui lòng đợi"
    },
    "French (Français)": {
        "login": "Connexion (PRO)", "guest": "Invité Gratuit", "key": "Clé d'activation", "email": "Email",
        "role": "Choisir", "back": "Retour", "logout": "Déconnexion", "upgrade": "Passer à PRO",
        "gen_btn": "✨ Générer", "upload": "📸 Télécharger", "download": "Télécharger", "copy": "Copier",
        "limit": "Limite quotidienne", "used": "utilisé", "wait": "Veuillez patienter"
    },
    "Spanish (Español)": {
        "login": "Acceso (PRO)", "guest": "Invitado Gratis", "key": "Clave de activación", "email": "Email",
        "role": "Elegir Rol", "back": "Volver", "logout": "Salir", "upgrade": "Mejorar a PRO",
        "gen_btn": "✨ Generar", "upload": "📸 Subir Imágenes", "download": "Descargar", "copy": "Copiar",
        "limit": "Límite diario", "used": "usado", "wait": "Espera por favor"
    },
    "German (Deutsch)": {
        "login": "Login (PRO)", "guest": "Gratis Gast", "key": "Aktivierungsschlüssel", "email": "E-Mail",
        "role": "Rolle wählen", "back": "Zurück", "logout": "Abmelden", "upgrade": "Upgrade auf PRO",
        "gen_btn": "✨ Generieren", "upload": "📸 Hochladen", "download": "Herunterladen", "copy": "Kopieren",
        "limit": "Tageslimit", "used": "benutzt", "wait": "Bitte warten"
    },
    "Russian (Русский)": {
        "login": "Вход (PRO)", "guest": "Гость", "key": "Ключ активации", "email": "Email",
        "role": "Выбрать роль", "back": "Назад", "logout": "Выйти", "upgrade": "Обновить до PRO",
        "gen_btn": "✨ Создать", "upload": "📸 Загрузить", "download": "Скачать", "copy": "Копировать",
        "limit": "Лимит", "used": "исп.", "wait": "Подождите"
    }
}

# 界面语言列表也是输出语言列表
OUTPUT_LANGUAGES = list(LANG_DICT.keys())

# ==========================================
# 3. 核心数据库 (Content DB)
# ==========================================
COMMON_TONES = [
    "🌟 Professional & Confident (专业自信)", "🥰 Empathetic & Warm (温暖共情)", "🔥 Persuasive & Bold (极具说服力)",
    "👻 Witty & Humorous (幽默风趣)", "📖 Storyteller / Narrative (故事叙述感)", "⚡ Urgent / FOMO (紧迫感)",
    "🧘 Calm & Minimalist (冷静极简)", "🎓 Academic & Formal (学术正式)"
]

MODES_DB = {
    "Global Educator": {
        "🟢 Pedagogy": { "dd": ["Direct Instruction", "Gamification", "Socratic Method", "Project-Based Learning", "STEAM Education"], "tones": COMMON_TONES, "in": "Topic & Level", "desc": "Lesson Plans." },
        "🔵 Visuals": { "dd": ["Pixar 3D Style", "Realistic Photography", "Infographic / Poster", "Watercolor Art", "Scientific Schematic"], "in": "Visual Description", "desc": "AI Art Prompts." },
        "🟣 Comm & Social": { "dd": ["Student Showcase", "Parent Message (WhatsApp)", "Official Proposal", "Behavior Report", "Classroom Newsletter"], "tones": COMMON_TONES, "in": "Context", "desc": "Letters & Posts." }
    },
    "Global Creator": {
        "🟢 Scripting": { "dd": ["TikTok/Reels (Short)", "YouTube Tutorial (Long)", "Live Stream Script", "Storytelling Vlog", "Podcast Outline"], "tones": COMMON_TONES, "in": "Video Topic", "desc": "Scripts." },
        "🔵 Thumbnail": { "dd": ["High CTR (Shocked)", "Aesthetic / Clean", "Cinematic Poster", "Tech / Neon", "Before & After"], "in": "Image Scenario", "desc": "Cover Art." },
        "🟣 Marketing": { "dd": ["Xiaohongshu (Soft Sell)", "Facebook Ad (Hard Sell)", "Instagram Caption", "LinkedIn Thought Leader", "Email Newsletter"], "tones": COMMON_TONES, "in": "Product", "desc": "Social Copy." }
    },
    "Global Parent": {
        "🟢 Story Time": { "dd": ["Bedtime Story", "Behavior Lesson", "Hero Adventure", "Science Story", "Cultural Tale"], "tones": ["😴 Calming/Sleepy", "🦸 Exciting/Heroic", "❤️ Heartwarming", "🤣 Funny/Silly", "🤔 Mystery/Curious"], "in": "Child Name/Age", "desc": "Stories." },
        "🔵 Activities": { "dd": ["DIY Craft Guide", "Indoor Game", "Science Experiment", "Scavenger Hunt", "Cooking Recipe"], "tones": ["🎨 Creative", "🔬 Educational", "🎉 Fun & Energetic"], "in": "Interest", "desc": "Activities." },
        "🟣 Tutor": { "dd": ["Explain like I'm 5", "Homework Helper", "Quiz Generator", "Vocabulary Builder", "Math Solver"], "tones": ["👩‍🏫 Encouraging Teacher", "🤖 Logical/Direct", "🧩 Gamified/Fun"], "in": "Question", "desc": "Tutor." }
    },
    "Global Seller": {
        "🟢 Copywriting": { "dd": ["PAS (Pain-Agitate-Solve)", "AIDA (Attention-Action)", "Storytelling Sales", "FAQ Generator", "Brand Story"], "tones": COMMON_TONES, "in": "Product USP", "desc": "Sales Copy." },
        "🔵 Product Shot": { "dd": ["Studio White BG", "Lifestyle Cozy", "Luxury Gold", "Nature/Outdoor", "Cyberpunk/Neon"], "in": "Product Item", "desc": "Photography." },
        "🟣 Support": { "dd": ["Apology Letter", "Review Request", "Complaint Reply", "Sale Announcement", "Crisis Statement"], "tones": ["🤝 Apologetic & Sincere", "💼 Professional & Firm", "💖 Gratitude & Warm"], "in": "Issue", "desc": "Customer Service." }
    },
    "Global Student": {
        "🟢 Study": { "dd": ["Summarizer", "Simplifier (ELI5)", "Flashcard Maker", "Translator", "Grammar Fixer"], "tones": ["📚 Academic", "⚡ Quick/Brief", "🗣️ Conversational"], "in": "Text/Topic", "desc": "Study Notes." },
        "🔵 Project": { "dd": ["Essay Outline", "Presentation Script", "Thesis Generator", "Lab Report", "Group Roles"], "tones": COMMON_TONES, "in": "Topic", "desc": "Projects." },
        "🟣 Career": { "dd": ["Resume Builder", "Cover Letter", "Interview Q&A", "LinkedIn Bio", "Cold Email"], "tones": ["💼 Corporate Professional", "🚀 Startup/Energetic", "🎨 Creative/Unique"], "in": "Role", "desc": "Career." }
    },
    "Global Corporate": {
        "🟢 Admin": { "dd": ["Meeting Minutes", "Email Drafter", "Proposal Outline", "Internal Memo", "Excel Formula"], "tones": ["👔 Formal", "🤝 Collaborative", "⚡ Direct/Brief"], "in": "Context", "desc": "Admin." },
        "🔵 Strategy": { "dd": ["SWOT Analysis", "Competitor Analysis", "Business Model", "OKRs", "Risk Assessment"], "in": "Business", "desc": "Strategy." },
        "🟣 HR & Team": { "dd": ["Job Description", "Team Building Idea", "Performance Review", "Onboarding Plan", "Conflict Resolution"], "tones": ["⚖️ Fair & Balanced", "🚀 Motivational", "❤️ Empathetic"], "in": "Situation", "desc": "HR." }
    }
}

FAQ_DB = {
    "💰 Billing": [("Card rejected?", "Check international usage."), ("Cancel?", "Sidebar > Billing.")],
    "⚙️ Tech": [("Blank screen?", "Clear cache."), ("Lost Key?", "Use sidebar button.")],
    "🧠 Tips": [("Better prompts?", "Be specific."), ("Commercial use?", "Yes, it's yours.")]
}

# ==========================================
# 4. 辅助函数
# ==========================================

COPYRIGHT_FOOTER = "\n\n✨ Generated by PromptLab AI (Free Version)"

def clean_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'#+\s', '', text)
    return text.strip()

def get_text_download_link(text, label, filename="prompt.txt"):
    clean_text = clean_markdown(text)
    b64 = base64.b64encode(clean_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}" style="text-decoration:none;">📄 {label} TXT</a>'

def get_csv_download_link(text, is_pro, label, filename="prompt.csv"):
    if not is_pro: return f'<a href="#" class="disabled-link">📊 {label} CSV (PRO)</a>'
    clean_text = clean_markdown(text)
    csv_content = f"Content\n{clean_text}"
    b64 = base64.b64encode(csv_content.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="text-decoration:none;">📊 {label} CSV</a>'

def get_pdf_download_link(text, is_pro, label, filename="prompt.pdf"):
    if not is_pro: return f'<a href="#" class="disabled-link">📑 {label} PDF (PRO)</a>'
    clean_text = clean_markdown(text)
    b64 = base64.b64encode(clean_text.encode()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="text-decoration:none;">📑 {label} PDF</a>'

def get_social_links(text):
    safe_text = urllib.parse.quote(text) 
    return {
        "wa": f"https://wa.me/?text={safe_text}",
        "fb": f"https://www.facebook.com/sharer/sharer.php?u=promptlab.com&quote={safe_text}",
        "tw": f"https://twitter.com/intent/tweet?text={safe_text}",
        "li": f"https://www.linkedin.com/sharing/share-offsite/?url=promptlab.com",
        "mail": f"mailto:?subject=Generated Content&body={safe_text}"
    }

def send_to_airtable(user, issue, sub, msg): return True
def send_telegram_notification(user, issue, sub): pass
def check_ai_knowledge_base(sub, msg): return False, None
def send_enterprise_email_workflow(user, issue, sub, msg, tid, ai=None): return True

# ==========================================
# 5. 页面逻辑 (Main Logic)
# ==========================================

# State Init
if 'page' not in st.session_state: st.session_state.page = 1
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'user_tier' not in st.session_state: st.session_state.user_tier = "FREE"
if 'current_role' not in st.session_state: st.session_state.current_role = ""
if 'generated_result' not in st.session_state: st.session_state.generated_result = ""
if 'last_gen_time' not in st.session_state: st.session_state.last_gen_time = 0
if 'interface_lang' not in st.session_state: st.session_state.interface_lang = "English"

# Quota Init
if 'daily_gen_count' not in st.session_state: st.session_state.daily_gen_count = 0
if 'daily_img_count' not in st.session_state: st.session_state.daily_img_count = 0
if 'last_reset_date' not in st.session_state: st.session_state.last_reset_date = datetime.date.today()

if st.session_state.last_reset_date != datetime.date.today():
    st.session_state.daily_gen_count = 0; st.session_state.daily_img_count = 0
    st.session_state.last_reset_date = datetime.date.today()

LIMITS = {
    "FREE": {"gen": 5, "img": 3, "chars": 500, "batch_gen": 1, "batch_img": 1},
    "PRO": {"gen": 100, "img": 200, "chars": 2000, "batch_gen": 50, "batch_img": 50}
}

# 获取当前语言的标签包
ui = LANG_DICT.get(st.session_state.interface_lang, LANG_DICT["English"])

# PAGE 1: LOGIN
if st.session_state.page == 1:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🧠 PromptLab AI</h1>", unsafe_allow_html=True)
        # 语言选择器
        st.session_state.interface_lang = st.selectbox("🌐 Language / 语言", list(LANG_DICT.keys()))
        ui = LANG_DICT.get(st.session_state.interface_lang, LANG_DICT["English"]) # 刷新 UI

        with st.form("login_form"):
            st.markdown(f"### {ui['login']}")
            email = st.text_input(f"📧 {ui['email']}")
            key = st.text_input(f"🔑 {ui['key']}", type="password")
            c1, c2 = st.columns(2)
            if c1.form_submit_button(f"🚀 {ui['login']}"):
                if "@" in email and key:
                    st.session_state.user_email = email; st.session_state.user_tier = "PRO"; st.session_state.page = 2; st.rerun()
                else: st.error("Key Required.")
            if c2.form_submit_button(f"👤 {ui['guest']}"):
                if "@" in email:
                    st.session_state.user_email = email; st.session_state.user_tier = "FREE"; st.session_state.page = 2; st.rerun()
                else: st.warning("Enter Email.")

# PAGE 2: ROLE SELECTION
elif st.session_state.page == 2:
    c1, c2 = st.columns([1, 4])
    if c1.button(f"⬅️ {ui['back']}"): st.session_state.page = 1; st.rerun()
    badge = "💎 PRO" if st.session_state.user_tier == "PRO" else "👤 FREE"
    st.markdown(f"### 👋 Hi, {st.session_state.user_email} ({badge})")
    
    st.markdown(f"## {ui['role']}"); st.markdown("---")
    roles = list(MODES_DB.keys())
    col1, col2, col3 = st.columns(3)
    for i, role in enumerate(roles):
        with [col1, col2, col3][i % 3]:
            if st.button(f"🎭\n{role}", key=f"role_{i}", use_container_width=True):
                st.session_state.current_role = role; st.session_state.page = 3; st.rerun()

# PAGE 3: DASHBOARD
elif st.session_state.page == 3:
    is_pro = st.session_state.user_tier == "PRO"
    limits = LIMITS["PRO"] if is_pro else LIMITS["FREE"]
    
    with st.sidebar:
        st.info(f"👤 {st.session_state.user_email}")
        if is_pro: st.success("💎 PRO PLAN")
        else: st.warning("👤 FREE PLAN")
        
        st.caption(f"📊 **{ui['limit']}**")
        st.progress(st.session_state.daily_gen_count / limits["gen"], text=f"Generations: {st.session_state.daily_gen_count}/{limits['gen']} {ui['used']}")
        img_disp = "Unlimited*" if is_pro else f"{limits['img']}"
        st.progress(st.session_state.daily_img_count / limits["img"], text=f"Uploads: {st.session_state.daily_img_count}/{img_disp} {ui['used']}")
        
        st.markdown("---")
        st.session_state.interface_lang = st.selectbox("🌐 Language", list(LANG_DICT.keys()))
        ui = LANG_DICT.get(st.session_state.interface_lang, LANG_DICT["English"])

        if not is_pro:
            st.markdown(f"### 🔓 {ui['upgrade']}")
            st.link_button(f"💎 {ui['upgrade']} ($12.90)", "#", type="primary")
        
        with st.expander("🎫 Support Ticket"):
            st.markdown("#### 🔍 Search FAQ")
            q = st.text_input("Search...", label_visibility="collapsed")
            if q: 
                 for cat, items in FAQ_DB.items():
                    for question, ans in items:
                        if q.lower() in question.lower(): st.info(f"**{question}**\n{ans}")

            with st.form("ticket"):
                st.text_input("User", value=st.session_state.user_email, disabled=True)
                itype = st.selectbox("Issue", ["Bug", "Billing", "Feature", "Inquiry"])
                sub = st.text_input("Subject"); msg = st.text_area("Message")
                st.markdown('<div class="warning-text">⚠️ Check FAQ first!</div>', unsafe_allow_html=True)
                if st.form_submit_button("🚀 Submit"):
                    if sub and msg:
                         send_to_airtable(st.session_state.user_email, itype, sub, msg)
                         st.success("✅ Sent!")

        st.markdown("---")
        if st.button(f"🚪 {ui['logout']}"): st.session_state.clear(); st.rerun()

    # Main Content
    bc1, bc2 = st.columns([1, 5])
    if bc1.button(f"⬅️ {ui['role']}"): st.session_state.page = 2; st.rerun()
    
    role = st.session_state.current_role; role_data = MODES_DB[role]
    st.title(f"🎭 {role}")
    
    mode_keys = list(role_data.keys())
    if is_pro: display_modes = mode_keys
    else: display_modes = [k if i == 0 else f"🔒 {k} (PRO)" for i, k in enumerate(mode_keys)]
    
    sel_label = st.radio("Mode:", display_modes, horizontal=True)
    if "🔒" in sel_label: real_mode = sel_label.replace("🔒 ", "").replace(" (PRO)", ""); locked = True
    else: real_mode = sel_label; locked = False
    
    curr_data = role_data[real_mode]
    st.caption(f"💡 {curr_data['desc']}"); st.markdown("---")

    if locked:
        st.error(f"🔒 PRO Only.")
        st.link_button(f"💎 {ui['upgrade']}", "#", type="primary")
    else:
        with st.container():
            c_in1, c_in2 = st.columns(2)
            with c_in1:
                opts = curr_data['dd'].copy()
                if is_pro: opts.append("✨ Custom...")
                else: opts = opts[:3]; opts.append("🔒 More... (PRO)")
                
                choice = st.selectbox("👉 Option", opts)
                if "🔒" in choice: topic = "LOCKED"
                elif "Custom" in choice: topic = st.text_input("✍️ Custom:")
                else: topic = choice
                
                tone_val = "Professional"
                if "tones" in curr_data: tone_val = st.selectbox("🗣️ Tone", curr_data['tones'])
                
                batch_qty = 1
                if is_pro:
                    st.markdown("---")
                    batch_qty = st.number_input("⚡ Batch (1-50)", 1, 50, 1)
            
            with c_in2:
                details = st.text_area(f"⌨️ {curr_data['in']}", placeholder=f"Max {limits['chars']} chars...", height=100)
                if len(details) > limits["chars"]: st.error("Too long!"); topic = "LOCKED"
                # 输出语言直接使用界面语言列表
                out_lang = st.selectbox("🌐 Output Language", OUTPUT_LANGUAGES)

            # Upload Image Area (Restored with Limits)
            with st.expander(f"{ui['upload']}"):
                if is_pro: st.caption("💎 Unlimited")
                else: st.caption(f"📊 {st.session_state.daily_img_count}/{limits['img']}")

                if st.session_state.daily_img_count >= limits["img"]: st.error("Limit Reached.")
                else:
                    up_files = st.file_uploader("JPG/PNG", type=["jpg", "png"], accept_multiple_files=True)

            if topic == "LOCKED": st.button(ui['gen_btn'], disabled=True)
            else:
                if st.button(f"{ui['gen_btn']} ({batch_qty})", type="primary"):
                    if st.session_state.daily_gen_count + batch_qty > limits["gen"]: st.error("Daily Limit Reached."); st.stop()
                    
                    if not is_pro:
                        t_now = time.time()
                        if t_now - st.session_state.last_gen_time < 60:
                            st.warning(f"⏳ {ui['wait']} {int(60 - (t_now - st.session_state.last_gen_time))}s."); st.stop()
                        st.session_state.last_gen_time = t_now

                    st.session_state.daily_gen_count += batch_qty
                    if up_files: st.session_state.daily_img_count += len(up_files)
                    
                    bar = st.progress(0, ui['wait'])
                    speed = 0.5 if is_pro else 2.0
                    for p in range(100): time.sleep(speed/100); bar.progress(p+1, "Processing...")
                    bar.empty()
                    
                    img_txt = f"[Image]: {len(up_files)} files" if up_files else ""
                    
                    # 生成内容模拟
                    final_output = ""
                    for i in range(batch_qty):
                        final_output += f"""
=== Variation #{i+1} ===
[SYSTEM]: Act as a {role}. Tone: {tone_val}.
[INSTRUCTION]: Write 100% human-like.
[CONTENT]: {topic} - {details}
[LANG]: {out_lang}
{img_txt}
(Simulated AI response for variation #{i+1}...)

"""
                    st.session_state.generated_result = final_output
                    st.success("✅ Done!")

    if st.session_state.generated_result and not locked:
        st.markdown("### 📄 Result:")
        st.code(st.session_state.generated_result)
        
        share_content = clean_markdown(st.session_state.generated_result)
        if not is_pro: share_content += COPYRIGHT_FOOTER
        links = get_social_links(share_content)

        st.markdown("---"); st.caption("🚀 **Social Deck**")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown(f'<a href="{links["wa"]}" target="_blank" class="social-link">WhatsApp</a>', unsafe_allow_html=True)
        with c2: st.markdown(f'<a href="{links["fb"]}" target="_blank" class="social-link">Facebook</a>', unsafe_allow_html=True)
        with c3: st.markdown(f'<a href="{links["tw"]}" target="_blank" class="social-link">X</a>', unsafe_allow_html=True)
        with c4: st.markdown(f'<a href="{links["li"]}" target="_blank" class="social-link">LinkedIn</a>', unsafe_allow_html=True)
        with c5: st.markdown(f'<a href="{links["mail"]}" target="_blank" class="social-link">Email</a>', unsafe_allow_html=True)

        st.caption("💾 **Utility Deck**")
        u1, u2 = st.columns([1.5, 2.5])
        with u1:
            b1, b2, b3 = st.columns(3)
            with b1: st.markdown(get_text_download_link(st.session_state.generated_result, ui['download']), unsafe_allow_html=True)
            with b2: st.markdown(get_pdf_download_link(st.session_state.generated_result, is_pro, ui['download']), unsafe_allow_html=True)
            with b3: st.markdown(get_csv_download_link(st.session_state.generated_result, is_pro, ui['download']), unsafe_allow_html=True)
        with u2:
            d1, d2, d3, d4 = st.columns([1.2,1,1,1])
            with d1: st.button(f"📋 {ui['copy']}")
            with d2: st.markdown(f'<a href="#" class="app-link insta">Insta</a>', unsafe_allow_html=True)
            with d3: st.markdown(f'<a href="#" class="app-link xhs">XHS</a>', unsafe_allow_html=True)
            with d4: st.markdown(f'<a href="#" class="app-link tiktok">TikTok</a>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""<div style='text-align: center; color: #666; font-size: 12px; margin-top: 20px;'><p>© 2025 <strong>Cikgu Lai Inc.</strong> | PromptLab AI® <em>Enterprise v3.3</em></p><p>Legal Disclaimer: Users are responsible for commercial use.</p></div>""", unsafe_allow_html=True)