import openai
import streamlit as st
import time

st.set_page_config(page_title="VetGPT 三角系統", page_icon="🩺")
# 顯示 SDK 版本
st.write("OpenAI SDK version:", openai.__version__)

# 初始化 OpenAI API 金鑰（v1.1.0 用法）
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 載入提示詞
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

# 呼叫 OpenAI 回應
def get_response(prompt, user_input):
    try:
        response = openai.ChatCompletion.create(
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

# Streamlit 畫面設定
st.title("VetGPT 三角系統")
st.markdown("請輸入你的問題，並選擇角色（V / 一 / A）進行對話")

# 選擇提示詞
selected_prompt = st.selectbox("選擇角色", ["小V", "小一", "阿寶"])
if selected_prompt == "小V":
    prompt = prompt_v
elif selected_prompt == "小一":
    prompt = prompt_1
else:
    prompt = prompt_a

# 輸入區
user_input = st.text_area("你想問什麼？", height=150)

# 提交按鈕
if st.button("送出"):
    if not user_input.strip():
        st.warning("請輸入內容再送出。")
    else:
        with st.spinner("正在思考中..."):
            reply = get_response(prompt, user_input)
            st.success("回覆完成：")
            st.markdown(reply)