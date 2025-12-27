import streamlit as st
import time
import json
import datetime
import random
import base64
from fpdf import FPDF
import os

# ==========================================
# 1. 配置与常量 (CONFIG & CONSTANTS)
# ==========================================
st.set_page_config(
    page_title="PromptLab AI v6.0 Ultimate",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 商业规则常量
PRICE_PRO = "$12.90"
PRICE_OLD = "$39.90"
LIMIT_TEXT_FREE = 5
LIMIT_IMAGE_FREE = 3
LIMIT_IMAGE_PRO = 200
UPLOAD_BATCH_FREE = 1
UPLOAD_BATCH_PRO = 50

# 15国语言列表 (PRO) vs 3国 (FREE)
LANG_ALL = [
    "English", "简体中文", "Bahasa Melayu", "Russian", "Japanese", 
    "Korean", "French", "Spanish", "German", "Indonesian", 
    "Thai", "Vietnamese", "Arabic", "Tamil", "Portuguese"
]
LANG_FREE = ["English", "简体中文", "Bahasa Melayu"]

# UI 字典映射 (部分示例，覆盖主要界面)
UI_DICT = {
    "English": {
        "title": "PromptLab AI", "tagline": "Enterprise-Grade Prompt Generator",
        "login_pro": "Login (PRO)", "guest": "Free Guest", "logout": "Logout",
        "role_select": "Choose Your Workspace", "gen_btn": "✨ Generate Prompt",
        "copy_btn": "📋 Copy Result", "upload_label": "Upload Reference Images",
        "limit_reached": "Daily Limit Reached!", "upgrade_msg": "Upgrade to PRO for Unlimited Access",
        "queue_msg": "🐢 Standard Engine: You are in queue...", "turbo_msg": "🚀 Turbo Engine: Priority Access",
        "footer": "© 2026 Lai's Lab | Disclaimer: AI content for reference only."
    },
    "简体中文": {
        "title": "PromptLab AI", "tagline": "企业级 AI 提示词生成器",
        "login_pro": "登录 (PRO)", "guest": "免费试用", "logout": "退出登录",
        "role_select": "选择您的工作区", "gen_btn": "✨ 开始生成",
        "copy_btn": "📋 复制结果", "upload_label": "上传参考图片",
        "limit_reached": "今日限额已用完！", "upgrade_msg": "升级 PRO 享受无限生成",
        "queue_msg": "🐢 标准引擎：正在排队中...", "turbo_msg": "🚀 极速引擎：优先通道已激活",
        "footer": "© 2026 黎志坚实验室 | 免责声明：AI内容仅供参考。"
    },
    "Bahasa Melayu": {
        "title": "PromptLab AI", "tagline": "Penjana Prompt Gred Perusahaan",
        "login_pro": "Log Masuk (PRO)", "guest": "Tetamu Percuma", "logout": "Log Keluar",
        "role_select": "Pilih Ruang Kerja", "gen_btn": "✨ Jana Prompt",
        "copy_btn": "📋 Salin Hasil", "upload_label": "Muat Naik Gambar",
        "limit_reached": "Had Harian Dicapai!", "upgrade_msg": "Naik Taraf PRO untuk Akses Tanpa Had",
        "queue_msg": "🐢 Enjin Standard: Anda dalam barisan...", "turbo_msg": "🚀 Enjin Turbo: Akses Prioriti",
        "footer": "© 2026 Lai's Lab | Penafian: Kandungan AI untuk rujukan sahaja."
    },
    # 其他语言默认回落到英文，此处省略以节省空间
}

# 角色与模式定义
ROLES = {
    "Global Educator": ["Pedagogy (教学法)", "Lesson Plan (教案)", "Assessment (评估)"],
    "Global Creator": ["Thumbnail (封面图)", "Scripting (脚本)", "Shorts/Reels (短视频)"],
    "Global Seller": ["Copywriting (文案)", "Product Description (产品)", "Email Marketing (邮件)"],
    "Parent": ["Storytelling (故事)", "Activity (活动)", "Discipline (管教)"],
    "Student": ["Essay (论文)", "Study Plan (计划)", "Summary (总结)"],
    "Corporate": ["Strategy (战略)", "Meeting (会议)", "HR/Email (行政)"]
}

# ==========================================
# 2. 数据库与记忆系统 (DATABASE & PERSISTENCE)
# ==========================================
DB_FILE = 'user_db.json'

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f)

def get_daily_usage(email):
    db = load_db()
    today = str(datetime.date.today())
    if email not in db:
        db[email] = {"date": today, "text_count": 0, "image_count": 0}
    
    # 如果日期跨天，重置
    if db[email]["date"] != today:
        db[email] = {"date": today, "text_count": 0, "image_count": 0}
        save_db(db)
    
    return db[email]

def update_usage(email, type="text"):
    db = load_db()
    today = str(datetime.date.today())
    if email not in db or db[email]["date"] != today:
         db[email] = {"date": today, "text_count": 0, "image_count": 0}
    
    if type == "text":
        db[email]["text_count"] += 1
    elif type == "image":
        db[email]["image_count"] += 1
    
    save_db(db)

# ==========================================
# 3. 核心逻辑函数 (CORE LOGIC)
# ==========================================
def validate_license(key):
    # 模拟验证：如果是 admin-8888 或以 PRO 开头则通过
    if key == "ADMIN-8888" or key.startswith("PRO-2026"):
        return True
    return False

def get_ui_text(key, lang):
    # 简单的字典查找，如果找不到语言默认英文
    l_dict = UI_DICT.get(lang, UI_DICT["English"])
    return l_dict.get(key, UI_DICT["English"][key])

def smart_ticket_intercept(subject):
    keywords = ["refund", "key", "money", "code", "activate", "lost"]
    for k in keywords:
        if k in subject.lower():
            return True
    return False

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    # 尝试加载字体，如果失败使用默认
    try:
        pdf.add_font('NotoSans', '', 'font.ttf', uni=True)
        pdf.set_font('NotoSans', '', 12)
    except:
        pdf.set_font("Arial", size=12)
        content = content + "\n\n[System Note: font.ttf not found for CJK characters]"
    
    pdf.multi_cell(0, 10, txt=content)
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 4. 界面构建 (UI BUILDER)
# ==========================================

# --- 侧边栏 ---
with st.sidebar:
    st.header("🔑 Login / Access")
    
    # 登录状态管理
    if 'user_type' not in st.session_state:
        st.session_state['user_type'] = 'guest'
        st.session_state['user_email'] = f"guest_{random.randint(1000,9999)}@temp.com"

    # 全局语言设置
    app_lang = st.selectbox("🌐 Language / 语言", LANG_FREE + ["Russian (PRO)", "Japanese (PRO)"] if st.session_state['user_type'] == 'pro' else LANG_FREE)
    
    if st.session_state['user_type'] == 'guest':
        st.info(f"👤 **{get_ui_text('guest', app_lang)}**")
        with st.expander("🔓 Unlock PRO Access", expanded=True):
            email_input = st.text_input("Email")
            key_input = st.text_input("License Key")
            if st.button(get_ui_text('login_pro', app_lang)):
                if validate_license(key_input):
                    st.session_state['user_type'] = 'pro'
                    st.session_state['user_email'] = email_input
                    st.rerun()
                else:
                    st.error("Invalid Key")
        
        # 侧边栏广告
        st.markdown(f"""
        <div style='background-color:#ffebeb; padding:10px; border-radius:5px; border:1px solid #ff4b4b;'>
            <h4 style='color:#ff4b4b; margin:0;'>🔥 Lifetime Deal</h4>
            <p style='font-size:14px;'>Get Unlimited Access for <br>
            <b style='font-size:18px;'>{PRICE_PRO}</b> <s style='color:grey'>{PRICE_OLD}</s></p>
            <p style='font-size:12px;'>No Monthly Fees. One-time Payment.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.success(f"💎 **PRO Enterprise**\n\nUser: {st.session_state['user_email']}")
        if st.button(get_ui_text('logout', app_lang)):
            st.session_state['user_type'] = 'guest'
            st.rerun()

    st.markdown("---")
    
    # 智能工单系统
    with st.expander("🎫 Support Ticket (VIP)"):
        ticket_subject = st.text_input("Subject")
        ticket_msg = st.text_area("Message")
        
        # AI 拦截逻辑
        if ticket_subject and smart_ticket_intercept(ticket_subject):
            st.info("🤖 **AI Helper:**\nIt seems you are asking about Refunds or Keys.\n\n- [Find My Key](https://app.lemonsqueezy.com)\n- [Refund Policy](https://example.com)\n\n*Ticket submission blocked for instant resolution.*")
        else:
            if st.button("🚀 Submit Ticket"):
                if not ticket_subject or not ticket_msg:
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner("AI Agent reviewing..."):
                        time.sleep(1.5)
                        if st.session_state['user_type'] == 'pro':
                            st.success("✅ [Priority] Ticket logged. We will reply within 1 business day.")
                        else:
                            st.warning("✅ [Queue] Ticket logged. Standard response time: 1-3 business days.")

    # FAQ
    with st.expander("❓ FAQ / 常见问题"):
        st.markdown(f"""
        **Q: Is this a subscription?**
        A: No. It is a **One-Time Payment** of {PRICE_PRO}.
        
        **Q: Refund Policy?**
        A: **No Refunds** for digital products.
        
        **Q: PDF Text Issues?**
        A: Please submit a ticket if characters are missing.
        """)

# --- 主工作区 ---
st.title(f"{get_ui_text('title', app_lang)} v6.0")
st.caption(get_ui_text('tagline', app_lang))

# 引擎标识
if st.session_state['user_type'] == 'pro':
    st.markdown("##### 🚀 **Engine: Turbo Priority (Active)**")
else:
    st.markdown("##### 🐢 **Engine: Standard (Queue Active)**")

# 获取用量
usage = get_daily_usage(st.session_state['user_email'])
text_usage = usage['text_count']
image_usage = usage['image_count']

# 显示限额条
col_lim1, col_lim2 = st.columns(2)
with col_lim1:
    if st.session_state['user_type'] == 'pro':
        st.progress(0, text="Text: Unlimited (Fair Use)")
    else:
        st.progress(text_usage / LIMIT_TEXT_FREE, text=f"Text: {text_usage}/{LIMIT_TEXT_FREE}")
with col_lim2:
    if st.session_state['user_type'] == 'pro':
        st.progress(0, text=f"Image Vision: {image_usage}/{LIMIT_IMAGE_PRO}")
    else:
        st.progress(image_usage / LIMIT_IMAGE_FREE, text=f"Image Vision: {image_usage}/{LIMIT_IMAGE_FREE}")

st.markdown("---")

# 角色选择 (Grid Layout)
st.subheader(get_ui_text('role_select', app_lang))
role_cols = st.columns(6)
selected_role = None

# 使用 Session State 记住选择
if 'current_role' not in st.session_state:
    st.session_state['current_role'] = "Global Educator"

for i, role_name in enumerate(ROLES.keys()):
    with role_cols[i]:
        if st.button(role_name.split()[1], key=f"role_{i}", help=role_name, use_container_width=True):
            st.session_state['current_role'] = role_name

st.info(f"🎭 **Current Role:** {st.session_state['current_role']}")

# 动态输入表单
col1, col2 = st.columns([1, 1])

with col1:
    # 模式选择锁
    available_modes = ROLES[st.session_state['current_role']]
    # 免费用户只看第1个模式，其他的显示锁
    mode_options = []
    if st.session_state['user_type'] == 'pro':
        mode_options = available_modes
    else:
        mode_options = [available_modes[0]] + [f"🔒 {m} (PRO)" for m in available_modes[1:]]
    
    selected_mode = st.selectbox("Select Mode", mode_options)
    
    # 拦截模式选择
    if "🔒" in selected_mode:
        st.warning(f"⚠️ **PRO Feature Locked**\n\nUnlock all 18 modes for just {PRICE_PRO}.")
        st.stop() # 停止渲染后续

    # 输出语言 (Pro 15 vs Free 3)
    out_lang_opts = LANG_ALL if st.session_state['user_type'] == 'pro' else LANG_FREE
    output_lang = st.selectbox("🌐 Output Language", out_lang_opts)

with col2:
    # 上传组件 (Free 1 vs Pro 50)
    is_multi = True if st.session_state['user_type'] == 'pro' else False
    upload_limit_msg = "Batch limit: 50 files" if is_multi else "Batch limit: 1 file (PRO: 50)"
    uploaded_files = st.file_uploader(
        get_ui_text('upload_label', app_lang), 
        accept_multiple_files=is_multi,
        help=upload_limit_msg
    )

# 输入框
input_topic = st.text_area("✍️ Input Topic / Details", placeholder="Enter your topic here...")

# 生成按钮逻辑
if st.button(get_ui_text('gen_btn', app_lang), type="primary", use_container_width=True):
    
    # 1. 检查限额 (含图算图逻辑)
    has_image = uploaded_files is not None and len(uploaded_files) > 0
    
    allow_gen = False
    
    if st.session_state['user_type'] == 'pro':
        # PRO 检查
        if has_image and image_usage >= LIMIT_IMAGE_PRO:
             st.error("Fair use limit reached for images (200/day).")
        else:
             allow_gen = True
    else:
        # FREE 检查
        if has_image:
            if image_usage >= LIMIT_IMAGE_FREE:
                st.error(f"🖼️ **Image Limit Reached ({LIMIT_IMAGE_FREE}/{LIMIT_IMAGE_FREE})**\n\nUpgrade to PRO for 200 images/day!")
            else:
                allow_gen = True
        else:
            if text_usage >= LIMIT_TEXT_FREE:
                st.error(f"🔒 **Daily Limit Reached ({LIMIT_TEXT_FREE}/{LIMIT_TEXT_FREE})**\n\nTomorrow is another day, or Upgrade Now!")
            else:
                allow_gen = True

    if allow_gen:
        # 2. 扣费
        update_type = "image" if has_image else "text"
        update_usage(st.session_state['user_email'], update_type)
        
        # 3. 模拟等待剧场 (Waiting Theater)
        status_box = st.status("🚀 Initializing...", expanded=True)
        
        if st.session_state['user_type'] == 'pro':
            # Turbo 模式
            time.sleep(0.5)
            status_box.update(label=get_ui_text('turbo_msg', app_lang), state="complete")
        else:
            # Standard 模式 (戏要做足)
            status_box.write(get_ui_text('queue_msg', app_lang))
            progress_bar = status_box.progress(0)
            
            tips = [
                "💡 Tip: PRO users skip this queue instantly.",
                "🧠 Analyzing logic vectors...",
                f"⏳ High traffic. Position #{random.randint(50,150)}..."
            ]
            
            for i in range(100):
                time.sleep(0.04) # 约 4 秒
                progress_bar.progress(i + 1)
                if i % 30 == 0:
                    status_box.write(random.choice(tips))
            
            status_box.update(label="✅ Generation Complete", state="complete")

        # 4. 生成内容 (Mock Engine with Super Dictionary)
        # 简单模拟不同语言的输出结构
        mock_content = ""
        
        if output_lang == "Russian":
            mock_content = f"""# {st.session_state['current_role']} (Russian Edition)\n\n## Введение\nВот контент для: {input_topic}\n\n## Ключевые моменты\n1. Пункт первый\n2. Пункт второй\n\n## Заключение\nСпасибо."""
        elif output_lang == "Bahasa Melayu":
            mock_content = f"""# {st.session_state['current_role']} (Malay Edition)\n\n## Pengenalan\nBerikut adalah konten untuk: {input_topic}\n\n## Isi Penting\n1. Poin pertama\n2. Poin kedua\n\n## Kesimpulan\nTerima kasih."""
        elif output_lang == "简体中文":
             mock_content = f"""# {st.session_state['current_role']} (中文版)\n\n## 简介\n这是关于 {input_topic} 的内容生成。\n\n## 关键点\n1. 第一点\n2. 第二点\n\n## 总结\n希望这对您有帮助。"""
        else:
             mock_content = f"""# {st.session_state['current_role']} (English)\n\n## Introduction\nHere is the generated content for: {input_topic}\n\n## Key Points\n1. First point\n2. Second point\n\n## Conclusion\nHope this helps."""

        # 免费版水印
        if st.session_state['user_type'] != 'pro':
            mock_content += "\n\n---\n🔒 [Trial Version - Generated by PromptLab AI v6.0]"
        
        # 存入 Session 用于展示
        st.session_state['result'] = mock_content
        st.rerun() # 刷新以更新额度条

# ==========================================
# 5. 结果展示与 5层操作塔 (5-LAYER DECK)
# ==========================================
if 'result' in st.session_state:
    st.markdown("### 🎉 Generated Result")
    st.text_area("Output", value=st.session_state['result'], height=300)
    
    # Layer 1: Action Core
    st.button(get_ui_text('copy_btn', app_lang), use_container_width=True, type="primary")
    
    # Layer 2: AI Direct Connect
    st.caption("🤖 **Layer 2: AI Direct Connect**")
    ai_cols = st.columns(9)
    ai_links = [
        ("Gemini", "https://gemini.google.com"), ("ChatGPT", "https://chat.openai.com"),
        ("Claude", "https://claude.ai"), ("Perplexity", "https://www.perplexity.ai"),
        ("Grok", "https://x.com"), ("SD", "https://stablediffusionweb.com"),
        ("MJ", "https://discord.com"), ("Notion", "https://notion.so"), ("Canva", "https://canva.com")
    ]
    for i, (name, link) in enumerate(ai_links):
        with ai_cols[i]:
            st.link_button(name, link)

    # Layer 3: Social Deck
    st.caption("📤 **Layer 3: Social Share**")
    soc_cols = st.columns(6)
    with soc_cols[0]:
        if st.session_state['user_type'] == 'pro':
            st.button("🟢 WeChat")
        else:
            st.button("🔒 WeChat", disabled=True, help="Upgrade to PRO to unlock System Share")
    with soc_cols[1]:
        st.button("📤 System")
    with soc_cols[2]:
        st.link_button("WhatsApp", f"https://wa.me/?text={st.session_state['result'][:100]}")
    
    # Layer 4: App Portals
    st.caption("📱 **Layer 4: App Portals (Copy & Go)**")
    app_cols = st.columns(3)
    with app_cols[0]: st.link_button("Instagram", "https://instagram.com")
    with app_cols[1]: st.link_button("📕 XiaoHongShu", "https://xiaohongshu.com")
    with app_cols[2]: st.link_button("TikTok", "https://tiktok.com")

    # Layer 5: Utility Deck (Download)
    st.caption("💾 **Layer 5: Downloads**")
    dl_cols = st.columns(3)
    
    # TXT 下载
    b64_txt = base64.b64encode(st.session_state['result'].encode()).decode()
    dl_cols[0].markdown(f'<a href="data:file/txt;base64,{b64_txt}" download="prompt.txt"><button style="width:100%">📄 Download TXT</button></a>', unsafe_allow_html=True)
    
    # PDF 下载 (锁)
    with dl_cols[1]:
        if st.session_state['user_type'] == 'pro':
            # 生成 PDF
            try:
                pdf_bytes = generate_pdf(st.session_state['result'])
                b64_pdf = base64.b64encode(pdf_bytes).decode()
                st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="prompt.pdf"><button style="width:100%">📕 Download PDF</button></a>', unsafe_allow_html=True)
            except Exception as e:
                st.error("Font Error")
        else:
            if st.button("🔒 PDF (PRO)"):
                st.error(f"💎 Upgrade to {PRICE_PRO} to unlock clean PDF downloads.")

    # CSV 下载 (锁)
    with dl_cols[2]:
         if st.session_state['user_type'] == 'pro':
             st.button("📊 Download CSV")
         else:
             st.button("🔒 CSV (PRO)", disabled=True)

# ==========================================
# 6. 页脚 (FOOTER)
# ==========================================
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: grey; font-size: 12px;'>{get_ui_text('footer', app_lang)}</div>", unsafe_allow_html=True)