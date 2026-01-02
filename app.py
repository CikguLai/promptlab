# app.py (V9.33 - COMMERCIAL RELEASE)
# Integration: Splits Logic into Services & Gen modules

import streamlit as st
import lc_services as lcs  # Backend
import lc_gen as lcg       # Generation
import dm_data as dm       # Data
import dm_core as core     # Core Logic
import dm_ui as ui_module  # UI Strings
import random
from datetime import datetime

st.set_page_config(page_title="Lai's Lab AI", page_icon="🧬", layout="wide")

# CSS Styling
st.markdown("""
<style>
    .footer-container { position: fixed; bottom: 0; left: 0; width: 100%; background: white; border-top: 1px solid #eee; padding: 10px 0; z-index: 1000; text-align: center; }
    .price-strike { text-decoration: line-through; color: #999; }
    .price-promo { color: #d32f2f; font-weight: 800; }
    .stProgress > div > div > div > div { background-color: #0277bd !important; }
</style>
""", unsafe_allow_html=True)

# Session State
defaults = {
    'logged_in': False, 'user_tier': 'Guest', 'user_email': '', 
    'daily_usage': 0, 'language': 'English', 'output_language': 'English',
    'has_result': False, 'generated_result': ''
}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# Load Secrets
if "general" in st.secrets:
    sec = st.secrets["general"]
    lcs.CONFIG.update({
        "EMAIL_SENDER_ADDRESS": sec.get("email_sender", ""),
        "EMAIL_APP_PASSWORD": sec.get("email_app_password", ""),
        "TELEGRAM_BOT_TOKEN": sec.get("telegram_token", ""),
        "TELEGRAM_CHAT_ID": sec.get("telegram_chat_id", ""),
        "LEMONSQUEEZY_API_KEY": sec.get("lemonsqueezy_key", ""),
        "AIRTABLE_API_KEY": sec.get("airtable_key", ""),
        "AIRTABLE_BASE_ID": sec.get("airtable_base_id", ""),
        "MASTER_KEY": sec.get("master_key", "LAI-ADMIN-8888")
    })

def render_footer():
    tier = st.session_state.user_tier
    st.markdown(f"""
        <div style="height: 100px;"></div>
        <div class="footer-container">
            <small>© 2026 LAI'S LAB • SYSTEM V9.33 • STATUS: <span style="color:green">● ONLINE</span></small><br>
            <small style="color:#666">Current License: <b>{tier}</b></small>
        </div>
    """, unsafe_allow_html=True)

def show_login_page():
    ui = ui_module.get_safe_ui(st.session_state.language)
    
    # Language Selector
    try: idx = dm.ALL_LANGUAGES.index(st.session_state.language)
    except: idx = 0
    new_lang = st.selectbox("🌍", dm.ALL_LANGUAGES, index=idx, label_visibility="collapsed")
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()

    st.title(f"🧬 {ui['sidebar_title']}")
    col1, col2 = st.columns([1, 1.5], gap="large")
    
    with col1:
        st.info("🚀 AI Automated Prompt Engineer")
        t1, t2 = st.tabs([ui['plan_guest'], ui['plan_pro']])
        
        with t1:
            e = st.text_input("Email", key="login_email", placeholder="you@example.com")
            if st.button(ui['generate'], use_container_width=True):
                if "@" in e:
                    st.session_state.user_email = e
                    st.session_state.user_tier = "Guest"
                    st.session_state.logged_in = True
                    st.rerun()
        
        with t2:
            st.markdown(f"🔥 **Pro:** <span class='price-strike'>$39.90</span> <span class='price-promo'>$12.90</span>", unsafe_allow_html=True)
            pe = st.text_input("Billing Email", key="pro_email")
            lk = st.text_input("License Key", type="password")
            if st.button("💎 Activate Pro", type="primary", use_container_width=True):
                with st.spinner("Verifying..."):
                    tier, msg = lcs.check_user_tier(pe, lk)
                    if tier == "Pro":
                        st.session_state.user_email = pe
                        st.session_state.user_tier = "Pro"
                        st.session_state.logged_in = True
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

    with col2:
        st.markdown(f"### {ui['tbl_head'][0]}")
        head, rows = dm.get_table_data(st.session_state.language)
        # Table Rendering
        st.markdown(f"""
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background:#f0f2f6; border-bottom:2px solid #ddd;">
                <th style="padding:8px;">Feature</th>
                <th style="padding:8px;">Guest</th>
                <th style="padding:8px; color:#d32f2f;">Pro</th>
            </tr>
            {''.join([f'<tr><td style="padding:8px; border-bottom:1px solid #eee;">{r["k"]}</td><td style="padding:8px; border-bottom:1px solid #eee;">{r["v1"]}</td><td style="padding:8px; border-bottom:1px solid #eee; font-weight:bold;">{r["v2"]}</td></tr>' for r in rows])}
        </table>
        """, unsafe_allow_html=True)

    render_footer()

def show_main_app():
    ui = ui_module.get_safe_ui(st.session_state.language)
    
    # Sidebar
    with st.sidebar:
        st.title(f"🧬 {ui['sidebar_title']}")
        st.caption(f"👤 {st.session_state.user_email}")
        
        # [NEW] Buy Button for Guests
        if st.session_state.user_tier == "Guest":
            st.link_button(ui['buy_btn'], "https://laislab.lemonsqueezy.com/buy", type="primary", use_container_width=True)
            st.markdown("---")

        # Usage Bar
        can_gen, rem, tot = lcg.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        st.progress(st.session_state.daily_usage / tot)
        st.caption(f"{ui['usage']}: {st.session_state.daily_usage} / {tot}")
        st.divider()
        
        # Settings
        try: idx = dm.ALL_LANGUAGES.index(st.session_state.language)
        except: idx = 0
        new_lang = st.selectbox(ui['lang'], dm.ALL_LANGUAGES, index=idx, key="main_lang")
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.rerun()

        # Support Section
        with st.expander(ui['faq_title']):
            st.markdown(f"**{ui['quick_ans']}**")
            qs = [i["q"] for i in dm.FAQ_DATABASE.get(st.session_state.language, dm.FAQ_DATABASE["English"])]
            q_sel = st.selectbox(ui['sel_topic'], qs)
            for i in dm.FAQ_DATABASE.get(st.session_state.language, dm.FAQ_DATABASE["English"]):
                if i["q"] == q_sel: st.info(i["a"])
            
            st.divider()
            st.markdown(f"**{ui['submit_ticket']}**")
            t_type = st.selectbox(ui['type_lbl'], dm.get_ticket_types(st.session_state.language))
            t_msg = st.text_input(ui['issue_lbl'])
            
            # Smart Intercept Visual
            if t_msg:
                hit, ans = lcg.smart_intercept(t_msg, st.session_state.language)
                if hit: st.warning(f"💡 AI Suggestion: {ans}")
            
            if st.button(ui['send_btn'], use_container_width=True):
                if t_msg:
                    lcs.log_ticket_to_airtable(st.session_state.user_email, t_type, t_msg, st.session_state.user_tier)
                    st.success("Ticket Sent!")

        if st.button(ui['logout'], use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # Main Area
    role = st.selectbox(ui['role'], list(core.ROLES_CONFIG.keys()))
    
    # Mode with Lock Visual
    modes = list(core.ROLES_CONFIG[role].keys())
    mode_opts = [f"🔒 {m}" if lcg.check_mode_lock(st.session_state.user_tier, m) else m for m in modes]
    mode_sel_display = st.selectbox(ui['mode'], mode_opts)
    mode = mode_sel_display.replace("🔒 ", "")
    
    # Options
    opt_labels = [o["label"] for o in core.ROLES_CONFIG[role][mode]]
    opt = st.selectbox(ui['action'], opt_labels)
    
    c1, c2 = st.columns(2)
    with c1: 
        try: o_idx = dm.ALL_LANGUAGES.index(st.session_state.output_language)
        except: o_idx = 0
        out_lang = st.selectbox(ui['out_lang_lbl'], dm.ALL_LANGUAGES, index=o_idx)
        st.session_state.output_language = out_lang
    with c2: 
        tone = st.selectbox(ui['tone_lbl'], core.ROLE_TONES.get(role, core.DEFAULT_TONES))
        
    inp = st.text_area(ui['input_label'], height=120)
    
    if st.button(ui['generate'], type="primary", use_container_width=True):
        # Hard Lock Check
        if lcg.check_mode_lock(st.session_state.user_tier, mode):
            st.error(ui['lock_msg'])
            st.link_button(ui['buy_btn'], "https://laislab.lemonsqueezy.com/buy")
        elif not can_gen:
            st.error("Daily Limit Reached.")
        elif inp:
            st.session_state.daily_usage += 1
            res = lcg.generate_pasec_prompt(role, mode, opt, inp, st.session_state.user_tier, out_lang, tone)
            st.session_state.generated_result = res
            st.session_state.has_result = True
            
    # Result Area (Black Tech Layers)
    if st.session_state.has_result:
        res = st.session_state.generated_result
        st.markdown(f"### {ui['result']}")
        
        st.caption(ui['ad_copy'])
        st.code(res, language="text")
        
        st.caption(ui['ad_connect'])
        c1, c2, c3, c4 = st.columns(4)
        c1.link_button("ChatGPT", "https://chat.openai.com", use_container_width=True)
        c2.link_button("Gemini", "https://gemini.google.com", use_container_width=True)
        c3.link_button("Claude", "https://claude.ai", use_container_width=True)
        c4.link_button("Perplexity", "https://www.perplexity.ai", use_container_width=True)
        
        st.caption(ui['ad_social'])
        links = lcg.get_social_links(res)
        s1, s2, s3 = st.columns(3)
        s1.link_button("WhatsApp", links['WhatsApp'], use_container_width=True)
        s2.link_button("Telegram", links['Telegram'], use_container_width=True)
        s3.link_button("Email", links['Email'], use_container_width=True)
        
        st.caption(ui['ad_download'])
        d1, d2, d3 = st.columns(3)
        d1.download_button("📄 TXT", res, "prompt.txt", use_container_width=True)
        
        # PDF/CSV Logic
        if st.session_state.user_tier == "Pro":
            pdf_bytes = lcg.create_pdf(res, role, mode)
            if pdf_bytes: d2.download_button("📕 PDF", pdf_bytes, "report.pdf", "application/pdf", use_container_width=True)
            
            csv_bytes = lcg.create_csv(res)
            d3.download_button("📊 CSV", csv_bytes, "data.csv", "text/csv", use_container_width=True)
        else:
            d2.button(ui['ad_locked'], disabled=True, use_container_width=True)
            d3.button(ui['ad_locked'], disabled=True, use_container_width=True)

    render_footer()

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
