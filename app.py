import streamlit as st
import openai
import time

# 頁面設定
st.set_page_config(page_title="VetGPT 三角系統", page_icon="🐾")

# 顯示 SDK 版本
st.write("OpenAI SDK version:", openai.__version__)

# 設定 API 金鑰（OpenAI SDK v1.1.0 寫法）
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 載入角色提示詞
def load_prompt(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"無法找到提示詞檔案：{file_name}")
        return ""

prompt_v = load_prompt("prompt_v.txt")
prompt_1 = load_prompt("prompt_1.txt")
prompt_a = load_prompt("prompt_a.txt")

# 呼叫 OpenAI API 回應
def get_response(prompt, user_input):
    try:
        response = openaiChatCompletions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"發生錯誤：{e}")
        return ""

# Streamlit 畫面
st.title("VetGPT 三角系統")
st.write("請輸入你的問題，三位角色將共同回應。")

user_input = st.text_input("你想問什麼？", "")

if st.button("送出") and user_input:
    with st.spinner("思考中..."):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("小V")
            response_v = get_response(prompt_v, user_input)
            st.write(response_v)

        with col2:
            st.subheader("小一")
            response_1 = get_response(prompt_1, user_input)
            st.write(response_1)

        with col3:
            st.subheader("阿寶")
            response_a = get_response(prompt_a, user_input)
            st.write(response_a)