# === PAGE 1: LANDING (大企业级首页 - 带 Slogan) ===
if st.session_state.page == 1:
    # 1. 顶部留白 & 语言切换
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    c_top1, c_top2 = st.columns([9, 1])
    with c_top2:
        st.session_state.lang = st.selectbox("🌐", ["English", "简体中文", "Español"], label_visibility="collapsed")

    # 2. 🌟 HERO 区域 (Logo + 霸气 Slogan)
    # ------------------------------------------------
    # 这是一个居中的容器，专门放 Logo 和口号
    with st.container():
        c_hero1, c_hero2, c_hero3 = st.columns([1, 2, 1]) # 中间宽，两边窄，保证居中
        with c_hero2:
            st.image("logo.png", use_column_width=True) # Logo 居中
            
            # 👇 这里就是 Slogan！用了深蓝色 + 粗体，非常显眼
            st.markdown("""
            <div style='text-align: center; margin-top: -10px; margin-bottom: 40px;'>
                <h1 style='color: #0F52BA; font-size: 2.5rem; margin-bottom: 10px;'>
                    The Ultimate Enterprise Prompt Engine
                </h1>
                <p style='color: #5d6d7e; font-size: 1.2rem; font-weight: 500;'>
                    Empowering Educators with Scale, Security & Pedagogical Impact.
                </p>
                <div style="display: flex; justify-content: center; gap: 15px; margin-top: 15px; font-size: 0.9rem; color: #7f8c8d;">
                    <span style="background:#eef2f7; padding:5px 10px; border-radius:15px;">🛡️ Secure & Private</span>
                    <span style="background:#eef2f7; padding:5px 10px; border-radius:15px;">🚀 Turbo Engine</span>
                    <span style="background:#eef2f7; padding:5px 10px; border-radius:15px;">🌍 15+ Languages</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 3. 主要内容区 (双卡片布局：登录 vs 对比)
    # ------------------------------------------------
    main_c1, main_c2 = st.columns([4, 5], gap="large")
    
    # 左侧：登录卡片
    with main_c1:
        with st.container():
            enterprise_card() # 激活柔和阴影
            st.subheader("🔐 Secure Access")
            
            tab_login, tab_guest = st.tabs(["💎 PRO Login", "👤 Guest Trial"])
            
            with tab_login:
                st.markdown("<br>", unsafe_allow_html=True)
                st.text_input("Enterprise Email", key="p_email", placeholder="name@organization.com")
                st.text_input("License Key", key="p_key", type="password", placeholder="••••••••••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # 登录按钮
                if st.button(get_ui('login_pro'), use_container_width=True, type="primary", key="btn_pro_login"):
                    pk = st.session_state.p_key
                    pe = st.session_state.p_email
                    if pl.validate_license_key(pk):
                        st.session_state.user_email = pe
                        st.session_state.user_role = "PRO"
                        st.session_state.page = 2
                        st.rerun()
                    else:
                        st.error("Authentication Failed. Invalid Key.")
            
            with tab_guest:
                st.markdown("<br>", unsafe_allow_html=True)
                st.text_input("Email Address", key="g_email", placeholder="Enter email to continue...")
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                st.caption("Limited access to standard models and basic features.")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Continue as Guest", use_container_width=True, type="secondary", key="btn_guest_login"):
                    if st.session_state.g_email:
                        st.session_state.user_email = st.session_state.g_email
                        st.session_state.user_role = "Guest"
                        st.session_state.page = 2
                        st.rerun()

    # 右侧：对比表卡片
    with main_c2:
        with st.container():
            enterprise_card() # 激活柔和阴影
            st.subheader("📋 Plan Comparison")
            
            # 对比数据
            compare_data = {
                "Capability": ["🤖 Model Infrastructure", "⚡ Processing Speed", "📝 Text Generation", "🎨 Image Generation", "📂 Batch Operations", "💼 Commercial Rights"],
                "Starter (Guest)": ["Standard Shared", "Normal queue", "5 / day", "3 / day", "Single file", "❌ Non-commercial"],
                "Enterprise (PRO)": ["✅ Dedicated Turbo", "✅ Priority access", "✅ Unlimited", "✅ 200 / day", "✅ Bulk (50+)", "✅ Included"]
            }
            df_compare = pds.DataFrame(compare_data)
            
            st.dataframe(
                df_compare, 
                hide_index=True, 
                use_container_width=True,
                column_config={
                    "Capability": st.column_config.TextColumn("Capability", width="medium"),
                    "Starter (Guest)": st.column_config.TextColumn("Starter", width="small"),
                    "Enterprise (PRO)": st.column_config.TextColumn("💎 Enterprise", width="medium"),
                }
            )
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            st.info("💡 Enterprise plan includes advanced pedagogy modes, Python script generation, and priority support SLAs.")
