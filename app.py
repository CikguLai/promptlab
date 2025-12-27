import streamlit as st
import time
import json
import datetime
import random
import base64
from fpdf import FPDF
import os

# ==========================================
# 1. 全局配置与常量 (CONFIG & CONSTANTS)
# ==========================================
st.set_page_config(
    page_title="PromptLab AI V7.1",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 商业规则
PRICE_PRO = "$12.90"
PRICE_OLD = "$39.90"
BUY_LINK = "https://your-lemonsqueezy-link.com" # 替换为您的收款链接
LIMIT_TEXT_FREE = 5
LIMIT_IMAGE_FREE = 3
LIMIT_IMAGE_PRO = 200
UPLOAD_BATCH_FREE = 1
UPLOAD_BATCH_PRO = 50

# 国际化语言策略
LANG_FREE = ["English", "Español", "简体中文"] # 国际范儿三巨头
LANG_PRO = [
    "English", "简体中文", "Bahasa Melayu", "Español", "Russian", 
    "Japanese", "Korean", "French", "German", "Indonesian", 
    "Thai", "Vietnamese", "Arabic", "Tamil", "Portuguese", 
    "Italian", "Hindi", "Filipino"
]

# 角色定义
ROLES = {
    "Global Educator": ["Pedagogy", "Lesson Plan", "Assessment"],
    "Global Creator": ["Thumbnail", "Scripting", "Shorts/Reels"],
    "Global Seller": ["Copywriting", "Product Desc", "Email Marketing"],
    "Parent": ["Storytelling", "Activity", "Discipline"],
    "Student": ["Essay", "Study Plan", "Summary"],
    "Corporate": ["Strategy", "Meeting", "HR/Email"]
}

# UI 字典 (精简版)
UI = {
    "English": {"limit_reached": "Limit Reached!", "queue": "🐢 Standard Engine: Queuing...", "turbo": "🚀 Turbo Engine: Active"},
    "Español": {"limit_reached": "¡Límite alcanzado!", "queue": "🐢 Motor Estándar: En cola...", "turbo": "🚀 Motor Turbo: Activo"},
    "简体中文": {"limit_reached": "限额已满！", "queue": "🐢 标准引擎：排队中...", "turbo": "🚀 极速引擎：已激活"},
}

# ==========================================
# 2. 数据库与工具函数 (TOOLS)
# ==========================================
DB_FILE = 'user_db.json'

def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, 'r') as f: return json.load(f)

def save_db(db):
    with open(DB_FILE, 'w') as f: json.dump(db, f)

def get_usage(email):
    db = load_db()
    today = str(datetime.date.today())
    if email not in db: db[email] = {"date": today, "text": 0, "image": 0}
    if db[email]["date"] != today: # 跨天重置
        db[email] = {"date": today, "text": 0, "image": 0}
        save_db(db)
    return db[email]

def update_usage(email, type="text"):
    db = load_db()
    today = str(datetime.date.today())
    if email not in db or db[email]["date"] != today:
        db[email] = {"date": today, "text": 0, "image": 0}
    
    db[email][type] += 1
    save_db(db)

def validate_license(key):
    return key == "ADMIN-8888" or key.startswith("PRO")

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    # 尝试加载中文字体，否则回退
    try:
        pdf.add_font('CustomFont', '', 'font.ttf', uni=True)
        pdf.set_font('CustomFont', '', 12)
    except:
        pdf.set_font("Arial", size=12)
        content += "\n\n[System Error: font.ttf not found. CJK characters may not render.]"
    
    pdf.multi_cell(0, 10, txt=content)
    return pdf.output(dest='S').encode('latin-1')

# 路由控制
if 'page' not in st.session_state: st.session_state['page'] = 'home'
if 'user_type' not in st.session_state: st.session_state['user_type'] = 'guest'
if 'user_email' not in st.session_state: st.session_state['user_email'] = 'guest'

def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()

# ==========================================
# 3. 全局侧边栏 (GLOBAL SIDEBAR)
# ==========================================
def render_sidebar():
    with st.sidebar:
        # 1. Logo (Branding)
        try:
            st.image("logo.png", width=100)
        except:
            st.markdown("# 🤖 PromptLab")
        
        st.markdown("---")

        # 2. 用户身份卡
        is_pro = st.session_state['user_type'] == 'pro'
        engine_status = "🚀 Turbo" if is_pro else "🐢 Standard"
        user_badge = "💎 PRO Enterprise" if is_pro else "👤 Free Guest"
        
        st.caption(f"User: {st.session_state.get('user_email', 'Guest')}")
        st.info(f"**{user_badge}**\n\nEngine: {engine_status}")

        # 3. 语言切换 (Global)
        lang_opts = LANG_PRO if is_pro else LANG_FREE
        app_lang = st.selectbox("🌐 Language", lang_opts, key="global_lang")

        # 4. 侧边栏常驻广告 (Free Only)
        if not is_pro:
            st.markdown(f"""
            <div style='background-color:#ffebeb; padding:15px; border-radius:8px; border:1px solid #ff4b4b; text-align:center; margin-top:20px; margin-bottom:20px;'>
                <h4 style='color:#ff4b4b; margin:0;'>🔥 Lifetime Deal</h4>
                <p style='font-size:13px; margin:5px 0;'>Unlock Full Power for just</p>
                <h2 style='color:#ff4b4b; margin:0;'>{PRICE_PRO}</h2>
                <p style='text-decoration: line-through; color:grey; font-size:12px; margin:0;'>Was {PRICE_OLD}</p>
                <a href="{BUY_LINK}" target="_blank" style='text-decoration:none;'>
                    <button style='background-color:#ff4b4b; color:white; border:none; padding:8px 16px; border-radius:4px; margin-top:10px; cursor:pointer; width:100%; font-weight:bold;'>
                        👉 Get Access Now
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 5. 智能工单系统 (Smart Support)
        with st.expander("🎫 Support Ticket (VIP)"):
            t_sub = st.text_input("Subject", key="t_sub")
            t_msg = st.text_area("Message", key="t_msg")
            
            # AI 拦截
            keywords = ["refund", "money", "return", "key", "code"]
            if any(k in t_sub.lower() for k in keywords):
                st.info("🤖 **AI Assistant:**\n\n- **Refunds:** No refunds for digital goods.\n- **Lost Key:** Recover at LemonSqueezy.\n\n*Ticket blocked by AI based on Policy.*")
            else:
                if st.button("Submit Ticket"):
                    st.success("✅ Ticket sent! (Priority: High)" if is_pro else "✅ Ticket queued. (Wait: 1-3 days)")

        # 6. FAQ
        with st.expander("❓ FAQ / Policy"):
            st.markdown(f"""
            - **Refunds?** No. Digital products are final sale.
            - **Subscription?** No. One-time {PRICE_PRO}.
            - **PDF Error?** Contact support if fonts missing.
            """)

        # 7. 底部退出
        st.markdown("---")
        if st.button("Logout"):
            st.session_state['user_type'] = 'guest'
            st.session_state['page'] = 'home'
            st.rerun()

# ==========================================
# 4. PAGE 1: 首页 (LANDING)
# ==========================================
def render_home():
    render_sidebar()
    
    st.markdown("<h1 style='text-align: center; font-size: 3.5em;'>🤖 PromptLab AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey; margin-bottom: 40px;'>The Ultimate Enterprise Prompt Engine</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("🔓 Login / Access")
        tab_guest, tab_pro = st.tabs(["👤 Guest Trial", "💎 PRO Login"])
        
        with tab_guest:
            st.markdown("Try limited features for free.")
            em = st.text_input("Email Address", key="guest_email")
            if st.button("🚀 Start Free Trial", use_container_width=True):
                if em:
                    st.session_state['user_type'] = 'guest'
                    st.session_state['user_email'] = em
                    navigate_to('roles')
                else:
                    st.error("Email required.")

        with tab_pro:
            st.markdown("Access your Enterprise Dashboard.")
            pem = st.text_input("PRO Email", key="pro_email")
            pkey = st.text_input("License Key", type="password")
            if st.button("💎 Login PRO", use_container_width=True):
                if validate_license(pkey):
                    st.session_state['user_type'] = 'pro'
                    st.session_state['user_email'] = pem
                    navigate_to('roles')
                else:
                    st.error("Invalid Key")

    with col2:
        st.subheader("🆚 Plan Comparison")
        st.markdown(f"""
        | Feature | 👤 Free Guest | 💎 PRO ({PRICE_PRO}) |
        | :--- | :--- | :--- |
        | **Engine** | 🐢 Standard | 🚀 **Turbo Priority** |
        | **Limits** | 🔒 {LIMIT_TEXT_FREE} Text / {LIMIT_IMAGE_FREE} Img | ✅ **Unlimited** |
        | **Languages** | 🔒 3 (Intl.) | ✅ **15 Global** |
        | **Uploads** | 🔒 1 File | ✅ **Batch 50** |
        | **Export** | 🔒 Watermarked | ✅ **Clean PDF/CSV** |
        """)
        
        # 折叠的超详细规格表
        with st.expander("🔍 Click to view Full Specs (Languages, Modes, Platforms)"):
            st.markdown("**🌏 15 Supported Languages (PRO):**")
            st.caption(", ".join(LANG_PRO))
            st.markdown("**🛠️ 18 Specialized Modes:**")
            for r, ms in ROLES.items():
                st.caption(f"**{r}**: {', '.join(ms)}")
            st.markdown("**📱 Supported Platforms:**")
            st.caption("WeChat, WhatsApp, Instagram, TikTok, XiaoHongShu, Midjourney, Stable Diffusion")

# ==========================================
# 5. PAGE 2: 角色大厅 (ROLE HALL)
# ==========================================
def render_roles():
    render_sidebar()
    st.button("⬅️ Back to Home", on_click=lambda: navigate_to('home'))
    
    st.title("🎭 Choose Your Workspace")
    st.markdown("Select a specialized role to activate the AI context.")
    
    cols = st.columns(3)
    role_list = list(ROLES.keys())
    
    for i, role in enumerate(role_list):
        with cols[i % 3]:
            # 修复：不再尝试拆分字符串，避免 IndexError
            if st.button(f"✨ {role}", key=role, use_container_width=True, type="secondary"):
                st.session_state['current_role'] = role
                navigate_to('workspace')
            
            # 模式预览
            st.caption(f"Modes: {', '.join(ROLES[role])}")
            st.markdown("---")

# ==========================================
# 6. PAGE 3: 核心工作台 (WORKSPACE)
# ==========================================
def render_workspace():
    render_sidebar()
    
    # 顶部导航
    col_nav1, col_nav2 = st.columns([1, 5])
    with col_nav1:
        st.button("⬅️ Change Role", on_click=lambda: navigate_to('roles'))
    with col_nav2:
        # 显示当前状态
        curr_role = st.session_state.get('current_role', 'Global Educator')
        st.success(f"🛠️ **Workspace Active:** {curr_role}")

    # 获取额度
    u_email = st.session_state.get('user_email')
    usage = get_usage(u_email)
    is_pro = st.session_state['user_type'] == 'pro'

    # 额度条
    c1, c2 = st.columns(2)
    with c1:
        txt_limit = "Unlimited" if is_pro else LIMIT_TEXT_FREE
        st.progress(0 if is_pro else usage['text']/LIMIT_TEXT_FREE, f"Text Usage: {usage['text']}/{txt_limit}")
    with c2:
        img_limit = LIMIT_IMAGE_PRO if is_pro else LIMIT_IMAGE_FREE
        st.progress(usage['image']/img_limit, f"Image Vision: {usage['image']}/{img_limit}")

    st.markdown("---")

    # 核心操作区
    col_input1, col_input2 = st.columns([1, 1])
    
    with col_input1:
        # 模式选择 (锁免费用户的高级模式)
        modes = ROLES[st.session_state['current_role']]
        # 免费只给第一个，其他加锁
        mode_opts = modes if is_pro else [modes[0]] + [f"🔒 {m} (PRO)" for m in modes[1:]]
        sel_mode = st.selectbox("Select Mode", mode_opts)
        
        if "🔒" in sel_mode:
            st.error(f"⚠️ Mode Locked. Upgrade to {PRICE_PRO} to unlock.")
            st.stop()
            
        # 语言选择 (使用侧边栏全局设置，这里只显示确认)
        curr_lang = st.session_state.get("global_lang", "English")
        st.caption(f"Output Language: **{curr_lang}** (Change in Sidebar)")

    with col_input2:
        # 上传限制
        multi = True if is_pro else False
        limit_msg = f"Batch: {UPLOAD_BATCH_PRO}" if is_pro else f"Batch: {UPLOAD_BATCH_FREE} (PRO: 50)"
        up_files = st.file_uploader("Upload Context (Image/Doc)", accept_multiple_files=multi, help=limit_msg)

    # 输入框
    user_topic = st.text_area("Input Topic / Details", height=150, placeholder="Enter your topic here...")

    # 生成按钮
    if st.button("✨ Generate Prompt (PASEC Auto-Structure)", type="primary", use_container_width=True):
        
        # 1. 额度检查
        has_img = up_files is not None and len(up_files) > 0
        allow = False
        
        if is_pro:
            if has_img and usage['image'] >= LIMIT_IMAGE_PRO: st.error("Image Limit Reached"); st.stop()
            allow = True
        else:
            if has_img:
                if usage['image'] >= LIMIT_IMAGE_FREE: st.error(f"Image Limit Reached ({LIMIT_IMAGE_FREE})"); st.stop()
            else:
                if usage['text'] >= LIMIT_TEXT_FREE: st.error(f"Text Limit Reached ({LIMIT_TEXT_FREE})"); st.stop()
            allow = True
            
        if allow:
            # 扣费
            update_usage(u_email, "image" if has_img else "text")
            
            # 2. 等待剧场
            with st.status("🚀 Initializing...", expanded=True) as status:
                if is_pro:
                    time.sleep(0.5)
                    status.update(label="🚀 Turbo Engine: Done!", state="complete")
                else:
                    status.write("🐢 Connecting to Standard Server...")
                    progress = status.progress(0)
                    for i in range(100):
                        time.sleep(0.03)
                        progress.progress(i+1)
                        if i == 50: status.write("💡 Tip: Upgrade to PRO to skip queue...")
                    status.update(label="✅ Generation Complete", state="complete")
            
            # 3. 生成 PASEC 结构化内容 (Mock)
            # 这里展示 PromptLab 的核心价值：自动输出结构
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            watermark = f"\n\n---\n🔒 [Trial Version - {timestamp}]" if not is_pro else ""
            
            mock_res = f"""# {sel_mode} Prompt (Generated by PromptLab V7.1)
            
## 👤 P - Persona (角色设定)
**Role**: {st.session_state['current_role']}
**Tone**: Professional, Engaging, Authoritative.
**Language**: {curr_lang}

## 🎯 A - Aim (任务目标)
To create a high-quality **{sel_mode}** based on the topic: "{user_topic}".
Ensure the content is optimized for the target audience.

## 📂 S - Structure (输出格式)
Please output the result in the following format:
1.  **Headline/Title**: Catchy and relevant.
2.  **Core Content**: Detailed explanation.
3.  **Call to Action**: Clear next steps.

## 📝 E - Effective (限制条件)
- Avoid jargon unless necessary.
- Keep sentences concise.
- strictly follow {curr_lang} grammar rules.

## 💡 C - Context (背景分析)
User provided {len(up_files) if up_files else 0} reference files.
The content should be tailored for {curr_lang} speaking regions.

---
**[Prompt Content Starts Here]**
(Here the AI would generate the actual lesson plan/copywriting based on the structure above...)
{watermark}
"""
            st.session_state['result'] = mock_res
            st.rerun()

    # 结果展示与 5层塔
    if 'result' in st.session_state:
        st.divider()
        st.subheader("🎉 Result")
        st.text_area("Output", st.session_state['result'], height=300)
        
        # Layer 1: Copy
        st.button("📋 Copy Result", use_container_width=True)
        
        # Layer 2: AI Links
        st.caption("🤖 **Direct AI Connect:**")
        ai_cols = st.columns(6)
        links = [("Gemini","https://gemini.google.com"), ("ChatGPT","https://chat.openai.com"), ("Claude","https://claude.ai"), ("Perplexity","https://perplexity.ai"), ("Midjourney","https://discord.com"), ("Canva","https://canva.com")]
        for i, (n, l) in enumerate(links):
            ai_cols[i].link_button(n, l)
            
        # Layer 3: Social Share
        st.caption("📤 **Social Share:**")
        s_cols = st.columns(4)
        with s_cols[0]:
            if is_pro: st.button("🟢 WeChat")
            else: st.button("🔒 WeChat", disabled=True)
        with s_cols[1]: st.button("📤 System Share")
        with s_cols[2]: st.link_button("WhatsApp", "https://wa.me")
        
        # Layer 4: App Portals
        st.caption("📱 **App Portals:**")
        a_cols = st.columns(3)
        a_cols[0].link_button("Instagram", "https://instagram.com")
        a_cols[1].link_button("📕 XiaoHongShu", "https://xiaohongshu.com")
        a_cols[2].link_button("TikTok", "https://tiktok.com")
        
        # Layer 5: Downloads
        st.caption("💾 **Downloads:**")
        d_cols = st.columns(3)
        
        # TXT
        b64_txt = base64.b64encode(st.session_state['result'].encode()).decode()
        d_cols[0].markdown(f'<a href="data:file/txt;base64,{b64_txt}" download="prompt.txt"><button style="width:100%">📄 TXT</button></a>', unsafe_allow_html=True)
        
        # PDF & CSV (Locked)
        with d_cols[1]:
            if is_pro:
                try:
                    pdf_data = generate_pdf(st.session_state['result'])
                    b64_pdf = base64.b64encode(pdf_data).decode()
                    st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="prompt.pdf"><button style="width:100%">📕 PDF</button></a>', unsafe_allow_html=True)
                except:
                    st.error("Font Error")
            else:
                st.button("🔒 PDF (PRO)")
        
        with d_cols[2]:
            if is_pro: st.button("📊 CSV")
            else: st.button("🔒 CSV (PRO)")

# ==========================================
# 7. 主程序入口 (ROUTER)
# ==========================================
if st.session_state['page'] == 'home':
    render_home()
elif st.session_state['page'] == 'roles':
    render_roles()
elif st.session_state['page'] == 'workspace':
    render_workspace()