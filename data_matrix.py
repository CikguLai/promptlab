# data_matrix.py
# Lai's Lab V9.0 - 核心数据库
# 包含：角色/模式/选项配置、Prompt 模板、FAQ 知识库、多语言字典

# ==========================================
# 1. 角色与模式矩阵 (The 6x3 Matrix)
# ==========================================
# 结构: Role -> Mode -> Options (List of dicts)
# 每个 Option 包含: label (显示名), prompt_template (给 AI 的指令)

ROLES_CONFIG = {
    "Global Educator": {
        "Pedagogy (Free)": [
            {"label": "1. Rubric Creator (评分标准)", "template": "Create a detailed grading rubric for: {input}. Include columns for Criteria, Excellent, Good, and Needs Improvement."},
            {"label": "2. Direct Instruction", "template": "Design a Direct Instruction lesson plan for: {input}. Include Objective, Input, Modeling, and Independent Practice."},
            {"label": "3. Gamification", "template": "Create a gamification strategy to teach: {input}. Include game mechanics, rewards, and learning objectives."},
            {"label": "4. Project-Based Learning", "template": "Design a PBL project for: {input}. Include Driving Question, Project Milestones, and Final Public Product."},
            {"label": "5. Socratic Method", "template": "Generate a list of deep, open-ended Socratic questions to guide discussion on: {input}."},
            {"label": "6. Flipped Classroom", "template": "Plan a Flipped Classroom module for: {input}. List pre-class videos/readings and in-class active learning activities."},
            {"label": "7. Custom (自定义)", "template": "Act as an expert educator. {input}"}
        ],
        "Visuals (Pro)": [
            {"label": "1. Pixar/Disney 3D", "template": "Write a Midjourney prompt for a Pixar-style 3D animation scene: {input}. Include lighting, mood, and render details."},
            {"label": "2. National Geographic", "template": "Write a Midjourney prompt for a National Geographic style photograph: {input}. Specific camera settings and lighting."},
            {"label": "3. Minimalist Vector", "template": "Write a prompt for a flat, minimalist vector illustration: {input}. Use clean lines and specific color palette."},
            {"label": "4. Vintage Watercolor", "template": "Write a prompt for a vintage watercolor painting: {input}. Soft edges, paper texture, nostalgic mood."},
            {"label": "5. Scientific Schematic", "template": "Write a prompt for a detailed scientific schematic diagram: {input}. Cross-section, labels, clean white background."},
            {"label": "6. Cyberpunk Concept", "template": "Write a prompt for a futuristic Cyberpunk concept art: {input}. Neon lights, high tech, low life, rain."},
            {"label": "7. Custom (自定义)", "template": "Write a detailed AI image generation prompt for: {input}."}
        ],
        "Comm (Pro)": [
            {"label": "1. Parent Message", "template": "Draft a professional yet warm message to a parent regarding: {input}. Use the sandwich method (Positive-Negative-Positive)."},
            {"label": "2. Behavior Report", "template": "Write a formal student behavior report about: {input}. Be objective, factual, and constructive."},
            {"label": "3. Official Proposal", "template": "Write a formal proposal for school administration regarding: {input}. Include Budget, Rationale, and Expected Outcomes."},
            {"label": "4. Classroom Newsletter", "template": "Draft a monthly classroom newsletter section about: {input}. Keep it engaging and informative."},
            {"label": "5. Event Invitation", "template": "Write an invitation for parents/community for: {input}. Include Who, What, Where, When, Why."},
            {"label": "6. Grant Application", "template": "Draft a grant application narrative for: {input}. Focus on impact, innovation, and sustainability."},
            {"label": "7. Custom (自定义)", "template": "Draft a professional communication document regarding: {input}."}
        ]
    },
    "Global Creator": {
        "Scripting (Free)": [
            {"label": "1. Viral Hook Generator", "template": "Generate 10 viral video hooks (first 3 seconds) for a video about: {input}. Make them curiosity-inducing."},
            {"label": "2. TikTok/Reels Script", "template": "Write a 60-second short video script for: {input}. Structure: Hook, Value, Call to Action."},
            {"label": "3. YouTube Edutainment", "template": "Outline a YouTube Edutainment video script for: {input}. Balance education and entertainment."},
            {"label": "4. Storytelling Vlog", "template": "Write a voiceover script for a storytelling vlog about: {input}. Use the Hero's Journey structure."},
            {"label": "5. Podcast Interview", "template": "Generate an interview outline and question list for a podcast about: {input}."},
            {"label": "6. Live Stream Flow", "template": "Design a 1-hour live stream run-of-show for: {input}. Include warm-up, value delivery, and sales pitch."},
            {"label": "7. Custom (自定义)", "template": "Write a creative script for: {input}."}
        ],
        "Thumbnail (Pro)": [
            {"label": "1. High CTR (Shocked)", "template": "Write a prompt for a YouTube thumbnail with high CTR: {input}. Exaggerated facial expression, bright colors."},
            {"label": "2. Cinematic Poster", "template": "Write a prompt for a movie poster style thumbnail: {input}. Dramatic lighting, title placement."},
            {"label": "3. Tech/Neon/Glowing", "template": "Write a prompt for a tech review thumbnail: {input}. Glowing products, neon background, futuristic."},
            {"label": "4. Before & After", "template": "Write a prompt for a split-screen 'Before and After' comparison thumbnail: {input}."},
            {"label": "5. Minimalist Apple", "template": "Write a prompt for a clean, Apple-style minimalist thumbnail: {input}. White space, focus on subject."},
            {"label": "6. Comic Book Style", "template": "Write a prompt for a comic book style thumbnail: {input}. Bold outlines, action lines, speech bubbles."},
            {"label": "7. Custom (自定义)", "template": "Write a thumbnail generation prompt for: {input}."}
        ],
        "Marketing (Pro)": [
            {"label": "1. Xiaohongshu (KOC)", "template": "Write a Xiaohongshu (Little Red Book) style post about: {input}. Use many emojis, tags, and a friendly 'sister' tone."},
            {"label": "2. Instagram Caption", "template": "Write an engaging Instagram caption for: {input}. Include relevant hashtags and a question for engagement."},
            {"label": "3. Facebook Ad", "template": "Write a direct response Facebook Ad copy for: {input}. Focus on pain points and solution."},
            {"label": "4. LinkedIn Leader", "template": "Write a professional LinkedIn thought leadership post about: {input}. Use short paragraphs and professional tone."},
            {"label": "5. Twitter Thread", "template": "Write a viral Twitter thread (5-7 tweets) about: {input}. Make the first tweet a strong hook."},
            {"label": "6. Email Newsletter", "template": "Write an email newsletter segment about: {input}. Subject line, body, and click-to-action."},
            {"label": "7. Custom (自定义)", "template": "Write marketing copy for: {input}."}
        ]
    },
    "Global Parent": {
        "Story Time (Free)": [
            {"label": "1. 'My Day' Magic", "template": "Turn this daily event into a magical story for a child: {input}. Keep it safe and wondering."},
            {"label": "2. Bedtime Story", "template": "Write a calming bedtime story about: {input}. Ensure a happy ending and relaxing tone."},
            {"label": "3. Hero's Journey", "template": "Write a story where the child is the hero overcoming: {input}. Use the Hero's Journey structure."},
            {"label": "4. Social Emotional", "template": "Write a story that teaches a lesson about: {input}. Focus on feelings and empathy."},
            {"label": "5. Science 'Why'", "template": "Explain the scientific concept of '{input}' through a fun story for kids."},
            {"label": "6. Cultural Tale", "template": "Retell or create a story related to the culture/festival: {input}."},
            {"label": "7. Custom (自定义)", "template": "Write a story for a child about: {input}."}
        ],
        "Activities (Pro)": [
            {"label": "1. DIY Craft Guide", "template": "Create a step-by-step DIY craft guide using materials: {input}. Safe for kids."},
            {"label": "2. Rainy Day Game", "template": "Suggest a fun indoor game for kids involving: {input}. High energy or low energy."},
            {"label": "3. Kitchen Science", "template": "Design a safe kitchen science experiment using: {input}. Explain the science behind it."},
            {"label": "4. Scavenger Hunt", "template": "Create a scavenger hunt list for the location/theme: {input}."},
            {"label": "5. Family Bonding", "template": "Suggest a family bonding activity plan for: {input}. No screens allowed."},
            {"label": "6. No-Screen Coding", "template": "Design a logic/coding game that requires no computer, teaching: {input}."},
            {"label": "7. Custom (自定义)", "template": "Suggest a parenting activity for: {input}."}
        ],
        "Tutor (Pro)": [
            {"label": "1. Mnemonic Generator", "template": "Create a catchy mnemonic or song to help memorize: {input}."},
            {"label": "2. Feynman Technique", "template": "Explain the concept '{input}' in simple terms as if to a 5-year-old (Feynman Technique)."},
            {"label": "3. Homework Helper", "template": "Provide a step-by-step guide to solve this type of problem (do not give the answer directly): {input}."},
            {"label": "4. Quiz Generator", "template": "Generate 5 practice quiz questions (with answers at the bottom) for the topic: {input}."},
            {"label": "5. Vocabulary Builder", "template": "Explain the word '{input}'. Provide definition, synonyms, antonyms, and 3 example sentences."},
            {"label": "6. Essay Proofreader", "template": "Proofread and suggest improvements for this student essay text: {input}. Focus on grammar and flow."},
            {"label": "7. Custom (自定义)", "template": "Act as a private tutor. Help with: {input}."}
        ]
    },
    "Global Seller": {
        "Copywriting (Free)": [
            {"label": "1. Landing Page Structure", "template": "Outline a high-converting landing page structure for: {input}. Include Headline, Subhead, Benefits, Social Proof, CTA."},
            {"label": "2. PAS Model", "template": "Write sales copy using the Problem-Agitation-Solution (PAS) framework for: {input}."},
            {"label": "3. AIDA Model", "template": "Write sales copy using the Attention-Interest-Desire-Action (AIDA) framework for: {input}."},
            {"label": "4. FAB Model", "template": "Analyze the Features, Advantages, and Benefits (FAB) for the product: {input}."},
            {"label": "5. Storytelling Sales", "template": "Write a brand story or sales narrative for: {input}. Connect emotionally with the customer."},
            {"label": "6. Objection Handling", "template": "Generate persuasive responses to the customer objection: {input}."},
            {"label": "7. Custom (自定义)", "template": "Write sales copy for: {input}."}
        ],
        "Product Shot (Pro)": [
            {"label": "1. Studio White BG", "template": "Write a Midjourney prompt for a high-end product shot on clean white background: {input}. Studio lighting."},
            {"label": "2. Lifestyle Home", "template": "Write a prompt for a lifestyle product photography shot in a cozy home setting: {input}."},
            {"label": "3. Luxury Gold/Black", "template": "Write a prompt for a luxury product shot with black and gold theme: {input}. Elegant, premium."},
            {"label": "4. Nature/Sunlight", "template": "Write a prompt for a product shot in nature with natural sunlight/dappled light: {input}."},
            {"label": "5. Cyberpunk/Tech", "template": "Write a prompt for a tech product shot with neon/cyberpunk lighting: {input}."},
            {"label": "6. Flat Lay", "template": "Write a prompt for a flat lay (knolling) photography composition of: {input}."},
            {"label": "7. Custom (自定义)", "template": "Write a product photography prompt for: {input}."}
        ],
        "Support (Pro)": [
            {"label": "1. Apology & Recovery", "template": "Draft a professional apology email to a customer regarding: {input}. Offer a solution/compensation."},
            {"label": "2. Review Request", "template": "Write a polite email asking a happy customer for a product review for: {input}."},
            {"label": "3. Complaint Reply", "template": "Draft a calm, professional response to an angry customer complaint about: {input}."},
            {"label": "4. Promo Announcement", "template": "Write an announcement message for a sale/promotion event: {input}."},
            {"label": "5. Crisis Statement", "template": "Draft a public statement addressing the crisis/issue: {input}. Be transparent and reassuring."},
            {"label": "6. FAQ Gen", "template": "Generate a list of Frequently Asked Questions (FAQ) and answers for the product: {input}."},
            {"label": "7. Custom (自定义)", "template": "Draft a customer support response regarding: {input}."}
        ]
    },
    "Global Student": {
        "Study (Free)": [
            {"label": "1. Note Summarizer", "template": "Summarize the following notes into key bullet points and takeaways: {input}."},
            {"label": "2. Feynman Technique", "template": "Explain the academic concept '{input}' simply."},
            {"label": "3. Lit Review Matrix", "template": "Create a structure for a literature review based on the topic: {input}."},
            {"label": "4. Flashcard (Anki)", "template": "Generate content for flashcards (Front/Back) for the topic: {input}."},
            {"label": "5. Concept Simplifier", "template": "Rewrite the following complex text into simple, easy-to-understand language: {input}."},
            {"label": "6. Translation", "template": "Translate the following academic text into high-quality English (or target language implied): {input}."},
            {"label": "7. Custom (自定义)", "template": "Help me study: {input}."}
        ],
        "Project (Pro)": [
            {"label": "1. Essay Outline", "template": "Create a structured outline for an academic essay on: {input}. Introduction, Body Paragraphs, Conclusion."},
            {"label": "2. Presentation Script", "template": "Write a script for a presentation on: {input}. Include slide cues."},
            {"label": "3. Debate Prep", "template": "Generate arguments (Pro and Con) for the debate topic: {input}."},
            {"label": "4. Lab Report", "template": "Outline a lab report for the experiment: {input}. Intro, Methods, Results, Discussion."},
            {"label": "5. Methodology", "template": "Suggest a research methodology for the study: {input}."},
            {"label": "6. Group Roles", "template": "Assign roles and responsibilities for a group project team of {input}."},
            {"label": "7. Custom (自定义)", "template": "Help with school project: {input}."}
        ],
        "Career (Pro)": [
            {"label": "1. ATS Resume", "template": "Optimize the following resume points for ATS (Applicant Tracking Systems) for the role of: {input}."},
            {"label": "2. Cover Letter", "template": "Write a tailored cover letter for the job description: {input}."},
            {"label": "3. Interview Prep", "template": "Generate 10 likely interview questions and suggested answers for the role: {input}."},
            {"label": "4. LinkedIn Bio", "template": "Write a professional LinkedIn 'About' section for: {input}."},
            {"label": "5. Cold Email", "template": "Draft a cold networking email to a recruiter/professional at: {input}."},
            {"label": "6. Portfolio Desc", "template": "Write a description for a portfolio project: {input}."},
            {"label": "7. Custom (自定义)", "template": "Career advice for: {input}."}
        ]
    },
    "Global Corporate": {
        "Admin (Free)": [
            {"label": "1. Email Polisher", "template": "Rewrite the following email draft to be more professional, concise, and clear: {input}."},
            {"label": "2. Meeting Minutes", "template": "Format the following notes into official Meeting Minutes: {input}."},
            {"label": "3. Official Proposal", "template": "Draft a formal business proposal for: {input}."},
            {"label": "4. Internal Memo", "template": "Write an internal company memo regarding: {input}."},
            {"label": "5. SOP / Process", "template": "Draft a Standard Operating Procedure (SOP) for the task: {input}."},
            {"label": "6. Press Release", "template": "Write a formal press release announcing: {input}."},
            {"label": "7. Custom (自定义)", "template": "Assist with admin task: {input}."}
        ],
        "Strategy (Pro)": [
            {"label": "1. OKRs", "template": "Generate Objectives and Key Results (OKRs) for: {input}."},
            {"label": "2. SWOT Analysis", "template": "Perform a SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats) for: {input}."},
            {"label": "3. Competitor Dive", "template": "Analyze the competitor '{input}' and suggest strategic responses."},
            {"label": "4. Business Canvas", "template": "Draft a Business Model Canvas section for the idea: {input}."},
            {"label": "5. Risk Matrix", "template": "Identify potential risks and mitigation strategies for: {input}."},
            {"label": "6. Pitch Deck", "template": "Outline a pitch deck structure for the product/business: {input}."},
            {"label": "7. Custom (自定义)", "template": "Business strategy advice for: {input}."}
        ],
        "HR & Team (Pro)": [
            {"label": "1. Performance Review", "template": "Draft a performance review feedback for employee: {input}. Use constructive language."},
            {"label": "2. Job Desc (JD)", "template": "Write a detailed Job Description (JD) for the role: {input}."},
            {"label": "3. Onboarding Plan", "template": "Create a 30-60-90 day onboarding plan for: {input}."},
            {"label": "4. Crisis Comms", "template": "Draft a crisis communication message regarding: {input}."},
            {"label": "5. Team Building", "template": "Suggest team building activities for: {input}."},
            {"label": "6. Termination", "template": "Script a professional and compliant termination meeting for: {input}."},
            {"label": "7. Custom (自定义)", "template": "HR advice for: {input}."}
        ]
    }
}

# ==========================================
# 2. FAQ 知识库与拦截逻辑 (16 Items)
# ==========================================

FAQ_DATABASE = {
    "Purchase & License": [
        {"q": "Is this a subscription?", "a": "No. It is a One-Time Payment of $12.90. No monthly fees."},
        {"q": "What is the Refund Policy?", "a": "Strictly No Refunds. This is a digital product (License Key) with instant access."},
        {"q": "I lost my License Key.", "a": "Please visit the LemonSqueezy Order Locator to recover it."},
        {"q": "Can I use it on multiple devices?", "a": "Yes. Your license is tied to your email, accessible on mobile/desktop."}
    ],
    "Business & Affiliate": [
        {"q": "Do you have an Affiliate Program?", "a": "Yes! You earn 40% commission on every sale. Sign up via our LemonSqueezy Affiliate Hub."},
        {"q": "How do I get an Invoice/Receipt?", "a": "LemonSqueezy automatically emails you a tax invoice immediately after purchase."},
        {"q": "Do you offer Education/Bulk Discounts?", "a": "Yes. For schools buying 10+ licenses, please contact support for a tailored quote."}
    ],
    "Technical Support": [
        {"q": "PDF Text is missing/boxes?", "a": "This happens if the system font is missing. Please contact support."},
        {"q": "WeChat button not working?", "a": "Click the green icon -> Select 'WeChat' from your phone's share menu."},
        {"q": "'Invalid Key' error?", "a": "Ensure no spaces are copied. Check your email spelling."},
        {"q": "Why is the generation slow?", "a": "Guest users are in a shared queue. PRO users enjoy dedicated high-speed servers."}
    ],
    "Usage Limits": [
        {"q": "Is PRO truly Unlimited?", "a": "Yes! However, to ensure system stability, we apply a Fair Usage Policy (FUP) of 1000 generations per day."},
        {"q": "Can I use content commercially?", "a": "Yes, PRO users have 100% commercial rights."},
        {"q": "Does it work offline?", "a": "No. PromptLab is a cloud-based AI engine and requires an internet connection."}
    ],
    "Privacy & Security": [
        {"q": "Do you store my prompts?", "a": "We prioritize privacy. Your inputs are processed for generation and not used to train public models."},
        {"q": "Can I share my account?", "a": "No. Your license key is limited to your personal devices only. Excessive sharing triggers our security lock."}
    ]
}

# 简单的多语言映射 (Sidebar用)
LANG_MAP = {
    "English": {"guest": "Guest Trial", "pro": "Pro Enterprise", "generate": "✨ Generate", "input_ph": "Enter details here..."},
    "Bahasa Melayu": {"guest": "Percubaan Pelawat", "pro": "Pro Enterprise", "generate": "✨ Hasilkan", "input_ph": "Masukkan butiran di sini..."},
    "简体中文": {"guest": "试用访客", "pro": "企业专业版", "generate": "✨ 生成内容", "input_ph": "在此输入详细信息..."},
    # ... 其他语言可后续添加
}