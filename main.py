import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. 页面配置
# ==========================================
st.set_page_config(
    page_title="商金宝老师的数理辅导",
    page_icon="🎓",
    layout="centered"
)

# 苹果风 CSS
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
        font-size: 16px;
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
    .status-badge {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 5px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 自动获取密钥 (核心修改)
# ==========================================

# 优先从服务器 Secrets 里找 Key
api_key = st.secrets.get("GEMINI_API_KEY")

# 如果没找到（比如你在本地运行），才显示输入框
if not api_key:
    with st.sidebar:
        api_key = st.text_input("请输入 Gemini API Key", type="password")

# ==========================================
# 3. 界面显示
# ==========================================

st.markdown("<h1 style='text-align: center;'>🎓 商金宝老师的数理辅导</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #86868b;'>物理老师商金宝 · Grade 9 专属 · 拍照解题</p>", unsafe_allow_html=True)

# 显示“已授权”状态，让用户安心
if api_key:
    st.markdown("<div style='text-align: center;'><span class='status-badge'>✅ 已自动激活商老师授权</span></div>", unsafe_allow_html=True)

# 上传区
uploaded_file = st.file_uploader("📸 上传题目图片", type=["jpg", "jpeg", "png"])
image = Image.open(uploaded_file) if uploaded_file else None
if image:
    st.image(image, caption="已上传题目", use_container_width=True)

# 输入区
input_text = st.text_area("📝 手动输入题目或补充问题...", height=100)
submit = st.button("开始解答")

# ==========================================
# 4. 解题逻辑 (自适应模型)
# ==========================================
if submit:
    if not api_key:
        st.error("🔒 未检测到 API Key，请联系管理员配置 Secrets。")
    elif not input_text and not image:
        st.warning("⚠️ 请上传图片或输入文字")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # 自动匹配模型
            valid_model_name = None
            try:
                # 优先找 flash，其次 pro
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                for m in models:
                    if 'flash' in m: valid_model_name = m; break
                if not valid_model_name:
                    for m in models:
                        if 'pro' in m: valid_model_name = m; break
                if not valid_model_name and models:
                    valid_model_name = models[0]
            except:
                st.error("Key 配置有误，无法连接谷歌服务器。")
                st.stop()

            if valid_model_name:
                model = genai.GenerativeModel(valid_model_name)
                
                system_prompt = """
                你是一位叫【商金宝】的资深初中物理和数学老师。
                请用亲切、鼓励的口吻（中文）为 Grade 9 学生讲解。
                要求：步骤清晰，公式使用 LaTeX 格式。
                """
                
                content = [system_prompt]
                if input_text: content.append(input_text)
                if image: content.append(image)

                with st.spinner('商老师正在看题...'):
                    response = model.generate_content(content)
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown("### 💡 商老师的解答：")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("❌ 账号无可用模型权限")

        except Exception as e:
            st.error(f"发生错误: {e}")
