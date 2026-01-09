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

# CSS 苹果风美化
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

# ==========================================
# 2. 界面设计
# ==========================================

st.markdown("<h1 style='text-align: center;'>🎓 商金宝老师的数理辅导</h1>", unsafe_allow_html=True)
st.markdown("<p class='teacher-name'>物理老师商金宝 · Grade 9 专属 · 拍照解题</p>", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input("请输入 Gemini API Key", type="password")
    st.caption("提示：Key 仅用于连接谷歌大脑")

# 图片上传
uploaded_file = st.file_uploader("📸 上传题目图片 (可选)", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="已上传题目", use_container_width=True)

# 文本输入
input_text = st.text_area("📝 手动输入题目或补充问题...", height=100)

submit = st.button("开始解答")

# ==========================================
# 3. 核心逻辑 (保留了自动修复功能的完美版)
# ==========================================
if submit:
    if not api_key:
        st.error("🔒 请先在侧边栏输入 API Key")
    elif not input_text and not image:
        st.warning("⚠️ 请至少上传一张图片或输入一段文字")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- 自动寻找可用模型 (静默模式) ---
            valid_model_name = None
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        if 'flash' in m.name: # 优先用 flash
                            valid_model_name = m.name
                            break
                        elif 'pro' in m.name and not valid_model_name:
                            valid_model_name = m.name
                
                # 兜底策略
                if not valid_model_name:
                     for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            valid_model_name = m.name
                            break
            except Exception:
                st.error("无法连接谷歌服务器，请检查 API Key 是否正确。")
                st.stop()

            # --- 开始解题 ---
            if valid_model_name:
                model = genai.GenerativeModel(valid_model_name)
                
                system_prompt = """
                你是一位名字叫【商金宝】的资深初中物理和数学老师。
                你的学生是 Grade 9 (初三) 水平。
                请用亲切、鼓励的口吻（中文）回答。
                
                要求：
                1. **识别题目**：准确识别图片内容。
                2. **步骤清晰**：像板书一样分步骤讲解。
                3. **公式规范**：数学公式务必使用 LaTeX 格式。
                """
                
                content = [system_prompt]
                if input_text: content.append(input_text)
                if image: content.append(image)

                with st.spinner('商老师正在思考中...'):
                    response = model.generate_content(content)
                    
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown("### 💡 商老师的解答：")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("❌ 你的 API Key 似乎没有权限访问任何模型。")

        except Exception as e:
            st.error(f"发生错误: {e}")
