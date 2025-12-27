import streamlit as st
import time
import json
import datetime
import base64
import os
import random

# ==========================================
# 1. 核心配置与样式 (Configuration & CSS)
# ==========================================
st.set_page_config(
    page_title="PromptLab AI V7.3 Ultimate",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 商业规则常量
PRICE_PRO = "$12.90"
PRICE_OLD = "$39.90"
BUY_LINK = "https://promptlab.lemonsqueezy.com/checkout"  # 替换您的链接
LIMIT_TEXT_FREE = 5
LIMIT_IMAGE_FREE = 3
LIMIT_IMAGE_PRO = 200
UPLOAD_BATCH_FREE = 1
UPLOAD_BATCH_PRO = 50

# 自定义样式 (红色边框广告 + 按钮美化)
st.markdown("""
<style>
    /* 红色边框广告 */
    .sticky-ad {
        border: 2px solid #ff4b4b;
        background-color: #fff5f5;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .ad-price { font-size: 24px; color: #ff4b4b; font-weight: 800; }
    .ad-old { text-decoration: line-through; color: #888; font-size: 14px; }
    .ad-btn {
        background-color: #ff4b4b; color: white;
        padding: 8px 20px; border-radius: 5px;
        text-decoration: none; font-weight: bold;
        display: block; margin-top: 10px;
    }
    .ad-btn:hover { background-color: #e00000; color: white; }
    
    /* 状态条样式 */
    .stProgress > div > div > div > div { background-color: #2E86C1; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 终极数据字典 (The Master Database)
#    包含了 6 角色、18 模式、144+ 选项
# ==========================================
LANG_FREE = ["English", "Español", "简体中文"]
LANG_PRO = ["English", "简体中文", "Bahasa Melayu", "Español", "Russian", "Japanese", "Korean", "French", "German", "Indonesian", "Thai", "Vietnamese", "Arabic", "Tamil", "Portuguese"]

COMMON_TONES = ["🌟 Professional", "🥰 Empathetic", "🔥 Persuasive", "👻 Witty", "📖 Storyteller", "⚡ Urgent", "🧘 Calm", "🎓 Academic"]

# 完整数据结构：Role -> Mode -> {Options, Tones, InputType}
MODES_DB = {
    "Global Educator": {
        "🟢 Pedagogy": { 
            "dd": ["📸 Analyze Student Work", "Direct Instruction", "Gamification", "Project-Based Learning (PBL)", "Socratic Method", "Flipped Classroom", "Differentiated Instruction"], 
            "tones": COMMON_TONES, 
            "input_type": "text", # 默认为文本，若选项含 📸 会自动覆盖为传图
            "desc": "Generate lesson plans & teaching strategies." 
        },
        "🔵 Visuals": { 
            "dd": ["Pixar/Disney 3D", "National Geographic Photo", "Minimalist Vector", "Vintage Watercolor", "Scientific Schematic", "Cyberpunk Concept"], 
            "input_type": "visual_desc", 
            "desc": "Create educational visual prompts (Midjourney/SD)." 
        },
        "🟣 Comm": { 
            "dd": ["Parent Message", "Behavior Report", "Official Proposal", "Classroom Newsletter", "Event Invitation", "Grant Application"], 
            "tones": ["🥰 Empathetic", "🌟 Professional", "⚡ Urgent"], 
            "input_type": "text", 
            "desc": "Draft professional emails & notices." 
        }
    },
    "Global Creator": {
        "🟢 Scripting": { 
            "dd": ["📸 Visual-to-Script", "TikTok/Reels (Hook-Value-CTA)", "YouTube Edutainment", "Storytelling Vlog", "Podcast Interview", "Live Stream Flow"], 
            "tones": ["🔥 Persuasive", "👻 Witty", "🤩 Hype"], 
            "input_type": "text", 
            "desc": "Video scripts & flow structures." 
        },
        "🔵 Thumbnail": { 
            "dd": ["High CTR (Shocked)", "Cinematic Poster", "Tech/Neon/Glowing", "Before & After", "Minimalist Apple", "Comic Book Style"], 
            "input_type": "visual_desc", 
            "desc": "Thumbnail art prompts." 
        },
        "🟣 Marketing": { 
            "dd": ["Xiaohongshu (KOC)", "Instagram Caption", "Facebook Ad", "LinkedIn Thought Leader", "Twitter Thread", "Email Newsletter"], 
            "tones": ["⚡ Urgent", "🤝 Friendly", "💼 Pro"], 
            "input_type": "text", 
            "desc": "Social media copy & ads." 
        }
    },
    "Global Parent": {
        "🟢 Story Time": { "dd": ["📸 From Child's Drawing", "Bedtime Story", "Hero's Journey", "Social Emotional Learning", "Science 'Why' Story", "Cultural Tale"], "tones": ["😴 Calming", "🦸 Exciting"], "input_type": "text", "desc": "Custom stories for kids." },
        "🔵 Activities": { "dd": ["DIY Craft Guide", "Rainy Day Game", "Kitchen Science", "Scavenger Hunt", "Family Bonding", "No-Screen Coding"], "tones": ["🎉 Fun", "🔬 Edu"], "input_type": "text", "desc": "Offline activity ideas." },
        "🟣 Tutor": { "dd": ["📸 Solve Problem", "Feynman Technique", "Homework Helper", "Quiz Generator", "Vocabulary Builder", "Essay Proofreader"], "tones": ["👩‍🏫 Encouraging", "🧠 Logical"], "input_type": "text", "desc": "Homework aid & tutoring." }
    },
    "Global Seller": {
        "🟢 Copywriting": { "dd": ["📸 Product Desc from Photo", "PAS (Pain-Agitate-Solve)", "AIDA (Attention-Action)", "FAB (Feature-Benefit)", "Storytelling Sales", "Objection Handling"], "tones": ["🔥 Persuasive", "💼 Trustworthy"], "input_type": "text", "desc": "Sales pages & ads." },
        "🔵 Product Shot": { "dd": ["Studio White BG", "Lifestyle Home", "Luxury Gold/Black", "Nature/Sunlight", "Cyberpunk/Tech", "Flat Lay"], "input_type": "visual_desc", "desc": "E-commerce photography prompts." },
        "🟣 Support": { "dd": ["Apology & Recovery", "Review Request", "Complaint Reply", "Promo Announcement", "Crisis Statement", "FAQ Gen"], "tones": ["🤝 Apologetic", "🌟 Professional"], "input_type": "text", "desc": "Customer service scripts." }
    },
    "Global Student": {
        "🟢 Study": { "dd": ["📸 Explain Chart", "Feynman Technique", "Lit Review Matrix", "Flashcard (Anki)", "Concept Simplifier", "Translation"], "tones": ["📚 Academic", "🤓 Simple"], "input_type": "text", "desc": "Study aids." },
        "🔵 Project": { "dd": ["Essay Outline", "Presentation Script", "Debate Prep", "Lab Report", "Methodology", "Group Roles"], "tones": COMMON_TONES, "input_type": "text", "desc": "Assignments & presentations." },
        "🟣 Career": { "dd": ["ATS Resume", "Cover Letter", "Interview Prep", "LinkedIn Bio", "Cold Email", "Portfolio Desc"], "tones": ["💼 Corporate", "🚀 Ambitious"], "input_type": "text", "desc": "Job hunting." }
    },
    "Global Corporate": {
        "🟢 Admin": { "dd": ["📸 Extract Data from Table", "Meeting Minutes", "Official Proposal", "Internal Memo", "SOP / Process", "Press Release"], "tones": ["⚡ Direct", "⚖️ Formal"], "input_type": "text", "desc": "Administrative tasks." },
        "🔵 Strategy": { "dd": ["OKRs", "SWOT Analysis", "Competitor Dive", "Business Canvas", "Risk Matrix", "Pitch Deck"], "input_type": "text", "desc": "Strategic planning." },
        "🟣 HR & Team": { "dd": ["Performance Review", "Job Desc (JD)", "Onboarding Plan", "Crisis Comms", "Team Building", "Termination"], "tones": ["⚖️ Fair", "🤝 Empathetic"], "input_type": "text", "desc": "Human resources." }
    }
}

# ==========================================
# 3. 工具函数 (Backend Logic)
# ==========================================
DB_FILE = 'user_db.json'

# --- 简单的本地数据库模拟 ---
def get_usage(email):
    # 实际项目中这里连接 SQL
    if not os.path.exists(DB_FILE): return {"date": str(datetime.date.today()), "text": 0, "image": 0}
    try:
        with open(DB_FILE, 'r') as f: db = json.load(f)
    except: return {"date": str(datetime.date.today()), "text": 0, "image": 0}
    
    today = str(datetime.date.today())
    if email not in db: db[email] = {"date": today, "text": 0, "image": 0}
    
    # 跨天重置逻辑
    if db[email]["date"] != today:
        db[email] = {"date": today, "text": 0, "image": 0}
        with open(DB_FILE, 'w') as f: json.dump(db, f)
        
    return db[email]

def update_usage(email, type="text"):
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as f: db = json.load(f)
        else: db = {}
    except: db = {}
    
    today = str(datetime.date.today())
    if email not in db: db[email] = {"date": today, "text": 0, "image": 0}
    
    db[email][type] += 1
    with open(DB_FILE, 'w') as f: json.dump(db, f)

# --- PDF 生成 (带字体回退) ---
def generate_pdf_bytes(text):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    
    # 字体检测
    font_path = 'font.ttf'
    has_font = os.path.exists(font_path)
    
    if has_font:
        try:
            pdf.add_font('CustomFont', '', font_path, uni=True)
            pdf.set_font('CustomFont', '', 12)
        except:
            pdf.set_font("Arial", size=12)
            text += "\n\n[Error: Font file corrupted. Rendered in Standard Mode.]"
    else:
        pdf.set_font("Arial", size=12)
        # 移除可能导致崩溃的非 ASCII 字符
        text = text.encode('latin-1', 'ignore').decode('latin-1')
        text += "\n\n[Note: font.ttf not found. Non-English characters removed.]"
        
    pdf.multi_cell(0, 10, txt=text)
    return pdf.output(dest='S').encode('latin-1')

# --- 验证逻辑 ---
def validate_key(key):
    # 后门 + 简单规则
    return key == "ADMIN-8888" or key.startswith("PRO")

# --- PASEC 动态引擎 (The Brain) ---
def generate_pasec(role, mode, option, tone, topic, files_count, lang):
    # 根据用户选择动态生成结构
    
    # S - Structure 逻辑分支
    if "Visual" in mode or "Thumbnail" in option or "Shot" in option:
        s_structure = """
* **Prompt Format**: `/imagine prompt: [Subject] + [Style Modifiers] + [Lighting/Camera] + --ar 16:9 --v 6.0`
* **Negative Prompt**: text, watermark, blurry, low quality.
"""
    elif "Script" in option or "Video" in option:
        s_structure = """
* **0:00-0:03**: The Hook (Grab attention).
* **0:03-0:30**: Value/Content (The 'Meat').
* **0:30-End**: CTA (Call to Action).
"""
    else:
        s_structure = """
1.  **Headline**: Engaging and relevant.
2.  **Key Points**: Bullet points for readability.
3.  **Summary/Action**: Clear next steps.
"""

    return f"""# {option} - Generated Prompt ({lang})

## 👤 P - Persona
**Role**: {role}
**Mode**: {mode}
**Tone**: {tone}

## 🎯 A - Aim
**Objective**: Create high-quality content for "{option}".
**Input Topic**: {topic}
**Language**: {lang}

## 📂 S - Structure
{s_structure}

## 📝 E - Effective (Constraints)
* Strictly follow the **{tone}** tone.
* Optimize for **{lang}** native speakers.
* Ensure professional output suitable for {role}.

## 💡 C - Context
* **Attachments**: Analyzed {files_count} reference files.
* **User Input**: "{topic[:50]}..."

---
**[AI Generation Output Starts Here]**
(Here is the specific content generated by the engine based on your request...)
"""

# ==========================================
# 4. 页面路由与状态 (State Management)
# ==========================================
if 'page' not in st.session_state: st.session_state['page'] = 'home'
if 'user_type' not in st.session_state: st.session_state['user_type'] = 'guest'
if 'user_email' not in st.session_state: st.session_state['user_email'] = 'Guest'

def navigate(page):
    st.session_state['page'] = page
    st.rerun()

# ==========================================
# 5. 全局侧边栏 (Sidebar Logic)
# ==========================================
def render_sidebar():
    with st.sidebar:
        # Logo
        if os.path.exists("logo.png"):
            st.image("logo.png", width=120)
        else:
            st.markdown("## 🤖 PromptLab")
        
        st.divider()
        
        # User Card
        is_pro = st.session_state['user_type'] == 'pro'
        badge = "💎 PRO Enterprise" if is_pro else "👤 Free Guest"
        engine = "🚀 Turbo (0.5s)" if is_pro else "🐢 Standard (Queue)"
        
        st.info(f"**{badge}**\n\nUser: {st.session_state['user_email']}\n\nEngine: {engine}")
        
        # Language Switcher
        langs = LANG_PRO if is_pro else LANG_FREE
        if 'global_lang' not in st.session_state: st.session_state['global_lang'] = "English"
        st.session_state['global_lang'] = st.selectbox("🌐 Language", langs, index=0)
        
        # 🔥 Sticky Ad (GUEST ONLY)
        if not is_pro:
            st.markdown("---")
            st.markdown(f"""
            <div class="sticky-ad">
                <div style="font-size:12px; font-weight:bold; color:#ff4b4b;">🔥 LIMITED TIME</div>
                <div class="ad-price">{PRICE_PRO}</div>
                <div class="ad-old">Was {PRICE_OLD}</div>
                <div style="font-size:13px; margin:5px 0;">Lifetime License • No Fees</div>
                <a href="{BUY_LINK}" target="_blank" class="ad-btn">👉 Get It Now</a>
            </div>
            """, unsafe_allow_html=True)
            
        st.divider()
        
        # 🎫 Smart Ticket
        with st.expander("🎫 Support Ticket"):
            sub = st.text_input("Subject")
            msg = st.text_area("Message")
            # AI 拦截
            block_words = ["refund", "money", "key", "code", "lost"]
            if any(w in sub.lower() for w in block_words):
                st.warning("🤖 **AI Auto-Reply:**\n\n- **Refunds:** Digital products are non-refundable.\n- **Lost Key:** Recover at LemonSqueezy.\n\n*Ticket intercepted.*")
            else:
                if st.button("Submit Ticket"):
                    st.success("✅ Priority Sent!" if is_pro else "✅ Queued (1-3 Days)")

        # 📚 FAQ (Knowledge Base)
        with st.expander("❓ FAQ / Policy"):
            st.markdown("""
            * **Refunds?** No. Final Sale.
            * **Hidden Fees?** None. One-time payment.
            * **Commercial Use?** Yes, for PRO users.
            * **PDF Glitch?** Known issue if font missing.
            """)
            
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

# ==========================================
# 6. 核心页面 (Pages)
# ==========================================

# --- Page 1: Home ---
def render_home():
    # 首页无侧边栏调用
    col1, col2 = st.columns([6,1])
    with col2:
        st.selectbox("🌐", ["English", "Español", "中文"], label_visibility="collapsed")
        
    st.markdown(f"<h1 style='text-align: center; font-size: 3em;'>PromptLab AI <span style='font-size:0.5em; vertical-align:top; color:#ff4b4b;'>V7.3</span></h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>The Ultimate Enterprise Prompt Engine</h3>", unsafe_allow_html=True)
    
    st.divider()
    
    c1, c2 = st.columns(2, gap="large")
    
    with c1:
        st.subheader("🔓 Login / Start")
        t1, t2 = st.tabs(["👤 Guest Trial", "💎 PRO Login"])
        
        with t1:
            email = st.text_input("Email", key="g_email")
            if st.button("🚀 Start Free Trial", use_container_width=True):
                st.session_state['user_type'] = 'guest'
                st.session_state['user_email'] = email if email else "Guest"
                navigate('roles')
                
        with t2:
            p_email = st.text_input("PRO Email", key="p_email")
            p_key = st.text_input("License Key", type="password")
            if st.button("💎 Verify & Login", use_container_width=True):
                if validate_key(p_key):
                    st.session_state['user_type'] = 'pro'
                    st.session_state['user_email'] = p_email
                    navigate('roles')
                else:
                    st.error("Invalid License Key")
                    
    with c2:
        st.subheader("🆚 Why PRO?")
        st.markdown(f"""
        | Feature | 👤 Free Guest | 💎 PRO ({PRICE_PRO}) |
        | :--- | :--- | :--- |
        | **Engine** | 🐢 Standard | 🚀 **Turbo Priority** |
        | **Text Limit** | 🔒 {LIMIT_TEXT_FREE} / Day | ✅ **Unlimited** |
        | **Image Limit** | 🔒 {LIMIT_IMAGE_FREE} / Day | ✅ **Max {LIMIT_IMAGE_PRO}** |
        | **Modes** | 🔒 Lock Mode 2&3 | ✅ **Unlock All 18** |
        | **Uploads** | 🔒 1 File | ✅ **Batch 50** |
        | **Export** | 🔒 Watermark | ✅ **Clean PDF/CSV** |
        """)
        with st.expander("🔍 Click for Specs"):
            st.caption("Includes: 15 Languages, 144+ Options, Commercial Rights.")

# --- Page 2: Role Hall ---
def render_roles():
    render_sidebar() # 呼叫侧边栏
    
    st.button("⬅️ Back to Home", on_click=lambda: navigate('home'))
    st.title("🎭 Role Hall")
    st.markdown("Select your professional identity to load specific neural contexts.")
    
    cols = st.columns(3)
    roles = list(MODES_DB.keys())
    
    for i, role in enumerate(roles):
        with cols[i % 3]:
            # 渲染大卡片按钮
            if st.button(f"✨ {role}", key=role, use_container_width=True, type="secondary"):
                st.session_state['current_role'] = role
                navigate('workspace')
            
            # 显示该角色下的模式预览
            modes_preview = ", ".join(list(MODES_DB[role].keys()))
            st.caption(f"Modes: {modes_preview}")
            st.markdown("---")

# --- Page 3: Workspace (The Core) ---
def render_workspace():
    render_sidebar() # 呼叫侧边栏
    
    # 获取用户状态
    role = st.session_state['current_role']
    is_pro = st.session_state['user_type'] == 'pro'
    usage = get_usage(st.session_state['user_email'])
    
    # 顶部导航
    c_nav1, c_nav2 = st.columns([1, 5])
    with c_nav1:
        st.button("⬅️ Change Role", on_click=lambda: navigate('roles'))
    with c_nav2:
        st.success(f"🛠️ **{role}** | Mode: {'💎 PRO' if is_pro else '👤 GUEST'}")

    # 额度条
    limit_txt = "Unl." if is_pro else LIMIT_TEXT_FREE
    limit_img = LIMIT_IMAGE_PRO if is_pro else LIMIT_IMAGE_FREE
    
    c1, c2 = st.columns(2)
    with c1: st.progress(0 if is_pro else min(usage['text']/LIMIT_TEXT_FREE, 1.0), f"Text Usage: {usage['text']}/{limit_txt}")
    with c2: st.progress(min(usage['image']/limit_img, 1.0), f"Image Usage: {usage['image']}/{limit_img}")
    
    st.divider()
    
    # === 核心操作区 ===
    role_data = MODES_DB[role]
    mode_keys = list(role_data.keys())
    
    # 1. 模式选择器 (带锁)
    # 免费用户只能看第一个模式，其他加锁
    display_modes = mode_keys if is_pro else [mode_keys[0]] + [f"🔒 {m} (PRO)" for m in mode_keys[1:]]
    
    c_in1, c_in2 = st.columns([1, 1])
    
    with c_in1:
        sel_mode_raw = st.selectbox("Select Mode", display_modes)
        
        # 拦截锁定的模式
        if "🔒" in sel_mode_raw:
            st.error(f"⚠️ This mode is locked for Guests. Please Upgrade to {PRICE_PRO}.")
            st.stop() # 停止渲染下方组件
            
        real_mode = sel_mode_raw # 真实模式名
        mode_config = role_data[real_mode]
        
        # 2. 选项选择器 (144+ Options)
        # PRO用户有 Custom 选项
        options = mode_config['dd'] + (["✨ Custom Input..."] if is_pro else [])
        sel_option = st.selectbox("Select Specific Option", options)
        
        # 3. 语气选择 (如果有)
        if "tones" in mode_config:
            sel_tone = st.selectbox("Tone / Style", mode_config['tones'])
        else:
            sel_tone = "Standard"

    with c_in2:
        # 4. 上传区 (带锁)
        # 判断是否是图片模式或选项包含 📸
        is_visual = mode_config['input_type'] == 'visual_desc' or "📸" in sel_option
        
        upload_limit = UPLOAD_BATCH_PRO if is_pro else UPLOAD_BATCH_FREE
        upload_label = f"Upload Context (Max {upload_limit})"
        
        uploaded_files = st.file_uploader(upload_label, accept_multiple_files=is_pro, key="uploader")
        
        if uploaded_files and not is_pro and len(uploaded_files) > 1:
            st.warning("⚠️ Free limit: 1 file. Only the first file will be processed.")
    
    # 5. 动态输入框 (Smart Input)
    # 根据选项变化 placeholder
    ph_text = "Enter details..."
    if "📸" in sel_option: ph_text = "📸 Describe what you want to analyze in the image..."
    elif is_visual: ph_text = "🎨 Describe the scene, lighting, and style..."
    elif "Story" in sel_option: ph_text = "📖 Enter child's name, age, and interests..."
    
    user_input = st.text_area("Input Details", placeholder=ph_text, height=150)
    
    # === 生成按钮逻辑 ===
    if st.button("✨ Generate Prompt (PASEC)", type="primary", use_container_width=True):
        
        # 检查额度
        allow_gen = False
        if is_pro:
            allow_gen = True
        else:
            # 免费限制检查
            if is_visual and usage['image'] >= LIMIT_IMAGE_FREE:
                st.error(f"❌ Daily Image Limit Reached ({LIMIT_IMAGE_FREE})")
            elif not is_visual and usage['text'] >= LIMIT_TEXT_FREE:
                st.error(f"❌ Daily Text Limit Reached ({LIMIT_TEXT_FREE})")
            else:
                allow_gen = True
        
        if allow_gen:
            # 扣费
            update_usage(st.session_state['user_email'], "image" if is_visual else "text")
            
            # 等待剧场
            with st.status("🚀 Processing...", expanded=True) as status:
                if is_pro:
                    time.sleep(0.5) # 极速
                    status.update(label="🚀 Turbo Engine: Done!", state="complete")
                else:
                    status.write("🐢 Connecting to Standard Queue...")
                    my_bar = status.progress(0)
                    for i in range(100):
                        time.sleep(0.03) # 模拟3秒
                        my_bar.progress(i+1)
                        if i == 50: status.write("💡 Tip: PRO users skip this wait...")
                    status.update(label="✅ Done!", state="complete")
            
            # 调用 PASEC 引擎
            res = generate_pasec(role, real_mode, sel_option, sel_tone, user_input, len(uploaded_files) if uploaded_files else 0, st.session_state['global_lang'])
            
            # 水印逻辑
            if not is_pro:
                res += f"\n\n---\n🔒 Generated by PromptLab Free Trial. Upgrade to remove watermark."
                
            st.session_state['result'] = res
            st.rerun()

    # === 结果展示与 5层塔 ===
    if 'result' in st.session_state:
        st.divider()
        st.subheader("🎉 Result")
        st.text_area("Output", st.session_state['result'], height=350)
        
        # Layer 1: Copy
        st.button("📋 Copy Result (Click to Copy)", use_container_width=True)
        
        # Layer 2: AI Connect
        st.caption("🤖 **AI Direct Connect:**")
        cols_ai = st.columns(6)
        ai_links = ["Gemini", "ChatGPT", "Claude", "Perplexity", "Midjourney", "Canva"]
        for i, al in enumerate(ai_links):
            cols_ai[i].button(al)
            
        # Layer 3: Social
        st.caption("📤 **Social Share:**")
        cols_soc = st.columns(4)
        with cols_soc[0]: 
            st.button("🟢 WeChat", disabled=not is_pro, help="PRO Only")
        with cols_soc[1]: st.button("📤 System")
        with cols_soc[2]: st.link_button("WhatsApp", "https://wa.me")
        
        # Layer 4: Apps
        st.caption("📱 **App Portals:**")
        cols_app = st.columns(3)
        cols_app[0].link_button("Instagram", "https://instagram.com")
        cols_app[1].link_button("📕 XiaoHongShu", "https://xiaohongshu.com")
        cols_app[2].link_button("TikTok", "https://tiktok.com")
        
        # Layer 5: Download (The Paywall Final Boss)
        st.caption("💾 **Downloads:**")
        d1, d2, d3 = st.columns(3)
        
        # TXT (Free allowed)
        b64_txt = base64.b64encode(st.session_state['result'].encode()).decode()
        d1.markdown(f'<a href="data:file/txt;base64,{b64_txt}" download="prompt.txt"><button style="width:100%; border-radius:5px; border:1px solid #ddd;">📄 TXT</button></a>', unsafe_allow_html=True)
        
        # PDF (PRO Only)
        with d2:
            if is_pro:
                pdf_bytes = generate_pdf_bytes(st.session_state['result'])
                b64_pdf = base64.b64encode(pdf_bytes).decode()
                st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="prompt.pdf"><button style="width:100%; border-radius:5px; border:1px solid #ddd;">📕 PDF</button></a>', unsafe_allow_html=True)
            else:
                st.button("🔒 PDF (PRO)", disabled=True)
                
        # CSV (PRO Only)
        with d3:
            if is_pro:
                st.button("📊 CSV")
            else:
                st.button("🔒 CSV (PRO)", disabled=True)

# ==========================================
# 7. 主程序入口
# ==========================================
if st.session_state['page'] == 'home':
    render_home()
elif st.session_state['page'] == 'roles':
    render_roles()
elif st.session_state['page'] == 'workspace':
    render_workspace()