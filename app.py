import streamlit as st
import time
import re
import google.generativeai as genai
from fpdf import FPDF
import pandas as pd
from io import StringIO

# ==============================================================================
# 1. 系统配置 & CSS
# ==============================================================================
st.set_page_config(
    page_title="Lai's Lab AI",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

VERSION = "V7.0 (Flagship Architecture)"

# 15 国语言支持
ALL_LANGS = [
    "English", "简体中文", "Bahasa Melayu", "Tamil (தமிழ்)", "Japanese (日本語)", 
    "Korean (한국어)", "Thai (ไทย)", "Vietnamese (Tiếng Việt)", "Indonesian (Bahasa Indonesia)",
    "French (Français)", "German (Deutsch)", "Spanish (Español)", "Russian (Русский)", 
    "Arabic (العربية)", "Portuguese (Português)"
]

def inject_custom_css():
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        body { font-family: 'Inter', sans-serif; }
        .stButton>button {
            background-color: #1A73E8; color: white; border-radius: 8px; border: none;
            padding: 10px 24px; font-weight: 600; transition: all 0.3s;
        }
        .stButton>button:hover { background-color: #1557B0; }
        .output-card {
            background-color: #fdfdfd; border: 1px solid #e0e0e0; border-radius: 8px;
            padding: 25px; margin-top: 20px; line-height: 1.6; color: #333;
            white-space: pre-wrap;
        }
        .custom-footer {
            position: fixed; left: 0; bottom: 0; width: 100%;
            background-color: #f8f9fa; color: #5f6368; text-align: center;
            padding: 12px; font-size: 0.75rem; border-top: 1px solid #e0e0e0; z-index: 999;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==============================================================================
# 2. AI 连接
# ==============================================================================
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("🚨 Missing GOOGLE_API_KEY in Secrets!")
except Exception as e:
    st.error(f"AI Connection Error: {e}")

# ==============================================================================
# 3. 核心工具：清洗、PDF (带字体修复)、CSV
# ==============================================================================
def clean_text(text, keep_emojis=True):
    # 去除 Markdown 标记
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text) # Bold
    text = re.sub(r'#+\s*', '', text) # Headers
    text = re.sub(r'^\*\s', '• ', text, flags=re.MULTILINE) # List
    if not keep_emojis:
        text = text.encode('ascii', 'ignore').decode('ascii')
    return text.strip()

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # [Step 1 修复] 尝试加载中文字体 font.ttf
    font_path = "font.ttf"
    try:
        # 注册字体 (必须存在 font.ttf 否则报错)
        pdf.add_font('CustomFont', '', font_path, uni=True)
        pdf.set_font("CustomFont", size=11)
    except:
        # 失败回退到 Arial (不支持中文)
        pdf.set_font("Arial", size=11)
        text = clean_text(text, keep_emojis=False) # 强制去Emoji和中文防止报错
        text += "\n\n[System Note: 'font.ttf' not found. Chinese characters may be missing.]"

    # 清洗内容 (PDF 永远去 Emoji，防止乱码)
    clean_content = clean_text(text, keep_emojis=False)
    
    pdf.set_font_size(14)
    pdf.cell(0, 10, "Lai's Lab Output", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font_size(11)
    pdf.multi_cell(0, 8, clean_content)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

def extract_csv(text):
    # 简单的逻辑：检查是否有 Markdown 表格符号
    if "|" in text and text.count("|") > 4:
        try:
            # 提取表格部分 (简化版逻辑)
            lines = text.split('\n')
            table_lines = [line for line in lines if '|' in line]
            csv_data = "\n".join(table_lines)
            return csv_data
        except:
            return None
    return None

# ==============================================================================
# 4. 状态管理
# ==============================================================================
if 'user_type' not in st.session_state: st.session_state['user_type'] = 'Free'
if 'usage_count' not in st.session_state: st.session_state['usage_count'] = 0
if 'last_generate_time' not in st.session_state: st.session_state['last_generate_time'] = 0

def get_text(lang, key):
    db = {
        "sidebar_identity": {"en": "Identity", "zh": "身份选择", "ms": "Identiti"},
        "sidebar_vip": {"en": "Membership", "zh": "会员中心", "ms": "Keahlian"},
        "btn_gen": {"en": "✨ Generate", "zh": "✨ 立即生成", "ms": "✨ Jana"},
        "limit_msg": {"en": "Daily Limit Reached", "zh": "今日额度已用完", "ms": "Had Harian Dicapai"},
        "cooldown_msg": {"en": "Cooling down...", "zh": "系统冷却中...", "ms": "Sistem sedang rehat..."},
    }
    code = "en"
    if "中文" in lang: code = "zh"
    elif "Melayu" in lang: code = "ms"
    return db.get(key, {}).get(code, db[key]["en"])

# ==============================================================================
# 5. 侧边栏 (Sidebar)
# ==============================================================================
with st.sidebar:
    try: st.image("logo.png", use_container_width=True)
    except: st.title("Lai's Lab")
    st.markdown("---")
    current_lang = st.selectbox("🌐 Language", ALL_LANGS, index=0)
    
    st.markdown(f"### 👤 {get_text(current_lang, 'sidebar_identity')}")
    # [Step 2 超级逻辑] 6 大群体
    role_map = {
        "👨‍🏫 Educator (老师)": "Educator",
        "🎥 Creator (创作者)": "Creator",
        "💰 Seller (电商)": "Seller",
        "👪 Parent (父母)": "Parent",
        "🎓 Student (学生)": "Student",
        "💼 Corporate (职场)": "Corporate"
    }
    selected_role_display = st.selectbox("Role", list(role_map.keys()), label_visibility="collapsed")
    selected_role = role_map[selected_role_display]
    
    st.markdown(f"### 💎 {get_text(current_lang, 'sidebar_vip')}")
    if st.session_state['user_type'] == 'Free':
        st.progress(st.session_state['usage_count'] / 3, text=f"Daily Limit: {3-st.session_state['usage_count']}/3")
        with st.expander("🔑 Activate"):
            if st.button("Activate Pro"): st.session_state['user_type'] = 'Pro'; st.rerun()
    else:
        st.success("👑 Lai's Lab VIP")

# ==============================================================================
# 6. 超级逻辑：策略下拉菜单构建 (The Matrix)
# ==============================================================================

# 定义每个身份的细分模式 (Modes) 和 策略 (Strategies)
UI_CONFIG = {
    "Educator": {
        "modes": ["Pedagogical Content", "Visual Aids", "Global Comm"],
        "strategies": {
            "Pedagogical Content": ["🧠 STEM Simplification", "❤️ SEL (Social Emotional)", "🤔 Critical Thinking", "🧊 Ice Breaker"],
            "Visual Aids": ["🖍️ Coloring Page", "🎴 Flashcard Style", "🎨 Flat Illustration", "📊 Diagram"],
            "Global Comm": ["🔔 Parent Notice", "📢 Professional Brand", "👔 Formal Email"]
        }
    },
    "Creator": {
        "modes": ["Scripting", "Visual Packaging", "Engagement"],
        "strategies": {
            "Scripting": ["🪝 Viral Hook (0-3s)", "🦸 Hero's Journey", "📦 Product Review", "🎓 Listicle"],
            "Visual Packaging": ["🔥 High CTR", "✨ Cinematic", "🎨 Minimalist", "👾 Cyberpunk"],
            "Engagement": ["❓ Curiosity Gap", "😱 Fear/FOMO", "🤝 Relatability", "🏆 Value/Tips"]
        }
    },
    # (篇幅限制，这里预留其他4个群体，您可以先测这2个核心，逻辑通了再加)
    "Seller": {"modes": ["Listing Copy", "Ad Visuals", "CS Reply"], "strategies": {}},
    "Parent": {"modes": ["Story Weaver", "Activity Planner", "Advice"], "strategies": {}},
    "Student": {"modes": ["Study Notes", "Writing Coach", "Concept Viz"], "strategies": {}},
    "Corporate": {"modes": ["Pro Email", "Report Smith", "Presentation"], "strategies": {}}
}

# ==============================================================================
# 7. 主工作台 (Workspace)
# ==============================================================================
st.markdown("---")
output_lang = st.selectbox("🗣️ Output Language", ["Same as Interface"] + ALL_LANGS)
target_lang = current_lang if output_lang == "Same as Interface" else output_lang

# 获取当前身份的 Tabs
current_config = UI_CONFIG.get(selected_role, {})
tabs = current_config.get("modes", ["General Mode"])
selected_tab_index = 0

# 渲染 Tabs
tab_objects = st.tabs(tabs)

for idx, tab_obj in enumerate(tab_objects):
    with tab_obj:
        mode_name = tabs[idx]
        st.markdown(f"#### {mode_name}")
        
        # [Step 2] 动态渲染策略下拉菜单
        strategies = current_config.get("strategies", {}).get(mode_name, [])
        selected_strategy = "Default"
        if strategies:
            selected_strategy = st.selectbox(f"⚙️ Strategy for {mode_name}", strategies, key=f"strat_{selected_role}_{mode_name}")
        
        # 视觉/比例选项 (仅在 Visual 模式出现)
        if "Visual" in mode_name:
            ratio = st.selectbox("📐 Aspect Ratio", ["16:9 (Slide/Video)", "1:1 (Square)", "9:16 (Mobile)"], key=f"ratio_{mode_name}")
            
        # 社交平台选项 (仅在 Engagement/Seller 模式出现)
        platform = "General"
        if "Engagement" in mode_name or "Seller" in selected_role:
            platform = st.selectbox("📱 Platform", ["YouTube", "TikTok", "Instagram", "LinkedIn", "Shopee"], key=f"plat_{mode_name}")

        # 输入区
        uploaded_file = st.file_uploader(f"📸 Upload Image", type=['png','jpg'], key=f"up_{mode_name}")
        user_input = st.text_area(f"✍️ Input Context for {mode_name}", height=120, key=f"in_{mode_name}")
        
        # 生成按钮
        if st.button(f"✨ Generate {mode_name}", key=f"btn_{mode_name}"):
            # 限制检查
            if st.session_state['user_type'] == 'Free' and st.session_state['usage_count'] >= 3:
                st.error(get_text(current_lang, 'limit_msg'))
            else:
                with st.spinner("🧪 Lai's Lab is optimizing..."):
                    # [Step 2] 构建超级 Prompt
                    full_prompt = f"""
                    Role: {selected_role}
                    Mode: {mode_name}
                    Strategy: {selected_strategy}
                    Platform: {platform}
                    Target Language: {target_lang}
                    Input: {user_input}
                    
                    Instruction: Write content strictly following the selected strategy. 
                    Make it human-like, professional, and impactful.
                    """
                    
                    try:
                        if uploaded_file:
                            img = Image.open(uploaded_file)
                            response = model.generate_content([full_prompt, img])
                        else:
                            response = model.generate_content(full_prompt)
                        
                        raw_result = response.text
                        st.session_state[f'res_{mode_name}'] = raw_result
                        
                        # 扣费
                        if st.session_state['user_type'] == 'Free': 
                            st.session_state['usage_count'] += 1
                            
                    except Exception as e:
                        st.error(f"Error: {e}")

        # 结果显示与导出区
        if f'res_{mode_name}' in st.session_state:
            result_text = st.session_state[f'res_{mode_name}']
            
            # 显示结果
            st.markdown(f'<div class="output-card">{result_text}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1, 1, 1])
            
            # 1. 复制按钮 (纯文本)
            with c1:
                clean_copy = clean_text(result_text, keep_emojis=True)
                st.code(clean_copy, language=None)
                st.caption("📋 Copy Clean Text")
                
            # 2. TXT 下载 (Step 1 基础)
            with c2:
                st.download_button("📝 Download .txt", data=clean_copy, file_name=f"{mode_name}.txt")

            # 3. 高级下载 (Step 1 修复 + Step 2 逻辑)
            with c3:
                if st.session_state['user_type'] == 'Pro':
                    # CSV 智能判断
                    csv_data = extract_csv(result_text)
                    if csv_data:
                        st.download_button("📊 Download .csv", data=csv_data, file_name=f"{mode_name}.csv", mime='text/csv')
                    else:
                        # PDF 下载 (带字体修复)
                        pdf_data = create_pdf(result_text)
                        st.download_button("📄 Download .pdf", data=pdf_data, file_name=f"{mode_name}.pdf", mime='application/pdf')
                else:
                    st.button("👑 Download PDF (Pro)", disabled=True)

st.markdown('<div class="custom-footer">© 2025 Lai\'s Lab. All Rights Reserved.</div>', unsafe_allow_html=True)