import streamlit as st
from openai import OpenAI
import time
import os

# 初始化 OpenAI client
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("請在 .streamlit/secrets.toml 中設置 OPENAI_API_KEY")
    st.stop()

# 載入提示詞
def load_prompt(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"找不到提示詞文件：{file_name}")
        return ""

# 載入三個角色的提示詞
prompt_v = load_prompt("prompt_v.txt")
prompt_1 = load_prompt("prompt_1.txt")
prompt_a = load_prompt("prompt_a.txt")

# 使用OpenAI API獲取回應
def get_ai_response(prompt, user_input, model="gpt-4o", temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"獲取AI回應時出錯：{str(e)}")
        return ""

# 主頁面設計
def main():
    st.set_page_config(
        page_title="VetGPT 三角系統",
        page_icon="🐾",
        layout="wide"
    )
    
    st.title("🐾 VetGPT 寵物智慧醫療助手")
    st.subheader("輸入您的觀察紀錄，獲取三方專業分析")
    
    # 初始化session_state
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # 使用者輸入區
    user_input = st.text_area("請輸入您對寵物的觀察紀錄", height=100)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        submit_button = st.button("獲取分析", use_container_width=True)
    with col2:
        clear_button = st.button("清除紀錄", use_container_width=True)
    with col3:
        # 可以添加其他功能按鈕
        pass
    
    # 清除歷史紀錄
    if clear_button:
        st.session_state.history = []
        st.experimental_rerun()
    
    # 處理提交
    if submit_button and user_input:
        with st.spinner("小V、小一和阿寶正在分析中..."):
            # 獲取小V的回應
            v_response = get_ai_response(prompt_v, user_input)
            
            # 獲取小一的回應
            one_response = get_ai_response(prompt_1, user_input)
            
            # 整合前兩個回應給阿寶
            integrated_input = f"""
            寵物觀察紀錄：{user_input}
            
            小V的分析：
            {v_response}
            
            小一的分析：
            {one_response}
            """
            
            # 獲取阿寶的整合回應
            a_response = get_ai_response(prompt_a, integrated_input)
            
            # 將結果添加到歷史紀錄
            st.session_state.history.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "user_input": user_input,
                "v_response": v_response,
                "one_response": one_response,
                "a_response": a_response
            })
    
    # 顯示歷史紀錄
    if st.session_state.history:
        st.markdown("---")
        st.subheader("歷史分析記錄")
        
        for i, record in enumerate(reversed(st.session_state.history)):
            with st.expander(f"記錄 {len(st.session_state.history) - i}: {record['timestamp']} - {record['user_input'][:50]}...", expanded=(i == 0)):
                st.markdown(f"🐾 **您的觀察紀錄**：\n{record['user_input']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"🟡 **小V（獸醫角度）**：\n{record['v_response']}")
                
                with col2:
                    st.markdown(f"🔵 **小一（臨床角度）**：\n{record['one_response']}")
                
                st.markdown(f"🟢 **阿寶（整合建議）**：\n{record['a_response']}")
    
    # 顯示頁腳信息
    st.markdown("---")
    st.markdown("### 關於VetGPT三角系統")
    st.markdown("""
    此系統整合了三個AI專家的視角：
    - 🟡 **小V**：提供結構化的治療節奏建議
    - 🔵 **小一**：從臨床角度補充與提醒
    - 🟢 **阿寶**：整合兩者觀點成具體可執行方案
    
    系統僅作為輔助工具，最終診斷和治療決策應咨詢專業獸醫。
    """)

if __name__ == "__main__":
    main()
