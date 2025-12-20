import streamlit as st
import google.generativeai as genai
import sys
import os

st.set_page_config(page_title="系统诊断工具", page_icon="🩺")
st.title("🩺 VisionPrompter 系统诊断")

# 1. 检查 Python 环境
st.subheader("1. 环境检查")
try:
    import google.generativeai
    version = google.generativeai.__version__
    st.write(f"**Google AI 库版本:** `{version}`")
    
    # 关键判断：如果版本低于 0.7.2，那就是 Streamlit 服务器没更新！
    if version < "0.7.2":
        st.error("❌ 严重错误：库版本太旧！服务器还在用旧缓存。")
        st.info("解决办法：请去 GitHub 修改 requirements.txt，随便加个空格再保存，强制触发更新。")
    else:
        st.success("✅ 库版本正常 (支持 Gemini 1.5)。")
except ImportError:
    st.error("❌ 严重错误：根本没安装 google-generativeai 库！")

# 2. 检查 API Key 格式
st.subheader("2. 钥匙 (Secrets) 检查")
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ 致命错误：Secrets 里找不到 GOOGLE_API_KEY。")
else:
    # 检查是否有空格或隐形字符
    if " " in api_key:
        st.error(f"❌ 格式错误：您的 Key 里面包含了空格！请检查开头或结尾。")
    elif len(api_key) < 30:
        st.error(f"❌ 格式错误：Key 太短了，看起来不像真的。")
    elif not api_key.startswith("AIza"):
        st.error(f"❌ 格式错误：Key 必须以 'AIza' 开头。您填的是：{api_key[:4]}...")
    else:
        st.success(f"✅ Key 格式看起来正确 (以 {api_key[:4]}... 开头)")
        
        # 3. 尝试连通性测试 (列出所有可用模型)
        st.subheader("3. 连通性测试 (关键！)")
        try:
            genai.configure(api_key=api_key)
            st.write("📡 正在尝试连接 Google 服务器...")
            
            models = []
            for m in genai.list_models():
                models.append(m.name)
            
            st.success("✅ 连接成功！您的 Key 是有效的。")
            st.write("📋 您的账号可用的模型列表：")
            st.json(models)
            
            # 检查是否有我们要的模型
            if "models/gemini-1.5-flash" in models:
                st.balloons()
                st.success("🎉 太好了！您的账号拥有 gemini-1.5-flash 的权限！可以把原来的代码换回来了！")
            else:
                st.warning("⚠️ 连接成功，但列表中没有 gemini-1.5-flash。这可能是 Google 账号的地区限制。")
                
        except Exception as e:
            st.error(f"❌ 连接失败：Google 拒绝了请求。原因：\n{e}")
            st.markdown("---")
            st.markdown("**如果这里报错 403/404，说明 Key 还是有问题，或者 Google Cloud 项目没开通 API。**")