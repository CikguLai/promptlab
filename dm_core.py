# dm_core.py
# 核心功能数据 (Roles, Modes, Options, Tones, Intercepts)
# Language: English (Core Logic)

# ==========================================
# 1. 核心功能选项 (6 Roles x 3 Modes x 7 Options = 126 Options)
# ==========================================
RAW_ROLES_DATA = {
    "Global Educator": {
        "Pedagogy (Free)": ["1. Direct Instruction", "2. Gamification", "3. Project-Based Learning", "4. Socratic Method", "5. Flipped Classroom", "6. Differentiated Instruction", "7. Analyze Student Work (OCR)"],
        "Visuals (Pro)": ["1. Pixar/Disney 3D", "2. National Geographic", "3. Minimalist Vector", "4. Vintage Watercolor", "5. Scientific Schematic", "6. Cyberpunk Concept"],
        "Comm (Pro)": ["1. Parent Message", "2. Behavior Report", "3. Official Proposal", "4. Classroom Newsletter", "5. Event Invitation", "6. Grant Application"]
    },
    "Global Creator": {
        "Scripting (Free)": ["1. Visual-to-Script", "2. Storyboard Outline", "3. Character Backstory", "4. Plot Twist Generator", "5. Dialogue Enhancer", "6. World Building"],
        "Copywriting (Pro)": ["1. Viral Hook (TickTok/Reels)", "2. SEO Blog Post", "3. Sales Landing Page", "4. Email Drip Campaign", "5. Press Release", "6. Ad Copy (FB/IG)"],
        "Art Direction (Pro)": ["1. Midjourney Prompts", "2. Stable Diffusion Specs", "3. Logo Design Brief", "4. UI/UX Concept", "5. Fashion Moodboard", "6. Game Asset Specs"]
    },
    "Global Parent": {
        "Activities (Free)": ["1. Rainy Day Games", "2. DIY Science Experiments", "3. Bedtime Story Generator", "4. Homework Helper Strategy", "5. Kids Party Planner", "6. Lunchbox Ideas"],
        "Guidance (Pro)": ["1. Digital Safety Talk", "2. Puberty Conversation", "3. Bullying Advice", "4. University Planning", "5. Financial Literacy for Kids", "6. Screen Time Contract"],
        "Family Mgmt (Pro)": ["1. Weekly Meal Prep", "2. Vacation Itinerary", "3. Chore Chart System", "4. Family Budget", "5. Emergency Plan", "6. Gift Organizer"]
    },
    "Global Seller": {
        "E-Commerce (Free)": ["1. Product Description", "2. Amazon Bullet Points", "3. FAQ Generator", "4. Review Response", "5. Shopify SEO Title", "6. Unboxing Script"],
        "Marketing (Pro)": ["1. Influencer Outreach", "2. Black Friday Strategy", "3. Retargeting Ad Text", "4. Brand Story", "5. Competitor Analysis", "6. Customer Avatar"],
        "Support (Pro)": ["1. Refund Negotiation", "2. Crisis Management", "3. Loyalty Program Rules", "4. Chatbot Scripts", "5. Training Manual", "6. Feedback Survey"]
    },
    "Global Student": {
        "Study (Free)": ["1. Summarize Text", "2. Flashcard Generator", "3. Essay Outliner", "4. Citation Formatter", "5. Complex Topic Simplifier", "6. Presentation Script"],
        "Research (Pro)": ["1. Literature Review", "2. Methodology Suggestions", "3. Data Analysis Plan", "4. Thesis Statement", "5. Research Gap Finder", "6. Abstract Writer"],
        "Career (Pro)": ["1. Resume/CV Polish", "2. Cover Letter", "3. Interview Mock Q&A", "4. LinkedIn Bio", "5. Networking Email", "6. Portfolio Description"]
    },
    "Global Corporate": {
        "Productivity (Free)": ["1. Meeting Minutes", "2. Email Polisher", "3. Task Prioritization", "4. Project Roadmap", "5. OKR Generator", "6. SWOT Analysis"],
        "Strategy (Pro)": ["1. Market Entry Plan", "2. Risk Assessment", "3. Pitch Deck Outline", "4. Change Management", "5. Quarter Review", "6. M&A Due Diligence"],
        "HR & Team (Pro)": ["1. Job Description", "2. Onboarding Checklist", "3. Performance Review", "4. Team Building Event", "5. Conflict Resolution", "6. Internal Memo"]
    }
}

# ==========================================
# 2. 角色语调 (Tones)
# ==========================================
ROLE_TONES = {
    "Global Educator": ["🎓 Encouraging", "📚 Academic", "💡 Inspiring", "🧠 Analytical", "🧸 Playful (Kids)", "⚡ Strict", "🗣️ Storyteller", "🤝 Collaborative", "📝 Formal", "🌍 Culturally Aware"],
    "Global Creator": ["🎨 Creative", "🔥 Viral/Hype", "📖 Narrative", "🤪 Humorous", "🎬 Cinematic", "💡 Minimalist", "📢 Persuasive", "🕶️ Edgy", "💖 Emotional", "🤖 Tech-Savvy"],
    "Global Parent": ["❤️ Nurturing", "🛡️ Protective", "🧸 Playful", "🗣️ Firm", "🤝 Understanding", "🧠 Educational", "🧘 Calm", "⚡ Energetic", "📖 Storytelling", "💡 Practical"],
    "Global Seller": ["💰 Persuasive", "📢 Urgent (FOMO)", "🤝 Trustworthy", "😎 Professional", "🔥 Hype", "📊 Data-Driven", "❤️ Empathetic", "⚡ Direct", "🌟 Luxury", "🤓 Technical"],
    "Global Student": ["🎓 Formal", "📝 Concise", "🤓 Geeky", "🎯 Goal-Oriented", "📚 Detailed", "🤔 Critical", "⚡ Quick", "🧠 Deep", "🗣️ Argumentative", "📝 Note-taking"],
    "Global Corporate": ["👔 Executive", "⚡ Direct", "🚀 Strategic", "⚖️ Compliance", "🤝 Diplomatic", "📊 Analytical", "📢 PR-Safe", "💼 Professional", "🗣️ Leadership", "🌍 Global"]
}
DEFAULT_TONES = ["Professional", "Friendly", "Informative"]

# ==========================================
# 3. 智能拦截逻辑 (Intercept Logic) - 匹配 16 FAQ
# ==========================================
# 顺序对应 dm_data.py 中的 FAQ 顺序 (0-15)
INTERCEPT_LOGIC = [
    (["subscription", "monthly", "fee", "订阅", "月费"], 0), 
    (["refund", "money", "back", "return", "退款", "退钱"], 1),
    (["key", "license", "code", "lost", "forgot", "激活码", "丢失"], 2), 
    (["device", "mobile", "phone", "desktop", "设备", "手机"], 3),
    (["affiliate", "partner", "commission", "program", "分销", "佣金"], 4), 
    (["invoice", "receipt", "bill", "发票", "收据"], 5),
    (["school", "student", "bulk", "discount", "教育", "团购"], 6), 
    (["pdf", "font", "garbled", "character", "乱码", "字体"], 7),
    (["wechat", "share", "weixin", "moment", "微信", "分享"], 8),
    (["invalid", "error", "activate", "not working", "无效", "报错"], 9),
    (["slow", "speed", "lag", "waiting", "慢", "速度", "卡"], 10),
    (["unlimited", "limit", "cap", "quota", "无限", "限制"], 11),
    (["commercial", "sell", "business", "copyright", "rights", "商用", "版权"], 12),
    (["offline", "internet", "wifi", "connect", "离线", "断网"], 13),
    (["privacy", "data", "store", "save", "隐私", "数据"], 14),
    (["share account", "multiple users", "sharing", "ban", "共享", "共用"], 15)
]

# ==========================================
# 4. 自动生成处理逻辑
# ==========================================
ROLES_CONFIG = {}
for role, modes in RAW_ROLES_DATA.items():
    ROLES_CONFIG[role] = {}
    for mode, options in modes.items():
        ROLES_CONFIG[role][mode] = []
        for opt in options:
            base_opts = [{"label": opt, "template": "{input}"}]
            ROLES_CONFIG[role][mode].extend(base_opts)
        ROLES_CONFIG[role][mode].append({"label": "7. Custom / DIY", "template": "{input}"})
