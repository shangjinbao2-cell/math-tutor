import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="商金宝老师的数理辅导", page_icon="🎓")

# CSS 美化
st.markdown("""
<style>
    .stButton button {background-color: #0071e3; color: white; border-radius: 20px; width: 100%;}
    .result-card {background-color: #f9f9f9; border-radius: 15px; padding: 20px; margin-top: 20px; border: 1px solid #ddd;}
</style>
""", unsafe_allow_html=True)

st.title("🎓 商金宝老师的数理辅导")
st.caption("自动适配模型版 · 专治 404 报错")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input("Gemini API Key", type="password")

# 输入区
uploaded_file = st.file_uploader("📸 上传图片", type=["jpg", "png", "jpeg"])
image = Image.open(uploaded_file) if uploaded_file else None
if image: st.image(image, caption="已上传", use_container_width=True)

input_text = st.text_area("📝 输入题目...")
submit = st.button("开始解答")

# 核心逻辑：直接使用查找到的真实模型名
if submit:
    if not api_key:
        st.error("🔒 请输入 Key")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- 第一步：侦测可用模型 ---
            valid_model_name = None
            debug_list = []
            
            with st.spinner('正在检测你的可用模型列表...'):
                for m in genai.list_models():
                    # 记录所有模型用于调试
                    debug_list.append(m.name)
                    # 寻找支持内容生成的模型
                    if 'generateContent' in m.supported_generation_methods:
                        # 优先找 flash 或 pro
                        if 'flash' in m.name:
                            valid_model_name = m.name
                            break
                        elif 'pro' in m.name and not valid_model_name:
                            valid_model_name = m.name
                
                # 如果没找到优选的，就拿列表里第一个能用的兜底
                if not valid_model_name:
                     for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            valid_model_name = m.name
                            break

            # --- 第二步：使用该模型 ---
            if valid_model_name:
                # 显示我们要用的模型名字（调试用）
                st.success(f"✅ 成功连接模型：{valid_model_name}")
                
                model = genai.GenerativeModel(valid_model_name)
                
                prompt = "你是一位叫【商金宝】的初中物理数学老师。请用中文为初三学生讲解题目。要求步骤清晰，使用LaTeX公式。"
                content = [prompt]
                if input_text: content.append(input_text)
                if image: content.append(image)
                
                with st.spinner('商老师正在解题...'):
                    response = model.generate_content(content)
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("❌ 你的Key似乎没有访问任何模型的权限。")
                st.write("谷歌返回的模型列表：", debug_list)

        except Exception as e:
            st.error(f"发生错误: {e}")
