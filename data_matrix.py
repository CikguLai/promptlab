# data_matrix.py
# Lai's Lab V9.28 - Global 15-Language Matrix (Dynamic Table Edition)

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
# 2. 15 国语言 UI 完整映射 (含表格数据)
# ==========================================
# 提取公共的表格数据结构，方便复用
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

LANG_MAP = {
    "default": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
        "usage": "Daily Usage", "lang": "🌐 Language", "role": "🎭 Role", "tone": "🗣️ Tone Style",
        "logout": "🚪 Logout", "mode": "⚙️ Select Mode", "action": "⚡ Select Action", 
        "input_label": "📝 Context", "generate": "✨ Generate with PASEC", 
        "lock_msg": "🔒 Pro Feature Locked", "buy_btn": "👉 Get Pro Access", 
        "result": "✨ PASEC Result", "live_stat": "Live Status",
        # 表格配置
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
        # 中文专用表格配置 (PDF数据)
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
        "tbl_data": TABLE_EN # 暂时复用英文数据，您可以后续翻译
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
    }
    # ... 其他语言会默认回退到 default (English)，这保证了系统不会崩 ...
}

# ==========================================
# 3. 角色与模式配置 (Role Configuration)
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
# 4. 智能拦截字典 (FAQ Logic)
# ==========================================
INTERCEPTORS = {
    "price": "$12.90 Lifetime",
    "refund": "No refunds on digital keys",
    "free": "Guest plan is free (5/day)",
    "support": "VIP support in 1-2 days"
}
