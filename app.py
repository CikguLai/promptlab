import streamlit as st
import time
import json
import datetime
import random
import base64
from fpdf import FPDF
import os

# ==========================================
# 1. 全局配置 (GLOBAL CONFIG)
# ==========================================
st.set_page_config(
    page_title="PromptLab AI V7.2",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 商业与限制规则
PRICE_PRO = "$12.90"
PRICE_OLD = "$39.90"
BUY_LINK = "https://your-lemonsqueezy-link.com"  # 替换为您的购买链接
LIMIT_TEXT_FREE = 5
LIMIT_IMAGE_FREE = 3
LIMIT_IMAGE_PRO = 200
UPLOAD_BATCH_FREE = 1
UPLOAD_BATCH_PRO = 50

# 语言定义
LANG_FREE = ["English", "Español", "简体中文"] # 国际范儿 3 巨头
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

# ==========================================
# 2. 工具函数 (UTILITIES)
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
    if db[email]["date"] != today: 
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
    # 模拟验证：管理员密码或 PRO 开头
    return key == "ADMIN-8888" or key.startswith("PRO")

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    # 字体容错机制
    try:
        pdf.add_font('CustomFont', '', 'font.ttf', uni=True)
        pdf.set_font('CustomFont', '', 12)
    except:
        pdf.set_font("Arial", size=12)
        content += "\n\n[System Note: CJK font (font.ttf) not found. Characters may be missing.]"
    
    # 防止编码错误
    safe_content = content.encode('latin-1', 'replace').decode('latin-1') if 'CustomFont' not in pdf.font_family else content
    pdf.multi_cell(0, 10, txt=content)
    return pdf.output(dest='S').encode('latin-1')

# 路由初始化
if 'page' not in st.session_state: st.session_state['page'] = 'home'
if 'user_type' not in st.session_state: st.session_state['user_type'] = 'guest'
if 'user_email' not in st.session_state: st.session_state['user_email'] = 'guest'

def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()

# ==========================================
# 3. 核心：全局侧边栏 (THE SIDEBAR)
# ==========================================
def render_sidebar():
    with st.sidebar:
        # 1. Logo (品牌)
        try:
            st.image("logo.png", width=120)
        except:
            st.markdown("# 🤖 PromptLab") # 回退方案
        
        st.markdown("---")

        # 2. 用户身份卡
        is_pro = st.session_state['user_type'] == 'pro'
        badge = "💎 PRO Enterprise" if is_pro else "👤 Free Guest"
        engine = "🚀 Turbo" if is_pro else "🐢 Standard"
        
        st.caption("Current User:")
        st.info(f"**{badge}**\n\nUser: {st.session_state.get('user_email')}\n\nEngine: {engine}")

        # 3. 语言切换 (PRO 15国 vs Guest 3国)
        lang_opts = LANG_PRO if is_pro else LANG_FREE
        # 保持语言选择记忆
        if "global_lang" not in st.session_state: st.session_state["global_lang"] = "English"
        st.selectbox("🌐 Language", lang_opts, key="global_lang")

        # 4. 侧边栏常驻广告 (仅限 Guest)
        if not is_pro:
            st.markdown("---")
            st.markdown(f"""
            <div style='background-color:#fff0f0; padding:15px; border-radius:8px; border:1px solid #ff4b4b; text-align:center;'>
                <div style='font-size:12px; color:#ff4b4b; font-weight:bold;'>🔥 LIMITED OFFER</div>
                <div style='font-size:14px; color:#333; margin-top:5px;'>Lifetime Access</div>
                <div style='font-size:24px; color:#ff4b4b; font-weight:bold; margin:5px 0;'>{PRICE_PRO}</div>
                <div style='font-size:12px; color:grey; text-decoration: line-through;'>Was {PRICE_OLD}</div>
                <a href="{BUY_LINK}" target="_blank">
                    <button style='background-color:#ff4b4b; color:white; border:none; padding:8px 20px; border-radius:5px; margin-top:10px; cursor:pointer; width:100%; font-weight:bold;'>
                        👉 Unlock Now
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 5. 智能工单 (Smart Ticket)
        with st.expander("🎫 Support Ticket (VIP)"):
            t_sub = st.text_input("Subject", key="ticket_sub")
            t_msg = st.text_area("Message", key="ticket_msg")
            
            # AI 拦截逻辑
            bad_words = ["refund", "money", "key", "code", "lost"]
            if any(w in t_sub.lower() for w in bad_words):
                st.warning("🤖 **AI Auto-Response:**\n\n- **Refunds:** Digital products are non-refundable.\n- **Keys:** Recover via LemonSqueezy.\n\n*Ticket intercepted.*")
            else:
                if st.button("Submit Ticket"):
                    st.success("✅ Priority Ticket Sent!" if is_pro else "✅ Ticket Queued (1-3 Days).")

        # 6. 完整分类 FAQ (Categorized)
        st.caption("📚 Knowledge Base")
        
        with st.expander("💰 Purchase & Billing"):
            st.markdown(f"""
            * **Is this a subscription?**
              No. One-time payment of {PRICE_PRO}.
            * **Refund Policy?**
              Strictly No Refunds for digital goods.
            * **Upgrade to PRO?**
              Instant activation after payment.
            """)
            
        with st.expander("🛠️ Technical Support"):
            st.markdown("""
            * **PDF Text Missing?**
              System requires 'font.ttf'. Contact admin.
            * **WeChat Button?**
              Opens system share menu on mobile.
            * **Output Language?**
              Auto-translated by V6.0 Engine.
            """)
            
        with st.expander("⚡ Limits & Usage"):
            st.markdown(f"""
            * **Free Limits?**
              {LIMIT_TEXT_FREE} Texts, {LIMIT_IMAGE_FREE} Images per day.
            * **Commercial Use?**
              PRO users have 100% commercial rights.
            * **Reset Time?**
              Limits reset daily at 00:00 server time.
            """)

        # 7. 底部退出
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['user_type'] = 'guest'
            st.session_state['page'] = 'home'
            st.rerun()

# ==========================================
# 4. 页面 1: 首页 (HOME) - 无侧边栏
# ==========================================
def render_home():
    # 注意：这里故意不调用 render_sidebar()，保持首页全屏
    
    # 顶部：小语言切换 (右上角)
    c_top1, c_top2 = st.columns([6, 1])
    with c_top2:
        st.selectbox("🌐", LANG_FREE, key="home_lang_select", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 居中 Logo 和 标题
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        try:
            st.image("logo.png", width=150) # 首页大 Logo
        except:
            st.markdown("<h1 style='text-align: center;'>🤖</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 3.5em; margin-top:-20px;'>PromptLab AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: grey; font-size: 1.2em;'>The Ultimate Enterprise Prompt Engine</p>", unsafe_allow_html=True)
    
    st.divider()

    # 左右布局：登录 vs 对比
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("🔓 Login / Access")
        tab1, tab2 = st.tabs(["👤 Guest Trial", "💎 PRO Login"])
        
        with tab1:
            email = st.text_input("Email Address", key="guest_email_in")
            if st.button("🚀 Start Free Trial", use_container_width=True):
                st.session_state['user_type'] = 'guest'
                st.session_state['user_email'] = email if email else "guest@temp.com"
                navigate_to('roles') # 跳转

        with tab2:
            pe = st.text_input("PRO Email", key="pro_email_in")
            pk = st.text_input("License Key", type="password")
            if st.button("💎 Login PRO", use_container_width=True):
                if validate_license(pk):
                    st.session_state['user_type'] = 'pro'
                    st.session_state['user_email'] = pe
                    navigate_to('roles') # 跳转
                else:
                    st.error("Invalid License Key")

    with col2:
        st.subheader("🆚 Plan Comparison")
        st.markdown(f"""
        | Feature | 👤 Free Guest | 💎 PRO ({PRICE_PRO}) |
        | :--- | :--- | :--- |
        | **Engine** | 🐢 Standard | 🚀 **Turbo Priority** |
        | **Text Limit** | 🔒 {LIMIT_TEXT_FREE} / Day | ✅ **Unlimited** |
        | **Image Limit** | 🔒 {LIMIT_IMAGE_FREE} / Day | ✅ **Max {LIMIT_IMAGE_PRO}** |
        | **Languages** | 🔒 3 (Intl.) | ✅ **15 Global** |
        | **Uploads** | 🔒 1 File | ✅ **Batch 50** |
        | **Export** | 🔒 Watermark | ✅ **Clean PDF/CSV** |
        """)
        
        # 折叠的详细规格
        with st.expander("🔍 Click to view Full Specs (Languages & Modes)"):
            st.markdown("**🌏 15 Supported Languages:**")
            st.caption(", ".join(LANG_PRO))
            st.markdown("**🛠️ 18 Professional Modes:**")
            for r in ROLES:
                st.caption(f"**{r}**: {', '.join(ROLES[r])}")

# ==========================================
# 5. 页面 2: 角色大厅 (ROLES)
# ==========================================
def render_roles():
    render_sidebar() # 侧边栏回归
    
    st.button("⬅️ Back to Home", on_click=lambda: navigate_to('home'))
    st.title("🎭 Choose Workspace")
    
    cols = st.columns(3)
    role_keys = list(ROLES.keys())
    
    for i, role in enumerate(role_keys):
        with cols[i % 3]:
            # 修复：直接显示完整名字，不拆分
            if st.button(f"✨ {role}", key=f"btn_{role}", use_container_width=True, type="secondary"):
                st.session_state['current_role'] = role
                navigate_to('workspace')
            
            st.caption(f"Includes: {', '.join(ROLES[role][:2])}...")
            st.markdown("---")

# ==========================================
# 6. 页面 3: 核心工作台 (WORKSPACE)
# ==========================================
def render_workspace():
    render_sidebar() # 侧边栏回归
    
    # 顶部导航
    c_nav1, c_nav2 = st.columns([1, 5])
    with c_nav1:
        st.button("⬅️ Change Role", on_click=lambda: navigate_to('roles'))
    with c_nav2:
        st.success(f"🛠️ **{st.session_state['current_role']}** | Mode: {st.session_state['user_type'].upper()}")

    # 额度展示
    u = get_usage(st.session_state['user_email'])
    is_pro = st.session_state['user_type'] == 'pro'
    
    c1, c2 = st.columns(2)
    with c1: st.progress(0 if is_pro else u['text']/LIMIT_TEXT_FREE, f"Text Usage: {u['text']}/{'Unl.' if is_pro else LIMIT_TEXT_FREE}")
    with c2: st.progress(u['image']/(LIMIT_IMAGE_PRO if is_pro else LIMIT_IMAGE_FREE), f"Image Usage: {u['image']}/{LIMIT_IMAGE_PRO if is_pro else LIMIT_IMAGE_FREE}")

    st.divider()

    # 输入区域
    ci1, ci2 = st.columns([1, 1])
    with ci1:
        modes = ROLES[st.session_state['current_role']]
        # 模式锁：免费只给第一个
        opts = modes if is_pro else [modes[0]] + [f"🔒 {m} (PRO)" for m in modes[1:]]
        sel_mode = st.selectbox("Select Mode", opts)
        
        if "🔒" in sel_mode:
            st.error(f"⚠️ Mode Locked. Upgrade to {PRICE_PRO} to unlock.")
            st.stop()
            
        # 显示当前语言（从侧边栏同步）
        cur_lang = st.session_state.get("global_lang", "English")
        st.caption(f"Output Language: **{cur_lang}** (Change in Sidebar)")

    with ci2:
        # 上传锁：免费单选，PRO多选 + 文案提示
        multi = True if is_pro else False
        help_msg = f"✅ Batch Mode: Support up to {UPLOAD_BATCH_PRO} images (Daily Limit: {LIMIT_IMAGE_PRO})" if is_pro else "🔒 Free Limit: 1 Image (Upgrade for Batch 50)"
        up_files = st.file_uploader("Upload Context", accept_multiple_files=multi, help=help_msg)

    user_topic = st.text_area("Input Topic / Details", height=150, placeholder="Enter details...")

    # 生成按钮 & 等待剧场
    if st.button("✨ Generate Prompt (PASEC)", type="primary", use_container_width=True):
        
        # 额度检查
        has_img = up_files is not None and len(up_files) > 0
        allow = False
        if is_pro: allow = True
        else:
            if has_img and u['image'] >= LIMIT_IMAGE_FREE: st.error("Image Limit Reached!"); st.stop()
            elif not has_img and u['text'] >= LIMIT_TEXT_FREE: st.error("Text Limit Reached!"); st.stop()
            allow = True
            
        if allow:
            update_usage(st.session_state['user_email'], "image" if has_img else "text")
            
            with st.status("🚀 Initializing...", expanded=True) as status:
                if is_pro:
                    time.sleep(0.5)
                    status.update(label="🚀 Turbo Engine: Done!", state="complete")
                else:
                    status.write("🐢 Connecting to Standard Server...")
                    p_bar = status.progress(0)
                    for i in range(100):
                        time.sleep(0.03) # 模拟 3秒
                        p_bar.progress(i+1)
                        if i == 50: status.write("💡 Tip: PRO users skip this queue...")
                    status.update(label="✅ Generation Complete", state="complete")
            
            # PASEC Mock 生成
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            wm = f"\n\n---\n🔒 [Trial Version - {timestamp}]" if not is_pro else ""
            
            st.session_state['result'] = f"""# Generated Prompt ({cur_lang})

## 👤 P - Persona
**Role**: {st.session_state['current_role']}
**Language**: {cur_lang}

## 🎯 A - Aim
**Task**: {sel_mode}
**Topic**: {user_topic}

## 📂 S - Structure
Output Format: Markdown Table & Lists.

## 📝 E - Effective
Constraints: Professional tone, no fluff.

## 💡 C - Context
Input: {len(up_files) if up_files else 0} files analyzed.

---
**[Prompt Content]**
(Here is the high-quality content generated by the AI based on PASEC framework...)
{wm}
"""
            st.rerun()

    # 结果展示 & 5层塔
    if 'result' in st.session_state:
        st.divider()
        st.subheader("🎉 Result")
        st.text_area("Output", st.session_state['result'], height=300)
        
        # Layer 1: Copy
        st.button("📋 Copy Result", use_container_width=True)
        
        # Layer 2: AI Direct
        st.caption("🤖 **AI Direct Connect:**")
        aic = st.columns(6)
        links = ["Gemini", "ChatGPT", "Claude", "Perplexity", "Midjourney", "Canva"]
        for i, l in enumerate(links): aic[i].button(l)
        
        # Layer 3: Social
        st.caption("📤 **Social Share:**")
        sc1, sc2, sc3 = st.columns(3)
        with sc1: 
            if is_pro: st.button("🟢 WeChat")
            else: st.button("🔒 WeChat", disabled=True)
        with sc2: st.button("📤 System")
        with sc3: st.link_button("WhatsApp", "https://wa.me")
        
        # Layer 4: Apps
        st.caption("📱 **App Portals:**")
        ap1, ap2, ap3 = st.columns(3)
        ap1.link_button("Instagram", "https://instagram.com")
        ap2.link_button("📕 XiaoHongShu", "https://xiaohongshu.com")
        ap3.link_button("TikTok", "https://tiktok.com")
        
        # Layer 5: Downloads
        st.caption("💾 **Downloads:**")
        dc1, dc2, dc3 = st.columns(3)
        
        # TXT
        b64 = base64.b64encode(st.session_state['result'].encode()).decode()
        dc1.markdown(f'<a href="data:file/txt;base64,{b64}" download="prompt.txt"><button style="width:100%">📄 TXT</button></a>', unsafe_allow_html=True)
        
        # PDF (Lock)
        with dc2:
            if is_pro:
                try:
                    pdf_d = generate_pdf(st.session_state['result'])
                    b64p = base64.b64encode(pdf_d).decode()
                    st.markdown(f'<a href="data:application/pdf;base64,{b64p}" download="prompt.pdf"><button style="width:100%">📕 PDF</button></a>', unsafe_allow_html=True)
                except:
                    st.error("Font Error")
            else:
                st.button("🔒 PDF (PRO)")
                
        # CSV (Lock)
        with dc3:
            if is_pro: st.button("📊 CSV")
            else: st.button("🔒 CSV (PRO)", disabled=True)

# ==========================================
# 7. 主程序路由 (MAIN)
# ==========================================
if st.session_state['page'] == 'home':
    render_home()
elif st.session_state['page'] == 'roles':
    render_roles()
elif st.session_state['page'] == 'workspace':
    render_workspace()