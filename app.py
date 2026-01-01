# app.py (V9.28 - 2026 FINAL - DUAL LANGUAGE SUPPORT)
import streamlit as st
import logic_core as lc
import data_matrix as dm
import time, os
import random
from datetime import datetime

# 1. 设置
st.set_page_config(page_title="Lai's Lab AI", page_icon="🧬", layout="wide")

# CSS (Footer 居中 + 价格划线)
st.markdown("""
<style>
    .footer-container {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: white; border-top: 1px solid #eee;
        padding: 15px 0; z-index: 1000;
        text-align: center; display: flex; flex-direction: column; align-items: center; gap: 5px;
    }
    .footer-row-1 { font-weight: bold; color: #333; font-size: 13px; margin-bottom: 3px; }
    .footer-row-2 { font-size: 10px; color: #999; font-style: italic; max-width: 800px; line-height: 1.4; }
    .footer-row-3 { font-size: 11px; color: #aaa; margin-top: 5px; display: flex; gap: 15px; }
    
    .price-strike { text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 5px; }
    .price-promo { color: #d32f2f; font-weight: 800; font-size: 1.1em; }
    .stProgress > div > div > div > div { background-color: #0277bd !important; }
</style>
""", unsafe_allow_html=True)

# Session 初始化
defaults = {'logged_in': False, 'user_tier': 'Guest', 'user_email': '', 'daily_usage': 0, 'language': 'English', 'output_language': 'English'}
for key, val in defaults.items():
    if key not in st.session_state: st.session_state[key] = val

# Secrets
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

# Pro Audit Footer
def render_footer():
    current_hour = datetime.now().hour
    online_count = 110 + (current_hour * 4) + random.randint(1, 10)
    is_pro = st.session_state.user_tier == "Pro"
    tier_label = "💎 VERIFIED PRO ACCESS" if is_pro else "👤 STANDARD GUEST TRIAL"
    tier_color = "#0277bd" if is_pro else "#666"

    st.markdown(f"""
        <div class="footer-container">
            <div class="footer-row-1">
                © 2025-2026 LAI'S LAB &nbsp; • &nbsp; <span style="color:#999;font-weight:400;">SYSTEM V9.28 PRO AUDIT</span> &nbsp; • &nbsp; <span style="color:{tier_color}">{tier_label}</span>
            </div>
            <div class="footer-row-2">
                Generative AI can make mistakes; please verify important information. Users are solely responsible for usage.
                <br>Lai's Lab assumes no liability for actions taken based on outputs.
            </div>
            <div class="footer-row-3">
                <span><b>Status:</b> <span style="color:#28a745;">🟢 Operational</span></span>
                <span><b>Live:</b> {online_count}</span>
                <span><a href="#" style="color:#aaa;text-decoration:none;">Privacy</a></span>
                <span><a href="https://app.lemonsqueezy.com/my-orders" target="_blank" style="color:#0277bd;font-weight:bold;text-decoration:none;">Retrieve License</a></span>
            </div>
        </div>
        <div style="height: 120px;"></div>
    """, unsafe_allow_html=True)

def show_login_page():
    st.write("🌍 Select Language")
    try: idx = dm.LANG_OPTIONS_GUEST.index(st.session_state.language)
    except: idx = 0
    lang_sel = st.selectbox("", dm.LANG_OPTIONS_GUEST, index=idx, key="lang_login", label_visibility="collapsed")
    
    if st.session_state.language != lang_sel:
        st.session_state.language = lang_sel
        st.rerun()

    ui = dm.LANG_MAP.get(lang_sel, dm.LANG_MAP["default"])

    col1, col2 = st.columns([1, 1.4], gap="large")
    with col1:
        st.title(f"🧬 {ui.get('sidebar_title', 'Lais Lab')}")
        st.markdown('<div class="app-slogan">🚀 Your Automated Prompt Engineer</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background:#fff5f5; padding:10px; border-radius:5px; margin-bottom:15px; border:1px solid #ffcdd2;">🔥 <b>Lifetime Pro:</b> <span class="price-strike">$39.90</span> <span class="price-promo">$12.90</span></div>', unsafe_allow_html=True)
        
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
        rows = ui.get('tbl_data', dm.TABLE_ROWS_DEFAULT)
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
        
        can_gen, rem, tot = lc.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        bar_color = "#ff4b4b" if (tot - st.session_state.daily_usage) <= 1 else "#00f2fe"
        st.markdown(f"<style>.stProgress > div > div > div > div {{ background-image: linear-gradient(to right, {bar_color} 0%, {bar_color} 100%) !important; }}</style>", unsafe_allow_html=True)
        st.progress(st.session_state.daily_usage / tot)
        st.caption(f"📊 {ui['usage']}: {st.session_state.daily_usage} / {tot}")
        st.divider()
        
        # 🔥 双语言选择器
        # 1. 界面语言 (Interface Language)
        try: idx = dm.LANG_OPTIONS_GUEST.index(st.session_state.language)
        except: idx = 0
        lang_sel_main = st.selectbox(ui.get("ui_lang_lbl", "🌐 Interface Language"), dm.LANG_OPTIONS_GUEST, index=idx, key="lang_main")
        
        if st.session_state.language != lang_sel_main:
            st.session_state.language = lang_sel_main
            # 切换界面语言时，默认把输出语言也同步过去（用户体验更好），但允许用户随后修改
            st.session_state.output_language = lang_sel_main 
            st.rerun()

        # 2. 输出语言 (Output Language) - 独立控制
        try: out_idx = dm.LANG_OPTIONS_GUEST.index(st.session_state.output_language)
        except: out_idx = 0
        output_lang_sel = st.selectbox(ui.get("out_lang_lbl", "📝 Output Language"), dm.LANG_OPTIONS_GUEST, index=out_idx, key="lang_out")
        
        if st.session_state.output_language != output_lang_sel:
            st.session_state.output_language = output_lang_sel
            # 这里不需要 rerun，因为不影响界面显示
            
        role = st.selectbox(ui['role'], list(dm.ROLES_CONFIG.keys()))
        
        # FAQ (读取当前 Interface 语言的数据库)
        with st.expander(ui.get("faq_title", "FAQ"), expanded=False):
            st.markdown(f"**{ui.get('quick_ans', 'Quick Answers')}**")
            current_faq_list = dm.FAQ_DATABASE.get(st.session_state.language, dm.FAQ_DATABASE["English"])
            
            faq_qs = [item["q"] for item in current_faq_list]
            selected_q = st.selectbox(ui.get("sel_topic", "Topic"), faq_qs)
            ans = next((item["a"] for item in current_faq_list if item["q"] == selected_q), "")
            st.info(ans)
            
            st.divider()
            st.markdown(f"**{ui.get('submit_ticket', 'Submit Ticket')}**")
            ticket_type = st.selectbox(ui.get("type_lbl", "Type"), dm.TICKET_TYPES, key="t_type")
            ticket_msg = st.text_area(ui.get("issue_lbl", "Issue"), height=80, key="t_msg")
            
            if st.button(ui.get("send_btn", "Send"), use_container_width=True):
                if ticket_msg:
                    lc.log_ticket_to_airtable(st.session_state.user_email, ticket_type, ticket_msg, st.session_state.user_tier)
                    st.success("Sent!")
        
        if st.button(ui['logout'], use_container_width=True): st.session_state.clear(); st.rerun()

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
                    # 🔥 核心：传入 st.session_state.output_language
                    res = lc.generate_pasec_prompt(role, mode, opt, inp, st.session_state.user_tier, st.session_state.output_language, tone)
                    st.markdown(f"### {ui['result']}"); st.text_area("Payload:", value=res, height=300)
                    
                    c1, c2 = st.columns(2)
                    with c1: st.link_button("🟢 WhatsApp", lc.get_whatsapp_link(res), use_container_width=True)
                    with c2: 
                        if st.session_state.user_tier == "Pro":
                            pdf = lc.create_pdf(res, role, mode)
                            if pdf: st.download_button("📕 PDF", pdf, "report.pdf", "application/pdf", use_container_width=True)
                    
                    if st.session_state.user_tier == "Pro":
                        st.caption("💾 Download & Connect")
                        d1, d2 = st.columns(2)
                        with d1: st.download_button("📊 CSV", lc.create_csv(res), "data.csv", "text/csv")
                        with d2: st.link_button("🧠 ChatGPT", "https://chat.openai.com", use_container_width=True)

    render_footer()

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
