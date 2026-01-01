# app.py (V9.28 - PRODUCTION READY - FINAL)
import streamlit as st
import logic_core as lc
import data_matrix as dm
import random
from datetime import datetime

st.set_page_config(page_title="Lai's Lab AI", page_icon="🧬", layout="wide")

st.markdown("""
<style>
    .footer-container { position: fixed; bottom: 0; left: 0; width: 100%; background: white; border-top: 1px solid #eee; padding: 15px 0; z-index: 1000; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 5px; }
    .footer-row-1 { font-weight: bold; color: #333; font-size: 13px; }
    .footer-row-2 { font-size: 10px; color: #999; font-style: italic; }
    .footer-row-3 { font-size: 11px; color: #aaa; margin-top: 5px; display: flex; gap: 15px; }
    .price-strike { text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 5px; }
    .price-promo { color: #d32f2f; font-weight: 800; font-size: 1.1em; }
    .stProgress > div > div > div > div { background-color: #0277bd !important; }
</style>
""", unsafe_allow_html=True)

defaults = {'logged_in': False, 'user_tier': 'Guest', 'user_email': '', 'daily_usage': 0, 'language': 'English', 'output_language': 'English'}
for key, val in defaults.items():
    if key not in st.session_state: st.session_state[key] = val

if "general" in st.secrets:
    sec = st.secrets["general"]
    lc.CONFIG["EMAIL_SENDER_ADDRESS"] = sec.get("email_sender", "")
    lc.CONFIG["EMAIL_APP_PASSWORD"] = sec.get("email_app_password", "")
    lc.CONFIG["TELEGRAM_BOT_TOKEN"] = sec.get("telegram_token", "")
    lc.CONFIG["TELEGRAM_CHAT_ID"] = sec.get("telegram_chat_id", "")
    lc.CONFIG["LEMONSQUEEZY_API_KEY"] = sec.get("lemonsqueezy_key", "")
    lc.CONFIG["AIRTABLE_API_KEY"] = sec.get("airtable_key", "")
    lc.CONFIG["AIRTABLE_BASE_ID"] = sec.get("airtable_base_id", "")
    if "master_key" in sec: lc.CONFIG["MASTER_KEY"] = sec["master_key"]

def render_footer():
    current_hour = datetime.now().hour
    online_count = 110 + (current_hour * 4) + random.randint(1, 10)
    tier_label = "💎 VERIFIED PRO ACCESS" if st.session_state.user_tier == "Pro" else "👤 STANDARD GUEST TRIAL"
    tier_color = "#0277bd" if st.session_state.user_tier == "Pro" else "#666"
    st.markdown(f"""<div class="footer-container"><div class="footer-row-1">© 2025-2026 LAI'S LAB &nbsp; • &nbsp; <span style="color:#999;font-weight:400;">SYSTEM V9.28 PRO AUDIT</span> &nbsp; • &nbsp; <span style="color:{tier_color}">{tier_label}</span></div><div class="footer-row-2">Generative AI can make mistakes. Users are responsible for usage.</div><div class="footer-row-3"><span><b>Status:</b> <span style="color:#28a745;">🟢 Operational</span></span><span><b>Live:</b> {online_count}</span><span>Privacy</span></div></div><div style="height: 120px;"></div>""", unsafe_allow_html=True)

def show_login_page():
    st.write("🌍 Select Language")
    try: idx = dm.LANG_OPTIONS_GUEST.index(st.session_state.language)
    except: idx = 0
    lang_sel = st.selectbox("", dm.LANG_OPTIONS_GUEST, index=idx, key="lang_login", label_visibility="collapsed")
    if st.session_state.language != lang_sel:
        st.session_state.language = lang_sel
        st.rerun()
    ui = dm.get_safe_ui(lang_sel)
    col1, col2 = st.columns([1, 1.4], gap="large")
    with col1:
        # 🔥 LOGO HERE
        try: st.image("logo.png", width=120)
        except: pass
        st.title(f"🧬 {ui['sidebar_title']}")
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
    ui = dm.get_safe_ui(st.session_state.language)
    with st.sidebar:
        # 🔥 LOGO HERE
        try: st.image("logo.png", use_container_width=True)
        except: st.markdown("## 🧬 Lai's Lab")
        st.caption(f"{'💎' if st.session_state.user_tier == 'Pro' else '👤'} {ui['plan_pro'] if st.session_state.user_tier == 'Pro' else ui['plan_guest']}")
        can_gen, rem, tot = lc.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        bar_color = "#ff4b4b" if (tot - st.session_state.daily_usage) <= 1 else "#00f2fe"
        st.markdown(f"<style>.stProgress > div > div > div > div {{ background-image: linear-gradient(to right, {bar_color} 0%, {bar_color} 100%) !important; }}</style>", unsafe_allow_html=True)
        st.progress(st.session_state.daily_usage / tot)
        st.caption(f"📊 {ui['usage']}: {st.session_state.daily_usage} / {tot}")
        st.divider()
        lang_opts = dm.LANG_OPTIONS_PRO if st.session_state.user_tier == "Pro" else dm.LANG_OPTIONS_GUEST
        try: idx = lang_opts.index(st.session_state.language)
        except: idx = 0
        lang_sel_main = st.selectbox(ui['lang'], lang_opts, index=idx, key="lang_main")
        if st.session_state.language != lang_sel_main:
            st.session_state.language = lang_sel_main
            st.session_state.output_language = lang_sel_main
            st.rerun()
        role = st.selectbox(ui['role'], list(dm.ROLES_CONFIG.keys()))
        with st.expander(ui['faq_title'], expanded=False):
            st.markdown(f"**{ui['quick_ans']}**")
            current_faq_list = dm.FAQ_DATABASE.get(st.session_state.language, dm.FAQ_DATABASE["English"])
            faq_qs = [item["q"] for item in current_faq_list]
            selected_q = st.selectbox(ui['sel_topic'], faq_qs)
            ans = next((item["a"] for item in current_faq_list if item["q"] == selected_q), "")
            st.info(ans)
            st.divider()
            st.markdown(f"**{ui['submit_ticket']}**")
            ticket_opts = dm.get_ticket_types(st.session_state.language)
            ticket_type = st.selectbox(ui['type_lbl'], ticket_opts, key="t_type")
            ticket_msg = st.text_area(ui['issue_lbl'], height=80, key="t_msg")
            if st.button(ui['send_btn'], use_container_width=True):
                if ticket_msg:
                    is_intercept, reply = lc.smart_intercept(ticket_msg, st.session_state.language)
                    if is_intercept:
                        st.warning(f"⚠️ {reply}")
                        st.caption("If this didn't help, click Send again.")
                    else:
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
        try: out_idx = dm.LANG_OPTIONS_PRO.index(st.session_state.output_language)
        except: out_idx = 0
        c_lang, c_tone = st.columns([1, 1])
        with c_lang:
            output_lang_sel = st.selectbox(ui['out_lang_lbl'], dm.LANG_OPTIONS_PRO, index=out_idx, key="lang_out")
            if st.session_state.output_language != output_lang_sel: st.session_state.output_language = output_lang_sel
        with c_tone: tone = st.selectbox(ui['tone_lbl'], dm.ROLE_TONES.get(role, dm.DEFAULT_TONES))
        input_help = "Enter your specific request..." if "Custom" in opt else ui['input_label']
        inp = st.text_area(input_help, height=150)
        
        if st.button(ui['generate'], type="primary", use_container_width=True):
            if inp:
                is_intercept, reply = lc.smart_intercept(inp, st.session_state.language)
                if is_intercept:
                    st.success("🤖 AI Support:"); st.info(reply)
                elif can_gen:
                    st.session_state.daily_usage += 1
                    res = lc.generate_pasec_prompt(role, mode, opt, inp, st.session_state.user_tier, st.session_state.output_language, tone)
                    
                    st.markdown(f"### {ui['result']}")
                    # Layer 1: Copy
                    st.caption(ui['ad_copy'])
                    st.code(res, language="text") 
                    
                    # Layer 2: AI Connect
                    st.caption(ui['ad_connect'])
                    l2_1, l2_2, l2_3, l2_4 = st.columns(4)
                    with l2_1: st.link_button("ChatGPT", "https://chat.openai.com", use_container_width=True)
                    with l2_2: st.link_button("Gemini", "https://gemini.google.com", use_container_width=True)
                    with l2_3: st.link_button("Claude", "https://claude.ai", use_container_width=True)
                    with l2_4: st.link_button("Perplexity", "https://www.perplexity.ai", use_container_width=True)
                    l2_5, l2_6, l2_7, l2_8 = st.columns(4)
                    with l2_5: st.link_button("Midjourney", "https://www.midjourney.com", use_container_width=True)
                    with l2_6: st.link_button("Stable Diffusion", "https://stablediffusionweb.com", use_container_width=True)
                    with l2_7: st.link_button("Notion", "https://www.notion.so", use_container_width=True)
                    with l2_8: st.link_button("Canva", "https://www.canva.com", use_container_width=True)

                    # Layer 3: Social Share
                    st.caption(ui['ad_social'])
                    s_links = lc.get_social_links(res)
                    s1, s2, s3, s4 = st.columns(4)
                    with s1: st.link_button("WhatsApp", s_links['WhatsApp'], use_container_width=True)
                    with s2: st.link_button("Telegram", s_links['Telegram'], use_container_width=True)
                    with s3: st.link_button("Email", s_links['Email'], use_container_width=True)
                    with s4: st.link_button("X (Twitter)", s_links['X'], use_container_width=True)

                    # Layer 4: App Manual
                    st.caption(ui['ad_manual'])
                    m1, m2, m3 = st.columns(3)
                    with m1: 
                        if st.button("Instagram", use_container_width=True): st.toast(ui['ad_toast'])
                    with m2: 
                        if st.button("TikTok", use_container_width=True): st.toast(ui['ad_toast'])
                    with m3: 
                        if st.button("WeChat/XHS", use_container_width=True): st.toast(ui['ad_toast'])

                    # Layer 5: Download
                    st.caption(ui['ad_download'])
                    d1, d2, d3 = st.columns(3)
                    with d1: st.download_button("📄 TXT", res, "prompt.txt", use_container_width=True)
                    with d2:
                        if st.session_state.user_tier == "Pro":
                            pdf = lc.create_pdf(res, role, mode)
                            if pdf: st.download_button("📕 PDF", pdf, "report.pdf", "application/pdf", use_container_width=True)
                    with d3:
                        if st.session_state.user_tier == "Pro":
                            st.download_button("📊 CSV", lc.create_csv(res), "data.csv", "text/csv", use_container_width=True)

    render_footer()

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
