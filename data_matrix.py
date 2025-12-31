# data_matrix.py
# Lai's Lab V9.28 - GLOBAL EDITION (Fixed)
# Free & Pro both get FULL 16 Languages | 16 FAQs | 5 Ticket Types | Multi-language Tables

# ==========================================
# 1. 语言选项 (16 种全开 - 免费付费同权)
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
# 2. 对比表数据生成器 (16国语言翻译)
# ==========================================
# 为了保持代码整洁，我们创建一个函数来生成表格数据
def get_table_data(lang):
    # 默认英文
    headers = ["Capability", "Guest", "💎 PRO Lifetime"]
    rows = [
        {"k": "Daily Limit", "v1": "5 / Day", "v2": "*Unlimited"},
        {"k": "Content Format", "v1": "With AI Symbols", "v2": "100% Clean & Human"},
        {"k": "Sharing", "v1": "Text + Watermark", "v2": "PDF + Clean Share"},
        {"k": "Languages", "v1": "16+ Global", "v2": "16+ Global"},
        {"k": "Expert Modes", "v1": "Basic (6)", "v2": "All 18 + Custom"},
        {"k": "Watermark", "v1": "Forced", "v2": "Removed"},
        {"k": "Support", "v1": "Standard", "v2": "VIP Priority"},
        {"k": "Price", "v1": "Free", "v2": "Limited $12.90"}
    ]

    if lang == "简体中文":
        headers = ["功能特性", "访客试用", "💎 PRO 永久版"]
        rows = [
            {"k": "每日限额", "v1": "5次 / 天", "v2": "*无限生成"},
            {"k": "内容纯净度", "v1": "含AI符号", "v2": "100% 纯净拟人"},
            {"k": "分享导出", "v1": "文本 + 水印", "v2": "PDF + 纯净分享"},
            {"k": "语言支持", "v1": "16+ 全球语言", "v2": "16+ 全球语言"},
            {"k": "专业模式", "v1": "基础 (6个)", "v2": "全套 18个 + 自定义"},
            {"k": "水印", "v1": "强制显示", "v2": "完全移除"},
            {"k": "客服响应", "v1": "标准速度", "v2": "VIP 优先通道"},
            {"k": "价格", "v1": "免费", "v2": "限时 $12.90"}
        ]
    elif lang == "繁體中文":
        headers = ["功能特性", "訪客試用", "💎 PRO 永久版"]
        rows = [
            {"k": "每日限額", "v1": "5次 / 天", "v2": "*無限生成"},
            {"k": "內容純淨度", "v1": "含AI符號", "v2": "100% 純淨擬人"},
            {"k": "分享導出", "v1": "文本 + 水印", "v2": "PDF + 純淨分享"},
            {"k": "語言支援", "v1": "16+ 全球語言", "v2": "16+ 全球語言"},
            {"k": "專業模式", "v1": "基礎 (6個)", "v2": "全套 18個 + 自定義"},
            {"k": "水印", "v1": "強制顯示", "v2": "完全移除"},
            {"k": "客服響應", "v1": "標準速度", "v2": "VIP 優先通道"},
            {"k": "價格", "v1": "免費", "v2": "限時 $12.90"}
        ]
    elif lang == "Bahasa Melayu":
        headers = ["Ciri", "Tetamu", "💎 PRO Seumur Hidup"]
        rows = [
            {"k": "Had Harian", "v1": "5 / Hari", "v2": "*Tanpa Had"},
            {"k": "Format", "v1": "Simbol AI", "v2": "100% Bersih & Manusia"},
            {"k": "Perkongsian", "v1": "Teks + Tera Air", "v2": "PDF + Bersih"},
            {"k": "Bahasa", "v1": "16+ Global", "v2": "16+ Global"},
            {"k": "Mod Pakar", "v1": "Asas (6)", "v2": "Semua 18 + Custom"},
            {"k": "Tera Air", "v1": "Ada", "v2": "Tiada"},
            {"k": "Sokongan", "v1": "Biasa", "v2": "VIP Prioriti"},
            {"k": "Harga", "v1": "Percuma", "v2": "Terhad $12.90"}
        ]
    elif lang == "Español":
        headers = ["Capacidad", "Invitado", "💎 PRO Vitalicio"]
        rows = [
            {"k": "Límite Diario", "v1": "5 / Día", "v2": "*Ilimitado"},
            {"k": "Formato", "v1": "Símbolos IA", "v2": "100% Limpio"},
            {"k": "Compartir", "v1": "Texto + Marca", "v2": "PDF + Limpio"},
            {"k": "Idiomas", "v1": "16+ Global", "v2": "16+ Global"},
            {"k": "Modos Expertos", "v1": "Básico (6)", "v2": "Todos 18 + Custom"},
            {"k": "Marca de Agua", "v1": "Forzada", "v2": "Removida"},
            {"k": "Soporte", "v1": "Estándar", "v2": "VIP Prioridad"},
            {"k": "Precio", "v1": "Gratis", "v2": "Oferta $12.90"}
        ]
    elif lang == "日本語":
        headers = ["機能", "ゲスト", "💎 PRO 永久版"]
        rows = [
            {"k": "1日の制限", "v1": "5回 / 日", "v2": "*無制限"},
            {"k": "フォーマット", "v1": "AI記号あり", "v2": "100% クリーン"},
            {"k": "共有", "v1": "テキスト+透かし", "v2": "PDF + クリーン"},
            {"k": "言語", "v1": "16+ グローバル", "v2": "16+ グローバル"},
            {"k": "エキスパート", "v1": "基本 (6)", "v2": "全18モード + Custom"},
            {"k": "透かし", "v1": "あり", "v2": "なし"},
            {"k": "サポート", "v1": "標準", "v2": "VIP 優先"},
            {"k": "価格", "v1": "無料", "v2": "特価 $12.90"}
        ]
    elif lang == "한국어":
        headers = ["기능", "게스트", "💎 PRO 평생판"]
        rows = [
            {"k": "일일 한도", "v1": "5회 / 일", "v2": "*무제한"},
            {"k": "형식", "v1": "AI 기호 포함", "v2": "100% 깔끔함"},
            {"k": "공유", "v1": "텍스트 + 워터마크", "v2": "PDF + 깔끔함"},
            {"k": "언어", "v1": "16+ 글로벌", "v2": "16+ 글로벌"},
            {"k": "전문가 모드", "v1": "기본 (6)", "v2": "전체 18 + 커스텀"},
            {"k": "워터마크", "v1": "표시됨", "v2": "제거됨"},
            {"k": "지원", "v1": "표준", "v2": "VIP 우선"},
            {"k": "가격", "v1": "무료", "v2": "특가 $12.90"}
        ]
    elif lang == "Français":
        headers = ["Fonctionnalité", "Invité", "💎 PRO à vie"]
        rows = [
            {"k": "Limite", "v1": "5 / Jour", "v2": "*Illimité"},
            {"k": "Format", "v1": "Symboles IA", "v2": "100% Propre"},
            {"k": "Partage", "v1": "Texte + Logo", "v2": "PDF + Propre"},
            {"k": "Langues", "v1": "16+ Global", "v2": "16+ Global"},
            {"k": "Modes", "v1": "Base (6)", "v2": "Tous 18 + Custom"},
            {"k": "Filigrane", "v1": "Oui", "v2": "Retiré"},
            {"k": "Support", "v1": "Standard", "v2": "VIP Priorité"},
            {"k": "Prix", "v1": "Gratuit", "v2": "Offre $12.90"}
        ]
    elif lang == "Deutsch":
        headers = ["Funktion", "Gast", "💎 PRO Lebenslang"]
        rows = [
            {"k": "Tageslimit", "v1": "5 / Tag", "v2": "*Unbegrenzt"},
            {"k": "Format", "v1": "KI-Symbole", "v2": "100% Sauber"},
            {"k": "Teilen", "v1": "Text + Logo", "v2": "PDF + Sauber"},
            {"k": "Sprachen", "v1": "16+ Global", "v2": "16+ Global"},
            {"k": "Modi", "v1": "Basis (6)", "v2": "Alle 18 + Custom"},
            {"k": "Wasserzeichen", "v1": "Ja", "v2": "Entfernt"},
            {"k": "Support", "v1": "Standard", "v2": "VIP Priorität"},
            {"k": "Preis", "v1": "Kostenlos", "v2": "Angebot $12.90"}
        ]
    elif lang == "Italiano":
        headers = ["Funzionalità", "Ospite", "💎 PRO a Vita"]
        rows = [
            {"k": "Limite", "v1": "5 / Giorno", "v2": "*Illimitato"},
            {"k": "Formato", "v1": "Simboli IA", "v2": "100% Pulito"},
            {"k": "Condivisione", "v1": "Testo + Logo", "v2": "PDF + Pulito"},
            {"k": "Lingue", "v1": "16+ Global", "v2": "16+ Global"},
            {"k": "Modalità", "v1": "Base (6)", "v2": "Tutte 18 + Custom"},
            {"k": "Filigrana", "v1": "Sì", "v2": "Rimossa"},
            {"k": "Supporto", "v1": "Standard", "v2": "VIP Priorità"},
            {"k": "Prezzo", "v1": "Gratis", "v2": "Offerta $12.90"}
        ]
    elif lang == "Português":
        headers = ["Recurso", "Visitante", "💎 PRO Vitalício"]
        rows = [
            {"k": "Limite", "v1": "5 / Dia", "v2": "*Ilimitado"},
            {"k": "Formato", "v1": "Símbolos IA", "v2": "100% Limpo"},
            {"k": "Partilha", "v1": "Texto + Logo", "v2": "PDF + Limpo"},
            {"k": "Idiomas", "v1": "16+ Global", "v2": "16+ Global"},
            {"k": "Modos", "v1": "Básico (6)", "v2": "Todos 18 + Custom"},
            {"k": "Marca d'água", "v1": "Sim", "v2": "Removida"},
            {"k": "Suporte", "v1": "Padrão", "v2": "VIP Prioridade"},
            {"k": "Preço", "v1": "Grátis", "v2": "Oferta $12.90"}
        ]
    elif lang == "Русский":
        headers = ["Функция", "Гость", "💎 PRO Навсегда"]
        rows = [
            {"k": "Лимит", "v1": "5 / День", "v2": "*Безлимит"},
            {"k": "Формат", "v1": "AI Символы", "v2": "100% Чистый"},
            {"k": "Поделиться", "v1": "Текст + Знак", "v2": "PDF + Чистый"},
            {"k": "Языки", "v1": "16+ Global", "v2": "16+ Global"},
            {"k": "Режимы", "v1": "База (6)", "v2": "Все 18 + Custom"},
            {"k": "Водяной знак", "v1": "Есть", "v2": "Удален"},
            {"k": "Поддержка", "v1": "Обычная", "v2": "VIP Приоритет"},
            {"k": "Цена", "v1": "Бесплатно", "v2": "$12.90"}
        ]
    elif lang == "Arabic":
        headers = ["الميزة", "ضيف", "💎 Pro مدى الحياة"]
        rows = [
            {"k": "الحد اليومي", "v1": "5 / يوم", "v2": "*غير محدود"},
            {"k": "التنسيق", "v1": "رموز AI", "v2": "100% نظيف"},
            {"k": "مشاركة", "v1": "نص + علامة", "v2": "PDF + نظيف"},
            {"k": "اللغات", "v1": "16+ عالمية", "v2": "16+ عالمية"},
            {"k": "أوضاع", "v1": "أساسي (6)", "v2": "الكل 18 + Custom"},
            {"k": "العلامة المائية", "v1": "موجودة", "v2": "محذوفة"},
            {"k": "الدعم", "v1": "قياسي", "v2": "VIP أولوية"},
            {"k": "السعر", "v1": "مجاني", "v2": "$12.90"}
        ]
    elif lang == "Hindi":
        headers = ["क्षमता", "गेस्ट", "💎 PRO लाइफटाइम"]
        rows = [
            {"k": "दैनिक सीमा", "v1": "5 / दिन", "v2": "*असीमित"},
            {"k": "प्रारूप", "v1": "AI प्रतीक", "v2": "100% साफ"},
            {"k": "साझा करें", "v1": "टेक्स्ट + वाटरमार्क", "v2": "PDF + साफ"},
            {"k": "भाषाएं", "v1": "16+ ग्लोबल", "v2": "16+ ग्लोबल"},
            {"k": "मोड", "v1": "बेसिक (6)", "v2": "सभी 18 + Custom"},
            {"k": "वाटरमार्क", "v1": "हाँ", "v2": "हटा दिया"},
            {"k": "समर्थन", "v1": "मानक", "v2": "VIP प्राथमिकता"},
            {"k": "मूल्य", "v1": "मुफ़्त", "v2": "$12.90"}
        ]
    elif lang == "Thai":
        headers = ["คุณสมบัติ", "ทั่วไป", "💎 PRO ตลอดชีพ"]
        rows = [
            {"k": "จำกัดรายวัน", "v1": "5 / วัน", "v2": "*ไม่จำกัด"},
            {"k": "รูปแบบ", "v1": "สัญลักษณ์ AI", "v2": "100% สะอาด"},
            {"k": "แชร์", "v1": "ข้อความ + ลายน้ำ", "v2": "PDF + สะอาด"},
            {"k": "ภาษา", "v1": "16+ ทั่วโลก", "v2": "16+ ทั่วโลก"},
            {"k": "โหมด", "v1": "พื้นฐาน (6)", "v2": "ครบ 18 + Custom"},
            {"k": "ลายน้ำ", "v1": "มี", "v2": "ลบออก"},
            {"k": "สนับสนุน", "v1": "มาตรฐาน", "v2": "VIP ด่วน"},
            {"k": "ราคา", "v1": "ฟรี", "v2": "$12.90"}
        ]
    elif lang == "Vietnamese":
        headers = ["Tính năng", "Khách", "💎 PRO Trọn đời"]
        rows = [
            {"k": "Giới hạn ngày", "v1": "5 / Ngày", "v2": "*Không giới hạn"},
            {"k": "Định dạng", "v1": "Ký tự AI", "v2": "100% Sạch"},
            {"k": "Chia sẻ", "v1": "Văn bản + Logo", "v2": "PDF + Sạch"},
            {"k": "Ngôn ngữ", "v1": "16+ Toàn cầu", "v2": "16+ Toàn cầu"},
            {"k": "Chế độ", "v1": "Cơ bản (6)", "v2": "Tất cả 18 + Custom"},
            {"k": "Watermark", "v1": "Có", "v2": "Đã xóa"},
            {"k": "Hỗ trợ", "v1": "Tiêu chuẩn", "v2": "VIP Ưu tiên"},
            {"k": "Giá", "v1": "Miễn phí", "v2": "$12.90"}
        ]
    
    return headers, rows

# ==========================================
# 3. 16 国语言 UI 完整映射 (调用上方生成器)
# ==========================================
TABLE_EN = get_table_data("English")[1] # 默认英文数据

BASE_EN = {
    "sidebar_title": "Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
    "usage": "Daily Usage", "lang": "🌐 Language", "role": "🎭 Role", "tone": "🗣️ Tone Style",
    "logout": "🚪 Logout", "mode": "⚙️ Select Mode", "action": "⚡ Select Action", 
    "input_label": "📝 Context", "generate": "✨ Generate", "lock_msg": "🔒 Locked (Pro Only)", 
    "buy_btn": "👉 Upgrade to Pro", "result": "✨ Result", "live_stat": "Live Status",
    "tbl_headers": get_table_data("English")[0], "tbl_data": get_table_data("English")[1]
}

LANG_MAP = {}
# 为所有语言生成映射
for lang in ALL_LANGUAGES:
    headers, rows = get_table_data(lang)
    
    # 基础 UI 词汇 (此处简化，您可以根据需要为每种语言定制 "sidebar_title" 等)
    # 重点是替换 tbl_headers 和 tbl_data
    lang_ui = BASE_EN.copy()
    lang_ui["tbl_headers"] = headers
    lang_ui["tbl_data"] = rows
    
    # 这里为了演示，我手动覆盖几种常用语言的 UI 词汇
    if lang == "简体中文":
        lang_ui.update({
            "sidebar_title": "Lai's Lab", "plan_guest": "访客计划", "plan_pro": "企业版 Pro",
            "usage": "今日用量", "lang": "🌐 语言设置", "role": "🎭 角色选择", "tone": "🗣️ 语气风格",
            "logout": "🚪 退出登录", "mode": "⚙️ 模式选择", "action": "⚡ 执行操作", 
            "input_label": "📝 详细要求", "generate": "✨ 开始生成", "lock_msg": "🔒 该模式仅限 Pro", 
            "buy_btn": "👉 升级 Pro 版", "result": "✨ 生成结果", "live_stat": "实时状态"
        })
    elif lang == "繁體中文":
        lang_ui.update({
            "sidebar_title": "Lai's Lab", "plan_guest": "訪客計劃", "plan_pro": "企業版 Pro",
            "usage": "今日用量", "lang": "🌐 語言設定", "role": "🎭 角色選擇", "tone": "🗣️ 語氣風格",
            "logout": "🚪 登出", "mode": "⚙️ 模式選擇", "action": "⚡ 執行操作", 
            "input_label": "📝 詳細要求", "generate": "✨ 開始生成", "lock_msg": "🔒 該模式僅限 Pro", 
            "buy_btn": "👉 升級 Pro 版", "result": "✨ 生成結果", "live_stat": "實時狀態"
        })
    # ... (其他语言会使用英文 UI 词汇，但表格内容已经是母语了！)
    
    LANG_MAP[lang] = lang_ui

LANG_MAP["default"] = BASE_EN

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
# 5. 5 大工单类型 (The 5 Ticket Types)
# ==========================================
TICKET_TYPES = [
    "🔴 Bug/Error Report",
    "🟠 Billing Issues",
    "🟡 Feature Request",
    "🟢 Partnership",
    "🔵 Other"
]

# ==========================================
# 6. 16 项 FAQ 完整拦截 (严格对应 16 FAQ.docx)
# ==========================================
INTERCEPTORS = {
    # Category 1: Purchase & License
    "subscription": "No. It is a One-Time Payment of $12.90. No monthly fees.",
    "refund": "Strictly No Refunds. This is a digital product (License Key) with instant access.",
    "key": "Lost Key? Please visit the LemonSqueezy Order Locator to recover it.",
    "devices": "Yes. Your license is tied to your email, accessible on mobile/desktop.",
    
    # Category 2: Business & Affiliate
    "affiliate": "Yes! You earn 40% commission on every sale. Sign up via our LemonSqueezy Affiliate Hub.",
    "invoice": "LemonSqueezy automatically emails you a tax invoice immediately after purchase.",
    "school": "Yes. For schools buying 10+ licenses, please contact support for a tailored quote.",
    
    # Category 3: Technical Support
    "pdf": "PDF Text missing? This happens if system font is missing. Please contact support.",
    "wechat": "WeChat button not working? Click the green icon -> Select 'WeChat' from share menu.",
    "invalid": "Invalid Key? Ensure no spaces are copied. Check your email spelling.",
    "slow": "Guest users are in a shared queue. PRO users enjoy dedicated high-speed servers.",
    
    # Category 4: Usage Limits
    "limit": "Is PRO Unlimited? Yes for text. For images, fair usage policy of ~200/day.",
    "commercial": "Can I use content commercially? Yes, PRO users have 100% commercial rights.",
    "offline": "Does it work offline? No. PromptLab is a cloud-based AI engine and requires internet.",
    
    # Category 5: Privacy & Security
    "privacy": "Do you store prompts? We prioritize privacy. Inputs are processed for generation only.",
    "share": "Can I share my account? No. Sharing accounts triggers our anti-abuse system."
}

# ==========================================
# 7. 完整的 126 个模式 + 自动注入 "7. Custom"
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
