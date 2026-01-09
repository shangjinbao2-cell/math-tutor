import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. 页面配置
# ==========================================
st.set_page_config(
    page_title="商金宝老师的数理辅导",
    page_icon="👨‍🏫",
    layout="centered"
)

# CSS 美化 (保持苹果风)
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
    /* 名字特效 */
    .teacher-name {
        font-size: 1.2rem;
        color: #86868b;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 400;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 界面设计 (已添加名字)
# ==========================================

# 主标题
st.markdown("<h1 style='text-align: center;'>🎓 商金宝老师的数理辅导</h1>", unsafe_allow_html=True)

# 副标题 (你的署名)
st.markdown("<p class='teacher-name'>物理老师商金宝 · Grade 9 专属 · 拍照解题</p>", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input("请输入 Gemini API Key", type="password")
    st.info("提示：请向商老师索取 Key 或自行申请")

# 图片上传区
uploaded_file = st.file_uploader("📸 上传题目图片 (可选)", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="已上传的题目", use_container_width=True)

# 文本输入区
input_text = st.text_area("📝 手动输入题目或补充问题...", height=100, placeholder="例如：请帮我讲解这道电路图的问题...")

submit = st.button("开始解答")

# ==========================================
# 3. AI 核心逻辑
# ==========================================
if submit:
    if not api_key:
        st.error("🔒 请输入 API Key 才能开始解题")
    elif not input_text and not image:
        st.warning("⚠️ 请上传图片或输入文字")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')

            
            # 定制提示词
            system_prompt = """
            你现在是【物理老师商金宝】的AI助教。
            请用商老师亲切、专业的口吻，为Grade 9 (初三) 的学生讲解题目。
            
            要求：
            1. **身份代入**：回答时可以使用"商老师觉得..."或"我们可以这样看..."。
            2. **逻辑清晰**：分步骤讲解，不要直接给答案。
            3. **公式规范**：数学公式使用 LaTeX 格式。
            4. **鼓励式教学**：如果题目很难，要给学生一点鼓励。
            """
            
            with st.spinner('商老师正在思考中...'):
                inputs = [system_prompt]
                if input_text:
                    inputs.append(f"学生的问题：{input_text}")
                if image:
                    inputs.append(image)
                
                response = model.generate_content(inputs)
                
                # 结果显示
                st.markdown("### 💡 商老师的解答：")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"出错了：{e}")
