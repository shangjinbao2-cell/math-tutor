import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Math & Physics Tutor",
    page_icon="🎓",
    layout="centered"
)

# 2. CSS Styling (Apple Style)
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
        font-size: 16px;
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

# 3. UI Layout
st.markdown("<h1 style='text-align: center;'>🎓 商金宝老师的数理辅导</h1>", unsafe_allow_html=True)
st.markdown("<p class='teacher-name'>物理老师商金宝 · Grade 9 专属 · 拍照解题</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ 设置 (Settings)")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("请输入你的 Google Gemini API Key")

# File Uploader
uploaded_file = st.file_uploader("📸 上传题目图片 (可选)", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="已上传图片", use_container_width=True)

# Text Input
input_text = st.text_area("📝 手动输入题目或补充问题...", height=100)

# Submit Button
submit = st.button("开始解答 (Start)")

# 4. Logic & AI Call
if submit:
    if not api_key:
        st.error("🔒 请先在侧边栏输入 API Key (Please enter API Key first)")
    elif not input_text and not image:
        st.warning("⚠️ 请上传图片或输入文字 (Please upload image or text)")
    else:
        try:
            # Configure API
            genai.configure(api_key=api_key)
            
            # Using the latest stable model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Prompt Engineering
            system_prompt = """
            你是一位名字叫【商金宝】的资深初中物理和数学老师。
            你的学生是 Grade 9 (初三) 水平。
            请用亲切、鼓励的口吻（中文）回答。
            
            要求：
            1. 识别图片中的题目。
            2. 步骤清晰，逻辑严密。
            3. 数学公式使用 LaTeX 格式。
            """
            
            with st.spinner('商老师正在思考中... (Thinking...)'):
                content = [system_prompt]
                if input_text:
                    content.append(input_text)
                if image:
                    content.append(image)
                
                # Generate
                response = model.generate_content(content)
                
                # Display
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown("### 💡 商老师的解答：")
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"发生错误 (Error): {e}")
