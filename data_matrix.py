# data_matrix.py
# Lai's Lab V9.28 - FINAL 2025 EDITION
# 100% Full Data: 16 Langs, 126 Modes, Custom Option, FAQ

# ==========================================
# 1. 语言选项 (16 种)
# ==========================================
LANG_OPTIONS_GUEST = ["English", "简体中文", "繁體中文"]

LANG_OPTIONS_PRO = [
    "English", "简体中文", "繁體中文", "Bahasa Melayu", "Español", 
    "日本語", "한국어", "Français", "Deutsch", 
    "Italiano", "Português", "Русский", "Arabic", 
    "Hindi", "Thai", "Vietnamese"
]

# ==========================================
# 2. 对比表数据 (保留核心)
# ==========================================
TABLE_EN = [
    {"k": "Daily Limit", "v1": "5 / Day", "v2": "*Unlimited"},
    {"k": "Content Format", "v1": "With AI Symbols", "v2": "100% Clean & Human"},
    {"k": "Sharing", "v1": "Text + Watermark", "v2": "PDF + Clean Share"},
    {"k": "Languages", "v1": "3 Basic", "v2": "16+ Global"},
    {"k": "Expert Modes", "v1": "Basic (6)", "v2": "All 18 + Custom"},
    {"k": "Watermark", "v1": "Forced", "v2": "Removed"},
    {"k": "Support", "v1": "Standard", "v2": "VIP Priority"},
    {"k": "Price", "v1": "Free", "v2": "Limited $12.90"}
]
# (中文/繁体等略，逻辑中会自动处理)

# ==========================================
# 3. 16 国语言 UI 完整映射 (死锁版)
# ==========================================
# 基础英文模板
BASE_EN = {
    "sidebar_title": "Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
    "usage": "Daily Usage", "lang": "🌐 Language", "role": "🎭 Role", "tone": "🗣️ Tone Style",
    "logout": "🚪 Logout", "mode": "⚙️ Select Mode", "action": "⚡ Select Action", 
    "input_label": "📝 Context", "generate": "✨ Generate", "lock_msg": "🔒 Locked (Pro Only)", 
    "buy_btn": "👉 Upgrade to Pro", "result": "✨ Result", "live_stat": "Live Status",
    "tbl_headers": ["Capability", "Guest", "💎 PRO Lifetime"], "tbl_data": TABLE_EN
}

LANG_MAP = {
    "default": BASE_EN,
    "English": BASE_EN,
    "简体中文": {
        "sidebar_title": "Lai's Lab", "plan_guest": "访客计划", "plan_pro": "企业版 Pro",
        "usage": "今日用量", "lang": "🌐 语言设置", "role": "🎭 角色选择", "tone": "🗣️ 语气风格",
        "logout": "🚪 退出登录", "mode": "⚙️ 模式选择", "action": "⚡ 执行操作", 
        "input_label": "📝 详细要求", "generate": "✨ 开始生成", "lock_msg": "🔒 该模式仅限 Pro", 
        "buy_btn": "👉 升级 Pro 版", "result": "✨ 生成结果", "live_stat": "实时状态",
        "tbl_headers": ["功能特性", "访客", "💎 PRO 永久版"], "tbl_data": TABLE_EN # 暂时复用英文数据结构，文字自动适配
    },
    "繁體中文": {
        "sidebar_title": "Lai's Lab", "plan_guest": "訪客計劃", "plan_pro": "企業版 Pro",
        "usage": "今日用量", "lang": "🌐 語言設定", "role": "🎭 角色選擇", "tone": "🗣️ 語氣風格",
        "logout": "🚪 登出", "mode": "⚙️ 模式選擇", "action": "⚡ 執行操作", 
        "input_label": "📝 詳細要求", "generate": "✨ 開始生成", "lock_msg": "🔒 該模式僅限 Pro", 
        "buy_btn": "👉 升級 Pro 版", "result": "✨ 生成結果", "live_stat": "實時狀態",
        "tbl_headers": ["功能特性", "訪客", "💎 PRO 永久版"], "tbl_data": TABLE_EN
    },
    "Bahasa Melayu": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Pelan Tetamu", "plan_pro": "Pro Enterprise",
        "usage": "Penggunaan", "lang": "🌐 Bahasa", "role": "🎭 Peranan", "tone": "🗣️ Gaya Nada",
        "logout": "🚪 Log Keluar", "mode": "⚙️ Pilih Mod", "action": "⚡ Pilih Tindakan", 
        "input_label": "📝 Konteks", "generate": "✨ Jana", "lock_msg": "🔒 Dikunci (Pro Sahaja)", 
        "buy_btn": "👉 Naik Taraf Pro", "result": "✨ Hasil", "live_stat": "Status Langsung",
        "tbl_headers": ["Keupayaan", "Tetamu", "💎 PRO Seumur Hidup"], "tbl_data": TABLE_EN
    },
    "Español": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Plan Invitado", "plan_pro": "Pro Empresa",
        "usage": "Uso", "lang": "🌐 Idioma", "role": "🎭 Rol", "tone": "🗣️ Tono",
        "logout": "🚪 Salir", "mode": "⚙️ Modo", "action": "⚡ Acción", 
        "input_label": "📝 Contexto", "generate": "✨ Generar", "lock_msg": "🔒 Bloqueado (Solo Pro)", 
        "buy_btn": "👉 Mejorar a Pro", "result": "✨ Resultado", "live_stat": "En Vivo",
        "tbl_headers": ["Capacidad", "Invitado", "💎 PRO Vitalicio"], "tbl_data": TABLE_EN
    }
}

# 🔥 核心修复：强制补全所有 16 种语言的 Key，防止回退到英文
# 即使翻译暂时用英文，Key 必须存在，才能触发 App.py 的切换逻辑
MISSING_LANGS = [
    "日本語", "한국어", "Français", "Deutsch", "Italiano", "Português", 
    "Русский", "Arabic", "Hindi", "Thai", "Vietnamese"
]
for lang in MISSING_LANGS:
    LANG_MAP[lang] = BASE_EN.copy() # 先用英文填充，保证不崩

# ==========================================
# 4. 完整 60 个语调
# ==========================================
ROLE_TONES = {
    "Global Educator": ["📚 Academic", "🌟 Encouraging", "🤝 Patient", "💡 Socratic", "📢 Instructional", "🧠 Cognitive", "✨ Storytelling", "🎯 Objective", "🌈 Inclusive", "🔥 Passionate"],
    "Global Creator": ["🔥 Viral", "😜 Witty", "📖 Narrative", "⚡ Punchy", "🧐 Controversial", "🎨 Artistic", "📱 Trendy", "🎥 Cinematic", "🎭 Dramatic", "🤖 Minimalist"],
    "Global Parent": ["🥰 Warm", "🎉 Playful", "🛡️ Firm", "👩‍🏫 Patient", "🤝 Supportive", "🧘 Calm", "🎈 Creative", "📖 Storyteller", "🩺 Caregiver", "🎓 Mentor"],
    "Global Seller": ["💰 Persuasive", "⏳ Urgent", "💎 Luxury", "🤝 Trustworthy", "📢 Hype", "📊 Data-Driven", "🎯 Targeted", "🗣️ Conversational", "🔥 Aggressive", "✨ Solution-Focused"],
    "Global Student": ["🎓 Formal", "📝 Concise", "🤓 Geeky", "🎯 Goal-Oriented", "📚 Detailed", "🤔 Critical", "⚡ Quick", "🧠 Deep", "🗣️ Argumentative", "📝 Note-taking"],
    "Global Corporate": ["👔 Executive", "⚡ Direct", "🚀 Strategic", "⚖️ Compliance", "🤝 Diplomatic", "📊 Analytical", "📢 PR-Safe", "💼 Professional", "🗣️ Leadership", "🌍 Global"]
}
DEFAULT_TONES = ["Professional", "Friendly", "Informative", "Assertive", "Empathetic"]

# ==========================================
# 5. 完整的 126 个模式 + 自动注入 "7. Custom"
# ==========================================
ROLES_CONFIG = {
    "Global Educator": {
        "Pedagogy (Free)": [
            {"label": "1. Rubric Creator", "template": "Create a grading rubric for: {input}"},
            {"label": "2. Lesson Plan", "template": "Create a 1-hour lesson plan for: {input}"},
            {"label": "3. Quiz Generator", "template": "Create 5 multiple choice questions for: {input}"},
            {"label": "4. IEP Drafter", "template": "Draft an IEP goal for: {input}"},
            {"label": "5. Concept Explainer", "template": "Explain this concept to a 5-year old: {input}"},
            {"label": "6. Activity Designer", "template": "Classroom activity for: {input}"}
        ],
        "Visuals (Pro)": [
            {"label": "1. Pixar 3D", "template": "Midjourney prompt, Pixar style: {input}"},
            {"label": "2. Blackboard Art", "template": "Chalkboard diagram prompt for: {input}"},
            {"label": "3. Infographic", "template": "Educational infographic prompt for: {input}"},
            {"label": "4. Flashcard Art", "template": "Visual flashcard design for: {input}"},
            {"label": "5. Classroom Poster", "template": "Motivational poster text for: {input}"},
            {"label": "6. Slide Design", "template": "PowerPoint slide layout description for: {input}"}
        ],
        "Admin (Pro)": [
            {"label": "1. Email to Parents", "template": "Write an email to parents about: {input}"},
            {"label": "2. Report Comments", "template": "Report card comment for: {input}"},
            {"label": "3. Newsletter", "template": "Classroom newsletter section about: {input}"},
            {"label": "4. Behavior Log", "template": "Document a behavioral incident: {input}"},
            {"label": "5. Grant Proposal", "template": "Write a grant proposal for: {input}"},
            {"label": "6. Meeting Agenda", "template": "Staff meeting agenda item: {input}"}
        ]
    },
    "Global Creator": {
        "Scripting (Free)": [
            {"label": "1. Viral Hook", "template": "Write 5 viral hooks for: {input}"},
            {"label": "2. TikTok Script", "template": "30-second TikTok script for: {input}"},
            {"label": "3. YouTube Intro", "template": "YouTube video intro for: {input}"},
            {"label": "4. Caption Writer", "template": "Instagram caption for: {input}"},
            {"label": "5. Hashtag Gen", "template": "30 relevant hashtags for: {input}"},
            {"label": "6. CTAs", "template": "Call to action for: {input}"}
        ],
        "Visuals (Pro)": [
            {"label": "1. Thumbnail", "template": "YouTube thumbnail prompt: {input}"},
            {"label": "2. Profile Pic", "template": "Profile picture prompt: {input}"},
            {"label": "3. Banner Art", "template": "Channel banner prompt: {input}"},
            {"label": "4. Sticker Set", "template": "Emoji/Sticker pack prompt: {input}"},
            {"label": "5. Merch Design", "template": "T-shirt design prompt: {input}"},
            {"label": "6. NFT Art", "template": "NFT collection concept for: {input}"}
        ],
        "Marketing (Pro)": [
            {"label": "1. Sponsor Pitch", "template": "Pitch email to brand: {input}"},
            {"label": "2. Bio Optimizer", "template": "Optimize social bio for: {input}"},
            {"label": "3. Content Calendar", "template": "1-week content calendar for: {input}"},
            {"label": "4. Collab Request", "template": "Collaboration DM to influencer: {input}"},
            {"label": "5. Community Post", "template": "Community engagement post for: {input}"},
            {"label": "6. Newsletter Intro", "template": "Newsletter introduction for: {input}"}
        ]
    },
    "Global Parent": {
        "Story (Free)": [
            {"label": "1. Bedtime Story", "template": "Bedtime story about: {input}"},
            {"label": "2. Moral Lesson", "template": "Story teaching the moral of: {input}"},
            {"label": "3. Personalized", "template": "Story featuring child name: {input}"},
            {"label": "4. Adventure", "template": "Choose-your-own-adventure segment: {input}"},
            {"label": "5. Poem", "template": "Rhyming poem about: {input}"},
            {"label": "6. Joke Gen", "template": "Kid-friendly jokes about: {input}"}
        ],
        "Education (Pro)": [
            {"label": "1. Homework Help", "template": "Explain homework question: {input}"},
            {"label": "2. Science Exp", "template": "Home science experiment for: {input}"},
            {"label": "3. Math Drill", "template": "Math practice problems for: {input}"},
            {"label": "4. History Fact", "template": "Fun history fact about: {input}"},
            {"label": "5. Coding Concept", "template": "Explain coding loop to kid: {input}"},
            {"label": "6. Language Practice", "template": "Spanish vocabulary practice for: {input}"}
        ],
        "Fun (Pro)": [
            {"label": "1. Party Planner", "template": "Birthday party plan for: {input}"},
            {"label": "2. Lunchbox Note", "template": "Cute note for lunchbox: {input}"},
            {"label": "3. Weekend Trip", "template": "Family trip itinerary for: {input}"},
            {"label": "4. Game Idea", "template": "Indoor game idea for: {input}"},
            {"label": "5. Craft Project", "template": "DIY craft project using: {input}"},
            {"label": "6. Movie Night", "template": "Family movie recommendation like: {input}"}
        ]
    },
    "Global Seller": {
        "Copy (Free)": [
            {"label": "1. Ad Headline", "template": "Facebook ad headline for: {input}"},
            {"label": "2. Product Desc", "template": "Amazon product description for: {input}"},
            {"label": "3. Email Subject", "template": "High open-rate subject lines for: {input}"},
            {"label": "4. Value Prop", "template": "Value proposition statement: {input}"},
            {"label": "5. SEO Keywords", "template": "SEO keyword list for: {input}"},
            {"label": "6. Tagline", "template": "Catchy tagline for: {input}"}
        ],
        "Strategy (Pro)": [
            {"label": "1. Upsell Script", "template": "Upsell script for: {input}"},
            {"label": "2. Objection Kill", "template": "Handle objection: {input}"},
            {"label": "3. Persona Gen", "template": "Customer persona for: {input}"},
            {"label": "4. Competitor Analysis", "template": "Analyze competitor: {input}"},
            {"label": "5. Pricing Strategy", "template": "Pricing strategy ideas for: {input}"},
            {"label": "6. Funnel Map", "template": "Sales funnel steps for: {input}"}
        ],
        "Content (Pro)": [
            {"label": "1. LinkedIn Post", "template": "LinkedIn thought leadership about: {input}"},
            {"label": "2. Twitter Thread", "template": "Twitter thread about: {input}"},
            {"label": "3. Blog Outline", "template": "SEO blog outline for: {input}"},
            {"label": "4. Video Script", "template": "Product demo video script: {input}"},
            {"label": "5. Case Study", "template": "Case study structure for: {input}"},
            {"label": "6. Whitepaper", "template": "Whitepaper topic ideas: {input}"}
        ]
    },
    "Global Student": {
        "Study (Free)": [
            {"label": "1. Summarizer", "template": "Summarize this text: {input}"},
            {"label": "2. Flashcards", "template": "Create flashcard content for: {input}"},
            {"label": "3. Essay Outline", "template": "Essay outline for topic: {input}"},
            {"label": "4. Thesis Statement", "template": "Strong thesis statement for: {input}"},
            {"label": "5. Study Schedule", "template": "Study schedule for exam: {input}"},
            {"label": "6. Mnemonics", "template": "Mnemonic device for: {input}"}
        ],
        "Research (Pro)": [
            {"label": "1. Source Finder", "template": "Find academic sources for: {input}"},
            {"label": "2. Citation Fix", "template": "Format citation in APA: {input}"},
            {"label": "3. Abstract Gen", "template": "Write an abstract for: {input}"},
            {"label": "4. Lit Review", "template": "Literature review structure: {input}"},
            {"label": "5. Methodology", "template": "Research methodology steps: {input}"},
            {"label": "6. Data Analysis", "template": "Explain this data set: {input}"}
        ],
        "Career (Pro)": [
            {"label": "1. Resume Bullet", "template": "Improve resume bullet: {input}"},
            {"label": "2. Cover Letter", "template": "Cover letter for job: {input}"},
            {"label": "3. Interview Prep", "template": "Interview questions for: {input}"},
            {"label": "4. LinkedIn Bio", "template": "Professional LinkedIn bio: {input}"},
            {"label": "5. Cold Email", "template": "Cold networking email: {input}"},
            {"label": "6. Portfolio Desc", "template": "Project description for portfolio: {input}"}
        ]
    },
    "Global Corporate": {
        "Admin (Free)": [
            {"label": "1. Email Polish", "template": "Professionalize this email: {input}"},
            {"label": "2. Meeting Mins", "template": "Format meeting minutes: {input}"},
            {"label": "3. Memo Writer", "template": "Write a corporate memo about: {input}"},
            {"label": "4. Agenda Gen", "template": "Meeting agenda for: {input}"},
            {"label": "5. Slack Update", "template": "Professional Slack update: {input}"},
            {"label": "6. OOO Message", "template": "Out of office reply: {input}"}
        ],
        "Strategy (Pro)": [
            {"label": "1. SWOT Analysis", "template": "SWOT analysis for: {input}"},
            {"label": "2. OKR Draft", "template": "Draft OKRs for: {input}"},
            {"label": "3. Policy Draft", "template": "Draft company policy for: {input}"},
            {"label": "4. Project Plan", "template": "Project plan outline: {input}"},
            {"label": "5. Risk Assess", "template": "Risk assessment for: {input}"},
            {"label": "6. Budget Justification", "template": "Justify budget for: {input}"}
        ],
        "HR (Pro)": [
            {"label": "1. Job Post", "template": "Job posting for: {input}"},
            {"label": "2. Feedback", "template": "Constructive feedback script for: {input}"},
            {"label": "3. Announcement", "template": "Company announcement about: {input}"},
            {"label": "4. Onboarding", "template": "Onboarding checklist for: {input}"},
            {"label": "5. Interview Qs", "template": "Interview questions for role: {input}"},
            {"label": "6. Culture Value", "template": "Define company value: {input}"}
        ]
    }
}

# 🔥 核心修复：自动为所有模式追加 "7. Custom / DIY"
CUSTOM_OPTION = {"label": "7. Custom / DIY", "template": "{input}"}
for role, modes in ROLES_CONFIG.items():
    for mode_name, options in modes.items():
        # 检查是否已有，防止重复添加
        if not any(o['label'].startswith("7.") for o in options):
            options.append(CUSTOM_OPTION)

# ==========================================
# 6. 16 项 FAQ 完整拦截
# ==========================================
INTERCEPTORS = {
    "price": "$12.90 Lifetime Access (One-time payment)",
    "refund": "Digital keys are non-refundable once activated.",
    "free": "Guest Plan: 5 generations per day with watermark.",
    "support": "VIP Support: 1-2 days response time.",
    "invoice": "Invoices are automatically sent by LemonSqueezy.",
    "license": "One license key per user account.",
    "upgrade": "Click 'Activate Pro' in the sidebar to upgrade.",
    "watermark": "Pro users get 100% clean output without watermarks.",
    "pdf": "PDF export supports 16 languages including Chinese/Japanese.",
    "privacy": "We do not store your input data. Local session only.",
    "language": "Supports 16+ languages. Switch in the sidebar.",
    "modes": "126+ Expert Modes available for Pro users.",
    "api": "API access is not currently available for public use.",
    "team": "Contact support@cikgulai.com for team licensing.",
    "cancel": "Lifetime deal does not require cancellation.",
    "contact": "Email: support@cikgulai.com"
}
