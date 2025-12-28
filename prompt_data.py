# prompt_data.py
# ==========================================
# PromptLab AI V7.3 Ultimate Edition
# 核心数据仓库 (Data Warehouse)
# 包含: 语言包, FAQ, 角色模式定义, 下拉选项
# ==========================================

# 1. 多语言界面字典 (15国语言 + 免费版逻辑)
# ------------------------------------------
LANG_DICT = {
    "English": {
        "login_guest": "Start Free Trial", "login_pro": "Activate PRO License",
        "email": "Email Address", "key": "License Key", "submit": "Login / Activate",
        "role_title": "Choose Your Workspace", "back_home": "Back to Home",
        "welcome": "Welcome", "engine": "Engine", "logout": "Logout",
        "mode_sel": "Select Mode", "opt_sel": "Select Option", "upload": "Upload Context",
        "batch_true": "✅ Batch Mode: 50 Images", "batch_false": "🔒 Limit: 1 Image (PRO: 50)",
        "generate": "✨ Generate Prompt", "wait": "Analyzing...", "done": "Generation Complete",
        "copy": "Copy Result", "connect": "🚀 AI Direct Connect", "download": "Download",
        "limit_reach": "Daily Limit Reached", "upgrade_txt": "Upgrade for Unlimited",
        "sticky_ad_title": "🔥 Limited Deal", "sticky_ad_btn": "👉 Get It Now",
        "ticket_title": "🎫 Support Ticket", "ticket_sub": "Subject", "ticket_msg": "Message",
        "ticket_btn_guest": "Submit (Queue)", "ticket_btn_pro": "Submit (Priority)"
    },
    "简体中文": {
        "login_guest": "开始免费试用", "login_pro": "激活 PRO 会员",
        "email": "电子邮箱", "key": "激活码 (License Key)", "submit": "登录 / 激活",
        "role_title": "选择您的工作区", "back_home": "返回首页",
        "welcome": "欢迎", "engine": "引擎状态", "logout": "退出登录",
        "mode_sel": "选择模式", "opt_sel": "具体选项", "upload": "上传参考资料",
        "batch_true": "✅ 批量模式: 支持 50 张", "batch_false": "🔒 限制: 1 张 (PRO: 50张)",
        "generate": "✨ 生成提示词", "wait": "正在分析...", "done": "生成完成",
        "copy": "复制结果", "connect": "🚀 AI 直通车", "download": "下载存档",
        "limit_reach": "今日额度已用完", "upgrade_txt": "升级解锁无限额度",
        "sticky_ad_title": "🔥 限时特惠", "sticky_ad_btn": "👉 立即抢购",
        "ticket_title": "🎫 智能工单", "ticket_sub": "主题", "ticket_msg": "问题描述",
        "ticket_btn_guest": "提交 (排队中)", "ticket_btn_pro": "提交 (优先处理)"
    },
    "Español": {
        "login_guest": "Prueba Gratis", "login_pro": "Activar Licencia PRO",
        "email": "Correo", "key": "Clave de Licencia", "submit": "Entrar / Activar",
        "role_title": "Elige tu Espacio", "back_home": "Volver",
        "welcome": "Hola", "engine": "Motor", "logout": "Salir",
        "mode_sel": "Modo", "opt_sel": "Opción", "upload": "Subir Contexto",
        "batch_true": "✅ Modo Lote: 50 imgs", "batch_false": "🔒 Límite: 1 img (PRO: 50)",
        "generate": "✨ Generar Prompt", "wait": "Analizando...", "done": "Completado",
        "copy": "Copiar", "connect": "🚀 Conexión AI", "download": "Descargar",
        "limit_reach": "Límite Diario", "upgrade_txt": "Actualizar a Ilimitado",
        "sticky_ad_title": "🔥 Oferta Limitada", "sticky_ad_btn": "👉 Comprar Ahora",
        "ticket_title": "🎫 Soporte", "ticket_sub": "Asunto", "ticket_msg": "Mensaje",
        "ticket_btn_guest": "Enviar (Cola)", "ticket_btn_pro": "Enviar (Prioridad)"
    },
    # PRO Languages (Simplified mapping for UI elements fallback to English/Symbolic)
    "Bahasa Melayu": {"generate": "✨ Jana Prompt", "mode_sel": "Pilih Mod", "copy": "Salin"},
    "Russian": {"generate": "✨ Создать", "mode_sel": "Режим", "copy": "Копировать"},
    "Japanese": {"generate": "✨ 作成する", "mode_sel": "モード", "copy": "コピー"},
    "Korean": {"generate": "✨ 생성하다", "mode_sel": "모드", "copy": "복사"},
    "French": {"generate": "✨ Générer", "mode_sel": "Mode", "copy": "Copier"},
    "German": {"generate": "✨ Generieren", "mode_sel": "Modus", "copy": "Kopieren"},
    "Indonesian": {"generate": "✨ Buat Prompt", "mode_sel": "Mode", "copy": "Salin"},
    "Thai": {"generate": "✨ สร้าง", "mode_sel": "โหมด", "copy": "คัดลอก"},
    "Vietnamese": {"generate": "✨ Tạo Prompt", "mode_sel": "Chế độ", "copy": "Sao chép"},
    "Arabic": {"generate": "✨ إنشاء", "mode_sel": "الوضع", "copy": "نسخ"},
    "Tamil": {"generate": "✨ உருவாக்கு", "mode_sel": "முறை", "copy": "நகல்"},
    "Portuguese": {"generate": "✨ Gerar", "mode_sel": "Modo", "copy": "Copiar"},
    "Italian": {"generate": "✨ Generare", "mode_sel": "Modo", "copy": "Copia"},
    "Hindi": {"generate": "✨ उत्पन्न करें", "mode_sel": "मोड", "copy": "कॉपी करें"},
    "Filipino": {"generate": "✨ Bumuo", "mode_sel": "Mode", "copy": "Kopyahin"}
}

# 2. 完整 FAQ 知识库 (16条)
# ------------------------------------------
FAQ_DB = {
    "💰 Purchase & Billing": [
        ("Is this a subscription?", "No. It is a One-Time Payment of $12.90. No monthly fees."),
        ("What is the Refund Policy?", "Strictly No Refunds. This is a digital product (License Key) with instant access."),
        ("Will future updates be free?", "Yes! The Lifetime Deal includes access to V6.0 and future standard updates."),
        ("I lost my License Key.", "Please check your email from LemonSqueezy or visit the LemonSqueezy Order Locator."),
        ("Can I ask for an Invoice?", "Yes. You can download an official invoice directly from the LemonSqueezy order confirmation email.")
    ],
    "🔑 Account & Activation": [
        ("Invalid Key error?", "Ensure no spaces are copied. Check if you are using the correct email."),
        ("Can I use on multiple devices?", "Yes. Your license is tied to your email, accessible on mobile/desktop."),
        ("Still showing Free Guest?", "Please click 'Logout' at the bottom sidebar, then login again with your PRO Key.")
    ],
    "🛠️ Technical Support": [
        ("PDF Text is missing/boxes?", "This is a known issue with system fonts. Please submit a Ticket so we can fix it."),
        ("Output Language Issue?", "Ensure the 'Output Language' dropdown in the workspace is set to your target language."),
        ("WeChat button not working?", "Click the green icon -> Select 'WeChat' from your phone's system share menu."),
        ("Is my data private?", "Yes. We do not store your prompt inputs. Your data is processed securely via encrypted API.")
    ],
    "⚡ Limits & Usage": [
        ("Is PRO truly Unlimited?", "Yes for text. For images, we have a fair usage policy of ~200/day to prevent abuse."),
        ("Can I use content commercially?", "Yes, PRO users have 100% commercial rights."),
        ("Do you have an Affiliate Program?", "Yes! Join our affiliate program to earn 30% commission on every sale. Contact us to apply."),
        ("Is there a Team License?", "Currently we focus on individual licenses. For bulk orders (10+), please contact support.")
    ]
}

# 3. 完整角色与模式数据 (6 Roles, 18 Modes, 144+ Options)
# ------------------------------------------
# 结构: Role -> Mode -> {options: [], placeholder: ""}
ROLES_DB = {
    "Global Educator": {
        "Pedagogy": {
            "options": ["Analyze Student Work (Image)", "Direct Instruction", "Gamification", "Project-Based Learning", "Socratic Method", "Flipped Classroom", "Differentiated Instruction", "Inquiry-Based Learning", "Cooperative Learning", "Montessori Method", "Waldorf Approach", "Reggio Emilia", "Bloom's Taxonomy", "Constructivism", "Scaffolding"],
            "placeholder": "Enter Topic (e.g., Photosynthesis, Grade 5)..."
        },
        "Visuals": {
            "options": ["Pixar/Disney 3D", "National Geographic", "Minimalist Vector", "Vintage Watercolor", "Scientific Schematic", "Cyberpunk Concept", "Ukiyo-e Style", "Oil Painting", "Line Art", "Infographic Style", "Claymation", "Paper Cutout", "Anime Style", "Isometric View", "Blackboard Sketch"],
            "placeholder": "Describe the educational visual you need..."
        },
        "Comm": {
            "options": ["Parent Message", "Behavior Report", "Official Proposal", "Classroom Newsletter", "Event Invitation", "Grant Application", "Syllabus Design", "Rubric Generator", "IEP Draft", "Recommendation Letter", "Field Trip Notice", "Volunteer Request", "Policy Update"],
            "placeholder": "Enter details (e.g., Student name, Incident, Date)..."
        }
    },
    "Global Creator": {
        "Scripting": {
            "options": ["Visual-to-Script (Image)", "TikTok/Reels (Hook-Value-CTA)", "YouTube Edutainment", "Storytelling Vlog", "Podcast Interview", "Live Stream Flow", "ASMR Script", "Unboxing Flow", "Tutorial Step-by-Step", "Comedy Skit", "Motivational Speech", "News Commentary", "Reaction Video"],
            "placeholder": "Enter Video Topic (e.g., 3 Life Hacks for Cables)..."
        },
        "Thumbnail": {
            "options": ["High CTR (Shocked Face)", "Cinematic Poster", "Tech/Neon/Glowing", "Before & After", "Minimalist Apple Style", "Comic Book Style", "Bokeh Portrait", "Split Screen", "Text-Heavy Overlay", "Glitch Effect", "Retro 80s", "Horror/Dark", "Dreamy Pastel", "3D Render Object"],
            "placeholder": "Describe video content for thumbnail..."
        },
        "Marketing": {
            "options": ["Xiaohongshu (KOC)", "Instagram Caption", "Facebook Ad", "LinkedIn Leader", "Twitter Thread", "Email Newsletter", "Bio Optimization", "Hashtag Generator", "Community Post", "Discord Announcement", "Pinterest Pin Description", "SEO Blog Title"],
            "placeholder": "Enter Product/Topic to market..."
        }
    },
    "Global Parent": {
        "Story Time": {
            "options": ["From Drawing (Image)", "Bedtime Story", "Hero's Journey", "Social Emotional", "Science 'Why'", "Cultural Tale", "Fable (Moral)", "Adventure Series", "Personalized Name Story", "History Time Travel", "Nature Mystery", "Space Exploration", "Animal Kingdom"],
            "placeholder": "Enter Child's Name, Age, Interests..."
        },
        "Activities": {
            "options": ["DIY Craft Guide", "Rainy Day Game", "Kitchen Science", "Scavenger Hunt", "Family Bonding", "No-Screen Coding", "Origami Steps", "Gardening Guide", "Music Game", "Sensory Play", "Road Trip Games", "Party Planner", "Holiday Decoration"],
            "placeholder": "Enter available materials or setting..."
        },
        "Tutor": {
            "options": ["Solve Problem (Image)", "Feynman Technique", "Homework Helper", "Quiz Generator", "Vocabulary Builder", "Essay Proofreader", "Math Word Problem", "Science Concept", "History Timeline", "Geography Facts", "Language Practice", "Reading Comprehension"],
            "placeholder": "Enter the question or concept to explain..."
        }
    },
    "Global Seller": {
        "Copywriting": {
            "options": ["Product Desc (Image)", "PAS (Pain-Agitate-Solution)", "AIDA (Attention-Interest-Desire-Action)", "FAB (Features-Advantages-Benefits)", "Storytelling Sales", "Objection Handling", "USP Highlighter", "FOMO Generator", "Value Proposition", "Brand Story", "Landing Page Copy", "Slogan Generator"],
            "placeholder": "Enter Product Name & Key Features..."
        },
        "Product Shot": {
            "options": ["Studio White BG", "Lifestyle Home", "Luxury Gold/Black", "Nature/Sunlight", "Cyberpunk/Tech", "Flat Lay", "Model Wearing", "Macro Detail", "Water Splash", "Podium Display", "Knolling (Organized)", "Pastel Background", "Neon Edge"],
            "placeholder": "Describe your product..."
        },
        "Support": {
            "options": ["Apology & Recovery", "Review Request", "Complaint Reply", "Promo Announcement", "Crisis Statement", "FAQ Gen", "Refund Policy", "Shipping Update", "Welcome Email", "VIP Invitation", "Survey Request", "Cross-sell Script"],
            "placeholder": "Enter Customer Issue or Event details..."
        }
    },
    "Global Student": {
        "Study": {
            "options": ["Explain Chart (Image)", "Feynman Technique", "Lit Review Matrix", "Flashcard (Anki)", "Concept Simplifier", "Translation", "Summarizer", "Mind Map Text", "Mnemonic Generator", "Note-Taking (Cornell)", "Exam Planner"],
            "placeholder": "Enter Topic or paste text to study..."
        },
        "Project": {
            "options": ["Essay Outline", "Presentation Script", "Debate Prep", "Lab Report", "Methodology", "Group Roles", "Gantt Chart Text", "Research Question", "Hypothesis Gen", "Bibliography Format", "Abstract Writer"],
            "placeholder": "Enter Project Topic..."
        },
        "Career": {
            "options": ["ATS Resume", "Cover Letter", "Interview Prep", "LinkedIn Bio", "Cold Email", "Portfolio Desc", "Networking Message", "Salary Negotiation", "Resignation Letter", "Personal Statement", "Reference Request"],
            "placeholder": "Enter Job Role & Your Experience..."
        }
    },
    "Global Corporate": {
        "Admin": {
            "options": ["Extract Data (Image)", "Meeting Minutes", "Official Proposal", "Internal Memo", "SOP / Process", "Press Release", "Agenda Setter", "Policy Drafting", "Executive Summary", "Report Formatting", "Email Etiquette Polish"],
            "placeholder": "Enter meeting notes or policy details..."
        },
        "Strategy": {
            "options": ["OKRs", "SWOT Analysis", "Competitor Dive", "Business Canvas", "Risk Matrix", "Pitch Deck", "PESTLE Analysis", "Value Chain", "Blue Ocean Strategy", "Growth Hacking Plan", "Vision/Mission Statement"],
            "placeholder": "Enter Company Name & Goal..."
        },
        "HR & Team": {
            "options": ["Performance Review", "Job Desc (JD)", "Onboarding Plan", "Crisis Comms", "Team Building", "Termination Script", "Offer Letter", "Employee Survey", "Culture Handbook", "Training Module Outline", "Conflict Resolution"],
            "placeholder": "Enter Employee details or Situation..."
        }
    }
}