# dm_ui.py
# Lai's Lab UI Module - COMMERCIAL V9.33
# Features: 30+ UI Keys per language to prevent crashes.

UI_BUNDLE = {
    "English": {
        "sidebar_title": "Lai's Lab AI",
        "plan_guest": "Guest Plan", "plan_pro": "Pro Plan",
        "usage": "Daily Usage", "lang": "Interface Language",
        "role": "Select Persona", "faq_title": "Support & FAQ",
        "quick_ans": "Quick Answers", "sel_topic": "Select Topic",
        "submit_ticket": "Submit Ticket", "type_lbl": "Ticket Type",
        "issue_lbl": "Describe issue or press Enter to search...",
        "send_btn": "Submit Ticket", "logout": "Reset / Logout",
        "mode": "Select Mode", "action": "Select Action",
        "out_lang_lbl": "Output Language", "tone_lbl": "Tone of Voice",
        "input_label": "Enter your topic, content, or keywords here...",
        "generate": "✨ Generate Content",
        "lock_msg": "This is a Pro Feature. Please upgrade to access.",
        "buy_btn": "👉 Upgrade to Pro Now",
        "result": "Generated Result",
        "ad_copy": "1. Copy Result", 
        "ad_connect": "2. Refine in AI Tools",
        "ad_social": "3. Share to Social",
        "ad_manual": "4. Manual Post",
        "ad_download": "5. Save Files",
        "ad_locked": "Pro Only",
        "tbl_head": ["Feature Comparison", "Guest (Free)", "Pro (Paid)"]
    },
    
    "简体中文": {
        "sidebar_title": "Lai's Lab AI",
        "plan_guest": "游客版", "plan_pro": "专业版",
        "usage": "今日用量", "lang": "界面语言",
        "role": "选择角色", "faq_title": "帮助与支持",
        "quick_ans": "快速问答", "sel_topic": "选择话题",
        "submit_ticket": "提交工单", "type_lbl": "工单类型",
        "issue_lbl": "描述问题或回车搜索答案...",
        "send_btn": "提交工单", "logout": "重置 / 登出",
        "mode": "选择模式", "action": "选择具体任务",
        "out_lang_lbl": "输出语言", "tone_lbl": "语气语调",
        "input_label": "在此输入主题、内容或关键词...",
        "generate": "✨ 立即生成",
        "lock_msg": "这是 Pro 专业版功能，请升级解锁。",
        "buy_btn": "👉 立即升级 Pro",
        "result": "生成结果",
        "ad_copy": "1. 一键复制", 
        "ad_connect": "2. AI 工具精修",
        "ad_social": "3. 社交分享",
        "ad_manual": "4. 手动发布",
        "ad_download": "5. 保存文件",
        "ad_locked": "仅限 Pro",
        "tbl_head": ["功能权益对比", "游客 (免费)", "Pro (付费)"]
    },

    "繁體中文": {
        "sidebar_title": "Lai's Lab AI",
        "plan_guest": "遊客版", "plan_pro": "專業版",
        "usage": "今日用量", "lang": "介面語言",
        "role": "選擇角色", "faq_title": "幫助與支援",
        "quick_ans": "快速問答", "sel_topic": "選擇話題",
        "submit_ticket": "提交工單", "type_lbl": "工單類型",
        "issue_lbl": "描述問題或按 Enter 搜尋...",
        "send_btn": "提交工單", "logout": "重置 / 登出",
        "mode": "選擇模式", "action": "選擇具體任務",
        "out_lang_lbl": "輸出語言", "tone_lbl": "語氣語調",
        "input_label": "在此輸入主題、內容或關鍵詞...",
        "generate": "✨ 立即生成",
        "lock_msg": "這是 Pro 專業版功能，請升級解鎖。",
        "buy_btn": "👉 立即升級 Pro",
        "result": "生成結果",
        "ad_copy": "1. 一鍵複製", 
        "ad_connect": "2. AI 工具精修",
        "ad_social": "3. 社交分享",
        "ad_manual": "4. 手動發佈",
        "ad_download": "5. 保存檔案",
        "ad_locked": "僅限 Pro",
        "tbl_head": ["功能權益對比", "遊客 (免費)", "Pro (付費)"]
    },

    "Bahasa Melayu": {
        "sidebar_title": "Lai's Lab AI",
        "plan_guest": "Pelan Tetamu", "plan_pro": "Pelan Pro",
        "usage": "Penggunaan", "lang": "Bahasa Antaramuka",
        "role": "Pilih Peranan", "faq_title": "Bantuan & Sokongan",
        "quick_ans": "Jawapan Pantas", "sel_topic": "Pilih Topik",
        "submit_ticket": "Hantar Tiket", "type_lbl": "Jenis Tiket",
        "issue_lbl": "Terangkan isu atau tekan Enter...",
        "send_btn": "Hantar", "logout": "Set Semula",
        "mode": "Pilih Mod", "action": "Pilih Tindakan",
        "out_lang_lbl": "Bahasa Output", "tone_lbl": "Nada Suara",
        "input_label": "Masukkan topik atau kandungan di sini...",
        "generate": "✨ Jana Kandungan",
        "lock_msg": "Ini ciri Pro. Sila naik taraf.",
        "buy_btn": "👉 Dapatkan Pro",
        "result": "Hasil",
        "ad_copy": "1. Salin", 
        "ad_connect": "2. Alat AI",
        "ad_social": "3. Kongsi Sosial",
        "ad_manual": "4. Manual",
        "ad_download": "5. Simpan Fail",
        "ad_locked": "Pro Sahaja",
        "tbl_head": ["Perbandingan Ciri", "Tetamu (Percuma)", "Pro (Berbayar)"]
    }
}

# 辅助函数：防止其他 12 种语言报错，自动回退到英文
def get_safe_ui(lang):
    base = UI_BUNDLE.get("English").copy() # 复制一份英文作为底版
    target = UI_BUNDLE.get(lang, {}) # 获取目标语言（如果只有部分翻译）
    base.update(target) # 用目标语言覆盖底版
    return base
