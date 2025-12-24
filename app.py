import streamlit as st
import datetime
import urllib.parse
import base64

# ==========================================
# 1. 全局配置 & 样式 (Configuration)
# ==========================================
st.set_page_config(page_title="PromptLab AI", layout="wide", page_icon="🧠")

# CSS 样式优化 (隐藏默认菜单，美化按钮)
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 8px; }
    .stSelectbox { border-radius: 8px; }
    .reportview-container { background: #f0f2f6; }
    .big-font { font-size:20px !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 核心数据库 (DATABASE - NO PLACEHOLDERS)
# ==========================================

# A. 界面语言字典
LANG_DICT = {
    "English": {"login": "Login", "role": "Choose Role", "back": "Back", "logout": "Logout"},
    "简体中文": {"login": "登入", "role": "选择角色", "back": "返回", "logout": "退出"},
    "Bahasa Melayu": {"login": "Log Masuk", "role": "Pilih Peranan", "back": "Kembali", "logout": "Keluar"}
}

# B. 输出语言 (15种)
OUTPUT_LANGUAGES = [
    "English (Default)", "Malay (Bahasa Melayu)", "Chinese Simplified (简体中文)", 
    "Chinese Traditional (繁體中文)", "Tamil (தமிழ்)", "Arabic (العربية)", 
    "Japanese (日本語)", "Korean (한국어)", "Indonesian (Bahasa Indonesia)", 
    "Thai (ไทย)", "Vietnamese (Tiếng Việt)", "French (Français)", 
    "Spanish (Español)", "German (Deutsch)", "Russian (Русский)"
]

# C. FAQ 数据库 (完整内容)
FAQ_DB = {
    "💰 Billing & Payment": [
        ("Why is my card rejected?", "Please ensure your card allows international transactions."),
        ("How do I cancel?", "Go to Sidebar > Manage Subscription to cancel anytime."),
        ("Is the $12.90 price permanent?", "Yes, if you subscribe now, you lock in this price forever.")
    ],
    "⚙️ Technical Issues": [
        ("The screen is blank?", "Try clearing your browser cache or use Chrome."),
        ("I lost my activation key?", "Click the 'Lost Key' button in the sidebar.")
    ],
    "🧠 Usage Tips": [
        ("How to get better prompts?", "Be specific in the input box. Add age, context, and tone."),
        ("Can I use this for commercial?", "Yes, all generated prompts belong to you.")
    ]
}

# D. V25.0 核心大脑数据 (完整版 - 含 STEM & Social)
MODES_DB = {
    "Global Educator": {
        "🟢 Pedagogy": {
            "dd": ["Direct Instruction (Standard)", "Gamification (Engagement)", "Socratic Method (Deep Thinking)", "Project-Based Learning (PBL)", "Differentiated Instruction (Mixed Ability)", "STEAM Education (Interdisciplinary)", "Flipped Classroom (Active Learning)", "Inquiry-Based Learning (Exploration)"], 
            "in": "Topic & Student Level (e.g. Photosynthesis, Year 4)", 
            "desc": "Generate structured Lesson Plans & Teaching Strategies."
        },
        "🔵 Visuals": {
            "dd": ["Pixar 3D Style (Cute)", "Line Art (Coloring Page)", "Realistic Photography", "Infographic / Educational Poster", "Watercolor Art (Soft)", "Scientific Schematic (Anatomy/Tech)", "Historical Archival Style", "Paper Cutout / Collage Style"], 
            "in": "Visual Description (e.g. Ant scientist holding test tube)", 
            "desc": "Generate AI Art Prompts for teaching materials."
        },
        "🟣 Comm & Social": {
            "dd": ["Student Work Showcase (FB/IG Caption)", "Classroom Activity Highlight (Fun)", "Teaching Reflection / LinkedIn Post", "WhatsApp Message (Parent Group)", "Formal Proposal / Official Letter", "Behavior Report to Parent (Private)", "Speech Script (Assembly/Event)", "Classroom Newsletter (Weekly Update)"], 
            "in": "Context / Image Description (e.g. Photo of Ali's robot project)", 
            "desc": "Generate Letters, Announcements & Social Media Posts."
        }
    },
    "Global Creator": {
        "🟢 Scripting": {
            "dd": ["TikTok/Reels (15-60s)", "YouTube Tutorial (Long Form)", "Live Stream Sales Script", "Storytelling / Vlog Voiceover", "Podcast Outline", "Unboxing / Product Review", "Teaser / Movie Trailer Script", "Comedy Skit / Parody"], 
            "in": "Video Topic / Hook (e.g. Reviewing the new iPhone)", 
            "desc": "Generate Video Scripts & Storyboards."
        },
        "🔵 Thumbnail": {
            "dd": ["High CTR (Shocked Expression)", "Aesthetic (Instagram/Pinterest)", "Cinematic / Movie Poster", "Tech / Futuristic / Neon", "Minimalist / Clean", "Before & After Comparison", "Typography Heavy (Big Text)", "Comic Book / Pop Art Style"], 
            "in": "Image Scenario (e.g. Dirty sneakers vs Clean sneakers)", 
            "desc": "Generate High-Click-Rate Cover Art Prompts."
        },
        "🟣 Marketing": {
            "dd": ["Xiaohongshu (Emoji/Soft Sell)", "Facebook Ad (Hard Sell)", "Instagram Caption (Lifestyle)", "LinkedIn Thought Leadership", "Twitter/X Thread", "SEO Blog Post (Long Form)", "Email Newsletter Sequence", "Press Release (Official Launch)"], 
            "in": "Product / Service (e.g. AI Course Launch)", 
            "desc": "Generate Social Media Copy & Hashtags."
        }
    },
    "Global Parent": {
        "🟢 Story Time": {
            "dd": ["Bedtime Story (Calming)", "Behavior Correction (Moral Lesson)", "Personalized Hero Adventure", "Fable / Folklore Retelling", "Science / Educational Story", "Social Skills (Sharing/Empathy)", "Choose Your Own Adventure", "Cultural Heritage Story"], 
            "in": "Child Name, Age & Theme (e.g. Ali, 5, learning to share)", 
            "desc": "Generate Personalized Stories for Kids."
        },
        "🔵 Activities": {
            "dd": ["Coloring Page Prompt", "DIY Craft Guide (Step-by-Step)", "Indoor Game Idea (No Props)", "Science Experiment (Safe)", "Outdoor Scavenger Hunt", "Kitchen Math/Cooking Recipe", "Origami / Paper Folding Guide", "Coding Without Computer (Unplugged)"], 
            "in": "Interest / Theme (e.g. Dinosaurs / Rainy Day)", 
            "desc": "Generate Fun Activities & Visual Prompts."
        },
        "🟣 Tutor": {
            "dd": ["Explain like I'm 5 (ELI5)", "Step-by-Step Solution Guide", "Quiz / Spelling Generator", "Vocabulary List (Bilingual)", "Creative Writing Prompt", "Math Word Problem Generator", "Science Concept Visualizer", "Debate Topic & Arguments"], 
            "in": "Subject / Question (e.g. Water Cycle)", 
            "desc": "Homework Helper & Private Tutor."
        }
    },
    "Global Seller": {
        "🟢 Copywriting": {
            "dd": ["PAS (Pain-Agitate-Solution)", "AIDA (Attention-Interest-Desire-Action)", "FAB (Features-Advantages-Benefits)", "Storytelling (Soft Sell)", "FAQ Generator", "SEO Product Description", "Brand Story / About Us", "Landing Page Headline Generator"], 
            "in": "Product Name & USP (e.g. Organic Soap)", 
            "desc": "Generate High-Conversion Sales Copy."
        },
        "🔵 Product Shot": {
            "dd": ["Studio White Background", "Lifestyle (Home/Cozy)", "Luxury (Gold/Marble)", "Nature / Outdoor / Sunlight", "Cyberpunk / Neon / Tech", "Flat Lay (Knolling Style)", "Model Wearing/Using Product", "Macro Close-Up (Texture Detail)"], 
            "in": "Product Item (e.g. Leather Watch Strap)", 
            "desc": "Generate Product Photography Background Prompts."
        },
        "🟣 Support": {
            "dd": ["Apology Letter (Delay/Defect)", "Review Request (5-Star)", "Reply to Angry Complaint", "Promotion / Sale Announcement", "Onboarding / Welcome Message", "Crisis Management Statement", "Customer Survey Questions", "Terms & Conditions Draft"], 
            "in": "Issue / Context (e.g. System outage)", 
            "desc": "Generate Professional Customer Service Replies."
        }
    },
    "Global Student": {
        "🟢 Study": {
            "dd": ["Summarizer (Bullet Points)", "Simplifier (Easy English)", "Flashcard Maker", "Translator (Bilingual)", "Grammar Checker & Fixer", "Code Explainer / Debugger", "Mind Map Structure Generator", "Exam Question Predictor"], 
            "in": "Text / Topic (e.g. Python Loop Error)", 
            "desc": "Study Notes & Revision Assistant."
        },
        "🔵 Project": {
            "dd": ["Essay Outline Structure", "Idea Brainstorming", "Presentation Script", "Citation / Reference Helper", "Thesis Statement Generator", "Lab Report Generator (STEM)", "Data Analysis / Interpretation", "Group Work Roles Assigner"], 
            "in": "Assignment Topic (e.g. Titration Experiment)", 
            "desc": "Assignment & Project Helper."
        },
        "🟣 Career": {
            "dd": ["Resume / CV Builder", "Cover Letter Writer", "Interview Prep (Q&A)", "LinkedIn Bio Optimization", "Cold Email for Internship", "Portfolio Description Writer", "Networking Message (Alumni)", "Scholarship Application Essay"], 
            "in": "Job Role / Experience (e.g. Engineering Intern)", 
            "desc": "Job Application & Interview Prep."
        }
    },
    "Global Corporate": {
        "🟢 Admin": {
            "dd": ["Meeting Minutes Formatter", "Email Drafter (Professional)", "Proposal Outline", "Internal Memo / Announcement", "Report Summarizer", "Meeting Agenda Setter", "Project Timeline / Roadmap", "Excel Formula Generator"], 
            "in": "Rough Notes / Context (e.g. Budget planning)", 
            "desc": "Office Tasks & Documentation."
        },
        "🔵 Strategy": {
            "dd": ["SWOT Analysis", "Competitor Analysis", "Business Model Canvas", "OKRs Generator", "Risk Assessment", "PESTLE Analysis (Macro)", "Value Proposition Canvas", "Market Entry Strategy"], 
            "in": "Business Topic / Company (e.g. AI Startup)", 
            "desc": "Business Insights & Strategic Planning."
        },
        "🟣 HR & Team": {
            "dd": ["Job Description (JD)", "Team Building Activity Idea", "Performance Review Writer", "Onboarding Plan (New Hire)", "Resignation Acceptance Letter", "Interview Question Generator", "Employee Satisfaction Survey", "Conflict Resolution Script"], 
            "in": "Role / Situation (e.g. Resolving team conflict)", 
            "desc": "HR Management & Team Culture."
        }
    }
}

# ==========================================
# 3. 辅助函数 (Helper Functions)
# ==========================================

# 模拟生成下载链接的函数
def get_text_download_link(text, filename="prompt.txt"):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download .TXT</a>'

# 模拟生成 WhatsApp 分享链接
def get_whatsapp_link(text):
    encoded_text = urllib.parse.quote(text)
    return f"https://wa.me/?text={encoded_text}"

# ==========================================
# 4. 页面逻辑 (Page Logic)
# ==========================================

# 初始化 State
if 'page' not in st.session_state: st.session_state.page = 1
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'current_role' not in st.session_state: st.session_state.current_role = ""
if 'generated_result' not in st.session_state: st.session_state.generated_result = ""

# ----------------------------
# PAGE 1: LOGIN (登入)
# ----------------------------
if st.session_state.page == 1:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🧠 PromptLab AI</h1>", unsafe_allow_html=True)
        
        # 语言选择
        lang_choice = st.selectbox("🌐 Interface Language / 界面语言", list(LANG_DICT.keys()))
        labels = LANG_DICT.get(lang_choice, LANG_DICT["English"])

        with st.form("login_form"):
            st.markdown("### Welcome Back / 欢迎回来")
            email = st.text_input("📧 Email Address")
            key = st.text_input("🔑 Activation Key", type="password")
            
            if st.form_submit_button(f"🚀 {labels['login']}"):
                if "@" in email and key: # 简单验证
                    st.session_state.user_email = email
                    st.session_state.page = 2
                    st.rerun()
                else:
                    st.error("❌ Invalid Email or Missing Key.")

# ----------------------------
# PAGE 2: ROLE SELECTION (角色)
# ----------------------------
elif st.session_state.page == 2:
    # Top Bar
    c1, c2 = st.columns([1, 4])
    if c1.button("⬅️ Back"):
        st.session_state.page = 1
        st.rerun()
    
    st.markdown(f"### 👋 Hi, {st.session_state.user_email}")
    st.markdown("## Choose your Workspace / 选择您的工作区")
    st.markdown("---")

    # Grid Display for Roles
    roles = list(MODES_DB.keys())
    col1, col2, col3 = st.columns(3)
    
    for i, role in enumerate(roles):
        with [col1, col2, col3][i % 3]:
            # 显示大按钮
            if st.button(f"🎭\n{role}", key=f"role_{i}", use_container_width=True):
                st.session_state.current_role = role
                st.session_state.page = 3
                st.rerun()

# ----------------------------
# PAGE 3: DASHBOARD (主控台)
# ----------------------------
elif st.session_state.page == 3:
    
    # === 左侧边栏 (SIDEBAR) ===
    with st.sidebar:
        st.info(f"👤 {st.session_state.user_email}")
        
        # A. 语言 & 设置
        st.selectbox("Display Language", list(LANG_DICT.keys()))
        
        # B. 付费升级
        st.markdown("---")
        st.markdown("### 💎 PRO Plan")
        st.markdown("<span style='text-decoration: line-through; color: red;'>$39.90</span>", unsafe_allow_html=True)
        st.markdown("**$12.90 / month**")
        st.button("💳 Upgrade Now")
        
        # C. FAQ (分类显示)
        with st.expander("❓ FAQ / Help"):
            faq_cats = st.selectbox("Category", list(FAQ_DB.keys()))
            for q, a in FAQ_DB[faq_cats]:
                st.markdown(f"**Q: {q}**")
                st.markdown(f"A: {a}")
                st.markdown("---")
        
        # D. Ticket Form (工单)
        with st.expander("🎫 Support Ticket"):
            with st.form("ticket_form"):
                st.text_input("User", value=st.session_state.user_email, disabled=True)
                st.selectbox("Issue", ["🔴 Bug / Error", "🟡 Billing", "🔵 Feature Request", "⚪ General"])
                st.text_input("Subject")
                msg_body = st.text_area("Message")
                if st.form_submit_button("🚀 Submit"):
                    if msg_body:
                        st.success("✅ Ticket Sent! ID: #8392")
                    else:
                        st.error("Please write a message.")

        # E. 底部按钮
        st.markdown("---")
        if st.button("🔑 Lost Key?"): st.info("Recovery link sent!")
        if st.button("🧹 Clear History"): st.success("History Cleared.")
        if st.button("🚪 Logout"): 
            st.session_state.clear()
            st.rerun()

    # === 右侧主内容 (MAIN CONTENT) ===
    
    # 顶部导航
    bc1, bc2 = st.columns([1, 5])
    if bc1.button("⬅️ Roles"):
        st.session_state.page = 2
        st.rerun()
    
    # 获取数据
    role = st.session_state.current_role
    role_data = MODES_DB[role]
    
    st.title(f"🎭 {role}")
    
    # 模式选择 (Tabs)
    modes = list(role_data.keys())
    selected_mode = st.radio("Select Mode:", modes, horizontal=True)
    
    current_mode_data = role_data[selected_mode]
    st.caption(f"💡 Info: {current_mode_data['desc']}")
    st.markdown("---")

    # 输入区域
    with st.container():
        c_in1, c_in2 = st.columns(2)
        
        with c_in1:
            # 智能选项逻辑 (8个 + 自定义)
            options = current_mode_data['dd'].copy()
            options.append("✨ Custom / Write Own...")
            
            choice = st.selectbox("👉 Select Option", options)
            
            if choice == "✨ Custom / Write Own...":
                user_topic = st.text_input("✍️ Enter Custom Topic:", placeholder="Type your own topic...")
            else:
                user_topic = choice
        
        with c_in2:
            user_details = st.text_input(f"⌨️ {current_mode_data['in']}", placeholder="Enter specific details...")
            
        out_lang = st.selectbox("🌐 Output Language", OUTPUT_LANGUAGES)
        
        # 生成按钮
        if st.button("✨ GENERATE PROMPT", type="primary"):
            # 模拟生成逻辑 (构建 prompt 字符串)
            final_prompt = f"""
            [SYSTEM]: Act as a World-Class {role}.
            [MODE]: {selected_mode}
            [STYLE/TOPIC]: {user_topic}
            [DETAILS]: {user_details}
            [LANGUAGE]: {out_lang}
            
            Please generate the content based on the above parameters.
            (This is a simulated output for Cikgu Lai's PromptLab).
            """
            st.session_state.generated_result = final_prompt
            st.success("✅ Content Generated Successfully!")

    # 输出 & 分享区域
    if st.session_state.generated_result:
        st.markdown("### 📄 Result:")
        st.code(st.session_state.generated_result, language="text")
        
        # 功能按钮行
        b1, b2, b3, b4, b5 = st.columns(5)
        
        # 1. 下载 TXT
        with b1:
            st.markdown(get_text_download_link(st.session_state.generated_result), unsafe_allow_html=True)
        
        # 2. 分享到 WhatsApp
        with b2:
            wa_url = get_whatsapp_link(st.session_state.generated_result)
            st.markdown(f'<a href="{wa_url}" target="_blank">📱 WhatsApp</a>', unsafe_allow_html=True)
            
        # 3. 模拟 Copy
        with b3:
            st.button("📋 Copy Text") # Streamlit 需插件实现真Copy，这里仅作按钮展示
            
        # 4. 模拟 PDF
        with b4:
            st.button("📥 PDF")
            
        # 5. 模拟 Facebook
        with b5:
            st.markdown(f'<a href="https://www.facebook.com/sharer/sharer.php?u=promptlab.com" target="_blank">📘 Facebook</a>', unsafe_allow_html=True)

# ==========================================
# 5. 页脚 (Footer)
# ==========================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
    PromptLab AI v26.0 © 2025 Cikgu Lai Inc.<br>
    <a href='#'>Terms</a> | <a href='#'>Privacy</a> | <a href='#'>Legal</a>
</div>
""", unsafe_allow_html=True)