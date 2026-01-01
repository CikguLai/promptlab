# data_matrix.py
# Lai's Lab V9.32 - FINAL GOLD
# 100% Data: 16 Langs | 126 Options | 16 FAQs | Table Translations

# ==========================================
# 1. 语言定义 (全解锁)
# ==========================================
ALL_LANGUAGES = [
    "English", "简体中文", "繁體中文", "Bahasa Melayu", "Español", 
    "日本語", "한국어", "Français", "Deutsch", 
    "Italiano", "Português", "Русский", "Arabic", 
    "Hindi", "Thai", "Vietnamese"
]

LANG_OPTIONS_GUEST = ALL_LANGUAGES
LANG_OPTIONS_PRO = ALL_LANGUAGES

# ==========================================
# 2. UI 界面字典 (包含 Action Deck & Table Headers)
# ==========================================
BASE_UI = {
    "sidebar_title": "Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
    "usage": "Daily Usage", "lang": "🌐 Interface Lang", "role": "🎭 Role", 
    "logout": "🚪 Logout", "mode": "⚙️ Select Mode", "action": "⚡ Select Action", 
    "input_label": "📝 Input Context", "generate": "✨ Generate Prompt", "lock_msg": "🔒 Locked (Pro Only)", 
    "buy_btn": "👉 Upgrade Now", "result": "✨ Generated Result", "live_stat": "Live Users",
    "faq_title": "❓ FAQ / Support", "quick_ans": "💡 Quick Help", "sel_topic": "Select Question:",
    "submit_ticket": "📩 Submit Ticket", "type_lbl": "Ticket Type", "issue_lbl": "Describe Issue", "send_btn": "Send Ticket",
    "ui_lang_lbl": "🌐 Interface Language", "out_lang_lbl": "📝 Output Language", "tone_lbl": "🗣️ Tone",
    # Layers
    "ad_copy": "Layer 1: Copy Code (Click 📋 top-right)", 
    "ad_connect": "Layer 2: Direct AI Login", 
    "ad_social": "Layer 3: Social Share", 
    "ad_manual": "Layer 4: App Guides", 
    "ad_download": "Layer 5: Download & Export",
    "ad_locked": "🔒 Upgrade to Pro to unlock",
    # Table Headers
    "tbl_head": ["Feature", "Guest", "Pro Lifetime"]
}

# 中文覆盖 (示例，其他语言可依此类推扩展)
CN_UI = BASE_UI.copy()
CN_UI.update({
    "sidebar_title": "Lai's Lab", "plan_guest": "访客试用", "plan_pro": "企业版 Pro",
    "usage": "今日用量", "lang": "🌐 界面语言", "role": "🎭 角色选择",
    "logout": "🚪 退出", "mode": "⚙️ 模式选择", "action": "⚡ 执行操作",
    "input_label": "📝 输入详细要求", "generate": "✨ 生成提示词", "lock_msg": "🔒 该模式已上锁 (Pro)",
    "buy_btn": "👉 立即升级", "result": "✨ 生成结果", "live_stat": "在线人数",
    "faq_title": "❓ 常见问题 / 客服", "quick_ans": "💡 快速查询", "sel_topic": "选择问题:",
    "submit_ticket": "📩 提交工单", "type_lbl": "问题类型", "issue_lbl": "详细描述", "send_btn": "发送工单",
    "ui_lang_lbl": "🌐 界面语言", "out_lang_lbl": "📝 AI输出语言", "tone_lbl": "🗣️ 语气口吻",
    "ad_copy": "Layer 1: 复制 (点击代码框右上角 📋)", 
    "ad_connect": "Layer 2: AI 直连跳转", 
    "ad_social": "Layer 3: 社交分享", 
    "ad_manual": "Layer 4: App 使用教程", 
    "ad_download": "Layer 5: 下载与导出",
    "ad_locked": "🔒 升级 Pro 解锁此功能",
    "tbl_head": ["核心功能", "访客", "Pro 永久版"]
})

# 建立全语言映射
UI_TRANSLATIONS = {}
for l in ALL_LANGUAGES: UI_TRANSLATIONS[l] = BASE_UI
UI_TRANSLATIONS["简体中文"] = CN_UI
UI_TRANSLATIONS["繁體中文"] = CN_UI 

def get_safe_ui(lang): return UI_TRANSLATIONS.get(lang, BASE_UI)

# ==========================================
# 3. 对比表数据 (Compare Plans)
# ==========================================
# 英文标准数据
TBL_KEYS = ["Daily Limit", "Content Format", "Sharing", "Languages", "Expert Modes", "Watermark", "Support", "Price"]
TBL_VALS_GUEST = ["5 / Day", "With Symbols", "Text Only", "16+ Global", "Basic (6)", "Forced", "Standard", "Free"]
TBL_VALS_PRO = ["*Unlimited", "100% Clean", "PDF + Clean", "16+ Global", "All 18+", "Removed", "VIP Priority", "$12.90"]

# 中文标准数据
TBL_KEYS_CN = ["每日限额", "内容纯净度", "分享形式", "语言支持", "专业模式", "水印", "客服响应", "价格"]
TBL_VALS_GUEST_CN = ["5次 / 天", "含AI符号", "仅文本", "16+ 全球", "基础 (6个)", "强制显示", "标准", "免费"]
TBL_VALS_PRO_CN = ["*无限生成", "100% 纯净", "PDF + 纯净", "16+ 全球", "全套 18+", "移除", "VIP 优先", "$12.90"]

def get_table_data(lang):
    # 默认英文
    ks, vg, vp = TBL_KEYS, TBL_VALS_GUEST, TBL_VALS_PRO
    ui = get_safe_ui(lang)
    
    # 中文特殊处理
    if lang in ["简体中文", "繁體中文"]:
        ks, vg, vp = TBL_KEYS_CN, TBL_VALS_GUEST_CN, TBL_VALS_PRO_CN
    
    # 构建 Rows
    rows = []
    for i in range(len(ks)):
        rows.append({"k": ks[i], "v1": vg[i], "v2": vp[i]})
    
    return ui["tbl_head"], rows

TABLE_ROWS_DEFAULT = get_table_data("English")[1]

# ==========================================
# 4. 16个 FAQ (硬编码，防止乱码)
# ==========================================
FAQ_EN = [
    {"q": "Q1: Is it a subscription?", "a": "No. It is a one-time payment for lifetime access."},
    {"q": "Q2: Can I get a refund?", "a": "Digital goods are non-refundable once the key is revealed."},
    {"q": "Q3: Lost my license key?", "a": "Use the 'Lost Key' link on LemonSqueezy order page."},
    {"q": "Q4: How many devices?", "a": "You can use it on multiple personal devices."},
    {"q": "Q5: Is there an affiliate program?", "a": "Yes, we offer 40% commission. Contact us."},
    {"q": "Q6: Where is my invoice?", "a": "It is automatically sent to your email after purchase."},
    {"q": "Q7: Bulk purchase for schools?", "a": "Contact support@cikgulai.com for edu discounts."},
    {"q": "Q8: PDF text is garbled?", "a": "Please install the font.ttf file in the app directory."},
    {"q": "Q9: How to share to WeChat?", "a": "Copy the text and paste it manually into WeChat."},
    {"q": "Q10: Invalid License Key?", "a": "Check for extra spaces. Keys are case-sensitive."},
    {"q": "Q11: Generation is slow?", "a": "Guest queue is shared. Pro users have dedicated servers."},
    {"q": "Q12: Is it truly unlimited?", "a": "Text generation is unlimited. Fair use applies."},
    {"q": "Q13: Commercial use?", "a": "Pro users have full commercial rights to the prompts."},
    {"q": "Q14: Offline mode?", "a": "No, an internet connection is required."},
    {"q": "Q15: Is my data safe?", "a": "We do not store your prompt inputs permanently."},
    {"q": "Q16: Can I share my account?", "a": "Account sharing is prohibited and may lead to a ban."}
]

FAQ_CN = [
    {"q": "问1: 是订阅制吗？", "a": "不是。一次性付费，永久使用。"},
    {"q": "问2: 可以退款吗？", "a": "虚拟商品一旦发出激活码，不支持退款。"},
    {"q": "问3: 激活码丢了？", "a": "请通过 LemonSqueezy 订单页找回。"},
    {"q": "问4: 支持多少设备？", "a": "支持个人多设备使用。"},
    {"q": "问5: 有分销计划吗？", "a": "有，提供 40% 佣金，请联系我们。"},
    {"q": "问6: 发票在哪里？", "a": "购买后会自动发送到您的邮箱。"},
    {"q": "问7: 学校团购？", "a": "教育采购请联系客服获取优惠。"},
    {"q": "问8: PDF乱码？", "a": "请确保服务器已安装 font.ttf 字体文件。"},
    {"q": "问9: 怎么分享到微信？", "a": "点击复制，然后手动粘贴到微信。"},
    {"q": "问10: 激活码无效？", "a": "请检查前后空格，区分大小写。"},
    {"q": "问11: 生成速度慢？", "a": "Pro 用户拥有优先生成通道。"},
    {"q": "问12: 真的无限吗？", "a": "文本生成无限。遵循公平使用原则。"},
    {"q": "问13: 可以商用吗？", "a": "Pro 用户拥有生成内容的完整商用权。"},
    {"q": "问14: 支持离线吗？", "a": "不支持，需要联网。"},
    {"q": "问15: 数据隐私？", "a": "我们不会永久存储您的输入数据。"},
    {"q": "问16: 共享账号？", "a": "禁止共享账号，违者可能封号。"}
]

FAQ_DATABASE = {}
for l in ALL_LANGUAGES: FAQ_DATABASE[l] = FAQ_EN
FAQ_DATABASE["简体中文"] = FAQ_CN
FAQ_DATABASE["繁體中文"] = FAQ_CN

# Ticket 下拉菜单
TICKET_OPTIONS = {
    "English": ["🔴 Bug Report", "🟠 Billing Issue", "🟡 Feature Request", "🟢 Partnership", "🔵 Other"],
    "简体中文": ["🔴 程序报错", "🟠 账单问题", "🟡 功能建议", "🟢 商务合作", "🔵 其他"]
}
def get_ticket_types(lang): return TICKET_OPTIONS.get(lang, TICKET_OPTIONS["English"])

# ==========================================
# 5. 126 功能点 (结构化全量)
# ==========================================
RAW_ROLES_DATA = {
    "Global Educator": {
        "Pedagogy (Free)": ["1. Direct Instruction", "2. Gamification", "3. Project-Based Learning", "4. Socratic Method", "5. Flipped Classroom", "6. Differentiated Instruction", "7. Analyze Student Work (OCR)"],
        "Visuals (Pro)": ["1. Pixar/Disney 3D", "2. National Geographic", "3. Minimalist Vector", "4. Vintage Watercolor", "5. Scientific Schematic", "6. Cyberpunk Concept"],
        "Comm (Pro)": ["1. Parent Message", "2. Behavior Report", "3. Official Proposal", "4. Classroom Newsletter", "5. Event Invitation", "6. Grant Application"]
    },
    "Global Creator": {
        "Scripting (Free)": ["1. Visual-to-Script", "2. TikTok/Reels Hook", "3. YouTube Edutainment", "4. Storytelling Vlog", "5. Podcast Interview", "6. Live Stream Flow"],
        "Thumbnail (Pro)": ["1. High CTR (Shocked)", "2. Cinematic Poster", "3. Tech/Neon/Glowing", "4. Before & After", "5. Minimalist Apple", "6. Comic Book Style"],
        "Marketing (Pro)": ["1. Xiaohongshu (KOC)", "2. Instagram Caption", "3. Facebook Ad", "4. LinkedIn Leader", "5. Twitter Thread", "6. Email Newsletter"]
    },
    "Global Parent": {
        "Story Time (Free)": ["1. From Drawing", "2. Bedtime Story", "3. Hero's Journey", "4. Social Emotional", "5. Science 'Why'", "6. Cultural Tale"],
        "Activities (Pro)": ["1. DIY Craft Guide", "2. Rainy Day Game", "3. Kitchen Science", "4. Scavenger Hunt", "5. Family Bonding", "6. No-Screen Coding"],
        "Tutor (Pro)": ["1. Solve Problem (OCR)", "2. Feynman Technique", "3. Homework Helper", "4. Quiz Generator", "5. Vocabulary Builder", "6. Essay Proofreader"]
    },
    "Global Seller": {
        "Copywriting (Free)": ["1. Product Desc (OCR)", "2. PAS Model", "3. AIDA Model", "4. FAB Model", "5. Storytelling Sales", "6. Objection Handling"],
        "Product Shot (Pro)": ["1. Studio White BG", "2. Lifestyle Home", "3. Luxury Gold/Black", "4. Nature/Sunlight", "5. Cyberpunk/Tech", "6. Flat Lay"],
        "Support (Pro)": ["1. Apology & Recovery", "2. Review Request", "3. Complaint Reply", "4. Promo Announcement", "5. Crisis Statement", "6. FAQ Gen"]
    },
    "Global Student": {
        "Study (Free)": ["1. Explain Chart (OCR)", "2. Feynman Technique", "3. Lit Review Matrix", "4. Flashcard (Anki)", "5. Concept Simplifier", "6. Translation"],
        "Project (Pro)": ["1. Essay Outline", "2. Presentation Script", "3. Debate Prep", "4. Lab Report", "5. Methodology", "6. Group Roles"],
        "Career (Pro)": ["1. ATS Resume", "2. Cover Letter", "3. Interview Prep", "4. LinkedIn Bio", "5. Cold Email", "6. Portfolio Desc"]
    },
    "Global Corporate": {
        "Admin (Free)": ["1. Extract Data (OCR)", "2. Meeting Minutes", "3. Official Proposal", "4. Internal Memo", "5. SOP / Process", "6. Press Release"],
        "Strategy (Pro)": ["1. OKRs", "2. SWOT Analysis", "3. Competitor Dive", "4. Business Canvas", "5. Risk Matrix", "6. Pitch Deck"],
        "HR & Team (Pro)": ["1. Performance Review", "2. Job Desc (JD)", "3. Onboarding Plan", "4. Crisis Comms", "5. Team Building", "6. Termination"]
    }
}

ROLES_CONFIG = {}
for role, modes in RAW_ROLES_DATA.items():
    ROLES_CONFIG[role] = {}
    for mode_name, options in modes.items():
        ROLES_CONFIG[role][mode_name] = []
        for opt in options:
            template = f"Act as a {role}. Mode: {mode_name}. Task: {opt}. Context: {{input}}"
            ROLES_CONFIG[role][mode_name].append({"label": opt, "template": template})
        ROLES_CONFIG[role][mode_name].append({"label": "7. Custom / DIY", "template": "{input}"})

ROLE_TONES = {
    "Global Educator": ["📚 Academic", "🌟 Encouraging", "📢 Instructional", "🤝 Patient", "💡 Socratic", "🧠 Cognitive", "✨ Storytelling", "🎯 Objective", "🌈 Inclusive", "🔥 Passionate"],
    "Global Creator": ["🔥 Viral", "😜 Witty", "📖 Narrative", "⚡ Punchy", "🧐 Controversial", "🎨 Artistic", "📱 Trendy", "🎥 Cinematic", "🎭 Dramatic", "🤖 Minimalist"],
    "Global Parent": ["🥰 Warm", "🎉 Playful", "🛡️ Firm", "👩‍🏫 Patient", "🤝 Supportive", "🧘 Calm", "🎈 Creative", "📖 Storyteller", "🩺 Caregiver", "🎓 Mentor"],
    "Global Seller": ["💰 Persuasive", "⏳ Urgent", "💎 Luxury", "🤝 Trustworthy", "📢 Hype", "📊 Data-Driven", "🎯 Targeted", "🗣️ Conversational", "🔥 Aggressive", "✨ Solution"],
    "Global Student": ["🎓 Formal", "📝 Concise", "🤓 Geeky", "🎯 Goal-Oriented", "📚 Detailed", "🤔 Critical", "⚡ Quick", "🧠 Deep", "🗣️ Argumentative", "📝 Note-taking"],
    "Global Corporate": ["👔 Executive", "⚡ Direct", "🚀 Strategic", "⚖️ Compliance", "🤝 Diplomatic", "📊 Analytical", "📢 PR-Safe", "💼 Professional", "🗣️ Leadership", "🌍 Global"]
}
DEFAULT_TONES = ["Professional", "Friendly", "Informative"]

# 智能拦截 (用于邮件分流)
INTERCEPT_LOGIC = [
    (["subscription", "monthly", "fee", "订阅", "月费"], 0), (["refund", "money", "back", "退款", "退钱"], 1),
    (["key", "license", "code", "lost", "激活码", "丢失"], 2), (["device", "mobile", "phone", "设备", "手机"], 3),
    (["affiliate", "partner", "commission", "分销", "佣金"], 4), (["invoice", "receipt", "bill", "发票", "收据"], 5),
    (["school", "student", "bulk", "教育", "团购"], 6), (["pdf", "font", "box", "乱码", "字体"], 7),
    (["wechat", "share", "微信", "分享"], 8), (["invalid", "error", "activate", "无效", "错误"], 9),
    (["slow", "speed", "wait", "慢", "卡"], 10), (["limit", "quota", "unlimited", "限制", "无限"], 11),
    (["commercial", "business", "商用", "版权"], 12), (["offline", "internet", "离线", "断网"], 13),
    (["privacy", "store", "data", "隐私", "保存"], 14), (["share account", "sharing", "login", "共享", "封号"], 15)
]
