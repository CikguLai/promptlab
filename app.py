import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. 配置与多语言字典
# ==========================================

st.set_page_config(
    page_title="Ultra Prompt Gacha",
    page_icon="🎨",
    layout="wide"
)

# 检查 Secrets 是否配置 (这是关键安全步骤)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("系统错误：未检测到 API Key配置。请联系管理员 (Cikgu Lai) 在 Streamlit 后台设置 Secrets。")
    st.stop()

# 直接从后台读取 Key，不让用户看到
api_key = st.secrets["GOOGLE_API_KEY"]

TRANS = {
    "简体中文": {
        "title": "🎨 AI 提示词抓取器 (学生版)",
        "subtitle": "上传图片，一键提取 AI 绘画提示词",
        "sidebar_title": "设置",
        "upload_label": "上传一张图片 (JPG/PNG)",
        "style_label": "图片风格分析模式",
        "styles": ["通用写实 (Photorealistic)", "动漫二次元 (Anime/Manga)", "3D 渲染 (3D Render/Chibi)", "油画艺术 (Oil Painting)"],
        "prefix_label": "自定义前缀 (Prefix) - 可选",
        "prefix_ph": "例如: best quality, masterpiece...",
        "btn_generate": "✨ 生成提示词",
        "result_label": "生成结果 (已优化为英文提示词):",
        "loading": "AI 正在观察图片，请稍候...",
        "success": "提取成功！快去画图吧！"
    },
    "繁體中文": {
        "title": "🎨 AI 提示詞抓取器 (學生版)",
        "subtitle": "上傳圖片，一鍵提取 AI 繪圖提示詞",
        "sidebar_title": "設定",
        "upload_label": "上傳一張圖片 (JPG/PNG)",
        "style_label": "圖片風格分析模式",
        "styles": ["通用寫實 (Photorealistic)", "動漫二次元 (Anime/Manga)", "3D 渲染 (3D Render/Chibi)", "油畫藝術 (Oil Painting)"],
        "prefix_label": "自訂前綴 (Prefix) - 可選",
        "prefix_ph": "例如: best quality, masterpiece...",
        "btn_generate": "✨ 生成提示詞",
        "result_label": "生成結果 (已優化為英文提示詞):",
        "loading": "AI 正在觀察圖片，請稍候...",
        "success": "提取成功！快去繪圖吧！"
    },
    "Bahasa Melayu": {
        "title": "🎨 Pengekstrak AI Prompt (Edisi Pelajar)",
        "subtitle": "Muat naik gambar untuk dapatkan prompt AI",
        "sidebar_title": "Tetapan",
        "upload_label": "Muat naik Gambar (JPG/PNG)",
        "style_label": "Mod Gaya Gambar",
        "styles": ["Fotorealistik (Photorealistic)", "Anime/Manga", "Render 3D (3D Render/Chibi)", "Lukisan Minyak (Oil Painting)"],
        "prefix_label": "Awalan Tersuai (Prefix) - Pilihan",
        "prefix_ph": "Contoh: best quality, masterpiece...",
        "btn_generate": "✨ Jana Prompt",
        "result_label": "Hasil (Prompt dalam Bahasa Inggeris):",
        "loading": "AI sedang menganalisis gambar...",
        "success": "Berjaya! Sila salin prompt di bawah."
    },
    "English": {
        "title": "🎨 AI Prompt Gacha (Student Ver.)",
        "subtitle": "Upload image to reverse-engineer AI prompts",
        "sidebar_title": "Settings",
        "upload_label": "Upload an Image (JPG/PNG)",
        "style_label": "Image Style Mode",
        "styles": ["Photorealistic", "Anime/Manga", "3D Render/Chibi", "Oil Painting"],
        "prefix_label": "Custom Prefix (Optional)",
        "prefix_ph": "e.g., best quality, masterpiece...",
        "btn_generate": "✨ Generate Prompt",
        "result_label": "Generated Result (English Prompt):",
        "loading": "AI is analyzing the image...",
        "success": "Success! Copy the prompt below."
    }
}

# ==========================================
# 2. 核心逻辑
# ==========================================

def get_gemini_response(key, image, style_mode, prefix):
    # 配置 API
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    system_prompt = f"""
    You are an expert AI art prompter.
    Analyze the uploaded image and generate a detailed text prompt.
    Target Style: {style_mode}
    Requirements:
    1. Output ONLY the prompt in English.
    2. Format: (Subject description), (Action/Pose), (Environment/Background), (Lighting/Atmosphere), (Camera angle), (Artistic Style tags).
    3. Use comma-separated tags.
    """
    if prefix:
        system_prompt += f"\nNote: Start the prompt strictly with: '{prefix}'"

    response = model.generate_content([system_prompt, image])
    return response.text

# ==========================================
# 3. 界面布局
# ==========================================

lang_option = st.sidebar.selectbox(
    "Language / 语言 / Bahasa",
    ["简体中文", "繁體中文", "Bahasa Melayu", "English"]
)
t = TRANS[lang_option]

st.title(t["title"])
st.caption(t["subtitle"])

st.sidebar.header(t["sidebar_title"])

# 侧边栏只保留“样式”和“前缀”，去掉了 Key 的输入框
selected_style = st.sidebar.selectbox(t["style_label"], t["styles"])
user_prefix = st.sidebar.text_area(t["prefix_label"], placeholder=t["prefix_ph"], height=100)
st.sidebar.info("Developed by Cikgu Lai") # 加上你的署名

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"### {t['upload_label']}")
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Preview", use_container_width=True)

with col2:
    st.markdown("### Result")
    # 把生成按钮放在这里，布局更合理
    if st.button(t["btn_generate"], type="primary", use_container_width=True):
        if uploaded_file is None:
            st.warning(t["upload_label"])
        else:
            with st.spinner(t["loading"]):
                try:
                    # 使用后台的 api_key
                    result_prompt = get_gemini_response(api_key, image, selected_style, user_prefix)
                    st.success(t["success"])
                    st.code(result_prompt, language="markdown")
                except Exception as e:
                    st.error(f"Error: {e}")