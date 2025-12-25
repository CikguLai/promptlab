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
    
    /* 红色温馨提示词 */
    .warning-text { 
        color: #FF4B4B; font-weight: bold; font-size: 14px; 
        margin-top: 10px; margin-bottom: 10px; padding: 10px;
        background-color: #ffe8e8; border-radius: 5px; border-left: 5px solid #FF4B4B;
    }
    
    /* 社交链接样式 */
    .social-link {
        display: inline-block; text-decoration: none; color: white;
        background-color: #2E86C1; padding: 8px 12px; border-radius: 5px;
        text-align: center; width: 100%; margin: 2px; font-size: 14px;
    }
    .social-link:hover { opacity: 0.8; color: white; }
    
    /* App 按钮样式 */
    .app-link {
        display: inline-block; text-decoration: none; color: white;
        background-color: #333; padding: 6px 10px; border-radius: 15px;
        text-align: center; width: 100%; font-size: 12px; border: 1px solid #555;
    }
    .xhs { background-color: #FF2442; }
    .insta { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); }
    .tiktok { background-color: #000000; }
    
    /* 禁用按钮样式 */
    .disabled-link {
        display: inline-block; text-decoration: none; color: #999;
        background-color: #eee; padding: 6px 10px; border-radius: 5px;
        text-align: center; width: 100%; border: 1px solid #ddd; pointer-events: none;
    }
    
    /* 页脚法律声明样式 */
    .footer-legal {
        font-size: 10px; color: #888; text-align: center; margin-top: 20px;
        padding-top: 10px; border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 核心数据库
# ==========================================

LANG_DICT = {
    "English": {"login": "Login (PRO)", "guest": "Free Guest", "role": "Choose Role", "back": "Back", "logout": "Logout"},
    "简体中文": {"login": "PRO 登入", "guest": "免费试用", "role": "选择角色", "back": "返回", "logout": "退出"},
    "Bahasa Melayu": {"login": "Log Masuk (PRO)", "guest": "Tetamu Percuma", "role": "Pilih Peranan", "back": "Kembali", "logout": "Keluar"}
}

OUTPUT_LANGUAGES = [
    "English (Default)", "Malay (Bahasa Melayu)", "Chinese Simplified (简体中文)", 
    "Chinese Traditional (繁體中文)", "Tamil (தமிழ்)", "Arabic (العربية)", 
    "Japanese (日本語)", "Korean (한국어)", "Indonesian (Bahasa Indonesia)", 
    "Thai (ไทย)", "Vietnamese (Tiếng Việt)", "French (Français)", 
    "Spanish (Español)", "German (Deutsch)", "Russian (Русский)"
]

COMMON_TONES = [
    "🌟 Professional & Confident (专业自信)",
    "🥰 Empathetic & Warm (温暖共情)",
    "🔥 Persuasive & Bold (极具说服力)",
    "👻 Witty & Humorous (幽默风趣)",
    "📖 Storyteller / Narrative (故事叙述感)",
    "⚡ Urgent / FOMO (紧迫感)",
    "🧘 Calm & Minimalist (冷静极简)",
    "🎓 Academic & Formal (学术正式)"
]

MODES_DB = {
    "Global Educator": {
        "🟢 Pedagogy": {
            "dd": ["Direct Instruction", "Gamification", "Socratic Method", "Project-Based Learning", "STEAM Education"], 
            "tones": COMMON_TONES, "in": "Topic & Level", "desc": "Lesson Plans."
        },
        "🔵 Visuals": {
            "dd": ["Pixar 3D Style", "Realistic Photography", "Infographic / Poster", "Watercolor Art", "Scientific Schematic"], 
            "in": "Visual Description", "desc": "AI Art Prompts."
        },
        "🟣 Comm & Social": {
            "dd": ["Student Showcase", "Parent Message (WhatsApp)", "Official Proposal", "Behavior Report", "Classroom Newsletter"], 
            "tones": COMMON_TONES, "in": "Context", "desc": "Letters & Posts."
        }
    },
    "Global Creator": {
        "🟢 Scripting": {
            "dd": ["TikTok/Reels (Short)", "YouTube Tutorial (Long)", "Live Stream Script", "Storytelling Vlog", "Podcast Outline"], 
            "tones": COMMON_TONES, "in": "Video Topic", "desc": "Scripts."
        },
        "🔵 Thumbnail": {
            "dd": ["High CTR (Shocked)", "Aesthetic / Clean", "Cinematic Poster", "Tech / Neon", "Before & After"], 
            "in": "Image Scenario", "desc": "Cover Art."
        },
        "🟣 Marketing": {
            "dd": ["Xiaohongshu (Soft Sell)", "Facebook Ad (Hard Sell)", "Instagram Caption", "LinkedIn Thought Leader", "Email Newsletter"], 
            "tones": COMMON_TONES, "in": "Product", "desc": "Social Copy."
        }
    },
    "Global Parent": {
        "🟢 Story Time": {
            "dd": ["Bedtime Story", "Behavior Lesson", "Hero Adventure", "Science Story", "Cultural Tale"], 
            "tones": ["😴 Calming/Sleepy", "🦸 Exciting/Heroic", "❤️ Heartwarming", "🤣 Funny/Silly", "🤔 Mystery/Curious"],
            "in": "Child Name/Age", "desc": "Stories."
        },
        "🔵 Activities": {
            "dd": ["DIY Craft Guide", "Indoor Game", "Science Experiment", "Scavenger Hunt", "Cooking Recipe"], 
            "tones": ["🎨 Creative", "🔬 Educational", "🎉 Fun & Energetic"],
            "in": "Interest", "desc": "Activities."
        },
        "🟣 Tutor": {
            "dd": ["Explain like I'm 5", "Homework Helper", "Quiz Generator", "Vocabulary Builder", "Math Solver"], 
            "tones": ["👩‍🏫 Encouraging Teacher", "🤖 Logical/Direct", "🧩 Gamified/Fun"],
            "in": "Question", "desc": "Tutor."
        }
    },
    "Global Seller": {
        "🟢 Copywriting": {
            "dd": ["PAS (Pain-Agitate-Solve)", "AIDA (Attention-Action)", "Storytelling Sales", "FAQ Generator", "Brand Story"], 
            "tones": COMMON_TONES, "in": "Product USP", "desc": "Sales Copy."
        },
        "🔵 Product Shot": {
            "dd": ["Studio White BG", "Lifestyle Cozy", "Luxury Gold", "Nature/Outdoor", "Cyberpunk/Neon"], 
            "in": "Product Item", "desc": "Photography."
        },
        "🟣 Support": {
            "dd": ["Apology Letter", "Review Request", "Complaint Reply", "Sale Announcement", "Crisis Statement"], 
            "tones": ["🤝 Apologetic & Sincere", "💼 Professional & Firm", "💖 Gratitude & Warm"],
            "in": "Issue", "desc": "Customer Service."
        }
    },
    "Global Student": {
        "🟢 Study": {
            "dd": ["Summarizer", "Simplifier (ELI5)", "Flashcard Maker", "Translator", "Grammar Fixer"], 
            "tones": ["📚 Academic", "⚡ Quick/Brief", "🗣️ Conversational"],
            "in": "Text/Topic", "desc": "Study Notes."
        },
        "🔵 Project": {
            "dd": ["Essay Outline", "Presentation Script", "Thesis Generator", "Lab Report", "Group Roles"], 
            "tones": COMMON_TONES, "in": "Topic", "desc": "Projects."
        },
        "🟣 Career": {
            "dd": ["Resume Builder", "Cover Letter", "Interview Q&A", "LinkedIn Bio", "Cold Email"], 
            "tones": ["💼 Corporate Professional", "🚀 Startup/Energetic", "🎨 Creative/Unique"],
            "in": "Role", "desc": "Career."
        }
    },
    "Global Corporate": {
        "🟢 Admin": {
            "dd": ["Meeting Minutes", "Email Drafter", "Proposal Outline", "Internal Memo", "Excel Formula"], 
            "tones": ["👔 Formal", "🤝 Collaborative", "⚡ Direct/Brief"],
            "in": "Context", "desc": "Admin."
        },
        "🔵 Strategy": {
            "dd": ["SWOT Analysis", "Competitor Analysis", "Business Model", "OKRs", "Risk Assessment"], 
            "in": "Business", "desc": "Strategy."
        },
        "🟣 HR & Team": {
            "dd": ["Job Description", "Team Building Idea", "Performance Review", "Onboarding Plan", "Conflict Resolution"], 
            "tones": ["⚖️ Fair & Balanced", "🚀 Motivational", "❤️ Empathetic"],
            "in": "Situation", "desc": "HR."
        }
    }
}

FAQ_DB = {
    "💰 Billing": [("Card rejected?", "Check international usage."), ("Cancel?", "Sidebar > Billing.")],
    "⚙️ Tech": [("Blank screen?", "Clear cache."), ("Lost Key?", "Use sidebar button.")],
    "🧠 Tips": [("Better prompts?", "Be specific."), ("Commercial use?", "Yes, it's yours.")]
}

# ==========================================
# 3. 辅助函数
# ==========================================

COPYRIGHT_FOOTER = "\n\n✨ Generated by PromptLab AI (Free Version)"

def clean_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'#+\s', '', text)
    return text.strip()

def get_text_download_link(text, filename="prompt.txt"):
    clean_text = clean_markdown(text)
    b64 = base64.b64encode(clean_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}" style="text-decoration:none;">📄 TXT (Clean)</a>'

def get_csv_download_link(text, is_pro, filename="prompt.csv"):
    if not is_pro: return f'<a href="#" class="disabled-link">📊 CSV (PRO)</a>'
    clean_text = clean_markdown(text)
    csv_content = f"Content\n{clean_text}"
    b64 = base64.b64encode(csv_content.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="text-decoration:none;">📊 CSV (Clean)</a>'

def get_pdf_download_link(text, is_pro, filename="prompt.pdf"):
    if not is_pro: return f'<a href="#" class="disabled-link">📑 PDF (PRO)</a>'
    clean_text = clean_markdown(text)
    b64 = base64.b64encode(clean_text.encode()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="text-decoration:none;">📑 PDF (Clean)</a>'

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
# 4. 页面逻辑
# ==========================================

if 'page' not in st.session_state: st.session_state.page = 1
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'user_tier' not in st.session_state: st.session_state.user_tier = "FREE"
if 'current_role' not in st.session_state: st.session_state.current_role = ""
if 'generated_result' not in st.session_state: st.session_state.generated_result = ""
if 'last_gen_time' not in st.session_state: st.session_state.last_gen_time = 0

if 'daily_gen_count' not in st.session_state: st.session_state.daily_gen_count = 0
if 'daily_img_count' not in st.session_state: st.session_state.daily_img_count = 0
if 'last_reset_date' not in st.session_state: st.session_state.last_reset_date = datetime.date.today()

if st.session_state.last_reset_date != datetime.date.today():
    st.session_state.daily_gen_count = 0
    st.session_state.daily_img_count = 0
    st.session_state.last_reset_date = datetime.date.today()

LIMITS = {
    "FREE": {"gen": 5, "img": 3, "chars": 500, "batch_gen": 1, "batch_img": 1},
    "PRO": {"gen": 100, "img": 200, "chars": 2000, "batch_gen": 50, "batch_img": 50}
}

# PAGE 1: LOGIN
if st.session_state.page == 1:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🧠 PromptLab AI</h1>", unsafe_allow_html=True)
        lang_choice = st.selectbox("🌐 Interface Language / 界面语言", list(LANG_DICT.keys()))
        labels = LANG_DICT.get(lang_choice, LANG_DICT["English"])
        with st.form("login_form"):
            st.markdown("### Login / 登入")
            email = st.text_input("📧 Email Address")
            key = st.text_input("🔑 Activation Key (Leave empty for Free Trial)", type="password")
            c1, c2 = st.columns(2)
            if c1.form_submit_button(f"🚀 {labels['login']}"):
                if "@" in email and key:
                    st.session_state.user_email = email
                    st.session_state.user_tier = "PRO"
                    st.session_state.page = 2
                    st.rerun()
                else: st.error("❌ Key Required for PRO.")
            if c2.form_submit_button(f"👤 {labels['guest']}"):
                if "@" in email:
                    st.session_state.user_email = email
                    st.session_state.user_tier = "FREE"
                    st.session_state.page = 2
                    st.rerun()
                else: st.warning("Enter Email.")

# PAGE 2: ROLE SELECTION
elif st.session_state.page == 2:
    c1, c2 = st.columns([1, 4])
    if c1.button("⬅️ Back"): st.session_state.page = 1; st.rerun()
    badge = "💎 PRO" if st.session_state.user_tier == "PRO" else "👤 FREE"
    st.markdown(f"### 👋 Hi, {st.session_state.user_email} ({badge})")
    roles = list(MODES_DB.keys())
    col1, col2, col3 = st.columns(3)
    for i, role in enumerate(roles):
        with [col1, col2, col3][i % 3]:
            if st.button(f"🎭\n{role}", key=f"role_{i}", use_container_width=True):
                st.session_state.current_role = role
                st.session_state.page = 3
                st.rerun()

# PAGE 3: DASHBOARD
elif st.session_state.page == 3:
    is_pro = st.session_state.user_tier == "PRO"
    limits = LIMITS["PRO"] if is_pro else LIMITS["FREE"]
    
    with st.sidebar:
        st.info(f"👤 {st.session_state.user_email}")
        if is_pro: st.success("💎 PRO PLAN")
        else: st.warning("👤 FREE PLAN")
        
        st.caption("📊 **Today's Usage**")
        st.progress(st.session_state.daily_gen_count / limits["gen"], text=f"Generations: {st.session_state.daily_gen_count}/{limits['gen']}")
        img_limit_display = "Unlimited*" if is_pro else f"{limits['img']}"
        st.progress(st.session_state.daily_img_count / limits["img"], text=f"Image Uploads: {st.session_state.daily_img_count}/{img_limit_display}")
        
        st.markdown("---")
        st.selectbox("Display Language", list(LANG_DICT.keys()))
        
        if not is_pro:
            st.markdown("### 🔓 Unlock PRO")
            st.link_button("💎 Upgrade ($12.90)", "#", type="primary")
            with st.expander("🏆 Benefits"):
                st.markdown(f"""
                | Feature | Free | PRO |
                | :--- | :--- | :--- |
                | **Batch Upload** | 1 File | **50 Files** |
                | **Bulk Generate** | 1x | **50x** |
                | **Images/Day** | 3 | **Unlimited*** |
                | **Wait Time** | 60s | Instant |
                """)
                st.caption("*Unlimited subject to Fair Use (200/day)")
        else: st.button("Billing Portal")
        
        with st.expander("🎫 Support"):
            with st.form("tick"):
                st.text_input("Subject")
                st.form_submit_button("Submit")
        
        st.markdown("---")
        if st.button("🚪 Logout"): st.session_state.clear(); st.rerun()

    bc1, bc2 = st.columns([1, 5])
    if bc1.button("⬅️ Roles"): st.session_state.page = 2; st.rerun()
    
    role = st.session_state.current_role; role_data = MODES_DB[role]
    st.title(f"🎭 {role}")
    
    mode_keys = list(role_data.keys())
    if is_pro: display_modes = mode_keys
    else: display_modes = [k if i == 0 else f"🔒 {k} (PRO)" for i, k in enumerate(mode_keys)]
    
    sel_label = st.radio("Select Mode:", display_modes, horizontal=True)
    if "🔒" in sel_label:
        real_mode = sel_label.replace("🔒 ", "").replace(" (PRO)", "")
        locked = True
    else: real_mode = sel_label; locked = False
    
    curr_data = role_data[real_mode]
    st.caption(f"💡 Info: {curr_data['desc']}"); st.markdown("---")

    if locked:
        st.error(f"🔒 Mode '{real_mode}' is for PRO users.")
        st.link_button("💎 Unlock Now", "#", type="primary")
    else:
        with st.container():
            c_in1, c_in2 = st.columns(2)
            with c_in1:
                opts = curr_data['dd'].copy()
                if is_pro: opts.append("✨ Custom / Write Own...")
                else: opts = opts[:3]; opts.append("🔒 More... (PRO)")
                
                choice = st.selectbox("👉 Select Option", opts)
                if "🔒" in choice: topic = "LOCKED"
                elif choice == "✨ Custom / Write Own...": topic = st.text_input("✍️ Custom Topic:")
                else: topic = choice
                
                tone_val = "Professional"
                if "tones" in curr_data:
                    tone_val = st.selectbox("🗣️ Tone of Voice (Human-like)", curr_data['tones'])
                
                batch_qty = 1
                if is_pro:
                    st.markdown("---")
                    batch_qty = st.number_input("⚡ Batch Quantity (1-50)", min_value=1, max_value=50, value=1)
            
            with c_in2:
                details = st.text_area(f"⌨️ {curr_data['in']}", placeholder=f"Max {limits['chars']} characters...", height=100)
                if len(details) > limits["chars"]:
                    st.error(f"⚠️ Text too long! ({len(details)}/{limits['chars']}).")
                    topic = "LOCKED"
                lang = st.selectbox("🌐 Output Language", OUTPUT_LANGUAGES)

            # === [Updated] Upload Image Section ===
            with st.expander("📸 Upload Images (Batch Analysis)"):
                if is_pro:
                    st.caption("💎 **PRO Plan**: Unlimited Uploads (Batch up to 50)")
                else:
                    st.caption(f"📊 **Free Plan**: {st.session_state.daily_img_count} / {limits['img']} used today")

                if st.session_state.daily_img_count >= limits["img"]:
                    st.error(f"❌ Daily Quota Exceeded ({limits['img']}/{limits['img']}). Please upgrade for unlimited.")
                    up_files = []
                else:
                    up_files = st.file_uploader("Upload Images (JPG/PNG)", type=["jpg", "png"], accept_multiple_files=True)
                    
                    if up_files:
                        if len(up_files) > limits["batch_img"]:
                            st.error(f"❌ Batch limit exceeded! Free plan allows {limits['batch_img']} image at a time.")
                            up_files = [] 
                        elif len(up_files) + st.session_state.daily_img_count > limits["img"]:
                            st.error(f"❌ This upload exceeds your daily limit of {limits['img']}. You have {limits['img'] - st.session_state.daily_img_count} left.")
                            up_files = []
                        else:
                            st.success(f"✅ {len(up_files)} image(s) ready for analysis.")

            if topic == "LOCKED":
                st.button("✨ GENERATE", disabled=True)
            else:
                if st.button(f"✨ GENERATE ({batch_qty})", type="primary"):
                    if st.session_state.daily_gen_count + batch_qty > limits["gen"]:
                        st.error(f"❌ Not enough daily generations left. Remaining: {limits['gen'] - st.session_state.daily_gen_count}")
                        st.stop()
                        
                    if not is_pro:
                        t_now = time.time()
                        if t_now - st.session_state.last_gen_time < 60:
                            st.warning(f"⏳ Free Cooldown: Wait {int(60 - (t_now - st.session_state.last_gen_time))}s.")
                            st.stop()
                        st.session_state.last_gen_time = t_now

                    st.session_state.daily_gen_count += batch_qty
                    if up_files: st.session_state.daily_img_count += len(up_files)
                    
                    bar = st.progress(0, "Analyzing...")
                    speed = 0.5 if is_pro else 2.0
                    for p in range(100):
                        time.sleep(speed/100)
                        bar.progress(p+1, f"Generating {batch_qty} variations...")
                    bar.empty()
                    
                    img_txt = f"[Image Context]: analyzed {len(up_files)} images.\n" if up_files else ""
                    
                    final_output = ""
                    for i in range(batch_qty):
                        final_output += f"""
=== Variation #{i+1} ===
[SYSTEM]: Act as a {role}. Tone: {tone_val}.
[CONTENT]: {topic} - {details}
{img_txt}
(Simulated human-like content for variation #{i+1}...)

"""
                    st.session_state.generated_result = final_output
                    st.success(f"✅ Successfully generated {batch_qty} variations!")

    if st.session_state.generated_result and not locked:
        st.markdown("### 📄 Result:")
        st.code(st.session_state.generated_result, language="text")
        
        share_content = clean_markdown(st.session_state.generated_result)
        if not is_pro: share_content += COPYRIGHT_FOOTER

        links = get_social_links(share_content)
        st.markdown("---"); st.caption("🚀 **Social Deck**")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown(f'<a href="{links["wa"]}" target="_blank" class="social-link">📱 WhatsApp</a>', unsafe_allow_html=True)
        with c2: st.markdown(f'<a href="{links["fb"]}" target="_blank" class="social-link">📘 Facebook</a>', unsafe_allow_html=True)
        with c3: st.markdown(f'<a href="{links["tw"]}" target="_blank" class="social-link">🐦 Twitter</a>', unsafe_allow_html=True)
        with c4: st.markdown(f'<a href="{links["li"]}" target="_blank" class="social-link">💼 LinkedIn</a>', unsafe_allow_html=True)
        with c5: st.markdown(f'<a href="{links["mail"]}" target="_blank" class="social-link">📧 Email</a>', unsafe_allow_html=True)

        st.caption("💾 **Utility Deck**")
        u1, u2 = st.columns([1.5, 2.5])
        with u1:
            b1, b2, b3 = st.columns(3)
            with b1: st.markdown(get_text_download_link(st.session_state.generated_result), unsafe_allow_html=True)
            with b2: st.markdown(get_pdf_download_link(st.session_state.generated_result, is_pro), unsafe_allow_html=True)
            with b3: st.markdown(get_csv_download_link(st.session_state.generated_result, is_pro), unsafe_allow_html=True)
        with u2:
            d1, d2, d3, d4 = st.columns([1.2,1,1,1])
            with d1: st.button("📋 Copy")
            with d2: st.markdown(f'<a href="https://instagram.com" target="_blank" class="app-link insta">📷 Insta</a>', unsafe_allow_html=True)
            with d3: st.markdown(f'<a href="https://xiaohongshu.com" target="_blank" class="app-link xhs">📕 XHS</a>', unsafe_allow_html=True)
            with d4: st.markdown(f'<a href="https://tiktok.com" target="_blank" class="app-link tiktok">🎵 TikTok</a>', unsafe_allow_html=True)

        st.caption("🔗 **System Deck**")
        s1, s2 = st.columns([1, 2])
        with s1: st.button("📤 System Share")
        with s2: st.text_input("Link", value="https://promptlab.ai/s/xyz", label_visibility="collapsed")

# ==========================================
# 5. 页脚 (Footer) - Updated
# ==========================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px; margin-top: 20px;'>
    <p>© 2025 <strong>Cikgu Lai Inc.</strong> | PromptLab AI® <em>Enterprise Edition v3.0</em></p>
    <p>
        <a href='#' style='color: #666; text-decoration: none;'>Terms of Service</a> | 
        <a href='#' style='color: #666; text-decoration: none;'>Privacy Policy</a> | 
        <a href='#' style='color: #666; text-decoration: none;'>Refund Policy</a>
    </p>
    <p style='font-size: 10px; color: #999; margin-top: 10px;'>
        <strong>Legal Disclaimer:</strong> This tool uses Artificial Intelligence. Results are for reference only. 
        Users are responsible for verifying facts before commercial use. Cikgu Lai Inc. assumes no liability for generated content.
        <br>免责声明：本工具使用人工智能技术，生成内容仅供参考。用户需自行核实内容的准确性，Cikgu Lai Inc. 不对生成内容的商业使用承担法律责任。
    </p>
</div>
""", unsafe_allow_html=True)