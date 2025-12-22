import streamlit as st
import time
import random
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==============================================================================
# 1. 系统配置 (已更新为 Lai's Lab)
# ==============================================================================
st.set_page_config(
    page_title="Lai's Lab AI",  # [修改] 浏览器标签页名字
    page_icon="🧪",             # [修改] 图标改为试管，呼应 Logo
    layout="wide",
    initial_sidebar_state="expanded"
)

VERSION = "V6.0.3 (Lai's Lab Edition)"

def inject_custom_css():
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        body { font-family: 'Inter', sans-serif; }
        .stButton>button {
            background-color: #1A73E8; color: white; border-radius: 8px; border: none;
            padding: 10px 24px; font-weight: 600; transition: all 0.3s;
        }
        .stButton>button:hover { background-color: #1557B0; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .output-card {
            background-color: #ffffff; border: 1px solid #dadce0; border-radius: 8px;
            padding: 20px; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .custom-footer {
            position: fixed; left: 0; bottom: 0; width: 100%;
            background-color: #f8f9fa; color: #5f6368; text-align: center;
            padding: 12px; font-size: 0.75rem; border-top: 1px solid #e0e0e0; z-index: 999;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==============================================================================
# 2. Session State (记忆库)
# ==============================================================================
if 'user_type' not in st.session_state: st.session_state['user_type'] = 'Free'
if 'usage_count' not in st.session_state: st.session_state['usage_count'] = 0
if 'last_generate_time' not in st.session_state: st.session_state['last_generate_time'] = 0

# ==============================================================================
# 3. 核心功能函数
# ==============================================================================
def send_telegram_alert(message):
    try:
        if "telegram" in st.secrets:
            token = st.secrets["telegram"]["TELEGRAM_BOT_TOKEN"]
            chat_id = st.secrets["telegram"]["TELEGRAM_CHAT_ID"]
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": message}, timeout=5)
    except: pass

def send_ticket_to_admin(user_email, issue_type, message):
    try:
        sender = st.secrets["EMAIL_SENDER_ADDRESS"]
        password = st.secrets["EMAIL_APP_PASSWORD"]
        admin = st.secrets["EMAIL_ADMIN_ADDRESS"]
        msg = MIMEMultipart()
        msg['From'] = f"Lai's Lab Support <{sender}>" # [修改] 发件人名字
        msg['To'] = admin
        msg['Subject'] = f"🧪 Ticket: {issue_type} from {user_email}"
        msg.add_header('Reply-To', user_email)
        body = f"User: {user_email}\nType: {issue_type}\nMsg: {message}"
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, password)
        server.sendmail(sender, admin, msg.as_string())
        server.quit()
        send_telegram_alert(f"🚨 [Lai's Lab] 新工单\n用户: {user_email}\n内容: {message}")
        return True
    except: return False

def get_tabs_by_persona(persona):
    mapping = {
        "👨‍🏫 Educator (老师)": ["Teaching Material", "Visual Aids", "Communication"],
        "🎥 Creator (创作者)": ["Scripts", "Thumbnails", "Social Captions"],
        "💰 Seller (电商)": ["Product Copy", "Ad Visuals", "Marketing Emails"],
        "👪 Parent (父母)": ["Story & Edu", "Activities", "School Reply"],
        "🎓 Student (学生)": ["Study Notes", "Mind Maps", "Presentation"],
        "💼 Corporate (职场)": ["Reports", "PPT Visuals", "Business Emails"]
    }
    return mapping.get(persona, ["Content", "Visual", "Social"])

def check_safety(text):
    forbidden = ["porn", "kill", "nude", "xxx", "gambling"]
    return not any(w in text.lower() for w in forbidden)

def handle_cooldown():
    current_time = time.time()
    time_diff = current_time - st.session_state['last_generate_time']
    if st.session_state['user_type'] == 'Free' and time_diff < 60 and st.session_state['last_generate_time'] != 0:
        st.warning(f"⏳ Lai's Lab Free Tier: Please wait {60-int(time_diff)}s.")
        return False
    st.session_state['last_generate_time'] = time.time()
    return True

# ==============================================================================
# 4. 侧边栏 (Sidebar)
# ==============================================================================
with st.sidebar:
    # [修改] Logo 显示区
    try:
        st.image("logo.png", use_container_width=True) # 优先显示您的 Lai's Lab 试管Logo
    except:
        st.title("Lai's Lab") # 如果没图，显示文字
    
    st.caption(f"{VERSION}")
    
    st.markdown("### 👤 Identity")
    selected_persona = st.selectbox("Select Persona", ["👨‍🏫 Educator (老师)", "🎥 Creator (创作者)", "💰 Seller (电商)", "👪 Parent (父母)", "🎓 Student (学生)", "💼 Corporate (职场)"], label_visibility="collapsed")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1: ui_lang = st.selectbox("🌐 UI", ["English", "中文", "Bahasa"])
    with col2: output_lang = st.selectbox("🗣️ Output", ["Same as UI", "English", "中文"])

    st.markdown("### 💎 Membership")
    if st.session_state['user_type'] == 'Free':
        st.progress(st.session_state['usage_count'] / 3, text=f"Free Limit: {3-st.session_state['usage_count']}/3 left")
        st.link_button("👑 Join Lai's Lab Pro", "https://cikgulai.lemonsqueezy.com/checkout") # [修改] 按钮文字
        with st.expander("🔑 Activate License"):
            k = st.text_input("Key")
            e = st.text_input("Email")
            if st.button("Activate"):
                if k and e:
                    st.session_state['user_type'] = 'Pro'
                    st.balloons()
                    send_telegram_alert(f"💰 [Lai's Lab] 收入进账!\nEmail: {e}")
                    st.rerun()
    else:
        st.success("👑 Lai's Lab VIP")
        st.link_button("🧾 Manage Subscription", "https://cikgulai.lemonsqueezy.com/billing")

    st.markdown("---")
    with st.expander("📩 Support / Ticket"):
        with st.form("ticket"):
            tm = st.text_input("Email")
            tt = st.selectbox("Type", ["Bug", "Billing", "Feature"])
            tb = st.text_area("Message")
            if st.form_submit_button("Send"):
                if tm and tb:
                    send_ticket_to_admin(tm, tt, tb)
                    st.success("Sent!")

# ==============================================================================
# 5. 主工作台
# ==============================================================================
tabs = get_tabs_by_persona(selected_persona)
t1, t2, t3 = st.tabs(tabs)

def render_workspace(mode_name):
    st.markdown(f"#### {mode_name}")
    user_input = st.text_area("Input", height=120, placeholder=f"Enter details for {mode_name}...", key=f"input_{mode_name}")
    if st.button(f"✨ Generate", key=f"btn_{mode_name}"):
        if not check_safety(user_input): return st.error("🚫 Unsafe content.")
        if st.session_state['user_type'] == 'Free' and st.session_state['usage_count'] >= 3: return st.error("🔒 Daily limit reached.")
        if not handle_cooldown(): return
        
        with st.spinner("🧪 Lai's Lab AI is thinking..."): # [修改] 加载提示语
            time.sleep(1.5)
            st.markdown(f'<div class="output-card">**[Lai\'s Lab Output]:**<br>Here is the content for "{user_input}"...</div>', unsafe_allow_html=True)
            if st.session_state['user_type'] == 'Free': st.session_state['usage_count'] += 1
        
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1: st.button("📋 Copy", key=f"cpy_{mode_name}")
        with c2: st.button("📥 PDF", disabled=(st.session_state['user_type']=='Free'), key=f"pdf_{mode_name}")

with t1: render_workspace(tabs[0])
with t2: render_workspace(tabs[1])
with t3: render_workspace(tabs[2])

# ==============================================================================
# 6. 页脚 (已更新)
# ==============================================================================
st.markdown("""
<div class="custom-footer">
    © 2025 Lai's Lab. All Rights Reserved.<br>
    <span style="color:green">● System Operational</span> &nbsp; | &nbsp; Powered by Cikgu Lai
</div>
""", unsafe_allow_html=True)