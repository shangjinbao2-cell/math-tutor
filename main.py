import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. 页面基础配置
# ==========================================
st.set_page_config(
    page_title="商金宝老师的数理辅导",
    page_icon="🎓",
    layout="centered"
)

# 苹果风 CSS 样式
st.markdown("""
<style>
    body, .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #FBFBFD;
        color: #1D1D1F;
    }
    .stButton button {
        background-color: #0071e3;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        width: 100%;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #0077ED;
    }
    .result-card {
        background-color: white;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 20px;
        border: 1px solid #F5F5F7;
    }
    .debug-info {
        font-size: 0.8rem;
        color: #86868b;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🎓 商金宝老师的数理辅导</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #86868b;'>智能匹配模型版 · Grade 9 专属</p>", unsafe_allow_html=True)

# ==========================================
# 2. 侧边栏与输入
# ==========================================
with st.sidebar:
    st.header("⚙️ 设置 (Settings)")
    api_key = st.text_input("Gemini API Key", type="password")

uploaded_file = st.file_uploader("📸 上传题目图片 (可选)", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="已上传图片", use_container_width=True)

input_text = st.text_area("📝 手动输入题目...", height=100)
submit = st.button("开始解答")

# ==========================================
# 3. 核心逻辑：自动寻找可用模型 (Auto-Find)
# ==========================================
if submit:
    if not api_key:
        st.error("🔒 请先输入 API Key")
    elif not input_text and not image:
        st.warning("⚠️ 请上传图片 or 输入文字")
    else:
        try:
            # 1. 配置 Key
            genai.configure(api_key=api_key)
            
            # 2. 【关键一步】自动侦测可用模型
            # 我们不指定死名字，而是问服务器有哪些
            available_models = []
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
            except Exception as e:
                st.error(f"连不上谷歌服务器，可能是Key有问题: {e}")
                st.stop()

            # 3. 智能选择策略
            final_model_name = ""
            
            # 优先找 flash (速度快)
            if any("gemini-1.5-flash" in m for m in available_models):
                final_model_name = "gemini-1.5-flash"
            # 其次找 pro (经典版)
            elif any("gemini-1.5-pro" in m for m in available_models):
                final_model_name = "gemini-1.5-pro"
            elif any("gemini-pro" in m for m in available_models):
                final_model_name = "gemini-pro"
            # 实在不行，就用列表里的第一个
            elif available_models:
                final_model_name = available_models[0].name
            else:
                st.error("❌ 你的 API Key 没有任何可用的模型权限。")
                st.stop()

            # 4. 启动模型
            model = genai.GenerativeModel(final_model_name)
            
            # 提示词
            prompt = """
            你是一位叫【商金宝】的初中物理和数学老师。
            请用亲切、鼓励的口吻（中文）为 Grade 9 学生讲解。
            要求：步骤清晰，数学公式用 LaTeX 格式。
            """
            
            content = [prompt]
            if input_text: content.append(input_text)
            if image: content.append(image)

            with st.spinner(f'商老师正在思考 (使用引擎: {final_model_name})...'):
                response = model.generate_content(content)
                
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown("### 💡 商老师的解答：")
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 显示调试信息，让你知道最后用了哪个模型
                st.markdown(f"<p class='debug-info'>🔧 成功调用模型: {final_model_name}</p>", unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"发生错误: {e}")
