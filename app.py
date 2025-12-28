# app.py
# ==========================================
# PromptLab AI V8.6 Enterprise Ultimate Final
# 更新：2026 版权、专业法律免责声明 (Legal Disclaimer)
# ==========================================

import streamlit as st
import time
import pandas as pds
import prompt_data as pd
import prompt_logic as pl

# 1. 页面配置
st.set_page_config(
    page_title="Lai's Lab Enterprise",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 企业级 CSS 注入
st.markdown("""
<style>
    /* --- 核心主题色 --- */
    :root {
        --primary-blue: #0F52BA;
        --secondary-blue: #1e62c9;
        --bg-light-gray: #F4F7F9;
        --text-dark: #2C3E50;
        --card-shadow: 0 8px 24px rgba(15, 82, 186, 0.08);
    }

    .stApp { background-color: var(--bg-light-gray); color: var(--text-dark); font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: var(--text-dark) !important; font-weight: 800 !important; letter-spacing: -0.5px; }

    /* --- 卡片容器 --- */
    div[data-testid="stVerticalBlock"] > div:has(> .enterprise-card-marker) {
        background-color: #ffffff; padding: 30px; border-radius: 16px;
        border: 1px solid rgba(15, 82, 186, 0.1); box-shadow: var(--card-shadow);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="stVerticalBlock"] > div:has(> .enterprise-card-marker):hover {
        transform: translateY(-3px); box-shadow: 0 12px 30px rgba(15, 82, 186, 0.12);
    }

    /* --- 按钮美化 --- */
    .stButton>button[kind="primary"] { background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue)) !important; border: none; box-shadow: 0 4px 10px rgba(15, 82, 186, 0.3); font-weight: 700; }
    .stButton>button[kind="secondary"] { color: var(--primary-blue) !important; border: 2px solid var(--primary-blue) !important; background: transparent !important; font-weight: 700; }
    
    /* --- 定制 HTML 表格样式 --- */
    .custom-table { width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #E0E6ED; border-radius: 12px; overflow: hidden; }
    .custom-table th { background-color: var(--primary-blue); color: white; padding: 15px; text-align: left; font-weight: 700; }
    .custom-table td { padding: 12px 15px; border-bottom: 1px solid #E0E6ED; color: var(--text-dark); }
    .custom-table tr:last-child td { border-bottom: none; }
    .custom-table tr:nth-child(even) { background-color: #F8FAFC; } /* 斑马纹 */
    .pro-feature { color: var(--primary-blue); font-weight: 700; }

    /* --- Footer 样式 (专业版) --- */
    .footer {
        width: 100%;
        text-align: center;
        padding: 40px 20px;
        margin-top: 60px;
        border-top: 1px solid #E0E6ED;
        color: #95a5a6;
        font-size: 13px;
        line-height: 1.6;
        background-color: #fff; /* 底部白色背景 */
    }
    .footer b { color: #2C3E50; }
    .footer-links { margin-bottom: 10px; }
    .footer-links a { color: #0F52BA; text-decoration: none; margin: 0 12px; font-weight: 500; transition: color 0.2s;}
    .footer-links a:hover { color: #1e62c9; text-decoration: underline; }
    
    .footer-disclaimer {
        font-size: 11px;
        color: #bdc3c7;
        max-width: 600px;
        margin: 10px auto;
        font-style: normal;
    }

    /* 隐藏元素 */
    #MainMenu, footer, header, section[data-testid="stSidebar"] > div:first-child {visibility: hidden;}
    /* 侧边栏背景 */
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #E0E6ED; }
    /* 逼单广告 */
    .sticky-ad { background: linear-gradient(to bottom right, #fff5f5, #ffebeb); border-left: 4px solid #ff4b4b; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(255, 75, 75, 0.1); }
    
    /* Hero 区域样式 */
    .hero-container { display: flex; align-items: center; justify-content: center; gap: 40px; margin-bottom: 40px; padding: 20px 0; }
</style>
""", unsafe_allow_html=True)

def enterprise_card(): st.markdown('<div class="enterprise-card-marker"></div>', unsafe_allow_html=True)

# --- 🌟 新增：专业法律 Footer 函数 ---
def render_footer():
    st.markdown("""
    <div class="footer">
        <div style="margin-bottom: 8px;">
            &copy; 2026 <b>Lai's Lab</b> • Enterprise Edition V8.5
        </div>
        
        <div class="footer-links">
            <a href="#">Privacy Policy</a> • 
            <a href="#">Terms of Service</a> • 
            <a href="#">Usage Guidelines</a>
        </div>

        <div class="footer-disclaimer">
            <b>Disclaimer:</b> PromptLab AI can make mistakes. Please verify important information independently. 
            Users are solely responsible for the content they generate and how they use it. 
            Lai's Lab assumes no liability for actions taken based on these outputs.
        </div>
    </div>
    """, unsafe_allow_html=True)

# 3. Session 初始化
if 'page' not in st.session_state: st.session_state.page = 1
if 'user_role' not in st.session_state: st.session_state.user_role = "Guest"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'current_role_card' not in st.session_state: st.session_state.current_role_card = "Global Educator"
if 'lang' not in st.session_state: st.session_state.lang = "English"

def get_ui(key):
    lang_pack = pd.LANG_DICT.get(st.session_state.lang, pd.LANG_DICT["English"])
    return lang_pack.get(key, pd.LANG_DICT["English"].get(key, key))

# 4. 侧边栏
def render_sidebar():
    if st.session_state.page > 1:
        with st.sidebar:
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            try: st.image("logo.png", width=120) 
            except: st.markdown("## 🧠 Lai's Lab")
            st.markdown("### **Enterprise Workspace**")
            st.caption("V8.5 Professional Edition")
            st.markdown("---")
            is_pro = st.session_state.user_role == "PRO"
            with st.container():
                enterprise_card()
                role_badge = "💎 **PRO Enterprise**" if is_pro else "👤 Guest Trial"
                st.markdown(f"{role_badge}")
                st.caption(f"{st.session_state.user_email or 'Anonymous'}")
                st.progress(100 if is_pro else 30, "Engine Status")
            st.markdown("<br>", unsafe_allow_html=True)
            avail_langs = list(pd.LANG_DICT.keys()) if is_pro else ["English", "简体中文", "Español"]
            st.selectbox("🌐 Global Language", avail_langs, key="lang_sidebar")
            st.session_state.lang = st.session_state.lang_sidebar
            if not is_pro:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""<div class="sticky-ad"><div style="font-size:14px; font-weight:800; color:#ff4b4b;">⚡ LIMITED UPGRADE</div><div style="font-size:28px; font-weight:900; color:#2C3E50;">$12.90</div><div style="font-size:13px; color:#7f8c8d;">Lifetime Enterprise License.</div><a href="https://cikgulai.lemonsqueezy.com/checkout/buy/6b49b11a-830a-46e3-a458-0d8f2d2b160c?discount=PROMPTLAB" target="_blank"><button style="background:#ff4b4b; color:white; border:none; width:100%; padding:10px; border-radius:8px; margin-top:10px; cursor:pointer; font-weight:bold;">👉 Activate Now</button></a></div>""", unsafe_allow_html=True)
            st.markdown("---")
            if st.button("🚪 " + get_ui('logout'), use_container_width=True, type="secondary"):
                st.session_state.page = 1; st.session_state.user_role = "Guest"; st.rerun()

render_sidebar()

# 5. 页面路由逻辑

# === PAGE 1: LANDING (首页) ===
if st.session_state.page == 1:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    c_top1, c_top2 = st.columns([9, 1])
    with c_top2: st.session_state.lang = st.selectbox("🌐", ["English", "简体中文", "Español"], label_visibility="collapsed")

    # HERO (横向排版)
    with st.container():
        c_hero_logo, c_hero_text = st.columns([1, 3]) 
        with c_hero_logo:
            try: st.image("logo.png", width=160)
            except: st.markdown("# 🧠 Lai's Lab")     
        with c_hero_text:
            st.markdown("""
            <div style='text-align: left;'>
                <h1 style='color: #0F52BA; font-size: 2.5rem; margin-bottom: 10px;'>The Ultimate Enterprise Prompt Engine</h1>
                <p style='color: #5d6d7e; font-size: 1.2rem; font-weight: 500;'>Empowering Educators with Scale, Security & Pedagogical Impact.</p>
                <div style="display: flex; gap: 15px; margin-top: 15px; font-size: 0.9rem; color: #7f8c8d;">
                    <span style="background:#eef2f7; padding:5px 12px; border-radius:15px; display: flex; align-items: center; gap: 5px;">🛡️ Secure & Private</span>
                    <span style="background:#eef2f7; padding:5px 12px; border-radius:15px; display: flex; align-items: center; gap: 5px;">🚀 Turbo Engine</span>
                    <span style="background:#eef2f7; padding:5px 12px; border-radius:15px; display: flex; align-items: center; gap: 5px;">🌍 15+ Languages</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    main_c1, main_c2 = st.columns([4, 5], gap="large")
    
    # 登录区
    with main_c1:
        with st.container():
            enterprise_card()
            st.subheader("🔐 Secure Access")
            tab_login, tab_guest = st.tabs(["💎 PRO Login", "👤 Guest Trial"])
            with tab_login:
                st.markdown("<br>", unsafe_allow_html=True)
                st.text_input("Enterprise Email", key="p_email", placeholder="name@organization.com")
                st.text_input("License Key", key="p_key", type="password", placeholder="••••••••••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(get_ui('login_pro'), use_container_width=True, type="primary", key="btn_pro"):
                    if pl.validate_license_key(st.session_state.p_key):
                        st.session_state.user_email = st.session_state.p_email; st.session_state.user_role = "PRO"; st.session_state.page = 2; st.rerun()
                    else: st.error("Invalid Key")
            with tab_guest:
                st.markdown("<br>", unsafe_allow_html=True)
                st.text_input("Email Address", key="g_email", placeholder="Enter email...")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Continue as Guest", use_container_width=True, type="secondary", key="btn_guest"):
                    if st.session_state.g_email:
                        st.session_state.user_email = st.session_state.g_email; st.session_state.user_role = "Guest"; st.session_state.page = 2; st.rerun()

    # 对比表
    with main_c2:
        with st.container():
            enterprise_card()
            st.subheader("📋 Plan Comparison")
            st.markdown("""
            <table class="custom-table">
                <thead>
                    <tr><th>Capability</th><th style="background:#e3f2fd; color:#0F52BA;">Starter (Guest)</th><th>💎 Enterprise (PRO)</th></tr>
                </thead>
                <tbody>
                    <tr><td>🤖 AI Model</td><td>Standard Shared</td><td class="pro-feature">⚡ Dedicated Turbo</td></tr>
                    <tr><td>📝 Text Gen</td><td>5 / day</td><td class="pro-feature">✅ Unlimited</td></tr>
                    <tr><td>🎨 Image Gen</td><td>3 / day</td><td class="pro-feature">✅ 200 / day</td></tr>
                    <tr><td>🌍 Languages</td><td>3 Basic</td><td class="pro-feature">✅ 15+ Global</td></tr>
                    <tr><td>📂 Batch Upload</td><td>Single File</td><td class="pro-feature">✅ Bulk (50+)</td></tr>
                    <tr><td>💼 Commercial Use</td><td>❌ No</td><td class="pro-feature">✅ Included</td></tr>
                    <tr><td>🛠️ Advanced Modes</td><td>Basic Only</td><td class="pro-feature">✅ All 18 Modes</td></tr>
                </tbody>
            </table>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🔍 View Full Enterprise Specifications"):
                 c_spec1, c_spec2 = st.columns(2)
                 with c_spec1: st.markdown("**🌍 15+ Languages:**"); st.caption("English, Chinese, Malay, Japanese, Korean, Spanish, French, German, Russian, etc.")
                 with c_spec2: st.markdown("**🛠️ 18 Modes:**"); st.caption("Pedagogy, Writing, Coding, SEO, Roleplay, Analysis, Email, Marketing, Scripting, etc.")

    # 🚀 在 Page 1 底部添加 Footer
    render_footer()


# === PAGE 2: ROLE HALL ===
elif st.session_state.page == 2:
    st.button(f"⬅️ Dashboard", on_click=lambda: st.session_state.update(page=1), type="secondary")
    st.title("Select Persona"); st.markdown("---")
    roles = list(pd.ROLES_DB.keys()); cols = st.columns(3, gap="medium")
    for i, role in enumerate(roles):
        with cols[i % 3]:
            with st.container():
                enterprise_card(); st.subheader(f"🎭 {role}")
                if st.button(f"Launch {role}", key=f"btn_{i}", use_container_width=True, type="primary" if i==0 else "secondary"):
                    st.session_state.current_role_card = role; st.session_state.page = 3; st.rerun()
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    render_footer()


# === PAGE 3: WORKSPACE ===
elif st.session_state.page == 3:
    is_pro = st.session_state.user_role == "PRO"
    usage = pl.get_user_usage(st.session_state.user_email)
    
    with st.container():
        enterprise_card()
        c1, c2 = st.columns([1, 6])
        with c1:
            if st.button("⬅️ Change", type="secondary"): st.session_state.page = 2; st.rerun()
        with c2: st.markdown(f"### 🛠️ Active: **{st.session_state.current_role_card}**")

    st.markdown("<br>", unsafe_allow_html=True)
    role_data = pd.ROLES_DB[st.session_state.current_role_card]; mode_names = list(role_data.keys())
    c_main1, c_main2 = st.columns([1, 1], gap="large")
    
    with c_main1:
        with st.container():
            enterprise_card(); st.subheader("1. Configuration")
            sel_mode = st.selectbox(get_ui('mode_sel'), mode_names)
            if not is_pro and sel_mode != mode_names[0]: st.warning(f"🔒 Enterprise Only"); st.stop()
            mode_data = role_data[sel_mode]; sel_option = st.selectbox(get_ui('opt_sel'), mode_data["options"])

    with c_main2:
        with st.container():
            enterprise_card(); st.subheader("2. Context & Input")
            st.file_uploader("📂 Attach Files", accept_multiple_files=is_pro)
            user_input = st.text_area("Instructions", height=150, placeholder=mode_data["placeholder"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ Generate Output", type="primary", use_container_width=True):
        pl.update_user_usage(st.session_state.user_email, "text", 1)
        with st.status("🚀 Processing...", expanded=True):
            time.sleep(1); st.write("✅ Done!")
        st.session_state.result = pl.generate_pasec_prompt(st.session_state.current_role_card, sel_mode, sel_option, user_input, 0, st.session_state.lang, is_pro)
        st.rerun()

    if 'result' in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            enterprise_card(); st.subheader("🎉 Output")
            st.text_area("Result", st.session_state.result, height=350)
            st.button("📋 Copy", use_container_width=True)

    render_footer()
