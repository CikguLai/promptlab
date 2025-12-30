# app.py (V9.28 - Global 15 & Lost Key Fixed)
import streamlit as st
import logic_core as lc
import data_matrix as dm
import time, os
import random
from datetime import datetime

st.set_page_config(page_title="Lai's Lab AI", layout="wide")

# 全量 CSS：优化表格与链接样式
st.markdown("""
<style>
    .compare-table { width: 100%; border-collapse: collapse; border: 1px solid #eee; background: white; font-size: 13px; }
    .compare-table th { background: #f8f9fa; padding: 10px; border-bottom: 2px solid #ddd; text-align: left; }
    .compare-table td { padding: 8px 10px; border-bottom: 1px solid #eee; vertical-align: middle; }
    .pro-column { background: #f0f7ff; color: #0277bd; font-weight: bold; border-left: 1px solid #cce5ff; }
    .price-tag { color: #d32f2f; font-size: 1.1em; font-weight: 800; }
    /* 修复链接悬停效果 */
    a:hover { text-decoration: underline !important; }
</style>
""", unsafe_allow_html=True)

# Session 初始化
for key, val in {'logged_in': False, 'user_tier': 'Guest', 'user_email': '', 'daily_usage': 0, 'language': 'English'}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 每一页都出现的 3 段式大厂 Footer ---
def render_footer():
    current_hour = datetime.now().hour
    online_count = 150 + (current_hour * 8) + random.randint(1, 15)
    is_pro = st.session_state.user_tier == "Pro"
    tier_label = "💎 VERIFIED PRO ACCESS" if is_pro else "👤 STANDARD GUEST TRIAL"
    tier_color = "#0277bd" if is_pro else "#666"

    st.markdown(f"""
        <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: white; border-top: 1px solid #f1f1f1; padding: 25px 40px; z-index: 1000;">
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 600; color: #111; margin-bottom: 10px;">
                <div style="flex: 1; text-align: left;">© 2025–2026 LAI'S LAB</div>
                <div style="flex: 1; text-align: center; color: #999;">SYSTEM V9.28 PRO AUDIT VERSION</div>
                <div style="flex: 1; text-align: right; color: {tier_color};">{tier_label}</div>
            </div>
            <div style="margin-bottom: 10px; text-align: center;">
                <p style="font-size: 10.5px; color: #888; margin: 0; font-style: italic;">
                    <b>Disclaimer:</b> Generative AI can make mistakes; please verify important information. 
                    Users are solely responsible for how they use the generated content. 
                    Lai's Lab assumes no liability for actions taken based on these outputs.
                </p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #aaa; border-top: 1px solid #fafafa; padding-top: 10px;">
                <div>👤 {st.session_state.user_email} | 🟢 All Systems Operational | <b>Live:</b> {online_count}</div>
                <div>
                    <a href="#" style="color: #aaa; text-decoration: none;">Privacy</a> | 
                    <a href="#" style="color: #aaa; text-decoration: none;">Terms</a> | 
                    <a href="https://app.lemonsqueezy.com/my-orders" target="_blank" style="color: #0277bd; text-decoration: none; font-weight: 700;">LemonSqueezy Verify</a>
                </div>
            </div>
        </div>
        <div style="height: 140px;"></div> 
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
            # ✅ 修复：找回激活码链接 (已补回)
            st.markdown('<div style="text-align: center; margin-top: 15px;"><a href="https://app.lemonsqueezy.com/my-orders" target="_blank" style="color: #666; font-size: 13px; text-decoration: none;">🔒 Lost your key? Retrieve via LemonSqueezy</a></div>', unsafe_allow_html=True)

    with col2:
        # 对比表保持最新
        st.subheader("🆚 Compare Plans")
        st.markdown(f"""
        <table class="compare-table">
            <tr><th>功能特性 (Capability)</th><th>访客试用 (Guest Trial)</th><th class="pro-column">💎 PRO 永久版 (Lifetime)</th></tr>
            <tr><td><b>每日生成限额 (Daily Limit)</b></td><td>5 次 / 天</td><td class="pro-column"><b>*Unlimited (无限生成)</b></td></tr>
            <tr><td><b>内容纯净度 (Format)</b></td><td>包含 AI 符号 (#, **)</td><td class="pro-column">100% 纯净 (人类书写感)</td></tr>
            <tr><td><b>结果分享与导出 (Sharing)</b></td><td>文本复制 + WhatsApp (带水印)</td><td class="pro-column">PDF 导出 + 纯净社媒分享</td></tr>
            <tr><td><b>全球语言支持 (Languages)</b></td><td>仅限 3 种基础语言</td><td class="pro-column">15+ 全球语言全开</td></tr>
            <tr><td><b>专业模式权限 (Expert Modes)</b></td><td>基础模式 (6个)</td><td class="pro-column">全部 18 种深度模式</td></tr>
            <tr><td><b>AI 结果水印 (Watermark)</b></td><td>强制包含推广水印</td><td class="pro-column">完全移除</td></tr>
            <tr><td><b>客服响应 (Support)</b></td><td>标准响应 (3-5天)</td><td class="pro-column">VIP 优先响应 (1-2天)</td></tr>
            <tr><td><b>价格 (Price)</b></td><td>免费 (Free)</td><td class="pro-column"><span class="price-tag">限时特惠 $12.90</span></td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.caption("* Fair Use Policy applies." if lang_sel == "English" else "* 遵循公平使用原则。")
    render_footer()

def show_main_app():
    ui = dm.LANG_MAP.get(st.session_state.language, dm.LANG_MAP["default"])
    with st.sidebar:
        st.caption(f"{'💎' if st.session_state.user_tier == 'Pro' else '👤'} {ui['plan_pro'] if st.session_state.user_tier == 'Pro' else ui['plan_guest']}")
        can_gen, rem, tot = lc.check_daily_limit_by_email(st.session_state.user_email, st.session_state.user_tier, st.session_state.daily_usage)
        bar_color = "#ff4b4b" if (tot - st.session_state.daily_usage) <= 1 else "#00f2fe"
        st.markdown(f"<style>.stProgress > div > div > div > div {{ background-image: linear-gradient(to right, {bar_color} 0%, {bar_color} 100%); }}</style>", unsafe_allow_html=True)
        st.progress(st.session_state.daily_usage / tot)
        st.caption(f"📊 {ui['usage']}: {st.session_state.daily_usage} / {tot}" if st.session_state.user_tier != "Pro" else f"✨ {ui.get('plan_pro', 'Pro Plan')}: Unlimited")
        st.divider()
        langs = dm.LANG_OPTIONS_PRO if st.session_state.user_tier == "Pro" else dm.LANG_OPTIONS_GUEST
        st.session_state.language = st.selectbox("Language", langs, index=langs.index(st.session_state.language) if st.session_state.language in langs else 0)
        role = st.selectbox(ui['role'], list(dm.ROLES_CONFIG.keys()))
        if st.button(ui['logout'], use_container_width=True): st.session_state.clear(); st.rerun()

    st.header(f"🎭 {role}")
    dynamic_count = 100 + (datetime.now().hour * 2) + random.randint(1, 15)
    st.markdown(f"""<div style="background: #fff9e6; border-left: 5px solid #ffcc00; padding: 10px; border-radius: 5px; margin-bottom: 15px;"><span style="font-size: 14px; color: #856404;">🔥 <b>{ui.get('live_stat', 'Live Status')}:</b> {dynamic_count} {'Users active today' if st.session_state.language == 'English' else '位用户今日活跃'}</span></div>""", unsafe_allow_html=True)

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
    render_footer()

if __name__ == "__main__":
    if st.session_state.logged_in: show_main_app()
    else: show_login_page()
