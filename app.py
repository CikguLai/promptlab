def show_login_page():
    st.write("🌍 Select Your Language / 选择您的语言")
    lang_sel = st.selectbox("", dm.LANG_OPTIONS_PRO, label_visibility="collapsed")
    st.session_state.language = lang_sel
    ui = dm.LANG_MAP.get(lang_sel, dm.LANG_MAP["default"])

    col1, col2 = st.columns([1, 1.4], gap="large")
    with col1:
        if os.path.exists("logo.png"): st.image("logo.png", width=110)
        
        # ✅ 修复：先定义变量，避开 f-string 内部反斜杠限制
        app_title = ui.get('sidebar_title', "Lai's Lab")
        st.title(f"🧬 {app_title}")
        
        # 3. 终极 Slogan
        st.markdown('<div class="app-slogan">🚀 Your Automated Prompt Engineer</div>', unsafe_allow_html=True)

        st.markdown(f'<p style="color:#e53935; background:#fff5f5; padding:10px; border-radius:5px;">🔥 <b>Lifetime Pro:</b> $12.90</p>', unsafe_allow_html=True)
        
        t1, t2 = st.tabs([ui['plan_guest'], ui['plan_pro']])
        with t1:
            e = st.text_input(ui['input_label'], key="l_e", placeholder="you@example.com")
            if st.button(ui['generate'], key="l_bt", use_container_width=True):
                if "@" in e: st.session_state.user_email, st.session_state.user_tier, st.session_state.logged_in = e, "Guest", True; st.rerun()
        with t2:
            pe = st.text_input("Billing Email", key="l_pe")
            lk = st.text_input("License Key", type="password")
            if st.button("💎 Activate Pro Access", key="l_pb", type="primary", use_container_width=True):
                if lc.check_user_tier(pe, lk) == "Pro":
                    st.session_state.user_email, st.session_state.user_tier, st.session_state.logged_in = pe, "Pro", True
                    st.balloons(); st.rerun()
            # 4. 找回 Key 链接
            st.markdown('<div style="text-align: center; margin-top: 15px;"><a href="https://app.lemonsqueezy.com/my-orders" target="_blank" style="color: #666; font-size: 13px; text-decoration: none;">🔒 Lost your key? Retrieve via LemonSqueezy</a></div>', unsafe_allow_html=True)

    with col2:
        # 5. 最新对比表
        st.subheader("🆚 Compare Plans")
        st.markdown(f"""
        <table class="compare-table">
            <tr><th>功能特性 (Capability)</th><th>访客试用 (Guest Trial)</th><th class="pro-column">💎 PRO 永久版 (Lifetime)</th></tr>
            <tr><td><b>每日生成限额 (Daily Limit)</b></td><td>5 次 / 天</td><td class="pro-column"><b>*Unlimited (无限生成)</b></td></tr>
            <tr><td><b>内容纯净度 (Format)</b></td><td>包含 AI 符号 (#, **)</td><td class="pro-column">100% 纯净 (人类书写感)</td></tr>
            <tr><td><b>结果分享与导出 (Sharing)</b></td><td>文本复制 + WhatsApp (带水印)</td><td class="pro-column">PDF 导出 + 纯净社媒分享</td></tr>
            <tr><td><b>全球语言支持 (Languages)</b></td><td>仅限 3 种基础语言</td><td class="pro-column">15+ 全球语言全开</td></tr>
            <tr><td><b>专业模式权限 (Expert Modes)</b></td><td>基础模式 (6个)</td><td class="pro-column">全部 18 种深度模式</td></tr>
            <tr><td><b>AI 结果水印 (Watermark)</b></td><td>强制包含推广水印</td><td class="pro-column">完全移除</td></tr>
            <tr><td><b>客服响应 (Support)</b></td><td>标准响应 (3-5天)</td><td class="pro-column">VIP 优先响应 (1-2天)</td></tr>
            <tr><td><b>价格 (Price)</b></td><td>免费 (Free)</td><td class="pro-column"><span class="price-tag">限时特惠 $12.90</span></td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.caption("* Fair Use Policy applies." if lang_sel == "English" else "* 遵循公平使用原则。")
    render_footer()
