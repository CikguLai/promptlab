# dm_ui.py
# Lai's Lab UI Module - FINAL COMPLETE VERSION
# Handles UI labels, buttons, and static text for 16 Languages.

# ==========================================
# UI 文本数据库 (16 Languages)
# Keys needed: 
# - title, subtitle
# - role, mode, tone, input_label
# - btn_submit, btn_copy, btn_clear
# - tab_main, tab_history, tab_upgrade, tab_help
# - tbl_head (List of 3 for Comparison Table)
# ==========================================

UI_BUNDLE = {
    "English": {
        "title": "PromptLab AI",
        "subtitle": "Professional Educational & Creative Assistant",
        "role": "Select Role", "mode": "Select Mode", "tone": "Select Tone",
        "input_label": "Enter your topic, content, or paste text here...",
        "btn_submit": "✨ Generate Content",
        "btn_copy": "📋 Copy",
        "btn_clear": "🗑️ Clear",
        "tab_main": "Generative AI",
        "tab_history": "History",
        "tab_upgrade": "Upgrade Pro",
        "tab_help": "Help & Support",
        "tbl_head": ["Feature Comparison", "Guest (Free)", "Pro (Paid)"],
        "upgrade_title": "Unlock Professional Power",
        "upgrade_btn": "Get Pro Key"
    },
    
    "简体中文": {
        "title": "PromptLab AI",
        "subtitle": "您的专业教育与创意 AI 助手",
        "role": "选择角色", "mode": "选择模式", "tone": "选择语调",
        "input_label": "请输入主题、内容或粘贴文本...",
        "btn_submit": "✨ 生成内容",
        "btn_copy": "📋 复制",
        "btn_clear": "🗑️ 清空",
        "tab_main": "AI 生成",
        "tab_history": "历史记录",
        "tab_upgrade": "升级 Pro",
        "tab_help": "帮助中心",
        "tbl_head": ["功能权益对比", "游客 (免费)", "Pro (付费)"],
        "upgrade_title": "解锁专业版功能",
        "upgrade_btn": "获取激活码"
    },

    "繁體中文": {
        "title": "PromptLab AI",
        "subtitle": "您的專業教育與創意 AI 助手",
        "role": "選擇角色", "mode": "選擇模式", "tone": "選擇語調",
        "input_label": "請輸入主題、內容或貼上文本...",
        "btn_submit": "✨ 生成內容",
        "btn_copy": "📋 複製",
        "btn_clear": "🗑️ 清空",
        "tab_main": "AI 生成",
        "tab_history": "歷史記錄",
        "tab_upgrade": "升級 Pro",
        "tab_help": "幫助中心",
        "tbl_head": ["功能權益對比", "遊客 (免費)", "Pro (付費)"],
        "upgrade_title": "解鎖專業版功能",
        "upgrade_btn": "獲取激活碼"
    },

    "Bahasa Melayu": {
        "title": "PromptLab AI",
        "subtitle": "Pembantu AI Pendidikan & Kreatif Profesional",
        "role": "Pilih Peranan", "mode": "Pilih Mod", "tone": "Nada Suara",
        "input_label": "Masukkan topik atau tampal teks di sini...",
        "btn_submit": "✨ Jana Kandungan",
        "btn_copy": "📋 Salin",
        "btn_clear": "🗑️ Padam",
        "tab_main": "AI Generatif",
        "tab_history": "Sejarah",
        "tab_upgrade": "Naik Taraf",
        "tab_help": "Bantuan",
        "tbl_head": ["Perbandingan Ciri", "Tetamu (Percuma)", "Pro (Berbayar)"],
        "upgrade_title": "Buka Kuasa Profesional",
        "upgrade_btn": "Dapatkan Kunci Pro"
    },

    "Español": {
        "title": "PromptLab AI",
        "subtitle": "Asistente AI Educativo y Creativo",
        "role": "Rol", "mode": "Modo", "tone": "Tono",
        "input_label": "Ingrese su tema o pegue texto aquí...",
        "btn_submit": "✨ Generar",
        "btn_copy": "📋 Copiar",
        "btn_clear": "🗑️ Borrar",
        "tab_main": "Generar",
        "tab_history": "Historial",
        "tab_upgrade": "Mejorar",
        "tab_help": "Ayuda",
        "tbl_head": ["Comparación", "Invitado", "Pro (Pago)"],
        "upgrade_title": "Desbloquear Pro",
        "upgrade_btn": "Obtener Clave"
    },

    "日本語": {
        "title": "PromptLab AI",
        "subtitle": "教育と創造のためのプロフェッショナルAI",
        "role": "役割選択", "mode": "モード", "tone": "口調",
        "input_label": "トピックを入力またはテキストを貼り付け...",
        "btn_submit": "✨ 生成する",
        "btn_copy": "📋 コピー",
        "btn_clear": "🗑️ 消去",
        "tab_main": "AI生成",
        "tab_history": "履歴",
        "tab_upgrade": "Proへ",
        "tab_help": "ヘルプ",
        "tbl_head": ["機能比較", "ゲスト (無料)", "Pro (有料)"],
        "upgrade_title": "Pro版を解除",
        "upgrade_btn": "キーを入手"
    },

    "한국어": {
        "title": "PromptLab AI",
        "subtitle": "교육 및 창의성을 위한 전문 AI",
        "role": "역할 선택", "mode": "모드", "tone": "어조",
        "input_label": "주제를 입력하거나 텍스트를 붙여넣으세요...",
        "btn_submit": "✨ 생성하기",
        "btn_copy": "📋 복사",
        "btn_clear": "🗑️ 지우기",
        "tab_main": "AI 생성",
        "tab_history": "기록",
        "tab_upgrade": "Pro 업그레이드",
        "tab_help": "도움말",
        "tbl_head": ["기능 비교", "게스트 (무료)", "Pro (유료)"],
        "upgrade_title": "Pro 잠금 해제",
        "upgrade_btn": "키 구매하기"
    },

    "Français": {
        "title": "PromptLab AI",
        "subtitle": "Assistant IA Éducatif et Créatif",
        "role": "Rôle", "mode": "Mode", "tone": "Ton",
        "input_label": "Entrez votre sujet ou collez du texte...",
        "btn_submit": "✨ Générer",
        "btn_copy": "📋 Copier",
        "btn_clear": "🗑️ Effacer",
        "tab_main": "Générer",
        "tab_history": "Historique",
        "tab_upgrade": "Upgrade",
        "tab_help": "Aide",
        "tbl_head": ["Comparaison", "Invité (Gratuit)", "Pro (Payant)"],
        "upgrade_title": "Débloquer Pro",
        "upgrade_btn": "Obtenir Clé"
    },

    "Deutsch": {
        "title": "PromptLab AI",
        "subtitle": "Ihr KI-Assistent für Bildung & Kreativität",
        "role": "Rolle", "mode": "Modus", "tone": "Tonfall",
        "input_label": "Thema eingeben oder Text einfügen...",
        "btn_submit": "✨ Generieren",
        "btn_copy": "📋 Kopieren",
        "btn_clear": "🗑️ Löschen",
        "tab_main": "Generieren",
        "tab_history": "Verlauf",
        "tab_upgrade": "Upgrade",
        "tab_help": "Hilfe",
        "tbl_head": ["Vergleich", "Gast (Gratis)", "Pro (Bezahlt)"],
        "upgrade_title": "Pro Freischalten",
        "upgrade_btn": "Key Kaufen"
    },

    "Italiano": {
        "title": "PromptLab AI",
        "subtitle": "Assistente AI Educativo e Creativo",
        "role": "Ruolo", "mode": "Modalità", "tone": "Tono",
        "input_label": "Inserisci argomento o incolla testo...",
        "btn_submit": "✨ Genera",
        "btn_copy": "📋 Copia",
        "btn_clear": "🗑️ Cancella",
        "tab_main": "Genera",
        "tab_history": "Cronologia",
        "tab_upgrade": "Upgrade",
        "tab_help": "Aiuto",
        "tbl_head": ["Confronto", "Ospite", "Pro"],
        "upgrade_title": "Sblocca Pro",
        "upgrade_btn": "Ottieni Chiave"
    },

    "Português": {
        "title": "PromptLab AI",
        "subtitle": "Assistente de IA Educacional e Criativo",
        "role": "Papel", "mode": "Modo", "tone": "Tom",
        "input_label": "Insira o tópico ou cole o texto...",
        "btn_submit": "✨ Gerar",
        "btn_copy": "📋 Copiar",
        "btn_clear": "🗑️ Limpar",
        "tab_main": "Gerar",
        "tab_history": "Histórico",
        "tab_upgrade": "Upgrade",
        "tab_help": "Ajuda",
        "tbl_head": ["Comparação", "Convidado", "Pro"],
        "upgrade_title": "Desbloquear Pro",
        "upgrade_btn": "Obter Chave"
    },

    "Русский": {
        "title": "PromptLab AI",
        "subtitle": "Ваш ИИ-помощник в образовании",
        "role": "Роль", "mode": "Режим", "tone": "Тон",
        "input_label": "Введите тему или вставьте текст...",
        "btn_submit": "✨ Создать",
        "btn_copy": "📋 Копия",
        "btn_clear": "🗑️ Сброс",
        "tab_main": "Генерация",
        "tab_history": "История",
        "tab_upgrade": "Pro Версия",
        "tab_help": "Помощь",
        "tbl_head": ["Сравнение", "Гость (0₽)", "Pro (Платный)"],
        "upgrade_title": "Открыть Pro",
        "upgrade_btn": "Купить Ключ"
    },

    "Arabic": {
        "title": "PromptLab AI",
        "subtitle": "مساعدك الذكي للتعليم والإبداع",
        "role": "الدور", "mode": "الوضع", "tone": "النبرة",
        "input_label": "أدخل الموضوع أو الصق النص هنا...",
        "btn_submit": "✨ توليد",
        "btn_copy": "📋 نسخ",
        "btn_clear": "🗑️ مسح",
        "tab_main": "الذكاء الاصطناعي",
        "tab_history": "السجل",
        "tab_upgrade": "ترقية",
        "tab_help": "مساعدة",
        "tbl_head": ["مقارنة الميزات", "زائر (مجاني)", "Pro (مدفوع)"],
        "upgrade_title": "فتح الميزات الاحترافية",
        "upgrade_btn": "احصل على المفتاح"
    },

    "Hindi": {
        "title": "PromptLab AI",
        "subtitle": "आपका शैक्षिक और रचनात्मक एआई सहायक",
        "role": "भूमिका", "mode": "मोड", "tone": "लहज़ा",
        "input_label": "अपना विषय दर्ज करें या टेक्स्ट पेस्ट करें...",
        "btn_submit": "✨ उत्पन्न करें",
        "btn_copy": "📋 कॉपी",
        "btn_clear": "🗑️ साफ़ करें",
        "tab_main": "एआई जनरेट",
        "tab_history": "इतिहास",
        "tab_upgrade": "Pro अपग्रेड",
        "tab_help": "सहायता",
        "tbl_head": ["सुविधा तुलना", "अतिथि (मुफ़्त)", "Pro (भुगतान)"],
        "upgrade_title": "Pro अनलॉक करें",
        "upgrade_btn": "कुंजी प्राप्त करें"
    },

    "Thai": {
        "title": "PromptLab AI",
        "subtitle": "ผู้ช่วย AI ด้านการศึกษาและความคิดสร้างสรรค์",
        "role": "บทบาท", "mode": "โหมด", "tone": "น้ำเสียง",
        "input_label": "ป้อนหัวข้อหรือวางข้อความที่นี่...",
        "btn_submit": "✨ สร้างเนื้อหา",
        "btn_copy": "📋 คัดลอก",
        "btn_clear": "🗑️ ล้าง",
        "tab_main": "สร้าง AI",
        "tab_history": "ประวัติ",
        "tab_upgrade": "อัปเกรด Pro",
        "tab_help": "ช่วยเหลือ",
        "tbl_head": ["เปรียบเทียบ", "ผู้เยี่ยมชม (ฟรี)", "Pro (จ่ายเงิน)"],
        "upgrade_title": "ปลดล็อก Pro",
        "upgrade_btn": "รับคีย์"
    },

    "Vietnamese": {
        "title": "PromptLab AI",
        "subtitle": "Trợ lý AI Giáo dục & Sáng tạo Chuyên nghiệp",
        "role": "Vai trò", "mode": "Chế độ", "tone": "Giọng văn",
        "input_label": "Nhập chủ đề hoặc dán văn bản vào đây...",
        "btn_submit": "✨ Tạo nội dung",
        "btn_copy": "📋 Sao chép",
        "btn_clear": "🗑️ Xóa",
        "tab_main": "Tạo AI",
        "tab_history": "Lịch sử",
        "tab_upgrade": "Nâng cấp Pro",
        "tab_help": "Hỗ trợ",
        "tbl_head": ["So sánh tính năng", "Khách (Miễn phí)", "Pro (Trả phí)"],
        "upgrade_title": "Mở khóa Pro",
        "upgrade_btn": "Mua Key"
    }
}

# ==========================================
# 核心函数: 获取UI字典 (Core Function)
# ==========================================
def get_safe_ui(lang):
    """
    Returns the UI dictionary for the specified language.
    Falls back to 'English' if the language is not found.
    """
    return UI_BUNDLE.get(lang, UI_BUNDLE["English"])