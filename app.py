import streamlit as st
import time
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==============================================================================
# 1. 系统配置与 CSS 注入 (System Config & UI)
# ==============================================================================
st.set_page_config(
    page_title="VisionPrompter AI V6.0.3",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

VERSION = "V6.0.3 (Global Stable)"

def inject_custom_css():
    st.markdown("""
    <style>
        /* 1. 隐藏 Streamlit 默认菜单，打造独立 App 质感 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* 2. Google Fonts 风格 (Inter/Roboto) */
        body { font-family: 'Inter', sans-serif; }
        
        /* 3. 主按钮美化 (Google Blue) */
        .stButton>button {
            background-color: #1A73E8;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #1557B0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        /* 4. 自定义页脚 */
        .custom-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            color: #5f6368;
            text-align: center;
            padding: 12px;
            font-size: 0.75rem;
            border-top: 1px solid #e0e0e0;
            z-index: 999;
        }
        
        /* 5. 卡片式输出容器 */
        .output-card {
            background-color: #ffffff;
            border: 1px solid #dadce0;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==============================================================================
# 2. Session State 初始化 (记忆库)
# ==============================================================================
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = 'Free' # 默认为 Free, 激活后变 Pro
if 'usage_count' not in st.session_state:
    st.session_state['usage_count'] = 0
if 'last_generate_time' not in st.session_state:
    st.session_state['last_generate_time'] = 0

# ==============================================================================
# 3. 核心功能函数 (Core Logic)
# ==============================================================================

# [A] 邮件发送函数 (零成本大厂方案)
def send_ticket_to_admin(user_email, issue_type, message):
    try:
        # 读取 Secrets
        sender_email = st.secrets["EMAIL_SENDER_ADDRESS"]
        sender_pass = st.secrets["EMAIL_APP_PASSWORD"]
        admin_email = st.secrets["EMAIL_ADMIN_ADDRESS"]
        
        msg = MIMEMultipart()
        msg['From'] = f"VisionPrompter Support <{sender_email}>"
        msg['To'] = admin_email
        msg['Subject'] = f"🚨 Ticket: {issue_type} from {user_email}"
        msg.add_header('Reply-To', user_email) # 关键：让您能直接回复给用户

        body = f"""
        <h3>New Support Ticket</h3>
        <p><strong>User:</strong> {user_email} ({st.session_state['user_type']})</p>
        <p><strong>Type:</strong> {issue_type}</p>
        <p><strong>Message:</strong><br>{message}</p>
        <hr>
        <p><em>System: VisionPrompter {VERSION}</em></p>
        """
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, admin_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        # 在本地开发如果没有配 secrets，会报错，这里捕获
        st.error(f"Email Config Error: {e}")
        return False

# [B] 动态 Tab 命名逻辑
def get_tabs_by_persona(persona):
    mapping = {
        "👨‍🏫 Educator (老师)": ["Teaching Material (教材)", "Visual Aids (教具)", "Communication (沟通)"],
        "🎥 Creator (创作者)": ["Scripts & Writing (脚本)", "Thumbnails & Art (封面)", "Social Captions (社媒)"],
        "💰 Seller (电商)": ["Product Copy (文案)", "Ad Visuals (广告图)", "Marketing Emails (营销)"],
        "👪 Parent (父母)": ["Story & Edu (故事)", "Fun Activities (活动)", "School Reply (回复老师)"],
        "🎓 Student (学生)": ["Study Notes (笔记)", "Mind Maps (导图)", "Presentation (演讲)"],
        "💼 Corporate (职场)": ["Reports & Docs (报告)", "Presentation Visuals (PPT)", "Business Emails (邮件)"]
    }
    return mapping.get(persona, ["Content", "Visual", "Social"])

# [C] 安全拦截 (敏感词库)
def check_safety(text):
    forbidden = ["porn", "kill", "nude", "xxx", "blood", "die", "gambling"] 
    for word in forbidden:
        if word in text.lower():
            return False
    return True

# [D] 冷却期与防刷 (Cooldown)
def handle_cooldown():
    current_time = time.time()
    time_diff = current_time - st.session_state['last_generate_time']
    
    if st.session_state['user_type'] == 'Pro':
        # Pro 用户：3秒隐形缓冲，防止误触连击
        if time_diff < 3:
            st.toast("⚡ System cooling down... (Pro Buffer)", icon="🧊")
            time.sleep(3 - time_diff)
    else:
        # Free 用户：60秒强制冷却
        if time_diff < 60 and st.session_state['last_generate_time'] != 0:
            wait_time = 60 - int(time_diff)
            st.warning(f"⏳ Free Plan Cooldown: Please wait {wait_time}s or upgrade to Pro.")
            return False
    
    st.session_state['last_generate_time'] = time.time()
    return True

# ==============================================================================
# 4. 侧边栏 (Sidebar - Control Center)
# ==============================================================================
with st.sidebar:
    st.title("VisionPrompter")
    st.caption(f"{VERSION}")
    
    # --- 1. 身份与设置 ---
    st.markdown("### 👤 Identity")
    selected_persona = st.selectbox(
        "Select Persona",
        ["👨‍🏫 Educator (老师)", "🎥 Creator (创作者)", "💰 Seller (电商)", 
         "👪 Parent (父母)", "🎓 Student (学生)", "💼 Corporate (职场)"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        ui_lang = st.selectbox("🌐 UI", ["English", "中文", "Bahasa"])
    with col2:
        output_lang = st.selectbox("🗣️ Output", ["Same as UI", "English", "中文", "Bahasa"])

    # --- 2. 支付与激活 (Lemon Squeezy) ---
    st.markdown("### 💎 Membership")
    if st.session_state['user_type'] == 'Free':
        # Free 状态
        left = 3 - st.session_state['usage_count']
        st.progress(st.session_state['usage_count'] / 3, text=f"Free Limit: {left}/3 left")
        
        # ⚠️ 请将下方的 URL 替换为您真实的 Lemon Squeezy 商品链接
        st.link_button("👑 Upgrade to Pro ($12.90)", "https://cikgulai.lemonsqueezy.com/checkout/buy/...")
        
        with st.expander("🔑 Activate License"):
            key_input = st.text_input("License Key")
            email_input = st.text_input("Email (Required)")
            if st.button("Activate"):
                if key_input and email_input:
                    # 模拟激活成功
                    st.session_state['user_type'] = 'Pro'
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Missing Key or Email")
    else:
        # Pro 状态
        st.success("👑 VIP Pro Active")
        st.caption("License: ••••••A1B2")
        st.link_button("🧾 Manage Subscription", "https://cikgulai.lemonsqueezy.com/billing")

    # --- 3. 智能工单 (Email Support System) ---
    st.markdown("---")
    st.caption("Support Center")
    with st.expander("📩 Submit a Ticket"):
        with st.form("ticket_form"):
            t_email = st.text_input("Your Email")
            t_type = st.selectbox("Type", ["🐛 Bug", "💰 Billing", "💡 Feature", "🤝 Partner"])
            t_msg = st.text_area("Message")
            if st.form_submit_button("🚀 Send Ticket"):
                if t_email and t_msg:
                    with st.spinner("Sending..."):
                        if send_ticket_to_admin(t_email, t_type, t_msg):
                            st.success("Sent! Check your email.")
                        else:
                            st.error("Failed. Please verify System Secrets.")
                else:
                    st.warning("Please fill all fields.")

# ==============================================================================
# 5. 主工作台 (Main Workspace)
# ==============================================================================

# 获取当前身份对应的 3 个 Tab 名字
tabs = get_tabs_by_persona(selected_persona)
t1, t2, t3 = st.tabs(tabs)

def render_workspace(mode_name):
    st.markdown(f"#### {mode_name}")
    user_input = st.text_area("Input", height=120, placeholder=f"Enter details for {mode_name}...", label_visibility="collapsed")
    
    col_btn, col_blank = st.columns([1, 4])
    with col_btn:
        run_btn = st.button(f"✨ Generate", key=f"btn_{mode_name}")
        
    if run_btn:
        # 1. 安全检查
        if not check_safety(user_input):
            st.error("🚫 Safety Alert: Input contains restricted content.")
            return
            
        # 2. 用量检查 (Free)
        if st.session_state['user_type'] == 'Free' and st.session_state['usage_count'] >= 3:
            st.error("🔒 Daily limit reached. Please Upgrade.")
            return

        # 3. 冷却与排队
        if not handle_cooldown():
            return
            
        # 4. 模拟生成 (Gemini API 占位符)
        res_box = st.empty()
        if st.session_state['user_type'] == 'Free':
            with st.spinner("⏳ Server busy... Queuing (Standard Tier)..."):
                time.sleep(2) # 假排队
                res_box.info("💡 Pro tip: Upgrade to skip the queue.")
                time.sleep(1)
        else:
            with st.spinner("⚡ VIP Processing..."):
                time.sleep(1) # 极速

        # 5. 显示结果
        mock_result = f"""
        **[System]:** Generated {mode_name} for "{selected_persona}"
        **[Language]:** {output_lang if output_lang != "Same as UI" else ui_lang}
        
        Here is the high-quality content generated by Gemini 2.5 Flash...
        (Content Placeholder: {user_input})
        """
        
        # 使用卡片样式显示结果
        st.markdown(f'<div class="output-card">{mock_result}</div>', unsafe_allow_html=True)
        
        # 增加计数
        if st.session_state['user_type'] == 'Free':
            st.session_state['usage_count'] += 1
            
        # 6. 导出区
        st.markdown("<br>", unsafe_allow_html=True)
        c_copy, c_pdf = st.columns([1, 1])
        with c_copy:
            st.button("📋 Copy Text", key=f"copy_{mode_name}")
        with c_pdf:
            st.button("📥 Download PDF (Pro)", disabled=(st.session_state['user_type'] == 'Free'), key=f"pdf_{mode_name}")

# 渲染三个 Tab
with t1: render_workspace(tabs[0])
with t2: render_workspace(tabs[1])
with t3: render_workspace(tabs[2])

# ==============================================================================
# 6. 国际版页脚 (Footer)
# ==============================================================================
st.markdown("""
<div class="custom-footer">
    © 2025 VisionPrompter AI by Cikgu Lai. All Rights Reserved.<br>
    <span style="opacity:0.6">Privacy Policy | Terms of Service | Disclaimer</span><br>
    <span style="color:green">● System Operational</span> &nbsp; | &nbsp; Version 6.0.3 (Global Stable)
</div>
""", unsafe_allow_html=True)