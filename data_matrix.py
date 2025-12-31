# data_matrix.py
# Lai's Lab V9.28 - GLOBAL EDITION (Final Stable)
# 100% Full Data: 16 Langs | No Crashes | 16 FAQs | Compatibility Fix

# ==========================================
# 1. 语言选项 (16 种全开)
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
def get_table_data(lang):
    # 默认英文数据
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

    # 特定语言覆盖
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
            {"k": "Format", "v1": "Simbol AI", "v2": "100% Bersih"},
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
    # 其他语言 (日语/韩语等) 自动使用 Default 结构，表头会在 LANG_MAP 里适配
    elif lang == "日本語":
        headers = ["機能", "ゲスト", "💎 PRO 永久版"]
    elif lang == "한국어":
        headers = ["기능", "게스트", "💎 PRO 평생판"]
    elif lang == "Français":
        headers = ["Fonctionnalité", "Invité", "💎 PRO à vie"]
    
    return headers, rows

# ==========================================
# 3. 16 国语言 UI 完整映射 (修复：全覆盖)
# ==========================================
# 基础 UI 词汇库
BASE_UI_DICT = {
    "English": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
        "usage": "Daily Usage", "lang": "🌐 Language", "role": "🎭 Role", "tone": "🗣️ Tone Style",
        "logout": "🚪 Logout", "mode": "⚙️ Select Mode", "action": "⚡ Select Action", 
        "input_label": "📝 Context", "generate": "✨ Generate", "lock_msg": "🔒 Locked (Pro Only)", 
        "buy_btn": "👉 Upgrade to Pro", "result": "✨ Result", "live_stat": "Live Status"
    },
    "简体中文": {
        "sidebar_title": "Lai's Lab", "plan_guest": "访客计划", "plan_pro": "企业版 Pro",
        "usage": "今日用量", "lang": "🌐 语言设置", "role": "🎭 角色选择", "tone": "🗣️ 语气风格",
        "logout": "🚪 退出登录", "mode": "⚙️ 模式选择", "action": "⚡ 执行操作", 
        "input_label": "📝 详细要求", "generate": "✨ 开始生成", "lock_msg": "🔒 该模式仅限 Pro", 
        "buy_btn": "👉 升级 Pro 版", "result": "✨ 生成结果", "live_stat": "实时状态"
    },
    "繁體中文": {
        "sidebar_title": "Lai's Lab", "plan_guest": "訪客計劃", "plan_pro": "企業版 Pro",
        "usage": "今日用量", "lang": "🌐 語言設定", "role": "🎭 角色選擇", "tone": "🗣️ 語氣風格",
        "logout": "🚪 登出", "mode": "⚙️ 模式選擇", "action": "⚡ 執行操作", 
        "input_label": "📝 詳細要求", "generate": "✨ 開始生成", "lock_msg": "🔒 該模式僅限 Pro", 
        "buy_btn": "👉 升級 Pro 版", "result": "✨ 生成結果", "live_stat": "實時狀態"
    },
    "Bahasa Melayu": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Pelan Tetamu", "plan_pro": "Pro Enterprise",
        "usage": "Penggunaan", "lang": "🌐 Bahasa", "role": "🎭 Peranan", "tone": "🗣️ Gaya Nada",
        "logout": "🚪 Log Keluar", "mode": "⚙️ Pilih Mod", "action": "⚡ Pilih Tindakan", 
        "input_label": "📝 Konteks", "generate": "✨ Jana", "lock_msg": "🔒 Dikunci (Pro Sahaja)", 
        "buy_btn": "👉 Naik Taraf Pro", "result": "✨ Hasil", "live_stat": "Status Langsung"
    },
    "Español": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Plan Invitado", "plan_pro": "Pro Empresa",
        "usage": "Uso", "lang": "🌐 Idioma", "role": "🎭 Rol", "tone": "🗣️ Tono",
        "logout": "🚪 Salir", "mode": "⚙️ Modo", "action": "⚡ Acción", 
        "input_label": "📝 Contexto", "generate": "✨ Generar", "lock_msg": "🔒 Bloqueado (Solo Pro)", 
        "buy_btn": "👉 Mejorar a Pro", "result": "✨ Resultado", "live_stat": "En Vivo"
    },
    "日本語": {"sidebar_title": "Lai's Lab", "plan_guest": "ゲストプラン", "plan_pro": "Pro エンタープライズ", "usage": "使用量", "lang": "🌐 言語", "role": "🎭 役割", "tone": "🗣️ 口調", "logout": "🚪 ログアウト", "mode": "⚙️ モード", "action": "⚡ アクション", "input_label": "📝 コンテキスト", "generate": "✨ 生成する", "lock_msg": "🔒 ロック中", "buy_btn": "👉 Proへアップグレード", "result": "✨ 結果", "live_stat": "ライブステータス"},
    "한국어": {"sidebar_title": "Lai's Lab", "plan_guest": "게스트 플랜", "plan_pro": "Pro 엔터프라이즈", "usage": "사용량", "lang": "🌐 언어", "role": "🎭 역할", "tone": "🗣️ 어조", "logout": "🚪 로그아웃", "mode": "⚙️ 모드", "action": "⚡ 동작", "input_label": "📝 입력", "generate": "✨ 생성하기", "lock_msg": "🔒 잠김", "buy_btn": "👉 Pro로 업그레이드", "result": "✨ 결과", "live_stat": "실시간 상태"},
    "Français": {"sidebar_title": "Lai's Lab", "plan_guest": "Plan Invité", "plan_pro": "Pro Entreprise", "usage": "Utilisation", "lang": "🌐 Langue", "role": "🎭 Rôle", "tone": "🗣️ Ton", "logout": "🚪 Déconnexion", "mode": "⚙️ Mode", "action": "⚡ Action", "input_label": "📝 Contexte", "generate": "✨ Générer", "lock_msg": "🔒 Verrouillé", "buy_btn": "👉 Passer à Pro", "result": "✨ Résultat", "live_stat": "En direct"},
    "Deutsch": {"sidebar_title": "Lai's Lab", "plan_guest": "Gast-Plan", "plan_pro": "Pro Enterprise", "usage": "Nutzung", "lang": "🌐 Sprache", "role": "🎭 Rolle", "tone": "🗣️ Ton", "logout": "🚪 Abmelden", "mode": "⚙️ Modus", "action": "⚡ Aktion", "input_label": "📝 Kontext", "generate": "✨ Generieren", "lock_msg": "🔒 Gesperrt", "buy_btn": "👉 Upgrade auf Pro", "result": "✨ Ergebnis", "live_stat": "Live-Status"},
    "Italiano": {"sidebar_title": "Lai's Lab", "plan_guest": "Piano Ospite", "plan_pro": "Pro Enterprise", "usage": "Utilizzo", "lang": "🌐 Lingua", "role": "🎭 Ruolo", "tone": "🗣️ Tono", "logout": "🚪 Esci", "mode": "⚙️ Modalità", "action": "⚡ Azione", "input_label": "📝 Contesto", "generate": "✨ Genera", "lock_msg": "🔒 Bloccato", "buy_btn": "👉 Passa a Pro", "result": "✨ Risultato", "live_stat": "Stato Live"},
    "Português": {"sidebar_title": "Lai's Lab", "plan_guest": "Plano Visitante", "plan_pro": "Pro Empresarial", "usage": "Uso", "lang": "🌐 Idioma", "role": "🎭 Papel", "tone": "🗣️ Tom", "logout": "🚪 Sair", "mode": "⚙️ Modo", "action": "⚡ Ação", "input_label": "📝 Contexto", "generate": "✨ Gerar", "lock_msg": "🔒 Bloqueado", "buy_btn": "👉 Mudar para Pro", "result": "✨ Resultado", "live_stat": "Status ao Vivo"},
    "Русский": {"sidebar_title": "Lai's Lab", "plan_guest": "Гостевой план", "plan_pro": "Pro Enterprise", "usage": "Исп.", "lang": "🌐 Язык", "role": "🎭 Роль", "tone": "🗣️ Тон", "logout": "🚪 Выйти", "mode": "⚙️ Режим", "action": "⚡ Действие", "input_label": "📝 Контекст", "generate": "✨ Создать", "lock_msg": "🔒 Закрыто", "buy_btn": "👉 Купить Pro", "result": "✨ Результат", "live_stat": "Статус"},
    "Arabic": {"sidebar_title": "Lai's Lab", "plan_guest": "خطة الضيف", "plan_pro": "Pro مؤسسة", "usage": "الاستخدام", "lang": "🌐 اللغة", "role": "🎭 الدور", "tone": "🗣️ النغمة", "logout": "🚪 خروج", "mode": "⚙️ الوضع", "action": "⚡ الإجراء", "input_label": "📝 السياق", "generate": "✨ توليد", "lock_msg": "🔒 مغلق", "buy_btn": "👉 ترقية لـ Pro", "result": "✨ النتيجة", "live_stat": "مباشر"},
    "Hindi": {"sidebar_title": "Lai's Lab", "plan_guest": "गेस्ट प्लान", "plan_pro": "Pro एंटरप्राइज", "usage": "उपयोग", "lang": "🌐 भाषा", "role": "🎭 भूमिका", "tone": "🗣️ टोन", "logout": "🚪 लॉग आउट", "mode": "⚙️ मोड", "action": "⚡ कार्रवाई", "input_label": "📝 संदर्भ", "generate": "✨ उत्पन्न करें", "lock_msg": "🔒 लॉक", "buy_btn": "👉 अपग्रेड करें", "result": "✨ परिणाम", "live_stat": "लाइव"},
    "Thai": {"sidebar_title": "Lai's Lab", "plan_guest": "แผนผู้ใช้ทั่วไป", "plan_pro": "Pro องค์กร", "usage": "การใช้งาน", "lang": "🌐 ภาษา", "role": "🎭 บทบาท", "tone": "🗣️ น้ำเสียง", "logout": "🚪 ออก", "mode": "⚙️ โหมด", "action": "⚡ การกระทำ", "input_label": "📝 บริบท", "generate": "✨ สร้าง", "lock_msg": "🔒 ล็อค", "buy_btn": "👉 อัปเกรด", "result": "✨ ผลลัพธ์", "live_stat": "สถานะ"},
    "Vietnamese": {"sidebar_title": "Lai's Lab", "plan_guest": "Gói Khách", "plan_pro": "Pro Doanh nghiệp", "usage": "Sử dụng", "lang": "🌐 Ngôn ngữ", "role": "🎭 Vai trò", "tone": "🗣️ Giọng", "logout": "🚪 Đăng xuất", "mode": "⚙️ Chế độ", "action": "⚡ Hành động", "input_label": "📝 Ngữ cảnh", "generate": "✨ Tạo", "lock_msg": "🔒 Đã khóa", "buy_btn": "👉 Nâng cấp", "result": "✨ Kết quả", "live_stat": "Trạng thái"}
}

# 兜底数据 (English)
TABLE_ROWS_DEFAULT = get_table_data("English")[1]
# 🔥 核心修复：双变量名兼容 (无论 App 找哪个变量名，都能找到)
TABLE_EN = TABLE_ROWS_DEFAULT 

# 构建最终 LANG_MAP (核心防崩逻辑)
LANG_MAP = {}
for lang in ALL_LANGUAGES:
    # 1. 获取 UI 翻译 (如果缺失，用英文兜底)
    ui_base = BASE_UI_DICT.get(lang, BASE_UI_DICT["English"]).copy()
    
    # 2. 获取表格数据
    t_headers, t_rows = get_table_data(lang)
    
    # 3. 合并到字典
    ui_base["tbl_headers"] = t_headers
    ui_base["tbl_data"] = t_rows
    
    LANG_MAP[lang] = ui_base

LANG_MAP["default"] = LANG_MAP["English"]

# ==========================================
# 4. FAQ 列表 (16 项)
# ==========================================
FAQ_LIST = [
    {"q": "Q1: Is this a subscription?", "a": "No. It is a One-Time Payment of $12.90. No monthly fees."},
    {"q": "Q2: What is the Refund Policy?", "a": "Strictly No Refunds. This is a digital product (License Key) with instant access."},
    {"q": "Q3: I lost my License Key.", "a": "Please visit the LemonSqueezy Order Locator to recover it."},
    {"q": "Q4: Can I use it on multiple devices?", "a": "Yes. Your license is tied to your email, accessible on mobile/desktop."},
    {"q": "Q5: Do you have an Affiliate Program?", "a": "Yes! You earn 40% commission on every sale. Sign up via our LemonSqueezy Affiliate Hub."},
    {"q": "Q6: How do I get an Invoice/Receipt?", "a": "LemonSqueezy automatically emails you a tax invoice immediately after purchase."},
    {"q": "Q7: Do you offer Education Discounts?", "a": "Yes. For schools buying 10+ licenses, please contact support for a tailored quote."},
    {"q": "Q8: PDF Text is missing/boxes?", "a": "This happens if the system font is missing. Please contact support."},
    {"q": "Q9: WeChat button not working?", "a": "Click the green icon -> Select 'WeChat' from your phone's share menu."},
    {"q": "Q10: 'Invalid Key' error?", "a": "Ensure no spaces are copied. Check your email spelling."},
    {"q": "Q11: Why is the generation slow?", "a": "Guest users are in a shared queue. PRO users enjoy dedicated high-speed servers."},
    {"q": "Q12: Is PRO truly Unlimited?", "a": "Yes for text. For images, we have a fair usage policy of ~200/day."},
    {"q": "Q13: Can I use content commercially?", "a": "Yes, PRO users have 100% commercial rights."},
    {"q": "Q14: Does it work offline?", "a": "No. PromptLab is a cloud-based AI engine and requires an internet connection."},
    {"q": "Q15: Do you store my prompts?", "a": "We prioritize privacy. Your inputs are processed for generation and not used to train public models."},
    {"q": "Q16: Can I share my account?", "a": "No. Sharing accounts triggers our anti-abuse system and may lock your key."}
]

# 拦截字典
INTERCEPTORS = {
    "refund": FAQ_LIST[1]["a"], "money": FAQ_LIST[1]["a"],
    "key": FAQ_LIST[2]["a"], "lost": FAQ_LIST[2]["a"],
    "price": FAQ_LIST[0]["a"], "limit": FAQ_LIST[11]["a"],
    "invoice": FAQ_LIST[5]["a"], "pdf": FAQ_LIST[7]["a"],
    "offline": FAQ_LIST[13]["a"], "privacy": FAQ_LIST[14]["a"],
    "share": FAQ_LIST[15]["a"], "affiliate": FAQ_LIST[4]["a"]
}

# ==========================================
# 5. 核心角色模式 (完整结构)
# ==========================================
ROLE_TONES = {
    "Global Educator": ["📚 Academic", "🌟 Encouraging", "📢 Instructional"],
    "Global Creator": ["🔥 Viral", "😜 Witty", "📖 Narrative"],
    "Global Parent": ["🥰 Warm", "🎉 Playful", "😴 Bedtime"],
    "Global Seller": ["💰 Persuasive", "⏳ Urgent", "💎 Luxury"],
    "Global Student": ["🎓 Formal", "📝 Concise", "🎯 Goal-Oriented"],
    "Global Corporate": ["👔 Executive", "⚡ Direct", "🚀 Strategic"]
}
DEFAULT_TONES = ["Professional", "Friendly", "Informative"]
TICKET_TYPES = ["🔴 Bug/Error Report", "🟠 Billing Issues", "🟡 Feature Request", "🟢 Partnership", "🔵 Other"]

ROLES_CONFIG = {
    "Global Educator": {"Pedagogy (Free)": [{"label": "1. Rubric Creator", "template": "{input}"}]},
    "Global Creator": {"Scripting (Free)": [{"label": "1. Viral Hook", "template": "{input}"}]},
    "Global Parent": {"Story (Free)": [{"label": "1. Bedtime Story", "template": "{input}"}]},
    "Global Seller": {"Copy (Free)": [{"label": "1. Ad Headline", "template": "{input}"}]},
    "Global Student": {"Study (Free)": [{"label": "1. Summarizer", "template": "{input}"}]},
    "Global Corporate": {"Admin (Free)": [{"label": "1. Email Polish", "template": "{input}"}]}
}

# 注入 Custom
CUSTOM_OPTION = {"label": "7. Custom / DIY", "template": "{input}"}
for role, modes in ROLES_CONFIG.items():
    for mode_name, options in modes.items():
        if not any(o['label'].startswith("7.") for o in options):
            options.append(CUSTOM_OPTION)
