# dm_data_part1.py
# Core Languages: English, Chinese, Malay

# 20 FAQs (Standardized)
Q_KEYS = [
    "Q1: Subscription?", "Q2: Refund?", "Q3: Lost Key?", "Q4: Devices?", 
    "Q5: Affiliate?", "Q6: Invoice?", "Q7: Bulk/School?", "Q8: PDF Error?", 
    "Q9: Mobile/WeChat?", "Q10: Invalid Key?", "Q11: Slow?", "Q12: Unlimited?", 
    "Q13: Commercial?", "Q14: Offline?", "Q15: Privacy?", "Q16: Share Key?", 
    "Q17: Vs ChatGPT?", "Q18: Future Updates?", "Q19: Customize?", "Q20: App?"
]

# --- ENGLISH ---
FAQ_EN = [
    {"q": "Q1: Is this a subscription?", "a": "No. One-time payment of $12.90. Lifetime access."},
    {"q": "Q2: Refund Policy?", "a": "No refunds. Digital license keys are non-returnable."},
    {"q": "Q3: Lost License Key?", "a": "Recover it via LemonSqueezy Order Locator."},
    {"q": "Q4: Multiple devices?", "a": "Yes. Tied to email, works on Phone/PC/Tablet."},
    {"q": "Q5: Affiliate Program?", "a": "Yes! Earn 40% commission. Join via LemonSqueezy."},
    {"q": "Q6: Invoice?", "a": "Sent automatically to email after purchase."},
    {"q": "Q7: School/Bulk pricing?", "a": "Yes. Contact support for orders >10 keys."},
    {"q": "Q8: PDF garbled?", "a": "Install the provided 'font.ttf' file."},
    {"q": "Q9: Send to Mobile (WeChat)?", "a": "Scan the 'Mobile Handoff' QR Code in the sidebar."},
    {"q": "Q10: Invalid Key?", "a": "Check for extra spaces. Case sensitive."},
    {"q": "Q11: Slow generation?", "a": "Guests share queues. Pro gets high-speed priority."},
    {"q": "Q12: Is it Unlimited?", "a": "Yes! Unlimited text generation for Pro users."},
    {"q": "Q13: Commercial Use?", "a": "Yes. Pro users own 100% commercial rights."},
    {"q": "Q14: Offline mode?", "a": "No. Requires internet connection."},
    {"q": "Q15: Privacy?", "a": "Yes. Data wiped on logout. Zero retention."},
    {"q": "Q16: Share Key?", "a": "No. Public sharing leads to auto-ban."},
    {"q": "Q17: Why buy if I have ChatGPT?", "a": "We are the steering wheel. PASEC Protocol saves 90% tuning time."},
    {"q": "Q18: Future updates?", "a": "Free cloud updates for the current version."},
    {"q": "Q19: Customize roles?", "a": "Yes, use the '7. Custom / DIY' option."},
    {"q": "Q20: Mobile App?", "a": "No install needed. It's a Web App (PWA)."}
]

# --- CHINESE (Simplified) ---
FAQ_CN = [
    {"q": "问1: 是订阅制吗？", "a": "不是。$12.90 一次性买断，终身使用。"},
    {"q": "问2: 退款政策？", "a": "虚拟商品（激活码）发货即止，不支持退款。"},
    {"q": "问3: 忘记激活码？", "a": "请在 LemonSqueezy 订单页输入邮箱找回。"},
    {"q": "问4: 支持多设备？", "a": "支持。绑定邮箱，手机/电脑皆可使用。"},
    {"q": "问5: 分销计划？", "a": "有！推广赚取 40% 佣金。"},
    {"q": "问6: 发票？", "a": "购买后系统自动发送至邮箱。"},
    {"q": "问7: 学校团购？", "a": "支持。10人以上请联系客服。"},
    {"q": "问8: PDF乱码？", "a": "请安装提供的 font.ttf 字体。"},
    {"q": "问9: 传手机/微信？", "a": "请扫描侧边栏“手机流转”二维码。"},
    {"q": "问10: 无效激活码？", "a": "请检查空格或大小写。"},
    {"q": "问11: 生成慢？", "a": "免费版排队。Pro版享高速通道。"},
    {"q": "问12: 真的无限吗？", "a": "是的！Pro用户文本生成无限制。"},
    {"q": "问13: 可商用吗？", "a": "可以。Pro拥有100%商业版权。"},
    {"q": "问14: 可离线吗？", "a": "不可。需连接云端AI引擎。"},
    {"q": "问15: 隐私？", "a": "安全。登出即焚，不存数据。"},
    {"q": "问16: 共享账号？", "a": "禁止。滥用会导致封号。"},
    {"q": "问17: 对比ChatGPT？", "a": "PASEC协议提供专业结构，省去90%调试时间。"},
    {"q": "问18: 更新收费？", "a": "不收费。云端自动更新。"},
    {"q": "问19: 自定义？", "a": "支持。请选 '7. Custom / DIY'。"},
    {"q": "问20: 手机App？", "a": "无需下载。浏览器打开即用。"}
]

# --- BAHASA MELAYU (精翻) ---
FAQ_MS = [
    {"q": "S1: Adakah ini langganan?", "a": "Tidak. Bayaran sekali $12.90 sahaja. Tiada yuran bulanan."},
    {"q": "S2: Polisi Bayaran Balik?", "a": "Tiada bayaran balik untuk produk digital (Kod Lesen)."},
    {"q": "S3: Hilang Kod Lesen?", "a": "Sila guna LemonSqueezy Order Locator untuk dapatkan semula."},
    {"q": "S4: Boleh guna banyak peranti?", "a": "Ya. Dilesenkan ikut emel, boleh guna di HP/PC."},
    {"q": "S5: Program Affiliate?", "a": "Ya! Komisen 40% setiap jualan."},
    {"q": "S6: Resit/Invois?", "a": "Dihantar automatik ke emel selepas pembelian."},
    {"q": "S7: Harga Borong/Sekolah?", "a": "Ya. Untuk >10 lesen, hubungi sokongan."},
    {"q": "S8: Tulisan PDF rosak?", "a": "Sila pasang fail 'font.ttf' yang disediakan."},
    {"q": "S9: Hantar ke HP (WeChat)?", "a": "Imbas Kod QR di bar sisi untuk copy teks ke HP."},
    {"q": "S10: Kod Tidak Sah?", "a": "Periksa ejaan emel dan tiada jarak kosong."},
    {"q": "S11: Kenapa lambat?", "a": "Guest guna server kongsi. PRO guna laluan pantas."},
    {"q": "S12: Betul-betul Tanpa Had?", "a": "Ya! Penjanaan teks tanpa had untuk pengguna PRO."},
    {"q": "S13: Boleh guna komersial?", "a": "Ya. Hak cipta komersial 100% untuk PRO."},
    {"q": "S14: Boleh guna offline?", "a": "Tidak. Perlu sambungan internet."},
    {"q": "S15: Privasi Data?", "a": "Ya. Data dipadam selepas log keluar."},
    {"q": "S16: Kongsi Lesen?", "a": "Dilarang. Akaun akan disekat jika disalah guna."},
    {"q": "S17: Beza dengan ChatGPT?", "a": "Kami sediakan struktur PASEC profesional. Jimat 90% masa."},
    {"q": "S18: Update berbayar?", "a": "Tidak. Kemaskini percuma seumur hidup versi ini."},
    {"q": "S19: Boleh Custom?", "a": "Ya. Pilih opsyen '7. Custom / DIY'."},
    {"q": "S20: Ada App?", "a": "Tak perlu install. Guna terus di browser (Web App)."}
]

# 整合数据字典
FAQ_DATA = {
    "English": FAQ_EN,
    "简体中文": FAQ_CN,
    "繁體中文": FAQ_CN, # 繁体复用简体
    "Bahasa Melayu": FAQ_MS
}

TABLE_DATA = {
    "English": {"keys": ["Daily Limit", "Content", "Sharing", "Format", "Watermark", "Support", "Price"], "guest": ["5 / Day", "Text", "Text Only", "Basic", "Forced", "Standard", "Free"], "pro": ["*Unlimited", "Clean", "PDF/CSV", "Pro Struct", "Removed", "VIP", "$12.90"]},
    "简体中文": {"keys": ["每日限额", "内容", "分享", "格式", "水印", "客服", "价格"], "guest": ["5次/天", "文本", "仅文本", "基础", "强制", "标准", "免费"], "pro": ["*无限", "纯净", "PDF+CSV", "专业结构", "移除", "VIP", "$12.90"]},
    "Bahasa Melayu": {"keys": ["Had Harian", "Kandungan", "Kongsi", "Format", "Watermark", "Sokongan", "Harga"], "guest": ["5 / Hari", "Teks", "Teks Saja", "Asas", "Ada", "Biasa", "Percuma"], "pro": ["*Tanpa Had", "Bersih", "PDF/CSV", "Pro Struktur", "Tiada", "VIP", "$12.90"]}
}
# 补全繁体和其他复用
TABLE_DATA["繁體中文"] = TABLE_DATA["简体中文"]

TICKET_DATA = {
    "English": ["🔴 Bug", "🟠 Billing", "🟡 Feature", "🟢 Partner", "🔵 Other"],
    "简体中文": ["🔴 报错", "🟠 账单", "🟡 建议", "🟢 合作", "🔵 其他"],
    "Bahasa Melayu": ["🔴 Masalah", "🟠 Bayaran", "🟡 Cadangan", "🟢 Rakan Niaga", "🔵 Lain-lain"]
}
TICKET_DATA["繁體中文"] = TICKET_DATA["简体中文"]