import streamlit as st
import openai
import time

# ✅ 初始化
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ✅ 載入提示詞
def load_prompt(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

prompt_v = load_prompt("prompt_v.txt")
prompt_1 = load_prompt("prompt_1.txt")
prompt_a = load_prompt("prompt_a.txt")

# ✅ 呼叫 AI 回應
def get_response(prompt, user_input):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"[錯誤] {e}"

# ✅ 畫面設定
st.set_page_config(page_title="VetGPT 三角系統", page_icon="🐾", layout="wide")
st.title("🐾 VetGPT 寵物智慧醫療助手")
st.subheader("請輸入觀察紀錄，三位 AI 將依序提供分析")

# ✅ 初始化歷史紀錄
if "history" not in st.session_state:
    st.session_state.history = []

# ✅ 使用者輸入介面
user_input = st.text_area("請描述阿極的今日狀況", height=120)
col1, col2 = st.columns(2)
with col1:
    submit = st.button("獲取分析")
with col2:
    if st.button("清除紀錄"):
        st.session_state.history = []

# ✅ 三方 AI 分析主流程
if submit and user_input:
    with st.spinner("AI 分析中..."):
        v_response = get_response(prompt_v, user_input)
        one_response = get_response(prompt_1, user_input)

        # 整合給阿寶
        combined_input = f"""
        原始觀察：{user_input}

        小V分析：
        {v_response}

        小一分析：
        {one_response}
        """
        a_response = get_response(prompt_a, combined_input)

        # 保存
        st.session_state.history.append({
            "input": user_input,
            "v": v_response,
            "one": one_response,
            "a": a_response,
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        })

# ✅ 顯示歷史紀錄
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 歷史分析紀錄")
    for i, record in enumerate(reversed(st.session_state.history)):
        with st.expander(f"第 {len(st.session_state.history) - i} 筆紀錄 - {record['time']}"):
            st.markdown(f"📝 **觀察輸入：**)
{record['input']}")
            st.markdown(f"🟡 **小V 建議：**
{record['v']}")
            st.markdown(f"🔵 **小一 補充：**
{record['one']}")
            st.markdown(f"🟢 **阿寶 總結：**
{record['a']}")
