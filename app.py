import streamlit as st
import google.generativeai as genai
from PIL import Image
import zipfile
import io
import time
import requests
from fpdf import FPDF
import base64
import random
import urllib.parse

# ==========================================
# 1. 全球多语言字典 (15 Languages - Fully Loaded)
# ==========================================
TRANSLATIONS = {
    "English": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 VIP Access",
        "activation_code": "Activation Code",
        "vip_active": "✅ VIP Active",
        "vip_benefits": "⚡ Unlock: Instant Speed, Max 50/Batch, PDF Export",
        "free_limit_info": "🔓 Free Daily Limit: {remaining} left",
        "upgrade_btn": "🚀 Get Lifetime Access",
        "limited_offer": "Limited time early-bird price.",
        "get_started": "📧 Get Started",
        "email_hint": "Enter email to activate free generator.",
        "config": "⚙️ Configuration",
        "mode_label": "Mode:",
        "input_method_label": "Input Method:",
        "input_upload": "📷 Upload Image (Analyze)",
        "input_text": "✍️ Type Idea (Create)",
        "text_area_label": "Enter your idea here (e.g., 'A cute dinosaur'):",
        "lang_label": "Output Language:",
        "style_vip_label": "🎨 Style (VIP):",
        "style_free_label": "🎨 Style (Free):",
        "style_lock_warning": "💎 This style is for VIPs only. Please upgrade.",
        "upload_label": "Upload Images (Max {limit}/Batch)",
        "email_warning": "🔒 Please enter your Email in sidebar to proceed.",
        "generate_btn": "🚀 Generate Content",
        "daily_limit_error": "⛔ Daily Limit Reached ({current}/{total}). Please come back tomorrow.",
        "credit_warning": "⚠️ You only have {count} credits left. Processing first {count} items.",
        "batch_warning": "⚠️ Batch limit is {limit}. Processing first {limit} only.",
        "processing_vip": "⚡ **VIP Speed:** Processing item {current}/{total} ...",
        "processing_free": "⏳ **Free Tier Queue:** {msg} ...",
        "complete": "✅ Complete!",
        "clear_btn": "🗑️ Clear All",
        "copy_text": "📋 Copy Text",
        "share_title": "🚀 Share to Social Media:",
        "download_pdf": "📄 Download PDF Report",
        "upsell_msg": "⚡ Want instant speed & PDF reports? <a href='#' style='color:#FF4B4B'>Upgrade to VIP</a>",
        "export_title": "📦 Export Data",
        "download_zip": "💎 Download VIP Batch Pack (.zip)",
        "zip_desc": "✅ Includes: Excel (CSV) + Text files",
        "download_txt": "📄 Download as Text (.txt)",
        "txt_desc": "🔒 Want Excel/CSV export? Upgrade to VIP.",
        "footer_rights": "© 2025 Cikgu Lai. All Rights Reserved.",
        "footer_disclaimer": "Disclaimer: Data is processed securely and deleted instantly.",
        "faq_title": "📚 FAQ",
        "faq_content": "**Q: Does it create images?** A: No, it generates Prompts. Copy to Bing/MJ.\n**Q: Subscription?** A: No! One-time payment.\n**Q: Paid but no code?** A: Check Spam.",
        "support_title": "💁 Help Center",
        "support_ticket_label": "Submit a support ticket.",
        "ticket_email": "Email (Required)",
        "ticket_type": "Issue Type",
        "ticket_desc": "Description",
        "ticket_btn": "🚀 Submit Ticket",
        "ticket_success": "✅ Ticket {id} Created!"
    },
    "Chinese (Simplified)": {
        "app_title": "VisionPrompter 视觉大师",
        "vip_access": "💎 VIP 会员通道",
        "activation_code": "输入激活码",
        "vip_active": "✅ VIP 已激活",
        "vip_benefits": "⚡ 解锁权益：极速生成、批量50次、PDF导出",
        "free_limit_info": "🔓 今日免费额度剩余: {remaining}",
        "upgrade_btn": "🚀 获取终身会员 (限时)",
        "limited_offer": "早鸟价限时优惠",
        "get_started": "📧 免费试用",
        "email_hint": "输入邮箱以开启免费生成器",
        "config": "⚙️ 生成设置",
        "mode_label": "选择模式:",
        "input_method_label": "输入方式:",
        "input_upload": "📷 上传图片 (分析风格)",
        "input_text": "✍️ 输入想法 (从零创作)",
        "text_area_label": "在这里输入你的想法 (例如：'一只吃披萨的猫'):",
        "lang_label": "生成语言:",
        "style_vip_label": "🎨 艺术风格 (VIP):",
        "style_free_label": "🎨 基础风格 (免费):",
        "style_lock_warning": "💎 此风格仅限 VIP。请升级以解锁高级风格。",
        "upload_label": "上传图片 (每批最多 {limit} 张)",
        "email_warning": "🔒 请在侧边栏输入邮箱以继续。",
        "generate_btn": "🚀 开始生成",
        "daily_limit_error": "⛔ 今日额度已用完 ({current}/{total})。请明天再来。",
        "credit_warning": "⚠️ 您只剩 {count} 次额度，将仅处理前 {count} 项。",
        "batch_warning": "⚠️ 单次限制 {limit} 项。仅处理前 {limit} 项。",
        "processing_vip": "⚡ **VIP 极速模式:** 正在处理第 {current}/{total} 项 ...",
        "processing_free": "⏳ **免费排队中:** {msg} ...",
        "complete": "✅ 处理完成!",
        "clear_btn": "🗑️ 清空历史",
        "copy_text": "📋 复制文案",
        "share_title": "🚀 一键分享到社媒:",
        "download_pdf": "📄 下载 PDF 报告",
        "upsell_msg": "⚡ 想要秒速生成和 Excel 报表？ <a href='#' style='color:#FF4B4B'>升级 VIP</a>",
        "export_title": "📦 数据导出",
        "download_zip": "💎 下载 VIP 数据包 (.zip)",
        "zip_desc": "✅ 包含: Excel表格 (CSV) + 文本文件",
        "download_txt": "📄 下载纯文本 (.txt)",
        "txt_desc": "🔒 需要 Excel 表格？请升级 VIP。",
        "footer_rights": "© 2025 Cikgu Lai. 版权所有。",
        "footer_disclaimer": "免责声明：数据仅供 AI 分析，处理后即刻删除，绝不留存。",
        "faq_title": "📚 常见问题",
        "faq_content": "**Q: 能直接生图吗？** A: 不能，生成的是提示词。\n**Q: 是订阅制吗？** A: 不是！一次付费终身使用。\n**Q: 没收到码？** A: 检查垃圾邮件。",
        "support_title": "💁 帮助中心",
        "support_ticket_label": "提交工单，24小时内回复。",
        "ticket_email": "联系邮箱",
        "ticket_type": "问题类型",
        "ticket_desc": "问题描述",
        "ticket_btn": "🚀 提交工单",
        "ticket_success": "✅ 工单 {id} 已创建！"
    },
    "Chinese (Traditional)": {
        "app_title": "VisionPrompter 視覺大師",
        "vip_access": "💎 VIP 會員通道",
        "activation_code": "輸入激活碼",
        "vip_active": "✅ VIP 已激活",
        "vip_benefits": "⚡ 解鎖權益：極速生成、批量50次、PDF導出",
        "free_limit_info": "🔓 今日免費額度剩餘: {remaining}",
        "upgrade_btn": "🚀 獲取終身會員 (限時)",
        "limited_offer": "早鳥價限時優惠",
        "get_started": "📧 免費試用",
        "email_hint": "輸入郵箱以開啟免費生成器",
        "config": "⚙️ 生成設置",
        "mode_label": "選擇模式:",
        "input_method_label": "輸入方式:",
        "input_upload": "📷 上傳圖片 (分析風格)",
        "input_text": "✍️ 輸入想法 (從零創作)",
        "text_area_label": "在這裡輸入你的想法:",
        "lang_label": "生成語言:",
        "style_vip_label": "🎨 藝術風格 (VIP):",
        "style_free_label": "🎨 基礎風格 (免費):",
        "style_lock_warning": "💎 此風格僅限 VIP。請升級以解鎖高級風格。",
        "upload_label": "上傳圖片 (每批最多 {limit} 張)",
        "email_warning": "🔒 請在側邊欄輸入郵箱以繼續。",
        "generate_btn": "🚀 開始生成",
        "daily_limit_error": "⛔ 今日額度已用完 ({current}/{total})。請明天再來。",
        "credit_warning": "⚠️ 您只剩 {count} 次額度。",
        "batch_warning": "⚠️ 單次限制 {limit} 項。",
        "processing_vip": "⚡ **VIP 極速模式:** 正在處理第 {current}/{total} 項 ...",
        "processing_free": "⏳ **免費排隊中:** {msg} ...",
        "complete": "✅ 處理完成!",
        "clear_btn": "🗑️ 清空歷史",
        "copy_text": "📋 複製文案",
        "share_title": "🚀 一鍵分享到社媒:",
        "download_pdf": "📄 下載 PDF 報告",
        "upsell_msg": "⚡ 想要秒速生成和 Excel 報表？ <a href='#' style='color:#FF4B4B'>升級 VIP</a>",
        "export_title": "📦 數據導出",
        "download_zip": "💎 下載 VIP 數據包 (.zip)",
        "zip_desc": "✅ 包含: Excel表格 (CSV) + 文本文件",
        "download_txt": "📄 下載純文本 (.txt)",
        "txt_desc": "🔒 需要 Excel 表格？請升級 VIP。",
        "footer_rights": "© 2025 Cikgu Lai. 版權所有。",
        "footer_disclaimer": "免責聲明：數據僅供 AI 分析，處理後即刻刪除。",
        "faq_title": "📚 常見問題",
        "faq_content": "**Q: 能直接生圖嗎？** A: 不能，生成的是提示詞。\n**Q: 是訂閱制嗎？** A: 不是！一次付費終身使用。",
        "support_title": "💁 幫助中心",
        "support_ticket_label": "提交工單。",
        "ticket_email": "聯繫郵箱",
        "ticket_type": "問題類型",
        "ticket_desc": "問題描述",
        "ticket_btn": "🚀 提交工單",
        "ticket_success": "✅ 工單 {id} 已創建！"
    },
    "Malay": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 Akses VIP",
        "activation_code": "Kod Pengaktifan",
        "vip_active": "✅ VIP Aktif",
        "vip_benefits": "⚡ Buka: Kelajuan Pantas, 50/Batch, PDF",
        "free_limit_info": "🔓 Had Harian Percuma: {remaining} tinggal",
        "upgrade_btn": "🚀 Dapatkan Akses Seumur Hidup",
        "limited_offer": "Tawaran harga terhad.",
        "get_started": "📧 Mula Sekarang",
        "email_hint": "Masukkan emel untuk mula.",
        "config": "⚙️ Tetapan",
        "mode_label": "Mod:",
        "input_method_label": "Kaedah Input:",
        "input_upload": "📷 Muat Naik Gambar (Analisis)",
        "input_text": "✍️ Tulis Idea (Cipta)",
        "text_area_label": "Masukkan idea anda di sini:",
        "lang_label": "Bahasa Output:",
        "style_vip_label": "🎨 Gaya Seni (VIP):",
        "style_free_label": "🎨 Gaya Asas (Percuma):",
        "style_lock_warning": "💎 Gaya ini untuk VIP sahaja. Sila naik taraf.",
        "upload_label": "Muat Naik Gambar (Max {limit})",
        "email_warning": "🔒 Sila masukkan Emel di sidebar.",
        "generate_btn": "🚀 Mula Jana",
        "daily_limit_error": "⛔ Had Harian Dicapai ({current}/{total}).",
        "credit_warning": "⚠️ Baki anda {count}.",
        "batch_warning": "⚠️ Had batch ialah {limit}.",
        "processing_vip": "⚡ **Kelajuan VIP:** Memproses item {current}/{total} ...",
        "processing_free": "⏳ **Barisan Percuma:** {msg} ...",
        "complete": "✅ Selesai!",
        "clear_btn": "🗑️ Padam Semua",
        "copy_text": "📋 Salin Teks",
        "share_title": "🚀 Kongsi ke Media Sosial:",
        "download_pdf": "📄 Muat Turun PDF",
        "upsell_msg": "⚡ Mahu laju & Excel? <a href='#' style='color:#FF4B4B'>Naik Taraf VIP</a>",
        "export_title": "📦 Eksport Data",
        "download_zip": "💎 Muat Turun Pek VIP (.zip)",
        "zip_desc": "✅ Termasuk: Excel (CSV) + Teks",
        "download_txt": "📄 Muat Turun Teks (.txt)",
        "txt_desc": "🔒 Mahu Excel? Naik Taraf VIP.",
        "footer_rights": "© 2025 Cikgu Lai. Hak Cipta Terpelihara.",
        "footer_disclaimer": "Penafian: Data diproses oleh AI dan dipadam serta-merta.",
        "faq_title": "📚 Soalan Lazim",
        "faq_content": "**Q: Jana gambar?** A: Tidak, hanya Prompt.\n**Q: Bayaran bulanan?** A: Tidak! Bayar sekali seumur hidup.",
        "support_title": "💁 Pusat Bantuan",
        "support_ticket_label": "Hantar tiket sokongan.",
        "ticket_email": "Emel",
        "ticket_type": "Jenis Masalah",
        "ticket_desc": "Huraian",
        "ticket_btn": "🚀 Hantar Tiket",
        "ticket_success": "✅ Tiket {id} Dicipta!"
    },
    "Indonesian": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 Akses VIP",
        "activation_code": "Kode Aktivasi",
        "vip_active": "✅ VIP Aktif",
        "vip_benefits": "⚡ Buka: Kecepatan Instan, 50/Batch, PDF",
        "free_limit_info": "🔓 Batas Harian Gratis: {remaining}",
        "upgrade_btn": "🚀 Dapatkan Akses Seumur Hidup",
        "limited_offer": "Penawaran terbatas.",
        "get_started": "📧 Mulai Sekarang",
        "email_hint": "Masukkan email untuk mulai.",
        "config": "⚙️ Pengaturan",
        "mode_label": "Mode:",
        "input_method_label": "Metode Input:",
        "input_upload": "📷 Unggah Gambar (Analisis)",
        "input_text": "✍️ Tulis Ide (Buat Baru)",
        "text_area_label": "Masukkan ide Anda di sini:",
        "lang_label": "Bahasa Output:",
        "style_vip_label": "🎨 Gaya Seni (VIP):",
        "style_free_label": "🎨 Gaya Dasar (Gratis):",
        "style_lock_warning": "💎 Gaya ini khusus VIP.",
        "upload_label": "Unggah Gambar (Maks {limit})",
        "email_warning": "🔒 Masukkan Email di sidebar.",
        "generate_btn": "🚀 Mulai",
        "daily_limit_error": "⛔ Batas Harian Tercapai.",
        "credit_warning": "⚠️ Sisa kredit {count}.",
        "batch_warning": "⚠️ Batas batch adalah {limit}.",
        "processing_vip": "⚡ **Kecepatan VIP:** Memproses {current}/{total} ...",
        "processing_free": "⏳ **Antrian Gratis:** {msg} ...",
        "complete": "✅ Selesai!",
        "clear_btn": "🗑️ Hapus Semua",
        "copy_text": "📋 Salin Teks",
        "share_title": "🚀 Bagikan:",
        "download_pdf": "📄 Unduh PDF",
        "upsell_msg": "⚡ Ingin Cepat & Excel? <a href='#' style='color:#FF4B4B'>Upgrade VIP</a>",
        "export_title": "📦 Ekspor Data",
        "download_zip": "💎 Unduh Paket VIP (.zip)",
        "zip_desc": "✅ Termasuk: Excel (CSV) + Teks",
        "download_txt": "📄 Unduh Teks (.txt)",
        "txt_desc": "🔒 Butuh Excel? Upgrade VIP.",
        "footer_rights": "© 2025 Cikgu Lai. Hak Cipta Dilindungi.",
        "footer_disclaimer": "Penafian: Gambar diproses aman & langsung dihapus.",
        "faq_title": "📚 FAQ",
        "faq_content": "**Q: Buat gambar?** A: Tidak, hanya Prompt.\n**Q: Langganan?** A: Tidak! Bayar sekali.",
        "support_title": "💁 Pusat Bantuan",
        "support_ticket_label": "Kirim tiket dukungan.",
        "ticket_email": "Email",
        "ticket_type": "Jenis Masalah",
        "ticket_desc": "Deskripsi",
        "ticket_btn": "🚀 Kirim Tiket",
        "ticket_success": "✅ Tiket {id} Dibuat!"
    },
    "Vietnamese": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 Truy cập VIP",
        "activation_code": "Mã kích hoạt",
        "vip_active": "✅ VIP đã kích hoạt",
        "vip_benefits": "⚡ Mở khóa: Tốc độ tức thì, 50/Lô, PDF",
        "free_limit_info": "🔓 Giới hạn miễn phí: còn {remaining}",
        "upgrade_btn": "🚀 Mua trọn đời",
        "limited_offer": "Ưu đãi giới hạn.",
        "get_started": "📧 Bắt đầu",
        "email_hint": "Nhập email để kích hoạt.",
        "config": "⚙️ Cấu hình",
        "mode_label": "Chế độ:",
        "input_method_label": "Phương thức:",
        "input_upload": "📷 Tải ảnh (Phân tích)",
        "input_text": "✍️ Nhập ý tưởng (Tạo mới)",
        "text_area_label": "Nhập ý tưởng của bạn:",
        "lang_label": "Ngôn ngữ đầu ra:",
        "style_vip_label": "🎨 Phong cách (VIP):",
        "style_free_label": "🎨 Phong cách (Free):",
        "style_lock_warning": "💎 Phong cách này chỉ dành cho VIP.",
        "upload_label": "Tải ảnh lên (Tối đa {limit})",
        "email_warning": "🔒 Vui lòng nhập Email để tiếp tục.",
        "generate_btn": "🚀 Tạo nội dung",
        "daily_limit_error": "⛔ Đã đạt giới hạn ngày.",
        "credit_warning": "⚠️ Bạn còn {count} lượt.",
        "batch_warning": "⚠️ Giới hạn mỗi lần là {limit}.",
        "processing_vip": "⚡ **Tốc độ VIP:** Đang xử lý {current}/{total} ...",
        "processing_free": "⏳ **Hàng chờ:** {msg} ...",
        "complete": "✅ Hoàn tất!",
        "clear_btn": "🗑️ Xóa tất cả",
        "copy_text": "📋 Sao chép",
        "share_title": "🚀 Chia sẻ:",
        "download_pdf": "📄 Tải PDF",
        "upsell_msg": "⚡ Cần tốc độ & Excel? <a href='#' style='color:#FF4B4B'>Nâng cấp VIP</a>",
        "export_title": "📦 Xuất dữ liệu",
        "download_zip": "💎 Tải gói VIP (.zip)",
        "zip_desc": "✅ Gồm: Excel (CSV) + Văn bản",
        "download_txt": "📄 Tải văn bản (.txt)",
        "txt_desc": "🔒 Cần Excel? Nâng cấp VIP.",
        "footer_rights": "© 2025 Cikgu Lai. Bảo lưu mọi quyền.",
        "footer_disclaimer": "Lưu ý: Dữ liệu được xử lý an toàn và xóa ngay lập tức.",
        "faq_title": "📚 Hỏi đáp",
        "faq_content": "**Q: Tạo ảnh?** A: Không, chỉ tạo Prompt.\n**Q: Thuê bao?** A: Không! Trả một lần.",
        "support_title": "💁 Trung tâm trợ giúp",
        "support_ticket_label": "Gửi phiếu hỗ trợ.",
        "ticket_email": "Email",
        "ticket_type": "Vấn đề",
        "ticket_desc": "Mô tả",
        "ticket_btn": "🚀 Gửi phiếu",
        "ticket_success": "✅ Phiếu {id} đã tạo!"
    },
    "Thai": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 สมาชิก VIP",
        "activation_code": "รหัสเปิดใช้งาน",
        "vip_active": "✅ VIP ใช้งานอยู่",
        "vip_benefits": "⚡ ปลดล็อก: ความเร็วสูง, 50รูป/ครั้ง, PDF",
        "free_limit_info": "🔓 โควต้าฟรีวันนี้: เหลือ {remaining}",
        "upgrade_btn": "🚀 รับสิทธิ์ใช้งานตลอดชีพ",
        "limited_offer": "ข้อเสนอเวลาจำกัด",
        "get_started": "📧 เริ่มต้นใช้งาน",
        "email_hint": "ใส่อีเมลเพื่อเริ่มใช้งาน",
        "config": "⚙️ ตั้งค่า",
        "mode_label": "โหมด:",
        "input_method_label": "วิธีการ:",
        "input_upload": "📷 อัปโหลดรูป (วิเคราะห์)",
        "input_text": "✍️ พิมพ์ไอเดีย (สร้างใหม่)",
        "text_area_label": "ใส่ไอเดียของคุณที่นี่:",
        "lang_label": "ภาษาผลลัพธ์:",
        "style_vip_label": "🎨 สไตล์ (VIP):",
        "style_free_label": "🎨 สไตล์ (ฟรี):",
        "style_lock_warning": "💎 สไตล์นี้สำหรับ VIP เท่านั้น",
        "upload_label": "อัปโหลดรูปภาพ (สูงสุด {limit})",
        "email_warning": "🔒 กรุณาใส่อีเมลเพื่อดำเนินการต่อ",
        "generate_btn": "🚀 สร้างเนื้อหา",
        "daily_limit_error": "⛔ ครบโควต้าประจำวันแล้ว",
        "credit_warning": "⚠️ เหลือโควต้า {count} รูป",
        "batch_warning": "⚠️ จำกัดครั้งละ {limit} รูป",
        "processing_vip": "⚡ **ความเร็ว VIP:** กำลังประมวลผล {current}/{total} ...",
        "processing_free": "⏳ **คิวฟรี:** {msg} ...",
        "complete": "✅ เสร็จสิ้น!",
        "clear_btn": "🗑️ ล้างทั้งหมด",
        "copy_text": "📋 คัดลอกข้อความ",
        "share_title": "🚀 แชร์:",
        "download_pdf": "📄 ดาวน์โหลด PDF",
        "upsell_msg": "⚡ ต้องการความเร็ว & Excel? <a href='#' style='color:#FF4B4B'>อัปเกรด VIP</a>",
        "export_title": "📦 ส่งออกข้อมูล",
        "download_zip": "💎 ดาวน์โหลด VIP Pack (.zip)",
        "zip_desc": "✅ รวม: Excel (CSV) + ข้อความ",
        "download_txt": "📄 ดาวน์โหลดข้อความ (.txt)",
        "txt_desc": "🔒 ต้องการ Excel? อัปเกรด VIP",
        "footer_rights": "© 2025 Cikgu Lai. สงวนลิขสิทธิ์",
        "footer_disclaimer": "คำเตือน: ข้อมูลถูกประมวลผลอย่างปลอดภัยและลบทันที",
        "faq_title": "📚 คำถามที่พบบ่อย",
        "faq_content": "**Q: สร้างรูป?** A: ไม่, สร้าง Prompt\n**Q: รายเดือน?** A: ไม่! จ่ายครั้งเดียว",
        "support_title": "💁 ศูนย์ช่วยเหลือ",
        "support_ticket_label": "ส่งตั๋วสนับสนุน",
        "ticket_email": "อีเมล",
        "ticket_type": "ประเภทปัญหา",
        "ticket_desc": "รายละเอียด",
        "ticket_btn": "🚀 ส่งตั๋ว",
        "ticket_success": "✅ ตั๋ว {id} ถูกสร้างแล้ว!"
    },
    "Japanese": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 VIPアクセス",
        "activation_code": "アクティベーションコード",
        "vip_active": "✅ VIP有効",
        "vip_benefits": "⚡ 特典：高速生成、一括50枚、PDF出力",
        "free_limit_info": "🔓 今日の残り回数: {remaining}",
        "upgrade_btn": "🚀 生涯アクセス権を入手",
        "limited_offer": "期間限定の早割価格",
        "get_started": "📧 メール登録",
        "email_hint": "メールアドレスを入力して開始",
        "config": "⚙️ 設定",
        "mode_label": "モード:",
        "input_method_label": "入力方法:",
        "input_upload": "📷 画像アップロード (分析)",
        "input_text": "✍️ アイデア入力 (作成)",
        "text_area_label": "アイデアを入力:",
        "lang_label": "生成言語:",
        "style_vip_label": "🎨 スタイル (VIP):",
        "style_free_label": "🎨 基本スタイル (無料):",
        "style_lock_warning": "💎 VIP限定です。",
        "upload_label": "画像アップロード (最大 {limit} 枚)",
        "email_warning": "🔒 メールを入力してください。",
        "generate_btn": "🚀 生成開始",
        "daily_limit_error": "⛔ 1日の制限に達しました。",
        "credit_warning": "⚠️ 残り {count} 回です。",
        "batch_warning": "⚠️ 一括制限は {limit} 枚です。",
        "processing_vip": "⚡ **VIPスピード:** 処理中 {current}/{total} ...",
        "processing_free": "⏳ **無料待機列:** {msg} ...",
        "complete": "✅ 完了!",
        "clear_btn": "🗑️ 履歴をクリア",
        "copy_text": "📋 コピー",
        "share_title": "🚀 共有:",
        "download_pdf": "📄 PDFダウンロード",
        "upsell_msg": "⚡ 高速化? <a href='#' style='color:#FF4B4B'>VIPへ</a>",
        "export_title": "📦 データエクスポート",
        "download_zip": "💎 VIPパック (.zip)",
        "zip_desc": "✅ Excel (CSV) + テキスト",
        "download_txt": "📄 テキスト (.txt)",
        "txt_desc": "🔒 Excelが必要ですか？VIPへ。",
        "footer_rights": "© 2025 Cikgu Lai. All Rights Reserved.",
        "footer_disclaimer": "免責事項：データは即座に削除されます。",
        "faq_title": "📚 FAQ",
        "faq_content": "**Q: 画像生成？** A: いいえ、プロンプト生成です。\n**Q: 月額？** A: いいえ！買い切りです。",
        "support_title": "💁 ヘルプセンター",
        "support_ticket_label": "サポートチケットを送信。",
        "ticket_email": "メール",
        "ticket_type": "問題の種類",
        "ticket_desc": "詳細",
        "ticket_btn": "🚀 送信",
        "ticket_success": "✅ チケット {id} 作成完了!"
    },
    "Korean": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 VIP 액세스",
        "activation_code": "활성화 코드",
        "vip_active": "✅ VIP 활성화됨",
        "vip_benefits": "⚡ 혜택: 초고속 생성, 50장 일괄, PDF",
        "free_limit_info": "🔓 무료 한도: {remaining}",
        "upgrade_btn": "🚀 평생 이용권",
        "limited_offer": "조기 구매 할인",
        "get_started": "📧 시작하기",
        "email_hint": "이메일 입력",
        "config": "⚙️ 설정",
        "mode_label": "모드:",
        "input_method_label": "입력 방식:",
        "input_upload": "📷 이미지 업로드 (분석)",
        "input_text": "✍️ 아이디어 입력 (생성)",
        "text_area_label": "아이디어를 입력하세요:",
        "lang_label": "결과 언어:",
        "style_vip_label": "🎨 스타일 (VIP):",
        "style_free_label": "🎨 스타일 (무료):",
        "style_lock_warning": "💎 VIP 전용입니다.",
        "upload_label": "업로드 (최대 {limit})",
        "email_warning": "🔒 이메일을 입력하세요.",
        "generate_btn": "🚀 생성 시작",
        "daily_limit_error": "⛔ 일일 한도 초과.",
        "credit_warning": "⚠️ 남은 크레딧 {count}.",
        "batch_warning": "⚠️ 배치 한도 {limit}.",
        "processing_vip": "⚡ **VIP 스피드:** 처리 중 {current}/{total} ...",
        "processing_free": "⏳ **대기열:** {msg} ...",
        "complete": "✅ 완료!",
        "clear_btn": "🗑️ 지우기",
        "copy_text": "📋 복사",
        "share_title": "🚀 공유:",
        "download_pdf": "📄 PDF 다운로드",
        "upsell_msg": "⚡ 속도 향상? <a href='#' style='color:#FF4B4B'>VIP 업그레이드</a>",
        "export_title": "📦 내보내기",
        "download_zip": "💎 VIP 팩 (.zip)",
        "zip_desc": "✅ 엑셀 (CSV) + 텍스트",
        "download_txt": "📄 텍스트 (.txt)",
        "txt_desc": "🔒 엑셀? VIP 업그레이드.",
        "footer_rights": "© 2025 Cikgu Lai. All Rights Reserved.",
        "footer_disclaimer": "데이터는 즉시 삭제됩니다.",
        "faq_title": "📚 FAQ",
        "faq_content": "**Q: 이미지 생성?** A: 아니요, 프롬프트 생성입니다.\n**Q: 월구독?** A: 아니요! 평생 이용권.",
        "support_title": "💁 고객 센터",
        "support_ticket_label": "문의 티켓 제출.",
        "ticket_email": "이메일",
        "ticket_type": "유형",
        "ticket_desc": "설명",
        "ticket_btn": "🚀 제출",
        "ticket_success": "✅ 티켓 {id} 생성됨!"
    },
    "Spanish": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 Acceso VIP",
        "activation_code": "Código",
        "vip_active": "✅ VIP Activo",
        "vip_benefits": "⚡ Desbloquear: Velocidad, Lote 50, PDF",
        "free_limit_info": "🔓 Límite Gratis: {remaining}",
        "upgrade_btn": "🚀 Acceso de Por Vida",
        "limited_offer": "Oferta limitada.",
        "get_started": "📧 Empezar",
        "email_hint": "Email para activar.",
        "config": "⚙️ Configuración",
        "mode_label": "Modo:",
        "input_method_label": "Método:",
        "input_upload": "📷 Subir Imagen (Analizar)",
        "input_text": "✍️ Escribir Idea (Crear)",
        "text_area_label": "Escribe tu idea:",
        "lang_label": "Idioma Salida:",
        "style_vip_label": "🎨 Estilo (VIP):",
        "style_free_label": "🎨 Estilo (Gratis):",
        "style_lock_warning": "💎 Solo VIP.",
        "upload_label": "Subir (Máx {limit})",
        "email_warning": "🔒 Introduce email.",
        "generate_btn": "🚀 Generar",
        "daily_limit_error": "⛔ Límite alcanzado.",
        "credit_warning": "⚠️ Restan {count}.",
        "batch_warning": "⚠️ Límite {limit}.",
        "processing_vip": "⚡ **Velocidad VIP:** {current}/{total} ...",
        "processing_free": "⏳ **Cola:** {msg} ...",
        "complete": "✅ ¡Listo!",
        "clear_btn": "🗑️ Borrar",
        "copy_text": "📋 Copiar",
        "share_title": "🚀 Compartir:",
        "download_pdf": "📄 Bajar PDF",
        "upsell_msg": "⚡ ¿Más rápido? <a href='#' style='color:#FF4B4B'>Hazte VIP</a>",
        "export_title": "📦 Exportar",
        "download_zip": "💎 Pack VIP (.zip)",
        "zip_desc": "✅ Excel (CSV) + Texto",
        "download_txt": "📄 Texto (.txt)",
        "txt_desc": "🔒 ¿Excel? Hazte VIP.",
        "footer_rights": "© 2025 Cikgu Lai.",
        "footer_disclaimer": "Datos eliminados al instante.",
        "faq_title": "📚 FAQ",
        "faq_content": "**Q: ¿Crea imágenes?** A: No, crea Prompts.\n**Q: ¿Suscripción?** A: ¡No! Pago único.",
        "support_title": "💁 Ayuda",
        "support_ticket_label": "Enviar ticket.",
        "ticket_email": "Email",
        "ticket_type": "Tipo",
        "ticket_desc": "Descripción",
        "ticket_btn": "🚀 Enviar",
        "ticket_success": "✅ Ticket {id} creado!"
    },
    "French": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 Accès VIP",
        "activation_code": "Code",
        "vip_active": "✅ VIP Actif",
        "vip_benefits": "⚡ Vitesse, Lot 50, PDF",
        "free_limit_info": "🔓 Limite Gratuit: {remaining}",
        "upgrade_btn": "🚀 Accès à Vie",
        "limited_offer": "Offre limitée.",
        "get_started": "📧 Commencer",
        "email_hint": "Email pour activer.",
        "config": "⚙️ Config",
        "mode_label": "Mode:",
        "input_method_label": "Méthode:",
        "input_upload": "📷 Image (Analyser)",
        "input_text": "✍️ Texte (Créer)",
        "text_area_label": "Entrez votre idée:",
        "lang_label": "Langue Sortie:",
        "style_vip_label": "🎨 Style (VIP):",
        "style_free_label": "🎨 Style (Gratuit):",
        "style_lock_warning": "💎 Réservé aux VIP.",
        "upload_label": "Télécharger (Max {limit})",
        "email_warning": "🔒 Entrez votre email.",
        "generate_btn": "🚀 Générer",
        "daily_limit_error": "⛔ Limite atteinte.",
        "credit_warning": "⚠️ Reste {count}.",
        "batch_warning": "⚠️ Limite {limit}.",
        "processing_vip": "⚡ **VIP:** {current}/{total} ...",
        "processing_free": "⏳ **Attente:** {msg} ...",
        "complete": "✅ Terminé!",
        "clear_btn": "🗑️ Effacer",
        "copy_text": "📋 Copier",
        "share_title": "🚀 Partager:",
        "download_pdf": "📄 PDF",
        "upsell_msg": "⚡ Vitesse? <a href='#' style='color:#FF4B4B'>Passer VIP</a>",
        "export_title": "📦 Exporter",
        "download_zip": "💎 Pack VIP (.zip)",
        "zip_desc": "✅ Excel (CSV) + Texte",
        "download_txt": "📄 Texte (.txt)",
        "txt_desc": "🔒 Excel? Passer VIP.",
        "footer_rights": "© 2025 Cikgu Lai.",
        "footer_disclaimer": "Données supprimées instantanément.",
        "faq_title": "📚 FAQ",
        "faq_content": "**Q: Images?** A: Non, Prompts.\n**Q: Abonnement?** A: Non! Paiement unique.",
        "support_title": "💁 Aide",
        "support_ticket_label": "Ticket support.",
        "ticket_email": "Email",
        "ticket_type": "Type",
        "ticket_desc": "Description",
        "ticket_btn": "🚀 Envoyer",
        "ticket_success": "✅ Ticket {id} créé!"
    },
    "German": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 VIP-Zugang",
        "activation_code": "Code",
        "vip_active": "✅ VIP Aktiv",
        "vip_benefits": "⚡ Speed, 50/Batch, PDF",
        "free_limit_info": "🔓 Limit: {remaining}",
        "upgrade_btn": "🚀 Lebenslanger Zugang",
        "limited_offer": "Angebot.",
        "get_started": "📧 Starten",
        "email_hint": "E-Mail eingeben.",
        "config": "⚙️ Konfig",
        "mode_label": "Modus:",
        "input_method_label": "Methode:",
        "input_upload": "📷 Bild (Analyse)",
        "input_text": "✍️ Text (Erstellen)",
        "text_area_label": "Idee eingeben:",
        "lang_label": "Sprache:",
        "style_vip_label": "🎨 Stil (VIP):",
        "style_free_label": "🎨 Stil (Gratis):",
        "style_lock_warning": "💎 Nur VIP.",
        "upload_label": "Upload (Max {limit})",
        "email_warning": "🔒 E-Mail eingeben.",
        "generate_btn": "🚀 Start",
        "daily_limit_error": "⛔ Limit erreicht.",
        "credit_warning": "⚠️ Noch {count}.",
        "batch_warning": "⚠️ Limit {limit}.",
        "processing_vip": "⚡ **VIP:** {current}/{total} ...",
        "processing_free": "⏳ **Warten:** {msg} ...",
        "complete": "✅ Fertig!",
        "clear_btn": "🗑️ Löschen",
        "copy_text": "📋 Kopieren",
        "share_title": "🚀 Teilen:",
        "download_pdf": "📄 PDF",
        "upsell_msg": "⚡ Schneller? <a href='#' style='color:#FF4B4B'>VIP holen</a>",
        "export_title": "📦 Export",
        "download_zip": "💎 VIP Pack (.zip)",
        "zip_desc": "✅ Excel (CSV) + Text",
        "download_txt": "📄 Text (.txt)",
        "txt_desc": "🔒 Excel? VIP holen.",
        "footer_rights": "© 2025 Cikgu Lai.",
        "footer_disclaimer": "Daten werden gelöscht.",
        "faq_title": "📚 FAQ",
        "faq_content": "**Q: Bilder?** A: Nein, Prompts.\n**Q: Abo?** A: Nein! Einmalzahlung.",
        "support_title": "💁 Hilfe",
        "support_ticket_label": "Ticket senden.",
        "ticket_email": "E-Mail",
        "ticket_type": "Typ",
        "ticket_desc": "Beschreibung",
        "ticket_btn": "🚀 Senden",
        "ticket_success": "✅ Ticket {id} erstellt!"
    },
    "Portuguese": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 VIP",
        "activation_code": "Código",
        "vip_active": "✅ VIP Ativo",
        "vip_benefits": "⚡ Velocidade, Lote 50, PDF",
        "free_limit_info": "🔓 Limite: {remaining}",
        "upgrade_btn": "🚀 Acesso Vitalício",
        "limited_offer": "Oferta.",
        "get_started": "📧 Começar",
        "email_hint": "Email.",
        "config": "⚙️ Config",
        "mode_label": "Modo:",
        "input_method_label": "Método:",
        "input_upload": "📷 Imagem (Analise)",
        "input_text": "✍️ Texto (Criar)",
        "text_area_label": "Sua ideia:",
        "lang_label": "Idioma:",
        "style_vip_label": "🎨 Estilo (VIP):",
        "style_free_label": "🎨 Estilo (Grátis):",
        "style_lock_warning": "💎 Apenas VIP.",
        "upload_label": "Upload (Máx {limit})",
        "email_warning": "🔒 Digite email.",
        "generate_btn": "🚀 Gerar",
        "daily_limit_error": "⛔ Limite atingido.",
        "credit_warning": "⚠️ Restam {count}.",
        "batch_warning": "⚠️ Limite {limit}.",
        "processing_vip": "⚡ **VIP:** {current}/{total} ...",
        "processing_free": "⏳ **Fila:** {msg} ...",
        "complete": "✅ Feito!",
        "clear_btn": "🗑️ Limpar",
        "copy_text": "📋 Copiar",
        "share_title": "🚀 Partilhar:",
        "download_pdf": "📄 PDF",
        "upsell_msg": "⚡ Rápido? <a href='#' style='color:#FF4B4B'>Seja VIP</a>",
        "export_title": "📦 Exportar",
        "download_zip": "💎 Pack VIP (.zip)",
        "zip_desc": "✅ Excel (CSV) + Texto",
        "download_txt": "📄 Texto (.txt)",
        "txt_desc": "🔒 Excel? Seja VIP.",
        "footer_rights": "© 2025 Cikgu Lai.",
        "footer_disclaimer": "Dados apagados.",
        "faq_title": "📚 FAQ",
        "faq_content": "**Q: Imagens?** A: Não, Prompts.\n**Q: Assinatura?** A: Não! Pagamento único.",
        "support_title": "💁 Ajuda",
        "support_ticket_label": "Enviar ticket.",
        "ticket_email": "Email",
        "ticket_type": "Tipo",
        "ticket_desc": "Descrição",
        "ticket_btn": "🚀 Enviar",
        "ticket_success": "✅ Ticket {id} criado!"
    },
    "Russian": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 VIP",
        "activation_code": "Код",
        "vip_active": "✅ VIP Активен",
        "vip_benefits": "⚡ Скорость, Пакет 50, PDF",
        "free_limit_info": "🔓 Лимит: {remaining}",
        "upgrade_btn": "🚀 Вечный доступ",
        "limited_offer": "Акция.",
        "get_started": "📧 Начать",
        "email_hint": "Email.",
        "config": "⚙️ Настройки",
        "mode_label": "Режим:",
        "input_method_label": "Метод:",
        "input_upload": "📷 Фото (Анализ)",
        "input_text": "✍️ Текст (Создать)",
        "text_area_label": "Ваша идея:",
        "lang_label": "Язык:",
        "style_vip_label": "🎨 Стиль (VIP):",
        "style_free_label": "🎨 Стиль (Беспл):",
        "style_lock_warning": "💎 Только VIP.",
        "upload_label": "Загрузка (Макс {limit})",
        "email_warning": "🔒 Введите email.",
        "generate_btn": "🚀 Создать",
        "daily_limit_error": "⛔ Лимит.",
        "credit_warning": "⚠️ Осталось {count}.",
        "batch_warning": "⚠️ Лимит {limit}.",
        "processing_vip": "⚡ **VIP:** {current}/{total} ...",
        "processing_free": "⏳ **Очередь:** {msg} ...",
        "complete": "✅ Готово!",
        "clear_btn": "🗑️ Очистить",
        "copy_text": "📋 Копировать",
        "share_title": "🚀 Поделиться:",
        "download_pdf": "📄 Скачать PDF",
        "upsell_msg": "⚡ Быстро? <a href='#' style='color:#FF4B4B'>Купите VIP</a>",
        "export_title": "📦 Экспорт",
        "download_zip": "💎 VIP Пакет (.zip)",
        "zip_desc": "✅ Excel (CSV) + Текст",
        "download_txt": "📄 Текст (.txt)",
        "txt_desc": "🔒 Excel? Купите VIP.",
        "footer_rights": "© 2025 Cikgu Lai.",
        "footer_disclaimer": "Данные удаляются.",
        "faq_title": "📚 FAQ",
        "faq_content": "**Q: Картинки?** A: Нет, Промпты.\n**Q: Подписка?** A: Нет! Разово.",
        "support_title": "💁 Помощь",
        "support_ticket_label": "Отправить тикет.",
        "ticket_email": "Email",
        "ticket_type": "Тип",
        "ticket_desc": "Описание",
        "ticket_btn": "🚀 Отправить",
        "ticket_success": "✅ Тикет {id} создан!"
    },
    "Arabic": {
        "app_title": "VisionPrompter AI",
        "vip_access": "💎 VIP",
        "activation_code": "رمز",
        "vip_active": "✅ VIP مفعل",
        "vip_benefits": "⚡ سرعة، 50/دفعة، PDF",
        "free_limit_info": "🔓 حد مجاني: {remaining}",
        "upgrade_btn": "🚀 وصول مدى الحياة",
        "limited_offer": "عرض محدود.",
        "get_started": "📧 ابدأ",
        "email_hint": "البريد الإلكتروني.",
        "config": "⚙️ إعدادات",
        "mode_label": "الوضع:",
        "input_method_label": "طريقة:",
        "input_upload": "📷 رفع صورة (تحليل)",
        "input_text": "✍️ كتابة فكرة (إنشاء)",
        "text_area_label": "أدخل فكرتك:",
        "lang_label": "لغة:",
        "style_vip_label": "🎨 نمط (VIP):",
        "style_free_label": "🎨 نمط (مجاني):",
        "style_lock_warning": "💎 لـ VIP فقط.",
        "upload_label": "رفع (حد أقصى {limit})",
        "email_warning": "🔒 أدخل البريد.",
        "generate_btn": "🚀 إنشاء",
        "daily_limit_error": "⛔ حد يومي.",
        "credit_warning": "⚠️ بقي {count}.",
        "batch_warning": "⚠️ حد {limit}.",
        "processing_vip": "⚡ **VIP:** {current}/{total} ...",
        "processing_free": "⏳ **طابور:** {msg} ...",
        "complete": "✅ تم!",
        "clear_btn": "🗑️ مسح",
        "copy_text": "📋 نسخ",
        "share_title": "🚀 مشاركة:",
        "download_pdf": "📄 تحميل PDF",
        "upsell_msg": "⚡ سرعة؟ <a href='#' style='color:#FF4B4B'>ترقية VIP</a>",
        "export_title": "📦 تصدير",
        "download_zip": "💎 حزمة VIP (.zip)",
        "zip_desc": "✅ Excel (CSV) + نص",
        "download_txt": "📄 نص (.txt)",
        "txt_desc": "🔒 Excel؟ ترقية VIP.",
        "footer_rights": "© 2025 Cikgu Lai.",
        "footer_disclaimer": "بيانات محذوفة.",
        "faq_title": "📚 أسئلة",
        "faq_content": "**س: صور؟** ج: لا، نصوص.\n**س: اشتراك؟** ج: لا! مرة واحدة.",
        "support_title": "💁 مساعدة",
        "support_ticket_label": "إرسال تذكرة.",
        "ticket_email": "بريد",
        "ticket_type": "نوع",
        "ticket_desc": "وصف",
        "ticket_btn": "🚀 إرسال",
        "ticket_success": "✅ تذكرة {id} تم إنشاؤها!"
    }
}

def get_text(t, key):
    """安全获取翻译，缺失则回退到英文"""
    return t.get(key, TRANSLATIONS["English"].get(key, key))

# ==========================================
# 2. 系统配置
# ==========================================
st.set_page_config(
    page_title="VisionPrompter AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'results' not in st.session_state: st.session_state['results'] = []
if 'usage_count' not in st.session_state: st.session_state['usage_count'] = 0 
if 'user_email' not in st.session_state: st.session_state['user_email'] = ""

# 检查 API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Critical: GOOGLE_API_KEY missing in Secrets.")
    st.stop()
api_key = st.secrets["GOOGLE_API_KEY"]

# CSS 美化
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom, #ffffff, #f8f9fa); font-family: 'Inter', sans-serif; }
    .result-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .share-btn { display: inline-block; padding: 6px 12px; border-radius: 4px; color: white !important; text-decoration: none !important; margin-right: 6px; margin-bottom: 6px; font-size: 0.8em; font-weight: bold; transition: opacity 0.3s; }
    .share-btn:hover { opacity: 0.8; }
    .btn-wa { background-color: #25D366; } .btn-fb { background-color: #1877F2; } .btn-tw { background-color: #000000; }
    .btn-li { background-color: #0077b5; } .btn-ig { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); }
    .btn-tt { background-color: #000000; border: 1px solid #333; } .btn-xhs { background-color: #FF2442; }
    .delay-msg { color: #f59e0b; font-size: 0.9em; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# === 📨 Telegram 通知函数 ===
def send_telegram_msg(name, email, msg):
    if "telegram" in st.secrets:
        token = st.secrets["telegram"]["token"]
        chat_id = st.secrets["telegram"]["chat_id"]
        text = f"🔔 **Notification**\n\n👤 **User:** {name}\n📧 **Email:** {email}\n💬 **Content:**\n{msg}"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
        except:
            pass

# === 📄 PDF 生成函数 (含权益署名) ===
def create_pdf(image, text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 标题
    pdf.cell(200, 10, txt=f"VisionPrompter: {filename}", ln=1, align='C')
    pdf.ln(10)
    
    # 图片
    if image:
        try:
            with io.BytesIO() as output:
                image.save(output, format="JPEG")
                pdf.image(output, x=10, y=30, w=190)
                pdf.ln(110)
        except:
            pdf.cell(200, 10, txt="[Image Error]", ln=1)
    
    # 正文
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, safe_text)
    
    # === 👑 Footer: Personal Branding ===
    pdf.ln(20)
    pdf.set_draw_color(200, 200, 200) # Grey line
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", size=9, style='I')
    pdf.set_text_color(100, 100, 100)
    
    # 自动获取用户身份
    user_identity = "Cikgu Lai AI Class"
    if 'user_email' in st.session_state and st.session_state['user_email']:
        user_identity = st.session_state['user_email']
    
    footer_text = f"Generated with VisionPrompter | Prepared for: {user_identity}"
    pdf.cell(0, 10, txt=footer_text, ln=1, align='R')
    # ====================================
    
    return pdf.output(dest='S').encode('latin-1')

def generate_share_links(text, url="https://app.cikgulai.com"):
    safe_text = urllib.parse.quote(text[:200] + "...") 
    safe_url = urllib.parse.quote(url)
    links = {
        "wa": f"https://wa.me/?text={safe_text} {safe_url}",
        "fb": f"https://www.facebook.com/sharer/sharer.php?u={safe_url}",
        "tw": f"https://twitter.com/intent/tweet?text={safe_text}&url={safe_url}",
        "li": f"https://www.linkedin.com/sharing/share-offsite/?url={safe_url}",
        "ig": "https://www.instagram.com/",
        "tt": "https://www.tiktok.com/upload",
        "xhs": "https://www.xiaohongshu.com/explore"
    }
    return links

# === 🧠 核心 AI 逻辑 (含双模引擎 + VIP增强) ===
def build_prompt(mode, language, style_modifier, is_vip, input_type="image"):
    style_recipes = {
        "📝 Detailed (More Words)": "highly detailed description, verbose, analyze every element, focus on textures and lighting",
        "⚡ Concise (Short)": "concise description, brief, to the point, short keywords only",
        "🖍️ Coloring Book (Line Art)": "coloring book page, black and white, clean lines, no shading, white background, thick outlines, vector style",
        "🧱 Claymation (Cute 3D)": "claymation style, plasticine texture, stop motion, soft lighting, 3d render, cute, miniature world, tilt-shift",
        "🎬 Pixar/Disney 3D": "Pixar style 3d render, unreal engine 5, cgsociety, disney animation style, expressive characters, cinematic lighting",
        "✨ Anime / Studio Ghibli": "Studio Ghibli style, anime, hayao miyazaki, pastel colors, cel shaded, breathtaking sky, detailed background",
        "📸 Hyper-Realistic Photo": "hyper-realistic photography, 8k resolution, raw photo, highly detailed, dslr, cinematic lighting, sharp focus",
        "🔳 Vector Flat Art": "flat vector art, minimal, clean geometric shapes, adobe illustrator, white background, corporate art style",
        "🌃 Cyberpunk / Neon": "cyberpunk, neon lights, night city, futuristic, synthwave, purple and blue gradient, cinematic",
        "📜 Vintage Watercolor": "vintage watercolor illustration, beatrix potter style, soft strokes, paper texture, dreamy, storybook"
    }

    vip_negative_prompt = "low quality, ugly, deformed, blurry, extra fingers, bad anatomy, watermark, text, signature, cropped"
    vip_quality_boost = "masterpiece, best quality, 8k resolution, highly detailed, sharp focus, cinematic lighting"

    added_prompt = ""
    if style_modifier and "None" not in style_modifier and "Lock" not in style_modifier:
        recipe = style_recipes.get(style_modifier, "")
        if recipe: added_prompt = f", {recipe}"

    # === Mode Logic ===
    if mode == "Prompt Gacha":
        if input_type == "text":
            if is_vip:
                return f"""
                You are an elite AI art director.
                Task: Turn the user's simple idea into a World-Class Stable Diffusion prompt.
                User Idea: {{INPUT}}
                Target Style: {added_prompt if added_prompt else "high quality"}
                Action:
                1. EXPAND the idea creatively.
                2. INTEGRATE the target style perfectly.
                3. APPEND these quality boosters: "{vip_quality_boost}".
                Output Format:
                Combine into a single raw prompt string.
                At the very end, append: " --no {vip_negative_prompt}"
                """
            else:
                return f"""
                You are a translator.
                Task: Translate the user's idea into a simple English prompt for AI generation.
                User Idea: {{INPUT}}
                Target Style: {added_prompt if added_prompt else "standard"}
                Output Format:
                Single raw prompt string.
                """
        else:
            base = """
            You are an expert AI art prompter. Analyze the image and reverse-engineer it into a Stable Diffusion prompt.
            Strictly output the prompt in these 4 distinct sections (comma separated, English Only):
            1. **Subject**: (Character, object, action)
            2. **Style**: (Art style, medium)
            3. **Environment**: (Background, lighting)
            4. **Quality**: (Tags e.g., masterpiece)
            """
            if added_prompt: base += f" INTEGRATE this style: '{added_prompt}'. "
            base += "Format: Combine into a single raw prompt string."
            if is_vip: base += f" Append ' --no {vip_negative_prompt}' at the end."
            return base

    elif mode == "Storyteller":
        style_instruction = f"Visual Style: {style_modifier}" if style_modifier else "Style: Warm"
        return f"""
        Task: Write a creative children's story in {language} based on the input (300 words).
        Structure: 1. Title 2. Story 3. Moral 4. 🎨 **AI Drawing Prompt**: Create a prompt to generate an illustration for this story in {style_modifier} style.
        Tone: {style_instruction}.
        Input: {{INPUT}}
        """

    elif mode == "Social Kit":
        return f"""
        Write a viral social post in {language} based on the input. 
        Structure: Hook, Content, 15+ Hashtags. 
        Tone/Style: {style_modifier}.
        Input: {{INPUT}}
        """
    return "Describe input."

def process_and_save(inputs, mode, output_lang, style, is_vip, ui_text, input_type):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    loading_messages = ["AI is dreaming...", "Analyzing...", "Extracting magic...", "Polishing words..."]

    progress_bar = st.progress(0)
    status_text = st.empty()
    total_items = len(inputs)

    for i, item in enumerate(inputs):
        if is_vip:
            msg = get_text(ui_text, "processing_vip").format(current=i+1, total=total_items)
            status_text.markdown(msg)
            time.sleep(1.0)
        else:
            rand_msg = random.choice(loading_messages)
            msg = get_text(ui_text, "processing_free").format(msg=rand_msg)
            status_text.markdown(msg)
            time.sleep(1.5)

        try:
            base_prompt = build_prompt(mode, output_lang, style, is_vip, input_type)
            if input_type == "text":
                final_prompt = base_prompt.replace("{{INPUT}}", item)
                response = model.generate_content(final_prompt)
                filename = f"Idea_{str(int(time.time()))}_{i}" 
                img_obj = None 
            else:
                img_obj = Image.open(item)
                response = model.generate_content([base_prompt, img_obj])
                filename = item.name

            content = response.text
            if "block" in str(content).lower(): content = "⚠️ Safety Block: Content filtered."
                
            st.session_state['results'].append({
                "filename": filename, "content": content, "image": img_obj, "mode": mode
            })
            if not is_vip: st.session_state['usage_count'] += 1
                
        except Exception as e:
            st.error(f"Error: {e}")
            
        progress_bar.progress((i + 1) / total_items)

    time.sleep(0.5)
    progress_bar.progress(100)
    status_text.success(get_text(ui_text, "complete"))
    time.sleep(1)
    status_text.empty()
    
    # 📊 静默监控
    try:
        log_user = st.session_state.get('user_email', 'Anonymous')
        if is_vip: log_user += " (VIP)"
        log_msg = f"🚀 **Usage**\n👤 {log_user}\n⚙️ {mode}\n📄 {len(inputs)} Items"
        if len(inputs) > 1 or is_vip:
            send_telegram_msg("System", log_user, log_msg)
    except:
        pass

# ==========================================
# 4. 侧边栏 (Sidebar)
# ==========================================
with st.sidebar:
    lang_list = list(TRANSLATIONS.keys())
    ui_lang = st.selectbox("🌐 Interface Language", lang_list, index=0)
    t = TRANSLATIONS.get(ui_lang, TRANSLATIONS["English"])

    st.markdown(f"## 🔮 {get_text(t, 'app_title')}")
    
    with st.expander(get_text(t, 'vip_access'), expanded=True):
        vip_code = st.text_input(get_text(t, 'activation_code'), type="password")
        
        # === 🛡️ Soft Security Warning ===
        st.markdown("""
        <div style="font-size: 0.75em; color: #555; background-color: #e2e3e5; padding: 8px; border-radius: 5px; margin-bottom: 10px;">
            🛡️ <b>Secure Session:</b> This workspace is personalized for you. Concurrent logins from multiple locations may trigger a temporary security lock.
        </div>
        """, unsafe_allow_html=True)
        # ================================
        
        if vip_code: vip_code = vip_code.strip()
        is_vip = vip_code in st.secrets.get("MANUAL_CODES", ["demo"])
        
        daily_limit = 200 if is_vip else 3
        remaining = daily_limit - st.session_state['usage_count']
        if remaining < 0: remaining = 0
        
        if is_vip:
            st.success(get_text(t, 'vip_active'))
            st.caption(f"📊 {st.session_state['usage_count']} / {daily_limit}")
        else:
            st.info(get_text(t, 'free_limit_info').format(remaining=remaining))
            st.markdown("""
            <div style="text-align: center; margin-bottom: 10px;">
                <span style="text-decoration: line-through; color: #888; font-size: 0.9em;">$39.90</span>
                <span style="color: #FF4B4B; font-weight: bold; font-size: 1.2em; margin-left: 5px;">$12.90</span>
            </div>
            """, unsafe_allow_html=True)
            # ⚠️ 请确保这里的链接换成您的真实支付链接
            buy_url = "https://your-shop.lemonsqueezy.com/buy/xxxx" 
            st.markdown(f"""
            <a href="{buy_url}" target="_blank">
                <button style="width:100%; background: linear-gradient(90deg, #FF4B4B 0%, #FF6B6B 100%); color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">
                    {get_text(t, 'upgrade_btn')}
                </button>
            </a>
            <p style="text-align:center; font-size:0.7em; color:#666; margin-top:5px;">{get_text(t, 'limited_offer')}</p>
            """, unsafe_allow_html=True)
            st.caption(get_text(t, 'vip_benefits'))

    st.markdown("---")
    
    if not is_vip:
        st.markdown(f"### {get_text(t, 'get_started')}")
        st.caption(get_text(t, 'email_hint'))
        email = st.text_input("Email", value=st.session_state['user_email'])
        if email: st.session_state['user_email'] = email
        
    st.markdown(f"### {get_text(t, 'config')}")
    
    # 🔄 Dual-Mode Input
    input_method = st.radio(get_text(t, "input_method_label"), ["upload", "text"], 
                            format_func=lambda x: get_text(t, "input_upload") if x == "upload" else get_text(t, "input_text"))

    mode = st.radio(get_text(t, 'mode_label'), ["Prompt Gacha", "Storyteller", "Social Kit"])
    output_lang = st.selectbox(get_text(t, 'lang_label'), lang_list, index=0)
    
    style_modifier = None
    if is_vip:
        style_options = [
            "None (Default)",
            "🖍️ Coloring Book (Line Art)",
            "🧱 Claymation (Cute 3D)",
            "🎬 Pixar/Disney 3D",
            "✨ Anime / Studio Ghibli",
            "📸 Hyper-Realistic Photo",
            "🔳 Vector Flat Art",
            "🌃 Cyberpunk / Neon",
            "📜 Vintage Watercolor"
        ]
        style_modifier = st.selectbox(get_text(t, 'style_vip_label'), style_options)
    else:
        style_options_free = [
            "None (Default)",
            "📝 Detailed (More Words)",
            "⚡ Concise (Short)",
            "🔒 Unlock 8+ Pro Styles (VIP Only)"
        ]
        style_modifier = st.selectbox(get_text(t, 'style_free_label'), style_options_free)
        if "Lock" in style_modifier:
            st.warning(get_text(t, 'style_lock_warning'))
            style_modifier = "None (Default)"

    with st.expander(get_text(t, 'faq_title')):
        st.markdown(get_text(t, 'faq_content'))
    
    # === 💼 Enterprise Ticket System ===
    st.markdown("---")
    with st.expander(get_text(t, "support_title"), expanded=False):
        st.caption(get_text(t, "support_ticket_label"))
        with st.form(key="support_ticket_form"):
            current_email = st.session_state.get('user_email', "")
            user_email_input = st.text_input(get_text(t, "ticket_email"), value=current_email)
            issue_type = st.selectbox(get_text(t, "ticket_type"), [
                "🐛 Bug Report", "💳 Billing/Payment", "💡 Feature Request", "🤝 Partnership", "Other"
            ])
            user_msg = st.text_area(get_text(t, "ticket_desc"), height=100)
            submit_btn = st.form_submit_button(get_text(t, "ticket_btn"))
            
            if submit_btn:
                if user_email_input and user_msg:
                    ticket_id = f"#{random.randint(10000, 99999)}"
                    st.success(get_text(t, "ticket_success").format(id=ticket_id))
                    full_msg = f"📌 **Type:** {issue_type}\n🎫 **Ticket:** {ticket_id}\n📝 **Content:** {user_msg}"
                    send_telegram_msg("User", user_email_input, full_msg)
                else:
                    st.error("Please provide Email and Description.")

# ==========================================
# 5. 主界面
# ==========================================
st.title(f"🔮 {mode}")

batch_limit = 50 if is_vip else 3
passed_gate = is_vip or (st.session_state['user_email'] != "")

inputs = []
input_type = "image"

if st.session_state['usage_count'] >= daily_limit:
    st.error(get_text(t, 'daily_limit_error').format(current=st.session_state['usage_count'], total=daily_limit))
else:
    if input_method == "upload":
        label = get_text(t, 'upload_label').format(limit=batch_limit)
        uploaded_files = st.file_uploader(label, type=["jpg","png","webp"], accept_multiple_files=True)
        if uploaded_files: inputs = uploaded_files
        input_type = "image"
    else:
        user_text = st.text_area(get_text(t, "text_area_label"), height=150)
        if user_text: inputs = [user_text] 
        input_type = "text"

if inputs:
    if not passed_gate:
        st.warning(get_text(t, 'email_warning'))
    else:
        if st.button(get_text(t, 'generate_btn')):
            potential_usage = st.session_state['usage_count'] + len(inputs)
            if potential_usage > daily_limit:
                allowed_count = daily_limit - st.session_state['usage_count']
                st.warning(get_text(t, 'credit_warning').format(count=allowed_count))
                inputs = inputs[:allowed_count]
            elif len(inputs) > batch_limit:
                st.warning(get_text(t, 'batch_warning').format(limit=batch_limit))
                inputs = inputs[:batch_limit]
            
            # Anti-Refresh Warning
            st.caption("⚠️ Please do not refresh the page, or you will lose the results!")
            process_and_save(inputs, mode, output_lang, style_modifier, is_vip, t, input_type)
            st.rerun()

# ==========================================
# 6. 结果展示
# ==========================================
if st.session_state['results']:
    st.markdown("---")
    if st.button(get_text(t, 'clear_btn')):
        st.session_state['results'] = []
        st.rerun()

    for item in reversed(st.session_state['results']):
        c = item['content']
        n = item['filename']
        m = item['mode']
        img = item['image']
        
        with st.container():
            st.markdown(f"<div class='result-card'>", unsafe_allow_html=True)
            cols = st.columns([1, 3])
            
            with cols[0]:
                if img:
                    st.image(img, use_container_width=True)
                else:
                    st.markdown("## ✍️ Idea")
                    st.info(n.split('_')[-1] if '_' in n else "Text")
                st.caption(n)
            
            with cols[1]:
                if m == "Prompt Gacha": 
                    st.code(c, language="markdown")
                else: 
                    st.markdown(c)
                    with st.expander(get_text(t, 'copy_text')):
                        st.code(c, language=None)
                
                if is_vip:
                    st.markdown("---")
                    if m == "Social Kit":
                        links = generate_share_links(c)
                        st.caption(get_text(t, 'share_title'))
                        st.markdown(f"""
                        <a href='{links['wa']}' target='_blank' class='share-btn btn-wa'>WhatsApp</a>
                        <a href='{links['fb']}' target='_blank' class='share-btn btn-fb'>Facebook</a>
                        <a href='{links['tw']}' target='_blank' class='share-btn btn-tw'>X (Twitter)</a>
                        <a href='{links['li']}' target='_blank' class='share-btn btn-li'>LinkedIn</a>
                        <br>
                        <a href='{links['ig']}' target='_blank' class='share-btn btn-ig'>Instagram</a>
                        <a href='{links['tt']}' target='_blank' class='share-btn btn-tt'>TikTok</a>
                        <a href='{links['xhs']}' target='_blank' class='share-btn btn-xhs'>RedNote</a>
                        """, unsafe_allow_html=True)
                    
                    if m == "Storyteller":
                        pdf = create_pdf(img, c, n)
                        st.download_button(get_text(t, 'download_pdf'), pdf, f"{n}.pdf", "application/pdf")
                else:
                    st.markdown("---")
                    st.markdown(f"<p class='delay-msg'>{get_text(t, 'upsell_msg')}</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(get_text(t, 'export_title'))
    
    txt_buffer = ""
    csv_buffer = "Filename,Mode,Content\n"
    
    for item in st.session_state['results']:
        n = item['filename']
        c = item['content'].replace('"', '""')
        m = item['mode']
        txt_buffer += f"=== [{m}] {n} ===\n{item['content']}\n\n"
        csv_buffer += f'"{n}","{m}","{c}"\n'

    col1, col2 = st.columns([1, 1])

    if is_vip:
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w") as zf:
            zf.writestr("all_results.txt", txt_buffer)
            zf.writestr("export_data.csv", csv_buffer)
        
        col1.download_button(
            get_text(t, 'download_zip'),
            zip_buf.getvalue(),
            "visionprompter_vip.zip",
            "application/zip",
            use_container_width=True,
            type="primary"
        )
        col1.caption(get_text(t, 'zip_desc'))
    else:
        col1.download_button(
            get_text(t, 'download_txt'),
            txt_buffer,
            "results.txt",
            "text/plain",
            use_container_width=True
        )
        col1.caption(get_text(t, 'txt_desc'))

# ==========================================
# 7. 最终底部 (Footer)
# ==========================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #aaa; font-size: 0.8em; line-height: 1.5;">
    <b>{get_text(t, 'footer_rights')}</b><br>
    {get_text(t, 'footer_disclaimer')}<br>
    <span style="font-size: 0.8em; opacity: 0.6; font-family: monospace;">System Version: v2.5 (International Edition)</span>
</div>

""", unsafe_allow_html=True)
