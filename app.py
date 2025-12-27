import streamlit as st
import time
import json
import datetime
import random
import base64
from fpdf import FPDF
import os

# ==========================================
# 1. 配置与常量
# ==========================================
st.set_page_config(
    page_title="PromptLab AI v7.0",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed" # 首页默认折叠侧边栏，更像Landing Page
)

# 商业规则常量
PRICE_PRO = "$12.90"
PRICE_OLD = "$39.90"
LIMIT_TEXT_FREE = 5
LIMIT_IMAGE_FREE = 3
LIMIT_IMAGE_PRO = 200
UPLOAD_BATCH_FREE = 1
UPLOAD_BATCH_PRO = 50

# 语言列表
LANG_FREE = ["English", "简体中文", "Bahasa Melayu"]
LANG_ALL = LANG_FREE + ["Russian", "Japanese", "Korean", "French", "German"]

# 角色定义
ROLES = {
    "Global Educator": ["Pedagogy", "Lesson Plan", "Assessment"],
    "Global Creator": ["Thumbnail", "Scripting", "Shorts/Reels"],
    "Global Seller": ["Copywriting", "Product Desc", "Email Marketing"],
    "Parent": ["Storytelling", "Activity", "Discipline"],
    "Student": ["Essay", "Study Plan", "Summary"],
    "Corporate": ["Strategy", "Meeting", "HR/Email"]
}

# ==========================================
# 2. 核心工具函数
# ==========================================
DB_FILE = 'user_db.json'

def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, 'r') as f: return json.load(f)

def save_db(db):
    with open(DB_FILE, 'w') as f: json.dump(db, f)

def update_usage(email, type="text"):
    # (简化版逻辑，保持原样)
    pass 

def validate_license(key):
    return key == "ADMIN-8888" or key.startswith("PRO")

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 3. 页面路由管理 (State Management)
# ==========================================
# 初始化页面状态
if 'page' not in st.session_state:
    st.session_state['page'] = 'home' # 默认在首页

if 'user_type' not in st.session_state:
    st.session_state['user_type'] = 'guest'

def navigate_to(page_name):
    st.session_state['page'] = page_name
    st.rerun()

# ==========================================
# 4. PAGE 1: 首页 & 登录 & 对比表
# ==========================================
def render_home():
    st.markdown("<h1 style='text-align: center; font-size: 3em;'>🤖 PromptLab AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>Enterprise-Grade Prompt Generator</h3>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🔓 Login / Access")
        
        # 登录区域
        tab_guest, tab_pro = st.tabs(["👤 Free Guest", "💎 PRO Login"])
        
        with tab_guest:
            st.info("Try basic features for free.")
            email_guest = st.text_input("Enter Email to start", placeholder="user@gmail.com")
            if st.button("🚀 Start as Guest", use_container_width=True):
                if email_guest:
                    st.session_state['user_type'] = 'guest'
                    st.session_state['user_email'] = email_guest
                    navigate_to('roles') # 跳转到角色页
                else:
                    st.error("Please enter an email.")

        with tab_pro:
            st.success("Unlock Unlimited Power.")
            email_pro = st.text_input("PRO Email")
            key_pro = st.text_input("License Key", type="password")
            if st.button("💎 Login PRO", use_container_width=True):
                if validate_license(key_pro):
                    st.session_state['user_type'] = 'pro'
                    st.session_state['user_email'] = email_pro
                    navigate_to('roles') # 跳转到角色页
                else:
                    st.error("Invalid Key")

    with col2:
        st.subheader("🆚 Plan Comparison")
        # 渲染对比表格
        st.markdown(f"""
        | Feature | 👤 Free Guest | 💎 PRO ({PRICE_PRO}) |
        | :--- | :--- | :--- |
        | **Engine** | 🐢 Standard | 🚀 **Turbo Priority** |
        | **Text Limit** | 🔒 {LIMIT_TEXT_FREE}/Day | ✅ **Unlimited** |
        | **Image Limit** | 🔒 {LIMIT_IMAGE_FREE}/Day | ✅ **Max {LIMIT_IMAGE_PRO}/Day** |
        | **Uploads** | 🔒 1 File | ✅ **Batch {UPLOAD_BATCH_PRO}** |
        | **Languages** | 🔒 3 Only | ✅ **15 Languages** |
        | **Export** | 🔒 TXT (Watermark) | ✅ **PDF, CSV, Clean** |
        """)
        st.caption(f"Lifetime Deal: {PRICE_PRO} (Was ~~{PRICE_OLD}~~). No Monthly Fees.")

# ==========================================
# 5. PAGE 2: 角色选择大厅
# ==========================================
def render_roles():
    st.button("⬅️ Back to Home", on_click=lambda: navigate_to('home'))
    
    st.title("🎭 Choose Your Workspace")
    st.markdown("Select a role to activate your specialized AI dashboard.")
    
    # 角色网格
    cols = st.columns(3)
    role_names = list(ROLES.keys())
    
    for i, role in enumerate(role_names):
        with cols[i % 3]:
            # 修复之前的 IndexError: 直接显示完整名字，或者安全的拆分
            display_name = role 
            
            # 大卡片按钮
            if st.button(f"✨ {display_name}", key=role, use_container_width=True, type="secondary"):
                st.session_state['current_role'] = role
                navigate_to('workspace') # 跳转到工作台
            
            # 显示该角色的模式预览
            modes_str = ", ".join(ROLES[role][:2]) + "..."
            st.caption(f"Includes: {modes_str}")
            st.markdown("---")

# ==========================================
# 6. PAGE 3: 核心工作台 (Center)
# ==========================================
def render_workspace():
    # 顶部导航条
    col_nav1, col_nav2 = st.columns([1, 4])
    with col_nav1:
        st.button("⬅️ Change Role", on_click=lambda: navigate_to('roles'))
    with col_nav2:
        st.info(f"👤 **{st.session_state.get('user_email', 'Guest')}** | Role: **{st.session_state.get('current_role')}** | Mode: **{st.session_state['user_type'].upper()}**")

    st.title(f"🛠️ {st.session_state.get('current_role')} Workspace")
    
    # --- 这里放入之前的核心工作台代码 ---
    
    col_main1, col_main2 = st.columns([1, 1])
    
    with col_main1:
        # 模式选择
        modes = ROLES[st.session_state['current_role']]
        selected_mode = st.selectbox("Select Mode", modes)
        
        # 语言选择
        langs = LANG_ALL if st.session_state['user_type'] == 'pro' else LANG_FREE
        out_lang = st.selectbox("Output Language", langs)
        
    with col_main2:
        st.file_uploader("Upload Context", accept_multiple_files=(st.session_state['user_type']=='pro'))

    user_input = st.text_area("Input Details", height=150)
    
    if st.button("✨ Generate Prompt", type="primary", use_container_width=True):
        with st.status("Thinking..."):
            time.sleep(1.5) # 模拟等待
            st.write("✅ Done!")
            st.session_state['result'] = f"Generated Prompt for {st.session_state['current_role']} in {out_lang}:\n\n{user_input}..."
            
    # 结果显示区
    if 'result' in st.session_state:
        st.success("Result Generated:")
        st.text_area("Result", st.session_state['result'], height=200)
        st.button("📋 Copy Result")
        
        # 底部存档区
        st.caption("Layer 5: Downloads")
        st.button("📄 Download PDF (PRO Only)" if st.session_state['user_type'] != 'pro' else "📄 Download PDF")


# ==========================================
# 7. 主程序入口 (Main Router)
# ==========================================
if st.session_state['page'] == 'home':
    render_home()
elif st.session_state['page'] == 'roles':
    render_roles()
elif st.session_state['page'] == 'workspace':
    render_workspace()

# 侧边栏始终显示 FAQ 和 Support (除了首页可能想隐藏)
if st.session_state['page'] != 'home':
    with st.sidebar:
        st.header("⚙️ Settings")
        if st.button("Logout"):
            navigate_to('home')