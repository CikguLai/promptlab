# app.py (V9.28 - Global 15 & Clean Layout)
import streamlit as st
import logic_core as lc
import data_matrix as dm
import time, os
import random
from datetime import datetime

st.set_page_config(page_title="Lai's Lab AI", layout="wide")

# 全量 CSS 保持页面美观
st.markdown("""
<style>
    .compare-table { width: 100%; border-collapse: collapse; border: 1px solid #eee; background: white; font-size: 14px; }
    .compare-table th { background: #f8f9fa; padding: 12px; border-bottom: 2px solid #ddd; }
    .compare-table td { padding: 10px; border-bottom: 1px solid #eee; }
    .pro-column { background: #f0f7ff; color: #0277bd; font-weight: bold; }
    /* 这里的 footer-box 样式保留，但在 render_footer 中我们会用更高级的固定定位 */
</style>
""", unsafe_allow_html=True)

# Session 初始化
for key, val in {'logged_in': False, 'user_tier': 'Guest', 'user_email': '', 'daily_usage': 0, 'language': 'English'}.items():
    if key not in st.session_state: st.session_state[key] = val

def render_footer():
    """新增加：大厂级三段式法律页脚"""
    current_hour = datetime.now().hour
    online_count = 150 + (current_hour * 8) + random.randint(1, 15)
    
    is_pro = st.session_state.user_tier == "Pro"
    tier_label = "💎 VERIFIED PRO ACCESS" if is_pro else "👤 STANDARD GUEST TRIAL"
    tier_color = "#0277bd" if is_pro else "#666"

    st.markdown(f"""
        <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: white; border-top: 1px solid #f1f1f1; padding: 25px 40px; z-index: 1000; font-family: 'Inter', -apple-system, sans-serif;">
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 600; color: #111; margin-bottom: 15px; letter-spacing: 0.5px;">
                <div style="flex: 1; text-align: left;">© 2025–2026 LAI'S LAB</div>
                <div style="flex: 1; text-align: center; color: #999;">SYSTEM V9.28 PRO AUDIT VERSION</div>
                <div style="flex: 1; text-align: right; color: {tier_color};">{tier_label}</div>
            </div>
            <div style="margin-bottom: 15px; text-align: center;">
                <p style="font-size: 11px; color: #888; margin: 0; line-height: 1.6; max-width: 900px; margin: 0 auto; font-style: italic;">
                    <b>Disclaimer:</b> Generative content on Lai's Lab is subject to our terms. AI can make mistakes. 
                    Users are solely responsible for reviewing and validating the output before use. 
                    Lai's Lab assumes no liability for actions taken based on these generated outputs.
                </p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #aaa; border-top: 1px solid #fafafa; padding-top: 10px;">
                <div style="flex: 1; text-align: left;">
                    <b>Logged as:</b> {st.session_state.user_email} &nbsp; • &nbsp; 
                    <span style="color: #28a745;">🟢 All Systems Operational</span> &nbsp; • &nbsp; 
                    <b>Live:</b> {online_count}
                </div>
                <div style="flex: 1; text-align: right;">
                    <a href="#" style="color: #aaa; text-decoration: none;">Privacy Policy</a> &nbsp; | &nbsp; 
                    <a href="#" style="color: #aaa; text-decoration: none;">Terms of Service</a> &nbsp; | &nbsp; 
                    <a href="https://app.lemonsqueezy.com/my-orders" target="_blank" style="color: #0277bd; text-decoration: none; font-weight: 700;">Retrieve License (LemonSqueezy Verify)</a>
                </div>
            </div>
        </div>
        <div style="height: 160px;"></div> 
    """, unsafe_allow_html=True)

def show_login_page():
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
        # --- 1. 顶部身份标识 ---
        tier_icon = "💎" if st.session_state.user_tier == "Pro" else "👤"
        st.caption(f"{tier_icon} {ui['plan_pro'] if st.session_state.user_tier == 'Pro' else ui['plan_guest']}")
        
        # --- 2. 动态颜色进度条黑科技 ---
        can_gen, rem, tot = lc.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        bar_color = "#ff4b4b" if (tot - st.session_state.daily_usage) <= 1 else "#00f2fe"
        st.markdown(f"""<style>.stProgress > div > div > div > div {{ background-image: linear-gradient(to right, {bar_color} 0%, {bar_color} 100%); }}</style>""", unsafe_allow_html=True)
        
        st.progress(st.session_state.daily_usage / tot)
        
        if st.session_state.user_tier == "Pro":
            st.caption(f"✨ {ui.get('plan_pro', 'Pro Plan')}: Unlimited Experience")
        else:
            st.caption(f"📊 {ui['usage']}: {st.session_state.daily_usage} / {tot}")
        
        st.divider()
        langs = dm.LANG_OPTIONS_PRO if st.session_state.user_tier == "Pro" else dm.LANG_OPTIONS_GUEST
        st.session_state.language = st.selectbox("Language", langs, index=langs.index(st.session_state.language) if st.session_state.language in langs else 0)
        role = st.selectbox(ui['role'], list(dm.ROLES_CONFIG.keys()))
        if st.button(ui['logout'], use_container_width=True): st.session_state.clear(); st.rerun()

    # --- 3. 主界面标题与动态统计 ---
    st.header(f"🎭 {role}")
    
    current_hour = datetime.now().hour
    base_users = 100 + (current_hour * 2) 
    dynamic_count = base_users + random.randint(1, 15)

    st.markdown(f"""
        <div style="background: #fff9e6; border-left: 5px solid #ffcc00; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
            <span style="font-size: 14px; color: #856404;">
                🔥 <b>{ui.get('live_stat', 'Live Status')}:</b> 
                {dynamic_count} {'Pro Users generated successfully today' if st.session_state.language == 'English' else '位 Pro 用户今日生成成功'}
            </span>
        </div>
        """, unsafe_allow_html=True)

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
                    wa_url = lc.get_whatsapp_link(res)
                    st.link_button("🟢 WhatsApp Share", wa_url, use_container_width=True)
                with c2:
                    if st.session_state.user_tier == "Pro":
                        pdf = lc.create_pdf(res, role, mode)
                        if pdf: st.download_button("📕 Download PDF", pdf, "report.pdf", "application/pdf", use_container_width=True)
    
    # 渲染最终页脚
    render_footer()

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
