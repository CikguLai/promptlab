# app.py
# Lai's Lab V9.21 - 界面核心 (Reply-To Config)

import streamlit as st
import time
import base64
import os
from fpdf import FPDF 

import logic_core as lc 
import data_matrix as dm

st.set_page_config(page_title="Lai's Lab AI", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    div[data-testid="stDecoration"] {visibility: hidden; height: 0px;}
    .block-container {padding-top: 1rem !important; padding-bottom: 5rem;}
    .promo-box {background-color: #fff0f0; border: 1px solid #ffcdd2; color: #d32f2f; padding: 10px; border-radius: 8px; margin-bottom: 20px;}
    .promo-price {font-weight: bold; font-size: 18px; color: #e53935;}
    .promo-old {text-decoration: line-through; color: #9e9e9e; font-size: 13px;}
    a {text-decoration: none !important; color: #666;} a:hover {text-decoration: underline !important; color: #333;}
    .lost-key-link {text-align: center; margin-top: 10px; font-size: 12px; color: #888;}
</style>
""", unsafe_allow_html=True)

# 🔐 Secrets 注入 (含 Reply-To)
if "general" in st.secrets:
    s = st.secrets["general"]
    # 邮件
    if "email_app_password" in s: lc.CONFIG["EMAIL_APP_PASSWORD"] = s["email_app_password"]
    if "email_sender" in s: lc.CONFIG["EMAIL_SENDER_ADDRESS"] = s["email_sender"]
    if "email_admin" in s: lc.CONFIG["EMAIL_ADMIN_ADDRESS"] = s["email_admin"]
    # ✅ 新增：读取 Reply-To
    if "email_reply_to" in s: lc.CONFIG["EMAIL_REPLY_TO"] = s["email_reply_to"]
    
    # 支付与验证
    if "lemonsqueezy_key" in s: lc.CONFIG["LEMONSQUEEZY_API_KEY"] = s["lemonsqueezy_key"]
    if "master_key" in s: lc.CONFIG["MASTER_KEY"] = s["master_key"]
    # Airtable
    if "airtable_key" in s: lc.CONFIG["AIRTABLE_API_KEY"] = s["airtable_key"]
    if "airtable_base_id" in s: lc.CONFIG["AIRTABLE_BASE_ID"] = s["airtable_base_id"]
    if "airtable_table_tickets" in s: lc.CONFIG["AIRTABLE_TABLE_TICKETS"] = s["airtable_table_tickets"]
    if "airtable_table_users" in s: lc.CONFIG["AIRTABLE_TABLE_USERS"] = s["airtable_table_users"]

# Session
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_tier' not in st.session_state: st.session_state.user_tier = "Guest"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'language' not in st.session_state: st.session_state.language = "English"
if 'daily_usage' not in st.session_state: st.session_state.daily_usage = 0

# 辅助函数
def render_download_button(text):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="prompt.txt" style="background:#f0f2f6; padding:8px; border-radius:5px; color:#333; font-size:14px;">📄 Download Prompt</a>'
    st.markdown(href, unsafe_allow_html=True)

def create_pdf(content, role, mode):
    pdf = FPDF(); pdf.add_page(); pdf.set_auto_page_break(auto=True, margin=15)
    font_path = "font.ttf"
    if os.path.exists(font_path): pdf.add_font('CustomFont', '', font_path, uni=True); pdf.set_font("CustomFont", size=12)
    else: pdf.set_font("Arial", size=12); content = content.encode('latin-1', 'replace').decode('latin-1')
    pdf.set_font_size(16); pdf.cell(0, 10, txt=f"Lai's Lab - {role}/{mode}", ln=True, align='C'); pdf.ln(10)
    pdf.set_font_size(12); pdf.multi_cell(0, 10, txt=content)
    return pdf.output(dest="S").encode("latin-1")

def render_footer():
    st.markdown("---")
    st.markdown('<div style="text-align: center; font-size: 12px; color: #666;">© 2025 <b>Lai\'s Lab</b> | System V9.21 Enterprise</div>', unsafe_allow_html=True)

def logout(): st.session_state.clear(); st.rerun()

# 登录页
def show_login_page():
    c1, c2 = st.columns([1, 1.3])
    with c1:
        if os.path.exists("logo.png"): st.image("logo.png", width=120)
        else: st.markdown("## 🧬 Lai's Lab")
        st.title("PromptLab AI V9.21"); st.caption("Enterprise Prompt Engine"); st.markdown("---")
        st.markdown('<div class="promo-box"><span>🔥 Lifetime Pro:</span> <span class="promo-price">$12.90</span> <span class="promo-old">$39.90</span></div>', unsafe_allow_html=True)
        
        t1, t2 = st.tabs(["👤 Guest Trial", "💎 Activate Pro"])
        with t1:
            email = st.text_input("Email", placeholder="you@example.com")
            if st.button("🚀 Start Free Trial", use_container_width=True):
                if "@" in email: st.session_state.user_email = email; st.session_state.user_tier = "Guest"; st.session_state.logged_in = True; st.rerun()
                else: st.warning("Invalid Email")
        with t2:
            p_email = st.text_input("Pro Email")
            l_key = st.text_input("License Key", type="password")
            if st.button("💎 Activate", type="primary", use_container_width=True):
                with st.spinner("Verifying License..."):
                    status = lc.check_user_tier(p_email, l_key)
                    if status == "Pro": st.session_state.user_email = p_email; st.session_state.user_tier = "Pro"; st.session_state.logged_in = True; st.balloons(); time.sleep(1); st.rerun()
                    else: st.error("❌ Invalid License Key")
            st.markdown('<div class="lost-key-link"><a href="https://app.lemonsqueezy.com/my-orders" target="_blank">🔒 Lost License Key?</a></div>', unsafe_allow_html=True)
    with c2:
        st.info("💡 Join 10,000+ Educators & Creators today.")
    render_footer()

# 主程序
def show_main_app():
    curr = st.session_state.language
    ui = dm.LANG_MAP.get(curr, dm.LANG_MAP["default"])
    
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png", width=80)
        st.caption(f"💎 {ui['plan_pro']}" if st.session_state.user_tier == "Pro" else f"👤 {ui['plan_guest']}")
        
        _, _, max_limit = lc.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        st.progress(min(st.session_state.daily_usage / max_limit if max_limit > 0 else 0, 1.0))
        st.caption(f"{ui['usage']}: {st.session_state.daily_usage}/{max_limit}")
        st.divider()
        
        langs = dm.LANG_OPTIONS_PRO if st.session_state.user_tier == "Pro" else dm.LANG_OPTIONS_GUEST
        sel_l = st.selectbox(ui['lang'], langs, index=langs.index(curr) if curr in langs else 0)
        if sel_l != curr: st.session_state.language = sel_l; st.rerun()
        
        role = st.selectbox(ui['role'], list(dm.ROLES_CONFIG.keys()))
        
        with st.expander(ui['support']):
            tt = st.selectbox("Type", ui['ticket_types'])
            ts = st.text_input("Subject")
            tm = st.text_area("Msg")
            if st.button("Submit"):
                intercept, msg = lc.smart_intercept(ts)
                if intercept: st.warning(msg)
                else:
                    tid = int(time.time())
                    lc.log_ticket_to_airtable(tid, st.session_state.user_email, st.session_state.user_tier, f"[{tt}] {ts}")
                    lc.send_auto_reply_email(st.session_state.user_email, st.session_state.user_tier, tid, ts)
                    st.success("✅ Ticket Sent!")
        st.divider(); 
        if st.button(ui['logout']): logout()

    st.header(f"{role} Workspace")
    modes = list(dm.ROLES_CONFIG[role].keys())
    mode = st.selectbox(ui['mode'], modes)
    
    if lc.check_mode_lock(st.session_state.user_tier, mode):
        st.error(ui['lock_msg']); st.link_button(ui['buy_btn'], "https://laislab.lemonsqueezy.com/buy", type="primary")
    else:
        opts = [o["label"] for o in dm.ROLES_CONFIG[role][mode]]
        opt = st.selectbox(ui['action'], opts)
        
        tones = dm.ROLE_TONES.get(role, dm.DEFAULT_TONES)
        tone = st.selectbox(ui.get('tone', "Tone"), tones)
        
        inp = st.text_area(ui['input_label'], height=150)
        
        if st.button(ui['generate'], type="primary", use_container_width=True):
            if not inp: st.warning("Empty input")
            elif st.session_state.daily_usage >= max_limit: st.error("Limit Reached")
            else:
                st.session_state.daily_usage += 1
                if st.session_state.user_tier == "Guest": time.sleep(1.5)
                
                final_res = lc.generate_pasec_prompt(role, mode, opt, inp, st.session_state.user_tier, st.session_state.language, tone)
                
                st.markdown(f"### {ui['result']}")
                st.text_area("Copy this prompt:", value=final_res, height=450)
                
                c1, c2, c3 = st.columns(3)
                with c1: render_download_button(final_res)
                with c2: st.link_button("🎨 Midjourney", "https://www.midjourney.com")
                with c3: st.link_button("💬 ChatGPT", "https://chat.openai.com")
                
                if st.session_state.user_tier == "Pro":
                    st.divider()
                    pdf = create_pdf(final_res, role, mode)
                    st.download_button("📕 Download PDF", pdf, "prompt.pdf", "application/pdf")

    render_footer()

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
