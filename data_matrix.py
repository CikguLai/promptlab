# data_matrix.py
# Lai's Lab V9.21 - 核心数据库 (1000 Limit Edition)

# ==========================================
# 1. 基础配置
# ==========================================
LANG_OPTIONS_GUEST = ["English", "简体中文", "Español"]

LANG_OPTIONS_PRO = [
    "English", "简体中文", "Español", "Bahasa Melayu", 
    "日本語", "한국어", "Français", "Deutsch", 
    "Italiano", "Português", "Русский", "Arabic", 
    "Hindi", "Thai", "Vietnamese"
]

ROLE_TONES = {
    "Global Educator": ["🌟 Encouraging", "📚 Academic", "🤔 Socratic", "👶 Simple", "📢 Instructional", "🤝 Constructive"],
    "Global Creator": ["🔥 Viral", "👻 Witty", "📖 Storytelling", "⚡ Punchy", "🧐 Controversial", "🎨 Artistic"],
    "Global Parent": ["🥰 Warm", "😴 Calming", "🎉 Playful", "🛡️ Firm", "🧙‍♂️ Magical", "👩‍🏫 Patient"],
    "Global Seller": ["💰 Persuasive", "⏳ Urgent", "💎 Luxury", "🤝 Trustworthy", "🎁 Benefit-Driven", "📣 Loud"],
    "Global Student": ["🎓 Academic", "📝 Concise", "🤔 Critical", "🗣️ Casual", "🤓 Detailed"],
    "Global Corporate": ["👔 Executive", "🤝 Diplomatic", "📊 Data-Driven", "🚀 Motivational", "⚡ Direct", "⚖️ Compliance"]
}
DEFAULT_TONES = ["Professional", "Casual", "Enthusiastic", "Direct"]

LANG_MAP = {
    "default": {
        "sidebar_title": "🧬 Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
        "usage": "Daily Usage", "lang": "🌐 Language", "role": "🎭 Role", "tone": "🗣️ Tone / Style",
        "faq": "❓ FAQ / Help", "support": "🎫 Support Ticket", "logout": "🚪 Logout",
        "mode": "⚙️ Select Mode", "action": "⚡ Select Action", "input_label": "📝 Context / Details",
        "generate": "✨ Generate with PASEC", "lock_msg": "🔒 Locked", "lock_desc": "Upgrade to Pro.",
        "buy_btn": "👉 Get Pro Access", "result": "✨ PASEC Result",
        "ticket_types": ["🔴 Bug/ error report", "🟠 Billing issues", "🟡 Feature Request", "🟢 Partnership/ Sponsorship", "🔵 Other Inquiry"]
    },
    "简体中文": {
        "sidebar_title": "🧬 Lai's Lab", "plan_guest": "访客计划", "plan_pro": "企业版 Pro",
        "usage": "今日用量", "lang": "🌐 语言设置", "role": "🎭 角色选择", "tone": "🗣️ 语气 / 风格",
        "faq": "❓ 常见问题 (FAQ)", "support": "🎫 客服工单", "logout": "🚪 退出登录",
        "mode": "⚙️ 模式选择", "action": "⚡ 执行操作", "input_label": "📝 详细要求",
        "generate": "✨ PASEC 生成", "lock_msg": "🔒 已锁定", "lock_desc": "请升级 Pro 解锁。",
        "buy_btn": "👉 获取 Pro 权限", "result": "✨ PASEC 结构化输出",
        "ticket_types": ["🔴 Bug/ 错误报告", "🟠 账单 / 支付问题", "🟡 功能建议", "🟢 商务合作 / 赞助", "🔵 其他咨询"]
    },
    "Español": {
        "sidebar_title": "🧬 Lai's Lab", "plan_guest": "Plan Invitado", "plan_pro": "Pro Empresa",
        "usage": "Uso Diario", "lang": "🌐 Idioma", "role": "🎭 Rol", "tone": "🗣️ Tono / Estilo",
        "faq": "❓ Preguntas Frecuentes", "support": "🎫 Soporte", "logout": "🚪 Cerrar Sesión",
        "mode": "⚙️ Modo", "action": "⚡ Acción", "input_label": "📝 Contexto",
        "generate": "✨ Generar PASEC", "lock_msg": "🔒 Bloqueado", "lock_desc": "Actualice a Pro.",
        "buy_btn": "👉 Obtener Pro", "result": "✨ Resultado PASEC",
        "ticket_types": ["🔴 Reporte de Bug/Error", "🟠 Problemas de Facturación", "🟡 Solicitud de Función", "🟢 Asociación/Patrocinio", "🔵 Otra Consulta"]
    },
    "Bahasa Melayu": {
        "sidebar_title": "🧬 Lai's Lab", "plan_guest": "Pelan Tetamu", "plan_pro": "Pro Enterprise",
        "usage": "Penggunaan", "lang": "🌐 Bahasa", "role": "🎭 Peranan", "tone": "🗣️ Nada / Gaya",
        "faq": "❓ Soalan Lazim", "support": "🎫 Tiket Bantuan", "logout": "🚪 Log Keluar",
        "mode": "⚙️ Pilih Mod", "action": "⚡ Pilih Tindakan", "input_label": "📝 Konteks / Butiran",
        "generate": "✨ Jana PASEC", "lock_msg": "🔒 Dikunci", "lock_desc": "Naik taraf ke Pro.",
        "buy_btn": "👉 Dapatkan Pro", "result": "✨ Keputusan PASEC",
        "ticket_types": ["🔴 Lapor Bug", "🟠 Isu Bil", "🟡 Cadangan Fitur", "🟢 Perkongsian", "🔵 Lain-lain"]
    }
}

# 智能拦截源 (FAQ 更新)
RAW_FAQ_DATA = [
    {"q": "Is it free?", "a": "Yes, Guest plan is free forever (5/day).", "kw": ["free", "charge", "trial", "cost"]},
    {"q": "Pro Cost?", "a": "$12.90 Lifetime (Limited Time Offer).", "kw": ["price", "subscription", "monthly", "12.90"]},
    {"q": "Refund Policy?", "a": "⚠️ No Refunds Policy: Digital license keys are non-refundable.", "kw": ["refund", "money", "back", "return"]},
    {"q": "Lost Key?", "a": "🔑 Lost Key? Visit [LemonSqueezy My Orders](https://app.lemonsqueezy.com/my-orders).", "kw": ["key", "lost", "code", "license"]},
    {"q": "Billing Issue?", "a": "🟠 Billing is handled by LemonSqueezy.", "kw": ["billing", "invoice", "receipt"]},
    {"q": "Commercial Use?", "a": "Pro Users: Yes (100% Rights). Guest: No.", "kw": ["commercial", "copyright", "sell", "business"]},
    {"q": "API Access?", "a": "Not available in V9.", "kw": ["api", "developer", "integrate"]},
    {"q": "Partnership?", "a": "🟢 Submit a ticket with 'Partnership' type.", "kw": ["team", "bulk", "school", "partner"]},
    {"q": "Privacy?", "a": "We do not store your inputs.", "kw": ["privacy", "data", "store"]},
    {"q": "History?", "a": "Saved locally in browser cache only.", "kw": ["history", "log", "record"]},
    {"q": "Languages?", "a": "15+ Global Languages in Pro.", "kw": ["language", "chinese", "spanish"]},
    {"q": "PDF/Font?", "a": "📄 Font Issue: Missing system font. Wait for update.", "kw": ["pdf", "font", "box", "square"]},
    {"q": "Watermark?", "a": "Pro has NO watermark.", "kw": ["watermark", "logo", "remove"]},
    # ✅ 修改：明确写出 Pro 限制 1000 次
    {"q": "Daily Limit?", "a": "Guest: 5/day. Pro: 1000/day (Fair Use).", "kw": ["limit", "quota", "stuck", "stop"]},
    {"q": "Payment?", "a": "Cards, PayPal, Apple Pay.", "kw": ["pay", "card", "paypal"]},
    {"q": "Mobile?", "a": "Works on all mobile browsers.", "kw": ["mobile", "phone", "android", "ios"]},
    {"q": "Support?", "a": "Pro: 1-2 Days. Guest: 3-5 Days.", "kw": ["support", "help", "time"]},
    {"q": "WeChat?", "a": "💬 WeChat: Copy link manually.", "kw": ["wechat", "weixin"]}
]

FAQ_LIST = [f"{i+1}. {item['q']} {item['a']}" for i, item in enumerate(RAW_FAQ_DATA)]
INTERCEPTORS = {}
for item in RAW_FAQ_DATA:
    for keyword in item['kw']:
        INTERCEPTORS[keyword] = item['a']

# Prompt 矩阵 (保持不变)
ROLES_CONFIG = {
    "Global Educator": {
        "Pedagogy (Free)": [
            {"label": "1. Rubric Creator (评分标准)", "template": "Create a detailed grading rubric for: {input}. Include columns for Criteria, Excellent, Good, and Needs Improvement."},
            {"label": "2. Direct Instruction", "template": "Design a Direct Instruction lesson plan for: {input}. Include Objective, Input, Modeling, and Independent Practice."},
            {"label": "3. Gamification", "template": "Create a gamification strategy to teach: {input}. Include game mechanics, rewards, and learning objectives."},
            {"label": "4. Project-Based Learning", "template": "Design a PBL project for: {input}. Include Driving Question, Project Milestones, and Final Public Product."},
            {"label": "5. Socratic Method", "template": "Generate a list of deep, open-ended Socratic questions to guide discussion on: {input}."},
            {"label": "6. Flipped Classroom", "template": "Plan a Flipped Classroom module for: {input}. List pre-class videos/readings and in-class active learning activities."},
            {"label": "7. Custom (自定义)", "template": "Act as an expert educator. {input}"}
        ],
        "Visuals (Pro)": [
            {"label": "1. Pixar/Disney 3D", "template": "Midjourney prompt for Pixar-style 3D animation: {input}"},
            {"label": "2. National Geographic", "template": "Midjourney prompt for NatGeo style photo: {input}"},
            {"label": "3. Minimalist Vector", "template": "Prompt for flat vector illustration: {input}"},
            {"label": "4. Vintage Watercolor", "template": "Prompt for vintage watercolor: {input}"},
            {"label": "5. Scientific Schematic", "template": "Prompt for scientific diagram: {input}"},
            {"label": "6. Cyberpunk Concept", "template": "Prompt for cyberpunk concept art: {input}"}
        ],
        "Comm (Pro)": [
            {"label": "1. Parent Message", "template": "Draft a message to a parent about: {input}"},
            {"label": "2. Behavior Report", "template": "Write a student behavior report: {input}"},
            {"label": "3. Official Proposal", "template": "Write a school proposal for: {input}"},
            {"label": "4. Newsletter", "template": "Draft a newsletter section: {input}"},
            {"label": "5. Event Invitation", "template": "Write an event invitation: {input}"},
            {"label": "6. Grant Application", "template": "Draft a grant application for: {input}"}
        ]
    },
    "Global Creator": {
        "Scripting (Free)": [
            {"label": "1. Viral Hook Generator", "template": "Generate 10 viral video hooks for: {input}"},
            {"label": "2. TikTok/Reels Script", "template": "Write a 60s video script for: {input}"},
            {"label": "3. YouTube Edutainment", "template": "Outline a YouTube educational script: {input}"},
            {"label": "4. Storytelling Vlog", "template": "Write a vlog voiceover: {input}"},
            {"label": "5. Podcast Interview", "template": "Podcast interview questions for: {input}"},
            {"label": "6. Live Stream Flow", "template": "Live stream run-of-show for: {input}"},
            {"label": "7. Custom", "template": "Script for: {input}"}
        ],
        "Thumbnail (Pro)": [
            {"label": "1. High CTR (Shocked)", "template": "Thumbnail prompt with shocked expression: {input}"},
            {"label": "2. Cinematic Poster", "template": "Movie poster style thumbnail prompt: {input}"},
            {"label": "3. Tech/Neon", "template": "Tech review thumbnail prompt: {input}"},
            {"label": "4. Before & After", "template": "Split screen comparison thumbnail prompt: {input}"},
            {"label": "5. Minimalist Apple", "template": "Clean minimalist thumbnail prompt: {input}"},
            {"label": "6. Comic Book", "template": "Comic style thumbnail prompt: {input}"}
        ],
        "Marketing (Pro)": [
            {"label": "1. Xiaohongshu (KOC)", "template": "Write a Xiaohongshu post with emojis: {input}"},
            {"label": "2. Instagram Caption", "template": "Engaging IG caption for: {input}"},
            {"label": "3. Facebook Ad", "template": "FB Ad copy for: {input}"},
            {"label": "4. LinkedIn Leader", "template": "LinkedIn thought leadership post: {input}"},
            {"label": "5. Twitter Thread", "template": "Viral Twitter thread about: {input}"},
            {"label": "6. Email Newsletter", "template": "Newsletter segment about: {input}"}
        ]
    },
    "Global Parent": {
        "Story Time (Free)": [
            {"label": "1. 'My Day' Magic", "template": "Turn this daily event into a magical story: {input}"},
            {"label": "2. Bedtime Story", "template": "Calming bedtime story about: {input}"},
            {"label": "3. Hero's Journey", "template": "Story where the child is the hero: {input}"},
            {"label": "4. Social Emotional", "template": "Story teaching a lesson about: {input}"},
            {"label": "5. Science 'Why'", "template": "Explain science through a story: {input}"},
            {"label": "6. Cultural Tale", "template": "Retell a cultural story: {input}"},
            {"label": "7. Custom", "template": "Story about: {input}"}
        ],
        "Activities (Pro)": [
            {"label": "1. DIY Craft Guide", "template": "DIY craft guide using: {input}"},
            {"label": "2. Rainy Day Game", "template": "Indoor game suggestion: {input}"},
            {"label": "3. Kitchen Science", "template": "Safe kitchen experiment: {input}"},
            {"label": "4. Scavenger Hunt", "template": "Scavenger hunt list for: {input}"},
            {"label": "5. Family Bonding", "template": "No-screen bonding activity: {input}"},
            {"label": "6. No-Screen Coding", "template": "Logic game teaching: {input}"}
        ],
        "Tutor (Pro)": [
            {"label": "1. Mnemonic Generator", "template": "Create a mnemonic for: {input}"},
            {"label": "2. Feynman Technique", "template": "Explain simply as if to a 5-year old: {input}"},
            {"label": "3. Homework Helper", "template": "Guide to solve (no answers): {input}"},
            {"label": "4. Quiz Generator", "template": "5 practice questions on: {input}"},
            {"label": "5. Vocabulary Builder", "template": "Define and explain word: {input}"},
            {"label": "6. Essay Proofreader", "template": "Proofread this text: {input}"}
        ]
    },
    "Global Seller": {
        "Copywriting (Free)": [
            {"label": "1. Landing Page", "template": "Landing page structure for: {input}"},
            {"label": "2. PAS Model", "template": "PAS sales copy for: {input}"},
            {"label": "3. AIDA Model", "template": "AIDA sales copy for: {input}"},
            {"label": "4. FAB Model", "template": "FAB analysis for: {input}"},
            {"label": "5. Storytelling", "template": "Brand story for: {input}"},
            {"label": "6. Objection Handling", "template": "Handle objection: {input}"},
            {"label": "7. Custom", "template": "Sales copy for: {input}"}
        ],
        "Product Shot (Pro)": [
            {"label": "1. Studio White BG", "template": "Prompt for studio product shot: {input}"},
            {"label": "2. Lifestyle Home", "template": "Prompt for lifestyle shot: {input}"},
            {"label": "3. Luxury Gold", "template": "Prompt for luxury black/gold shot: {input}"},
            {"label": "4. Nature Light", "template": "Prompt for nature sunlight shot: {input}"},
            {"label": "5. Cyberpunk", "template": "Prompt for cyberpunk product shot: {input}"},
            {"label": "6. Flat Lay", "template": "Prompt for flat lay knolling: {input}"}
        ],
        "Support (Pro)": [
            {"label": "1. Apology Email", "template": "Apology email for: {input}"},
            {"label": "2. Review Request", "template": "Review request email for: {input}"},
            {"label": "3. Complaint Reply", "template": "Reply to complaint: {input}"},
            {"label": "4. Promo Announce", "template": "Promo announcement: {input}"},
            {"label": "5. Crisis Statement", "template": "Public crisis statement: {input}"},
            {"label": "6. FAQ Gen", "template": "Generate FAQs for: {input}"}
        ]
    },
    "Global Student": {
        "Study (Free)": [
            {"label": "1. Note Summarizer", "template": "Summarize these notes: {input}"},
            {"label": "2. Feynman Tech", "template": "Explain concept simply: {input}"},
            {"label": "3. Lit Review", "template": "Lit review structure for: {input}"},
            {"label": "4. Flashcard", "template": "Anki flashcards for: {input}"},
            {"label": "5. Simplifier", "template": "Simplify text: {input}"},
            {"label": "6. Translation", "template": "Translate to academic English: {input}"},
            {"label": "7. Custom", "template": "Study help: {input}"}
        ],
        "Project (Pro)": [
            {"label": "1. Essay Outline", "template": "Essay outline for: {input}"},
            {"label": "2. Presentation", "template": "Presentation script for: {input}"},
            {"label": "3. Debate Prep", "template": "Debate arguments for: {input}"},
            {"label": "4. Lab Report", "template": "Lab report outline: {input}"},
            {"label": "5. Methodology", "template": "Research methodology for: {input}"},
            {"label": "6. Group Roles", "template": "Assign group roles for: {input}"}
        ],
        "Career (Pro)": [
            {"label": "1. ATS Resume", "template": "Optimize resume for: {input}"},
            {"label": "2. Cover Letter", "template": "Cover letter for: {input}"},
            {"label": "3. Interview Prep", "template": "Interview Q&A for: {input}"},
            {"label": "4. LinkedIn Bio", "template": "LinkedIn About section for: {input}"},
            {"label": "5. Cold Email", "template": "Cold networking email: {input}"},
            {"label": "6. Portfolio", "template": "Portfolio description for: {input}"}
        ]
    },
    "Global Corporate": {
        "Admin (Free)": [
            {"label": "1. Email Polisher", "template": "Polish this email: {input}"},
            {"label": "2. Meeting Minutes", "template": "Format minutes: {input}"},
            {"label": "3. Proposal", "template": "Business proposal for: {input}"},
            {"label": "4. Internal Memo", "template": "Internal memo about: {input}"},
            {"label": "5. SOP / Process", "template": "Draft SOP for: {input}"},
            {"label": "6. Press Release", "template": "Press release for: {input}"},
            {"label": "7. Custom", "template": "Admin task: {input}"}
        ],
        "Strategy (Pro)": [
            {"label": "1. OKRs", "template": "Generate OKRs for: {input}"},
            {"label": "2. SWOT", "template": "SWOT analysis for: {input}"},
            {"label": "3. Competitor", "template": "Analyze competitor: {input}"},
            {"label": "4. Business Canvas", "template": "Business Model Canvas for: {input}"},
            {"label": "5. Risk Matrix", "template": "Risk matrix for: {input}"},
            {"label": "6. Pitch Deck", "template": "Pitch deck structure for: {input}"}
        ],
        "HR & Team (Pro)": [
            {"label": "1. Performance Review", "template": "Performance review for: {input}"},
            {"label": "2. Job Desc", "template": "Job description for: {input}"},
            {"label": "3. Onboarding", "template": "Onboarding plan for: {input}"},
            {"label": "4. Crisis Comms", "template": "Crisis message: {input}"},
            {"label": "5. Team Building", "template": "Team building activity: {input}"},
            {"label": "6. Termination", "template": "Termination script for: {input}"}
        ]
    }
}

