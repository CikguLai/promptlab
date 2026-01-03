# dm_data_part1.py
# Core Languages: English, Chinese, Malay
# Features: 20 FAQs (Long Version) & Localized Table

# --- ENGLISH (Full Long Version) ---
FAQ_EN = [
    {"q": "Q1: Is this a subscription?", "a": "No. It is a One-Time Payment of $12.90. No monthly fees."},
    {"q": "Q2: What is the Refund Policy?", "a": "Strictly No Refunds. This is a digital product (License Key) with instant access."},
    {"q": "Q3: I lost my License Key.", "a": "Please visit the LemonSqueezy Order Locator to recover it."},
    {"q": "Q4: Can I use it on multiple devices?", "a": "Yes. Your license is tied to your email, accessible on mobile/desktop."},
    {"q": "Q5: Do you have an Affiliate Program?", "a": "Yes! You earn 40% commission on every sale. Sign up via our LemonSqueezy Affiliate Hub."},
    {"q": "Q6: Where is my Invoice?", "a": "It is sent automatically to your email upon purchase by LemonSqueezy."},
    {"q": "Q7: Do you offer Educational/Bulk pricing?", "a": "Yes. For schools or bulk orders (>10 keys), contact support@cikgulai.com."},
    {"q": "Q8: PDF text is garbled/missing characters.", "a": "Please install the provided 'font.ttf' or ensure your device supports UTF-8 fonts."},
    {"q": "Q9: How to send to Mobile (WeChat/TikTok)?", "a": "Use the 'Mobile Handoff' feature: Scan the QR Code in the sidebar to sync text to your phone instantly."},
    {"q": "Q10: \"Invalid Key\" error?", "a": "Ensure no spaces are copied. Check your email spelling. Keys are case-sensitive."},
    {"q": "Q11: Why is the generation slow?", "a": "Guest users are in a shared queue. PRO users enjoy dedicated high-speed servers."},
    {"q": "Q12: Is PRO truly Unlimited?", "a": "Yes! As a text-based AI engine, PRO users enjoy unlimited prompt generation."},
    {"q": "Q13: Can I use content commercially?", "a": "Yes, PRO users have 100% commercial rights."},
    {"q": "Q14: Does it work offline?", "a": "No. PromptLab is a cloud-based AI engine and requires an internet connection."},
    {"q": "Q15: Is my data private?", "a": "Yes. We do not store your inputs or outputs permanently. Session data is wiped upon logout."},
    {"q": "Q16: Can I share my license key?", "a": "No. Sharing keys publicly or with others may lead to an automatic ban."},
    {"q": "Q17: Why buy this if I have ChatGPT?", "a": "ChatGPT is the engine; we are the steering wheel. Our PASEC Protocol structures prompts professionally, saving you 90% of tuning time."},
    {"q": "Q18: Do I pay for future updates?", "a": "No. One-time payment grants you lifetime access to the current version. Cloud updates are usually free."},
    {"q": "Q19: Can I customize roles?", "a": "Yes. Use the '7. Custom / DIY' option in any dropdown to input your specific needs."},
    {"q": "Q20: Is there a Mobile App?", "a": "No download needed. This is a Web App. Just open the link on your phone browser."}
]

# --- CHINESE (Full Long Version) ---
FAQ_CN = [
    {"q": "问1: 这是订阅制吗？", "a": "完全不需要。本产品为一次性买断制 ($12.90)，无月费。"},
    {"q": "问2: 退款政策是什么？", "a": "虚拟数字商品（激活码），售出即止，概不退款。"},
    {"q": "问3: 忘记激活码怎么办？", "a": "请访问 LemonSqueezy 订单页（Order Locator）找回。"},
    {"q": "问4: 支持多设备吗？", "a": "支持。激活码绑定邮箱，可在手机和电脑端同时使用。"},
    {"q": "问5: 有分销计划吗？", "a": "是的！加入我们的分销计划，每单赚取 40% 佣金。"},
    {"q": "问6: 发票在哪里？", "a": "购买后 LemonSqueezy 会自动发送收据到您的邮箱。"},
    {"q": "问7: 学校/团购有优惠吗？", "a": "有。10个以上的批量采购请联系 support@cikgulai.com。"},
    {"q": "问8: PDF 文字乱码？", "a": "请下载并安装我们提供的 'font.ttf' 字体文件。"},
    {"q": "问9: 如何传送到手机 (微信/抖音)？", "a": "请使用“手机无缝流转”功能：扫描侧边栏二维码，文字即刻同步至手机。"},
    {"q": "问10: 提示“无效激活码”？", "a": "请检查是否复制了多余空格，或输错邮箱。区分大小写。"},
    {"q": "问11: 生成速度慢？", "a": "免费用户在共享队列。Pro 用户享有专属高速通道。"},
    {"q": "问12: 真的是无限吗？", "a": "是的！本产品为纯文本 AI 引擎，Pro 用户可无限生成。（需遵守公平使用原则）。"},
    {"q": "问13: 可以商用吗？", "a": "可以。Pro 用户拥有 100% 商业版权。"},
    {"q": "问14: 支持离线吗？", "a": "不支持。本产品是云端 AI 引擎，需要联网使用。"},
    {"q": "问15: 隐私安全吗？", "a": "安全。我们不永久存储您的输入或生成内容。登出即焚。"},
    {"q": "问16: 可以共享激活码吗？", "a": "不可以。系统检测到滥用或公开分享会导致封号。"},
    {"q": "问17: 有了 ChatGPT 为何还要买？", "a": "ChatGPT 是引擎，我们是方向盘。独家 PASEC 协议能生成普通人写不出的专业指令，节省 90% 调试时间。"},
    {"q": "问18: 未来更新收费吗？", "a": "不收费。一次购买，终身使用。云端功能更新自动同步。"},
    {"q": "问19: 可以自定义角色吗？", "a": "可以。请在下拉菜单选择 '7. Custom / DIY' 输入您的个性化需求。"},
    {"q": "问20: 有手机 App 吗？", "a": "无需下载。这是网页版应用 (Web App)，手机浏览器打开即用。"}
]

# --- BAHASA MELAYU (Full Translation) ---
FAQ_MS = [
    {"q": "S1: Adakah ini langganan?", "a": "Tidak. Ini adalah Bayaran Sekali $12.90. Tiada yuran bulanan."},
    {"q": "S2: Polisi Bayaran Balik?", "a": "Tiada Bayaran Balik. Ini adalah produk digital (Kod Lesen) dengan akses segera."},
    {"q": "S3: Saya hilang Kod Lesen.", "a": "Sila layari LemonSqueezy Order Locator untuk mendapatkannya semula."},
    {"q": "S4: Boleh guna di banyak peranti?", "a": "Ya. Lesen anda terikat dengan emel, boleh diakses di telefon/komputer."},
    {"q": "S5: Ada Program Affiliate?", "a": "Ya! Anda dapat komisen 40% untuk setiap jualan. Daftar melalui LemonSqueezy Affiliate Hub."},
    {"q": "S6: Di mana Invois saya?", "a": "Ia dihantar secara automatik ke emel anda selepas pembelian oleh LemonSqueezy."},
    {"q": "S7: Ada harga Pendidikan/Borong?", "a": "Ya. Untuk sekolah atau pesanan pukal (>10 lesen), hubungi support@cikgulai.com."},
    {"q": "S8: Tulisan PDF rosak/hilang.", "a": "Sila pasang fail 'font.ttf' yang disediakan atau pastikan peranti menyokong font UTF-8."},
    {"q": "S9: Macam mana hantar ke HP (WeChat)?", "a": "Gunakan ciri 'Mobile Handoff': Imbas Kod QR di bar sisi untuk menyegerakkan teks ke telefon anda serta-merta."},
    {"q": "S10: Ralat \"Kod Tidak Sah\"?", "a": "Pastikan tiada ruang kosong disalin. Semak ejaan emel. Kod adalah sensitif huruf."},
    {"q": "S11: Kenapa penjanaan lambat?", "a": "Pengguna tetamu berada dalam barisan kongsi. Pengguna PRO menikmati server berkelajuan tinggi khusus."},
    {"q": "S12: Adakah PRO benar-benar Tanpa Had?", "a": "Ya! Sebagai enjin AI berasaskan teks, pengguna PRO menikmati penjanaan prompt tanpa had."},
    {"q": "S13: Boleh guna untuk komersial?", "a": "Ya, pengguna PRO mempunyai 100% hak komersial."},
    {"q": "S14: Boleh guna offline?", "a": "Tidak. PromptLab adalah enjin AI berasaskan awan dan memerlukan sambungan internet."},
    {"q": "S15: Adakah data saya selamat?", "a": "Ya. Kami tidak menyimpan input atau output anda secara kekal. Data sesi dipadam apabila log keluar."},
    {"q": "S16: Boleh kongsi kod lesen?", "a": "Tidak. Berkongsi kod secara terbuka atau dengan orang lain boleh menyebabkan akaun disekat automatik."},
    {"q": "S17: Kenapa beli jika ada ChatGPT?", "a": "ChatGPT adalah enjin; kami adalah stereng. Protokol PASEC kami menyusun prompt secara profesional, menjimatkan 90% masa anda."},
    {"q": "S18: Perlu bayar untuk update?", "a": "Tidak. Bayaran sekali memberi anda akses seumur hidup ke versi semasa. Kemaskini awan biasanya percuma."},
    {"q": "S19: Boleh custom peranan?", "a": "Ya. Gunakan pilihan '7. Custom / DIY' dalam mana-mana menu untuk memasukkan keperluan khusus anda."},
    {"q": "S20: Ada App telefon?", "a": "Tidak perlu muat turun. Ini adalah Web App. Hanya buka pautan di pelayar telefon anda."}
]

FAQ_DATA = {
    "English": FAQ_EN,
    "简体中文": FAQ_CN,
    "繁體中文": FAQ_CN,
    "Bahasa Melayu": FAQ_MS
}

TABLE_DATA = {
    "English": {"keys": ["Daily Limit", "Content", "Sharing", "Format", "Watermark", "Support", "Price"], "guest": ["5 / Day", "Text", "Text Only", "Basic", "Forced", "Standard", "Free"], "pro": ["*Unlimited", "Clean", "PDF/CSV", "Pro Struct", "Removed", "VIP", "$12.90"]},
    "简体中文": {"keys": ["每日限额", "内容", "分享", "格式", "水印", "客服", "价格"], "guest": ["5次/天", "文本", "仅文本", "基础", "强制", "标准", "免费"], "pro": ["*无限", "纯净", "PDF+CSV", "专业结构", "移除", "VIP", "$12.90"]},
    "Bahasa Melayu": {"keys": ["Had Harian", "Kandungan", "Kongsi", "Format", "Watermark", "Sokongan", "Harga"], "guest": ["5 / Hari", "Teks", "Teks Saja", "Asas", "Ada", "Biasa", "Percuma"], "pro": ["*Tanpa Had", "Bersih", "PDF/CSV", "Pro Struktur", "Tiada", "VIP", "$12.90"]}
}
TABLE_DATA["繁體中文"] = TABLE_DATA["简体中文"]

TICKET_DATA = {
    "English": ["🔴 Bug", "🟠 Billing", "🟡 Feature", "🟢 Partner", "🔵 Other"],
    "简体中文": ["🔴 报错", "🟠 账单", "🟡 建议", "🟢 合作", "🔵 其他"],
    "Bahasa Melayu": ["🔴 Masalah", "🟠 Bayaran", "🟡 Cadangan", "🟢 Rakan Niaga", "🔵 Lain-lain"]
}
TICKET_DATA["繁體中文"] = TICKET_DATA["简体中文"]
