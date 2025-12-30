# app.py (V9.24 Professional)
import streamlit as st
import time, base64, os
import logic_core as lc
import data_matrix as dm

st.set_page_config(page_title="Lai's Lab AI", page_icon="🧬", layout="wide")

# 全量商业 CSS
st.markdown("""
<style>
    .promo-box { background: #fff5f5; border-radius: 8px; padding: 15px; border-left: 5px solid #e53935; margin-bottom: 20px; }
    .compare-table { width: 100%; border-collapse: collapse; border: 1px solid #eee; background: white; font-size: 14px; }
    .compare-table th { background: #fafafa; padding: 12px; text-align: left; border-bottom: 2px solid #eee; }
    .compare-table td { padding: 10px; border-bottom: 1px solid #f9f9f9; }
    .pro-highlight { background: #f0f7ff; color: #0277bd; font-weight: bold; }
    .footer-box { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; padding: 10px; background: white; border-top: 1px solid #eee; color: #888; font-size: 12px; z-index: 100; }
    .sidebar-footer { font-size: 11px; color: #bbb; text-align: center; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# 动态加载 Secrets
if "general" in st.secrets:
    for k, v in st.secrets["general"].items():
        if k.upper() in lc.CONFIG: lc.CONFIG[k.upper()] = v

# Session 初始化
for key, val in {'logged_in': False, 'user_tier': 'Guest', 'user_email': '', 'daily_usage': 0, 'language': 'English'}.items():
    if key not in st.session_state: st.session_state[key] = val

def render_footer():
    st.markdown(f'<div class="footer-box">© 2025 Lai\'s Lab | System V9.24 Enterprise | User: {st.session_state.user_email if st.session_state.user_email else "Visitor"}</div>', unsafe_allow_html=True)

def show_login_page():
    c1, c2 = st.columns([1, 1.4], gap="large")
    with c1:
        if os.path.exists("logo.png"): st.image("logo.png", width=120)
        st.title("PromptLab AI V9.24")
        st.markdown('<div class="promo-box">🔥 <b>Flash Sale:</b> Lifetime Pro <b style="color:#e53935">$12.90</b> <strike>$39.90</strike></div>', unsafe_allow_html=True)
        
        t1, t2 = st.tabs(["👤 Guest Trial", "💎 Activate Pro"])
        with t1:
            e = st.text_input("Enter Email to Start", key="login_e")
            if st.button("🚀 Start 5-Day Trial", use_container_width=True):
                if "@" in e: st.session_state.user_email, st.session_state.user_tier, st.session_state.logged_in = e, "Guest", True; st.rerun()
                else: st.error("Invalid Email Address")
        with t2:
            pe = st.text_input("Billing Email")
            lk = st.text_input("License Key", type="password")
            if st.button("💎 Activate Now", type="primary", use_container_width=True):
                if lc.check_user_tier(pe, lk) == "Pro":
                    st.session_state.user_email, st.session_state.user_tier, st.session_state.logged_in = pe, "Pro", True
                    st.balloons(); time.sleep(1); st.rerun()
                else: st.error("Verification Failed")
            # ✅ 补全：找回链接
            st.markdown('<p style="text-align:center; font-size:12px; margin-top:10px;"><a href="https://app.lemonsqueezy.com/my-orders" target="_blank">🔒 Forgot License Key?</a></p>', unsafe_allow_html=True)

    with c2:
        # ✅ 补全：方案对比表
        st.subheader("🆚 Compare Plans")
        st.markdown("""
        <table class="compare-table">
            <tr><th>Capability</th><th>Guest Trial</th><th class="pro-highlight">💎 PRO Lifetime</th></tr>
            <tr><td>Daily AI Generation</td><td>5 Times</td><td class="pro-highlight">1,000 Times</td></tr>
            <tr><td>Global Languages</td><td>3 (Basic)</td><td class="pro-highlight">15 (Global)</td></tr>
            <tr><td>Expert Modes</td><td>Free Modes Only</td><td class="pro-highlight">All 18 Modes</td></tr>
            <tr><td>AI Watermark</td><td>Included</td><td class="pro-highlight">Removed</td></tr>
            <tr><td>PDF Export</td><td>No</td><td class="pro-highlight">Yes</td></tr>
            <tr><td>Support priority</td><td>Normal</td><td class="pro-highlight">VIP Priority</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.info("💡 Pro Users enjoy the ultra-fast Turbo generation engine.")

def show_main_app():
    ui = dm.LANG_MAP.get(st.session_state.language, dm.LANG_MAP["default"])
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png", width=80)
        st.caption(f"Status: {st.session_state.user_tier}")
        can_gen, rem, tot = lc.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        st.progress(st.session_state.daily_usage / tot); st.caption(f"Usage: {st.session_state.daily_usage} / {tot}")
        st.divider()
        langs = dm.LANG_OPTIONS_PRO if st.session_state.user_tier == "Pro" else dm.LANG_OPTIONS_GUEST
        st.session_state.language = st.selectbox("Global Language", langs, index=langs.index(st.session_state.language) if st.session_state.language in langs else 0)
        role = st.selectbox("Role Expert", list(dm.ROLES_CONFIG.keys()))
        
        with st.expander("❓ FAQ & Help"):
            for q in dm.FAQ_LIST: st.write(f"• {q}") # ✅ 补全：完整 16 项 FAQ
            
        with st.expander("✉️ Support Tickets"):
            tt = st.selectbox("Type", ["Question", "Bug", "Billing", "Feature", "VIP Support"])
            ts = st.text_input("Subject")
            tm = st.text_area("Message")
            if st.button("Submit Ticket"):
                intercept, ans = lc.smart_intercept(ts) # ✅ 黑科技：拦截器
                if intercept: st.warning(ans)
                else:
                    tid = int(time.time()); lc.log_ticket_to_airtable(tid, st.session_state.user_email, st.session_state.user_tier, tt, ts, tm)
                    lc.send_auto_reply_email(st.session_state.user_email, st.session_state.user_tier, tid, ts)
                    st.success(f"Ticket #{tid} Sent!")
        
        st.divider()
        if st.button("Logout", use_container_width=True): st.session_state.clear(); st.rerun()

    st.header(f"🎭 {role} Dashboard")
    modes = list(dm.ROLES_CONFIG[role].keys())
    mode = st.selectbox("Mode", modes)
    
    # ✅ 黑科技：模式锁检测
    if lc.check_mode_lock(st.session_state.user_tier, mode):
        st.error("🔒 This is a Pro Mode"); st.link_button("💎 Upgrade to Unlock All 18 Modes", "https://laislab.lemonsqueezy.com/buy", type="primary")
    else:
        opt = st.selectbox("Action", [o["label"] for o in dm.ROLES_CONFIG[role][mode]])
        tone = st.selectbox("Tone / Style", dm.ROLE_TONES.get(role, dm.DEFAULT_TONES))
        inp = st.text_area("Input Context", height=150, placeholder="Type your requirements here...")
        
        if st.button("Generate System Payload", type="primary", use_container_width=True):
            if not inp: st.warning("Please provide input content.")
            elif not can_gen: st.error("Daily usage limit reached.")
            else:
                st.session_state.daily_usage += 1
                if st.session_state.user_tier == "Guest": 
                    with st.status("AI Analyzing..."): time.sleep(1.5) # ✅ 黑科技：假拖延
                
                res = lc.generate_pasec_prompt(role, mode, opt, inp, st.session_state.user_tier, st.session_state.language, tone)
                st.markdown("### 🧬 Optimized Output")
                st.text_area("Payload Result:", value=res, height=350)
                
                if st.session_state.user_tier == "Pro":
                    pdf = lc.create_pdf(res, role, mode) # ✅ 黑科技：PDF 导出
                    if pdf: st.download_button("📕 Download PDF Report", pdf, "report.pdf", "application/pdf", use_container_width=True)

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
    render_footer()
