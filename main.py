import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. 页面配置 & 苹果风 UI 设计
# ==========================================
st.set_page_config(
    page_title="Math & Physics Tutor",
    page_icon="🍎",
    layout="centered"
)

# 注入自定义 CSS 以实现“苹果风”
st.markdown("""
<style>
    /* 1. 引入系统字体 */
    body, .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #FBFBFD;
        color: #1D1D1F;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 标题样式 */
    h1 {
        font-weight: 600;
        letter-spacing: -0.02em;
        font-size: 2.5rem;
        text-align: center;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    /* 输入框美化 */
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #D2D2D7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        padding: 16px;
        font-size: 16px;
    }
    .stTextArea textarea:focus {
        border-color: #0071e3;
        box-shadow: 0 0 0 2px rgba(0,113,227,0.2);
    }

    /* 按钮美化 */
    .stButton button {
        background-color: #000000;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: 500;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #333333;
        transform: scale(1.01);
    }

    /* 结果卡片美化 */
    .result-card {
        background-color: white;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.04);
        margin-top: 20px;
        border: 1px solid #F5F5F7;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 逻辑处理核心
# ==========================================

st.markdown("<h1> Math & Physics Tutor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #86868b; margin-top: -20px; margin-bottom: 40px;'>Grade 9 专属 · 极简 · 智能</p>", unsafe_allow_html=True)

# 侧边栏设置 API Key
with st.sidebar:
    st.write("设置")
    api_key = st.text_input("Gemini API Key", type="password")
    
# 主输入区
input_text = st.text_area("请输入题目或疑问...", height=120, placeholder="例如：一个抛物线 y=ax²+bx+c 经过点(0,0)...")

# 按钮区
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit = st.button("开始解答")

# ==========================================
# 3. AI 回答逻辑
# ==========================================
if submit:
    if not api_key:
        st.warning("⚠️ 请先在侧边栏输入 API Key")
    elif not input_text:
        st.warning("⚠️ 请先输入题目")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            system_prompt = f"""
            你是一位世界顶级的初中数学和物理老师。
            你的学生是 Grade 9 (初三) 水平。
            请按照以下风格回答：
            1. **清晰直观**：像苹果的设计一样，逻辑分层。
            2. **公式规范**：所有数学公式必须使用 LaTeX 格式（用 $ 包裹）。
            3. **循循善诱**：先分析思路，再给出步骤。
            4. **语言风格**：亲切、鼓励性，用中文回答。
            
            学生的问题是：{input_text}
            """
            
            with st.spinner('正在分析题目逻辑...'):
                response = model.generate_content(system_prompt)
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"发生错误: {e}")
