# app.py
# ==========================================
# PromptLab AI V7.3 Ultimate Edition
# 主程序界面 (Main Interface)
# ==========================================

import streamlit as st
import time
import base64
import prompt_data as pd   # 导入数据仓库
import prompt_logic as pl  # 导入逻辑引擎

# 1. 页面配置 (Page Config)
# ------------------------------------------
st.set_page_config(
    page_title="PromptLab AI V7.3",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# 2. 样式注入 (CSS Injection)
# ------------------------------------------
st.markdown("""
<style>
    /* 全局按钮美化 */
    .stButton>button { border-radius: 8px; height: 45px; font-weight: 600; }
    
    /* 逼单广告红框 */
    .sticky-ad {
        border: 2px solid #ff4b4b;
        background-color: #fff5f5;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% {box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.4);} 70% {box-shadow: 0 0 0 10px rgba(255, 75, 75, 0);} 100% {box-shadow: 0 0 0 0 rgba(255, 75, 75, 0);} }
    
    /* 5层塔图标容器 */
    .layer-deck { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 10px; }
    .layer-btn { 
        text-decoration: none; border: 1px solid #eee; padding: 8px 12px; 
        border-radius: 8px; display: flex; align-items: center; gap: 5px; 
        color: #333; transition: 0.3s; background: white; font-size: 14px;
    }
    .layer-btn:hover { background: #f0f2f6; border-color: #ccc; }
    .layer-btn.disabled { opacity: 0.5; pointer-events: none; filter: grayscale(1); }
    
    /* 隐藏默认菜单 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. 会话状态初始化 (Session State)
# ------------------------------------------
if 'page' not in st.session_state: st.session_state.page = 1
if 'user_role' not in st.session_state: st.session_state.user_role = "Guest" # Guest or PRO
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'current_role_card' not in st.session_state: st.session_state.current_role_card = "Global Educator"
if 'lang' not in st.session_state: st.session_state.lang = "English"

# 获取当前语言的UI文本
def get_ui(key):
    # 如果当前语言没有对应的key，回退到英文
    lang_pack = pd.LANG_DICT.get(st.session_state.lang, pd.LANG_DICT["English"])
    return lang_pack.get(key, pd.LANG_DICT["English"].get(key, key))

# 4. 全局侧边栏 (仅在 Page 2, 3 显示)
# ------------------------------------------
def render_sidebar():
    if st.session_state.page > 1:
        with st.sidebar:
            # 1. Logo
            try:
                st.image("logo.png", width=120)
            except:
                st.markdown("## 🧠 PromptLab")
            
            st.markdown("---")
            
            # 2. 用户卡片
            is_pro = st.session_state.user_role == "PRO"
            role_badge = "💎 PRO Enterprise" if is_pro else "👤 Free Guest"
            engine_status = "🚀 Turbo" if is_pro else "🐢 Standard"
            
            st.caption("User Identity")
            st.info(f"**{role_badge}**\n\nEmail: {st.session_state.user_email}\nEngine: {engine_status}")
            
            # 3. 语言切换 (Guest 3种, PRO 15种)
            avail_langs = list(pd.LANG_DICT.keys()) if is_pro else ["English", "简体中文", "Español"]
            st.session_state.lang = st.selectbox("🌐 Language", avail_langs, index=0 if "English" in avail_langs else 0)
            
            # 4. 🔥 逼单广告 (仅 Guest)
            if not is_pro:
                st.markdown("---")
                st.markdown(f"""
                <div class="sticky-ad">
                    <div style="font-size:12px; font-weight:bold; color:#ff4b4b;">{get_ui('sticky_ad_title')}</div>
                    <div style="font-size:24px; font-weight:800; color:#333;">$12.90</div>
                    <div style="font-size:12px; text-decoration:line-through; color:grey;">$39.90</div>
                    <a href="https://promptlab.lemonsqueezy.com/checkout" target="_blank" style="text-decoration:none;">
                        <button style="background:#ff4b4b; color:white; border:none; width:100%; padding:8px; border-radius:5px; margin-top:5px; cursor:pointer; font-weight:bold;">
                            {get_ui('sticky_ad_btn')}
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # 5. 智能工单
            with st.expander(get_ui('ticket_title')):
                 ticket_type = st.selectbox("Category", [
                    "Bug / Error", 
                    "Billing Issue", 
                    "Feature Request", 
                    "Partnership / Sponsorship", 
                    "Others"
                ])
                # ====================

                sub = st.text_input(get_ui('ticket_sub'))
                msg = st.text_area(get_ui('ticket_msg'))
                
                # 实时拦截检查 (这段不要漏掉)
                should_intercept, reply = pl.check_ticket_intercept(sub, msg)
                if should_intercept:
                    st.warning(reply)
                else:
                    btn_txt = get_ui('ticket_btn_pro') if is_pro else get_ui('ticket_btn_guest')
                    if st.button(btn_txt):
                        if sub and msg:
                            st.success("✅ Ticket Sent!")
                            # 这里可以接入 pl.send_telegram_alert (如有配置)
                        else:
                            st.error("Please fill all fields.")
            
            # 6. 完整 FAQ
            st.caption("📚 Knowledge Base")
            for cat, qas in pd.FAQ_DB.items():
                with st.expander(cat):
                    for q, a in qas:
                        st.markdown(f"**Q: {q}**\n\n{a}")
            
            # 7. 退出
            st.markdown("---")
            if st.button(get_ui('logout')):
                st.session_state.page = 1
                st.session_state.user_role = "Guest"
                st.rerun()

render_sidebar()

# 5. 页面路由逻辑
# ------------------------------------------

# === PAGE 1: LANDING (无侧边栏) ===
if st.session_state.page == 1:
    # 顶部小语言切换
    c_top1, c_top2 = st.columns([8, 1])
    with c_top2:
        st.session_state.lang = st.selectbox("🌐", ["English", "简体中文", "Español"], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 居中 Logo
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        try:
            st.image("logo.png", use_column_width=True)
        except:
            st.markdown("<h1 style='text-align:center;'>🧠 PromptLab AI</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center; color:grey;'>The Ultimate Enterprise Prompt Engine</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 左右分栏
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("🔓 Login / Access")
        tab1, tab2 = st.tabs(["👤 Guest Trial", "💎 PRO Login"])
        
        with tab1:
            email = st.text_input(get_ui('email'), key="g_email")
            if st.button(get_ui('login_guest'), use_container_width=True):
                if email:
                    st.session_state.user_email = email
                    st.session_state.user_role = "Guest"
                    st.session_state.page = 2
                    st.rerun()
                else:
                    st.error("Please enter email.")
        
        with tab2:
            pe = st.text_input(get_ui('email'), key="p_email")
            pk = st.text_input(get_ui('key'), type="password")
            if st.button(get_ui('login_pro'), use_container_width=True):
                if pl.validate_license_key(pk):
                    st.session_state.user_email = pe
                    st.session_state.user_role = "PRO"
                    st.session_state.page = 2
                    st.rerun()
                else:
                    st.error("Invalid License Key")

    with col2:
        st.header("🆚 Compare Plans")
    
    # 🛡️ 关键修复：在这里单独引入 pandas 并改名为 pds
    # 这样无论外面的 pd 是什么，这里的表格都能正常工作！
    import pandas as pds

    # 豪华版数据
    compare_data = {
        "Feature": [
            "🧠 AI Engine", 
            "📝 Daily Text Gen", 
            "🎨 Daily Image Gen", 
            "🌍 Languages", 
            "📂 Batch Upload", 
            "💼 Commercial License", 
            "⚡ Support Speed"
        ],
        "👤 Free Guest": [
            "🐢 Standard", 
            "🔒 5 / Day", 
            "🔒 3 / Day", 
            "🔒 3 (Basic)", 
            "🔒 1 File", 
            "❌ No", 
            "🐢 Standard"
        ],
        "💎 PRO ($12.90)": [
            "🚀 Turbo Mode", 
            "✅ Unlimited", 
            "✅ 200 / Day", 
            "✅ 15 Global", 
            "✅ Batch 50+", 
            "✅ Included", 
            "⚡ Priority"
        ]
    }
    
    # 渲染表格 (注意：这里使用的是 pds，不是 pd)
    df_compare = pds.DataFrame(compare_data)
    
    st.dataframe(
        df_compare, 
        hide_index=True, 
        use_container_width=True, 
        column_config={
            "Feature": st.column_config.TextColumn("Feature", width="medium"),
            "👤 Free Guest": st.column_config.TextColumn("Free Guest", width="small"),
            "💎 PRO ($12.90)": st.column_config.TextColumn("💎 PRO Lifetime", width="small"),
        }
    )

    # Full Specs 展开项
    with st.expander("🔍 Click to view Full Specs (All 15 Languages & Modes)"):
        st.markdown("### 🌍 15 Supported Languages")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("- English\n- 简体中文\n- 繁體中文\n- Bahasa Melayu\n- 日本語")
        with c2:
            st.markdown("- 한국어 (Korean)\n- Español (Spanish)\n- Français (French)\n- Deutsch (German)\n- Русский (Russian)")
        with c3:
            st.markdown("- Português\n- Italiano\n- العربية (Arabic)\n- हिन्दी (Hindi)\n- ไทย (Thai)")

        st.markdown("---")
        st.markdown("### 🛠️ 18 Professional Modes")
        st.markdown("**Pedagogy, Creative Writing, Coding, SEO, Roleplay, Data Analysis, and more!**")
# === PAGE 2: ROLE HALL (侧边栏滑出) ===
elif st.session_state.page == 2:
    st.button(f"⬅️ {get_ui('back_home')}", on_click=lambda: st.session_state.update(page=1))
    st.title(get_ui('role_title'))
    
    roles = list(pd.ROLES_DB.keys())
    cols = st.columns(3)
    
    for i, role in enumerate(roles):
        with cols[i % 3]:
            if st.button(f"🎭 {role}", use_container_width=True, type="secondary"):
                st.session_state.current_role_card = role
                st.session_state.page = 3
                st.rerun()
            st.markdown("---")

# === PAGE 3: WORKSPACE (核心工作台) ===
elif st.session_state.page == 3:
    is_pro = st.session_state.user_role == "PRO"
    usage = pl.get_user_usage(st.session_state.user_email)
    
    # 顶部导航
    c_n1, c_n2 = st.columns([1, 5])
    with c_n1:
        if st.button("⬅️ Roles"):
            st.session_state.page = 2
            st.rerun()
    with c_n2:
        st.success(f"🛠️ **{st.session_state.current_role_card}** | {st.session_state.user_role}")

    # 额度显示
    limits = pl.LIMITS["PRO"] if is_pro else pl.LIMITS["FREE"]
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        txt_display = "Unlimited" if is_pro else f"{usage['text_count']}/{limits['text_daily']}"
        st.progress(0 if is_pro else min(usage['text_count']/5, 1.0), f"Text: {txt_display}")
    with col_l2:
        img_display = f"{usage['image_count']}/200" if is_pro else f"{usage['image_count']}/{limits['image_daily']}"
        st.progress(min(usage['image_count']/ (200 if is_pro else 3), 1.0), f"Image: {img_display}")

    st.markdown("---")

    # 核心表单
    role_data = pd.ROLES_DB[st.session_state.current_role_card]
    mode_names = list(role_data.keys())
    
    c_f1, c_f2 = st.columns([1, 1])
    
    with c_f1:
        # 1. 模式选择 (Mode Lock)
        # Guest 只能看到第一个，或者看到全部但点其他的报错
        # 这里为了体验，展示全部，但选2/3时提示
        sel_mode = st.selectbox(get_ui('mode_sel'), mode_names)
        
        if not is_pro and sel_mode != mode_names[0]:
            st.error(f"🔒 {sel_mode} is locked for PRO users.")
            st.stop()
            
        # 2. 选项选择 (144+ Options)
        mode_data = role_data[sel_mode]
        sel_option = st.selectbox(get_ui('opt_sel'), mode_data["options"])
        
        # 3. 平台选择 (仅视觉类)
        platform = "General AI"
        if sel_mode in ["Visuals", "Thumbnail", "Product Shot"]:
            platform = st.selectbox("🎨 Platform", ["Midjourney v6", "Stable Diffusion", "DALL-E 3", "General AI"])

    with c_f2:
        # 4. 上传 (Upload Lock)
        help_txt = get_ui('batch_true') if is_pro else get_ui('batch_false')
        up_files = st.file_uploader(get_ui('upload'), accept_multiple_files=is_pro, help=help_txt)
        
        # 5. 输入框
        user_input = st.text_area("Input Topic", height=150, placeholder=mode_data["placeholder"])

    # 生成按钮
    if st.button(get_ui('generate'), type="primary", use_container_width=True):
        # 额度检查
        has_img = up_files is not None and (len(up_files) > 0 if isinstance(up_files, list) else True)
        u_type = "image" if has_img else "text"
        cur_usage = usage['image_count'] if has_img else usage['text_count']
        max_limit = limits['image_daily'] if has_img else limits['text_daily']
        
        if cur_usage >= max_limit:
            st.error(f"🚫 {get_ui('limit_reach')}")
        else:
            # 扣费
            pl.update_user_usage(st.session_state.user_email, u_type, 1)
            
            # 模拟生成 (Waiting Theater)
            with st.status(get_ui('wait'), expanded=True) as status:
                if not is_pro:
                    st.write("🐢 Standard Queue: Processing...")
                    progress_bar = status.progress(0)
                    for i in range(100):
                        time.sleep(0.03) # 3秒等待
                        progress_bar.progress(i+1)
                        if i == 50: st.write("💡 Tip: Upgrade to PRO for 0.5s speed...")
                else:
                    time.sleep(0.5) # PRO 极速
                status.update(label=get_ui('done'), state="complete")
            
            # 调用核心引擎
            final_prompt = pl.generate_pasec_prompt(
                st.session_state.current_role_card,
                sel_mode,
                sel_option,
                user_input,
                len(up_files) if up_files else 0,
                st.session_state.lang,
                is_pro
            )
            st.session_state.result = final_prompt
            st.rerun()

    # 结果展示 (5-Layer Deck)
    if 'result' in st.session_state:
        st.markdown("---")
        st.subheader("🎉 Result")
        st.text_area("Output", st.session_state.result, height=300)
        
        # Layer 1: Copy
        st.button(f"📋 {get_ui('copy')}", use_container_width=True)
        
        # Layer 2: AI Connect
        st.caption(f"🤖 {get_ui('connect')}")
        ai_links = [
            ("Gemini", "https://gemini.google.com"), ("ChatGPT", "https://chat.openai.com"),
            ("Claude", "https://claude.ai"), ("Midjourney", "https://discord.com"),
            ("Canva", "https://canva.com"), ("Notion", "https://notion.so")
        ]
        cols_ai = st.columns(6)
        for i, (name, link) in enumerate(ai_links):
            cols_ai[i].link_button(name, link)
            
        # Layer 3: Social
        st.caption("📤 Social Share")
        c_s1, c_s2, c_s3 = st.columns(3)
        # 微信 (绿色按钮)
        if c_s1.button("🟢 WeChat", disabled=not is_pro, help="Click to open system share menu"):
            st.info("📲 Please use your phone's 'Share' menu to send to WeChat.")
        # 系统分享
        c_s2.button("📤 System", help="Use native sharing")
        # WhatsApp
        txt_encoded = base64.b64encode(st.session_state.result.encode()).decode()
        c_s3.link_button("WhatsApp", f"https://wa.me/?text={st.session_state.result[:100]}...")

        # Layer 4: App Portals
        st.caption("📱 App Portals")
        c_a1, c_a2, c_a3 = st.columns(3)
        # 简单的链接跳转
        if is_pro:
            c_a1.link_button("Instagram", "https://instagram.com")
            c_a2.link_button("📕 XiaoHongShu", "https://xiaohongshu.com")
            c_a3.link_button("TikTok", "https://tiktok.com")
        else:
            st.warning("🔒 Upgrade to unlock App Portals")

        # Layer 5: Download
        st.caption(f"💾 {get_ui('download')}")
        d_c1, d_c2, d_c3 = st.columns(3)
        
        # TXT
        d_c1.download_button("📄 TXT", st.session_state.result, "prompt.txt")
        
        # PDF (防崩溃)
        if is_pro:
            pdf_bytes = pl.create_pdf_bytes(st.session_state.result)
            d_c2.download_button("📕 PDF", pdf_bytes, "prompt.pdf", mime="application/pdf")
        else:
            d_c2.button("🔒 PDF", disabled=True)
            
        # CSV
        if is_pro:
            csv_data = "\ufeff" + st.session_state.result # BOM
            d_c3.download_button("📊 CSV", csv_data, "prompt.csv", mime="text/csv")
        else:
            d_c3.button("🔒 CSV", disabled=True)
