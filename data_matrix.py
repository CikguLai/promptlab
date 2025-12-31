# data_matrix.py
# Lai's Lab V9.28 - GLOBAL EDITION (Fixed)
# Free & Pro both get FULL 16 Languages

# ==========================================
# 1. 语言选项 (16 种全开 - 免费付费同权)
# ==========================================
# 核心修正：访客现在也能看到所有 16 种语言
ALL_LANGUAGES = [
    "English", "简体中文", "繁體中文", "Bahasa Melayu", "Español", 
    "日本語", "한국어", "Français", "Deutsch", 
    "Italiano", "Português", "Русский", "Arabic", 
    "Hindi", "Thai", "Vietnamese"
]

LANG_OPTIONS_GUEST = ALL_LANGUAGES
LANG_OPTIONS_PRO = ALL_LANGUAGES

# ==========================================
# 2. 对比表数据 (更新：语言不再是限制点)
# ==========================================
TABLE_EN = [
    {"k": "Daily Limit", "v1": "5 / Day", "v2": "*Unlimited"},
    {"k": "Content Format", "v1": "With AI Symbols", "v2": "100% Clean & Human"},
    {"k": "Sharing", "v1": "Text + WhatsApp", "v2": "PDF + Clean Share"},
    {"k": "Languages", "v1": "16+ Global (Full)", "v2": "16+ Global (Full)"}, # 修正：两边都是 Full
    {"k": "Expert Modes", "v1": "Basic (6)", "v2": "All 18 + Custom"},
    {"k": "Watermark", "v1": "Forced", "v2": "Removed"},
    {"k": "Support", "v1": "Standard (3-5 Days)", "v2": "VIP Priority (1-2 Days)"},
    {"k": "Price", "v1": "Free", "v2": "Limited $12.90"}
]

# ==========================================
# 3. 16 国语言 UI 完整翻译矩阵 (保持不变，已含全部翻译)
# ==========================================
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
        "tbl_headers": ["功能特性", "访客", "💎 PRO 永久版"], "tbl_data": TABLE_EN
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
    },
    "日本語": {
        "sidebar_title": "Lai's Lab", "plan_guest": "ゲストプラン", "plan_pro": "Pro エンタープライズ",
        "usage": "使用量", "lang": "🌐 言語", "role": "🎭 役割", "tone": "🗣️ 口調",
        "logout": "🚪 ログアウト", "mode": "⚙️ モード選択", "action": "⚡ アクション", 
        "input_label": "📝 コンテキスト", "generate": "✨ 生成する", "lock_msg": "🔒 ロック中 (Proのみ)", 
        "buy_btn": "👉 Proへアップグレード", "result": "✨ 結果", "live_stat": "ライブステータス",
        "tbl_headers": ["機能", "ゲスト", "💎 PRO 永久版"], "tbl_data": TABLE_EN
    },
    "한국어": {
        "sidebar_title": "Lai's Lab", "plan_guest": "게스트 플랜", "plan_pro": "Pro 엔터프라이즈",
        "usage": "사용량", "lang": "🌐 언어", "role": "🎭 역할", "tone": "🗣️ 어조",
        "logout": "🚪 로그아웃", "mode": "⚙️ 모드 선택", "action": "⚡ 동작 선택", 
        "input_label": "📝 입력 내용", "generate": "✨ 생성하기", "lock_msg": "🔒 잠김 (Pro 전용)", 
        "buy_btn": "👉 Pro로 업그레이드", "result": "✨ 결과", "live_stat": "실시간 상태",
        "tbl_headers": ["기능", "게스트", "💎 PRO 평생판"], "tbl_data": TABLE_EN
    },
    "Français": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Plan Invité", "plan_pro": "Pro Entreprise",
        "usage": "Utilisation", "lang": "🌐 Langue", "role": "🎭 Rôle", "tone": "🗣️ Ton",
        "logout": "🚪 Déconnexion", "mode": "⚙️ Mode", "action": "⚡ Action", 
        "input_label": "📝 Contexte", "generate": "✨ Générer", "lock_msg": "🔒 Verrouillé (Pro)", 
        "buy_btn": "👉 Passer à Pro", "result": "✨ Résultat", "live_stat": "Statut en direct",
        "tbl_headers": ["Fonctionnalité", "Invité", "💎 PRO à vie"], "tbl_data": TABLE_EN
    },
    "Deutsch": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Gast-Plan", "plan_pro": "Pro Enterprise",
        "usage": "Nutzung", "lang": "🌐 Sprache", "role": "🎭 Rolle", "tone": "🗣️ Tonfall",
        "logout": "🚪 Abmelden", "mode": "⚙️ Modus", "action": "⚡ Aktion", 
        "input_label": "📝 Kontext", "generate": "✨ Generieren", "lock_msg": "🔒 Gesperrt (Nur Pro)", 
        "buy_btn": "👉 Upgrade auf Pro", "result": "✨ Ergebnis", "live_stat": "Live-Status",
        "tbl_headers": ["Funktion", "Gast", "💎 PRO Lebenslang"], "tbl_data": TABLE_EN
    },
    "Italiano": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Piano Ospite", "plan_pro": "Pro Enterprise",
        "usage": "Utilizzo", "lang": "🌐 Lingua", "role": "🎭 Ruolo", "tone": "🗣️ Tono",
        "logout": "🚪 Esci", "mode": "⚙️ Modalità", "action": "⚡ Azione", 
        "input_label": "📝 Contesto", "generate": "✨ Genera", "lock_msg": "🔒 Bloccato (Solo Pro)", 
        "buy_btn": "👉 Passa a Pro", "result": "✨ Risultato", "live_stat": "Stato Live",
        "tbl_headers": ["Funzionalità", "Ospite", "💎 PRO a Vita"], "tbl_data": TABLE_EN
    },
    "Português": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Plano Visitante", "plan_pro": "Pro Empresarial",
        "usage": "Uso", "lang": "🌐 Idioma", "role": "🎭 Papel", "tone": "🗣️ Tom",
        "logout": "🚪 Sair", "mode": "⚙️ Modo", "action": "⚡ Ação", 
        "input_label": "📝 Contexto", "generate": "✨ Gerar", "lock_msg": "🔒 Bloqueado (Só Pro)", 
        "buy_btn": "👉 Mudar para Pro", "result": "✨ Resultado", "live_stat": "Status ao Vivo",
        "tbl_headers": ["Recurso", "Visitante", "💎 PRO Vitalício"], "tbl_data": TABLE_EN
    },
    "Русский": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Гостевой план", "plan_pro": "Pro Enterprise",
        "usage": "Исп.", "lang": "🌐 Язык", "role": "🎭 Роль", "tone": "🗣️ Тон",
        "logout": "🚪 Выйти", "mode": "⚙️ Режим", "action": "⚡ Действие", 
        "input_label": "📝 Контекст", "generate": "✨ Создать", "lock_msg": "🔒 Закрыто (Pro)", 
        "buy_btn": "👉 Купить Pro", "result": "✨ Результат", "live_stat": "Статус",
        "tbl_headers": ["Функция", "Гость", "💎 PRO Навсегда"], "tbl_data": TABLE_EN
    },
    "Arabic": {
        "sidebar_title": "Lai's Lab", "plan_guest": "خطة الضيف", "plan_pro": "Pro مؤسسة",
        "usage": "الاستخدام", "lang": "🌐 اللغة", "role": "🎭 الدور", "tone": "🗣️ نبرة الصوت",
        "logout": "🚪 خروج", "mode": "⚙️ الوضع", "action": "⚡ الإجراء", 
        "input_label": "📝 السياق", "generate": "✨ توليد", "lock_msg": "🔒 مغلق (Pro فقط)", 
        "buy_btn": "👉 ترقية لـ Pro", "result": "✨ النتيجة", "live_stat": "حالة مباشرة",
        "tbl_headers": ["الميزة", "ضيف", "💎 Pro مدى الحياة"], "tbl_data": TABLE_EN
    },
    "Hindi": {
        "sidebar_title": "Lai's Lab", "plan_guest": "गेस्ट प्लान", "plan_pro": "Pro एंटरप्राइज",
        "usage": "उपयोग", "lang": "🌐 भाषा", "role": "🎭 भूमिका", "tone": "🗣️ टोन",
        "logout": "🚪 लॉग आउट", "mode": "⚙️ मोड", "action": "⚡ कार्रवाई", 
        "input_label": "📝 संदर्भ", "generate": "✨ उत्पन्न करें", "lock_msg": "🔒 लॉक (केवल Pro)", 
        "buy_btn": "👉 Pro में अपग्रेड करें", "result": "✨ परिणाम", "live_stat": "लाइव स्थिति",
        "tbl_headers": ["क्षमता", "गेस्ट", "💎 PRO लाइफटाइम"], "tbl_data": TABLE_EN
    },
    "Thai": {
        "sidebar_title": "Lai's Lab", "plan_guest": "แผนผู้ใช้ทั่วไป", "plan_pro": "Pro องค์กร",
        "usage": "การใช้งาน", "lang": "🌐 ภาษา", "role": "🎭 บทบาท", "tone": "🗣️ น้ำเสียง",
        "logout": "🚪 ออกจากระบบ", "mode": "⚙️ โหมด", "action": "⚡ การกระทำ", 
        "input_label": "📝 บริบท", "generate": "✨ สร้าง", "lock_msg": "🔒 ล็อค (เฉพาะ Pro)", 
        "buy_btn": "👉 อัปเกรดเป็น Pro", "result": "✨ ผลลัพธ์", "live_stat": "สถานะสด",
        "tbl_headers": ["คุณสมบัติ", "ทั่วไป", "💎 PRO ตลอดชีพ"], "tbl_data": TABLE_EN
    },
    "Vietnamese": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Gói Khách", "plan_pro": "Pro Doanh nghiệp",
        "usage": "Sử dụng", "lang": "🌐 Ngôn ngữ", "role": "🎭 Vai trò", "tone": "🗣️ Giọng điệu",
        "logout": "🚪 Đăng xuất", "mode": "⚙️ Chế độ", "action": "⚡ Hành động", 
        "input_label": "📝 Ngữ cảnh", "generate": "✨ Tạo", "lock_msg": "🔒 Đã khóa (Chỉ Pro)", 
        "buy_btn": "👉 Nâng cấp Pro", "result": "✨ Kết quả", "live_stat": "Trạng thái",
        "tbl_headers": ["Tính năng", "Khách", "💎 PRO Trọn đời"], "tbl_data": TABLE_EN
    }
}

# ==========================================
# 4. 语调 (60 Tones - English)
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
# 5. 核心模式 (18 Modes, 162 Options - English)
# ==========================================
ROLES_CONFIG = {
    "Global Educator": {
        "Pedagogy (Free)": [
            {"label": "1. Rubric Creator", "template": "Create a grading rubric for: {input}. Columns: Criteria, Excellent, Good, Fair, Poor."},
            {"label": "2. Direct Instruction", "template": "Create a lesson plan using Direct Instruction model for: {input}"},
            {"label": "3. Gamification", "template": "Design a classroom game to teach: {input}"},
            {"label": "4. Project-Based Learning", "template": "Design a PBL project outline for: {input}"},
            {"label": "5. Socratic Method", "template": "Generate Socratic questions to guide students on: {input}"},
            {"label": "6. Flipped Classroom", "template": "Create a flipped classroom plan for: {input}"}
        ],
        "Visuals (Pro)": [
            {"label": "1. Pixar 3D Prompt", "template": "Midjourney prompt, Pixar style: {input}"},
            {"label": "2. National Geographic", "template": "Midjourney prompt, National Geographic photography: {input}"},
            {"label": "3. Minimalist Vector", "template": "Midjourney prompt, flat vector icon: {input}"},
            {"label": "4. Vintage Watercolor", "template": "Midjourney prompt, vintage watercolor style: {input}"},
            {"label": "5. Scientific Schematic", "template": "Midjourney prompt, scientific diagram: {input}"},
            {"label": "6. Cyberpunk Concept", "template": "Midjourney prompt, cyberpunk futuristic: {input}"}
        ],
        "Comm (Pro)": [
            {"label": "1. Parent Message", "template": "Write a message to parents regarding: {input}"},
            {"label": "2. Behavior Report", "template": "Write a behavior report about: {input}"},
            {"label": "3. Official Proposal", "template": "Write a formal school proposal for: {input}"},
            {"label": "4. Newsletter", "template": "Write a classroom newsletter section about: {input}"},
            {"label": "5. Event Invitation", "template": "Write an invitation for: {input}"},
            {"label": "6. Grant Application", "template": "Write a grant application for: {input}"}
        ]
    },
    "Global Creator": {
        "Scripting (Free)": [
            {"label": "1. Viral Hook Generator", "template": "Generate 10 viral hooks (3-seconds) for a video about: {input}"},
            {"label": "2. TikTok Script", "template": "Write a 30s TikTok script with Hook, Value, CTA for: {input}"},
            {"label": "3. YouTube Edutainment", "template": "Write a YouTube script structure for: {input}"},
            {"label": "4. Storytelling Vlog", "template": "Write a vlog narration script for: {input}"},
            {"label": "5. Podcast Interview", "template": "Generate interview questions for a guest expert on: {input}"},
            {"label": "6. Live Stream Flow", "template": "Create a run-down for a live stream selling: {input}"}
        ],
        "Thumbnail (Pro)": [
            {"label": "1. High CTR Shocked", "template": "YouTube thumbnail prompt, shocked face, high contrast: {input}"},
            {"label": "2. Cinematic Poster", "template": "Midjourney prompt, movie poster style: {input}"},
            {"label": "3. Tech/Neon", "template": "Midjourney prompt, glowing tech style: {input}"},
            {"label": "4. Before & After", "template": "Midjourney prompt, split screen comparison: {input}"},
            {"label": "5. Minimalist Apple", "template": "Midjourney prompt, clean white minimalist: {input}"},
            {"label": "6. Comic Book", "template": "Midjourney prompt, Marvel comic style: {input}"}
        ],
        "Marketing (Pro)": [
            {"label": "1. Xiaohongshu (KOC)", "template": "Write a Xiaohongshu post with emojis and tags for: {input}"},
            {"label": "2. Instagram Caption", "template": "Write an engaging IG caption for: {input}"},
            {"label": "3. Facebook Ad", "template": "Write a Facebook ad copy (PAS framework) for: {input}"},
            {"label": "4. LinkedIn Leader", "template": "Write a LinkedIn thought leadership post about: {input}"},
            {"label": "5. Twitter Thread", "template": "Write a viral Twitter thread (5 tweets) about: {input}"},
            {"label": "6. Email Newsletter", "template": "Write an email newsletter subject and body for: {input}"}
        ]
    },
    "Global Parent": {
        "Story Time (Free)": [
            {"label": "1. 'My Day' Magic", "template": "Transform this daily event into a magical fairytale: {input}"},
            {"label": "2. Bedtime Story", "template": "Write a calming bedtime story for: {input}"},
            {"label": "3. Hero's Journey", "template": "Write a hero's journey story to help a child overcome: {input}"},
            {"label": "4. Social Emotional", "template": "Write a story teaching the social skill of: {input}"},
            {"label": "5. Science 'Why'", "template": "Explain this science concept through a story: {input}"},
            {"label": "6. Cultural Tale", "template": "Tell a traditional cultural story about: {input}"}
        ],
        "Activities (Pro)": [
            {"label": "1. DIY Craft Guide", "template": "Step-by-step guide for a craft using: {input}"},
            {"label": "2. Rainy Day Game", "template": "Indoor game idea for: {input}"},
            {"label": "3. Kitchen Science", "template": "Safe kitchen science experiment using: {input}"},
            {"label": "4. Scavenger Hunt", "template": "Create a scavenger hunt list for location: {input}"},
            {"label": "5. Family Bonding", "template": "Family bonding activity idea for: {input}"},
            {"label": "6. No-Screen Coding", "template": "Teach coding logic without screens using: {input}"}
        ],
        "Tutor (Pro)": [
            {"label": "1. Mnemonic Generator", "template": "Create a catchy mnemonic rhyme to remember: {input}"},
            {"label": "2. Feynman Technique", "template": "Explain this concept simply (Feynman technique): {input}"},
            {"label": "3. Homework Helper", "template": "Guide the student to solve this (don't give answer): {input}"},
            {"label": "4. Quiz Generator", "template": "Create 5 practice questions for: {input}"},
            {"label": "5. Vocabulary Builder", "template": "Explain word, synonyms, and example sentences for: {input}"},
            {"label": "6. Essay Proofreader", "template": "Proofread and suggest improvements for: {input}"}
        ]
    },
    "Global Seller": {
        "Copywriting (Free)": [
            {"label": "1. Landing Page Structure", "template": "Outline a high-converting landing page structure for: {input}"},
            {"label": "2. PAS Model", "template": "Write copy using Problem-Agitation-Solution for: {input}"},
            {"label": "3. AIDA Model", "template": "Write copy using Attention-Interest-Desire-Action for: {input}"},
            {"label": "4. FAB Model", "template": "Write copy using Features-Advantages-Benefits for: {input}"},
            {"label": "5. Storytelling Sales", "template": "Write a brand story for: {input}"},
            {"label": "6. Objection Handling", "template": "Write a response to handle this customer objection: {input}"}
        ],
        "Product Shot (Pro)": [
            {"label": "1. Studio White BG", "template": "Midjourney prompt, e-commerce white background: {input}"},
            {"label": "2. Lifestyle Home", "template": "Midjourney prompt, cozy home lifestyle setting: {input}"},
            {"label": "3. Luxury Gold/Black", "template": "Midjourney prompt, luxury black and gold: {input}"},
            {"label": "4. Nature/Sunlight", "template": "Midjourney prompt, natural sunlight and nature: {input}"},
            {"label": "5. Cyberpunk/Tech", "template": "Midjourney prompt, futuristic tech style: {input}"},
            {"label": "6. Flat Lay", "template": "Midjourney prompt, organized flat lay photography: {input}"}
        ],
        "Support (Pro)": [
            {"label": "1. Apology & Recovery", "template": "Write a professional apology and recovery email for: {input}"},
            {"label": "2. Review Request", "template": "Write an email asking for a 5-star review after: {input}"},
            {"label": "3. Complaint Reply", "template": "Write a diplomatic reply to this angry complaint: {input}"},
            {"label": "4. Promo Announcement", "template": "Write an announcement for this sale event: {input}"},
            {"label": "5. Crisis Statement", "template": "Write a public crisis management statement regarding: {input}"},
            {"label": "6. FAQ Gen", "template": "Generate 5 FAQs and answers for: {input}"}
        ]
    },
    "Global Student": {
        "Study (Free)": [
            {"label": "1. Note Summarizer", "template": "Summarize these messy notes into structured key points: {input}"},
            {"label": "2. Feynman Technique", "template": "Explain this concept like I'm 5 years old: {input}"},
            {"label": "3. Lit Review Matrix", "template": "Create a literature review matrix structure for: {input}"},
            {"label": "4. Flashcard (Anki)", "template": "Create Anki flashcard content (Front/Back) for: {input}"},
            {"label": "5. Concept Simplifier", "template": "Simplify this complex text into plain language: {input}"},
            {"label": "6. Translation", "template": "Translate this text to academic English: {input}"}
        ],
        "Project (Pro)": [
            {"label": "1. Essay Outline", "template": "Create a structured essay outline for: {input}"},
            {"label": "2. Presentation Script", "template": "Write a presentation script (speech) for: {input}"},
            {"label": "3. Debate Prep", "template": "Generate arguments (Pro/Con) for: {input}"},
            {"label": "4. Lab Report", "template": "Outline a lab report structure for experiment: {input}"},
            {"label": "5. Methodology", "template": "Design a research methodology for: {input}"},
            {"label": "6. Group Roles", "template": "Assign group roles and tasks for project: {input}"}
        ],
        "Career (Pro)": [
            {"label": "1. ATS Resume", "template": "Optimize these resume bullet points for ATS: {input}"},
            {"label": "2. Cover Letter", "template": "Write a cover letter for this job role: {input}"},
            {"label": "3. Interview Prep", "template": "Generate common interview questions and answers for: {input}"},
            {"label": "4. LinkedIn Bio", "template": "Write a professional LinkedIn headline and about section for: {input}"},
            {"label": "5. Cold Email", "template": "Write a cold networking email to: {input}"},
            {"label": "6. Portfolio Desc", "template": "Write a project description for my portfolio: {input}"}
        ]
    },
    "Global Corporate": {
        "Admin (Free)": [
            {"label": "1. Email Polisher", "template": "Rewrite this draft to be professional and polite: {input}"},
            {"label": "2. Meeting Minutes", "template": "Format these notes into formal meeting minutes: {input}"},
            {"label": "3. Official Proposal", "template": "Draft a formal business proposal for: {input}"},
            {"label": "4. Internal Memo", "template": "Write an internal memo to staff about: {input}"},
            {"label": "5. SOP / Process", "template": "Draft a Standard Operating Procedure (SOP) for: {input}"},
            {"label": "6. Press Release", "template": "Write a press release announcing: {input}"}
        ],
        "Strategy (Pro)": [
            {"label": "1. OKRs", "template": "Draft Objectives and Key Results (OKRs) for: {input}"},
            {"label": "2. SWOT Analysis", "template": "Perform a SWOT analysis for: {input}"},
            {"label": "3. Competitor Dive", "template": "Analyze the competitor strategy for: {input}"},
            {"label": "4. Business Canvas", "template": "Create a Business Model Canvas for: {input}"},
            {"label": "5. Risk Matrix", "template": "Create a risk assessment matrix for: {input}"},
            {"label": "6. Pitch Deck", "template": "Outline a pitch deck structure for: {input}"}
        ],
        "HR & Team (Pro)": [
            {"label": "1. Performance Review", "template": "Write a performance review script (sandwich method) for: {input}"},
            {"label": "2. Job Desc (JD)", "template": "Write a professional Job Description for: {input}"},
            {"label": "3. Onboarding Plan", "template": "Create a 30-60-90 day onboarding plan for: {input}"},
            {"label": "4. Crisis Comms", "template": "Write an internal crisis communication email about: {input}"},
            {"label": "5. Team Building", "template": "Suggest team building activities for: {input}"},
            {"label": "6. Termination", "template": "Write a respectful termination meeting script for reason: {input}"}
        ]
    }
}

# 自动注入 "7. Custom / DIY"
CUSTOM_OPTION = {"label": "7. Custom / DIY", "template": "{input}"}
for role, modes in ROLES_CONFIG.items():
    for mode_name, options in modes.items():
        if not any(o['label'].startswith("7.") for o in options):
            options.append(CUSTOM_OPTION)

# ==========================================
# 6. 智能拦截 (FAQ)
# ==========================================
INTERCEPTORS = {
    "price": "$12.90 Lifetime Access (One-time payment)",
    "refund": "Digital keys are non-refundable once activated.",
    "free": "Guest Plan: 5 generations per day with watermark.",
    "support": "VIP Support: 1-2 days response time.",
    "invoice": "Invoices are automatically sent by LemonSqueezy.",
    "key": "Lost Key? Go to app.lemonsqueezy.com/my-orders",
    "limit": "Pro users get unlimited generations.",
    "pdf": "PDF export supports 16 languages.",
    "language": "Switch languages in the sidebar."
}
