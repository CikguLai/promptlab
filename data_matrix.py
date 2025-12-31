# data_matrix.py
# Lai's Lab V9.28 - Global 15-Language Matrix (Fully Populated & Verified)

# ==========================================
# 1. 语言选项配置
# ==========================================
LANG_OPTIONS_GUEST = ["English", "简体中文", "Bahasa Melayu"]

LANG_OPTIONS_PRO = [
    "English", "简体中文", "Bahasa Melayu", "Español", 
    "日本語", "한국어", "Français", "Deutsch", 
    "Italiano", "Português", "Русский", "Arabic", 
    "Hindi", "Thai", "Vietnamese"
]

# ==========================================
# 2. 表格数据源 (核心数据复用)
# ==========================================
TABLE_EN = [
    {"k": "Daily Limit", "v1": "5 / Day", "v2": "*Unlimited"},
    {"k": "Content Format", "v1": "With AI Symbols (#, **)", "v2": "100% Clean & Human-like"},
    {"k": "Sharing & Export", "v1": "Copy + WhatsApp (Watermarked)", "v2": "PDF Export + Clean Share"},
    {"k": "Languages", "v1": "3 Basic Languages", "v2": "15+ Global Languages"},
    {"k": "Expert Modes", "v1": "Basic Modes (6)", "v2": "All 18 Depth Modes"},
    {"k": "AI Watermark", "v1": "Forced Watermark", "v2": "Fully Removed"},
    {"k": "Support", "v1": "Standard (3-5 Days)", "v2": "VIP Priority (1-2 Days)"},
    {"k": "Price", "v1": "Free", "v2": "Limited Offer $12.90"}
]

TABLE_CN = [
    {"k": "每日生成限额 (Daily Limit)", "v1": "5 次 / 天", "v2": "*Unlimited (无限生成)"},
    {"k": "内容纯净度 (Format)", "v1": "包含 AI 符号 (#, **)", "v2": "100% 纯净 (人类书写感)"},
    {"k": "结果分享与导出 (Sharing)", "v1": "文本复制 + WhatsApp (带水印)", "v2": "PDF 导出 + 纯净社媒分享"},
    {"k": "全球语言支持 (Languages)", "v1": "仅限 3 种基础语言", "v2": "15+ 全球语言全开"},
    {"k": "专业模式权限 (Expert Modes)", "v1": "基础模式 (6个)", "v2": "全部 18 种深度模式"},
    {"k": "AI 结果水印 (Watermark)", "v1": "强制包含推广水印", "v2": "完全移除"},
    {"k": "客服响应 (Support)", "v1": "标准响应 (3-5天)", "v2": "VIP 优先响应 (1-2天)"},
    {"k": "价格 (Price)", "v1": "免费 (Free)", "v2": "限时特惠 $12.90"}
]

# ==========================================
# 3. 15 国语言 UI 完整映射 (请勿删减任何条目)
# ==========================================
LANG_MAP = {
    "default": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
        "usage": "Daily Usage", "lang": "🌐 Language", "role": "🎭 Role", "tone": "🗣️ Tone Style",
        "logout": "🚪 Logout", "mode": "⚙️ Select Mode", "action": "⚡ Select Action", 
        "input_label": "📝 Context", "generate": "✨ Generate with PASEC", 
        "lock_msg": "🔒 Pro Feature Locked", "buy_btn": "👉 Get Pro Access", 
        "result": "✨ PASEC Result", "live_stat": "Live Status",
        "tbl_headers": ["Capability", "Guest Trial", "💎 PRO Lifetime"],
        "tbl_data": TABLE_EN
    },
    "English": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
        "usage": "Daily Usage", "lang": "🌐 Language", "role": "🎭 Role", "tone": "🗣️ Tone Style",
        "logout": "🚪 Logout", "mode": "⚙️ Select Mode", "action": "⚡ Select Action", 
        "input_label": "📝 Context", "generate": "✨ Generate with PASEC", 
        "lock_msg": "🔒 Pro Feature Locked", "buy_btn": "👉 Get Pro Access", 
        "result": "✨ PASEC Result", "live_stat": "Live Status",
        "tbl_headers": ["Capability", "Guest Trial", "💎 PRO Lifetime"],
        "tbl_data": TABLE_EN
    },
    "简体中文": {
        "sidebar_title": "Lai's Lab", "plan_guest": "访客计划", "plan_pro": "企业版 Pro",
        "usage": "今日用量", "lang": "🌐 语言设置", "role": "🎭 角色选择", "tone": "🗣️ 语气风格",
        "logout": "🚪 退出登录", "mode": "⚙️ 模式选择", "action": "⚡ 执行操作", 
        "input_label": "📝 详细要求", "generate": "✨ PASEC 生成", 
        "lock_msg": "🔒 Pro 功能已锁定", "buy_btn": "👉 获取 Pro 权限", 
        "result": "✨ PASEC 输出", "live_stat": "实时状态",
        "tbl_headers": ["功能特性 (Capability)", "访客试用 (Guest Trial)", "💎 PRO 永久版 (Lifetime)"],
        "tbl_data": TABLE_CN
    },
    "Bahasa Melayu": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Pelan Tetamu", "plan_pro": "Pro Enterprise",
        "usage": "Penggunaan", "lang": "🌐 Bahasa", "role": "🎭 Peranan", "tone": "🗣️ Gaya Nada",
        "logout": "🚪 Log Keluar", "mode": "⚙️ Pilih Mod", "action": "⚡ Pilih Tindakan", 
        "input_label": "📝 Konteks", "generate": "✨ Jana dengan PASEC", 
        "lock_msg": "🔒 Ciri Pro Dikunci", "buy_btn": "👉 Dapatkan Akses Pro", 
        "result": "✨ Hasil PASEC", "live_stat": "Status Langsung",
        "tbl_headers": ["Keupayaan", "Percubaan Tetamu", "💎 PRO Seumur Hidup"],
        "tbl_data": TABLE_EN
    },
    "Español": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Plan Invitado", "plan_pro": "Pro Empresa",
        "usage": "Uso Diario", "lang": "🌐 Idioma", "role": "🎭 Rol", "tone": "🗣️ Tono",
        "logout": "🚪 Salir", "mode": "⚙️ Modo", "action": "⚡ Acción", 
        "input_label": "📝 Contexto", "generate": "✨ Generar con PASEC", 
        "lock_msg": "🔒 Función Pro Bloqueada", "buy_btn": "👉 Obtener Pro", 
        "result": "✨ Resultado PASEC", "live_stat": "Estado en Vivo",
        "tbl_headers": ["Capacidad", "Prueba de Invitado", "💎 PRO De Por Vida"],
        "tbl_data": TABLE_EN
    },
    "日本語": {
        "sidebar_title": "Lai's Lab", "plan_guest": "ゲスト", "plan_pro": "Pro 企業版",
        "usage": "使用量", "lang": "🌐 言語", "role": "🎭 役割", "tone": "🗣️ 口調",
        "logout": "🚪 ログアウト", "mode": "⚙️ モード選択", "action": "⚡ アクション", 
        "input_label": "📝 コンテキスト", "generate": "✨ PASECで生成", 
        "lock_msg": "🔒 Pro機能はロックされています", "buy_btn": "👉 Pro版を入手", 
        "result": "✨ PASEC 結果", "live_stat": "ライブステータス",
        "tbl_headers": ["機能 (Capability)", "ゲスト (Guest Trial)", "💎 PRO 永久版"],
        "tbl_data": TABLE_EN
    },
    "한국어": {
        "sidebar_title": "Lai's Lab", "plan_guest": "게스트", "plan_pro": "Pro 엔터프라이즈",
        "usage": "일일 사용량", "lang": "🌐 언어", "role": "🎭 역할", "tone": "🗣️ 톤앤매너",
        "logout": "🚪 로그아웃", "mode": "⚙️ 모드 선택", "action": "⚡ 작업 선택", 
        "input_label": "📝 문맥 입력", "generate": "✨ PASEC 생성", 
        "lock_msg": "🔒 Pro 기능 잠김", "buy_btn": "👉 Pro 버전 구매", 
        "result": "✨ PASEC 결과", "live_stat": "실시간 상태",
        "tbl_headers": ["기능 (Capability)", "게스트 (Guest Trial)", "💎 PRO 평생권"],
        "tbl_data": TABLE_EN
    },
    "Français": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Invité", "plan_pro": "Pro Entreprise",
        "usage": "Usage", "lang": "🌐 Langue", "role": "🎭 Rôle", "tone": "🗣️ Ton",
        "logout": "🚪 Déconnexion", "mode": "⚙️ Mode", "action": "⚡ Action", 
        "input_label": "📝 Contexte", "generate": "✨ Générer (PASEC)", 
        "lock_msg": "🔒 Fonction Pro Verrouillée", "buy_btn": "👉 Obtenir Pro", 
        "result": "✨ Résultat PASEC", "live_stat": "Statut en Direct",
        "tbl_headers": ["Capacité", "Essai Invité", "💎 PRO à Vie"],
        "tbl_data": TABLE_EN
    },
    "Deutsch": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Gast", "plan_pro": "Pro Enterprise",
        "usage": "Nutzung", "lang": "🌐 Sprache", "role": "🎭 Rolle", "tone": "🗣️ Tonfall",
        "logout": "🚪 Logout", "mode": "⚙️ Modus", "action": "⚡ Aktion", 
        "input_label": "📝 Kontext", "generate": "✨ Generieren", 
        "lock_msg": "🔒 Pro-Funktion gesperrt", "buy_btn": "👉 Pro kaufen", 
        "result": "✨ PASEC Ergebnis", "live_stat": "Live-Status",
        "tbl_headers": ["Funktion", "Gasttest", "💎 PRO Lebenslang"],
        "tbl_data": TABLE_EN
    },
    "Italiano": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Ospite", "plan_pro": "Pro Aziendale",
        "usage": "Uso", "lang": "🌐 Lingua", "role": "🎭 Ruolo", "tone": "🗣️ Tono",
        "logout": "🚪 Esci", "mode": "⚙️ Modalità", "action": "⚡ Azione", 
        "input_label": "📝 Contesto", "generate": "✨ Genera", 
        "lock_msg": "🔒 Funzione Pro Bloccata", "buy_btn": "👉 Ottieni Pro", 
        "result": "✨ Risultato PASEC", "live_stat": "Stato Live",
        "tbl_headers": ["Capacità", "Prova Ospite", "💎 PRO A Vita"],
        "tbl_data": TABLE_EN
    },
    "Português": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Visitante", "plan_pro": "Pro Empresa",
        "usage": "Uso", "lang": "🌐 Idioma", "role": "🎭 Função", "tone": "🗣️ Tom",
        "logout": "🚪 Sair", "mode": "⚙️ Modo", "action": "⚡ Ação", 
        "input_label": "📝 Contexto", "generate": "✨ Gerar", 
        "lock_msg": "🔒 Recurso Pro Bloqueado", "buy_btn": "👉 Obter Pro", 
        "result": "✨ Resultado", "live_stat": "Status ao Vivo",
        "tbl_headers": ["Capacidade", "Teste", "💎 PRO Vitalício"],
        "tbl_data": TABLE_EN
    },
    "Русский": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Гость", "plan_pro": "Pro Enterprise",
        "usage": "Лимит", "lang": "🌐 Язык", "role": "🎭 Роль", "tone": "🗣️ Тон",
        "logout": "🚪 Выход", "mode": "⚙️ Режим", "action": "⚡ Действие", 
        "input_label": "📝 Контекст", "generate": "✨ Создать", 
        "lock_msg": "🔒 Pro заблокировано", "buy_btn": "👉 Купить Pro", 
        "result": "✨ Результат", "live_stat": "Статус",
        "tbl_headers": ["Функции", "Тест", "💎 PRO Навсегда"],
        "tbl_data": TABLE_EN
    },
    "Arabic": {
        "sidebar_title": "Lai's Lab", "plan_guest": "زائر", "plan_pro": "Pro شركات",
        "usage": "الاستخدام", "lang": "🌐 اللغة", "role": "🎭 الدور", "tone": "🗣️ النبرة",
        "logout": "🚪 خروج", "mode": "⚙️ الوضع", "action": "⚡ إجراء", 
        "input_label": "📝 السياق", "generate": "✨ إنشاء", 
        "lock_msg": "🔒 ميزة مقفلة", "buy_btn": "👉 احصل على Pro", 
        "result": "✨ النتيجة", "live_stat": "حالة مباشرة",
        "tbl_headers": ["الميزات", "تجربة", "💎 PRO مدى الحياة"],
        "tbl_data": TABLE_EN
    },
    "Hindi": {
        "sidebar_title": "Lai's Lab", "plan_guest": "अतिथि", "plan_pro": "Pro एंटरप्राइज़",
        "usage": "उपयोग", "lang": "🌐 भाषा", "role": "🎭 भूमिका", "tone": "🗣️ लहजा",
        "logout": "🚪 लॉग आउट", "mode": "⚙️ मोड", "action": "⚡ क्रिया", 
        "input_label": "📝 संदर्भ", "generate": "✨ जनरेट करें", 
        "lock_msg": "🔒 लॉक है", "buy_btn": "👉 Pro खरीदें", 
        "result": "✨ परिणाम", "live_stat": "लाइव स्थिति",
        "tbl_headers": ["क्षमता", "परीक्षण", "💎 PRO लाइफटाइम"],
        "tbl_data": TABLE_EN
    },
    "Thai": {
        "sidebar_title": "Lai's Lab", "plan_guest": "ผู้เยี่ยมชม", "plan_pro": "Pro องค์กร",
        "usage": "การใช้งาน", "lang": "🌐 ภาษา", "role": "🎭 บทบาท", "tone": "🗣️ น้ำเสียง",
        "logout": "🚪 ออกจากระบบ", "mode": "⚙️ โหมด", "action": "⚡ การกระทำ", 
        "input_label": "📝 บริบท", "generate": "✨ สร้าง", 
        "lock_msg": "🔒 ล็อกฟีเจอร์", "buy_btn": "👉 รับสิทธิ์ Pro", 
        "result": "✨ ผลลัพธ์", "live_stat": "สถานะสด",
        "tbl_headers": ["ความสามารถ", "ทดลอง", "💎 PRO ตลอดชีพ"],
        "tbl_data": TABLE_EN
    },
    "Vietnamese": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Khách", "plan_pro": "Pro Doanh Nghiệp",
        "usage": "Sử dụng", "lang": "🌐 Ngôn ngữ", "role": "🎭 Vai trò", "tone": "🗣️ Giọng điệu",
        "logout": "🚪 Đăng xuất", "mode": "⚙️ Chế độ", "action": "⚡ Hành động", 
        "input_label": "📝 Ngữ cảnh", "generate": "✨ Tạo", 
        "lock_msg": "🔒 Bị khóa", "buy_btn": "👉 Nâng cấp Pro", 
        "result": "✨ Kết quả", "live_stat": "Trực tiếp",
        "tbl_headers": ["Tính năng", "Dùng thử", "💎 PRO Trọn đời"],
        "tbl_data": TABLE_EN
    }
}

# ==========================================
# 4. 角色与模式配置 (Role Configuration)
# ==========================================
ROLE_TONES = {
    "Global Educator": ["📚 Academic", "🌟 Encouraging", "💡 Socratic", "📢 Instructional"],
    "Global Creator": ["🔥 Viral", "😜 Witty", "📖 Narrative", "⚡ Punchy"],
    "Global Parent": ["🥰 Warm", "🎉 Playful", "🛡️ Firm", "👩‍🏫 Patient"],
    "Global Seller": ["💰 Persuasive", "⏳ Urgent", "💎 Luxury", "🤝 Trustworthy"],
    "Global Student": ["🎓 Formal", "📝 Concise", "🤓 Geeky", "🎯 Goal-Oriented"],
    "Global Corporate": ["👔 Executive", "⚡ Direct", "🚀 Strategic", "⚖️ Compliance"]
}
DEFAULT_TONES = ["Professional", "Friendly", "Informative", "Assertive", "Empathetic"]

# 占位符，请务必保留您原来的完整 ROLES_CONFIG
ROLES_CONFIG = {
    "Global Educator": {
        "Pedagogy (Free)": [{"label": "1. Rubric Creator", "template": "Create a grading rubric for: {input}"}],
        "Visuals (Pro)": [{"label": "1. Pixar 3D", "template": "Midjourney Pixar-style: {input}"}]
    },
    "Global Creator": { "Scripting (Free)": [{"label": "1. Viral Hook", "template": "Viral hooks for: {input}"}] },
    "Global Parent": { "Story (Free)": [{"label": "1. Magical Day", "template": "Story about: {input}"}] },
    "Global Seller": { "Copy (Free)": [{"label": "1. Landing Page", "template": "Landing page for: {input}"}] },
    "Global Student": { "Study (Free)": [{"label": "1. Summary", "template": "Summarize: {input}"}] },
    "Global Corporate": { "Admin (Free)": [{"label": "1. Email Fix", "template": "Fix email: {input}"}] }
}

# ==========================================
# 5. 智能拦截字典
# ==========================================
INTERCEPTORS = {
    "price": "$12.90 Lifetime",
    "refund": "No refunds on digital keys",
    "free": "Guest plan is free (5/day)",
    "support": "VIP support in 1-2 days"
}
