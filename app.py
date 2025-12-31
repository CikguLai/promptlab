# app.py (V9.28 - 2026 FINAL - FULL FEATURES)
import streamlit as st
import logic_core as lc
import data_matrix as dm
import time, os
import random

# 1. 设置
st.set_page_config(page_title="Lai's Lab AI", page_icon="🧬", layout="wide")

# 2. 读取 Secrets
if "general" in st.secrets:
    sec = st.secrets["general"]
    lc.CONFIG["EMAIL_SENDER_ADDRESS"] = sec.get("email_sender", "")
    lc.CONFIG["EMAIL_APP_PASSWORD"] = sec.get("email_app_password", "")
    lc.CONFIG["EMAIL_ADMIN_ADDRESS"] = sec.get("email_admin", "")
    lc.CONFIG["TELEGRAM_BOT_TOKEN"] = sec.get("telegram_token", "")
    lc.CONFIG["TELEGRAM_CHAT_ID"] = sec.get("telegram_chat_id", "")
    lc.CONFIG["LEMONSQUEEZY_API_KEY"] = sec.get("lemonsqueezy_key", "")
    lc.CONFIG["AIRTABLE_API_KEY"] = sec.get("airtable_key", "")
    lc.CONFIG["AIRTABLE_BASE_ID"] = sec.get("airtable_base_id", "")
    if "master_key" in sec: lc.CONFIG["MASTER_KEY"] = sec["master_key"]

# CSS 样式
st.markdown("""
<style>
    .compare-table { width: 100%; border-collapse: collapse; border: 1px solid #eee; background: white; font-size: 13px; margin-top: 10px; }
    .compare-table th { background: #f8f9fa; padding: 12px; border-bottom: 2px solid #ddd; text-align: left; color: #333; }
    .compare-table td { padding: 10px; border-bottom: 1px solid #eee; vertical-align: middle; color: #555; }
    .pro-column { background: #f0f7ff; color: #0277bd; font-weight: bold; border-left: 1px solid #cce5ff; }
    .price-tag { color: #d32f2f; font-size: 1.1em; font-weight: 800; }
    a:hover { text-decoration: underline !important; }
    .app-slogan { font-size: 18px; color: #555; margin-top: -15px; margin-bottom: 25px; font-weight: 500; letter-spacing: 0.5px; }
    .stProgress > div > div > div > div { background-color: #0277bd !important; }
    /* Footer 样式 */
    .footer-container { position: fixed; bottom: 0; left: 0; width: 100%; background: white; border-top: 1px solid #eee; padding: 20px; z-index: 999; text-align: center; }
</style>
""", unsafe_allow_html=True)

# Session 初始化
for key, val in {'logged_in': False, 'user_tier': 'Guest', 'user_email': '', 'daily_usage': 0, 'language': 'English'}.items():
    if key not in st.session_state: st.session_state[key] = val

# 🔥 核心：V9.28 原版 Footer
def render_footer():
    is_pro = st.session_state.user_tier == "Pro"
    tier_label = "💎 VERIFIED PRO ACCESS" if is_pro else "👤 STANDARD GUEST TRIAL"
    tier_color = "#0277bd" if is_pro else "#666"
    st.markdown(f"""
        <div class="footer-container">
            <div style="font-weight:bold; color:#333; margin-bottom:5px;">© 2025–2026 LAI'S LAB • V9.28 FINAL • <span style="color:{tier_color}">{tier_label}</span></div>
            <div style="font-size:10px; color:#999;">Disclaimer: AI outputs may vary. Users are responsible for content.</div>
            <div style="font-size:11px; color:#aaa; margin-top:5px;">
                👤 {st.session_state.user_email} | 🟢 System Operational | 
                <a href="https://app.lemonsqueezy.com/my-orders" target="_blank" style="color:#0277bd;font-weight:bold;">Lost Key?</a>
            </div>
        </div><div style="height:120px;"></div>
    """, unsafe_allow_html=True)

def show_login_page():
    st.write("🌍 Select Language")
    # 登录页语言选择
    lang_sel = st.selectbox("", dm.LANG_OPTIONS_GUEST, index=0, key="lang_login", label_visibility="collapsed")
    if st.session_state.language != lang_sel:
        st.session_state.language = lang_sel
        st.rerun()

    ui = dm.LANG_MAP.get(lang_sel, dm.LANG_MAP["default"])

    col1, col2 = st.columns([1, 1.4], gap="large")
    with col1:
        st.title(f"🧬 {ui.get('sidebar_title', 'Lais Lab')}")
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
            if st.button("💎 Activate Pro", key="l_pb", type="primary", use_container_width=True):
                if lc.check_user_tier(pe, lk) == "Pro":
                    st.session_state.user_email, st.session_state.user_tier, st.session_state.logged_in = pe, "Pro", True
                    st.balloons(); st.rerun()
            st.markdown('<div style="text-align: center; margin-top: 10px;"><a href="https://app.lemonsqueezy.com/my-orders" target="_blank" style="color: #666; font-size: 13px;">🔒 Lost Key?</a></div>', unsafe_allow_html=True)

    with col2:
        st.subheader("🆚 Compare Plans")
        headers = ui.get('tbl_headers', ["Capability", "Guest", "Pro"])
        rows = ui.get('tbl_data', dm.TABLE_EN)
        html = f'<table class="compare-table"><tr><th>{headers[0]}</th><th>{headers[1]}</th><th class="pro-column">{headers[2]}</th></tr>'
        for r in rows:
            v2 = f'<span class="price-tag">{r["v2"]}</span>' if "$" in r['v2'] else r['v2']
            html += f'<tr><td><b>{r["k"]}</b></td><td>{r["v1"]}</td><td class="pro-column">{v2}</td></tr>'
        st.markdown(html + "</table>", unsafe_allow_html=True)
    render_footer()

def show_main_app():
    ui = dm.LANG_MAP.get(st.session_state.language, dm.LANG_MAP["default"])
    
    with st.sidebar:
        st.caption(f"{'💎' if st.session_state.user_tier == 'Pro' else '👤'} {ui['plan_pro'] if st.session_state.user_tier == 'Pro' else ui['plan_guest']}")
        
        # 进度条
        can_gen, rem, tot = lc.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        bar_color = "#ff4b4b" if (tot - st.session_state.daily_usage) <= 1 else "#00f2fe"
        st.markdown(f"<style>.stProgress > div > div > div > div {{ background-image: linear-gradient(to right, {bar_color} 0%, {bar_color} 100%) !important; }}</style>", unsafe_allow_html=True)
        st.progress(st.session_state.daily_usage / tot)
        st.caption(f"📊 {ui['usage']}: {st.session_state.daily_usage} / {tot}")
        st.divider()
        
        # 🔥 语言切换 (全员开放)
        # 这里的 dm.LANG_OPTIONS_GUEST 已经是包含16种语言的完整列表了
        lang_sel_main = st.selectbox("Language", dm.LANG_OPTIONS_GUEST, index=dm.LANG_OPTIONS_GUEST.index(st.session_state.language) if st.session_state.language in dm.LANG_OPTIONS_GUEST else 0, key="lang_main")
        if st.session_state.language != lang_sel_main:
            st.session_state.language = lang_sel_main
            st.rerun() # 立即刷新界面
            
        role = st.selectbox(ui['role'], list(dm.ROLES_CONFIG.keys()))
        
        # FAQ 与 工单系统
        with st.expander("❓ FAQ / Support"):
            st.info("Ask keywords like 'refund' or 'key' in the main chat.")
            st.divider()
            ticket_msg = st.text_input("Submit Ticket:", placeholder="Issue description...")
            if st.button("📩 Send Ticket"):
                if ticket_msg:
                    lc.log_ticket_to_airtable(st.session_state.user_email, ticket_msg, st.session_state.user_tier)
                    st.success("Ticket Sent! Check email.")
        
        if st.button(ui['logout'], use_container_width=True): st.session_state.clear(); st.rerun()

    # 主界面
    st.header(f"🎭 {role}")
    st.markdown(f"""<div style="background: #fff9e6; border-left: 5px solid #ffcc00; padding: 10px; margin-bottom: 15px;"><span style="color: #856404;">🔥 <b>{ui.get('live_stat', 'Live')}:</b> {random.randint(100, 200)} Users active</span></div>""", unsafe_allow_html=True)

    mode = st.selectbox(ui['mode'], list(dm.ROLES_CONFIG[role].keys()))
    
    if lc.check_mode_lock(st.session_state.user_tier, mode):
        st.error(ui['lock_msg']); st.link_button(ui['buy_btn'], "https://laislab.lemonsqueezy.com/buy")
    else:
        opt = st.selectbox(ui['action'], [o["label"] for o in dm.ROLES_CONFIG[role][mode]])
        tone = st.selectbox(ui['tone'], dm.ROLE_TONES.get(role, dm.DEFAULT_TONES))
        
        input_help = "Enter your specific request..." if "Custom" in opt else ui['input_label']
        inp = st.text_area(input_help, height=150)
        
        if st.button(ui['generate'], type="primary", use_container_width=True):
            if inp:
                is_intercept, reply = lc.smart_intercept(inp)
                if is_intercept:
                    st.success("🤖 AI Support:"); st.info(reply)
                elif can_gen:
                    st.session_state.daily_usage += 1
                    # 传入当前选中的 language，AI 就会用该语言输出
                    res = lc.generate_pasec_prompt(role, mode, opt, inp, st.session_state.user_tier, st.session_state.language, tone)
                    st.markdown(f"### {ui['result']}"); st.text_area("Payload:", value=res, height=300)
                    
                    c1, c2 = st.columns(2)
                    with c1: st.link_button("🟢 WhatsApp", lc.get_whatsapp_link(res), use_container_width=True)
                    with c2: 
                        if st.session_state.user_tier == "Pro":
                            pdf = lc.create_pdf(res, role, mode)
                            if pdf: st.download_button("📕 Download PDF", pdf, "report.pdf", "application/pdf", use_container_width=True)

    render_footer()

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
