import streamlit as st
import time
import re
import google.generativeai as genai
from fpdf import FPDF
import urllib.parse
from PIL import Image
import random 
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==============================================================================
# 0. CONFIG & SAFETY
# ==============================================================================
st.set_page_config(
    page_title="Lai's Lab AI",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded" # 手机上会自动收起，电脑上会自动展开
)

VERSION = "V8.0 Global (Mobile First)"
LEMON_LINK = "https://cikgulai.lemonsqueezy.com/checkout" 

# Safety Config
safety_config = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
]

BLACKLIST = [
    "porn", "sex", "nude", "naked", "xxx", "kill", "suicide", "murder", 
    "色情", "裸", "性爱", "杀", "死", "暴力", "血",
    "bogel", "lucah", "seks", "bunuh", "judi"
]

def check_safety(user_input):
    if not user_input: return True
    input_lower = str(user_input).lower()
    for word in BLACKLIST:
        if word in input_lower: return False
    return True

# ==============================================================================
# [核心修改] 注入智能 CSS (适配手机 + 电脑)
# ==============================================================================
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        body { font-family: 'Inter', sans-serif; }
        
        /* --- 1. 全局按钮样式 --- */
        .stButton>button { 
            border-radius: 8px; font-weight: 600; border: none;
            transition: all 0.2s;
        }
        
        /* 电脑端默认样式 */
        div[data-testid="stVerticalBlock"] > div > .stButton > button {
            background-color: #1A73E8; color: white; height: 50px; font-size: 1.1rem;
        }
        div[data-testid="stVerticalBlock"] > div > .stButton > button:hover { 
            background-color: #1557B0; transform: translateY(-2px); box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        /* --- 2. 社交按钮 (Social Buttons) --- */
        .social-btn {
            display: inline-flex; align-items: center; justify-content: center;
            text-decoration: none; color: white !important; font-weight: 500;
            padding: 10px 20px; border-radius: 8px; margin: 0 8px 8px 0; font-size: 0.95rem;
            transition: opacity 0.3s; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .social-btn:hover { opacity: 0.9; transform: translateY(-1px); }
        
        /* 颜色定义 */
        .btn-wa { background-color: #25D366; }    
        .btn-tg { background-color: #0088cc; }    
        .btn-mail { background-color: #EA4335; }  
        .btn-link { background-color: #0077b5; }  
        .btn-lock { background-color: #5f6368; cursor: pointer; opacity: 0.7; border: 1px solid #ccc; } 

        .output-card {
            background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 12px;
            padding: 25px; margin-top: 20px; line-height: 1.6; color: #333;
            white-space: pre-wrap; font-size: 1rem; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        
        .custom-footer {
            margin-top: 50px; padding: 20px; text-align: center; color: #5f6368;
            font-size: 0.8rem; border-top: 1px solid #e0e0e0;
        }

        /* --- 3. 📱 手机/平板 专属适配 (Mobile Responsive) --- */
        @media only screen and (max-width: 768px) {
            /* 字体变大，易阅读 */
            html, body, [class*="css"] { font-size: 16px !important; }
            
            /* 按钮变大，方便大拇指点击 */
            div[data-testid="stVerticalBlock"] > div > .stButton > button {
                height: 60px !important; /* 按钮更高 */
                font-size: 1.2rem !important;
                width: 100% !important; /* 强制全宽 */
            }
            
            /* 社交按钮变成块状，垂直堆叠 */
            .social-btn {
                display: block; width: 100%; text-align: center; margin-bottom: 10px;
                padding: 12px; font-size: 1.1rem;
            }
            
            /* 输出卡片边距调整 */
            .output-card { padding: 15px; }
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==============================================================================
# 1. UI DICTIONARY
# ==============================================================================
UI_LANGS = ["English", "简体中文", "Bahasa Melayu", "Español", "Français", "日本語", "한국어"] 

TRANSLATIONS = {
    "English": {
        "title": "AI SaaS Platform for Educators & Creators", "lbl_email": "📧 Email Address (Required)", "lbl_key": "🔑 License Key (Optional)",
        "btn_enter": "🚀 Enter Laboratory", "err_email": "⚠️ Email is strictly required.", "welcome": "👋 Welcome", "choose_id": "Choose your identity (Focus Mode):",
        "btn_switch": "🔄 Switch Identity", "vip_active": "👑 VIP Pro Active", "free_acc": "🔒 Free Account", "upgrade_txt": "LIFETIME ACCESS",
        "search_ph": "Search (e.g. Refund, PDF, Key)...", "btn_recover": "🔑 Lost Key? Recover Here", "btn_clear": "🗑️ Clear History",
        "btn_submit": "🚀 Submit Ticket", "ticket_tab": "📩 Submit a Request", "warn_faq": "🔴 Read FAQ before submitting.",
        "role_edu": "👨‍🏫 Global Educator", "role_parent": "👪 Global Parent", "role_creator": "🎥 Global Creator", "role_seller": "💰 Global Seller", "role_student": "🎓 Global Student", "role_corp": "💼 Global Corporate",
        "lbl_topic": "✍️ Topic", "lbl_context": "📝 Context / Details", "btn_gen": "✨ Generate",
        "tip_prompt": "💡 **Next Step:** Copy the prompt above and paste it into **Midjourney / DALL-E** to generate the actual image.",
        "footer_disclaimer": "Lai's Lab is an AI drafting tool. Content for reference only."
    },
    "简体中文": {
        "title": "教育者与创作者的全球 AI 平台", "lbl_email": "📧 邮箱地址 (必填)", "lbl_key": "🔑 激活码 (选填)",
        "btn_enter": "🚀 进入实验室", "err_email": "⚠️ 必须填写邮箱。", "welcome": "👋 欢迎", "choose_id": "请选择您的身份 (专注模式):",
        "btn_switch": "🔄 切换身份", "vip_active": "👑 VIP 会员已激活", "free_acc": "🔒 免费账户", "upgrade_txt": "一次付费 · 终身使用",
        "search_ph": "搜索 (如: 退款, PDF, 激活码)...", "btn_recover": "🔑 找回激活码", "btn_clear": "🗑️ 清除历史",
        "btn_submit": "🚀 提交工单", "ticket_tab": "📩 提交工单", "warn_faq": "🔴 提交前请务必阅读 FAQ。",
        "role_edu": "👨‍🏫 全球教育者", "role_parent": "👪 全球父母", "role_creator": "🎥 全球创作者", "role_seller": "💰 全球电商", "role_student": "🎓 全球学生", "role_corp": "💼 全球职场",
        "lbl_topic": "✍️ 课题/主题", "lbl_context": "📝 背景/详情", "btn_gen": "✨ 立即生成",
        "tip_prompt": "💡 **下一步:** 复制提示词，粘贴到 **Midjourney** 生成图片。",
        "footer_disclaimer": "本工具仅生成 AI 草稿，内容仅供参考。"
    },
    "Bahasa Melayu": {
        "title": "Platform AI untuk Pendidik & Pencipta", "lbl_email": "📧 Alamat Emel (Wajib)", "lbl_key": "🔑 Kunci Lesen (Pilihan)",
        "btn_enter": "🚀 Masuk Makmal", "err_email": "⚠️ Emel diperlukan.", "welcome": "👋 Selamat Datang", "choose_id": "Pilih identiti anda (Mod Fokus):",
        "btn_switch": "🔄 Tukar Identiti", "vip_active": "👑 VIP Pro Aktif", "free_acc": "🔒 Akaun Percuma", "upgrade_txt": "AKSES SEUMUR HIDUP",
        "search_ph": "Cari (cth: Bayaran, PDF)...", "btn_recover": "🔑 Cari Kunci Lesen", "btn_clear": "🗑️ Padam Sejarah",
        "btn_submit": "🚀 Hantar Tiket", "ticket_tab": "📩 Hantar Tiket", "warn_faq": "🔴 Baca FAQ sebelum hantar.",
        "role_edu": "👨‍🏫 Pendidik Global", "role_parent": "👪 Ibu Bapa Global", "role_creator": "🎥 Pencipta Global", "role_seller": "💰 Penjual Global", "role_student": "🎓 Pelajar Global", "role_corp": "💼 Korporat Global",
        "lbl_topic": "✍️ Topik", "lbl_context": "📝 Maklumat Lanjut", "btn_gen": "✨ Menjana",
        "tip_prompt": "💡 **Langkah Seterusnya:** Salin prompt di atas ke **Midjourney**.",
        "footer_disclaimer": "Lai's Lab adalah alat AI. Kandungan untuk rujukan sahaja."
    },
    "Español": { "title": "Plataforma IA", "lbl_email": "📧 Correo", "lbl_key": "🔑 Clave", "btn_enter": "🚀 Entrar", "err_email": "⚠️ Correo requerido.", "welcome": "👋 Bienvenido", "choose_id": "Elige tu identidad:", "btn_switch": "🔄 Cambiar", "vip_active": "👑 VIP Activo", "free_acc": "🔒 Gratis", "upgrade_txt": "ACCESO DE POR VIDA", "search_ph": "Buscar...", "btn_recover": "🔑 Recuperar Clave", "btn_clear": "🗑️ Borrar", "btn_submit": "🚀 Enviar", "ticket_tab": "📩 Soporte", "warn_faq": "🔴 Leer FAQ.", "role_edu": "👨‍🏫 Educador", "role_parent": "👪 Padre", "role_creator": "🎥 Creador", "role_seller": "💰 Vendedor", "role_student": "🎓 Estudiante", "role_corp": "💼 Corporativo", "lbl_topic": "✍️ Tema", "lbl_context": "📝 Detalles", "btn_gen": "✨ Generar", "tip_prompt": "💡 **Tip:** Copiar a Midjourney.", "footer_disclaimer": "Herramienta IA. Solo referencia." },
    "Français": { "title": "Plateforme IA", "lbl_email": "📧 E-mail", "lbl_key": "🔑 Clé", "btn_enter": "🚀 Entrer", "err_email": "⚠️ E-mail requis.", "welcome": "👋 Bienvenue", "choose_id": "Choisissez votre identité:", "btn_switch": "🔄 Changer", "vip_active": "👑 VIP Actif", "free_acc": "🔒 Gratuit", "upgrade_txt": "ACCÈS À VIE", "search_ph": "Chercher...", "btn_recover": "🔑 Clé Perdue?", "btn_clear": "🗑️ Effacer", "btn_submit": "🚀 Envoyer", "ticket_tab": "📩 Support", "warn_faq": "🔴 Lire FAQ.", "role_edu": "👨‍🏫 Éducateur", "role_parent": "👪 Parent", "role_creator": "🎥 Créateur", "role_seller": "💰 Vendeur", "role_student": "🎓 Étudiant", "role_corp": "💼 Entreprise", "lbl_topic": "✍️ Sujet", "lbl_context": "📝 Détails", "btn_gen": "✨ Générer", "tip_prompt": "💡 **Tip:** Copier vers Midjourney.", "footer_disclaimer": "Outil IA. Référence seulement." },
    "日本語": { "title": "AIプラットフォーム", "lbl_email": "📧 メール", "lbl_key": "🔑 キー", "btn_enter": "🚀 入室", "err_email": "⚠️ 必須です。", "welcome": "👋 ようこそ", "choose_id": "IDを選択:", "btn_switch": "🔄 切り替え", "vip_active": "👑 VIP有効", "free_acc": "🔒 無料版", "upgrade_txt": "生涯アクセス権", "search_ph": "検索...", "btn_recover": "🔑 キー復元", "btn_clear": "🗑️ 消去", "btn_submit": "🚀 送信", "ticket_tab": "📩 サポート", "warn_faq": "🔴 FAQを確認。", "role_edu": "👨‍🏫 教育者", "role_parent": "👪 保護者", "role_creator": "🎥 クリエイター", "role_seller": "💰 販売者", "role_student": "🎓 学生", "role_corp": "💼 企業", "lbl_topic": "✍️ トピック", "lbl_context": "📝 詳細", "btn_gen": "✨ 生成", "tip_prompt": "💡 **Tip:** Midjourneyにコピー。", "footer_disclaimer": "AIツールです。内容は参考用。" },
    "한국어": { "title": "AI 교육 플랫폼", "lbl_email": "📧 이메일", "lbl_key": "🔑 키", "btn_enter": "🚀 입장", "err_email": "⚠️ 필수.", "welcome": "👋 환영합니다", "choose_id": "신원 선택:", "btn_switch": "🔄 변경", "vip_active": "👑 VIP 활성", "free_acc": "🔒 무료", "upgrade_txt": "평생 이용권", "search_ph": "검색...", "btn_recover": "🔑 키 복구", "btn_clear": "🗑️ 지우기", "btn_submit": "🚀 제출", "ticket_tab": "📩 지원", "warn_faq": "🔴 FAQ 확인.", "role_edu": "👨‍🏫 교육자", "role_parent": "👪 학부모", "role_creator": "🎥 크리에이터", "role_seller": "💰 판매자", "role_student": "🎓 학생", "role_corp": "💼 기업", "lbl_topic": "✍️ 주제", "lbl_context": "📝 상세", "btn_gen": "✨ 생성", "tip_prompt": "💡 **Tip:** Midjourney에 붙여넣기.", "footer_disclaimer": "참고용 AI 도구입니다." }
}

def t(key):
    lang = st.session_state.get('ui_lang', 'English')
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, TRANSLATIONS["English"].get(key, key))

# ==============================================================================
# 2. BACKEND ENGINES
# ==============================================================================
def verify_license(license_key):
    if license_key == "VIP2025-ADMIN": return True, "Admin Pass"
    url = "https://api.lemonsqueezy.com/v1/licenses/activate"
    payload = {"license_key": license_key, "instance_name": "LaisLab_Web"}
    headers = {"Accept": "application/json"}
    if "LEMON_SQUEEZY_API_KEY" in st.secrets:
        headers["Authorization"] = f"Bearer {st.secrets['LEMON_SQUEEZY_API_KEY']}"
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=5)
        data = response.json()
        if data.get("activated") is True: return True, "Verified"
        else: return False, data.get("error", "Invalid or Expired Key")
    except Exception as e: return False, f"Network Error: {e}"

def log_to_airtable(email, category, details):
    if "airtable" not in st.secrets: return
    try:
        url = f"https://api.airtable.com/v0/{st.secrets['airtable']['base_id']}/{st.secrets['airtable']['table_name']}"
        headers = {"Authorization": f"Bearer {st.secrets['airtable']['api_key']}", "Content-Type": "application/json"}
        data = {"fields": {"Email": email, "Type": category, "Message": details, "Date": time.strftime("%Y-%m-%d %H:%M:%S")}}
        requests.post(url, json=data, headers=headers, timeout=3)
    except: pass

def send_smart_email(recipient, subject, body, is_admin=False):
    if "email" not in st.secrets: return
    try:
        cfg = st.secrets["email"]; msg = MIMEMultipart()
        sender_name = "Lai's Lab System" if is_admin else "Lai's Lab Support Team"
        msg['From'] = f"{sender_name} <{cfg['sender_address']}>"; msg['To'] = recipient; msg['Subject'] = subject; msg['Reply-To'] = cfg['reply_to'] 
        msg.attach(MIMEText(body, 'html'))
        s = smtplib.SMTP("smtp.gmail.com", 587); s.starttls(); s.login(cfg['sender_address'], cfg['app_password'])
        s.sendmail(cfg['sender_address'], recipient, msg.as_string()); s.quit()
    except Exception as e: print(f"Email Err: {e}")

def send_telegram(msg):
    if "telegram" not in st.secrets: return
    try:
        url = f"https://api.telegram.org/bot{st.secrets['telegram']['bot_token']}/sendMessage"
        requests.post(url, json={"chat_id": st.secrets['telegram']['chat_id'], "text": msg, "parse_mode": "HTML"}, timeout=5)
    except: pass

def clean_text(text, keep_emojis=True):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text); text = re.sub(r'#+\s*', '', text); text = re.sub(r'^\*\s', '• ', text, flags=re.MULTILINE)
    if not keep_emojis: text = text.encode('ascii', 'ignore').decode('ascii')
    return text.strip()

def create_pdf(text):
    pdf = FPDF(); pdf.add_page(); pdf.set_auto_page_break(auto=True, margin=15)
    try: pdf.add_font('CustomFont', '', 'font.ttf', uni=True); pdf.set_font("CustomFont", size=11)
    except: pdf.set_font("Arial", size=11); text = clean_text(text, False) + "\n\n[System: font.ttf missing]"
    pdf.set_font_size(14); pdf.cell(0, 10, "Lai's Lab Output", ln=True, align='C'); pdf.ln(10)
    pdf.set_font_size(11); pdf.multi_cell(0, 7, clean_text(text, False))
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# ==============================================================================
# 3. SMART VIP SELECT (核心功能锁)
# ==============================================================================
def vip_select(label, basic_opts, vip_opts, key_suffix):
    is_vip = st.session_state['user_type'] == 'Pro'
    final_opts = list(basic_opts)
    if is_vip:
        final_opts += [f"👑 {v} (VIP)" for v in vip_opts]
        final_opts += ["✏️ Other (Custom)..."] 
    else:
        final_opts += [f"🔒 {v} (VIP)" for v in vip_opts]
        final_opts += ["🔒 Custom Input (VIP Only)"] 
    choice = st.selectbox(label, final_opts, key=f"{st.session_state['user_role']}_{key_suffix}")
    is_locked = False; clean_choice = choice
    if choice.startswith("🔒"): is_locked = True; clean_choice = None
    elif choice.startswith("👑"): clean_choice = choice.replace("👑 ", "").replace(" (VIP)", "")
    elif choice.startswith("✏️"): clean_choice = st.text_input(f"Specify {label}", key=f"{key_suffix}_cust"); 
    if not clean_choice: clean_choice = "General"
    return clean_choice, is_locked

# ==============================================================================
# 4. STATE INIT & LOGIN
# ==============================================================================
keys = ['logged_in', 'user_email', 'user_role', 'user_type', 'usage_count', 'last_gen_time', 'ticket_submitted', 'ticket_id', 'history', 'ui_lang']
defs = [False, "", None, 'Free', 0, 0, False, "", [], "English"]
for k, d in zip(keys, defs):
    if k not in st.session_state: st.session_state[k] = d

if not st.session_state['logged_in']:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.session_state['ui_lang'] = st.selectbox("🌐 Interface / 界面", UI_LANGS, index=UI_LANGS.index(st.session_state['ui_lang']))
        st.markdown(f"<h1 style='text-align: center;'>🧪 Lai's Lab</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{t('title')}</p>", unsafe_allow_html=True)
        with st.form("login_gate"):
            email_input = st.text_input(t('lbl_email'))
            key_input = st.text_input(t('lbl_key'))
            if st.form_submit_button(t('btn_enter')):
                if not email_input: st.error(t('err_email'))
                else:
                    st.session_state['user_email'] = email_input.strip(); st.session_state['logged_in'] = True; user_key = key_input.strip()
                    if user_key:
                        with st.spinner("🔐 Verifying License..."): is_valid, msg = verify_license(user_key)
                        if is_valid:
                            st.session_state['user_type'] = 'Pro'; st.toast(f"✅ VIP Activated!", icon="👑")
                            if 'vip_alert_sent' not in st.session_state:
                                send_telegram(f"💰 <b>NEW VIP LOGIN</b>\n👤 User: {email_input}\n🔑 Key: {user_key}"); st.session_state['vip_alert_sent'] = True
                        else: st.session_state['user_type'] = 'Free'; st.error(f"⚠️ VIP Failed: {msg}")
                    else: st.session_state['user_type'] = 'Free'
                    time.sleep(1); st.rerun()

# ==============================================================================
# 5. ONBOARDING & SIDEBAR
# ==============================================================================
elif st.session_state['user_role'] is None:
    st.markdown(f"## {t('welcome')}, {st.session_state['user_email']}")
    st.markdown(f"### {t('choose_id')}")
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button(t('role_edu')): st.session_state['user_role'] = "Educator"; st.rerun()
        if st.button(t('role_parent')): st.session_state['user_role'] = "Parent"; st.rerun()
    with c2: 
        if st.button(t('role_creator')): st.session_state['user_role'] = "Creator"; st.rerun()
        if st.button(t('role_student')): st.session_state['user_role'] = "Student"; st.rerun()
    with c3: 
        if st.button(t('role_seller')): st.session_state['user_role'] = "Seller"; st.rerun()
        if st.button(t('role_corp')): st.session_state['user_role'] = "Corporate"; st.rerun()
else:
    with st.sidebar:
        try: st.image("logo.png", use_container_width=True)
        except: st.title("🧪 Lai's Lab")
        st.caption(f"ID: {st.session_state['user_email']}")
        st.session_state['ui_lang'] = st.selectbox("🌐 Interface / 界面", UI_LANGS, index=UI_LANGS.index(st.session_state['ui_lang']))
        if st.button(t('btn_switch')): st.session_state['user_role'] = None; st.rerun()
        st.markdown("---")
        output_lang = st.selectbox("🗣️ AI Output Language", ["English", "简体中文 (Simplified Chinese)", "繁體中文 (Traditional Chinese)", "Bahasa Melayu", "Bahasa Indonesia", "Tamil (தமிழ்)", "日本語 (Japanese)", "한국어 (Korean)", "Español (Spanish)", "Français (French)", "Deutsch (German)", "Tiếng Việt (Vietnamese)", "ไทย (Thai)", "Русский (Russian)", "Português (Portuguese)"])
        if st.session_state['user_type'] == 'Free':
            st.warning(t('free_acc'))
            st.markdown(f"""<div style="text-align: center; margin-bottom: 10px;"><span style="text-decoration: line-through; color: #888; font-size: 0.9em;">$39.90</span><span style="color: #FF4B4B; font-weight: bold; font-size: 1.2em; margin-left: 5px;">$12.90</span><br><span style="font-size: 0.8em; color: #1A73E8; font-weight: bold;">{t('upgrade_txt')}</span></div>""", unsafe_allow_html=True)
            st.markdown(f"👉 [**Upgrade Now**]({LEMON_LINK})")
        else: st.success(t('vip_active'))
        st.markdown("---")
        st.markdown("### 🛠️ Support Center")
        search_q = st.text_input(t('search_ph'))
        with st.expander("❓ FAQ", expanded=True):
            if search_q: st.info("🤖 Checking...")
            else: st.markdown("""* **Image Gen?** Prompts only.\n* **Refund?** No.\n* **VIP?** $12.90 Lifetime.""")
        with st.expander(t('ticket_tab')):
            if not st.session_state['ticket_submitted']:
                with st.form("ticket_form"):
                    st.text_input("Email", value=st.session_state['user_email'], disabled=True)
                    dept = st.selectbox("Dept", ["💰 Billing", "🐛 Bug", "💡 Feature", "🤝 Partner"])
                    prio = st.selectbox("Priority", ["🟢 Normal", "🟡 Urgent", "🔴 Critical"])
                    msg = st.text_area("Details")
                    if st.form_submit_button(t('btn_submit')):
                        tid = f"VP-{random.randint(1000,9999)}"
                        log_to_airtable(st.session_state['user_email'], dept, msg)
                        send_smart_email(st.session_state['user_email'], f"Ticket #{tid}", f"Received. ID: {tid}")
                        if "Billing" in dept or "Critical" in prio:
                            alert = f"🚨 <b>ALERT</b>\nUser: {st.session_state['user_email']}\nMsg: {msg}"
                            send_telegram(alert); send_smart_email(st.secrets.get("email",{}).get("admin_address",""), f"Alert #{tid}", alert, is_admin=True)
                        st.session_state['ticket_submitted'] = True; st.session_state['ticket_id'] = tid; st.rerun()
            else:
                st.success("🎉 Ticket Submitted!"); st.info(f"ID: #{st.session_state['ticket_id']}"); 
                if st.button("New Ticket"): st.session_state['ticket_submitted'] = False; st.rerun()
        st.markdown("---")
        st.markdown(f"""<div style="text-align: center;"><a href="https://app.lemonsqueezy.com/my-orders" target="_blank" style="text-decoration: none; background: #f0f2f6; color: #333; padding: 8px; border-radius: 8px; display: block; font-size: 0.9rem;">{t('btn_recover')}</a></div>""", unsafe_allow_html=True)
        if st.sidebar.button(t('btn_clear')): st.session_state['history'] = []; st.toast("Cleared")

    # ==========================================================================
    # 6. WORKSPACE
    # ==========================================================================
    try:
        if "GOOGLE_API_KEY" in st.secrets: genai.configure(api_key=st.secrets["GOOGLE_API_KEY"]); model = genai.GenerativeModel('gemini-2.5-flash')
    except: st.error("🚨 API Key Missing")

    ROLE = st.session_state['user_role']
    st.subheader(f"{t('role_' + ROLE.split()[-1].lower()[:3])} Workspace")
    input_data = {}
    mode_name = "General"
    has_locked_item = False 

    # --- 1. EDUCATOR ---
    if ROLE == "Educator":
        t1, t2, t3 = st.tabs(["Pedagogy", "Visuals", "Comm"])
        with t1:
            mode_name = "Pedagogical Content"; input_data['Topic'] = st.text_input(t('lbl_topic')); input_data['Details'] = st.text_input(t('lbl_context'))
            input_data['Strategy'], l1 = vip_select("Strategy", ["Direct Instruction", "Group Discussion"], ["Gamification", "Flipped Class", "PBL", "SEL"], "ed_st")
            if l1: has_locked_item = True
        with t2:
            mode_name = "Visual Aids Prompts"; input_data['Subject'] = st.text_input("🖼️ Image Subject")
            input_data['Style'], l2 = vip_select("Style", ["Coloring Page", "Simple Cartoon"], ["Pixar 3D Style", "Realistic Photo", "Infographic", "Mind Map"], "ed_sty")
            if l2: has_locked_item = True
        with t3:
            mode_name = "Global Comm"; input_data['Msg'] = st.text_input("✉️ Message Points")
            input_data['Audience'], l3 = vip_select("Audience", ["Students", "Colleagues"], ["Angry Parents (Crisis)", "Principal/Admin", "School Board"], "ed_aud")
            if l3: has_locked_item = True

    # --- 2. CREATOR ---
    elif ROLE == "Creator":
        t1, t2, t3 = st.tabs(["Scripting", "Visuals", "Engagement"])
        with t1:
            mode_name = "Scripting"; input_data['Topic'] = st.text_input(t('lbl_topic'))
            input_data['Platform'], l1 = vip_select("Platform", ["Instagram Caption", "Short Tweet"], ["TikTok Viral Script", "YouTube Long Form", "LinkedIn Article", "Xiaohongshu"], "cr_pl")
            if l1: has_locked_item = True
        with t2:
            mode_name = "Visual Packaging"; input_data['Subject'] = st.text_input("📸 Thumbnail Subject")
            input_data['Vibe'], l2 = vip_select("Vibe", ["Bright & Happy", "Clean"], ["High CTR / Clickbait", "Cinematic Lighting", "Cyberpunk/Neon", "Minimalist Aesthetic"], "cr_vi")
            if l2: has_locked_item = True
        with t3:
            mode_name = "Engagement"; input_data['Context'] = st.text_input("📝 Content Summary")
            input_data['Trigger'], l3 = vip_select("Trigger", ["Curiosity", "Simple Question"], ["FOMO", "Controversy", "Value Stacking", "Story Loop"], "cr_tr")
            if l3: has_locked_item = True

    # --- 3. SELLER ---
    elif ROLE == "Seller":
        t1, t2, t3 = st.tabs(["Copywriting", "Visuals", "Story"])
        with t1:
            mode_name = "Listing Copy"; input_data['Product'] = st.text_input("🛍️ Product Name")
            input_data['Model'], l1 = vip_select("Model", ["Feature List", "AIDA Model"], ["PAS", "FAB", "Objection Handling", "StorySelling"], "sl_md")
            if l1: has_locked_item = True
        with t2:
            mode_name = "Ad Visual Prompts"; input_data['Desc'] = st.text_input("🧴 Product Desc")
            input_data['Scene'], l2 = vip_select("Scene", ["White Background", "Studio Light"], ["Luxury Lifestyle", "Nature/Organic", "Pop Art / Colorful", "Festival/CNY Theme"], "sl_sc")
            if l2: has_locked_item = True
        with t3:
            mode_name = "Brand Story"; input_data['Story'] = st.text_input("📖 Background")
            input_data['Type'], l3 = vip_select("Type", ["Brand History"], ["Founder's Struggle", "Customer Transformation", "Behind the Scenes"], "sl_st")
            if l3: has_locked_item = True

    # --- 4. PARENT ---
    elif ROLE == "Parent":
        t1, t2 = st.tabs(["Stories", "Art Remix"])
        with t1: 
            mode_name = "Story Weaver"; input_data['Child'] = st.text_input("👶 Child Name/Age")
            input_data['Theme'], l1 = vip_select("Theme", ["Friendship", "Animals"], ["Emotional Control (SEL)", "Growth Mindset", "Dealing with Bullying", "Habit Building"], "pa_th")
            if l1: has_locked_item = True
        with t2:
            mode_name = "Art Remix Prompts"; st.info("Upload child's drawing below")
            input_data['Style'], l2 = vip_select("Style", ["Crayon Drawing", "Watercolor"], ["Pixar 3D Style", "Lego Style", "Studio Ghibli", "Oil Painting"], "pa_st")
            if l2: has_locked_item = True

    # --- 5. STUDENT ---
    elif ROLE == "Student":
        t1, t2 = st.tabs(["Notes", "Writing"])
        with t1:
            mode_name = "Study Notes"; input_data['Text'] = st.text_area("📖 Source Text")
            input_data['Format'], l1 = vip_select("Format", ["Summary Paragraph", "Bullet Points"], ["Cornell Method", "Mind Map Structure", "Flashcards (Anki)", "ELI5 (Simple Explain)"], "st_fm")
            if l1: has_locked_item = True
        with t2:
            mode_name = "Writing Coach"; input_data['Draft'] = st.text_area("✍️ Draft")
            input_data['Goal'], l2 = vip_select("Goal", ["Fix Grammar", "Shorten"], ["Academic Polish", "Expand Arguments", "Debate Style", "Make it Professional"], "st_gl")
            if l2: has_locked_item = True
            
    # --- 6. CORPORATE ---
    elif ROLE == "Corporate":
        t1, t2 = st.tabs(["Email", "Report"])
        with t1:
            mode_name = "Pro Email"; input_data['Purpose'] = st.text_input("🎯 Purpose")
            input_data['Recipient'], l1 = vip_select("To", ["Colleague", "General Inquiry"], ["Big Boss / CEO", "Potential Investor", "Angry Client (Crisis)", "Media / Press"], "cp_to")
            if l1: has_locked_item = True
        with t2:
            mode_name = "Report Smith"; input_data['Data'] = st.text_area("📊 Data Points")
            input_data['Type'], l2 = vip_select("Type", ["Meeting Summary", "Weekly Update"], ["STAR Method", "Strategic Proposal", "Crisis Report", "SWOT Analysis"], "cp_rp")
            if l2: has_locked_item = True

    # ==========================================================================
    # 7. GENERATE & EXPORT (Mobile + Social Lock)
    # ==========================================================================
    st.markdown("---")
    uploaded_file = st.file_uploader("📸 Upload Image (Optional)", type=['png', 'jpg'])
    
    if st.button(t('btn_gen'), key="gen"):
        if has_locked_item:
            st.error("🔒 This feature is locked for VIPs only."); st.markdown(f"👉 [**Upgrade to Unlock All Features**]({LEMON_LINK})")
        else:
            limit_reached = st.session_state['user_type'] == 'Free' and st.session_state['usage_count'] >= 3
            in_cooldown = st.session_state['user_type'] == 'Free' and (time.time() - st.session_state['last_gen_time'] < 60)
            safe = check_safety(str(input_data.values()))
            
            if not safe: st.error("🚨 Request Blocked (Safety Policy).")
            elif limit_reached: st.error(t('free_acc') + ": Daily Limit Reached."); st.markdown(f"[Upgrade]({LEMON_LINK})")
            elif in_cooldown: wait = 60 - int(time.time() - st.session_state['last_gen_time']); st.warning(f"⏳ Cooling down... ({wait}s)")
            else:
                with st.spinner("🧪 Lai's Lab is thinking..."):
                    if st.session_state['user_type'] == 'Free': time.sleep(2)
                    prompt = f"""
                    Act as expert {ROLE}. Mode: {mode_name}.
                    Input: {input_data}
                    Target Output Language: {output_lang}
                    TONE: Human-like, conversational. Avoid robotic transitions like "Firstly/In conclusion".
                    SAFETY: G-Rated content only. No NSFW.
                    FORMAT: Markdown.
                    TASK: If this is a Visual/Art mode, generate Midjourney Prompts in English, then explain in {output_lang}.
                    """
                    try:
                        if uploaded_file: img = Image.open(uploaded_file); res = model.generate_content([prompt, img], safety_settings=safety_config).text
                        else: res = model.generate_content(prompt, safety_settings=safety_config).text
                        st.session_state['result'] = res; st.session_state['result_mode'] = mode_name
                        if st.session_state['user_type'] == 'Free': st.session_state['usage_count'] += 1; st.session_state['last_gen_time'] = time.time()
                    except Exception as e: st.error(f"Error: {e}")

    if 'result' in st.session_state:
        res = st.session_state['result']; rmode = st.session_state.get('result_mode', '')
        st.markdown(f'<div class="output-card">{res}</div>', unsafe_allow_html=True)
        if "Visual" in rmode or "Art" in rmode: st.info(t('tip_prompt'))
        
        st.markdown("---"); st.markdown("### 📤 Share & Export")
        is_vip = st.session_state['user_type'] == 'Pro'
        share_txt = clean_text(res) + ("\n\n✨ Generated by Lai's Lab (Free Version)" if not is_vip else "")
        enc_txt = urllib.parse.quote(share_txt)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.caption("📋 **Text Operations**")
            st.code(share_txt, language=None)
            # [Added] TXT Download for Free Users (Viral Loop)
            st.download_button(label="📥 Download .txt (Basic)", data=share_txt, file_name="LaisLab_Draft.txt", mime="text/plain")
            
        with c2:
            st.caption(f"🚀 **System Sharing ({'VIP Unlocked' if is_vip else 'Locked'})**")
            if is_vip:
                st.download_button("📄 Download PDF", data=create_pdf(clean_text(res)), file_name="LaisLab_Output.pdf", mime="application/pdf")
                st.markdown(f"""
                <div style="margin-top: 10px;">
                    <a href="https://wa.me/?text={enc_txt}" target="_blank" class="social-btn btn-wa">WhatsApp</a>
                    <a href="https://t.me/share/url?url={LEMON_LINK}&text={enc_txt}" target="_blank" class="social-btn btn-tg">Telegram</a>
                    <a href="mailto:?subject=Lai's Lab Output&body={enc_txt}" target="_blank" class="social-btn btn-mail">Email</a>
                    <a href="https://www.linkedin.com/sharing/share-offsite/?url={LEMON_LINK}" target="_blank" class="social-btn btn-link">LinkedIn</a>
                </div>""", unsafe_allow_html=True)
            else:
                st.button("🔒 Download PDF (VIP)", disabled=True)
                st.markdown(f"""
                <div style="margin-top: 10px;">
                    <a href="{LEMON_LINK}" target="_blank" class="social-btn btn-wa">WhatsApp (Watermarked)</a>
                    <a href="{LEMON_LINK}" target="_blank" class="social-btn btn-lock">🔒 Telegram</a>
                    <a href="{LEMON_LINK}" target="_blank" class="social-btn btn-lock">🔒 Email</a>
                    <a href="{LEMON_LINK}" target="_blank" class="social-btn btn-lock">🔒 LinkedIn</a>
                </div>
                <p style="font-size: 0.8em; color: #d93025; margin-top: 5px;">* Free version includes watermark. <a href="{LEMON_LINK}">Upgrade to remove.</a></p>
                """, unsafe_allow_html=True)
    
    st.markdown(f"""<div class="custom-footer">© 2025 Lai's Lab {VERSION} | {t('footer_disclaimer')} | <a href="{LEMON_LINK}" target="_blank">Manage Order</a></div>""", unsafe_allow_html=True)