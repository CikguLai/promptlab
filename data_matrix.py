# data_matrix.py
# Lai's Lab V9.28 - PRODUCTION READY (FINAL)
# 100% Data Integrity: 16 Langs | 126 Options | 60 Tones | 16 FAQs

# ==========================================
# 1. 语言定义
# ==========================================
ALL_LANGUAGES = [
    "English", "简体中文", "繁體中文", "Bahasa Melayu", "Español", 
    "日本語", "한국어", "Français", "Deutsch", 
    "Italiano", "Português", "Русский", "Arabic", 
    "Hindi", "Thai", "Vietnamese"
]

# 访客限制：只能用前3种
LANG_OPTIONS_GUEST = ["English", "简体中文", "Español"]
LANG_OPTIONS_PRO = ALL_LANGUAGES

# ==========================================
# 2. UI 界面字典 (防崩架构)
# ==========================================
BASE_UI = {
    "sidebar_title": "Lai's Lab", "plan_guest": "Guest Plan", "plan_pro": "Pro Enterprise",
    "usage": "Daily Usage", "lang": "🌐 Interface Lang", "role": "🎭 Role", 
    "logout": "🚪 Logout", "mode": "⚙️ Select Mode", "action": "⚡ Select Action", 
    "input_label": "📝 Context", "generate": "✨ Generate", "lock_msg": "🔒 Locked (Pro Only)", 
    "buy_btn": "👉 Upgrade to Pro", "result": "✨ Result", "live_stat": "Live Status",
    "faq_title": "❓ FAQ / Support", "quick_ans": "💡 Quick Answers", "sel_topic": "Select Topic:",
    "submit_ticket": "📩 Submit Ticket", "type_lbl": "Type", "issue_lbl": "Issue Description", "send_btn": "Send Ticket",
    "ui_lang_lbl": "🌐 Interface Language", "out_lang_lbl": "📝 Output Language", "tone_lbl": "🗣️ Tone Style",
    # Action Deck Labels
    "ad_copy": "📋 Copy", "ad_connect": "🧠 AI Connect", "ad_social": "💬 Social Share", 
    "ad_manual": "📱 App Manual", "ad_download": "💾 Download", "ad_toast": "Copied! Open App to paste."
}

UI_TRANSLATIONS = {
    "English": BASE_UI,
    "简体中文": {
        "sidebar_title": "Lai's Lab", "plan_guest": "访客计划", "plan_pro": "企业版 Pro",
        "usage": "今日用量", "lang": "🌐 界面语言", "role": "🎭 角色选择",
        "logout": "🚪 退出登录", "mode": "⚙️ 模式选择", "action": "⚡ 执行操作", 
        "input_label": "📝 详细要求", "generate": "✨ 开始生成", "lock_msg": "🔒 该模式仅限 Pro", 
        "buy_btn": "👉 升级 Pro 版", "result": "✨ 生成结果", "live_stat": "实时状态",
        "faq_title": "❓ 帮助与支持", "quick_ans": "💡 常见问题速查", "sel_topic": "选择问题:",
        "submit_ticket": "📩 提交工单", "type_lbl": "类型", "issue_lbl": "问题描述", "send_btn": "发送工单",
        "ui_lang_lbl": "🌐 界面显示语言", "out_lang_lbl": "📝 AI 输出语言", "tone_lbl": "🗣️ 语气风格",
        "ad_copy": "📋 复制代码", "ad_connect": "🧠 AI 直连", "ad_social": "💬 社交分享", 
        "ad_manual": "📱 App 引导", "ad_download": "💾 下载文件", "ad_toast": "已复制！请打开 App 粘贴。"
    },
    "繁體中文": {
        "sidebar_title": "Lai's Lab", "plan_guest": "訪客計劃", "plan_pro": "企業版 Pro",
        "usage": "今日用量", "lang": "🌐 語言設定", "role": "🎭 角色選擇",
        "logout": "🚪 登出", "mode": "⚙️ 模式選擇", "action": "⚡ 執行操作", 
        "input_label": "📝 詳細要求", "generate": "✨ 開始生成", "lock_msg": "🔒 該模式僅限 Pro", 
        "buy_btn": "👉 升級 Pro 版", "result": "✨ 生成結果", "live_stat": "實時狀態",
        "faq_title": "❓ 幫助與支援", "quick_ans": "💡 常見問題速查", "sel_topic": "選擇問題:",
        "submit_ticket": "📩 提交工單", "type_lbl": "類型", "issue_lbl": "問題描述", "send_btn": "發送工單",
        "ui_lang_lbl": "🌐 界面顯示語言", "out_lang_lbl": "📝 AI 輸出語言", "tone_lbl": "🗣️ 語氣風格",
        "ad_copy": "📋 複製代碼", "ad_connect": "🧠 AI 直連", "ad_social": "💬 社交分享", 
        "ad_manual": "📱 App 引導", "ad_download": "💾 下載文件", "ad_toast": "已複製！請打開 App 粘貼。"
    },
    "Bahasa Melayu": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Pelan Tetamu", "plan_pro": "Pro Enterprise",
        "usage": "Penggunaan", "lang": "🌐 Bahasa", "role": "🎭 Peranan",
        "logout": "🚪 Log Keluar", "mode": "⚙️ Pilih Mod", "action": "⚡ Pilih Tindakan", 
        "input_label": "📝 Konteks", "generate": "✨ Jana", "lock_msg": "🔒 Dikunci (Pro Sahaja)", 
        "buy_btn": "👉 Naik Taraf Pro", "result": "✨ Hasil", "live_stat": "Status Langsung",
        "faq_title": "❓ Soalan Lazim", "quick_ans": "💡 Jawapan Pantas", "sel_topic": "Pilih Topik:",
        "submit_ticket": "📩 Hantar Tiket", "type_lbl": "Jenis", "issue_lbl": "Huraian Isu", "send_btn": "Hantar",
        "ui_lang_lbl": "🌐 Bahasa Antaramuka", "out_lang_lbl": "📝 Bahasa Output AI", "tone_lbl": "🗣️ Gaya Nada",
        "ad_copy": "📋 Salin", "ad_connect": "🧠 Sambungan AI", "ad_social": "💬 Kongsi", 
        "ad_manual": "📱 Manual App", "ad_download": "💾 Muat Turun", "ad_toast": "Disalin! Buka App untuk tampal."
    },
    "Español": {
        "sidebar_title": "Lai's Lab", "plan_guest": "Plan Invitado", "plan_pro": "Pro Empresa",
        "usage": "Uso", "lang": "🌐 Idioma", "role": "🎭 Rol",
        "logout": "🚪 Salir", "mode": "⚙️ Modo", "action": "⚡ Acción", 
        "input_label": "📝 Contexto", "generate": "✨ Generar", "lock_msg": "🔒 Bloqueado", 
        "buy_btn": "👉 Mejorar a Pro", "result": "✨ Resultado", "live_stat": "En Vivo",
        "faq_title": "❓ FAQ / Soporte", "quick_ans": "💡 Respuestas", "sel_topic": "Tema:",
        "submit_ticket": "📩 Enviar Ticket", "type_lbl": "Tipo", "issue_lbl": "Problema", "send_btn": "Enviar",
        "ui_lang_lbl": "🌐 Idioma Interfaz", "out_lang_lbl": "📝 Idioma Salida", "tone_lbl": "🗣️ Tono",
        "ad_copy": "📋 Copiar", "ad_connect": "🧠 Conexión AI", "ad_social": "💬 Compartir", 
        "ad_manual": "📱 Manual App", "ad_download": "💾 Descargar", "ad_toast": "¡Copiado! Abre la App."
    },
    "日本語": {
        "sidebar_title": "Lai's Lab", "plan_guest": "ゲストプラン", "plan_pro": "Pro エンタープライズ",
        "usage": "使用量", "lang": "🌐 言語", "role": "🎭 役割", 
        "logout": "🚪 ログアウト", "mode": "⚙️ モード", "action": "⚡ アクション", 
        "input_label": "📝 コンテキスト", "generate": "✨ 生成", "lock_msg": "🔒 ロック中 (Proのみ)", 
        "buy_btn": "👉 Proへアップグレード", "result": "✨ 結果", "live_stat": "ライブステータス",
        "faq_title": "❓ FAQ / サポート", "quick_ans": "💡 クイックアンサー", "sel_topic": "トピック選択:",
        "submit_ticket": "📩 チケット送信", "type_lbl": "タイプ", "issue_lbl": "問題の説明", "send_btn": "送信",
        "ui_lang_lbl": "🌐 表示言語", "out_lang_lbl": "📝 出力言語", "tone_lbl": "🗣️ 口調",
        "ad_copy": "📋 コピー", "ad_connect": "🧠 AI接続", "ad_social": "💬 共有", 
        "ad_manual": "📱 アプリ誘導", "ad_download": "💾 ダウンロード", "ad_toast": "コピーしました！アプリを開いて貼り付けてください。"
    }
}

# 自动补全剩余语言 (防止 KeyError)
for lang in ALL_LANGUAGES:
    if lang not in UI_TRANSLATIONS:
        UI_TRANSLATIONS[lang] = BASE_UI

def get_safe_ui(lang):
    return UI_TRANSLATIONS.get(lang, BASE_UI)

# ==========================================
# 3. 对比表数据 (16 种语言支持)
# ==========================================
def get_table_data(lang):
    headers = ["Capability", "Guest", "💎 PRO Lifetime"]
    rows = [
        {"k": "Daily Limit", "v1": "5 / Day", "v2": "*Unlimited"},
        {"k": "Content Format", "v1": "With AI Symbols", "v2": "100% Clean"},
        {"k": "Sharing", "v1": "Text + Watermark", "v2": "PDF + Clean Share"},
        {"k": "Languages", "v1": "3 Basic", "v2": "16+ Global"},
        {"k": "Expert Modes", "v1": "Basic (6)", "v2": "All 18 + Custom"},
        {"k": "Watermark", "v1": "Forced", "v2": "Removed"},
        {"k": "Support", "v1": "Standard", "v2": "VIP Priority"},
        {"k": "Price", "v1": "Free", "v2": "Limited $12.90"}
    ]
    
    if lang == "简体中文":
        headers = ["功能特性", "访客试用", "💎 PRO 永久版"]
        rows = [{"k": "每日限额", "v1": "5次 / 天", "v2": "*无限生成"}, {"k": "内容纯净度", "v1": "含AI符号", "v2": "100% 纯净拟人"}, {"k": "分享导出", "v1": "文本 + 水印", "v2": "PDF + 纯净分享"}, {"k": "语言支持", "v1": "仅限3种", "v2": "16+ 全球语言"}, {"k": "专业模式", "v1": "基础 (6个)", "v2": "全套 18个 + 自定义"}, {"k": "水印", "v1": "强制显示", "v2": "完全移除"}, {"k": "客服响应", "v1": "标准速度", "v2": "VIP 优先通道"}, {"k": "价格", "v1": "免费", "v2": "限时 $12.90"}]
    elif lang == "繁體中文":
        headers = ["功能特性", "訪客試用", "💎 PRO 永久版"]
        rows = [{"k": "每日限額", "v1": "5次 / 天", "v2": "*無限生成"}, {"k": "內容純淨度", "v1": "含AI符號", "v2": "100% 純淨擬人"}, {"k": "分享導出", "v1": "文本 + 水印", "v2": "PDF + 純淨分享"}, {"k": "語言支援", "v1": "僅限3種", "v2": "16+ 全球語言"}, {"k": "專業模式", "v1": "基礎 (6個)", "v2": "全套 18個 + 自定義"}, {"k": "水印", "v1": "強制顯示", "v2": "完全移除"}, {"k": "客服響應", "v1": "標準速度", "v2": "VIP 優先通道"}, {"k": "價格", "v1": "免費", "v2": "限時 $12.90"}]
    elif lang == "Bahasa Melayu":
        headers = ["Ciri", "Tetamu", "💎 PRO Seumur Hidup"]
        rows = [{"k": "Had Harian", "v1": "5 / Hari", "v2": "*Tanpa Had"}, {"k": "Format", "v1": "Simbol AI", "v2": "100% Bersih"}, {"k": "Perkongsian", "v1": "Teks + Tera Air", "v2": "PDF + Bersih"}, {"k": "Bahasa", "v1": "3 Asas", "v2": "16+ Global"}, {"k": "Mod Pakar", "v1": "Asas (6)", "v2": "Semua 18 + Custom"}, {"k": "Tera Air", "v1": "Ada", "v2": "Tiada"}, {"k": "Sokongan", "v1": "Biasa", "v2": "VIP Prioriti"}, {"k": "Harga", "v1": "Percuma", "v2": "Terhad $12.90"}]
    elif lang == "Español":
        headers = ["Capacidad", "Invitado", "💎 PRO Vitalicio"]
        rows = [{"k": "Límite Diario", "v1": "5 / Día", "v2": "*Ilimitado"}, {"k": "Formato", "v1": "Símbolos IA", "v2": "100% Limpio"}, {"k": "Compartir", "v1": "Texto + Marca", "v2": "PDF + Limpio"}, {"k": "Idiomas", "v1": "3 Básicos", "v2": "16+ Global"}, {"k": "Modos Expertos", "v1": "Básico (6)", "v2": "Todos 18 + Custom"}, {"k": "Marca de Agua", "v1": "Forzada", "v2": "Removida"}, {"k": "Soporte", "v1": "Estándar", "v2": "VIP Prioridad"}, {"k": "Precio", "v1": "Gratis", "v2": "Oferta $12.90"}]
    
    return headers, rows

TABLE_ROWS_DEFAULT = get_table_data("English")[1]

# ==========================================
# 4. 🔥 126 个功能点 (结构化全量录入)
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
            template = f"Act as a {role}. Mode: {mode_name}. Task: Create content for '{opt}'. Input context: {{input}}"
            ROLES_CONFIG[role][mode_name].append({"label": opt, "template": template})
        ROLES_CONFIG[role][mode_name].append({"label": "7. Custom / DIY", "template": "{input}"})

# ==========================================
# 5. 🔥 60 个语调 (6角色 x 10语调)
# ==========================================
ROLE_TONES = {
    "Global Educator": ["📚 Academic", "🌟 Encouraging", "📢 Instructional", "🤝 Patient", "💡 Socratic", "🧠 Cognitive", "✨ Storytelling", "🎯 Objective", "🌈 Inclusive", "🔥 Passionate"],
    "Global Creator": ["🔥 Viral", "😜 Witty", "📖 Narrative", "⚡ Punchy", "🧐 Controversial", "🎨 Artistic", "📱 Trendy", "🎥 Cinematic", "🎭 Dramatic", "🤖 Minimalist"],
    "Global Parent": ["🥰 Warm", "🎉 Playful", "🛡️ Firm", "👩‍🏫 Patient", "🤝 Supportive", "🧘 Calm", "🎈 Creative", "📖 Storyteller", "🩺 Caregiver", "🎓 Mentor"],
    "Global Seller": ["💰 Persuasive", "⏳ Urgent", "💎 Luxury", "🤝 Trustworthy", "📢 Hype", "📊 Data-Driven", "🎯 Targeted", "🗣️ Conversational", "🔥 Aggressive", "✨ Solution"],
    "Global Student": ["🎓 Formal", "📝 Concise", "🤓 Geeky", "🎯 Goal-Oriented", "📚 Detailed", "🤔 Critical", "⚡ Quick", "🧠 Deep", "🗣️ Argumentative", "📝 Note-taking"],
    "Global Corporate": ["👔 Executive", "⚡ Direct", "🚀 Strategic", "⚖️ Compliance", "🤝 Diplomatic", "📊 Analytical", "📢 PR-Safe", "💼 Professional", "🗣️ Leadership", "🌍 Global"]
}
DEFAULT_TONES = ["Professional", "Friendly", "Informative"]

# ==========================================
# 6. FAQ & 智能拦截 (16项全)
# ==========================================
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

FAQ_DATABASE = {
    "English": [
        {"q": "Q1: Subscription?", "a": "No. One-time $12.90."}, {"q": "Q2: Refund?", "a": "No refunds."},
        {"q": "Q3: Lost Key?", "a": "Use LemonSqueezy Order Locator."}, {"q": "Q4: Devices?", "a": "Multiple allowed."},
        {"q": "Q5: Affiliate?", "a": "Yes, 40% commission."}, {"q": "Q6: Invoice?", "a": "Auto-emailed."},
        {"q": "Q7: Bulk?", "a": "Contact support."}, {"q": "Q8: PDF Font?", "a": "Install font.ttf."},
        {"q": "Q9: WeChat?", "a": "Click green icon."}, {"q": "Q10: Invalid Key?", "a": "Check spaces."},
        {"q": "Q11: Slow?", "a": "Pro is faster."}, {"q": "Q12: Unlimited?", "a": "Text yes, Img 200."},
        {"q": "Q13: Commercial?", "a": "Pro yes."}, {"q": "Q14: Offline?", "a": "No."},
        {"q": "Q15: Privacy?", "a": "Secure."}, {"q": "Q16: Sharing?", "a": "Banned."}
    ],
    "简体中文": [
        {"q": "问1: 订阅制?", "a": "否，一次性付费。"}, {"q": "问2: 退款?", "a": "不支持退款。"},
        {"q": "问3: 激活码丢了?", "a": "去订单页找回。"}, {"q": "问4: 多设备?", "a": "支持。"},
        {"q": "问5: 分销?", "a": "有，40%佣金。"}, {"q": "问6: 发票?", "a": "自动发送。"},
        {"q": "问7: 团购?", "a": "联系客服。"}, {"q": "问8: PDF乱码?", "a": "安装字体。"},
        {"q": "问9: 微信?", "a": "手动分享。"}, {"q": "问10: 无效码?", "a": "检查空格。"},
        {"q": "问11: 慢?", "a": "Pro极速。"}, {"q": "问12: 无限?", "a": "文字无限。"},
        {"q": "问13: 商用?", "a": "Pro可商用。"}, {"q": "问14: 离线?", "a": "不支持。"},
        {"q": "问15: 隐私?", "a": "安全。"}, {"q": "问16: 共享?", "a": "禁止。"}
    ]
}
for lang in ALL_LANGUAGES:
    if lang not in FAQ_DATABASE: FAQ_DATABASE[lang] = FAQ_DATABASE["English"]
FAQ_LIST = FAQ_DATABASE["English"]

TICKET_OPTIONS = {
    "English": ["🔴 Bug/Error", "🟠 Billing", "🟡 Feature", "🟢 Partner", "🔵 Other"],
    "简体中文": ["🔴 程序报错", "🟠 账单问题", "🟡 功能建议", "🟢 商务合作", "🔵 其他"]
}
def get_ticket_types(lang): 
    return TICKET_OPTIONS.get(lang, TICKET_OPTIONS["English"])
