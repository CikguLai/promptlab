# data_matrix.py
# Lai's Lab V9.28 - 2026 Ready (16 Languages incl. TC)
# Full Commercial Edition: 126 Modes | 60 Tones | 16 Lang UI

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
# 2. 对比表数据 (关键语言本地化)
# ==========================================
TABLE_EN = [
    {"k": "Daily Limit", "v1": "5 / Day", "v2": "*Unlimited"},
    {"k": "Content Format", "v1": "With AI Symbols", "v2": "100% Clean & Human"},
    {"k": "Sharing", "v1": "Text + Watermark", "v2": "PDF + Clean Share"},
    {"k": "Languages", "v1": "3 Basic", "v2": "16+ Global"},
    {"k": "Expert Modes", "v1": "Basic (6)", "v2": "All 18 Depth Modes"},
    {"k": "Watermark", "v1": "Forced", "v2": "Removed"},
    {"k": "Support", "v1": "Standard", "v2": "VIP Priority"},
    {"k": "Price", "v1": "Free", "v2": "Limited $12.90"}
]
TABLE_CN = [
    {"k": "每日生成限额", "v1": "5 次 / 天", "v2": "*Unlimited (无限)"},
    {"k": "内容纯净度", "v1": "含 AI 符号", "v2": "100% 纯净拟人"},
    {"k": "分享与导出", "v1": "带水印文本", "v2": "PDF + 纯净分享"},
    {"k": "全球语言", "v1": "仅 3 种", "v2": "16+ 全球全开"},
    {"k": "专业模式", "v1": "基础 (6个)", "v2": "全部 18 种深度模式"},
    {"k": "结果水印", "v1": "强制显示", "v2": "完全移除"},
    {"k": "客服响应", "v1": "标准速度", "v2": "VIP 极速通道"},
    {"k": "价格", "v1": "免费", "v2": "特惠 $12.90"}
]
# ✅ 新增：繁体中文表格
TABLE_TC = [
    {"k": "每日生成限額", "v1": "5 次 / 天", "v2": "*Unlimited (無限)"},
    {"k": "內容純淨度", "v1": "含 AI 符號", "v2": "100% 純淨擬人"},
    {"k": "分享與導出", "v1": "帶浮水印文本", "v2": "PDF + 純淨分享"},
    {"k": "全球語言", "v1": "僅 3 種", "v2": "16+ 全球全開"},
    {"k": "專業模式", "v1": "基礎 (6個)", "v2": "全部 18 種深度模式"},
    {"k": "結果浮水印", "v1": "強制顯示", "v2": "完全移除"},
    {"k": "客服響應", "v1": "標準速度", "v2": "VIP 極速通道"},
    {"k": "價格", "v1": "免費", "v2": "特惠 $12.90"}
]

# ==========================================
# 3. 16 国语言 UI 完整映射 (全覆盖)
# ==========================================
LANG_MAP = {
    "default": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
        "usage": "Daily Usage", "lang": "🌐 Language", "role": "🎭 Role", "tone": "🗣️ Tone Style",
        "logout": "🚪 Logout", "mode": "⚙️ Select Mode", "action": "⚡ Select Action", 
        "input_label": "📝 Context", "generate": "✨ Generate", "lock_msg": "🔒 Locked (Pro Only)", 
        "buy_btn": "👉 Upgrade to Pro", "result": "✨ Result", "live_stat": "Live Status",
        "tbl_headers": ["Capability", "Guest", "💎 PRO Lifetime"], "tbl_data": TABLE_EN
    },
    "English": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
        "usage": "Daily Usage", "lang": "🌐 Language", "role": "🎭 Role", "tone": "🗣️ Tone Style",
        "logout": "🚪 Logout", "mode": "⚙️ Select Mode", "action": "⚡ Select Action", 
        "input_label": "📝 Context", "generate": "✨ Generate", "lock_msg": "🔒 Locked (Pro Only)", 
        "buy_btn": "👉 Upgrade to Pro", "result": "✨ Result", "live_stat": "Live Status",
        "tbl_headers": ["Capability", "Guest", "💎 PRO Lifetime"], "tbl_data": TABLE_EN
    },
    "简体中文": {
        "sidebar_title": "Lai's Lab", "plan_guest": "访客计划", "plan_pro": "企业版 Pro",
        "usage": "今日用量", "lang": "🌐 语言设置", "role": "🎭 角色选择", "tone": "🗣️ 语气风格",
        "logout": "🚪 退出登录", "mode": "⚙️ 模式选择", "action": "⚡ 执行操作", 
        "input_label": "📝 详细要求", "generate": "✨ 开始生成", "lock_msg": "🔒 该模式仅限 Pro", 
        "buy_btn": "👉 升级 Pro 版", "result": "✨ 生成结果", "live_stat": "实时状态",
        "tbl_headers": ["功能特性", "访客", "💎 PRO 永久版"], "tbl_data": TABLE_CN
    },
    # ✅ 繁体中文 UI
    "繁體中文": {
        "sidebar_title": "Lai's Lab", "plan_guest": "訪客計劃", "plan_pro": "企業版 Pro",
        "usage": "今日用量", "lang": "🌐 語言設定", "role": "🎭 角色選擇", "tone": "🗣️ 語氣風格",
        "logout": "🚪 登出", "mode": "⚙️ 模式選擇", "action": "⚡ 執行操作", 
        "input_label": "📝 詳細要求", "generate": "✨ 開始生成", "lock_msg": "🔒 該模式僅限 Pro", 
        "buy_btn": "👉 升級 Pro 版", "result": "✨ 生成結果", "live_stat": "實時狀態",
        "tbl_headers": ["功能特性", "訪客", "💎 PRO 永久版"], "tbl_data": TABLE_TC
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
    },
    # 补全其他 10 种语言 (UI 映射)
    "日本語": { "sidebar_title": "Lai's Lab", "plan_guest": "ゲスト", "plan_pro": "Pro 企業版", "usage": "使用量", "lang": "🌐 言語", "role": "🎭 役割", "tone": "🗣️ 口調", "logout": "🚪 ログアウト", "mode": "⚙️ モード", "action": "⚡ アクション", "input_label": "📝 コンテキスト", "generate": "✨ 生成", "lock_msg": "🔒 ロック (Proのみ)", "buy_btn": "👉 Proへアップグレード", "result": "✨ 結果", "live_stat": "ライブ", "tbl_headers": ["機能", "ゲスト", "💎 PRO 永久版"], "tbl_data": TABLE_EN },
    "한국어": { "sidebar_title": "Lai's Lab", "plan_guest": "게스트", "plan_pro": "Pro 엔터프라이즈", "usage": "사용량", "lang": "🌐 언어", "role": "🎭 역할", "tone": "🗣️ 톤", "logout": "🚪 로그아웃", "mode": "⚙️ 모드", "action": "⚡ 작업", "input_label": "📝 문맥", "generate": "✨ 생성", "lock_msg": "🔒 잠김 (Pro 전용)", "buy_btn": "👉 Pro 업그레이드", "result": "✨ 결과", "live_stat": "실시간", "tbl_headers": ["기능", "게스트", "💎 PRO 평생권"], "tbl_data": TABLE_EN },
    "Français": { "sidebar_title": "Lai's Lab", "plan_guest": "Invité", "plan_pro": "Pro Entreprise", "usage": "Usage", "lang": "🌐 Langue", "role": "🎭 Rôle", "tone": "🗣️ Ton", "logout": "🚪 Déconnexion", "mode": "⚙️ Mode", "action": "⚡ Action", "input_label": "📝 Contexte", "generate": "✨ Générer", "lock_msg": "🔒 Verrouillé (Pro)", "buy_btn": "👉 Obtenir Pro", "result": "✨ Résultat", "live_stat": "En Direct", "tbl_headers": ["Capacité", "Invité", "💎 PRO à Vie"], "tbl_data": TABLE_EN },
    "Deutsch": { "sidebar_title": "Lai's Lab", "plan_guest": "Gast", "plan_pro": "Pro Enterprise", "usage": "Nutzung", "lang": "🌐 Sprache", "role": "🎭 Rolle", "tone": "🗣️ Ton", "logout": "🚪 Logout", "mode": "⚙️ Modus", "action": "⚡ Aktion", "input_label": "📝 Kontext", "generate": "✨ Generieren", "lock_msg": "🔒 Gesperrt", "buy_btn": "👉 Upgrade", "result": "✨ Ergebnis", "live_stat": "Live", "tbl_headers": ["Funktion", "Gast", "💎 PRO Lifetime"], "tbl_data": TABLE_EN },
    "Italiano": { "sidebar_title": "Lai's Lab", "plan_guest": "Ospite", "plan_pro": "Pro Aziendale", "usage": "Uso", "lang": "🌐 Lingua", "role": "🎭 Ruolo", "tone": "🗣️ Tono", "logout": "🚪 Esci", "mode": "⚙️ Modalità", "action": "⚡ Azione", "input_label": "📝 Contesto", "generate": "✨ Genera", "lock_msg": "🔒 Bloccato", "buy_btn": "👉 Ottieni Pro", "result": "✨ Risultato", "live_stat": "Live", "tbl_headers": ["Capacità", "Ospite", "💎 PRO A Vita"], "tbl_data": TABLE_EN },
    "Português": { "sidebar_title": "Lai's Lab", "plan_guest": "Visitante", "plan_pro": "Pro Empresa", "usage": "Uso", "lang": "🌐 Idioma", "role": "🎭 Função", "tone": "🗣️ Tom", "logout": "🚪 Sair", "mode": "⚙️ Modo", "action": "⚡ Ação", "input_label": "📝 Contexto", "generate": "✨ Gerar", "lock_msg": "🔒 Bloqueado", "buy_btn": "👉 Obter Pro", "result": "✨ Resultado", "live_stat": "Ao Vivo", "tbl_headers": ["Capacidade", "Visitante", "💎 PRO Vitalício"], "tbl_data": TABLE_EN },
    "Русский": { "sidebar_title": "Lai's Lab", "plan_guest": "Гость", "plan_pro": "Pro Enterprise", "usage": "Лимит", "lang": "🌐 Язык", "role": "🎭 Роль", "tone": "🗣️ Тон", "logout": "🚪 Выход", "mode": "⚙️ Режим", "action": "⚡ Действие", "input_label": "📝 Контекст", "generate": "✨ Создать", "lock_msg": "🔒 Заблокировано", "buy_btn": "👉 Купить Pro", "result": "✨ Результат", "live_stat": "Статус", "tbl_headers": ["Функции", "Гость", "💎 PRO Навсегда"], "tbl_data": TABLE_EN },
    "Arabic": { "sidebar_title": "Lai's Lab", "plan_guest": "زائر", "plan_pro": "Pro شركات", "usage": "الاستخدام", "lang": "🌐 اللغة", "role": "🎭 الدور", "tone": "🗣️ النبرة", "logout": "🚪 خروج", "mode": "⚙️ الوضع", "action": "⚡ إجراء", "input_label": "📝 السياق", "generate": "✨ إنشاء", "lock_msg": "🔒 مقفل", "buy_btn": "👉 ترقية", "result": "✨ النتيجة", "live_stat": "مباشر", "tbl_headers": ["الميزات", "زائر", "💎 PRO مدى الحياة"], "tbl_data": TABLE_EN },
    "Hindi": { "sidebar_title": "Lai's Lab", "plan_guest": "अतिथि", "plan_pro": "Pro एंटरप्राइज़", "usage": "उपयोग", "lang": "🌐 भाषा", "role": "🎭 भूमिका", "tone": "🗣️ लहजा", "logout": "🚪 लॉग आउट", "mode": "⚙️ मोड", "action": "⚡ क्रिया", "input_label": "📝 संदर्भ", "generate": "✨ जनरेट करें", "lock_msg": "🔒 लॉक है", "buy_btn": "👉 अपग्रेड", "result": "✨ परिणाम", "live_stat": "लाइव", "tbl_headers": ["क्षमता", "अतिथि", "💎 PRO लाइफटाइम"], "tbl_data": TABLE_EN },
    "Thai": { "sidebar_title": "Lai's Lab", "plan_guest": "ผู้เยี่ยมชม", "plan_pro": "Pro องค์กร", "usage": "การใช้งาน", "lang": "🌐 ภาษา", "role": "🎭 บทบาท", "tone": "🗣️ น้ำเสียง", "logout": "🚪 ออกจากระบบ", "mode": "⚙️ โหมด", "action": "⚡ การกระทำ", "input_label": "📝 บริบท", "generate": "✨ สร้าง", "lock_msg": "🔒 ล็อก", "buy_btn": "👉 อัปเกรด", "result": "✨ ผลลัพธ์", "live_stat": "สด", "tbl_headers": ["ความสามารถ", "ผู้เยี่ยมชม", "💎 PRO ตลอดชีพ"], "tbl_data": TABLE_EN },
    "Vietnamese": { "sidebar_title": "Lai's Lab", "plan_guest": "Khách", "plan_pro": "Pro Doanh Nghiệp", "usage": "Sử dụng", "lang": "🌐 Ngôn ngữ", "role": "🎭 Vai trò", "tone": "🗣️ Giọng điệu", "logout": "🚪 Đăng xuất", "mode": "⚙️ Chế độ", "action": "⚡ Hành động", "input_label": "📝 Ngữ cảnh", "generate": "✨ Tạo", "lock_msg": "🔒 Bị khóa", "buy_btn": "👉 Nâng cấp", "result": "✨ Kết quả", "live_stat": "Trực tiếp", "tbl_headers": ["Tính năng", "Khách", "💎 PRO Trọn đời"], "tbl_data": TABLE_EN }
}
# 防止键值缺失
for lang in LANG_OPTIONS_PRO:
    if lang not in LANG_MAP: LANG_MAP[lang] = LANG_MAP["English"]

# ==========================================
# 4. 完整 60 个语调 (每个角色 10 个)
# ==========================================
ROLE_TONES = {
    "Global Educator": [
        "📚 Academic", "🌟 Encouraging", "🤝 Patient", "💡 Socratic", "📢 Instructional",
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
        "📊 Data-Driven", "🎯 Targeted", "🗣️ Conversational", "🔥 Aggressive", "✨ Solution-Focused"
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
DEFAULT_TONES = ["Professional", "Friendly", "Informative", "Assertive", "Empathetic"]

# ==========================================
# 5. 完整 126 个模式 (6角色 x 3子模式 x 7选项)
# ==========================================
ROLES_CONFIG = {
    "Global Educator": {
        "Pedagogy (Free)": [
            {"label": "1. Rubric Creator", "template": "Create a grading rubric for: {input}"},
            {"label": "2. Lesson Plan", "template": "Create a 1-hour lesson plan for: {input}"},
            {"label": "3. Quiz Generator", "template": "Create 5 multiple choice questions for: {input}"},
            {"label": "4. IEP Drafter", "template": "Draft an IEP goal for: {input}"},
            {"label": "5. Concept Explainer", "template": "Explain this concept to a 5-year old: {input}"},
            {"label": "6. Activity Designer", "template": "Classroom activity for: {input}"},
            {"label": "7. Learning Objectives", "template": "Write learning objectives for: {input}"}
        ],
        "Visuals (Pro)": [
            {"label": "1. Pixar 3D", "template": "Midjourney prompt, Pixar style: {input}"},
            {"label": "2. Blackboard Art", "template": "Chalkboard diagram prompt for: {input}"},
            {"label": "3. Infographic", "template": "Educational infographic prompt for: {input}"},
            {"label": "4. Flashcard Art", "template": "Visual flashcard design for: {input}"},
            {"label": "5. Classroom Poster", "template": "Motivational poster text for: {input}"},
            {"label": "6. Slide Design", "template": "PowerPoint slide layout description for: {input}"},
            {"label": "7. Textbook Illustration", "template": "Textbook illustration prompt for: {input}"}
        ],
        "Admin (Pro)": [
            {"label": "1. Email to Parents", "template": "Write an email to parents about: {input}"},
            {"label": "2. Report Comments", "template": "Report card comment for: {input}"},
            {"label": "3. Newsletter", "template": "Classroom newsletter section about: {input}"},
            {"label": "4. Behavior Log", "template": "Document a behavioral incident: {input}"},
            {"label": "5. Grant Proposal", "template": "Write a grant proposal for: {input}"},
            {"label": "6. Meeting Agenda", "template": "Staff meeting agenda item: {input}"},
            {"label": "7. Recommendation Letter", "template": "Letter of recommendation for: {input}"}
        ]
    },
    "Global Creator": {
        "Scripting (Free)": [
            {"label": "1. Viral Hook", "template": "Write 5 viral hooks for: {input}"},
            {"label": "2. TikTok Script", "template": "30-second TikTok script for: {input}"},
            {"label": "3. YouTube Intro", "template": "YouTube video intro for: {input}"},
            {"label": "4. Caption Writer", "template": "Instagram caption for: {input}"},
            {"label": "5. Hashtag Gen", "template": "30 relevant hashtags for: {input}"},
            {"label": "6. CTAs", "template": "Call to action for: {input}"},
            {"label": "7. Storyboard Text", "template": "Video storyboard description for: {input}"}
        ],
        "Visuals (Pro)": [
            {"label": "1. Thumbnail", "template": "YouTube thumbnail prompt: {input}"},
            {"label": "2. Profile Pic", "template": "Profile picture prompt: {input}"},
            {"label": "3. Banner Art", "template": "Channel banner prompt: {input}"},
            {"label": "4. Sticker Set", "template": "Emoji/Sticker pack prompt: {input}"},
            {"label": "5. Merch Design", "template": "T-shirt design prompt: {input}"},
            {"label": "6. NFT Art", "template": "NFT collection concept for: {input}"},
            {"label": "7. Logo Concept", "template": "Personal brand logo prompt: {input}"}
        ],
        "Marketing (Pro)": [
            {"label": "1. Sponsor Pitch", "template": "Pitch email to brand: {input}"},
            {"label": "2. Bio Optimizer", "template": "Optimize social bio for: {input}"},
            {"label": "3. Content Calendar", "template": "1-week content calendar for: {input}"},
            {"label": "4. Collab Request", "template": "Collaboration DM to influencer: {input}"},
            {"label": "5. Community Post", "template": "Community engagement post for: {input}"},
            {"label": "6. Newsletter Intro", "template": "Newsletter introduction for: {input}"},
            {"label": "7. Media Kit Bio", "template": "Bio for media kit: {input}"}
        ]
    },
    "Global Parent": {
        "Story (Free)": [
            {"label": "1. Bedtime Story", "template": "Bedtime story about: {input}"},
            {"label": "2. Moral Lesson", "template": "Story teaching the moral of: {input}"},
            {"label": "3. Personalized", "template": "Story featuring child name: {input}"},
            {"label": "4. Adventure", "template": "Choose-your-own-adventure segment: {input}"},
            {"label": "5. Poem", "template": "Rhyming poem about: {input}"},
            {"label": "6. Joke Gen", "template": "Kid-friendly jokes about: {input}"},
            {"label": "7. Song Lyrics", "template": "Lullaby lyrics about: {input}"}
        ],
        "Education (Pro)": [
            {"label": "1. Homework Help", "template": "Explain homework question: {input}"},
            {"label": "2. Science Exp", "template": "Home science experiment for: {input}"},
            {"label": "3. Math Drill", "template": "Math practice problems for: {input}"},
            {"label": "4. History Fact", "template": "Fun history fact about: {input}"},
            {"label": "5. Coding Concept", "template": "Explain coding loop to kid: {input}"},
            {"label": "6. Language Practice", "template": "Spanish vocabulary practice for: {input}"},
            {"label": "7. Reading Comp", "template": "Reading comprehension questions for: {input}"}
        ],
        "Fun (Pro)": [
            {"label": "1. Party Planner", "template": "Birthday party plan for: {input}"},
            {"label": "2. Lunchbox Note", "template": "Cute note for lunchbox: {input}"},
            {"label": "3. Weekend Trip", "template": "Family trip itinerary for: {input}"},
            {"label": "4. Game Idea", "template": "Indoor game idea for: {input}"},
            {"label": "5. Craft Project", "template": "DIY craft project using: {input}"},
            {"label": "6. Movie Night", "template": "Family movie recommendation like: {input}"},
            {"label": "7. Meal Plan", "template": "Kid-friendly meal plan for: {input}"}
        ]
    },
    "Global Seller": {
        "Copy (Free)": [
            {"label": "1. Ad Headline", "template": "Facebook ad headline for: {input}"},
            {"label": "2. Product Desc", "template": "Amazon product description for: {input}"},
            {"label": "3. Email Subject", "template": "High open-rate subject lines for: {input}"},
            {"label": "4. Value Prop", "template": "Value proposition statement: {input}"},
            {"label": "5. SEO Keywords", "template": "SEO keyword list for: {input}"},
            {"label": "6. Tagline", "template": "Catchy tagline for: {input}"},
            {"label": "7. FAQ Gen", "template": "FAQ section for: {input}"}
        ],
        "Strategy (Pro)": [
            {"label": "1. Upsell Script", "template": "Upsell script for: {input}"},
            {"label": "2. Objection Kill", "template": "Handle objection: {input}"},
            {"label": "3. Persona Gen", "template": "Customer persona for: {input}"},
            {"label": "4. Competitor Analysis", "template": "Analyze competitor: {input}"},
            {"label": "5. Pricing Strategy", "template": "Pricing strategy ideas for: {input}"},
            {"label": "6. Funnel Map", "template": "Sales funnel steps for: {input}"},
            {"label": "7. Offer Stack", "template": "Create an irresistible offer stack: {input}"}
        ],
        "Content (Pro)": [
            {"label": "1. LinkedIn Post", "template": "LinkedIn thought leadership about: {input}"},
            {"label": "2. Twitter Thread", "template": "Twitter thread about: {input}"},
            {"label": "3. Blog Outline", "template": "SEO blog outline for: {input}"},
            {"label": "4. Video Script", "template": "Product demo video script: {input}"},
            {"label": "5. Case Study", "template": "Case study structure for: {input}"},
            {"label": "6. Whitepaper", "template": "Whitepaper topic ideas: {input}"},
            {"label": "7. Webinar Title", "template": "Webinar title and bullets: {input}"}
        ]
    },
    "Global Student": {
        "Study (Free)": [
            {"label": "1. Summarizer", "template": "Summarize this text: {input}"},
            {"label": "2. Flashcards", "template": "Create flashcard content for: {input}"},
            {"label": "3. Essay Outline", "template": "Essay outline for topic: {input}"},
            {"label": "4. Thesis Statement", "template": "Strong thesis statement for: {input}"},
            {"label": "5. Study Schedule", "template": "Study schedule for exam: {input}"},
            {"label": "6. Mnemonics", "template": "Mnemonic device for: {input}"},
            {"label": "7. Quiz Myself", "template": "Generate self-test questions: {input}"}
        ],
        "Research (Pro)": [
            {"label": "1. Source Finder", "template": "Find academic sources for: {input}"},
            {"label": "2. Citation Fix", "template": "Format citation in APA: {input}"},
            {"label": "3. Abstract Gen", "template": "Write an abstract for: {input}"},
            {"label": "4. Lit Review", "template": "Literature review structure: {input}"},
            {"label": "5. Methodology", "template": "Research methodology steps: {input}"},
            {"label": "6. Data Analysis", "template": "Explain this data set: {input}"},
            {"label": "7. Lab Report", "template": "Lab report structure for: {input}"}
        ],
        "Career (Pro)": [
            {"label": "1. Resume Bullet", "template": "Improve resume bullet: {input}"},
            {"label": "2. Cover Letter", "template": "Cover letter for job: {input}"},
            {"label": "3. Interview Prep", "template": "Interview questions for: {input}"},
            {"label": "4. LinkedIn Bio", "template": "Professional LinkedIn bio: {input}"},
            {"label": "5. Cold Email", "template": "Cold networking email: {input}"},
            {"label": "6. Portfolio Desc", "template": "Project description for portfolio: {input}"},
            {"label": "7. Skill Gap", "template": "Identify skills needed for: {input}"}
        ]
    },
    "Global Corporate": {
        "Admin (Free)": [
            {"label": "1. Email Polish", "template": "Professionalize this email: {input}"},
            {"label": "2. Meeting Mins", "template": "Format meeting minutes: {input}"},
            {"label": "3. Memo Writer", "template": "Write a corporate memo about: {input}"},
            {"label": "4. Agenda Gen", "template": "Meeting agenda for: {input}"},
            {"label": "5. Slack Update", "template": "Professional Slack update: {input}"},
            {"label": "6. OOO Message", "template": "Out of office reply: {input}"},
            {"label": "7. Task List", "template": "Prioritized task list: {input}"}
        ],
        "Strategy (Pro)": [
            {"label": "1. SWOT Analysis", "template": "SWOT analysis for: {input}"},
            {"label": "2. OKR Draft", "template": "Draft OKRs for: {input}"},
            {"label": "3. Policy Draft", "template": "Draft company policy for: {input}"},
            {"label": "4. Project Plan", "template": "Project plan outline: {input}"},
            {"label": "5. Risk Assess", "template": "Risk assessment for: {input}"},
            {"label": "6. Budget Justification", "template": "Justify budget for: {input}"},
            {"label": "7. Executive Summary", "template": "Executive summary for: {input}"}
        ],
        "HR (Pro)": [
            {"label": "1. Job Post", "template": "Job posting for: {input}"},
            {"label": "2. Feedback", "template": "Constructive feedback script for: {input}"},
            {"label": "3. Announcement", "template": "Company announcement about: {input}"},
            {"label": "4. Onboarding", "template": "Onboarding checklist for: {input}"},
            {"label": "5. Interview Qs", "template": "Interview questions for role: {input}"},
            {"label": "6. Culture Value", "template": "Define company value: {input}"},
            {"label": "7. Retention Plan", "template": "Employee retention ideas: {input}"}
        ]
    }
}

# ==========================================
# 6. 智能拦截字典 (FAQ Logic)
# ==========================================
INTERCEPTORS = {
    "price": "$12.90 Lifetime",
    "refund": "No refunds on digital keys",
    "free": "Guest plan is free (5/day)",
    "support": "VIP support in 1-2 days"
}
