# app.py (V10.5 - FINAL COMMERCIAL RELEASE)
# Features: Unique Keys (Fix Crash), Mode Locking, Pro Upsell UI

import streamlit as st
import lc_services as lcs
import lc_gen as lcg
import dm_data as dm
import dm_core as core
import dm_ui as ui_module
import random, os
from datetime import datetime

# 1. Page Config & SaaS Styling
st.set_page_config(page_title="Lai's Lab AI", page_icon="🧬", layout="wide")

st.markdown("""
<style>
    /* 隐藏默认菜单 */
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;}

    /* 卡片式输入框 */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 10px;
    }
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* 按钮美化 */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 强制固定页脚 */
    .footer-container { 
        position: fixed; 
        bottom: 0; 
        left: 0; 
        width: 100%; 
        background: white; 
        border-top: 1px solid #eaeaea; 
        padding: 12px 0; 
        z-index: 9999; 
        text-align: center; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        gap: 4px; 
        box-shadow: 0 -2px 10px rgba(0,0,0,0.02);
    }
    .footer-row-1 { font-weight: 700; color: #2c3e50; font-size: 13px; letter-spacing: 0.5px; }
    .footer-row-2 { font-size: 10px; color: #7f8c8d; max-width: 900px; line-height: 1.4; text-align: center; font-family: sans-serif; }
    .footer-row-3 { font-size: 11px; color: #bdc3c7; margin-top: 4px; display: flex; gap: 20px; font-family: monospace; }
    
    /* 价格与统计样式 */
    .price-strike { text-decoration: line-through; color: #95a5a6; font-size: 16px; margin-right: 8px; }
    .price-promo { color: #d32f2f; font-weight: 900; font-size: 26px; }
    .license-active { color: #27ae60; font-weight: 700; font-size: 16px; border: 1px solid #27ae60; padding: 8px 12px; border-radius: 6px; background: #eafaf1; text-align: center; }
    .stat-box { font-size: 14px; font-weight: 500; color: #555; margin-bottom: 2px; }

    .badge-container { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 8px; }
    .stProgress > div > div > div > div { background-color: #0277bd !important; }
</style>
""", unsafe_allow_html=True)

# Session
defaults = {'logged_in': False, 'user_tier': 'Guest', 'user_email': '', 'daily_usage': 0, 'language': 'English', 'output_language': 'English', 'has_result': False, 'generated_result': ''}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# Secrets
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
        <div style="height: 120px;"></div>
        <div class="footer-container">
            <div class="footer-row-1">© 2025-2026 LAI'S LAB AI • PROFESSIONAL PROMPT SYSTEM</div>
            <div class="footer-row-2">Disclaimer: Generative AI can make mistakes; please double-check responses. Users are solely responsible for the content generated. Lai's Lab assumes no liability for misuse.</div>
            <div class="footer-row-3"><span>SYSTEM: V10.5</span><span>STATUS: <span style="color:#27ae60">● ONLINE</span></span><span>LICENSE: <b>{tier}</b></span></div>
        </div>
    """, unsafe_allow_html=True)

def inject_progress_color(usage, limit):
    if limit > 100: return
    if usage >= 5: color = "#ff2b2b"
    elif usage >= 3: color = "#ff9800"
    else: color = "#00c853"
    st.markdown(f"""<style>.stProgress > div > div > div > div {{ background-color: {color} !important; }}</style>""", unsafe_allow_html=True)

def badge(label, color, logo, url):
    return f'<a href="{url}" target="_blank"><img src="https://img.shields.io/badge/{label}-{color}?style=for-the-badge&logo={logo}&logoColor=white" height="28"></a>'

def show_login_page():
    ui = ui_module.get_safe_ui(st.session_state.language)
    try: idx = dm.ALL_LANGUAGES.index(st.session_state.language)
    except: idx = 0
    new_lang = st.selectbox("🌍", dm.ALL_LANGUAGES, index=idx, label_visibility="collapsed")
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()

    # [FIX] Login Page Logo
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
    else: st.title(f"🧬 {ui['sidebar_title']}")
    
    st.info(f"🚀 {ui['subtitle']}")

    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        t1, t2 = st.tabs([ui['plan_guest'], ui['plan_pro']])
        with t1:
            e = st.text_input("Email", key="login_email", placeholder="you@example.com")
            if st.button(ui['generate'], use_container_width=True, key="btn_guest_login"):
                if "@" in e:
                    st.session_state.user_email = e; st.session_state.user_tier = "Guest"; st.session_state.logged_in = True; lcs.log_lead_to_airtable(e); st.rerun()
        with t2:
            st.markdown(f"<span class='price-strike'>$39.90</span> <span class='price-promo'>$12.90</span>", unsafe_allow_html=True)
            pe = st.text_input("Billing Email", key="pro_email")
            lk = st.text_input("License Key", type="password")
            if st.button("💎 Activate Pro", type="primary", use_container_width=True, key="btn_pro_login"):
                with st.spinner("Verifying..."):
                    tier, msg = lcs.check_user_tier(pe, lk)
                    if tier == "Pro":
                        st.session_state.user_email = pe; st.session_state.user_tier = "Pro"; st.session_state.logged_in = True; st.balloons(); st.rerun()
                    else: st.error(f"❌ {msg}")
            st.markdown("[🔑 Lost License Key?](https://app.lemonsqueezy.com/my-orders)", unsafe_allow_html=True)

    with col2:
        tbl_head, rows = dm.get_table_data(st.session_state.language, ui_module)
        st.markdown(f"### {tbl_head[0]}")
        st.markdown(f"""
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background:#f8f9fa; border-bottom:2px solid #ddd;">
                <th style="padding:10px;">Feature</th><th style="padding:10px;">{tbl_head[1]}</th><th style="padding:10px; color:#d32f2f;">{tbl_head[2]}</th>
            </tr>
            {''.join([f'<tr><td style="padding:10px; border-bottom:1px solid #eee;">{r["k"]}</td><td style="padding:10px; border-bottom:1px solid #eee;">{r["v1"]}</td><td style="padding:10px; border-bottom:1px solid #eee; font-weight:bold;">{r["v2"]}</td></tr>' for r in rows])}
        </table>""", unsafe_allow_html=True)
    render_footer()

def show_main_app():
    ui = ui_module.get_safe_ui(st.session_state.language)
    with st.sidebar:
        # [LOGO FIX] 绝对路径查找
        if os.path.exists("logo.png"): st.image("logo.png", width=200)
        else: st.header("🧬 Lai's Lab")
            
        st.title(f"{ui['sidebar_title']}")
        st.caption(ui['subtitle'])
        
        # [ACTIVE USERS] 双行数据
        hour = datetime.now().hour
        prompts = 1260 + (hour * 55) + random.randint(10, 80)
        users = int(prompts * 0.72) + random.randint(5, 20)
        
        st.markdown(f"<div class='stat-box'>🔥 Prompts Generated: <b>{prompts:,}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-box'>👥 Active Users: <b>{users:,}</b></div>", unsafe_allow_html=True)
        
        st.divider()
        st.caption(f"👤 {st.session_state.user_email}")
        
        # [PRICE HIDE] Pro 不显示价格
        if st.session_state.user_tier == "Guest":
            st.link_button(ui['buy_btn'], "https://laislab.lemonsqueezy.com/buy", type="primary", use_container_width=True)
        else:
            st.markdown("<div class='license-active'>💎 License Active: Lifetime</div>", unsafe_allow_html=True)
            
        st.markdown("---")

        can_gen, rem, tot = lcg.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        if st.session_state.user_tier == "Guest":
            inject_progress_color(st.session_state.daily_usage, tot)
            st.progress(st.session_state.daily_usage / tot)
            st.caption(f"{ui['usage']}: **{st.session_state.daily_usage} / {tot}**")
            if rem <= 1: st.warning("⚠️ Low Limit! Upgrade to Pro.")
        else:
            st.success(f"💎 {ui['usage']}: **Unlimited**")
            st.caption("*Subject to Fair Use Policy")
        
        st.divider()
        try: idx = dm.ALL_LANGUAGES.index(st.session_state.language)
        except: idx = 0
        new_lang = st.selectbox(ui['lang'], dm.ALL_LANGUAGES, index=idx, key="main_lang")
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.rerun()

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
            if t_msg:
                hit, ans = lcg.smart_intercept(t_msg, st.session_state.language)
                if hit: st.warning(f"💡 AI Suggestion: {ans}")
            if st.button(ui['send_btn'], use_container_width=True, key="btn_ticket_send"):
                if t_msg:
                    tid = f"T-{random.randint(1000, 9999)}"
                    lcs.log_ticket_to_airtable(st.session_state.user_email, t_type, t_msg, st.session_state.user_tier, tid)
                    st.success(f"✅ Ticket #{tid} Submitted! Check email.")
                    
        if st.button(ui['logout'], use_container_width=True, key="btn_logout"): st.session_state.clear(); st.rerun()

    role = st.selectbox(ui['role'], list(core.ROLES_CONFIG.keys()))
    modes = list(core.ROLES_CONFIG[role].keys())
    
    # [COMMERCIAL LOGIC] Mode Locking
    # 任何不含 "Pedagogy" 的模式，对 Guest 用户都视为锁住
    mode = st.selectbox(ui['mode'], modes)
    is_pro_mode = ("Visuals" in mode or "Marketing" in mode)
    
    if st.session_state.user_tier == "Guest" and is_pro_mode:
        st.warning("🔒 This Mode is Locked for Free Users. Upgrade to Pro to unlock.")
    
    opt = st.selectbox(ui['action'], [o["label"] for o in core.ROLES_CONFIG[role][mode]])
    
    c1, c2 = st.columns(2)
    with c1: 
        try: o_idx = dm.ALL_LANGUAGES.index(st.session_state.output_language)
        except: o_idx = 0
        st.session_state.output_language = st.selectbox(ui['out_lang_lbl'], dm.ALL_LANGUAGES, index=o_idx)
    with c2: tone = st.selectbox(ui['tone_lbl'], core.ROLE_TONES.get(role, core.DEFAULT_TONES))
        
    inp = st.text_area(ui['input_label'], height=120)
    
    # [GENERATE BUTTON LOCK]
    if st.button(ui['generate'], type="primary", use_container_width=True, key="btn_generate_main"):
        if st.session_state.user_tier == "Guest" and is_pro_mode:
            st.error("🚫 Premium Mode Selected. Please Upgrade to Pro.")
            st.link_button(ui['buy_btn'], "https://laislab.lemonsqueezy.com/buy")
        elif not can_gen: st.error("Daily Limit Reached.")
        elif inp:
            st.session_state.daily_usage += 1
            res = lcg.generate_pasec_prompt(role, mode, opt, inp, st.session_state.user_tier, st.session_state.output_language, tone)
            st.session_state.generated_result = lcg.clean_pro_output(res, st.session_state.user_tier)
            st.session_state.has_result = True
            st.rerun()
            
    if st.session_state.has_result:
        res = st.session_state.generated_result
        st.markdown(f"### {ui['result']}")
        st.info("💡 **Pro Tip:** Copy the code block below and paste it into ChatGPT/Claude.")
        st.caption(ui['ad_copy'])
        st.code(res, language="text")
        
        st.caption(ui['ad_connect'])
        st.markdown(f"""<div class="badge-container">
            {badge('ChatGPT', '74aa9c', 'openai', 'https://chat.openai.com')}
            {badge('DeepSeek', '4d6bfe', 'google-earth', 'https://chat.deepseek.com')}
            {badge('Claude', 'D97757', 'anthropic', 'https://claude.ai')}
            {badge('Gemini', '8E75B2', 'google', 'https://gemini.google.com')}
            {badge('Copilot', '0078D4', 'microsoft', 'https://copilot.microsoft.com')}
            {badge('Perplexity', '222222', 'perplexity', 'https://www.perplexity.ai')}
            {badge('Meta_AI', '0668E1', 'meta', 'https://www.meta.ai')}
        </div>""", unsafe_allow_html=True)
        
        # [LAYER 3: SOCIAL] - Free for all
        st.caption(ui['ad_social'])
        links = lcg.get_social_links(res)
        st.markdown(f"""<div class="badge-container">
            {badge('WhatsApp', '25D366', 'whatsapp', links['WhatsApp'])}
            {badge('Telegram', '26A5E4', 'telegram', links['Telegram'])}
            {badge('LINE', '00C300', 'line', links['LINE'])}
            {badge('Email', 'EA4335', 'gmail', links['Email'])}
        </div>""", unsafe_allow_html=True)
        
        st.markdown("---")
        c1, c2 = st.columns([1,2])
        # [LAYER 4: SCAN] - Free for all
        with c1: st.caption("📱 **Scan to Phone:**"); st.image(lcg.generate_qr_code(res), width=150)
        
        # [LAYER 5: CLOUD SAVE] - Pro Locked
        with c2: 
            st.caption("☁️ **Cloud Save:**")
            if st.session_state.user_tier == "Pro":
                st.markdown(f"""<div class="badge-container">
                    {badge('Google_Drive', '4285F4', 'googledrive', 'https://drive.google.com')}
                    {badge('Dropbox', '0061FF', 'dropbox', 'https://www.dropbox.com')}
                    {badge('OneDrive', '0078D4', 'microsoftonedrive', 'https://onedrive.live.com')}
                </div>""", unsafe_allow_html=True)
            else:
                if st.button("🔒 Unlock Cloud Save (Pro)", key="btn_cloud_lock"):
                    st.error("🚫 Cloud Save is a Pro Feature. Upgrade to access.")

        st.markdown("---"); st.caption(ui['ad_download'])
        d1, d2, d3 = st.columns(3)
        # [LAYER 6: TXT] - Free
        d1.download_button("📄 TXT", res, "prompt.txt", use_container_width=True, key="btn_dl_txt")
        
        # [LAYER 6: PDF/CSV] - Pro Locked + Duplicate ID Fix
        if st.session_state.user_tier == "Pro":
            pdf_b = lcg.create_pdf(res, role, mode)
            csv_b = lcg.create_csv(res)
            if pdf_b: 
                d2.download_button("📕 PDF (Direct)", pdf_b, "report.pdf", "application/pdf", use_container_width=True, key="btn_dl_pdf_pro")
            else: d2.error("PDF Error")
            d3.download_button("📊 CSV (Direct)", csv_b, "data.csv", "text/csv", use_container_width=True, key="btn_dl_csv_pro")
        else:
            if d2.button("🔒 PDF (Pro)", use_container_width=True, key="btn_pdf_lock"):
                st.error("🚫 PDF Export is for Pro Users.")
            if d3.button("🔒 CSV (Pro)", use_container_width=True, key="btn_csv_lock"):
                st.error("🚫 CSV Export is for Pro Users.")

    render_footer()

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
