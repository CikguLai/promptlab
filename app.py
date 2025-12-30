# app.py (V9.28 - Global 15 & Clean Layout)
import streamlit as st
import logic_core as lc
import data_matrix as dm
import time, os

st.set_page_config(page_title="Lai's Lab AI", layout="wide")

# 全量 CSS 保持页面美观
st.markdown("""
<style>
    .compare-table { width: 100%; border-collapse: collapse; border: 1px solid #eee; background: white; font-size: 14px; }
    .compare-table th { background: #f8f9fa; padding: 12px; border-bottom: 2px solid #ddd; }
    .compare-table td { padding: 10px; border-bottom: 1px solid #eee; }
    .pro-column { background: #f0f7ff; color: #0277bd; font-weight: bold; }
    .footer-box { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; padding: 10px; background: white; border-top: 1px solid #eee; color: #999; font-size: 11px; z-index: 1000; }
</style>
""", unsafe_allow_html=True)

# Session 初始化
for key, val in {'logged_in': False, 'user_tier': 'Guest', 'user_email': '', 'daily_usage': 0, 'language': 'English'}.items():
    if key not in st.session_state: st.session_state[key] = val

def show_login_page():
    # ✅ 修正：登录页 15 种语言全开
    st.write("🌍 Select Your Language / 选择您的语言")
    lang_sel = st.selectbox("", dm.LANG_OPTIONS_PRO, label_visibility="collapsed")
    st.session_state.language = lang_sel
    ui = dm.LANG_MAP.get(lang_sel, dm.LANG_MAP["default"])

    col1, col2 = st.columns([1, 1.4], gap="large")
    with col1:
        if os.path.exists("logo.png"): st.image("logo.png", width=110)
        st.title(ui.get('sidebar_title', "Lai's Lab"))
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
        st.markdown('<p style="text-align:center; font-size:12px;"><a href="https://app.lemonsqueezy.com/my-orders" target="_blank">🔒 Forgot License?</a></p>', unsafe_allow_html=True)

    with col2:
        # ✅ 修正：对比表详细内容
        st.subheader("🆚 Compare Plans")
        st.markdown(f"""
        <table class="compare-table">
            <tr><th>Capability</th><th>Guest Trial</th><th class="pro-column">💎 PRO Lifetime</th></tr>
            <tr><td><b>Daily Limit</b></td><td>5 / Day</td><td class="pro-column">Unlimited*</td></tr>
            <tr><td><b>Content Format</b></td><td>With AI Symbols (#, **)</td><td class="pro-column">Clean & Human-like</td></tr>
            <tr><td><b>Languages</b></td><td>3 Basic</td><td class="pro-highlight">15 Global</td></tr>
            <tr><td><b>WhatsApp Share</b></td><td>With Watermark</td><td class="pro-column">Pure Content</td></tr>
            <tr><td><b>PDF Export</b></td><td>❌ Locked</td><td class="pro-column">✅ Unlocked</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.caption("* Fair Use Policy applies." if lang_sel == "English" else "* 遵循公平使用原则。")

def show_main_app():
    ui = dm.LANG_MAP.get(st.session_state.language, dm.LANG_MAP["default"])
    with st.sidebar:
        st.caption(f"💎 {ui['plan_pro']}" if st.session_state.user_tier == "Pro" else f"👤 {ui['plan_guest']}")
        # 限额逻辑
        can_gen, rem, tot = lc.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        st.progress(st.session_state.daily_usage / tot); st.caption(f"{ui['usage']}: {st.session_state.daily_usage} / {tot}")
        st.divider()
        langs = dm.LANG_OPTIONS_PRO if st.session_state.user_tier == "Pro" else dm.LANG_OPTIONS_GUEST
        st.session_state.language = st.selectbox("Language", langs, index=langs.index(st.session_state.language) if st.session_state.language in langs else 0)
        role = st.selectbox(ui['role'], list(dm.ROLES_CONFIG.keys()))
        if st.button(ui['logout'], use_container_width=True): st.session_state.clear(); st.rerun()

    st.header(f"🎭 {role}")
    mode = st.selectbox(ui['mode'], list(dm.ROLES_CONFIG[role].keys()))
    if lc.check_mode_lock(st.session_state.user_tier, mode):
        st.error(ui['lock_msg']); st.link_button(ui['buy_btn'], "https://laislab.lemonsqueezy.com/buy")
    else:
        opt = st.selectbox(ui['action'], [o["label"] for o in dm.ROLES_CONFIG[role][mode]])
        tone = st.selectbox(ui['tone'], dm.ROLE_TONES.get(role, dm.DEFAULT_TONES))
        inp = st.text_area(ui['input_label'], height=150)
        if st.button(ui['generate'], type="primary", use_container_width=True):
            if inp and can_gen:
                st.session_state.daily_usage += 1
                if st.session_state.user_tier == "Guest": time.sleep(1.5)
                res = lc.generate_pasec_prompt(role, mode, opt, inp, st.session_state.user_tier, st.session_state.language, tone)
                st.markdown(f"### {ui['result']}"); st.text_area("Payload:", value=res, height=300)
                
                c1, c2 = st.columns(2)
                with c1:
                    wa_url = lc.get_whatsapp_link(res) # ✅ 分享功能
                    st.link_button("🟢 WhatsApp Share", wa_url, use_container_width=True)
                with c2:
                    if st.session_state.user_tier == "Pro":
                        pdf = lc.create_pdf(res, role, mode)
                        if pdf: st.download_button("📕 Download PDF", pdf, "report.pdf", "application/pdf", use_container_width=True)

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
    st.markdown(f'<div class="footer-box">© 2025 Lai\'s Lab | System V9.28 | {st.session_state.user_email}</div>', unsafe_allow_html=True)
