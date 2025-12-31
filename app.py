# app.py (V9.28 - Dynamic Table & Perfect Footer)
import streamlit as st
import logic_core as lc
import data_matrix as dm
import time, os
import random
from datetime import datetime

# 1. 网页标签图标设为 DNA
st.set_page_config(page_title="Lai's Lab AI", page_icon="🧬", layout="wide")

# 全量 CSS：居中页脚、表格、Slogan
st.markdown("""
<style>
    .compare-table { width: 100%; border-collapse: collapse; border: 1px solid #eee; background: white; font-size: 13px; margin-top: 10px; }
    .compare-table th { background: #f8f9fa; padding: 12px; border-bottom: 2px solid #ddd; text-align: left; color: #333; }
    .compare-table td { padding: 10px; border-bottom: 1px solid #eee; vertical-align: middle; color: #555; }
    .pro-column { background: #f0f7ff; color: #0277bd; font-weight: bold; border-left: 1px solid #cce5ff; }
    .price-tag { color: #d32f2f; font-size: 1.1em; font-weight: 800; }
    a:hover { text-decoration: underline !important; }
    .app-slogan { font-size: 18px; color: #555; margin-top: -15px; margin-bottom: 25px; font-weight: 500; letter-spacing: 0.5px; }
    
    /* ✅ Footer 绝对居中修正 */
    .footer-container {
        position: fixed; bottom: 0; left: 0; width: 100%; 
        background-color: white; border-top: 1px solid #f1f1f1; 
        padding: 20px; z-index: 1000; text-align: center; /* 确保所有文本居中 */
        font-family: 'Inter', sans-serif;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .footer-row-1 { font-size: 12px; font-weight: 600; color: #333; margin-bottom: 8px; }
    .footer-row-2 { font-size: 10px; color: #999; margin-bottom: 8px; font-style: italic; max-width: 800px; line-height: 1.4; }
    .footer-row-3 { font-size: 11px; color: #aaa; }
    .footer-link { color: #aaa; text-decoration: none; margin: 0 5px; }
    .footer-verify { color: #0277bd; font-weight: 700; text-decoration: none; margin-left: 10px; }
</style>
""", unsafe_allow_html=True)

# Session 初始化
for key, val in {'logged_in': False, 'user_tier': 'Guest', 'user_email': '', 'daily_usage': 0, 'language': 'English'}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- Footer 渲染函数 (完美居中) ---
def render_footer():
    current_hour = datetime.now().hour
    online_count = 150 + (current_hour * 8) + random.randint(1, 15)
    is_pro = st.session_state.user_tier == "Pro"
    tier_label = "💎 VERIFIED PRO ACCESS" if is_pro else "👤 STANDARD GUEST TRIAL"
    tier_color = "#0277bd" if is_pro else "#666"

    st.markdown(f"""
        <div class="footer-container">
            <div class="footer-row-1">
                © 2025–2026 LAI'S LAB &nbsp; • &nbsp; 
                <span style="color: #999;">SYSTEM V9.28 PRO AUDIT</span> &nbsp; • &nbsp; 
                <span style="color: {tier_color};">{tier_label}</span>
            </div>
            <div class="footer-row-2">
                Disclaimer: Generative AI can make mistakes. Users are solely responsible for content usage. 
                Lai's Lab assumes no liability for actions taken based on these outputs.
            </div>
            <div class="footer-row-3">
                👤 {st.session_state.user_email} &nbsp;|&nbsp; 
                <span style="color: #28a745;">🟢 All Systems Operational</span> &nbsp;|&nbsp; 
                <b>Live:</b> {online_count} &nbsp;&nbsp;&nbsp;
                <a href="#" class="footer-link">Privacy</a> • 
                <a href="#" class="footer-link">Terms</a> • 
                <a href="https://app.lemonsqueezy.com/my-orders" target="_blank" class="footer-verify">LemonSqueezy Verify</a>
            </div>
        </div>
        <div style="height: 140px;"></div> 
    """, unsafe_allow_html=True)

def show_login_page():
    st.write("🌍 Select Your Language / 选择您的语言")
    # 强制 key 以同步刷新
    lang_sel = st.selectbox("", dm.LANG_OPTIONS_PRO, index=0, key="lang_select", label_visibility="collapsed")
    if st.session_state.language != lang_sel:
        st.session_state.language = lang_sel
        st.rerun()

    ui = dm.LANG_MAP.get(lang_sel, dm.LANG_MAP["default"])

    col1, col2 = st.columns([1, 1.4], gap="large")
    with col1:
        # DNA 标题与 Slogan (修复反斜杠语法错误)
        app_title = ui.get('sidebar_title', "Lai's Lab")
        st.title(f"🧬 {app_title}")
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
            st.markdown('<div style="text-align: center; margin-top: 15px;"><a href="https://app.lemonsqueezy.com/my-orders" target="_blank" style="color: #666; font-size: 13px; text-decoration: none;">🔒 Lost your key? Retrieve via LemonSqueezy</a></div>', unsafe_allow_html=True)

    with col2:
        # ✅ 动态生成表格：根据 ui 中的数据自动构建 HTML
        st.subheader("🆚 Compare Plans")
        
        # 获取表头和数据
        headers = ui.get('tbl_headers', ["Capability", "Guest Trial", "💎 PRO Lifetime"])
        rows = ui.get('tbl_data', [])
        
        # 构建表格 HTML
        table_html = '<table class="compare-table">'
        table_html += f'<tr><th>{headers[0]}</th><th>{headers[1]}</th><th class="pro-column">{headers[2]}</th></tr>'
        
        for r in rows:
            # 特殊处理价格行的颜色
            v2_display = f'<span class="price-tag">{r["v2"]}</span>' if "Price" in r['k'] or "价格" in r['k'] else r['v2']
            table_html += f'<tr><td><b>{r["k"]}</b></td><td>{r["v1"]}</td><td class="pro-column">{v2_display}</td></tr>'
            
        table_html += '</table>'
        
        st.markdown(table_html, unsafe_allow_html=True)
        
        note = "* 遵循公平使用原则。" if lang_sel == "简体中文" else "* Fair Use Policy applies."
        st.caption(note)
        
    render_footer()

def show_main_app():
    ui = dm.LANG_MAP.get(st.session_state.language, dm.LANG_MAP["default"])
    with st.sidebar:
        st.caption(f"{'💎' if st.session_state.user_tier == 'Pro' else '👤'} {ui['plan_pro'] if st.session_state.user_tier == 'Pro' else ui['plan_guest']}")
        # 进度条
        can_gen, rem, tot = lc.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        bar_color = "#ff4b4b" if (tot - st.session_state.daily_usage) <= 1 else "#00f2fe"
        st.markdown(f"<style>.stProgress > div > div > div > div {{ background-image: linear-gradient(to right, {bar_color} 0%, {bar_color} 100%); }}</style>", unsafe_allow_html=True)
        st.progress(st.session_state.daily_usage / tot)
        st.caption(f"📊 {ui['usage']}: {st.session_state.daily_usage} / {tot}" if st.session_state.user_tier != "Pro" else f"✨ {ui.get('plan_pro', 'Pro Plan')}: Unlimited")
        st.divider()
        
        # 语言切换
        lang_sel_main = st.selectbox("Language", dm.LANG_OPTIONS_PRO, index=dm.LANG_OPTIONS_PRO.index(st.session_state.language) if st.session_state.language in dm.LANG_OPTIONS_PRO else 0, key="lang_select_main")
        if st.session_state.language != lang_sel_main:
            st.session_state.language = lang_sel_main
            st.rerun()

        role = st.selectbox(ui['role'], list(dm.ROLES_CONFIG.keys()))
        if st.button(ui['logout'], use_container_width=True): st.session_state.clear(); st.rerun()

    st.header(f"🎭 {role}")
    dynamic_count = 100 + (datetime.now().hour * 2) + random.randint(1, 15)
    live_label = ui.get('live_stat', 'Live Status')
    st.markdown(f"""<div style="background: #fff9e6; border-left: 5px solid #ffcc00; padding: 10px; border-radius: 5px; margin-bottom: 15px;"><span style="font-size: 14px; color: #856404;">🔥 <b>{live_label}:</b> {dynamic_count} Users active today</span></div>""", unsafe_allow_html=True)

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
                res = lc.generate_pasec_prompt(role, mode, opt, inp, st.session_state.user_tier, st.session_state.language, tone)
                st.markdown(f"### {ui['result']}"); st.text_area("Payload:", value=res, height=300)
                
                # 分享功能
                c1, c2 = st.columns(2)
                with c1:
                    wa_url = lc.get_whatsapp_link(res)
                    st.link_button("🟢 WhatsApp Share", wa_url, use_container_width=True)
                with c2:
                    if st.session_state.user_tier == "Pro":
                        pdf = lc.create_pdf(res, role, mode)
                        if pdf: st.download_button("📕 Download PDF", pdf, "report.pdf", "application/pdf", use_container_width=True)

    render_footer()

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
