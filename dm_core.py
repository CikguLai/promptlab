# dm_core.py
# 核心功能数据 (Roles, Modes, Options, Tones, Intercepts)
# Language: English (Core Logic)

# ==========================================
# 1. 核心功能选项 (6 Roles x 3 Modes x 7 Options = 126 Options)
# ==========================================
RAW_ROLES_DATA = {
    "Global Educator": {
        "Pedagogy (Free)": [
            "1. Direct Instruction", 
            "2. Gamification", 
            "3. Project-Based Learning", 
            "4. Socratic Method", 
            "5. Flipped Classroom", 
            "6. Differentiated Instruction", 
            "7. Analyze Student Work (OCR)"
        ],
        "Visuals (Pro)": [
            "1. Pixar/Disney 3D", 
            "2. National Geographic", 
            "3. Minimalist Vector", 
            "4. Vintage Watercolor", 
            "5. Scientific Schematic", 
            "6. Cyberpunk Concept"
        ],
        "Comm (Pro)": [
            "1. Parent Message", 
            "2. Behavior Report", 
            "3. Official Proposal", 
            "4. Classroom Newsletter", 
            "5. Event Invitation", 
            "6. Grant Application"
        ]
    },
    "Global Creator": {
        "Scripting (Free)": [
            "1. Visual-to-Script", 
            "2. TikTok/Reels Hook", 
            "3. YouTube Edutainment", 
            "4. Storytelling Vlog", 
            "5. Podcast Interview", 
            "6. Live Stream Flow"
        ],
        "Thumbnail (Pro)": [
            "1. High CTR (Shocked)", 
            "2. Cinematic Poster", 
            "3. Tech/Neon/Glowing", 
            "4. Before & After", 
            "5. Minimalist Apple", 
            "6. Comic Book Style"
        ],
        "Marketing (Pro)": [
            "1. Xiaohongshu (KOC)", 
            "2. Instagram Caption", 
            "3. Facebook Ad", 
            "4. LinkedIn Leader", 
            "5. Twitter Thread", 
            "6. Email Newsletter"
        ]
    },
    "Global Parent": {
        "Story Time (Free)": [
            "1. From Drawing", 
            "2. Bedtime Story", 
            "3. Hero's Journey", 
            "4. Social Emotional", 
            "5. Science 'Why'", 
            "6. Cultural Tale"
        ],
        "Activities (Pro)": [
            "1. DIY Craft Guide", 
            "2. Rainy Day Game", 
            "3. Kitchen Science", 
            "4. Scavenger Hunt", 
            "5. Family Bonding", 
            "6. No-Screen Coding"
        ],
        "Tutor (Pro)": [
            "1. Solve Problem (OCR)", 
            "2. Feynman Technique", 
            "3. Homework Helper", 
            "4. Quiz Generator", 
            "5. Vocabulary Builder", 
            "6. Essay Proofreader"
        ]
    },
    "Global Seller": {
        "Copywriting (Free)": [
            "1. Product Desc (OCR)", 
            "2. PAS Model", 
            "3. AIDA Model", 
            "4. FAB Model", 
            "5. Storytelling Sales", 
            "6. Objection Handling"
        ],
        "Product Shot (Pro)": [
            "1. Studio White BG", 
            "2. Lifestyle Home", 
            "3. Luxury Gold/Black", 
            "4. Nature/Sunlight", 
            "5. Cyberpunk/Tech", 
            "6. Flat Lay"
        ],
        "Support (Pro)": [
            "1. Apology & Recovery", 
            "2. Review Request", 
            "3. Complaint Reply", 
            "4. Promo Announcement", 
            "5. Crisis Statement", 
            "6. FAQ Gen"
        ]
    },
    "Global Student": {
        "Study (Free)": [
            "1. Explain Chart (OCR)", 
            "2. Feynman Technique", 
            "3. Lit Review Matrix", 
            "4. Flashcard (Anki)", 
            "5. Concept Simplifier", 
            "6. Translation"
        ],
        "Project (Pro)": [
            "1. Essay Outline", 
            "2. Presentation Script", 
            "3. Debate Prep", 
            "4. Lab Report", 
            "5. Methodology", 
            "6. Group Roles"
        ],
        "Career (Pro)": [
            "1. ATS Resume", 
            "2. Cover Letter", 
            "3. Interview Prep", 
            "4. LinkedIn Bio", 
            "5. Cold Email", 
            "6. Portfolio Desc"
        ]
    },
    "Global Corporate": {
        "Admin (Free)": [
            "1. Extract Data (OCR)", 
            "2. Meeting Minutes", 
            "3. Official Proposal", 
            "4. Internal Memo", 
            "5. SOP / Process", 
            "6. Press Release"
        ],
        "Strategy (Pro)": [
            "1. OKRs", 
            "2. SWOT Analysis", 
            "3. Competitor Dive", 
            "4. Business Canvas", 
            "5. Risk Matrix", 
            "6. Pitch Deck"
        ],
        "HR & Team (Pro)": [
            "1. Performance Review", 
            "2. Job Desc (JD)", 
            "3. Onboarding Plan", 
            "4. Crisis Comms", 
            "5. Team Building", 
            "6. Termination"
        ]
    }
}

# 自动生成 Template 配置 (不要删除)
ROLES_CONFIG = {}
for role, modes in RAW_ROLES_DATA.items():
    ROLES_CONFIG[role] = {}
    for mode_name, options in modes.items():
        ROLES_CONFIG[role][mode_name] = []
        for opt in options:
            template = f"Act as a {role}. Mode: {mode_name}. Task: {opt}. Context: {{input}}"
            ROLES_CONFIG[role][mode_name].append({"label": opt, "template": template})
        # 添加自定义选项
        ROLES_CONFIG[role][mode_name].append({"label": "7. Custom / DIY", "template": "{input}"})

# ==========================================
# 2. 60个语调 (6 Roles x 10 Tones)
# ==========================================
ROLE_TONES = {
    "Global Educator": [
        "📚 Academic", "🌟 Encouraging", "📢 Instructional", "🤝 Patient", "💡 Socratic", 
        "🧠 Cognitive", "✨ Storytelling", "🎯 Objective", "🌈 Inclusive", "🔥 Passionate"
    ],
    "Global Creator": [
        "🔥 Viral", "😜 Witty", "📖 Narrative", "⚡ Punchy", "🧐 Controversial", 
        "🎨 Artistic", "📱 Trendy", "🎥 Cinematic", "🎭 Dramatic", "🤖 Minimalist"
    ],
    "Global Parent": [
        "🥰 Warm", "🎉 Playful", "🛡️ Firm", "👩‍🏫 Patient", "🤝 Supportive", 
        "🧘 Calm", "🎈 Creative", "📖 Storyteller", "🩺 Caregiver", "🎓 Mentor"
    ],
    "Global Seller": [
        "💰 Persuasive", "⏳ Urgent", "💎 Luxury", "🤝 Trustworthy", "📢 Hype", 
        "📊 Data-Driven", "🎯 Targeted", "🗣️ Conversational", "🔥 Aggressive", "✨ Solution"
    ],
    "Global Student": [
        "🎓 Formal", "📝 Concise", "🤓 Geeky", "🎯 Goal-Oriented", "📚 Detailed", 
        "🤔 Critical", "⚡ Quick", "🧠 Deep", "🗣️ Argumentative", "📝 Note-taking"
    ],
    "Global Corporate": [
        "👔 Executive", "⚡ Direct", "🚀 Strategic", "⚖️ Compliance", "🤝 Diplomatic", 
        "📊 Analytical", "📢 PR-Safe", "💼 Professional", "🗣️ Leadership", "🌍 Global"
    ]
}
DEFAULT_TONES = ["Professional", "Friendly", "Informative"]

# ==========================================
# 3. 智能拦截逻辑 (Intercept Logic)
# ==========================================
# (关键词列表, 对应FAQ索引)
INTERCEPT_LOGIC = [
    (["subscription", "monthly", "fee", "订阅", "月费"], 0), 
    (["refund", "money", "back", "退款", "退钱"], 1),
    (["key", "license", "code", "lost", "激活码", "丢失"], 2), 
    (["device", "mobile", "phone", "设备", "手机"], 3),
    (["affiliate", "partner", "commission", "分销", "佣金"], 4), 
    (["invoice", "receipt", "bill", "发票", "收据"], 5),
    (["school", "student", "bulk", "教育", "团购"], 6), 
    (["pdf", "font", "box", "乱码", "字体"], 7),
    (["wechat", "share", "微信", "分享"], 8), 
    (["invalid", "error", "activate", "无效", "错误"], 9),
    (["slow", "speed", "wait", "慢", "卡"], 10), 
    (["limit", "quota", "unlimited", "限制", "无限"], 11),
    (["commercial", "business", "商用", "版权"], 12), 
    (["offline", "internet", "离线", "断网"], 13),
    (["privacy", "store", "data", "隐私", "保存"], 14), 
    (["share account", "sharing", "login", "共享", "封号"], 15)
]