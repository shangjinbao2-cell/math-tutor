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

# CSS 美化 (苹果风)
st.markdown("""
<style>
    body, .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #FBFBFD;
        color: #1D1D1F;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
    .teacher-name {
        font-size: 1.1rem;
        color: #86868b;
        text-align: center;
        margin-bottom: 30px;
    }
    .result-card {
        background-color: white;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 20px;
        border: 1px solid #F5F5F7;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 界面设计
# ==========================================

st.markdown("<h1 style='text-align: center;'>🎓 商金宝老师的数理辅导</h1>", unsafe_allow_html=True)
st.markdown("<p class='teacher-name'>物理老师商金宝 · Grade 9 专属 · 拍照解题</p>", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.header("⚙️ 设置 (Settings)")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("请输入你的 Google Gemini API Key")

# 图片上传
uploaded_file = st.file_uploader("📸 上传题目图片 (可选)", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="已上传图片", use_container_width=True)

# 文本输入
input_text = st.text_area("📝 手动输入题目或补充问题...", height=100)

submit = st.button("开始解答 (Start)")

# ==========================================
# 3. 核心逻辑 (换回了 gemini-pro)
# ==========================================
if submit:
    if not api_key:
        st.error("🔒 请先在侧边栏输入 API Key")
    elif not input_text and not image:
        st.warning("⚠️ 请上传图片或输入文字")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- 关键修改：换回最稳定的 gemini-pro ---
            if image:
                # 如果有图片，必须用 vision 模型
                model = genai.GenerativeModel('gemini-pro-vision')
            else:
                # 如果只有文字，用普通 pro 模型
                model = genai.GenerativeModel('gemini-pro')
            
            # 提示词
            system_prompt = """
            你是一位名字叫【商金宝】的资深初中物理和数学老师。
            你的学生是 Grade 9 (初三) 水平。
            请用亲切、鼓励的口吻（中文）回答。
            要求：步骤清晰，逻辑严密，数学公式使用 LaTeX 格式。
            """
            
            with st.spinner('商老师正在思考中...'):
                content = [system_prompt]
                if input_text:
                    content.append(input_text)
                if image:
                    content.append(image)
                
                response = model.generate_content(content)
                
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown("### 💡 商老师的解答：")
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            # 如果 vision 模型也报错，提示用户
            if "404" in str(e) and image:
                st.error(f"发生错误：模型暂时繁忙，请尝试仅输入文字，或稍后再试。详细错误：{e}")
            else:
                st.error(f"发生错误: {e}")
