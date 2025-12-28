# app.py
# ==========================================
# PromptLab AI V9.0 Enterprise Final
# 架构：MVC 分离版 (UI Only)
# 功能：侧边栏7大模块 + 底部Footer + 企业级UI
# ==========================================

import streamlit as st
import time
import pandas as pds       # 表格处理
import prompt_data as pd   # 📚 数据仓库 (Data)
import prompt_logic as pl  # ⚙️ 逻辑引擎 (Logic)

# 1. 页面配置 (必须在第一行)
st.set_page_config(
    page_title="Lai's Lab Enterprise",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 企业级 CSS 样式注入
st.markdown("""
<style>
    /* --- 核心配色 --- */
    :root { --primary-blue: #0F52BA; --text-dark: #2C3E50; --bg-gray: #F4F7F9; }
    
    /* 全局字体与背景 */
    .stApp { background-color: var(--bg-gray); font-family: 'Inter', sans-serif; color: var(--text-dark); }
    h1, h2, h3 { color: var(--text-dark) !important; font-weight: 800 !important; }

    /* --- 卡片容器样式 --- */
    div[data-testid="stVerticalBlock"] > div:has(> .enterprise-card-marker) {
        background-color: white; padding: 25px; border-radius: 15px;
        border: 1px solid rgba(15, 82, 186, 0.1); 
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }

    /* --- 侧边栏样式 --- */
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #E0E6ED; }
    
    /* 侧边栏: 逼单广告 (红框) */
    .sticky-ad {
        background-color: #fff5f5; border: 2px solid #ff4b4b;
        border-radius: 12px; padding: 15px; text-align: center;
        margin-top: 20px; box-shadow: 0 4px 12px rgba(255, 75, 75, 0.1);
    }
    
    /* --- 表格样式 --- */
    .custom-table { width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #E0E6ED; border-radius: 12px; overflow: hidden; }
    .custom-table th { background: #0F52BA; color: white; padding: 12px; text-align: left; }
    .custom-table td { padding: 12px; border-bottom: 1px solid #eee; background: white; color: #333; }
    .pro-tag { color: #0F52BA; font-weight: bold; }

    /* --- Footer 样式 --- */
    .footer {
        width: 100%; text-align: center; padding: 40px 20px; margin-top: 60px;
        border-top: 1px solid #E0E6ED; color: #95a5a6; font-size: 13px; line-height: 1.6;
        background-color: #fff;
    }
    .footer b { color: #2C3E50; }
    .footer-links a { color: #0F52BA; text-decoration: none; margin: 0 10px; }
    .footer-disclaimer { font-size: 11px; color: #bdc3c7; max-width: 600px; margin: 10px auto; font-style: normal; }

    /* 隐藏默认元素 */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Hero 布局 */
    .hero-container { display: flex; align-items: center; justify-content: center; gap: 40px; }
</style>
""", unsafe_allow_html=True)

# 辅助函数：卡片标记
def enterprise_card(): 
    st.markdown('<div class="enterprise-card-marker"></div>', unsafe_allow_html=True)

# Footer 渲染函数
def render_footer():
    st.markdown("""
    <div class="footer">
        <div style="margin-bottom: 8px;">&copy; 2026 <b>Lai's Lab</b> • Enterprise Edition V9.0</div>
        <div class="footer-links">
            <a href="#">Privacy Policy</a> • <a href="#">Terms of Service</a> • <a href="#">Usage Guidelines</a>
        </div>
        <div class="footer-disclaimer">
            <b>Disclaimer:</b> PromptLab AI can make mistakes. Please verify important information independently. 
            Users are solely responsible for the content they generate. 
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

# UI 文本获取 (从 pd 拿数据)
def get_ui(key):
    lang_pack = pd.LANG_DICT.get(st.session_state.lang, pd.LANG_DICT["English"])
    return lang_pack.get(key, pd.LANG_DICT["English"].get(key, key))

# 4. 侧边栏逻辑 (Sidebar Logic) - 7大模块完整版
def render_sidebar():
    if st.session_state.page > 1:
        with st.sidebar:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            try: st.image("logo.png", width=140) 
            except: st.markdown("## 🧠 Lai's Lab")
            
            st.markdown("### **Enterprise Workspace**")
            st.caption("V9.0 Professional Edition")
            st.markdown("---")
            
            is_pro = st.session_state.user_role == "PRO"
            
            # --- 1. 用户身份卡 (Identity) ---
            with st.container():
                enterprise_card() # 卡片背景
                role_badge = "💎 **PRO Enterprise**" if is_pro else "👤 Guest Trial"
                st.markdown(f"{role_badge}")
                st.caption(f"ID: {st.session_state.user_email or 'Guest_User'}")
            
            st.markdown("<br>", unsafe_allow_html=True)

            # --- 2. 语言切换 (Language) ---
            # 逻辑：PRO看15种，Guest看3种
            avail_langs = list(pd.LANG_DICT.keys()) if is_pro else ["English", "简体中文", "Español"]
            st.selectbox("🌐 Global Language", avail_langs, key="lang_sidebar")
            st.session_state.lang = st.session_state.lang_sidebar

            st.markdown("<br>", unsafe_allow_html=True)

            # --- 3. 使用次数表 (Usage Stats) ---
            # 逻辑：绑定 Email 查询用量
            usage = pl.get_user_usage(st.session_state.user_email)
            limits = pl.LIMITS["PRO"] if is_pro else pl.LIMITS["FREE"]
            
            st.caption("📊 Daily Usage Stats")
            # 文本进度条
            txt_max = "∞" if is_pro else limits['text_daily']
            st.progress(0 if is_pro else min(usage['text_count']/5, 1.0), 
                        f"Text Gen: {usage['text_count']} / {txt_max}")
            # 图片进度条
            img_max = 200 if is_pro else limits['image_daily']
            st.progress(min(usage['image_count']/img_max, 1.0), 
                        f"Image Gen: {usage['image_count']} / {img_max}")

            # --- 4. 逼单广告 (Sticky Ad) ---
            # 逻辑：仅 Guest 可见
            if not is_pro:
                st.markdown("""
                <div class="sticky-ad">
                    <div style="color:#ff4b4b; font-weight:800; font-size:12px;">⚡ LIMITED UPGRADE</div>
                    <div style="color:#2C3E50; font-weight:900; font-size:24px;">$12.90</div>
                    <div style="color:grey; font-size:12px; margin-bottom:8px;">Lifetime Enterprise License</div>
                    <a href="https://cikgulai.lemonsqueezy.com/checkout/buy/6b49b11a-830a-46e3-a458-0d8f2d2b160c?discount=PROMPTLAB" target="_blank" style="text-decoration:none;">
                        <button style="background:#ff4b4b; color:white; border:none; width:100%; padding:10px; border-radius:6px; cursor:pointer; font-weight:bold;">👉 Activate Now</button>
                    </a>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            
            # --- 5. 智能工单系统 (Smart Ticket) ---
            with st.expander(get_ui('ticket_title')): # "Submit Ticket"
                cat = st.selectbox("Category", [
                    "Bug / Error",
                    "Billing Issue",
                    "Feature Request", 
                    "Partnership / Sponsorship", 
                    "Others"
                ])
                sub = st.text_input(get_ui('ticket_sub')) # "Subject"
                msg = st.text_area(get_ui('ticket_msg'))  # "Message"
                
                # 拦截逻辑 check_ticket_intercept
                should_intercept, reply = pl.check_ticket_intercept(sub, msg)
                
                if should_intercept:
                    st.warning(reply)
                else:
                    if st.button("Submit Ticket"):
                        if sub and msg:
                            st.success("✅ Ticket Sent! Support team will reply in 24h.")
                            # 这里实际上 pl 可以处理发送逻辑
                        else:
                            st.error("Please fill all fields.")

            # --- 6. FAQ 知识库 (Knowledge Base) ---
            st.caption("📚 Knowledge Base")
            # 逻辑：遍历 pd.FAQ_DB，自动显示 Affiliate 等所有分类
            for cat, qas in pd.FAQ_DB.items():
                with st.expander(cat):
                    for q, a in qas:
                        st.markdown(f"**Q: {q}**\n\n{a}")
            
            st.markdown("---")
            
            # --- 7. 登出按钮 (Logout) ---
            if st.button("🚪 " + get_ui('logout'), use_container_width=True):
                st.session_state.page = 1
                st.session_state.user_role = "Guest"
                st.rerun()

render_sidebar()

# 5. 页面路由逻辑

# === PAGE 1: LANDING (首页) ===
if st.session_state.page == 1:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    c_top1, c_top2 = st.columns([9, 1])
    with c_top2: st.session_state.lang = st.selectbox("🌐", ["English", "简体中文", "Español"], label_visibility="collapsed")

    # HERO (横向 Logo + Slogan)
    with st.container():
        c1, c2 = st.columns([1, 3])
        with c1:
            try: st.image("logo.png", width=160)
            except: st.markdown("# 🧠")
        with c2:
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
            t1, t2 = st.tabs(["💎 PRO Login", "👤 Guest"])
            with t1:
                st.text_input("Enterprise Email", key="p_e")
                st.text_input("License Key", type="password", key="p_k")
                if st.button("Login PRO", type="primary", use_container_width=True):
                    # 调用 pl 验证
                    if pl.validate_license_key(st.session_state.p_k):
                        st.session_state.user_email=st.session_state.p_e; st.session_state.user_role="PRO"; st.session_state.page=2; st.rerun()
                    else: st.error("Invalid Key")
            with t2:
                st.text_input("Email", key="g_e")
                if st.button("Guest Trial", type="secondary", use_container_width=True):
                    if st.session_state.g_e:
                        st.session_state.user_email=st.session_state.g_e; st.session_state.user_role="Guest"; st.session_state.page=2; st.rerun()

    # 对比表 (HTML)
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
                    <tr><td>🤖 AI Model</td><td>Standard Shared</td><td class="pro-tag">⚡ Dedicated Turbo</td></tr>
                    <tr><td>📝 Text Gen</td><td>5 / day</td><td class="pro-tag">✅ Unlimited</td></tr>
                    <tr><td>🎨 Image Gen</td><td>3 / day</td><td class="pro-tag">✅ 200 / day</td></tr>
                    <tr><td>🌍 Languages</td><td>3 Basic</td><td class="pro-tag">✅ 15+ Global</td></tr>
                    <tr><td>📂 Batch Upload</td><td>Single File</td><td class="pro-tag">✅ Bulk (50+)</td></tr>
                    <tr><td>💼 Commercial</td><td>❌ No</td><td class="pro-tag">✅ Included</td></tr>
                </tbody>
            </table>
            """, unsafe_allow_html=True)
            with st.expander("🔍 Full Specs"):
                 st.write("Full support for 15+ languages and 18+ pedagogical modes.")

    render_footer()

# === PAGE 2: ROLE HALL ===
elif st.session_state.page == 2:
    st.button("⬅️ Dashboard", on_click=lambda: st.session_state.update(page=1))
    st.title("Select Persona"); st.write("---")
    
    # 从 pd 读取角色列表
    roles = list(pd.ROLES_DB.keys())
    cols = st.columns(3)
    for i, r in enumerate(roles):
        with cols[i%3]:
            with st.container():
                enterprise_card(); st.subheader(f"🎭 {r}")
                if st.button(f"Launch {r}", key=f"b{i}", use_container_width=True, type="primary" if i==0 else "secondary"):
                    st.session_state.current_role_card=r; st.session_state.page=3; st.rerun()
    render_footer()

# === PAGE 3: WORKSPACE ===
elif st.session_state.page == 3:
    # 顶部
    with st.container():
        enterprise_card()
        c1, c2 = st.columns([1,6])
        with c1: 
            if st.button("⬅️ Back"): st.session_state.page=2; st.rerun()
        with c2: st.markdown(f"### 🛠️ Active: **{st.session_state.current_role_card}**")
    
    st.write("<br>", unsafe_allow_html=True)
    is_pro = st.session_state.user_role == "PRO"
    
    # 从 pd 读取当前角色的数据
    role_data = pd.ROLES_DB[st.session_state.current_role_card]
    
    c1, c2 = st.columns(2, gap="large")
    with c1:
        with st.container():
            enterprise_card(); st.subheader("1. Config")
            mode = st.selectbox(get_ui('mode_sel'), list(role_data.keys()))
            
            # PRO 锁
            if not is_pro and mode != list(role_data.keys())[0]: st.warning("🔒 PRO Only"); st.stop()
            
            opt = st.selectbox(get_ui('opt_sel'), role_data[mode]["options"])
            
    with c2:
        with st.container():
            enterprise_card(); st.subheader("2. Input")
            st.file_uploader("Attach", accept_multiple_files=is_pro)
            txt = st.text_area("Context", height=150, placeholder=role_data[mode]["placeholder"])
            
    if st.button("✨ Generate", type="primary", use_container_width=True):
        # 调用 pl 更新用量
        pl.update_user_usage(st.session_state.user_email, "text", 1)
        
        with st.status("🚀 Processing..."):
            time.sleep(1); st.write("✅ Done")
        
        # 调用 pl 生成核心 Prompt
        st.session_state.result = pl.generate_pasec_prompt(
            st.session_state.current_role_card, mode, opt, txt, 0, st.session_state.lang, is_pro
        )
        st.rerun()
        
    if 'result' in st.session_state:
        st.write("---")
        with st.container():
            enterprise_card(); st.subheader("🎉 Result")
            st.text_area("Output", st.session_state.result, height=300)
            
    render_footer()
