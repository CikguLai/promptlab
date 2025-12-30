# data_matrix.py
# Lai's Lab V9.25 - Professional Database (Full Audit Edition)

# ==========================================
# 1. 语言与基础配置
# ==========================================
LANG_OPTIONS_GUEST = ["English", "简体中文", "Español"]

LANG_OPTIONS_PRO = [
    "English", "简体中文", "Español", "Bahasa Melayu", 
    "日本語", "한국어", "Français", "Deutsch", 
    "Italiano", "Português", "Русский", "Arabic", 
    "Hindi", "Thai", "Vietnamese"
]

# ✅ 审查增强：每个角色 10 个高对比度语调
ROLE_TONES = {
    "Global Educator": [
        "📚 Academic (学术严谨)", "🌟 Encouraging (鼓舞人心)", "🤝 Patient (耐心引导)", 
        "💡 Socratic (启发式)", "📢 Instructional (指令明确)", "🧠 Cognitive (认知优化)",
        "✨ Storytelling (叙事化)", "🎯 Objective (客观)", "🌈 Inclusive (包容性)", "🔥 Passionate (激情)"
    ],
    "Global Creator": [
        "🔥 Viral (爆款潜质)", "😜 Witty (机智幽默)", "📖 Narrative (叙事感)", 
        "⚡ Punchy (有力简练)", "🧐 Controversial (深刻/争议)", "🎨 Artistic (艺术感)",
        "📱 Trendy (潮流前沿)", "🎥 Cinematic (画面感)", "🎭 Dramatic (戏剧性)", "🤖 Futurist (未来感)"
    ],
    "Global Parent": [
        "🥰 Warm (温馨)", "🧙‍♂️ Magical (童话感)", "🎉 Playful (趣味十足)", 
        "😴 Calming (睡前安抚)", "🛡️ Firm (坚定引导)", "👩‍🏫 Patient (耐心细致)",
        "🌿 Gentle (柔和)", "🧠 Educational (寓教于乐)", "💖 Empathetic (情感共鸣)", "🦄 Whimsical (天马行空)"
    ],
    "Global Seller": [
        "💰 Persuasive (说服力)", "⏳ Urgent (紧迫感)", "💎 Luxury (奢华感)", 
        "🤝 Trustworthy (可靠)", "🎁 Benefit-Driven (利益导向)", "📣 Bold (大胆有力)",
        "📈 Analytical (数据驱动)", "🔥 Enthusiastic (热情)", "🎯 Targeted (精准转化)", "🛡️ Reassuring (安全保障)"
    ],
    "Global Student": [
        "🎓 Formal (正式学术)", "📝 Concise (极其简练)", "🔍 Critical (批判思考)", 
        "🗣️ Explanatory (解释性)", "✍️ Reflective (反思性)", "🤓 Geeky (极客深度)",
        "💡 Creative (创意)", "📊 Methodical (条理清晰)", "📚 Literature-based (基于文献)", "🎯 Goal-Oriented (目标导向)"
    ],
    "Global Corporate": [
        "👔 Executive (决策风)", "🤝 Diplomatic (外交辞令)", "📊 Data-Driven (数据驱动)", 
        "⚡ Direct (直率干练)", "🚀 Strategic (战略高度)", "⚖️ Compliance (合规严谨)",
        "🏆 Visionary (远见卓识)", "📣 Authoritative (权威)", "💬 Collaborative (协作式)", "📉 Conservative (稳健)"
    ]
}
DEFAULT_TONES = ["Professional", "Friendly", "Informative", "Assertive", "Empathetic"]

# ==========================================
# 2. 多语言 UI 映射
# ==========================================
LANG_MAP = {
    "default": {
        "sidebar_title": "🧬 Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
        "usage": "Daily Usage", "lang": "🌐 Language", "role": "🎭 Role", "tone": "🗣️ Tone Style",
        "faq": "❓ FAQ / Help", "support": "🎫 Support Ticket", "logout": "🚪 Logout",
        "mode": "⚙️ Select Mode", "action": "⚡ Select Action", "input_label": "📝 Context",
        "generate": "✨ Generate with PASEC", "lock_msg": "🔒 Pro Feature Locked", "buy_btn": "👉 Get Pro Access", 
        "result": "✨ PASEC Result", "ticket_types": ["Bug", "Billing", "Feature", "Partnership", "Other"]
    },
    "简体中文": {
        "sidebar_title": "🧬 Lai's Lab", "plan_guest": "访客计划", "plan_pro": "企业版 Pro",
        "usage": "今日用量", "lang": "🌐 语言设置", "role": "🎭 角色选择", "tone": "🗣️ 语气风格",
        "faq": "❓ 常见问题", "support": "🎫 客服工单", "logout": "🚪 退出登录",
        "mode": "⚙️ 模式选择", "action": "⚡ 执行操作", "input_label": "📝 详细要求",
        "generate": "✨ PASEC 生成", "lock_msg": "🔒 Pro 功能已锁定", "buy_btn": "👉 获取 Pro 权限", 
        "result": "✨ PASEC 输出", "ticket_types": ["错误报告", "账单问题", "功能建议", "商务合作", "其他"]
    }
}

# ==========================================
# 3. 完整 16 项 FAQ 与 智能拦截
# ==========================================
RAW_FAQ_DATA = [
    {"q": "Is it free?", "a": "Guest plan is free forever (5/day).", "kw": ["free", "charge", "cost"]},
    {"q": "Pro Cost?", "a": "$12.90 Lifetime (Limited Offer).", "kw": ["price", "subscription", "12.90"]},
    {"q": "Refund Policy?", "a": "No Refunds: License keys are digital assets.", "kw": ["refund", "money", "back"]},
    {"q": "Lost Key?", "a": "Visit [LemonSqueezy Orders](https://app.lemonsqueezy.com/my-orders).", "kw": ["key", "lost", "code"]},
    {"q": "Daily Limit?", "a": "Guest: 5/day. Pro: 1000/day.", "kw": ["limit", "quota", "stuck"]},
    {"q": "Commercial Use?", "a": "Pro Users: 100% Commercial Rights.", "kw": ["commercial", "business"]},
    {"q": "API Access?", "a": "Not available in V9.", "kw": ["api", "developer"]},
    {"q": "Privacy?", "a": "We do not store your prompt data.", "kw": ["privacy", "data", "secure"]},
    {"q": "Languages?", "a": "15+ Global Languages in Pro.", "kw": ["language", "chinese", "malay"]},
    {"q": "PDF Issue?", "a": "Pro users can export PDF reports directly.", "kw": ["pdf", "export", "download"]},
    {"q": "Watermark?", "a": "Pro version has NO watermark.", "kw": ["watermark", "remove"]},
    {"q": "Payment?", "a": "PayPal, Stripe, Cards accepted.", "kw": ["pay", "card", "paypal"]},
    {"q": "Mobile?", "a": "Fully optimized for iOS/Android.", "kw": ["mobile", "phone", "app"]},
    {"q": "Support?", "a": "Pro: 1-2 Days. Guest: 3-5 Days.", "kw": ["support", "help", "time"]},
    {"q": "Master Key?", "a": "Admin backdoor for enterprise management.", "kw": ["master", "admin"]},
    {"q": "Future Updates?", "a": "Lifetime Pro gets all future V9.x updates.", "kw": ["update", "version", "new"]}
]

FAQ_LIST = [f"{i+1}. {item['q']} {item['a']}" for i, item in enumerate(RAW_FAQ_DATA)]
INTERCEPTORS = {kw: item['a'] for item in RAW_FAQ_DATA for kw in item['kw']}

# ==========================================
# 4. 角色/模式/选项矩阵 (126个选项)
# ==========================================
ROLES_CONFIG = {
    "Global Educator": {
        "Pedagogy (Free)": [
            {"label": "1. Rubric Creator", "template": "Create a detailed grading rubric for: {input}"},
            {"label": "2. Direct Instruction", "template": "Design a lesson plan for: {input}"},
            {"label": "3. Gamification", "template": "Create gamification strategy for: {input}"},
            {"label": "4. Project-Based Learning", "template": "Design a PBL project: {input}"},
            {"label": "5. Socratic Method", "template": "Generate Socratic questions for: {input}"},
            {"label": "6. Flipped Classroom", "template": "Plan a flipped module: {input}"},
            {"label": "7. Custom Educator", "template": "Expert educator prompt: {input}"}
        ],
        "Visuals (Pro)": [
            {"label": "1. Pixar 3D", "template": "Midjourney Pixar-style: {input}"},
            {"label": "2. NatGeo Photo", "template": "NatGeo photography prompt: {input}"},
            {"label": "3. Vector Illustration", "template": "Flat vector art: {input}"},
            {"label": "4. Watercolor Art", "template": "Watercolor painting: {input}"},
            {"label": "5. Scientific Diagram", "template": "Scientific schematic: {input}"},
            {"label": "6. Cyberpunk Scene", "template": "Cyberpunk concept art: {input}"},
            {"label": "7. Architecture Shot", "template": "Architectural photo: {input}"}
        ],
        "Comm (Pro)": [
            {"label": "1. Parent Message", "template": "Draft parent message: {input}"},
            {"label": "2. Behavior Report", "template": "Student behavior report: {input}"},
            {"label": "3. School Proposal", "template": "Official school proposal: {input}"},
            {"label": "4. Newsletter", "template": "Class newsletter content: {input}"},
            {"label": "5. Event Invitation", "template": "School event invite: {input}"},
            {"label": "6. Grant Request", "template": "Grant application draft: {input}"},
            {"label": "7. Policy Update", "template": "School policy announcement: {input}"}
        ]
    },
    "Global Creator": {
        "Scripting (Free)": [
            {"label": "1. Viral Hook", "template": "10 viral hooks for: {input}"},
            {"label": "2. TikTok Script", "template": "60s TikTok script: {input}"},
            {"label": "3. YouTube Outline", "template": "YouTube video outline: {input}"},
            {"label": "4. Story Vlog", "template": "Vlog voiceover script: {input}"},
            {"label": "5. Podcast Interview", "template": "Podcast questions: {input}"},
            {"label": "6. Live Flow", "template": "Live stream run-of-show: {input}"},
            {"label": "7. Ad Script", "template": "Short video ad script: {input}"}
        ],
        "Thumbnail (Pro)": [
            {"label": "1. High CTR Shock", "template": "CTR thumbnail prompt: {input}"},
            {"label": "2. Cinematic Movie", "template": "Movie poster thumbnail: {input}"},
            {"label": "3. Tech Neon", "template": "Tech review thumbnail: {input}"},
            {"label": "4. Before/After", "template": "Comparison thumbnail: {input}"},
            {"label": "5. Apple Minimalist", "template": "Clean Apple-style thumbnail: {input}"},
            {"label": "6. Comic Style", "template": "Comic book thumbnail: {input}"},
            {"label": "7. 3D Render", "template": "Octane render thumbnail: {input}"}
        ],
        "Marketing (Pro)": [
            {"label": "1. Xiaohongshu KOC", "template": "XHS post with emojis: {input}"},
            {"label": "2. Instagram Captions", "template": "5 IG captions for: {input}"},
            {"label": "3. Facebook Sales Ad", "template": "FB sales copy: {input}"},
            {"label": "4. LinkedIn Thought", "template": "LinkedIn leadership post: {input}"},
            {"label": "5. Twitter Thread", "template": "Viral Twitter thread: {input}"},
            {"label": "6. Email Sequence", "template": "3-day email sequence: {input}"},
            {"label": "7. Press Release", "template": "Marketing press release: {input}"}
        ]
    },
    "Global Parent": {
        "Story (Free)": [
            {"label": "1. Magical Day", "template": "Magical story about: {input}"},
            {"label": "2. Bedtime Calming", "template": "Calming bedtime story: {input}"},
            {"label": "3. Child Hero", "template": "Heroic journey for: {input}"},
            {"label": "4. Moral Lesson", "template": "Lesson-based story: {input}"},
            {"label": "5. Science Story", "template": "Explain science via story: {input}"},
            {"label": "6. Cultural Myth", "template": "Cultural retelling: {input}"},
            {"label": "7. Personalized Tale", "template": "Custom story for: {input}"}
        ],
        "Activities (Pro)": [
            {"label": "1. DIY Craft", "template": "Step-by-step DIY: {input}"},
            {"label": "2. Rainy Day Game", "template": "Indoor game plan: {input}"},
            {"label": "3. Kitchen Experiment", "template": "Kitchen science: {input}"},
            {"label": "4. Scavenger Hunt", "template": "Custom hunt list: {input}"},
            {"label": "5. Screen-Free Play", "template": "Bonding activity: {input}"},
            {"label": "6. Logic Coding", "template": "No-screen coding game: {input}"},
            {"label": "7. Nature Explorer", "template": "Outdoor exploration guide: {input}"}
        ],
        "Tutor (Pro)": [
            {"label": "1. Mnemonic Maker", "template": "Create mnemonic for: {input}"},
            {"label": "2. Feynman Simple", "template": "Explain to a 5yo: {input}"},
            {"label": "3. Homework Guide", "template": "Guide to solve: {input}"},
            {"label": "4. Quiz Master", "template": "5 practice questions: {input}"},
            {"label": "5. Vocabulary Fun", "template": "Etymology and usage: {input}"},
            {"label": "6. Essay Fixer", "template": "Constructive proofread: {input}"},
            {"label": "7. Math Visualizer", "template": "Visual math explanation: {input}"}
        ]
    },
    "Global Seller": {
        "Copy (Free)": [
            {"label": "1. Landing Page", "template": "Landing page copy for: {input}"},
            {"label": "2. PAS Model", "template": "Problem-Agitate-Solve: {input}"},
            {"label": "3. AIDA Model", "template": "Attention-Interest-Desire: {input}"},
            {"label": "4. FAB Benefits", "template": "Features and Benefits: {input}"},
            {"label": "5. Brand Story", "template": "Engaging brand story: {input}"},
            {"label": "6. Objection Kill", "template": "Handle objections for: {input}"},
            {"label": "7. Sales script", "template": "Cold calling script: {input}"}
        ],
        "Product (Pro)": [
            {"label": "1. White Studio", "template": "Minimalist white BG: {input}"},
            {"label": "2. Home Lifestyle", "template": "Lifestyle product shot: {input}"},
            {"label": "3. Luxury Gold", "template": "Luxury gold/black shot: {input}"},
            {"label": "4. Nature Light", "template": "Sunlight nature shot: {input}"},
            {"label": "5. Tech Cyber", "template": "Neon tech product shot: {input}"},
            {"label": "6. Knolling Layout", "template": "Flat lay knolling: {input}"},
            {"label": "7. Macro Detail", "template": "Macro detail product shot: {input}"}
        ],
        "Support (Pro)": [
            {"label": "1. Apology Email", "template": "Professional apology: {input}"},
            {"label": "2. Review Invite", "template": "Post-purchase review: {input}"},
            {"label": "3. Complaint Fix", "template": "Resolution email for: {input}"},
            {"label": "4. Promo Launch", "template": "Launch email for: {input}"},
            {"label": "5. Crisis PR", "template": "Public PR statement: {input}"},
            {"label": "6. Dynamic FAQ", "template": "Product FAQ generation: {input}"},
            {"label": "7. VIP Welcome", "template": "High-tier welcome email: {input}"}
        ]
    },
    "Global Student": {
        "Study (Free)": [
            {"label": "1. Summary Pro", "template": "Executive summary of: {input}"},
            {"label": "2. Concept Map", "template": "Concept map structure: {input}"},
            {"label": "3. Lit Review", "template": "Academic lit review: {input}"},
            {"label": "4. Flashcards Anki", "template": "Anki-ready flashcards: {input}"},
            {"label": "5. Text Simplifier", "template": "Simplify complex text: {input}"},
            {"label": "6. Uni Translation", "template": "Academic EN translation: {input}"},
            {"label": "7. Exam Strategy", "template": "Exam prep schedule: {input}"}
        ],
        "Project (Pro)": [
            {"label": "1. Essay Outline", "template": "Comprehensive outline: {input}"},
            {"label": "2. Slide Content", "template": "Presentation slide text: {input}"},
            {"label": "3. Debate Prep", "template": "Debate points for/against: {input}"},
            {"label": "4. Lab Report", "template": "Standard lab report: {input}"},
            {"label": "5. Methodology", "template": "Research methodology: {input}"},
            {"label": "6. Group Roles", "template": "Team collaboration plan: {input}"},
            {"label": "7. Abstract Writer", "template": "Paper abstract generator: {input}"}
        ],
        "Career (Pro)": [
            {"label": "1. ATS Optimizer", "template": "ATS-friendly resume: {input}"},
            {"label": "2. Cover Letter", "template": "Winning cover letter: {input}"},
            {"label": "3. Interview Q&A", "template": "Hard interview questions: {input}"},
            {"label": "4. LinkedIn Bio", "template": "Professional About section: {input}"},
            {"label": "5. Cold Networking", "template": "Networking email for: {input}"},
            {"label": "6. Portfolio Case", "template": "Portfolio case study: {input}"},
            {"label": "7. Salary Negotiate", "template": "Salary negotiation script: {input}"}
        ]
    },
    "Global Corporate": {
        "Admin (Free)": [
            {"label": "1. Email Polisher", "template": "Professional email fix: {input}"},
            {"label": "2. Meeting Minutes", "template": "Minutes formatting: {input}"},
            {"label": "3. Biz Proposal", "template": "Executive proposal: {input}"},
            {"label": "4. Internal Memo", "template": "Official internal memo: {input}"},
            {"label": "5. SOP Workflow", "template": "Step-by-step SOP: {input}"},
            {"label": "6. Press Release", "template": "Corporate press release: {input}"},
            {"label": "7. Agenda Planner", "template": "Efficient meeting agenda: {input}"}
        ],
        "Strategy (Pro)": [
            {"label": "1. OKR Generator", "template": "OKRs and KPIs for: {input}"},
            {"label": "2. SWOT Analysis", "template": "Full SWOT analysis: {input}"},
            {"label": "3. Market Audit", "template": "Competitor market audit: {input}"},
            {"label": "4. Business Canvas", "template": "9-block business model: {input}"},
            {"label": "5. Risk Matrix", "template": "Risk mitigation plan: {input}"},
            {"label": "6. Pitch Structure", "template": "Investor pitch deck: {input}"},
            {"label": "7. Blue Ocean", "template": "Blue ocean strategy for: {input}"}
        ],
        "HR & Team (Pro)": [
            {"label": "1. Performance Review", "template": "Constructive review for: {input}"},
            {"label": "2. Job Description", "template": "Modern job description: {input}"},
            {"label": "3. Onboarding Plan", "template": "30-60-90 day plan: {input}"},
            {"label": "4. Crisis Comms", "template": "Internal crisis message: {input}"},
            {"label": "5. Team Bonding", "template": "Team building strategy: {input}"},
            {"label": "6. Exit Interview", "template": "Exit interview questions: {input}"},
            {"label": "7. Culture Deck", "template": "Company culture manifesto: {input}"}
        ]
    }
}
