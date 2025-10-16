import streamlit as st
import google.generativeai as genai
import os

# ----------------- 초기 설정 -----------------
# API 키 설정
os.environ["GEMINI_API_KEY"] = "AIzaSyDlOVDHM576b71EbLO5_4L_pZ8UeAFSqRQ"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Streamlit 페이지 설정
st.set_page_config(
    page_title="건설기술 도우미 '아키'",
    page_icon="🤖",
)

# ----------------- 챗봇 페르소나 -----------------
system_prompt = """
너의 이름은 '아키'이고, 중학생들을 위한 건설기술 도우미 챗봇이야.
너의 목표는 학생들이 스스로 생각하고 답을 찾도록 돕는 것이야.
따라서, 절대로 질문에 대한 정답을 직접적으로 알려주면 안 돼.
대신, 학생들이 답을 유추할 수 있도록 친절한 말투로 힌트를 주거나 관련된 질문을 던져줘.
어려운 건설 용어는 반드시 중학생 눈높이에 맞춰 쉬운 비유를 들어 설명해줘.
"""

# ----------------- 모델 초기화 -----------------
model = genai.GenerativeModel(
    "models/gemini-pro-latest",
    system_instruction=system_prompt
)

# ----------------- 세션 상태 관리 -----------------
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ----------------- 웹 화면 구성 -----------------
st.title("건설기술 도우미 '아키' 🤖")
st.caption("무엇이든 물어보세요! 아키가 힌트를 줄게요. 😉")

# 이전 대화 표시
for message in st.session_state.chat.history:
    icon = "🧑‍💻" if message.role == "user" else "🤖"
    with st.chat_message(name=message.role, avatar=icon):
        st.markdown(message.parts[0].text)

# 사용자 입력
if prompt := st.chat_input("아키에게 질문하기..."):
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(prompt)

    response = st.session_state.chat.send_message(prompt)

    with st.chat_message(name="assistant", avatar="🤖"):
        st.markdown(response.text)
