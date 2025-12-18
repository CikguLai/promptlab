import streamlit as st
import google.generativeai as genai
from PIL import Image
import zipfile
import io
import time
import requests

# ==========================================
# 1. 系统初始化与全局配置
# ==========================================
st.set_page_config(
    page_title="VisionPrompter AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 检查 API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Critical Error: GOOGLE_API_KEY is missing in Streamlit Secrets.")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]

# CSS 专业级美化 (Apple/Stripe 风格)
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom, #ffffff, #f8f9fa); font-family: 'Inter', sans-serif; }
    .result-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }
    .vip-tag { background: linear-gradient(90deg, #FFD700, #FDB931); color: white; padding: 4px 10px; border-radius: 20px; font-weight: 800; font-size: 0.75rem; }
    /* 手机端购买卡片样式 */
    .mobile-buy-card { background-color: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 10px; margin-top: 10px; margin-bottom: 20px; }
    a { text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# === 数据字典 ===
LANG_CONFIG = {
    "🇺🇸 English": "English", "🇲🇾 Bahasa Melayu": "Malay", "🇨🇳 简体中文": "Simplified Chinese",
    "🇹🇼 繁體中文": "Traditional Chinese", "🇯🇵 日本語": "Japanese", "🇰🇷 한국어": "Korean",
    "🇹🇭 ภาษาไทย": "Thai", "🇻🇳 Tiếng Việt": "Vietnamese", "🇪🇸 Español": "Spanish"
}

STYLE_PRESETS = {
    "✨ Original / 原图风格": "",
    "📸 Photorealistic / 写实光影": "photorealistic, cinematic lighting, 8k, ray tracing, highly detailed, realistic texture",
    "⛩️ Anime / 日式漫画": "anime style, japanese manga, studio ghibli style, cel shaded, vibrant colors",
    "🏰 Disney / 迪士尼动画": "disney style, pixar 3d style, 3d render, c4d, character design, cute",
    "👾 Pixel Art / 像素风格": "pixel art, 16-bit, retro game style, low res, blocky",
    "🤖 Cyberpunk / 赛博朋克": "cyberpunk, neon lights, futuristic, sci-fi, high tech, dark atmosphere",
    "🧊 3D Render / 3D 渲染": "3d render, unreal engine 5, octane render, blender, clay material",
    "🖍️ Line Art / 线稿风格": "line art, black and white, sketch, coloring book style, clean lines",
    "🔮 Fantasy / 奇幻风格": "fantasy art, magical, ethereal, dreamlike, oil painting style"
}

# ==========================================
# 2. 核心逻辑函数
# ==========================================

def validate_license_key(input_key):
    """VIP 验证逻辑"""
    manual_codes = st.secrets.get("MANUAL_CODES", [])
    if input_key in manual_codes: return True, "✅ Manual Access Granted"
    
    lemon_api_key = st.secrets.get("LEMON_API_KEY", "")
    if not lemon_api_key: return False, "⚠️ System Error: LEMON_API_KEY missing"
    if len(input_key) < 5: return False, "❌ Invalid Format"

    try:
        url = "https://api.lemonsqueezy.com/v1/licenses/activate"
        headers = {"Accept": "application/json"}
        data = {"license_key": input_key, "instance_name": "VisionPrompter_Web"}
        res = requests.post(url, headers=headers, data=data).json()
        
        if res.get("activated") == True or res.get("meta", {}).get("valid") == True:
            return True, "💎 VIP License Verified"
        return False, f"❌ {res.get('error', 'Invalid Key')}"
    except:
        return False, "⚠️ Network Verification Error"

def get_ai_response(image, prompt):
    """AI 生成逻辑 (含安全过滤器)"""
    genai.configure(api_key=api_key)
    # 设置安全等级：尽量不拦截，避免误杀正常图片
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
    ]
    model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
    
    try:
        response = model.generate_content([prompt, image])
        # 检查是否因安全原因被拦截
        if not response.parts:
            return "⚠️ AI Safety Block: Image content flagged as unsafe by Google."
        return response.text.strip()
    except Exception as e:
        time.sleep(1)
        if "400" in str(e) or "blocked" in str(e).lower():
             return "⚠️ Content Filtered: Image contains sensitive content."
        return f"⚠️ Server Busy ({str(e)}). Please retry."

def build_prompt(mode, is_vip, lang, ai_model, style_key, prefix, suffix, negative):
    """Prompt 拼装工厂"""
    target_lang = LANG_CONFIG[lang]
    style_words = STYLE_PRESETS[style_key]
    
    # 1. 基础指令
    if mode == "Art":
        if "Z-Image" in ai_model: base = "Output detailed Chinese and English tags. Format: (Chinese, English)."
        else:
            fmt = "comma-separated tags" if "Stable Diffusion" in ai_model else "natural language"
            base = f"Analyze image for {ai_model}. Use {fmt}. Output in English."
    elif mode == "Story":
        if is_vip: base = f"Write a creative 300-word story in {target_lang}. Structure: Title, Story, Moral."
        else: base = f"Write a simple 1-sentence description in {target_lang}."
    elif mode == "Social":
        if is_vip: base = f"Write a Viral Post in {target_lang} with Headline & 15 Hashtags."
        else: base = f"Write a caption in {target_lang}."
    else: base = "Analyze image."

    # 2. 注入参数
    final = base
    if style_words and mode == "Art": final += f"\nIMPORTANT Style: {style_words}"
    if prefix: final += f"\nStart output with: {prefix}"
    if suffix: final += f"\nEnd output with: {suffix}"
    if negative: final += f"\nExclude concepts: {negative}"
    
    return final

# ==========================================
# 3. 侧边栏 (设置与 VIP 控制台)
# ==========================================
with st.sidebar:
    st.header("⚙️ Settings")
    lang = st.selectbox("🌐 Language", list(LANG_CONFIG.keys()))
    
    with st.expander("🤖 AI Model"):
        ai_model = st.selectbox("Format:", ["General", "Stable Diffusion", "Midjourney v6", "DALL·E 3", "Z-Image (中文)"])

    st.markdown("---")
    st.markdown("### 🔑 VIP Activation")
    input_code = st.text_input("License Key", type="password", placeholder="Paste Key here...")
    
    is_vip = False
    if input_code:
        valid, msg = validate_license_key(input_code)
        if valid: is_vip = True; st.success(msg)
        else: st.error(msg)
        
    limit = 100 if is_vip else 3

    # === 核心差异化功能区 ===
    st.markdown("---")
    if is_vip:
        st.markdown("### 🎨 VIP Controls (Unlocked)")
        # VIP 才能选风格
        style_key = st.selectbox("Style Filter", list(STYLE_PRESETS.keys()))
        # VIP 才能微调
        with st.expander("🛠️ Fine-tune Prompts"):
            prefix = st.text_input("Prefix", placeholder="e.g. masterpiece")
            suffix = st.text_input("Suffix", placeholder="e.g. --ar 16:9")
            negative = st.text_input("Negative", placeholder="e.g. blur")
    else:
        st.markdown("### 🔒 VIP Controls (Locked)")
        st.caption("Upgrade to unlock Styles, Fine-tuning & Batch Mode.")
        style_key = list(STYLE_PRESETS.keys())[0] # 强制原图
        prefix, suffix, negative = "", "", ""
        
        # 侧边栏购买按钮
        # ⚠️ 【待修改 1】 Lemon Squeezy 链接
        buy_url = "https://your-shop.lemonsqueezy.com/buy/xxxx" 
        st.link_button(f"👉 Buy Lifetime ($12.90)", buy_url, type="primary", use_container_width=True)

    # 重置按钮
    st.markdown("---")
    if st.button("🗑️ Reset All / 清空", use_container_width=True):
        st.rerun()

    # 客服表单
    with st.expander("💬 Help & Support"):
        st.markdown("[📧 support@cikgulai.com](mailto:support@cikgulai.com)")
        with st.form("support_form"):
            user_msg = st.text_area("Issue/Feedback")
            user_email = st.text_input("Your Email (Optional)")
            if st.form_submit_button("Send"):
                if user_msg:
                    # ⚠️ 【待修改 2】 Formspree 链接
                    try:
                        requests.post("https://formspree.io/f/你的FormspreeID", json={"msg":user_msg, "email":user_email})
                        st.success("Sent!")
                    except: st.error("Network Error")
                else: st.warning("Write something first.")

# ==========================================
# 4. 主界面构建
# ==========================================
st.title("VisionPrompter AI")
st.caption("Visual-to-Content Intelligence Hub | 视觉内容生成平台")

mode = st.radio("Mode:", ["Art", "Story", "Social"], horizontal=True, format_func=lambda x: {"Art":"🎨 Art Prompt", "Story":"📖 Storyteller", "Social":"📱 Social Kit"}[x])

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.markdown("### 📥 Upload")
    files = st.file_uploader(f"Batch Limit: {limit} images", type=["jpg","png","webp"], accept_multiple_files=True)
    
    if files and len(files) > limit: 
        st.warning(f"⚠️ Limit Exceeded. Free: {limit}, VIP: 100.")
    
    # === 📱 手机端/主界面 购买卡片 (只展示给免费用户) ===
    if not is_vip:
        st.markdown(f"""
        <div class="mobile-buy-card">
            <p style="color: #856404; font-weight: bold; margin: 0;">🔓 Unlock VIP Power</p>
            <p style="color: #856404; font-size: 0.9em; margin: 5px 0;">
                • Batch process 100+ images<br>
                • Excel export & 10+ Art Styles
            </p>
        </div>
        """, unsafe_allow_html=True)
        # 这里放购买链接，确保手机用户看得到
        st.link_button("👉 Upgrade Now ($12.90)", buy_url, type="primary", use_container_width=True)

with col2:
    st.markdown("### 🚀 Action")
    if st.button("Start Analysis & Generate", type="primary", use_container_width=True):
        if not files: st.warning("Please upload image first.")
        elif len(files) > limit: st.error("Upgrade to VIP to process this many images.")
        else:
            st.session_state.res = []
            bar = st.progress(0)
            status = st.empty()
            
            for i, f in enumerate(files):
                status.text(f"Analyzing {i+1}/{len(files)}: {f.name}...")
                img = Image.open(f)
                
                # 调用 AI
                res_text = get_ai_response(img, build_prompt(mode, is_vip, lang, ai_model, style_key, prefix, suffix, negative))
                st.session_state.res.append((f.name, res_text))
                
                # 智能限速 (VIP快，免费慢)
                time.sleep(0.5 if is_vip else 2.0)
                bar.progress((i+1)/len(files))
            
            status.text("✅ Done!")
            time.sleep(1)
            status.empty()
            st.rerun()

# ==========================================
# 5. 结果展示与下载 (分级策略)
# ==========================================
if 'res' in st.session_state and st.session_state.res:
    st.markdown("---")
    st.subheader("🎉 Generation Results")
    
    txt_content = ""
    csv_data = "Filename,Prompt\n"
    
    for n, c in st.session_state.res:
        txt_content += f"=== {n} ===\n{c}\n\n"
        # CSV 处理换行和引号
        clean_c = c.replace('"', '""') 
        csv_data += f'"{n}","{clean_c}"\n'
        
        # 界面展示：使用 st.code 实现一键复制
        st.caption(f"🖼️ {n}")
        st.code(c, language=None)
    
    st.markdown("---")
    
    if is_vip:
        # === 💎 VIP 专属：ZIP 大礼包 ===
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w") as zf:
            zf.writestr("results.txt", txt_content)
            zf.writestr("results.csv", csv_data)
        
        st.download_button("📦 Download VIP Pack (TXT + Excel)", zip_buf.getvalue(), "vision_vip.zip", "application/zip", type="primary", use_container_width=True)
    else:
        # === 🔓 免费版：仅 TXT ===
        st.download_button("📄 Download Results (.txt)", txt_content, "vision_results.txt", "text/plain", use_container_width=True)
        st.caption("💡 Tip: Upgrade to VIP for Excel export and style filters.")

# ==========================================
# 6. 专业法律页脚
# ==========================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #999; padding: 20px 0;">
    <p style="font-weight: bold; margin-bottom: 5px;">VisionPrompter AI <span style="font-weight: normal;">v1.0.9</span></p>
    <p style="font-size: 0.8em; margin-bottom: 10px;">Built with ❤️ by <a href="#" style="color:#666;">Cikgu Lai</a></p>
    <p style="font-size: 0.7em; font-style: italic;">
        Disclaimer: AI-generated content may be inaccurate. Users are responsible for verifying information.<br>
        © 2026 Cikgu Lai Digital Assets. All Rights Reserved.
    </p>
</div>
""", unsafe_allow_html=True)