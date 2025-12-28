# app.py
# ==========================================
# PromptLab AI V8.2 Enterprise Ultimate Final
# 修复：Logo尺寸、移除多余提示、找回Full Specs、定制HTML表格
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

# 2. 企业级 CSS 注入 (核心机密)
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
    
    /* --- 定制 HTML 表格样式 (新) --- */
    .custom-table { width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #E0E6ED; border-radius: 12px; overflow: hidden; }
    .custom-table th { background-color: var(--primary-blue); color: white; padding: 15px; text-align: left; font-weight: 700; }
    .custom-table td { padding: 12px 15px; border-bottom: 1px solid #E0E6ED; color: var(--text-dark); }
    .custom-table tr:last-child td { border-bottom: none; }
    .custom-table tr:nth-child(even) { background-color: #F8FAFC; } /* 斑马纹 */
    .pro-feature { color: var(--primary-blue); font-weight: 700; }

    /* 隐藏元素 */
    #MainMenu, footer, header, section[data-testid="stSidebar"] > div:first-child {visibility: hidden;}
    /* 侧边栏背景 */
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #E0E6ED; }
    /* 逼单广告 */
    .sticky-ad { background: linear-gradient(to bottom right, #fff5f5, #ffebeb); border-left: 4px solid #ff4b4b; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(255, 75, 75, 0.1); }
</style>
""", unsafe_allow_html=True)

def enterprise_card(): st.markdown('<div class="enterprise-card-marker"></div>', unsafe_allow_html=True)

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
            try:
                # 修复：侧边栏 Logo 也限制宽度
                st.image("logo.png", width=120) 
            except:
                st.markdown("## 🧠 Lai's Lab")
            st.markdown("### **Enterprise Workspace**")
            st.caption("V8.2 Professional Edition")
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

# === PAGE 1: LANDING (首页 - 终极修复版) ===
if st.session_state.page == 1:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    c_top1, c_top2 = st.columns([9, 1])
    with c_top2: st.session_state.lang = st.selectbox("🌐", ["English", "简体中文", "Español"], label_visibility="collapsed")

    # 🌟 HERO 区域 (Logo 修复 + Slogan)
    with st.container():
        c_hero1, c_hero2, c_hero3 = st.columns([1, 2, 1])
        with c_hero2:
            try:
                # 🛠️ 修复重点：强制设置宽度为 180px，不再使用 use_column_width
                st.image("logo.png", width=180)
            except:
                st.markdown("# 🧠 Lai's Lab")
            
            st.markdown("""
            <div style='text-align: center; margin-top: -10px; margin-bottom: 40px;'>
                <h1 style='color: #0F52BA; font-size: 2.5rem; margin-bottom: 10px;'>The Ultimate Enterprise Prompt Engine</h1>
                <p style='color: #5d6d7e; font-size: 1.2rem; font-weight: 500;'>Empowering Educators with Scale, Security & Pedagogical Impact.</p>
                <div style="display: flex; justify-content: center; gap: 15px; margin-top: 15px; font-size: 0.9rem; color: #7f8c8d;">
                    <span style="background:#eef2f7; padding:5px 10px; border-radius:15px;">🛡️ Secure & Private</span>
                    <span style="background:#eef2f7; padding:5px 10px; border-radius:15px;">🚀 Turbo Engine</span>
                    <span style="background:#eef2f7; padding:5px 10px; border-radius:15px;">🌍 15+ Languages</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    main_c1, main_c2 = st.columns([4, 5], gap="large")
    
    # 左侧：登录
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

    # 右侧：全新定制 HTML 对比表 (修复重点)
    with main_c2:
        with st.container():
            enterprise_card()
            st.subheader("📋 Plan Comparison")
            
            # 🛠️ 使用定制 HTML 表格替代 datafram，更专业
            st.markdown("""
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>Capability</th>
                        <th style="background:#e3f2fd; color:#0F52BA;">Starter (Guest)</th>
                        <th>💎 Enterprise (PRO)</th>
                    </tr>
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
            
            # 🛠️ 修复重点：找回 Full Specs 列表，并美化
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🔍 View Full Enterprise Specifications"):
                 c_spec1, c_spec2 = st.columns(2)
                 with c_spec1:
                     st.markdown("**🌍 15+ Supported Languages:**")
                     st.caption("English, Chinese (Simplified/Traditional), Malay, Japanese, Korean, Spanish, French, German, Russian, Portuguese, Italian, Arabic, Hindi, Thai.")
                 with c_spec2:
                     st.markdown("**🛠️ 18 Professional Modes:**")
                     st.caption("Pedagogy, Creative Writing, Coding (Python/HTML), SEO, Roleplay, Data Analysis, Scriptwriting, Email Wizard, Marketing Copy, and more.")
            
            # 🛠️ 修复重点：已移除底部的蓝色 st.info 提示框

# === PAGE 2 & 3 (保持不变，省略以节省篇幅，请使用您现有的 Page 2/3 代码或我上一个完整版中的) ===
# 为了确保代码完整运行，我这里还是放上简化的 Page 2/3，您也可以直接用之前的完整版
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
elif st.session_state.page == 3:
    # ... (使用您现有的 Page 3 代码) ...
    st.title("Workspace (Page 3 Placeholder)")
    st.button("⬅️ Back", on_click=lambda: st.session_state.update(page=2))
